# Nextcloud connector

The connector is the Nextcloud ExApp that bridges your Nextcloud to the Bee Flow service. It runs as a Docker container next to your Nextcloud, deployed and managed by [AppAPI](https://apps.nextcloud.com/apps/app_api).

Source: [github.com/Bee-Flow/connector](https://github.com/Bee-Flow/connector). Licensed AGPL-3.0-or-later.

## What it does

- Serves the Bee Flow web UI (a static React bundle) inside your Nextcloud.
- Authenticates users via your existing Nextcloud session — no second login.
- Reverse-proxies API calls from the SPA to the Bee Flow service.
- Reverse-proxies callback calls from the Bee Flow service back to Nextcloud's APIs (Files, Mail, Calendar, etc.) using HMAC-signed requests.
- Listens for Nextcloud events (user created, group added) and syncs changes to your Bee Flow tenant.

## Deeper reading

- [Architecture](architecture.md) — request flow diagrams.
- [Permissions & scopes](permissions.md) — exactly what data leaves your tenant.
- [Privacy & data flow](privacy.md) — what's sent to the Bee Flow service and when.
- [Troubleshooting](troubleshooting.md) — install hangs, heartbeat failures, log locations.
