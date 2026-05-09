# Automations

!!! warning "Pro tier feature"
    Requires a Pro or higher license key. See [Tiers](../getting-started/tiers.md).

Automations are trigger-based workflows. When something happens, run an agent.

## Anatomy

```
Trigger ──▶ Filter ──▶ Agent ──▶ Action
```

- **Trigger** — what kicks it off (incoming email, calendar event 15 min away, file added to folder, schedule, webhook).
- **Filter** — optional condition (e.g. only emails tagged `urgent`).
- **Agent** — which Bee Flow agent processes the input.
- **Action** — what to do with the agent's output (send email, post in Talk, create a calendar event, write to a file).

## Visual builder

The builder is a dataflow graph — drag nodes, connect them, validate.

![Automation builder](../img/screenshots/automation-builder.png)

## Recent runs

Every fired automation logs a run with input, output, and timing. Drill in to debug failures or replay.

## Examples

- **Inbox triage** — every 10 min, summarise unread urgent mail and post in `#triage` Talk channel.
- **Meeting prep** — 30 min before a calendar event, drop a brief in your "Today" Notes file with attendee context.
- **Daily standup digest** — at 09:00, summarise yesterday's Deck moves and post in your team channel.
