---
title: Tiers
---

# Tiers

:::warning[Subject to change]

Tier limits, pricing and feature gates on this page are being reworked over the coming weeks. Treat the numbers below as indicative — we'll update this page when the new structure lands.

:::

Source of truth: [`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js).

## Limits

Hard-enforced limits from `tiers.js`:

| Limit (`tiers.js` key) | Community | Pro | Enterprise | Full |
|-------|:---------:|:---:|:----------:|:----:|
| Users (`max_users`) | 1 | 25 | unl. | unl. |
| Agents (`max_agents`) | 2 | 20 | unl. | unl. |
| Messages / month (`max_messages_per_month`) | 1 000 | 50 000 | unl. | unl. |
| Knowledge-base sources (`max_kb_sources`) | 5 | 100 | unl. | unl. |

Conventions used elsewhere in the product (cron intervals, KB document size cap, audit retention) are policy defaults rather than hard-coded limits and may move at any time.

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
| Guardrail audit log export | — | — | ✅ | ✅ |
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
| `compliance_hub_gdpr` | Enterprise | `/api/compliance`, guardrail audit log export, DSR flows |
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
