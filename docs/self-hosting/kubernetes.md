# Kubernetes

A Helm chart will be published at [Bee-Flow/helm](https://github.com/Bee-Flow/helm) once stable.

For now, treat the [Docker Compose](docker-compose.md) layout as a reference and translate it to your cluster's preferred patterns.

## Required workloads

- **`beeflow-server`** — Deployment, 1+ replicas, port 3101.
- **`postgres`** — StatefulSet (or external managed Postgres 16+).
- **`redis`** — Deployment or StatefulSet (or managed Redis).

## Required secrets

| Secret | Purpose |
|--------|---------|
| `JWT_SECRET` | Session signing |
| `DB_PASSWORD` | Postgres password |
| `BEEFLOW_LICENSE_KEY` | (Optional) Premium tier license |
| Model provider keys | At least one of Anthropic / OpenAI / Mistral / Azure |

## Status

The chart is on the roadmap. Track progress in [Bee-Flow/helm/issues](https://github.com/Bee-Flow/helm/issues).
