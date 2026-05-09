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
| **`DB_NAME`** | `beeflow` | Database name. |
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

| Variable | Provider | Notes |
|----------|----------|-------|
| `BING_SEARCH_API_KEY` | Microsoft Bing | Web-search agent tool. |
| `TAVILY_API_KEY` | Tavily | Alternative web-search provider. |

## Privacy & DLP

| Variable | Default | Purpose |
|----------|---------|---------|
| `AZURE_PII_ENDPOINT` | (none) | Azure AI Text Analytics endpoint. Falls back to local model if not set. |
| `AZURE_PII_KEY` | (none) | Azure AI Text Analytics key. |
| `AZURE_PII_API_VERSION` | `2023-04-15-preview` | API version. |
| `GUARD_SERVICE_URL` | (none) | Local CPU PII model service (`/pii` endpoint). |
| `AZURE_CONTENT_SAFETY_ENDPOINT` | (none) | Azure Content Safety for moderation. |
| `AZURE_CONTENT_SAFETY_KEY` | (none) | Azure Content Safety key. |
| `LLAMA_GUARD_URL` | (none) | Self-hosted Llama Guard endpoint. Alternative moderation. |
| `PII_DEFAULT_CONFIDENCE` | `0.7` | Default detection confidence (0–1). |
| `PII_MAX_TOKENS_PER_CONVO` | `500` | Cap on placeholder-map size per conversation. |

## Search service (KB)

| Variable | Default | Purpose |
|----------|---------|---------|
| `SEARCH_SERVICE_URL` | (none) | External search-service endpoint. Falls back to local Postgres path. |
| `SEARCH_SERVICE_KEY` | (none) | Optional bearer for the search service. |
| `KB_PER_CHUNK_TOKEN_CAP` | `800` | Token budget per chunk. |
| `KB_GLOBAL_INJECT_TOKEN_CAP` | `4000` | Total tokens injected into the prompt from KB. |
| `KB_DEDUP_THRESHOLD` | `0.85` | Jaccard similarity threshold for chunk dedup. |

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
| `N8N_BASE_URL` | n8n — instance URL |
| `N8N_API_KEY` | n8n |
| `SIGNREQUEST_API_KEY` | SignRequest |
| `FIREFLIES_API_KEY` | Fireflies |
| `GAMMA_API_KEY` | Gamma |
| `WHATSAPP_TWILIO_SID` | WhatsApp (Twilio backend) |
| `WHATSAPP_TWILIO_TOKEN` | WhatsApp |
| `WHATSAPP_FROM_NUMBER` | WhatsApp |

## License

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_LICENSE_KEY` | (empty) | JWT licence. Empty = Community tier. |
| `BEEFLOW_LICENSE_PUBLIC_KEY_PATH` | `license/bundled-public-key.pem` | Override only for testing. |
| `BEEFLOW_LICENSE_REFRESH_URL` | `https://license.beeflow.ai/refresh` | Where Pro+ keys check for revocation. |
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
| `LOG_FORMAT` | `json` | `json` for SIEM, `pretty` for local dev. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | (none) | OpenTelemetry endpoint for traces / metrics. |
| `OTEL_SERVICE_NAME` | `beeflow-server` | OTel service name. |
| `METRICS_ENABLED` | `true` | Exposes `/metrics` (Prometheus format). |
| `METRICS_BASIC_AUTH` | (none) | `user:pass` to protect `/metrics`. |
| `SENTRY_DSN` | (none) | Sentry error reporting. |
| `AUDIT_LOG_RETENTION_DAYS` | `90` | How long guardrail / audit events stay in Postgres. |

## Feature flags

| Variable | Default | Purpose |
|----------|---------|---------|
| `FEATURE_NOTEBOOKS_ENABLED` | `true` | Notebooks page (per-user research workspace). |
| `FEATURE_VOICE_ENABLED` | `true` | Voice features (require Pro+ at runtime). |
| `FEATURE_AGENT_MARKETPLACE` | `true` | Public agent marketplace tab in Studio. |
| `FEATURE_KB_MARKETPLACE` | `true` | Public KB marketplace tab. |
| `FEATURE_SKILLS_ENABLED` | `true` | Skills system (Pro+ at runtime). |
| `FEATURE_AUTOMATIONS_ENABLED` | `true` | Automations (Pro+ at runtime). |

These are `true` by default — set to `false` to hide the UI even for tiers that would otherwise allow it. Use case: test installs, or compliance lockdowns.

## Email (outbound)

| Variable | Default | Purpose |
|----------|---------|---------|
| `SMTP_HOST` | (none) | SMTP server for invitations, password resets, notifications. |
| `SMTP_PORT` | `587` | |
| `SMTP_USER` | (none) | |
| `SMTP_PASS` | (none) | |
| `SMTP_FROM` | `noreply@beeflow.ai` | From address. |
| `SMTP_TLS` | `true` | STARTTLS. |

## Encryption-at-rest

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_ENCRYPTION_KEY` | (none) | 32-byte key for encrypting OAuth tokens / API keys at rest in Postgres. |

## Bee Flow service URL (used by the Nextcloud connector)

| Variable | Default | Purpose |
|----------|---------|---------|
| `BEEFLOW_API_BASE_URL` | `https://api.beeflow.ai` | Set on the **connector** side via `occ app_api:app:setenv`. Override only for staging / on-prem. |
| `BEEFLOW_TENANT_KEY` | `auto` | Connector-side. Literal `auto` means provision automatically. |
