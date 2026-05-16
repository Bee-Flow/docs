---
title: Tiers
---

# Tiers

Bee Flow ships in three tiers. **Community** is the default state of a fresh
install — no licence key, no caps, no missing features. Paid tiers add
compliance, branding, and resale capabilities on top.

Source of truth: [`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js).

## Limits

The Community tier is uncapped. Paid tiers do not introduce smaller limits;
they add capability rather than headroom.

| Limit (`tiers.js` key) | Community | Enterprise | Full |
|-------|:---------:|:----------:|:----:|
| Users (`max_users`) | unl. | unl. | unl. |
| Agents (`max_agents`) | unl. | unl. | unl. |
| Messages / month (`max_messages_per_month`) | unl. | unl. | unl. |
| Knowledge-base sources (`max_kb_sources`) | unl. | unl. | unl. |

Conventions used elsewhere in the product (cron intervals, KB document size
cap, audit retention) are policy defaults rather than hard-coded limits and
may move at any time.

## Feature × tier matrix

| Feature | Community | Enterprise | Full |
|---------|:---------:|:----------:|:----:|
| **Core chat** |
| Basic chat with agents | ✅ | ✅ | ✅ |
| 10 system starter agents | ✅ | ✅ | ✅ |
| Marketplace (browse + install) | ✅ | ✅ | ✅ |
| Per-agent system prompts + starter prompts | ✅ | ✅ | ✅ |
| Voice (push-to-talk + voice call) | ✅ | ✅ | ✅ |
| **Knowledge** |
| Local KB | ✅ | ✅ | ✅ |
| Vector / hybrid / reranked KB | ✅ | ✅ | ✅ |
| KB Marketplace | ✅ | ✅ | ✅ |
| Web pages crawler & ingest | ✅ | ✅ | ✅ |
| **Workflow** |
| Automations | ✅ | ✅ | ✅ |
| Agent routines (scheduled) | ✅ | ✅ | ✅ |
| Skills marketplace | ✅ | ✅ | ✅ |
| Component Designer (custom UI) | ✅ | ✅ | ✅ |
| Notebooks (per-user research) | ✅ | ✅ | ✅ |
| **Productivity** |
| Meeting notes | ✅ | ✅ | ✅ |
| Ticket assistant / Email KB | ✅ | ✅ | ✅ |
| **Privacy** |
| Privacy Shield (Standard) | ✅ | ✅ | ✅ |
| Privacy Shield (Strict / Custom) | ✅ | ✅ | ✅ |
| Guardrail DLP rules | — | ✅ | ✅ |
| Guardrail audit log export | — | ✅ | ✅ |
| Moderation (Azure Content Safety) | — | ✅ | ✅ |
| **Admin** |
| Org settings | ✅ | ✅ | ✅ |
| User & group management | ✅ | ✅ | ✅ |
| NC integration toggles | ✅ | ✅ | ✅ |
| Beta features | ✅ | ✅ | ✅ |
| Custom themes | — | ✅ | ✅ |
| Advanced analytics | — | ✅ | ✅ |
| Swarm (multi-agent orchestration) | — | ✅ | ✅ |
| **Compliance** |
| GDPR archive / DSR flows | — | ✅ | ✅ |
| AI Act compliance hub | — | ✅ | ✅ |
| SAML 2.0 SSO | — | ✅ | ✅ |
| Audit log webhook → SIEM | — | ✅ | ✅ |
| **Branding & resale** |
| White-label (logo, colours, domain) | — | — | ✅ |
| Sub-licence issuance (your own customers) | — | — | ✅ |

Legend: ✅ available · — not available

## Feature-flag names

The server enforces premium features via `requireLicenseFeature(name)`. Names
you'll see in 403 responses:

| Flag | Min tier | Routes / surfaces |
|------|:--------:|--------------------|
| `compliance_hub_gdpr` | Enterprise | `/api/compliance`, guardrail audit log export, DSR flows |
| `compliance_hub_aia` | Enterprise | AI Act compliance hub |
| `sso_saml` | Enterprise | SAML 2.0 IdP config |
| `audit_log_export` | Enterprise | Audit-log SIEM webhook |
| `guardrails_dlp` | Enterprise | DLP rule editor + enforcement |
| `custom_themes` | Enterprise | Theme overrides beyond branding basics |
| `swarm` | Enterprise | Parallel multi-agent orchestration |
| `advanced_analytics` | Enterprise | Org-wide usage analytics |
| `white_label` | Full | Branding overrides (logo, colours, domain) |
| `license_issuance` | Full | Sub-licence minting |

Community-tier features (`automations`, `webpages`, `meeting_notes`, `skills`,
`ticket_assistant`, `voice_chat`, `kb_unlimited`, etc.) are still passed
through `requireLicenseFeature` at their mount sites — the gate is a no-op
because the feature lives in `TIER_FEATURES.community`. Beta opt-in via
`requireBetaFeature` remains in force and is independent of the licence tier.

## Limit enforcement

With Community uncapped, no limit currently fires for unlicensed installs.
The enforcement plumbing is still in place so paid tiers (or future custom
plans) can impose caps:

| Limit | Where it fires | What you see |
|-------|----------------|---------------|
| Users | `POST /auth/admin/users` and the NC sync job | UI shows "Tier limit reached"; sync skips new users (only fires when a custom plan sets `max_users` > 0) |
| Agents | `POST /api/agents` | UI shows "Tier limit reached" |
| Messages / mo | `POST /api/chat` | 402 Payment Required, `error: "tier_limit"` |
| KB count | `POST /api/knowledge` | 402 |

Counters reset on the first day of each calendar month at 00:00 UTC.

## Picking a tier

| Need | Suggested tier |
|------|----------------|
| Anything from a homelab to a large team — no compliance ask | Community |
| Regulated environment (SSO, audit export, GDPR/AI-Act compliance) | Enterprise |
| Reseller / private-label deployment | Full |

Custom plans (e.g. capped seats, specific feature sets) are available —
contact [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl).

## Legacy Pro tier

Earlier versions of Bee Flow exposed a paid **Pro** tier that gated
automations, voice, meeting notes, knowledge-base expansion and similar
features. That tier has been retired: all of those features now ship in
Community.

For backward compatibility, existing licences carrying `tier: "pro"` — whether
JWT-signed, admin-issued blobs, or Stripe subscription rows — are still
accepted and silently resolved to `enterprise`. Paying customers therefore
gain (rather than lose) capability at renewal. The mapping lives in
[`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js)
as `LEGACY_TIER_ALIAS`.
