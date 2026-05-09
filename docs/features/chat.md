# Chat & agents

The chat surface is the entry point for every Bee Flow interaction. Every conversation runs against an **agent** — a named persona with a system prompt, a model choice, and an explicit set of tools.

## Anatomy of an agent

| Field | Type | Purpose |
|-------|------|---------|
| `name` | text | Human-readable agent name. |
| `description` | text | One-line summary shown in the picker. |
| `avatar` | URL / emoji | Picker icon. |
| `model` | enum / null | Specific model override (e.g. `claude-opus-4-7`). `null` = use the org's default. |
| `system_prompt` | text | The agent's instructions. Markdown supported. |
| `starter_prompts` | array | Up to 4 suggested opening messages users can click. |
| `threads_enabled` | bool | Allow branching conversations into threads. |
| `copy_enabled` | bool | Show "copy reply" buttons. |
| `workspace_enabled` | bool | Open results in the side workspace pane (artifacts). |
| `embed_enabled` | bool | Allow embedding this agent in an iframe outside Bee Flow. |
| `is_published` | bool | Visible in the Marketplace. |
| `category_id` | uuid | Marketplace category. |
| `shared_groups` | array | NC groups that can use this agent. |
| `config.knowledge_base_ids` | array | KBs auto-attached. |
| `config.includeSourceReferences` | bool | Render citations as a separate UI block. |
| `config.llamaGuardEnabled` | bool | Run Llama Guard moderation on inputs/outputs. |
| `config.webSearchGuardEnabled` | bool | Apply PII filter to web-search results before injection. |

Agents live in Postgres (`agents` table). The fields above are exposed in **Studio → Agent designer** ([details](../studio/agent-designer.md)) and in **Studio → Agent wizard** for non-technical creators.

## System starter agents

Every new tenant gets 10 built-in system agents. They're seeded automatically, owned by the special `system` user, and selectively updated when their prompt files change (hash-based detection):

| Agent | Purpose |
|-------|---------|
| **Title Generator** | Generates a short conversation title after the first turn. |
| **Memory Extractor** | Pulls memorable facts out of a conversation for the user's profile memory. |
| **Component Designer** | Designs custom UI components from a description. |
| **PDF Extractor** | Specialised PDF reader; layout-aware extraction. |
| **Prompt Designer** | Helps you write a system prompt for a new agent. |
| **Conversation Starters** | Suggests opening messages for a new agent. |
| **Description Improver** | Polishes agent descriptions before publishing. |
| **Identity Improver** | Iterates on an agent's persona/tone. |
| **OrgIntel Scout** | Gathers public info about an organisation by name. |
| **Regex Generator** | Admin-only — drafts regex patterns for DLP rules. |

These aren't visible to end users in the chat picker by default — they run behind the scenes for system features. Org admins can promote any of them to user-visible by editing in **Studio**.

![Chat empty state with starter prompts](../img/screenshots/features/chat-empty-state/)

## Tool dispatch

When you send a message, the server:

1. Resolves the agent's allowed tool set by combining:
   - Org-level enabled integrations (`enabledIntegrations`)
   - Per-group disable lists ("enable wins")
   - User-level personal overrides
   - The user's OAuth status (Google connected? GitHub connected?)
   - Beta-feature flags
2. Sends the prompt + tool list to the model in the right format (Claude tool-use, OpenAI function-calling, etc.).
3. As the model emits a tool call, the server dispatches it to the correct integration handler in `server/integrations/*.js`.
4. The result is streamed back into the conversation as a `tool_result` event.
5. The model continues its turn with the tool result in context.

This loop continues until the model emits a normal text completion (no further tool calls).

## Streaming UX

Replies stream token-by-token over Server-Sent Events. Tool calls also stream — you see "Reading file…" or "Searching mail…" as they happen, not just at the end:

```
event: token
data: {"text": "Looking"}
event: token
data: {"text": " for"}
event: tool_call
data: {"id":"tc_1", "name":"nc_files_search", "args":{"query":"Q3 report"}}
event: tool_result
data: {"id":"tc_1", "result":[{"path":"/Reports/Q3.pdf"}]}
event: token
data: {"text": " I found it..."}
event: done
data: {"messageId":"msg_abc"}
```

See [API → Streaming (SSE)](../api/sse.md) for the full event spec and reconnection rules.

## Tool-call visibility (audit-friendly)

Every tool call shows up inline as a clickable row in the conversation. Click it to expand the full request and response. This makes every action auditable — for compliance you can also export the audit log (Enterprise+).

![Inline tool-call row, expanded](../img/screenshots/features/chat-tool-call/)

## Conversation lifecycle

| State | Trigger |
|-------|---------|
| Created | First user message |
| Active | Agent is generating |
| Completed | Agent emits `done` event |
| Cancelled | User clicks stop, or `/api/chat/:id/cancel` is called |
| Deleted | User clicks delete (soft-delete; purged after 30 days) |

Conversations are stored in Postgres (`conversations`, `messages`, `tool_calls` tables). Retention is org-configurable; the default is "until the user deletes it".

## Threads

If `threads_enabled` is on, any message can be branched into a thread. Threads share the parent's context up to the branch point, then continue independently. Useful for "what if" exploration without polluting the main thread.

## Workspace pane

If `workspace_enabled` is on, certain tool results (rendered HTML, generated images, code artefacts) open in a side pane instead of inline. This keeps the conversation scannable when the agent produces large artefacts.

## Memory

Per-user memory is automatically populated by the **Memory Extractor** agent — facts like preferred timezone, current project, recurring tasks. The user manages it under **Settings → Account → Memory** (delete individual entries or clear all). Memory is injected into the system prompt for every conversation that opts in.

## Where to next

- [Studio → Agent designer](../studio/agent-designer.md) — build a new agent from scratch.
- [Studio → Agent wizard](../studio/agent-wizard.md) — guided flow for non-technical creators.
- [Knowledge bases](knowledge.md) — attach a document set to an agent.
- [Privacy shield](privacy-shield.md) — what's filtered before the model sees a prompt.
