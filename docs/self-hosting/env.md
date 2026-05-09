# Environment variables

All configuration is via environment variables. The full list lives in [`server/.env.example`](https://github.com/Bee-Flow/beeflow/blob/main/.env.example) — this page covers the most-used ones.

## Core

| Variable | Default | Purpose |
|----------|---------|---------|
| `PUBLIC_URL` | `http://localhost:3101` | The public URL users hit. |
| `JWT_SECRET` | — (required) | Random 64+ char string used to sign session JWTs. |
| `PORT` | `3101` | HTTP port the server listens on. |
| `LOG_LEVEL` | `info` | `debug` / `info` / `warn` / `error`. |

## Database

| Variable | Default | Purpose |
|----------|---------|---------|
| `DB_HOST` | `postgres` | Postgres host. |
| `DB_PORT` | `5432` | Postgres port. |
| `DB_NAME` | `beeflow` | Database name. |
| `DB_USER` | `beeflow` | Database user. |
| `DB_PASSWORD` | — (required) | Database password. |

## Redis

| Variable | Default | Purpose |
|----------|---------|---------|
| `REDIS_URL` | `redis://redis:6379` | Optional but strongly recommended for sessions/rate-limits. |

## Model providers

Set at least one:

| Variable | Provider |
|----------|----------|
| `ANTHROPIC_API_KEY` | Anthropic Claude |
| `OPENAI_API_KEY` | OpenAI |
| `MISTRAL_API_KEY` | Mistral |
| `AZURE_OPENAI_ENDPOINT` + `AZURE_OPENAI_KEY` | Azure OpenAI |

## License

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_LICENSE_KEY` | (none) | JWT license key. Empty = Community tier. |

## Nextcloud connector pairing

| Variable | Default | Purpose |
|----------|---------|---------|
| `NC_CONNECTOR_HMAC_SECRET` | (auto) | Shared secret for `/nc/*` HMAC reverse-proxy. |
