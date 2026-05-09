# Skills

A **Skill** is a bundle of prompt + tool selection + KB pointer that any agent can absorb. Think of it as a reusable "talent" — drop it into an agent and the agent gains that capability.

URL: `/app/skills` · Min tier: **Pro**.

## Why skills exist

You'd build the same "extract action items from a meeting transcript" flow into 3 different agents. Skills let you build it once, share it, and have all 3 agents stay in sync as you improve it.

A skill packages:

- A focused system-prompt extension ("When you receive a transcript, look for action items, format as `- [ ] ...`")
- A required tool subset (e.g. `transcribe_audio`, `nextcloud_notes_create`)
- An optional starter KB

When an agent has the skill, those instructions / tools become available to the agent's runtime without modifying the agent's own definition.

## Marketplace

The Skills Marketplace ships with curated skills:

| Skill | What it does |
|-------|--------------|
| Action Item Extractor | Parse meeting transcripts → assignable action items |
| Email Triager | Categorise emails into Reply / Defer / Archive / FYI |
| PR Reviewer | Read a PR diff, comment with suggestions |
| Standup Digester | Group changes by user, summarise |
| Customer Sentiment | Score chat history sentiment 1–5 |
| Research Synthesiser | Take 5 sources, write a 1-page brief with citations |
| Calendar Scheduler | Find a slot across attendees, propose times |
| Code Explainer | Plain-English explanation of a code snippet |

Install with one click; uninstall any time.

## Creating your own

1. **Studio → Skills → Create**.
2. Name + description.
3. Skill prompt extension (Markdown).
4. Required tools (ticked from your tool list).
5. Optional starter KB.
6. Visibility (private / group / org / public).
7. Save.

## Attaching to an agent

In the [Agent Designer → Tools](agent-designer.md#tab-3-tools), there's a **Skills** sub-section. Tick the skills you want to include.

## How skills compose

When an agent runs:

1. The agent's own system prompt is combined with all attached skills' prompt extensions.
2. The agent's tool list is the **union** of its own tool selection + the tools required by the attached skills.
3. The agent's KBs are the union of attached KBs + skill-required KBs.

If a skill requires a tool the user lacks access to, the skill silently disables (with a UI warning at edit time).

## Skill versioning

Skills are versioned. Updating a skill does not auto-upgrade existing attachments — agents using the skill see an "update available" badge and can opt in.

## Permissions

| Permission | Default |
|------------|---------|
| Create skill | Any user (Pro+) |
| Publish skill org-wide | Org admin |
| Submit to public marketplace | Org admin (if approval policy is on) |

## Skills vs templates vs agents

| | Template | Skill | Agent |
|---|----------|-------|-------|
| Standalone usable? | Cloned into an agent | Attached to an agent | Yes |
| Updatable upstream? | No (clone is detached) | Yes (versioned) | Yes |
| Reusable across agents? | No (clone-time) | Yes | No |
| Use case | "Start a new agent like this" | "Give an existing agent this capability" | "Talk to this agent" |
