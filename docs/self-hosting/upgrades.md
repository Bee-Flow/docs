# Upgrades

## Server

```bash
docker compose pull beeflow-server
docker compose up -d beeflow-server
```

Database migrations run automatically on boot. To pin to a specific version:

```yaml
services:
  beeflow-server:
    image: ghcr.io/bee-flow/beeflow:0.5.0
```

## Frontend

```bash
cd hive
git pull
npm install
npm run build
# Replace your served dist/
```

Or, if you consume the npm package:

```bash
npm install @beeflow/frontend@latest
```

## Connector

The Nextcloud App Store auto-updates the connector when AppAPI's daily background job runs. To force-update:

1. Open **Apps** in your Nextcloud admin area.
2. Click **Update** on the Bee Flow card.

## Migrations and rollback

Bee Flow ships forward-compatible migrations within a major version. Cross-major upgrades may require a one-shot migration step — those are called out in the [release notes](https://github.com/Bee-Flow/beeflow/releases).

Always back up your Postgres volume before a major upgrade.
