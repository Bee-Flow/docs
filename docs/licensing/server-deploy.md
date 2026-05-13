---
title: Deploying the License Server
description: Production runbook for license.beeflow.ai on Scaleway.
---

# Deploying the Beeflow License Server

This runbook covers a fresh production install of the license server on a
Scaleway VPS, terminated by Caddy with Let's Encrypt and persisted in a
managed Postgres instance.

The license server is the single source of truth for JWT issuance, refresh
and revocation. The main Bee-Flow app calls it from the Stripe webhook
after a paid checkout and pings `/v1/refresh` once per hour for monthly
licenses. Without it, the SaaS still works via the subscription-fallback
in `getTierForOrg`, but customers do not receive a portable license blob.

## 1. Provision

- Scaleway DEV1-S (or larger) — 2 vCPU, 2 GB RAM is plenty.
- Scaleway Database for PostgreSQL — smallest tier; create a database
  `beeflow_license` and a dedicated role.
- DNS A-record `license.beeflow.ai` → VPS public IP.
- Open inbound ports 22 (your IP only), 80, 443.

## 2. Generate the keypair

Run **once** on a workstation you trust. Do not generate keys on the VPS
itself; you want the private key handled deliberately.

```bash
git clone <repo>
cd Bee-Flow-AI/license-server
npm ci
node scripts/generate-keypair.js
```

This writes `keys/private.pem` and `keys/public.pem`. Then:

1. Copy `keys/public.pem` into the main Bee-Flow distribution:
   ```bash
   cp keys/public.pem ../server/license/bundled-public-key.pem
   ```
   Commit the resulting `bundled-public-key.pem` to git. It is whitelisted in
   `.gitignore` so the `*.pem` rule does not exclude it.

2. Upload `keys/private.pem` to **Scaleway Secret Manager** as
   `beeflow/license-server/private-key`. Do not place it in the repo. Do not
   email it. Do not paste it into chat. The dev keypair from
   `node scripts/issue-test-keys.js` MUST NOT be reused in production.

## 3. Install the service on the VPS

```bash
# As root or via sudo
adduser --system --group --home /srv/beeflow-license beeflow
mkdir -p /srv/beeflow-license/keys
chown -R beeflow:beeflow /srv/beeflow-license

# Pull the repo into a release dir
sudo -u beeflow git clone <repo> /srv/beeflow-license/app
cd /srv/beeflow-license/app/license-server
sudo -u beeflow npm ci --omit=dev

# Fetch the private key from Secret Manager into the home dir
scw secret-manager secret access-by-name name=beeflow/license-server/private-key \
    > /srv/beeflow-license/keys/private.pem
chmod 0600 /srv/beeflow-license/keys/private.pem
chown beeflow:beeflow /srv/beeflow-license/keys/private.pem
```

## 4. Environment file

`/etc/beeflow-license.env` (mode `0640`, owned by `root:beeflow`):

```env
NODE_ENV=production
PORT=4400
LICENSE_DB_URL=postgresql://beeflow_license:CHANGE_ME@<pg-host>:5432/beeflow_license?sslmode=require
LICENSE_PRIVATE_KEY_FILE=/srv/beeflow-license/keys/private.pem
LICENSE_API_KEY=<64-byte hex from `openssl rand -hex 32`>
LICENSE_ISSUER=license.beeflow.ai
LICENSE_REFRESH_RATE_PER_MIN=120
LICENSE_STRIPE_VERIFY=true
STRIPE_SECRET_KEY=sk_live_...
TRUST_PROXY=loopback
```

Save the `LICENSE_API_KEY` value — it must match `LICENSE_ISSUE_API_KEY` on
the main app.

## 5. systemd unit

`/etc/systemd/system/beeflow-license.service`:

```ini
[Unit]
Description=Beeflow License Server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=beeflow
Group=beeflow
WorkingDirectory=/srv/beeflow-license/app/license-server
EnvironmentFile=/etc/beeflow-license.env
ExecStart=/usr/bin/node index.js
Restart=on-failure
RestartSec=5s
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/srv/beeflow-license

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now beeflow-license
journalctl -u beeflow-license -f
```

## 6. Caddy reverse proxy with TLS

`/etc/caddy/Caddyfile`:

```caddyfile
license.beeflow.ai {
    encode zstd gzip
    reverse_proxy 127.0.0.1:4400
    log {
        output file /var/log/caddy/license.log
        format json
    }
}
```

```bash
systemctl reload caddy
```

Test:

```bash
curl -fsS https://license.beeflow.ai/v1/health
```

## 7. Wire the main app

On the production main app (Scaleway 51.15.201.69), set in
`/srv/beeflow/server/.env`:

```env
LICENSE_PUBLIC_KEY_FILE=/srv/beeflow/server/license/bundled-public-key.pem
LICENSE_ISSUE_URL=https://license.beeflow.ai/v1/issue
LICENSE_ISSUE_API_KEY=<same value as LICENSE_API_KEY above>
LICENSE_REFRESH_URL=https://license.beeflow.ai/v1/refresh
```

Restart the main app. The next paid Stripe checkout will mint a real JWT
that the customer can also paste into another instance.

## 8. End-to-end verification

1. `curl -fsS https://license.beeflow.ai/v1/health` returns `{"ok":true}`.
2. Issue a test license via the main app's Stripe webhook (use a test card,
   then refund).
3. Confirm a row exists in `licenses` on the license-server database.
4. Confirm a `license_keys` row exists in the main app DB and
   `/api/license/status` returns `source: 'license_key'`.
5. Tail `audit_events`:
   ```sql
   SELECT ts, action, license_id, actor_ip, result
     FROM audit_events ORDER BY ts DESC LIMIT 10;
   ```
6. Revoke the test license via `POST /v1/revoke` (or from the main app's
   admin UI). After the next refresh tick, the main app reports tier=`community`.

## 9. Key rotation (future)

To rotate the signing keypair without downtime:

1. Generate a new keypair on a workstation.
2. Add both old and new keys to the main app's bundled public keys (this
   requires the JWKS endpoint, which is a Phase 3 enhancement).
3. Set `LICENSE_API_KEYS=<old>,<new>` on the license server temporarily.
4. Roll the private key in Secret Manager and reload systemd.
5. After the longest license lifetime expires (typically yearly), drop the
   old public key.

## 10. Backups

- Scaleway Database backups run nightly by default. Verify retention is at
  least 30 days for the `beeflow_license` instance.
- The private key in Secret Manager is versioned automatically.
- Audit events should be archived off-host quarterly if customer count or
  refresh frequency makes the table grow beyond a few hundred MB.
