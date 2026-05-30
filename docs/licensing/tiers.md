---
title: Tiers
---

# Tiers

:::warning[Subject to change]

Tier limits, pricing and feature gates on this page are still being tuned
over the coming weeks. Treat the numbers below as indicative — we'll update
this page as the structure settles.

:::

Bee Flow ships in three tiers. **Community** is the default state of a fresh
install — no licence key, no caps. Community covers the free self-hosted
core: chat with agents, knowledge bases, the Nextcloud connector, multi-user
with groups, themes, and the skills marketplace. **Enterprise** adds
Studio-class capabilities (voice chat, webpage creation, automations, agent
routines, meeting notes, notebooks, component designer, projects) plus the
advanced Privacy Shield modes, guardrail DLP, the compliance hub (GDPR + AI
Act) and SAML SSO — **all beta features also require Enterprise**.
**Full** layers white-label branding and sub-licence issuance on top for
resellers.

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
| Per-agent system prompts + starter prompts | ✅ | ✅ | ✅ |
| Voice (push-to-talk + voice call) | — | ✅ | ✅ |
| **Knowledge** |
| Knowledge Bases | ✅ | ✅ | ✅ |
| Webpage creation | — | ✅ | ✅ |
| **Workflow** |
| Automations | — | ✅ | ✅ |
| Agent routines (scheduled) | — | ✅ | ✅ |
| Skills marketplace | ✅ | ✅ | ✅ |
| Projects | — | ✅ | ✅ |
| Notebooks (per-user research) | — | ✅ | ✅ |
| **Productivity** |
| Meeting notes | — | ✅ | ✅ |
| **Privacy** |
| Privacy Shield — block PII | ✅ | ✅ | ✅ |
| Privacy Shield — Tokenize & round-trip PII | — | ✅ | ✅ |
| Web Search Guard (block PII in outbound search) | — | ✅ | ✅ |
| **Admin** |
| Org settings | ✅ | ✅ | ✅ |
| User & group management | ✅ | ✅ | ✅ |
| Usage & Monitoring — Overview tab | ✅ | ✅ | ✅ |
| Usage & Monitoring — Safety / Integrations / Feedback / Terminations tabs | — | ✅ | ✅ |
| Beta features | — | ✅ | ✅ |
| Themes | ✅ | ✅ | ✅ |

Legend: ✅ available · — not available

## Feature-flag names

The server enforces premium features via `requireLicenseFeature(name)`. Names
you'll see in 403 responses:

| Flag | Min tier | Routes / surfaces |
|------|:--------:|--------------------|
| `voice_chat` | Enterprise | Realtime voice chat (Voxtral STT/TTS), `/ai/voice` |
| `webpages` | Enterprise | AI-built static webpages, `/api/webpages` |
| `automations` | Enterprise | No-code automation builder, `/api/automation*` |
| `agent_routines` | Enterprise | Scheduled agent runs (Studio → Routines) |
| `meeting_notes` | Enterprise | Transcription + summarisation, `/api/transcriptions`, `/api/meet-bot` |
| `component_designer` | Enterprise | Custom UI components, `/components` |
| `notebooks` | Enterprise | Per-user research notebooks, `/api/notebooks` |
| `projects` | Enterprise | Projects (sidebar accordion + `/api/projects`) |
| `pii_tokenize` | Enterprise | Privacy Shield "Tokenize & round-trip" PII action; community PUT clamps `piiDetectionAction` to `block` server-side |
| `web_search_guard` | Enterprise | Privacy Shield Web Search Guard toggle + category filter; community PUT force-disables it server-side |
| `advanced_usage_monitoring` | Enterprise | Usage & Monitoring tabs other than Overview — Safety, Integrations, Feedback, Terminations. Gates `/api/usage/{guardrails,integrations,azure-services}/*`, `/api/feedback`, `/api/terminations` |
| `compliance_hub_gdpr` | Enterprise | `/api/compliance`, guardrail audit log export, DSR flows |
| `compliance_hub_aia` | Enterprise | AI Act compliance hub |
| `sso_saml` | Enterprise | SAML 2.0 IdP config |
| `guardrails_dlp` | Enterprise | DLP rule editor + enforcement |
| `custom_themes` | Community | Theme overrides beyond branding basics |
| `white_label` | Full | Branding overrides (logo, colours, domain) |
| `license_issuance` | Full | Sub-licence minting |

Community-tier features (`chat_basic`, `kb_local_small`, `kb_unlimited`,
`nextcloud_basic`, `nextcloud_oauth`, `multi_user`, `skills`) are still
passed through `requireLicenseFeature` at their mount sites — the gate is
a no-op because the feature lives in `TIER_FEATURES.community`. Beta
features (the entire `BETA_FEATURES` registry) require Enterprise or
higher: on a Community install every `requireBetaFeature(...)` call
short-circuits to a 403 with
`{ error: 'feature_locked', reason: 'beta_requires_enterprise', required:
'enterprise', upgrade_url: … }` so the UI can route the user to the right
CTA. Super-admins bypass the tier check (same exemption that already
exists for licensed-feature gates).

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
| Free self-hosted core — chat, KB, agents, skills | Community |
| Team that wants Studio (voice, webpage creation, automations, agent routines, notebooks, meeting notes, projects, component designer), the advanced Privacy Shield modes (tokenize PII, web-search guard), the full Usage & Monitoring tabs, beta features, or compliance (SSO, GDPR/AI-Act) | Enterprise |
| Reseller / private-label deployment | Full |

Custom plans (e.g. capped seats, specific feature sets) are available —
contact [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl).

## Legacy Pro tier

Earlier versions of Bee Flow exposed a paid **Pro** tier that gated
automations, voice, meeting notes, knowledge-base expansion and similar
features. That tier has been retired and those features now ship in
**Enterprise**.

For backward compatibility, existing licences carrying `tier: "pro"` —
whether JWT-signed, admin-issued blobs, or Stripe subscription rows — are
still accepted and silently resolved to `enterprise`. Paying Pro
customers therefore retain everything they had and pick up the additional
Enterprise capabilities (compliance hub, SSO, etc.) at no extra step. The
mapping lives in
[`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js)
as `LEGACY_TIER_ALIAS`.
