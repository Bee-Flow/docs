---
title: Environment variables
---

# Environment variables

Every variable the Bee Flow server reads, grouped by area. Defaults are shown where they exist; **bold** vars are required for that area to work.

The full list also lives in [`.env.example`](https://github.com/Bee-Flow/beeflow/blob/main/.env.example) in the server repo.

## Core / runtime

| Variable | Default | Purpose |
|----------|---------|---------|
| **`PUBLIC_URL`** | `http://localhost:3101` | The public URL users hit. Used for OAuth redirect, email links. |
| **`JWT_SECRET`** | — | 64+ char random string. Signs session JWTs. |
| `PORT` | `3101` | HTTP port the server listens on. |
| `LOG_LEVEL` | `info` | `trace` / `debug` / `info` / `warn` / `error`. |
| `NODE_ENV` | `production` | Standard Node convention. |
| `TIMEZONE` | `UTC` | Default timezone for cron schedules and date display. |
| `BEEFLOW_DATA_DIR` | `/data` | Directory for any small on-disk state (rare; most state is in Postgres). |
| `BEEFLOW_REQUEST_BODY_LIMIT` | `10mb` | Max JSON body. Raise for large KB document uploads. |

## Database

| Variable | Default | Purpose |
|----------|---------|---------|
| **`DB_HOST`** | `postgres` | Postgres host. |
| **`DB_PORT`** | `5432` | Postgres port. |
| **`DB_NAME`** | `beeflow_core` | Primary database name. The Compose setup also creates `beeflow_tasks` and `monitoring_db` on the same instance — see [Docker Compose → Three databases](docker-compose.md#three-databases-not-one). |
| `DATABASE_URL` | derived from `DB_*` | Override for the productivity-tasks DB. Default points at `beeflow_tasks`. |
| `MONITORING_DATABASE_URL` | derived from `DB_*` | Override for the monitoring DB. Default points at `monitoring_db`. |
| **`DB_USER`** | `beeflow` | Database user. |
| **`DB_PASSWORD`** | — | Database password. |
| `DB_SSL` | `false` | `true` to require TLS. Use for managed Postgres. |
| `DB_POOL_MAX` | `10` | Max connections from each server replica. |
| `DB_POOL_IDLE_TIMEOUT_MS` | `30000` | Close idle connections after this many ms. |

## Redis

| Variable | Default | Purpose |
|----------|---------|---------|
| `REDIS_URL` | (none) | E.g. `redis://redis:6379`. Required for >1 server replica. |
| `REDIS_TLS` | `false` | Set to `true` for `rediss://` connections. |
| `REDIS_KEY_PREFIX` | `bf:` | Prefix to namespace keys. Useful when sharing a Redis instance. |

## Model providers

Set **at least one**. Agents pick whichever is configured for their model.

| Variable | Provider | Notes |
|----------|----------|-------|
| `ANTHROPIC_API_KEY` | Anthropic Claude | Recommended default. |
| `ANTHROPIC_BASE_URL` | (override) | For self-hosted Claude proxy. |
| `OPENAI_API_KEY` | OpenAI | GPT-4.x, GPT-5. |
| `OPENAI_BASE_URL` | (override) | OpenAI-compatible endpoints (LiteLLM, vLLM, etc.). |
| `MISTRAL_API_KEY` | Mistral | Hosted Mistral. |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI | E.g. `https://my-aoai.openai.azure.com`. |
| `AZURE_OPENAI_KEY` | Azure OpenAI | API key. |
| `AZURE_OPENAI_API_VERSION` | `2024-08-01-preview` | API version string. |
| `AZURE_OPENAI_DEPLOYMENT_GPT4` | (deployment name) | Maps the GPT-4 model alias to your deployment. |
| `AZURE_OPENAI_DEPLOYMENT_EMBED` | (deployment name) | For Azure-hosted embeddings. |
| `OLLAMA_BASE_URL` | (none) | E.g. `http://localhost:11434`. Self-hosted local models. |
| `VOXTRAL_API_KEY` | Voxtral | Voice (STT + TTS). |
| `ELEVENLABS_API_KEY` | ElevenLabs | TTS, music, sound effects. |
| `DEEPGRAM_API_KEY` | Deepgram | Alternative STT provider. |
| `MISTRAL_TRANSCRIPTION_KEY` | Mistral | Transcription pipeline. |

## Web search

The web-search provider is picked in **Admin → Integrations → Zoeken**. API keys live in the admin DB (encrypted), **not** in `.env`. Set the keys in the admin UI:

| Provider | Where to set |
|---|---|
| Self-hosted Agent Search + Serper | Admin → Integrations → Zoeken (Serper key) + `SEARCH_SERVICE_URL` env var below |
| Cloud-only (Serper + provider APIs) | Admin → Integrations → Zoeken (Serper key only) |
| Azure Bing Web Search | Admin → Integrations → Zoeken (Bing key + market) |

See [Web search integration](../integrations/web-search.md) for the full setup.

## Privacy Shield

| Variable | Default | Purpose |
|----------|---------|---------|
| `AZURE_PII_ENDPOINT` | (none) | Azure AI Text Analytics endpoint. Falls back to in-process Transformers.js detector + then to optional `PII_SERVICE_URL` if set. |
| `AZURE_PII_KEY` | (none) | Azure AI Text Analytics key. |
| `PII_SERVICE_URL` | (none — opt-in) | Optional Python sidecar running GLiNER multi PII v1 (Apache 2.0). Only probed when explicitly set; otherwise the in-process Transformers.js detector handles the CPU path. |
| `GUARD_SERVICE_URL` | (none — opt-in) | Optional sidecar health probe for `/api/guard/health`. Returns `not-configured` when unset. Moderation now goes via Azure Content Safety natively. |
| `AZURE_CONTENT_SAFETY_ENDPOINT` | (none) | Azure Content Safety for moderation. The default moderation provider when configured. |
| `AZURE_CONTENT_SAFETY_KEY` | (none) | Azure Content Safety key. |

## Search service (KB)

The KB pipeline can run entirely **in-process** (chunking + pgvector + RRF + cross-encoder rerank) — no GPU service required. Pick **Local** under Admin → AI Configuratie → Limits & Self-host. The remote search-service is opt-in via `SEARCH_SERVICE_URL`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SEARCH_SERVICE_URL` | (none — opt-in) | External GPU-backed search-service endpoint. When set, KB ingestion / search routes to it for users who pick `kb_provider = remote` in admin. Leave empty for fully local KB. |
| `RERANKER_URL` | (none — opt-in) | vLLM cross-encoder sidecar. Used as a tier between Azure Cohere and the in-process CPU reranker. Most self-hosted deployments don't need it. |
| `EMBED_API_URL` | (none — legacy) | Self-hosted GPU embedding service (BGE-M3). Memory store falls back to it only when no provider and no CPU embedder are available. |

## Embeddings

Global embedding model is picked in **Admin → AI Configuratie → Embeddings**. Used for KB ingestion, KB query, memory store, and as the default embed for web-search inference. The Web Search Inference tab can override per-feature.

The CPU fallback (`@huggingface/transformers` + `Xenova/multilingual-e5-small`, MIT, 384-dim) loads automatically when no provider is configured. No env var to set.

## Reranking

| Method | How |
|---|---|
| Azure Cohere reranker | Admin → AI Configuratie → API Sleutels → Azure Cohere Reranker |
| CPU cross-encoder | Admin → AI Configuratie → Limits & Self-host → toggle `cpu_reranker_enabled`. Uses `Xenova/bge-reranker-base` (MIT, ~280 MB), loaded in-process |
| Local GPU vLLM sidecar | Set `RERANKER_URL` env var. Skipped when CPU reranker is enabled. |
| LLM-as-rerank | Admin → AI Configuratie → Web Search Inference → method = "Provider model" + pick a chat model |

## OAuth providers

For each provider you enable, register an OAuth app with redirect URI `https://<your-host>/auth/<provider>/callback`.

| Variable | Provider | Purpose |
|----------|----------|---------|
| `OAUTH_GOOGLE_CLIENT_ID` | Google | Gmail / Calendar / Drive / Docs / Keep / Contacts / Groups |
| `OAUTH_GOOGLE_CLIENT_SECRET` | Google | |
| `OAUTH_MICROSOFT_CLIENT_ID` | Microsoft | Outlook / MS Calendar / Contacts / OneDrive |
| `OAUTH_MICROSOFT_CLIENT_SECRET` | Microsoft | |
| `OAUTH_MICROSOFT_TENANT` | Microsoft | `common` (multi-tenant) or your tenant ID |
| `OAUTH_GITHUB_CLIENT_ID` | GitHub | GitHub tools |
| `OAUTH_GITHUB_CLIENT_SECRET` | GitHub | |
| `OAUTH_NEXTCLOUD_CLIENT_ID` | Nextcloud | Standalone NC OAuth (when not using the connector) |
| `OAUTH_NEXTCLOUD_CLIENT_SECRET` | Nextcloud | |
| `OAUTH_NEXTCLOUD_BASE_URL` | Nextcloud | E.g. `https://nc.example.com` |
| `OAUTH_LINKEDIN_CLIENT_ID` | LinkedIn | LinkedIn read-only |
| `OAUTH_LINKEDIN_CLIENT_SECRET` | LinkedIn | |

## API-key integrations

| Variable | Integration |
|----------|-------------|
| `YOUTRACK_BASE_URL` | YouTrack — instance URL |
| `YOUTRACK_API_TOKEN` | YouTrack |
| `SIGNREQUEST_API_KEY` | SignRequest |
| `FIREFLIES_API_KEY` | Fireflies |
| `GAMMA_API_KEY` | Gamma |

## License

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_LICENSE_KEY` | (empty) | JWT licence. Empty = Community tier. |
| `BEEFLOW_LICENSE_PUBLIC_KEY_PATH` | `license/bundled-public-key.pem` | Override only for testing. |
| `BEEFLOW_LICENSE_REFRESH_URL` | `https://license.beeflow.nl/refresh` | Where Pro+ keys check for revocation. |
| `BEEFLOW_LICENSE_REFRESH_INTERVAL_HOURS` | `24` | How often to re-check. |

## Nextcloud connector pairing

| Variable | Default | Purpose |
|----------|---------|---------|
| `NC_CONNECTOR_HMAC_SECRET` | (auto-generated per tenant) | Shared secret for the `/nc/*` HMAC reverse proxy. Stored in DB; you usually don't set this manually. |
| `NC_CONNECTOR_BOOTSTRAP_TOKEN_TTL` | `300` | Seconds the bootstrap handshake token is valid. |

## Observability

| Variable | Default | Purpose |
|----------|---------|---------|
| `LOG_LEVEL` | `info` | See above. |
| `AUDIT_LOG_RETENTION_DAYS` | `90` | How long guardrail / audit events stay in Postgres. |
| `SENTRY_DSN` | (none) | Sentry error reporting (if a Sentry SDK is wired in your fork). |

A global Prometheus `/metrics` endpoint and OpenTelemetry exporter (`OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME`, `METRICS_ENABLED`, `METRICS_BASIC_AUTH`) are on the roadmap but **not wired today**. See [Reference → Telemetry](../reference/telemetry.md) for the current state.

## Feature flags

Most feature gating in Bee Flow is **licence-driven**, not env-driven. The server enforces premium features via `requireLicenseFeature(name)` middleware against the active org's tier (see [Licensing → Tiers](../licensing/tiers.md)).

A handful of features can additionally be toggled per-server via env:

| Variable | Default | Purpose |
|----------|---------|---------|
| `ENABLE_TASKS` | `true` | Productivity tasks/projects routes (`/api/projects`, `/api/reminders`, `/api/ai-tasks`). |
| `ENABLE_MONITORING` | `true` | Monitoring DB writes for the analytics dashboards. |
| `ENABLE_MEETING_NOTES` | `true` | Meeting-notes UI surface (still requires the `meeting_notes` licence feature to use). |
| `ENABLE_TEMPLATES` | `true` | Template gallery in Studio. |

Setting any of these to `false` hides the corresponding UI surface even on tiers that would otherwise allow it. Use case: test installs, compliance lockdowns. Other "feature flag"-looking vars (e.g. `FEATURE_NOTEBOOKS_ENABLED`, `FEATURE_SKILLS_ENABLED`) are reserved for future use and ignored today.

## Email (outbound)

| Variable | Default | Purpose |
|----------|---------|---------|
| `SMTP_HOST` | (none) | SMTP server for invitations, password resets, notifications. |
| `SMTP_PORT` | `587` | |
| `SMTP_USER` | (none) | |
| `SMTP_PASS` | (none) | |
| `SMTP_FROM` | `noreply@beeflow.nl` | From address. |
| `SMTP_TLS` | `true` | STARTTLS. |

## Encryption-at-rest

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_ENCRYPTION_KEY` | (none) | 32-byte key for encrypting OAuth tokens / API keys at rest in Postgres. |

## Bee Flow service URL (used by the Nextcloud connector)

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_API_BASE_URL` | `https://server.beeflow.nl` | Set on the **connector** side via `occ app_api:app:setenv`. Override only for staging / on-prem. |
| `BEEFLOW_TENANT_KEY` | `auto` | Connector-side. Literal `auto` means provision automatically. |
