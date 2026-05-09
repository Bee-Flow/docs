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

Bee Flow turns your Nextcloud into an AI workspace. Click the bee icon in your top bar and chat with an assistant that already knows your files, mail, calendar and team. Ask it to summarise a long PDF, draft a reply to an email, find that document from last quarter, or schedule a meeting — Bee Flow does the work in the apps you already use.

## Three pieces, one product

<div class="grid cards" markdown>

-   :material-server:{ .lg .middle } **Server** — `Bee-Flow/beeflow`

    ---

    Node.js + Express backend. Chat, agents, knowledge bases, integrations, automations, license gate. Self-host for free at the Community tier.

-   :material-application:{ .lg .middle } **Frontend** — `Bee-Flow/hive`

    ---

    React + Vite SPA. The UI for everything: chat, agents, admin panels. Embedded inside the Nextcloud connector as a static bundle.

-   :material-cloud-sync:{ .lg .middle } **Connector** — `Bee-Flow/connector`

    ---

    The Nextcloud ExApp that bridges your Nextcloud to Bee Flow. Signed proxy, HMAC-authenticated, AGPL-3.0.

</div>

## Quick links

- [First-run wizard walk-through](getting-started/wizard.md)
- [Free vs paid features](getting-started/tiers.md)
- [Privacy & data flow](connector/privacy.md)
- [Self-hosting on Docker Compose](self-hosting/docker-compose.md)
- [API reference](api/index.md)

## Source code

All three components are open source on [github.com/Bee-Flow](https://github.com/Bee-Flow).

- Frontend + server: **Sustainable Use Licence** (fair-code) — free to self-host for your own organisation.
- Nextcloud connector: **AGPL-3.0-or-later**.
