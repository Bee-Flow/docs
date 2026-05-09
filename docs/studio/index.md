# Studio

Studio is where you build, configure and ship the AI workspace your team uses every day. It's the home of agents, knowledge bases, automations, skills, components and templates.

URL inside Bee Flow: `/app/studio`.

## What's in Studio

<div class="grid cards" markdown>

-   :material-pencil-box-outline:{ .lg .middle } [Agent designer](agent-designer.md)

    Visual designer to build agents from scratch — name, model, prompt, tools, KB, sharing.

-   :material-magic-staff:{ .lg .middle } [Agent wizard](agent-wizard.md)

    Guided flow for non-technical creators. Q&A → working agent.

-   :material-clipboard-text-multiple:{ .lg .middle } [Templates](templates.md)

    Browse and install agent templates from the public marketplace.

-   :material-puzzle:{ .lg .middle } [Components](components.md)

    AI-built UI components you can embed in workflows and conversations.

-   :material-book-multiple:{ .lg .middle } [Knowledge bases](knowledge-bases.md)

    Create KBs, upload docs, attach to agents, browse the KB Marketplace.

-   :material-toolbox:{ .lg .middle } [Skills](skills.md)

    Reusable agent skills — drop into any agent for instant capability.

</div>

Routines (automations) live in their own top-level section in the SPA at `/app/routines`. See [Features → Automations](../features/automations.md) for the full guide.

## Studio navigation

```
Studio
├── Agents
│   ├── Designer (advanced)
│   ├── Wizard (guided)
│   └── Library (your agents)
├── Templates
│   ├── Marketplace (browse)
│   └── My templates (saved)
├── Components
│   └── Component Designer
├── Knowledge bases
│   ├── My KBs
│   └── Marketplace
└── Skills
    ├── Marketplace
    └── My skills
```

## Permissions

By default, every user can create their own agents and KBs (subject to tier limits). Admins can:

- **Lock** Studio — disable agent / KB creation org-wide.
- **Mandate templates** — require new agents to start from a template.
- **Approve publishing** — require admin sign-off before an agent goes to the org-wide library.

Configure under **Admin → Organisation settings → Studio policy**.

## Marketplace

Studio surfaces three marketplaces:

| Marketplace | What it ships | Source |
|-------------|---------------|--------|
| Agents | Pre-built agents (e.g. "PR Reviewer", "Meeting Coach") | Curated by Bee Flow + community PRs |
| Templates | Agent templates with placeholder fields | Same |
| Skills | Reusable agent capabilities (e.g. "Search GitHub PRs", "Format meeting notes") | Same |
| Knowledge | Pre-built KBs (e.g. "Bee Flow Docs", "GDPR text") | Same |

Installing from the marketplace creates a copy in your tenant — you can edit it freely without affecting the upstream.

## Where to next

- [Agent designer](agent-designer.md) — every field explained.
- [Studio → Knowledge bases](knowledge-bases.md) — connecting docs to agents.
- [Features → Automations](../features/automations.md) — scheduled / event-driven workflows.
