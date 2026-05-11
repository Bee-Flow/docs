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

AppAPI deploys ExApps as Docker containers. Two deployment daemons are supported:

| Daemon | Use when | Trade-off |
|--------|----------|-----------|
| **HaRP** | Production / shared hosting | One container manages every ExApp. Reverse proxy + DNS handled by HaRP. Insecure local registries need explicit trust. |
| **`manual-install`** | Local dev, single host | Uses your host's Docker daemon directly. Easier for debugging — `docker logs` works as you'd expect. |

Configure the daemon at **Administration → AppAPI → Deployment daemons**, or with:

```bash
sudo -u www-data php occ app_api:daemon:register \
  manual_dev \
  "Manual local Docker" \
  manual-install \
  http \
  localhost \
  http://nextcloud
```

Pick the daemon that suits your environment, then test it with `app_api:daemon:test`.

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
