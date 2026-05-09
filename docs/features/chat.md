# Chat & agents

The chat surface is the entry point for every Bee Flow interaction. Every conversation runs against an **agent** — a named persona with a system prompt, a model choice, and an explicit set of tools.

## Default agents

Every new tenant gets a small set of starter agents:

- **Assistant** — general-purpose, all integrations enabled.
- **Mail drafter** — focused on writing replies, mail integration only.
- **Researcher** — focused on multi-document reasoning, knowledge-base + web tools.

## Creating your own

In **Studio → Agents → New agent** you pick:

- Name + icon
- Model (Anthropic / OpenAI / Mistral / Azure / local)
- System prompt
- Allowed tools (per-agent allow-list, e.g. only Files + Calendar)
- Privacy shield level

## Tool calls

When the agent uses a tool, you see it inline in the conversation:

![Tool call inline](../img/screenshots/chat-toolcall.png)

Click the row to expand the full request/response. This makes every action auditable.

## Streaming

Replies stream token-by-token over Server-Sent Events. Tool calls also stream — you see "Reading file…" or "Searching mail…" as they happen, not just at the end.
