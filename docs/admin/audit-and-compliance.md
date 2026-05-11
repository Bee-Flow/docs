---
title: "Audit & compliance"
---

# Audit & compliance

:::warning[Enterprise tier feature]

Most audit-export functions require an Enterprise or Full licence.

:::

Path: **Admin → Audit**.

## What's logged

Every prompt scan, guardrail trigger, and admin operation is recorded in three tables:

| Table | What it stores | Retention |
|-------|----------------|-----------|
| `guardrail_events` | PII / moderation / unicode-smuggling violations | 30 / 90 / configurable per tier |
| `admin_audit_events` | Admin UI actions (user create/delete, role change, settings update) | Same |
| `automation_runs` + `automation_run_steps` | Every automation run + per-step input/output | Same |

Plaintext sensitive content is **never** stored — only categories and the action taken.

## Guardrail events

Schema:

| Field | Type | Notes |
|-------|------|-------|
| `id` | UUID | |
| `organization_id` | UUID | Tenant. |
| `user_id` | UUID | Who triggered the prompt. |
| `agent_id` | UUID | Which agent. |
| `conversation_id` | UUID | Which conversation. |
| `violation_type` | enum | `pii` / `custom_term` / `moderation` / `unicode_smuggling` |
| `violation_categories` | text | Comma-joined labels (`email,phone,bsn`). |
| `direction` | enum | `input` (prompt) or `output` (model reply / tool result). |
| `action_taken` | enum | `block` / `redact` / `alert` / `stripped`. |
| `source` | enum | `chat` / `automation` / `unknown`. |
| `model` | text | Provider + model name. |
| `timestamp` | timestamptz | UTC. |

## Querying

![Guardrail event browser](../img/screenshots/admin/audit-log/)

In the admin UI:

| Filter | Notes |
|--------|-------|
| Time range | Default last 7 days. |
| User | Multi-select. |
| Agent | Multi-select. |
| Violation type | `pii` / `custom_term` / `moderation` / `unicode_smuggling`. |
| Action taken | `block` / `redact` / `alert` / `stripped`. |
| Categories | Free-text match against `violation_categories`. |

The result table is paginated, sortable. Click a row for the (non-plaintext) detail.

## CSV export

```http
GET /api/guardrails/events.csv?from=2026-04-01&to=2026-05-01
Authorization: Bearer <admin_jwt>
```

Returns the same rows as the UI, in CSV. Useful for quarterly compliance reviews.

## SIEM webhook

In **Settings → Organisation → Audit → Webhooks**:

| Field | Notes |
|-------|-------|
| Webhook URL | Your SIEM endpoint. |
| Shared secret | HMAC-SHA256 secret for request signing. |
| Severity filter | Only push events at this severity or higher. |
| Retry policy | 3 attempts with exponential backoff. |

Each event is POSTed as JSON with `X-Beeflow-Sig: <hmac-hex>`. Verify on your side.

## GDPR Compliance Hub (Enterprise+)

Path: **Admin → Audit → GDPR**.

Features:

| Tool | Purpose |
|------|---------|
| **Subject Access Request** | Generate a ZIP archive of everything Bee Flow has on a user (conversations, memories, audit refs). |
| **Right to Erasure** | Hard-delete a user with cascade-anonymise. Records the deletion in the GDPR archive. |
| **Right to Portability** | Same archive as SAR, in machine-readable JSON. |
| **Processing record** | The standard GDPR "register of processing activities" — pre-filled with Bee Flow's data flows, exportable as PDF. |
| **DPIA template** | Boilerplate for a Data Protection Impact Assessment. |

## AI Act (EU)

For organisations within scope of the EU AI Act:

| Asset | Purpose |
|-------|---------|
| Model card | Lists every model used + provider + region. |
| Risk tier classifier | Helps you map each agent to AI-Act risk tier (minimal / limited / high). |
| Transparency obligations | Pre-built prompts to surface "you are talking to an AI" disclaimers. |

## Admin actions audit

Every admin action in the UI is logged:

| Action | Logged fields |
|--------|---------------|
| User create | who, target user, initial role + groups |
| User delete | who, target user, hard vs soft |
| Role change | who, target user, before/after role |
| Group create / delete | who, group, reason |
| Settings update | who, setting key, before/after value |
| Licence apply | who, tier, expiry |

Same query UI; tab labelled **Admin actions**.

## Retention

| Tier | `guardrail_events` retention | `admin_audit_events` retention |
|------|------------------------------|--------------------------------|
| Community | 30 days | 30 days |
| Pro | 90 days | 90 days |
| Enterprise | configurable | configurable |
| Full | configurable | configurable |

Configure under **Org settings → Audit → Retention**. Min 30 days; max 7 years.

## Audit log integrity

Audit rows are append-only at the application layer (no UPDATE / DELETE endpoints). For tamper-evidence:

- Daily log digest (SHA-256 of all that day's rows) is signed and exposed at `/api/audit/digest/<date>`.
- (Roadmap) optional Postgres-extension write-once with `pg_rewind`-style protection.

## Where to next

- [Privacy shield](../features/privacy-shield.md) — the detection engine that produces guardrail events.
- [Reference → Telemetry](../reference/telemetry.md) — shipping events to SIEM.
