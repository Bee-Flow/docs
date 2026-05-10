---
title: Upgrades
---

# Upgrades

## Version skew policy

Bee Flow ships forward-compatible migrations within a major version (e.g. `0.x.y`). Cross-major upgrades may require a one-shot migration step — those are called out explicitly in the [release notes](https://github.com/Bee-Flow/beeflow/releases).

| Component | Compatibility |
|-----------|---------------|
| Server ↔ Frontend | Same minor version recommended; one minor of skew tolerated. |
| Server ↔ Connector | Connector is independently versioned, all 0.x connectors talk to all 0.x servers. |
| Server ↔ Postgres | Postgres 16+. Earlier versions lack required SQL features. |
| Server ↔ Redis | Redis 6.2+ (any 7.x recommended). |

## Server upgrade

### Docker Compose

```bash
docker compose pull beeflow-server
docker compose up -d beeflow-server
```

Database migrations run automatically on boot. You'll see them in the log:

```
[Migrations] Applying 0042_user_schema.sql...
[Migrations] Applied 0042 (1.2s)
```

If a migration fails, the server refuses to start. Check the log, fix the cause (usually a permissions issue on Postgres), and restart.

### Pinning to a specific version

```yaml
services:
  beeflow-server:
    image: ghcr.io/bee-flow/beeflow:0.5.0
```

### Kubernetes

```bash
kubectl set image deployment/beeflow-server server=ghcr.io/bee-flow/beeflow:0.5.0
kubectl rollout status deployment/beeflow-server
```

The readiness probe gates traffic until migrations finish.

## Frontend upgrade

If you build from source:

```bash
cd hive
git fetch && git checkout v0.5.0
npm install
npm run build
sudo cp -r dist/* /var/www/beeflow-frontend/
```

If you consume the npm package:

```bash
npm install @beeflow/frontend@0.5.0
```

The frontend is a static bundle — pure file replace, no service restart needed.

## Connector upgrade

The Nextcloud App Store auto-checks for connector updates daily. To force-update:

1. Open **Apps → Updates** in the Nextcloud admin area.
2. Click **Update** on the Bee Flow card.

Or via CLI:

```bash
sudo -u www-data php occ app_api:app:update bee_flow
```

Pin to a specific connector version:

```bash
sudo -u www-data php occ app_api:app:update bee_flow --image-tag 0.2.0
```

## Blue/green for zero downtime

For Pro+ deployments wanting zero-downtime upgrades:

1. Stand up a second `beeflow-server` deployment (`-blue` and `-green`) sharing the same Postgres + Redis.
2. Point the load balancer at one colour at a time.
3. Migrate by:
   - Pull new image into the inactive colour.
   - Run a smoke test against it via a private endpoint.
   - Flip the LB.
   - Pull the same image into the previous colour for next round.

The DB schema is forward-compatible within a minor version, so old + new can coexist briefly.

## Rollback procedure

:::warning[Always back up Postgres first]

`docker exec -t $(docker compose ps -q postgres) pg_dump -U beeflow -d beeflow -Fc > /backups/pre-upgrade.dump` before any cross-major upgrade.

:::

Cross-major rollback is not supported — schema changes are forward-only. To roll back:

1. Restore the Postgres backup taken before the upgrade.
2. Re-deploy the previous server image.
3. Re-deploy the previous frontend.

Within a minor version, you can downgrade by switching the image tag back without DB rollback.

## Major-version upgrades (e.g. 0.x → 1.0)

When a 1.0 or future major lands, the release notes will explicitly say:

- Breaking config changes (renamed env vars, removed defaults)
- One-shot migrations (run a CLI before / after the deploy)
- Min Postgres / Node versions

Always read the upgrade guide for each major before flipping.

## Telemetry on upgrade health

Enable Prometheus metrics with `METRICS_ENABLED=true` and watch:

- `beeflow_migrations_applied_total` — bumps on each successful migration
- `beeflow_http_requests_total{status="5xx"}` — should stay flat across the upgrade
- `beeflow_db_pool_in_use` — spikes are normal during migrations, should drop after

If 5xx rate sustains > 1% for >2 min after upgrade, roll back.

## Connector + server version pairing

Both ship 0.x. A 0.5 server speaks to 0.4 and 0.5 connectors transparently. Across a 1.0 boundary, upgrade the server first (it stays compatible with the previous connector), then bump the connector via the App Store.
