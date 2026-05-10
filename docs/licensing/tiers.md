# Tiers

:::warning[Subject to change]

Tier limits, pricing and feature gates on this page are being reworked over the coming weeks. Treat the numbers below as indicative — we'll update this page when the new structure lands.

:::

Source of truth: [`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js).

## Limits

| Limit | Community | Pro | Enterprise | Full |
|-------|:---------:|:---:|:----------:|:----:|
| Users | 1 | 25 | unl. | unl. |
| Agents | 2 | 20 | unl. | unl. |
| Messages / month | 1 000 | 50 000 | unl. | unl. |
| Knowledge bases | 3 | 100 | unl. | unl. |
| Automations (active) | — | 100 | unl. | unl. |
| Min cron interval | — | 5 min | 1 min | 1 min |
| KB document size cap | 10 MB | 100 MB | 1 GB | 1 GB |
| Audit log retention | 30 days | 90 days | configurable | configurable |

## Feature × tier matrix

| Feature | Community | Pro | Enterprise | Full |
|---------|:---------:|:---:|:----------:|:----:|
| **Core chat** |
| Basic chat with agents | ✅ | ✅ | ✅ | ✅ |
| 10 system starter agents | ✅ | ✅ | ✅ | ✅ |
| Marketplace (browse + install) | ✅ | ✅ | ✅ | ✅ |
| Per-agent system prompts + starter prompts | ✅ | ✅ | ✅ | ✅ |
| Voice (push-to-talk + voice call) | — | ✅ | ✅ | ✅ |
| **Knowledge** |
| Local KB | ✅ | ✅ | ✅ | ✅ |
| Vector / hybrid / reranked KB | — | ✅ | ✅ | ✅ |
| KB Marketplace | ✅ | ✅ | ✅ | ✅ |
| Web pages crawler & ingest | — | ✅ | ✅ | ✅ |
| **Workflow** |
| Automations | — | ✅ | ✅ | ✅ |
| Skills marketplace | — | ✅ | ✅ | ✅ |
| Component Designer (custom UI) | — | ✅ | ✅ | ✅ |
| Notebooks (per-user research) | ✅ | ✅ | ✅ | ✅ |
| **Productivity** |
| Meeting notes | — | ✅ | ✅ | ✅ |
| Ticket assistant / Email KB | — | ✅ | ✅ | ✅ |
| **Privacy** |
| Privacy Shield (Standard) | ✅ | ✅ | ✅ | ✅ |
| Privacy Shield (Strict / Custom) | ✅ | ✅ | ✅ | ✅ |
| DLP gate (interactive / block) | — | — | ✅ | ✅ |
| DLP audit log export | — | — | ✅ | ✅ |
| Moderation (Azure Content Safety) | — | — | ✅ | ✅ |
| **Admin** |
| Org settings + branding | ✅ | ✅ | ✅ | ✅ |
| User & group management | ✅ | ✅ | ✅ | ✅ |
| NC integration toggles | ✅ | ✅ | ✅ | ✅ |
| Beta features | ✅ | ✅ | ✅ | ✅ |
| **Compliance** |
| GDPR archive / DSR flows | — | — | ✅ | ✅ |
| SAML 2.0 SSO | — | — | ✅ | ✅ |
| Audit log webhook → SIEM | — | — | ✅ | ✅ |
| **Branding & resale** |
| White-label (logo, colours, domain) | — | — | — | ✅ |
| Sub-licence issuance (your own customers) | — | — | — | ✅ |

Legend: ✅ available · — not available

## Feature-flag names

The server enforces premium features via `requireLicenseFeature(name)`. Names you'll see in 403 responses:

| Flag | Min tier | Routes / surfaces |
|------|:--------:|--------------------|
| `automations` | Pro | `/api/automation`, `/api/automation/builder`, Studio → Routines |
| `webpages` | Pro | `/api/webpages` |
| `meeting_notes` | Pro | `/api/transcriptions`, `/api/meet-bot`, voice |
| `skills` | Pro | `/api/skills` |
| `ticket_assistant` | Pro | `/api/ticket-assistant`, `/api/email-kb` |
| `dlp` | Enterprise | DLP rule editor, guardrail audit log export |
| `gdpr_hub` | Enterprise | `/api/compliance/gdpr/*` |
| `saml_sso` | Enterprise | SAML 2.0 IdP config |
| `audit_export` | Enterprise | Audit-log SIEM webhook |
| `white_label` | Full | Branding overrides |
| `license_issuance` | Full | Sub-licence minting |

## Limit enforcement

| Limit | Where it fires | What you see |
|-------|----------------|---------------|
| Users | `POST /auth/admin/users` and the NC sync job | UI shows "Tier limit reached"; sync skips new users |
| Agents | `POST /api/agents` | UI shows "Tier limit reached" |
| Messages / mo | `POST /api/chat` | 402 Payment Required, `error: "tier_limit"` |
| KB count | `POST /api/knowledge` | 402 |

Counters reset on the first day of each calendar month at 00:00 UTC.

## Picking a tier

| Org size | Suggested tier |
|----------|----------------|
| Solo / homelab | Community |
| Team of ≤25 | Pro |
| Mid-market with compliance ask | Enterprise |
| Reseller / private-label | Full |

Custom plans (e.g. 100 users, no automations) are available — contact [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl).
