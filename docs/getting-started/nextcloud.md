---
title: Install on Nextcloud
---

# Install on Nextcloud

This page walks an admin through installing the Bee Flow connector via the Nextcloud App Store.

:::info[Requirements]

- Nextcloud 31, 32, 33.0.1+, or 34
- [AppAPI](https://apps.nextcloud.com/apps/app_api) installed and enabled
- A deployment daemon configured (HaRP **or** `manual-install`)
- Admin permissions on the Nextcloud instance
- Outbound HTTPS to `ghcr.io` (image pull) and `server.beeflow.ai` (or your self-hosted Bee Flow server)

:::

## 1. Install AppAPI

If you haven't already:

```bash
sudo -u www-data php occ app:install app_api
sudo -u www-data php occ app:enable app_api
```

Or install **App API** from the **Apps** page in the Nextcloud admin UI.

## 2. Configure a deployment daemon

AppAPI deploys ExApps as Docker containers. Pick the daemon that matches your Nextcloud setup:

| Your setup | Daemon | One-time command |
|---|---|---|
| **Vanilla Nextcloud** (self-managed bare-metal or VM with Docker) | `docker-install` | See [§2a](#2a-vanilla-nextcloud) below |
| **Nextcloud All-in-One** (AIO master container) | `docker-install` (auto-configured) | Usually nothing — see [§2b](#2b-nextcloud-all-in-one) |
| **Behind reverse proxy / NAT** (NC not directly reachable from the public internet) | `docker-install` + `BEEFLOW_NC_PUBLIC_URL` | See [§2c](#2c-behind-reverse-proxy-or-nat) |
| **Multi-tenant / shared hosting** | **HaRP** | See [HaRP setup guide](https://docs.nextcloud.com/server/latest/admin_manual/app_api/harp.html) |

### 2a. Vanilla Nextcloud

Register a daemon that talks to the host's Docker socket. Run this once on the server hosting Nextcloud:

```bash
sudo -u www-data php occ app_api:daemon:register \
  docker_local \
  "Local Docker" \
  docker-install \
  http \
  localhost \
  http://nextcloud
```

Verify it works:

```bash
sudo -u www-data php occ app_api:daemon:list
sudo -u www-data php occ app_api:daemon:test docker_local
```

The Docker socket must be readable by `www-data`. On most Nextcloud Docker images this means adding `www-data` to the host's `docker` group inside the Nextcloud container:

```bash
docker exec <nextcloud-container> bash -c "
  groupadd -g $(stat -c '%g' /var/run/docker.sock) docker-host 2>/dev/null || true
  usermod -aG docker-host www-data
"
```

### 2b. Nextcloud All-in-One

Nextcloud AIO ships AppAPI pre-installed and exposes a docker-socket-proxy on `nextcloud-aio-docker-socket-proxy:2375`. The daemon is **already registered** in most AIO releases — verify with:

```bash
sudo docker exec --user www-data nextcloud-aio-nextcloud \
  php occ app_api:daemon:list
```

If the list is empty (older AIO image), register manually:

```bash
sudo docker exec --user www-data nextcloud-aio-nextcloud \
  php occ app_api:daemon:register \
  docker_aio \
  "AIO Docker socket proxy" \
  docker-install \
  http \
  nextcloud-aio-docker-socket-proxy:2375 \
  http://nextcloud-aio-nextcloud
```

### 2c. Behind reverse proxy or NAT

If your Nextcloud is reached via a public URL (e.g. `https://cloud.example.com`) but lives on a private network, Bee Flow Cloud needs a publicly resolvable callback URL for user-sync webhooks. Set `BEEFLOW_NC_PUBLIC_URL` on the ExApp **before** the install so the bootstrap handshake registers the right callback:

```bash
sudo -u www-data php occ app_api:app:setenv bee_flow \
  BEEFLOW_NC_PUBLIC_URL "https://cloud.example.com"
```

If you forget this, the install still completes but user-sync webhooks fail silently and Bee Flow shows a yellow "user sync degraded" banner. You can set it any time after the install and run `app_api:app:redeploy bee_flow` to apply.

## 3. Install Bee Flow from the App Store

1. Open **Apps** in your Nextcloud admin area.
2. Search **Bee Flow** in the **AI** category.
3. Click **Install**.

Or via CLI:

```bash
sudo -u www-data php occ app_api:app:register \
  bee_flow \
  --info-xml https://raw.githubusercontent.com/Bee-Flow/connector/main/appinfo/info.xml
```

AppAPI pulls the connector image from `ghcr.io/bee-flow/connector:latest` and starts a container next to your Nextcloud. The first install typically takes **30–60 seconds** end-to-end on a stock VPS.

![App Store listing](../img/screenshots/getting-started/nextcloud-app-store/)

## 4. Verify the install

After AppAPI reports the install as successful:

```bash
# Heartbeat from Nextcloud's perspective
sudo -u www-data php occ app_api:app:heartbeat bee_flow
# → {"status":"ok"}

# Direct heartbeat from the host (if reachable)
curl http://localhost:23000/heartbeat
# → {"status":"ok"}

# Container logs
docker logs nc_app_bee_flow --tail 50
# → [Bee Flow] Init complete (5 events registered)
```

A **bee icon** should now appear in your Nextcloud top bar.

![Top-bar icon](../img/screenshots/getting-started/nextcloud-topbar/)

## 5. First-time consent

The first time **each user** opens Bee Flow they see a privacy-disclosure modal. Read, then **I agree — start Bee Flow**. Acceptance is recorded server-side so the modal never reappears for that user (unless the consent text version changes).

## 6. First-time admin wizard

The first time the **organisation admin** opens Bee Flow, a 4-step wizard runs covering user-sync mode, default integrations, privacy shield level, and an optional licence key. Other users see a "Setup in progress" screen until the admin finishes.

[Continue: First-run wizard walk-through →](wizard.md)

## Updating the connector

AppAPI auto-checks for updates daily. To force-update:

1. **Apps → Updates** in the Nextcloud admin area.
2. Click **Update** on the Bee Flow card.

Or:

```bash
sudo -u www-data php occ app_api:app:update bee_flow
```

[More about upgrades →](../self-hosting/upgrades.md)

## Uninstalling

```bash
sudo -u www-data php occ app_api:app:unregister bee_flow
```

This stops the container, removes it, and cleans up the AppAPI registration. The Bee Flow tenant is **not** deleted automatically — your data on the Bee Flow server (or hosted SaaS) stays until you delete the organisation explicitly via **Settings → Organisation → Danger zone**.

## Troubleshooting

If the install hangs, fails, or the heartbeat doesn't return: see [Connector → Troubleshooting](../connector/troubleshooting.md). The most common causes are:

- AppAPI's deployment daemon can't pull from `ghcr.io` (firewall / DNS)
- Port 23000 already taken on the host
- Nextcloud 33.0.0 (broken events listener — upgrade to 33.0.1+)
- HaRP doesn't trust a local insecure registry (dev-only)
