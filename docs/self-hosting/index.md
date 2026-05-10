# Self-hosting

Bee Flow's server and frontend are open-source under the Sustainable Use Licence. You can run the entire stack on your own infrastructure for free, for your own organisation.

## What you'll run

| Component | Image / package | Required? |
|-----------|-----------------|:---------:|
| Bee Flow server | `ghcr.io/bee-flow/beeflow:latest` | ✅ |
| Bee Flow frontend (`hive`) | `@beeflow/frontend` (npm) or build from source | ✅ |
| PostgreSQL 16+ | `postgres:16-alpine` | ✅ |
| Redis 7 | `redis:7-alpine` | recommended |
| Bee Flow Nextcloud connector | NC App Store (`bee_flow`) | optional |
| Guard service (PII detection) | `ghcr.io/bee-flow/guard-service:latest` | optional |
| Search service (KB ingestion + reranking) | `ghcr.io/bee-flow/search-service:latest` | optional |

The minimum useful deployment is **server + Postgres**. Add Redis as soon as you scale to >1 server replica or >50 concurrent users.

## Stack diagram

```
                Browser
                   │
                   ▼
       ┌──────────────────────┐
       │  Reverse proxy       │  Caddy / Nginx / Traefik / Cloudflare
       │  ─ TLS termination   │
       │  ─ Path routing      │
       └──────────┬───────────┘
                  │
       ┌──────────┼─────────────────┐
       │          │                 │
       ▼          ▼                 ▼
  ┌──────┐   ┌──────────┐     ┌────────────┐
  │ hive │   │ beeflow  │ ◀───│ bee_flow   │ (Nextcloud connector,
  │ /    │   │ /api/    │     │ ExApp      │  optional, same network)
  │ /app │   │ /auth/   │     └────────────┘
  └──────┘   └─────┬────┘
                   │
       ┌───────────┼──────────────┐
       │           │              │
       ▼           ▼              ▼
  ┌──────────┐ ┌────────┐  ┌─────────────────┐
  │ Postgres │ │ Redis  │  │ guard / search  │
  │  16      │ │  7     │  │ services        │
  └──────────┘ └────────┘  └─────────────────┘
```

## Minimum and recommended hardware

| | Minimum | Recommended | Heavy use |
|---|---|---|---|
| **CPU** | 2 cores | 4 cores | 8 cores |
| **RAM** | 4 GB | 8 GB | 16+ GB |
| **Disk** | 10 GB | 50 GB | 200+ GB (KB) |
| **Postgres** | 1 GB RAM | 2 GB | 4 GB |
| **Network** | 100 Mbps | 1 Gbps | 1 Gbps + |

The server is stateless when Redis is configured — scale horizontally. Postgres carries all durable state (users, agents, conversations, KB chunks, automation runs, audit log).

## Pick your deploy target

<div className="bf-grid">

-    [Docker Compose](docker-compose.md)

    Single host, simplest. Production-ready for most small/mid orgs.

-    [Kubernetes](kubernetes.md)

    Multi-node, Helm chart in progress. Use the manual manifests until then.

-    [Environment variables](env.md)

    The full reference for every `BEEFLOW_*` and dependency knob.

-    [Upgrades](upgrades.md)

    Version skew policy, migration safety, rollback procedure.

</div>

## Supported deploy targets

| Target | Status | Notes |
|--------|:------:|-------|
| Docker Compose (single host) | ✅ | Recommended for self-hosters. |
| Kubernetes (manual manifests) | ✅ | Helm chart is on the roadmap. |
| Coolify | ✅ | `deploy/coolify.json` in the server repo. |
| Kamal | ✅ | Standard Docker image works. |
| Render / Fly / Railway | ✅ | Treat the server like any Node service, mount Postgres + Redis. |
| Vercel / Netlify (frontend only) | ✅ | Static `dist/` from `hive` builds anywhere. |
| Cloudflare Pages (frontend only) | ✅ | Same. |
| Bare-metal (systemd) | ⚠️ | Works but unsupported — you maintain the service files. |

## Required external services

- **At least one model provider** — Anthropic, OpenAI, Mistral, Azure OpenAI, or a local Ollama endpoint.
- **Postgres 16+** — primary store. Earlier versions lack required SQL features.
- **DNS + TLS** for the hostname your users hit (Let's Encrypt via Caddy is the simplest path).

Optional but commonly added:

- **Azure AI Text Analytics** — for the higher-quality Privacy Shield path.
- **Azure Content Safety** — for the moderation guardrail.
- **Bing or Tavily** — for the web-search agent tool.
- **Voxtral** / **ElevenLabs** — for voice features.

## What's next

- [Docker Compose recipe](docker-compose.md) — full annotated stack.
- [Environment variables](env.md) — every `BEEFLOW_*` and dependency knob.
- [Upgrades](upgrades.md) — version skew, migration safety, rollback.
