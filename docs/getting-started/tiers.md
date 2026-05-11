---
title: Free vs paid features
---

# Free vs paid features

:::warning[Subject to change]

Tier limits, pricing and feature gates on this page are being reworked over the coming weeks. Treat the numbers below as indicative — we'll update this page when the new structure lands.

:::

Bee Flow ships in four tiers. The **Community** tier is fully functional with no licence key — basic chat, agents, knowledge bases and the Nextcloud connector all work out of the box.

## At a glance

| Tier         | Users  | Agents | Messages/mo | Premium features |
|--------------|:------:|:------:|:-----------:|------------------|
| `community`  | 1      | 2      | 1,000       | Basic chat, local KB, Nextcloud basic |
| `pro`        | 25     | 20     | 50,000      | + Automations, web pages, meeting notes, skills, ticket assistant, voice |
| `enterprise` | unl.   | unl.   | unl.        | + compliance hub (GDPR + audit log export), SAML SSO |
| `full`       | unl.   | unl.   | unl.        | + White-label, licence issuance |

The full feature × tier matrix lives in [Licensing → Tiers](../licensing/tiers.md). Source of truth: [`server/license/tiers.js`](https://github.com/Bee-Flow/beeflow/blob/main/license/tiers.js).

## Where the limits fire

| Limit | Where it's enforced | What happens at the cap |
|-------|---------------------|--------------------------|
| Users | User-create endpoint, NC sync job | New users are skipped; existing users stay active |
| Agents | Agent-create endpoint | UI shows "Tier limit reached — upgrade to add more" |
| Messages / mo | Chat endpoint, automations runner | Org-wide chat returns 402 with `tier_limit` until the next month |

A monthly counter resets on the first UTC day of each calendar month. Counter state is in Postgres; nothing is sent off-machine.

## Feature flags (premium gates)

The server uses a `requireLicenseFeature(name)` middleware that returns 403 to any user/org without the feature. Specific gates:

| Feature flag | Tier | What it unlocks |
|--------------|------|-----------------|
| `automations` | Pro+ | `/api/automation`, the Automation Builder UI |
| `webpages` | Pro+ | `/api/webpages`, the Webpages section |
| `meeting_notes` | Pro+ | `/api/transcriptions`, `/api/meet-bot`, voice |
| `skills` | Pro+ | `/api/skills`, the Skills marketplace |
| `ticket_assistant` | Pro+ | `/api/ticket-assistant`, `/api/email-kb` |
| `compliance_hub_gdpr` | Enterprise+ | `/api/compliance`, guardrail audit log export, DSR flows |
| `saml_sso` | Enterprise+ | SAML 2.0 identity-provider config |
| `gdpr_hub` | Enterprise+ | GDPR archive, data-subject request flows |
| `white_label` | Full | Replace branding, custom theme assets |
| `license_issuance` | Full | Mint sub-licences for downstream tenants |

## What's free forever

You can run a single user, two agents, ~1k chats/mo, with the full Nextcloud bridge, all 30+ tool integrations, and the Privacy Shield. Two distinctions:

- **Privacy Shield** is in every tier — but the **guardrail audit log export** (compliance hub) is Enterprise.
- **Knowledge Bases** are in every tier — but the **Local KB** is single-user; **vector / hybrid KBs** with reranking are Pro+.

## Why fair-code?

The frontend and server are released under the **Sustainable Use Licence**. You can use, modify and self-host them for free for your own organisation. You cannot offer Bee Flow as a paid service to third parties without a commercial agreement.

The Nextcloud connector is **AGPL-3.0-or-later** to comply with App Store requirements.

[More on the licensing model →](../licensing/index.md)
