# Self-hosting

Bee Flow's server and frontend are open-source under the Sustainable Use Licence. You can run the entire stack on your own infrastructure for free, for your own organisation.

## Components you'll run

| Component | Image / package |
|-----------|-----------------|
| Bee Flow server | `ghcr.io/bee-flow/beeflow:latest` |
| Bee Flow frontend | `@beeflow/frontend` (npm) or build from [Bee-Flow/hive](https://github.com/Bee-Flow/hive) |
| PostgreSQL 16+ | `postgres:16-alpine` |
| Redis (recommended) | `redis:7-alpine` |
| Bee Flow Nextcloud connector (optional) | Installed via NC App Store |

## Pick your deploy target

- [Docker Compose](docker-compose.md) — single-host, simplest.
- [Kubernetes](kubernetes.md) — Helm chart, multi-node.
- [Environment variables](env.md) — all `BEEFLOW_*` knobs.
- [Upgrades](upgrades.md) — how to bump versions safely.
