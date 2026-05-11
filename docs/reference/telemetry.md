---
title: Telemetry
---

# Telemetry

What Bee Flow logs, how to ship it elsewhere, and what guarantees we make about PII in logs.

:::warning[Implementation status]

The sections below describe the **target observability stack**. Today's reality:

- **Logs**: plain `console.*` JSON (no structured Pino logger wired yet). Captured by `docker logs` or the container runtime.
- **Metrics**: only the ticket-assistant route exposes Prometheus-style metrics ([server/routes/ticketAssistant.js](https://github.com/Bee-Flow/beeflow/blob/main/server/routes/ticketAssistant.js)). There is **no** global `/metrics` endpoint, **no** OTLP exporter, and **no** app-wide HTTP / DB instrumentation.
- **Audit log**: real and complete — `guardrail_events`, `admin_audit_events`, `automation_runs` tables in Postgres. See [Admin → Audit & compliance](../admin/audit-and-compliance.md).

Sections explicitly marked **Planned** below are roadmap. Treat them as design intent, not current behaviour.

:::

## What's logged

Bee Flow's server emits structured JSON logs covering:

| Category | Examples |
|----------|----------|
| HTTP requests | method, path, status, duration_ms, requestId |
| Auth | login attempts, JWT issuance, OAuth callbacks (no tokens logged) |
| Chat | conversationId, messageId, agentId, model, token usage |
| Tool calls | toolName, durationMs, success boolean (no payloads at default level) |
| Errors | stack trace, requestId |
| Migrations | which migration applied, duration |
| Background jobs | NC sync, KB ingestion, audit retention purge |
| License | tier, lastVerifiedAt, refresh ticks |

At `LOG_LEVEL=debug`: also logs request bodies (PII-redacted via the same Privacy Shield used at runtime), full tool call args + results.

## What's NEVER logged

- **OAuth access tokens** / refresh tokens
- **Session JWTs**
- **API keys**
- **Licence private key material** (we don't have it in the open-source server)
- **Plaintext PII matched by the Privacy Shield** (only the categories + counts)

This is true at every log level.

## Log destinations

| Mode | How |
|------|-----|
| `LOG_FORMAT=json` (default) | Stdout — pipe to your log collector. |
| `LOG_FORMAT=pretty` | Human-readable — for local dev only. |
| Sentry | Set `SENTRY_DSN`. Errors go to Sentry; the rest stays in stdout. |

## Shipping to a SIEM / log store

Three good patterns:

### 1. Loki (Grafana stack)

```yaml
# Docker Compose snippet
services:
  beeflow-server:
    logging:
      driver: "loki"
      options:
        loki-url: http://loki:3100/loki/api/v1/push
        loki-batch-size: "100"
```

Then query in Grafana with `{app="beeflow"}`.

### 2. Vector → Elastic / Splunk

Run [Vector](https://vector.dev) as a sidecar; configure source = Docker JSON logs, sink = your destination. Vector handles batching, retries, transformation.

### 3. CloudWatch (AWS)

```yaml
services:
  beeflow-server:
    logging:
      driver: awslogs
      options:
        awslogs-group: /beeflow/server
        awslogs-region: eu-west-1
```

## Audit log shipping (Enterprise+)

Different mechanism from app logs. Bee Flow can push **guardrail events** in real time to a webhook:

| Setting | Value |
|---------|-------|
| URL | Your SIEM ingest endpoint |
| Shared secret | HMAC-SHA256 secret |
| Severity filter | `low` / `medium` / `high` |
| Retry | 3× with exponential backoff |

Configure in **Admin → Audit & compliance → Webhooks**. Format:

```json
{
  "id": "ev_abc",
  "organizationId": "org_123",
  "userId": "u_alice",
  "agentId": "asst_xyz",
  "violationType": "pii",
  "violationCategories": "email,phone",
  "direction": "input",
  "actionTaken": "redact",
  "model": "claude-opus-4-7",
  "timestamp": "2026-05-09T13:30:00Z"
}
```

Verify the `X-Beeflow-Sig` HMAC on your end before processing.

## Metrics (Prometheus) — **Planned**

A global `/metrics` endpoint is not yet exposed by the server. The only Prometheus-formatted endpoint that ships today is the ticket-assistant's internal `/metrics` (mounted under `/api/ticket-assistant`), gated by the `ticket_assistant` license feature.

The target series listed below are the design for an upcoming server-wide `/metrics` endpoint. If you need observability today, parse the JSON log stream into your metrics backend (Loki + recording rules works well).

Planned series:

| Metric | Labels | Unit |
|--------|--------|------|
| `beeflow_http_requests_total` | method, route, status | counter |
| `beeflow_http_request_duration_seconds` | method, route, status | histogram |
| `beeflow_chat_turns_total` | tier, model | counter |
| `beeflow_chat_turn_duration_seconds` | tier, model | histogram |
| `beeflow_chat_tokens_total` | direction, model | counter |
| `beeflow_tool_calls_total` | tool_name, status | counter |
| `beeflow_db_pool_in_use` | (none) | gauge |
| `beeflow_db_pool_max` | (none) | gauge |
| `beeflow_redis_connected` | (none) | gauge (0/1) |
| `beeflow_migrations_applied_total` | (none) | counter |
| `beeflow_guardrail_events_total` | violation_type, action | counter |
| `beeflow_license_active` | tier | gauge (0/1 per tier) |
| `beeflow_license_expires_at` | (none) | gauge (unix seconds) |
| `beeflow_users_active_total` | (none) | gauge |
| `beeflow_users_messages_month_total` | (none) | counter |

## Tracing (OpenTelemetry) — **Planned**

OTLP exporter and span instrumentation are not yet wired. The intended design (HTTP requests, chat turns with model + tool sub-spans, DB queries, integration tool calls; configured via `OTEL_EXPORTER_OTLP_ENDPOINT` + `OTEL_SERVICE_NAME`) is on the roadmap.

## Health checks

| Endpoint | Purpose |
|----------|---------|
| `GET /api/health` | Liveness. Always returns 200 if the process is up. |
| `GET /api/guard/health` | Guard sidecar liveness — returns `not-configured` when `GUARD_SERVICE_URL` is unset. |

Sub-endpoints for DB, Redis, and per-integration readiness are not currently exposed. For Kubernetes probes, point both `livenessProbe` and `readinessProbe` at `/api/health`; the server fails to start if Postgres is unreachable, so a 200 from `/api/health` is a reliable readiness signal.

## Privacy / GDPR notes

For self-hosters running with EU users:

- Set `LOG_LEVEL=info` (not `debug`). Debug-level logs include redacted but more verbose payloads — still no plaintext PII, but more inferable structure.
- Set `EU_MODE_ENABLED=true` (org config). Anonymises IPs, drops `User-Agent` headers from log lines, shortens audit retention to default 30 days.
- Strip request IDs from outgoing logs if you don't want them correlatable across services.
- Ship logs to an EU-region log store.

## Self-host opt-out for telemetry

Bee Flow does not phone home except for licence-server refresh checks. To disable that:

```bash
echo 'BEEFLOW_LICENSE_REFRESH_URL=' >> .env
```

The licence stays valid through `exp` regardless. This is the only outbound connection the server initiates without user action — every other outbound is in response to a user prompt or tool call.
