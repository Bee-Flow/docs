---
hide:
  - navigation
  - toc
---

# Bee Flow

**AI-native workspace for Nextcloud.** Chat with your Files, Mail, Calendar, Deck, Notes, Tasks, Contacts and Talk — without your data leaving your tenant boundary.

[Install on Nextcloud :material-arrow-right:](getting-started/nextcloud.md){ .md-button .md-button--primary }
[Self-host the server :material-arrow-right:](self-hosting/docker-compose.md){ .md-button }

---

## What is Bee Flow?

Bee Flow turns your existing Nextcloud into an AI workspace. Click the bee icon in your top bar and chat with an assistant that already knows your files, mail, calendar and team. Ask it to summarise a long PDF, draft a reply to an email, find that document from last quarter, or schedule a meeting — Bee Flow does the work in the apps you already use.

Bee Flow works equally well **standalone** (without Nextcloud) for teams running just the server + frontend, with Google Workspace, Microsoft 365, GitHub and ~30 other integrations.

## Who is this for?

| You are… | Start here |
|----------|------------|
| A Nextcloud admin who wants AI for the team | [Install on Nextcloud](getting-started/nextcloud.md) |
| A developer / DevOps self-hosting on Docker | [Self-hosting → Docker Compose](self-hosting/docker-compose.md) |
| An end-user using Bee Flow in Nextcloud | [First-run wizard](getting-started/wizard.md) |
| An org admin configuring access | [Admin → Users & groups](admin/users-and-groups.md) |
| A builder creating agents / automations | [Studio overview](studio/index.md) |
| Compliance / DPO reviewing data flow | [Privacy & data flow](connector/privacy.md) |

## Three pieces, one product

<div class="grid cards" markdown>

-   :material-server:{ .lg .middle } **Server** — `Bee-Flow/beeflow`

    ---

    Node.js + Express backend. Chat, agents, knowledge bases, integrations, automations, license gate. Self-host for free at the Community tier.

    [:octicons-arrow-right-24: Self-hosting](self-hosting/index.md)

-   :material-application:{ .lg .middle } **Frontend** — `Bee-Flow/hive`

    ---

    React + Vite SPA. The UI for everything: chat, agents, admin panels. Embedded inside the Nextcloud connector as a static bundle.

    [:octicons-arrow-right-24: Studio](studio/index.md)

-   :material-cloud-sync:{ .lg .middle } **Connector** — `Bee-Flow/connector`

    ---

    The Nextcloud ExApp that bridges your Nextcloud to Bee Flow. Signed proxy, HMAC-authenticated, AGPL-3.0.

    [:octicons-arrow-right-24: Connector docs](connector/index.md)

</div>

## Where to go next

<div class="grid cards" markdown>

-   :material-rocket-launch: **Install Bee Flow**

    Step-by-step install on Nextcloud, plus self-hosting recipes for Docker Compose and Kubernetes.

    [Getting started :material-arrow-right:](getting-started/index.md)

-   :material-puzzle: **Connect a service**

    Gmail, Outlook, Drive, OneDrive, Deck, Talk, GitHub, n8n, YouTrack, SignRequest, and more.

    [Integrations catalog :material-arrow-right:](integrations/index.md)

-   :material-tools: **Build agents & automations**

    Agent Designer, Wizard, knowledge bases, skills, scheduled and event-driven automations.

    [Studio :material-arrow-right:](studio/index.md)

-   :material-shield-check: **Privacy & compliance**

    Privacy Shield, DLP, audit logs, GDPR archive, SAML SSO, Sustainable Use Licence.

    [Privacy & data flow :material-arrow-right:](connector/privacy.md)

-   :material-cog: **Admin operations**

    User sync, group-based integration access, license & usage, beta features.

    [Admin :material-arrow-right:](admin/index.md)

-   :material-code-tags: **API**

    REST + SSE reference for building your own client or pulling Bee Flow into an existing app.

    [API reference :material-arrow-right:](api/index.md)

</div>

## At a glance

- **Tiers**: free Community → Pro → Enterprise → Full. [Compare features](licensing/tiers.md).
- **License model**: fair-code (Sustainable Use Licence) for server + frontend, AGPL-3.0 for the Nextcloud connector.
- **Source code**: all three repos public on [github.com/Bee-Flow](https://github.com/Bee-Flow).
- **Hosted SaaS**: <https://app.beeflow.ai> runs the same code as this repo.
- **Languages**: UI ships in English, Dutch and German out of the box.
- **Models supported**: Anthropic Claude, OpenAI, Mistral, Azure OpenAI, plus a local-only mode via Ollama.

## Help & community

- File a bug: [github.com/Bee-Flow/beeflow/issues](https://github.com/Bee-Flow/beeflow/issues)
- Connector bug: [github.com/Bee-Flow/connector/issues](https://github.com/Bee-Flow/connector/issues)
- Frontend bug: [github.com/Bee-Flow/hive/issues](https://github.com/Bee-Flow/hive/issues)
- Security: <tomkooy@beeflow.nl> — see [SECURITY.md](https://github.com/Bee-Flow/connector/blob/main/SECURITY.md)
- Commercial questions: <tomkooy@beeflow.nl>
