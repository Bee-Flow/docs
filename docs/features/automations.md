---
title: Automations
---

# Automations

:::warning[Pro tier feature]

Requires a Pro or higher licence key. See [Tiers](../getting-started/tiers.md).

:::

Automations (also called **routines**) are trigger-based workflows. When something happens — a cron tick, an inbound webhook, a Nextcloud event, or a button press — Bee Flow runs a graph of steps end-to-end and logs every input/output along the way.

The same toolbox the chat assistant uses is available to automations: ~30 integrations, AI steps, generated media (image / video / audio / transcription), and a set of n8n-style utility nodes for shaping data without code.

## Anatomy

```
Trigger ─▶ Step 1 ─▶ Step 2 ─▶ … ─▶ Step N
              │          │
              │          └─ each step is logged in `automation_run_steps`
              └─ outputs flow forward via refs ({{steps.step1.output.foo}})
```

Every step has a stable `id`, a `type`, an optional `label`, and a set of `inputs` bound to upstream values. The runner walks the DAG defined by `definition.edges`; branches and loops fan out from there.

## Trigger types

| Type | When it fires | Config |
|------|---------------|--------|
| `schedule` | A cron expression in the org timezone. | `schedule_cron`, `schedule_tz` |
| `webhook` | A POST to `/api/automation/webhook/{automationId}` with the bearer token lands. | URL + token are generated; copy/paste into the source system. |
| `event` | A subscribed app event happens (Nextcloud event poller every 30 s, Microsoft Graph subscription, integration webhooks). | Pick the event in the builder. |
| `manual` | A user clicks "Run now" in the UI, or calls `POST /api/automation/{id}/run`. | None. |

The next-run time for cron triggers is computed by [`server/automation/cron.js`](https://github.com/Bee-Flow/beeflow). Due jobs are claimed atomically by the runner with `SELECT … FOR UPDATE SKIP LOCKED` so multiple server replicas can share the load without double-firing.

## Step types

The runner ([`server/core/automationRunner.js`](https://github.com/Bee-Flow/beeflow)) supports the following step types. Validation lives in [`server/automation/validate.js`](https://github.com/Bee-Flow/beeflow) and is the source of truth for the up-to-date list.

### Action steps

| Step type | What it does |
|-----------|--------------|
| `integration_action` | Calls a single integration tool directly (no LLM). E.g. `gmail_send`, `nextcloud_deck_create_card`, `sheets_append_rows`. |
| `ai_step` | Calls an agent or a bare model with the previous step's output as input. Optional structured output (`outputSchema`) so downstream steps can reference `output.fieldName` instead of free-text. |
| `code` | Runs JavaScript in a sandboxed worker. Useful for a quick transform between steps. |
| `notification` | Sends one or more channels (in-app banner, Talk message, etc.). Title + body accept `{{template}}` placeholders. |

### Control flow

| Step type | What it does |
|-----------|--------------|
| `condition` | If/else branch on a single boolean expression. Outgoing edges labelled `then` / `else`. |
| `switch` | Multi-way branch with named cases + a `default`. Each case is its own outgoing edge so the canvas shows the routing visually. |
| `loop` | Iterates over an array reference (`overRef: 'steps.x.output.items'`), running the inner body for each element. Item available as `loop.<itemVar>`. |
| `wait` | Pauses the run for a fixed duration or until an absolute timestamp. |
| `stop_error` | Halts the run with a templated error message. Useful in a switch's `default` case to fail loudly when an unexpected value lands. |

### Utility (n8n-style) nodes

These run with no LLM call and no integration tool — they exist to shape data between steps so simple workflows stay author-able by non-developers.

| Step type | What it does |
|-----------|--------------|
| `set` | Edit fields — write a small object of `{ key: bindingValue }` pairs into `output`. Used to rename, default, or re-shape data. |
| `datetime` | `now`, `parse`, `format`, `addDays/Hours/Minutes`, `diff`, `extract`. Single-purpose date math without leaning on the code step. |
| `filter` | Drop array items that don't match a boolean expression. Reads `arrayRef`, writes `output.items`. |
| `limit` | Take the first or last N items of an array. |
| `dedupe` | Drop duplicates by a chosen field, preserving order. |
| `aggregate` | `sum / count / avg / min / max` over a numeric field across items. |
| `summarize` | Same operations as `aggregate`, returns a single scalar instead of `{ value }` — handy for dropping straight into a notification body. |

## Bindings

Step inputs are not free strings — they're typed bindings so the runner knows what kind of substitution to perform. Four kinds:

| Kind | Shape | Example |
|------|-------|---------|
| `literal` | `{ kind: 'literal', value: <any> }` | Hard-coded value (`"Hello"`, `42`, `true`). |
| `ref` | `{ kind: 'ref', path: 'steps.<id>.output.foo' }` | Single dotted reference to an upstream value. |
| `template` | `{ kind: 'template', value: 'Hi {{steps.x.output.name}}!' }` | String with `{{…}}` interpolation. |
| `expr` | `{ kind: 'expr', value: 'a > 5 && b == "x"' }` | A safe expression evaluated by [`server/automation/expr.js`](https://github.com/Bee-Flow/beeflow). |

The visual builder shows refs as `‹Step Label›.foo` on the canvas instead of the raw `steps.<id>.output.foo` so non-developers can read the diagram at a glance. The raw value stays available in the inspector + on hover.

## Run lifecycle

```
pending  ─▶ running  ─▶ success
                  │
                  ├─▶ failed (non-retryable error)
                  │
                  ├─▶ awaiting (paused at an approval step)
                  │
                  └─▶ cancelled (user stopped, or supersedes flag)
```

Run row fields (`automation_runs` table):

| Field | Notes |
|-------|-------|
| `id`, `automation_id`, `version` | The version of the automation definition that ran. |
| `user_id` | Who triggered it (or system, for schedules). |
| `trigger_kind` | `schedule` / `webhook` / `event` / `manual`. |
| `trigger_payload` | The exact payload the trigger received. Available to steps as `trigger.<…>`. |
| `mode` | `dry_run` (test, side-effects synthesised) or `live`. |
| `status` | See diagram. |
| `started_at`, `finished_at`, `duration_ms` | Timing. |
| `error` | Error message, if any. |
| `summary` | Short LLM-generated one-liner. |
| `parent_run_id` | Set when a run was retried from a step. |
| `awaiting_step_id` | Set when paused on approval. |
| `cancel_requested` | Boolean cancellation flag. |

Step rows (`automation_run_steps`) record `step_id`, `step_type`, `attempts`, `status`, `started_at`, `finished_at`, `input_json`, `output_json`, `error`.

### Dry-run vs live

Every routine has two run modes:

- **Dry-run** — invoked from the builder's `Dry-run` button. Steps that have side-effects (tools that send / create / update / delete) are not actually invoked; instead the runner synthesises a sample output from each tool's declared output schema ([`server/automation/outputSchemas.js`](https://github.com/Bee-Flow/beeflow)) so the variable tree stays connected. Read-only tools and pure utility nodes execute for real.
- **Live** — the trigger fires the routine and every step runs end-to-end. The first live run from a draft is gated behind a one-time confirmation dialog so authors don't accidentally email customers while testing.

The side-effect map ([`server/automation/sideEffectMap.js`](https://github.com/Bee-Flow/beeflow)) is **fail-closed**: any tool that isn't on the read-only allow-list is treated as a write. New write integrations get conservative handling automatically.

## Validation flow

1. Author drafts the automation (`is_draft=true`). Saves are debounced + versioned.
2. The first time a draft runs live, the user is asked to confirm — `needs_first_run_confirm=true`.
3. Live runs honour `run_timeout_ms` (default 5 minutes, max 1 hour).
4. A reaper job resets stuck runs older than `REAPER_FLOOR_MS` (6 minutes).
5. Failed runs can be **retried from a specific step** via `resumeFromStep()`. The retry creates a child run linked via `parent_run_id`.

The validator runs on every save and surfaces issues as red/yellow chips on the affected nodes:

- Disconnected outputs (a step that nothing references and that has no outgoing edge)
- Tools the user doesn't have access to (integration not connected, or org-disabled)
- Steps with missing required config (e.g. a `loop` with no `overRef`)
- Cyclic graphs (not allowed)
- Refs pointing at step IDs that don't exist
- Switch cases that all fall through to the same branch

## The visual builder

Routines are authored in a React Flow graph at **Studio → Routines** (URL: `/app/routines`).

### Palette

The left palette lists every node type the user can use right now: a category per integration the org has enabled (and the user has connected, or has org-key access to), plus the utility / control-flow nodes. Apps the user can see but hasn't connected get an amber "Connect" chip — they're still draggable, and the inspector links to the connect flow.

Brand artwork is shared with the chat sidebar so the same Nextcloud / Gmail / GitHub / etc. logos appear in both places. A bundled brand letter-mark falls back when no SVG is registered.

### Inspector

Click a node → the right-hand inspector shows its config. Inputs render as the right widget per binding kind (text input for literals, dropdown of upstream refs for `ref`, two-line text area for `template`, expression editor for `expr`). Saves are debounced and serialised through a single in-flight request so rapid edits don't stomp each other.

### Variable tree

The inspector's variable picker shows a tree of every output produced by every preceding step. Tools advertise their shape via [`server/automation/outputSchemas.js`](https://github.com/Bee-Flow/beeflow), so even before a first run you can pick `steps.gmail_search.output.messages[0].subject` from a typed picker rather than typing the path by hand.

### AI builder assistant

A chat panel runs alongside the canvas. It exposes a small set of `builder_*` tools to a model: add a step, wire an edge, set an input binding, configure a switch case. Ask "wire a routine that classifies inbound mail and posts urgent ones in Talk" and it'll author the graph step-by-step. You confirm before anything saves.

## Three worked examples

### 1. Inbox triage every 10 minutes

- **Trigger** — `schedule`, cron `*/10 * * * *`, tz `Europe/Amsterdam`.
- **Step 1** (`integration_action`) — `nextcloud_mail_search` for messages newer than `trigger.last_seen_at` tagged `urgent`.
- **Step 2** (`condition`) — `steps.search.output.messages.length > 0`. Else branch ends.
- **Step 3** (`ai_step`) — Inbox-Triage agent, prompt: *"Summarise these emails. Highlight any with action verbs in the subject."* `outputSchema: { summary, urgentCount, items }`.
- **Step 4** (`integration_action`) — `nextcloud_talk_send_message` to `#triage`, body: `"{{steps.ai.output.summary}}"`.

### 2. Sort an intake folder with AI

- **Trigger** — `event`, Nextcloud "file added in `/Intake`".
- **Step 1** (`ai_step`) — Document-classifier agent. `outputSchema: { type: 'invoice|contract|report|unknown', urgency: 'low|high' }`.
- **Step 2** (`switch`) — on `steps.ai.output.type`, branches: `invoice` → `nextcloud_move` to `/Facturen`; `contract` → `/Contracten`; `report` → `/Rapporten`; `default` → `/Onbekend` + a Talk notification.
- **Step 3** (in the `invoice` branch) — `condition`: `steps.ai.output.urgency == 'high'`. Then branch creates a Nextcloud task plus an in-app notification.

### 3. Daily standup digest at 09:00

- **Trigger** — `schedule`, cron `0 9 * * 1-5`.
- **Step 1** (`integration_action`) — `nextcloud_deck_list_changes` for boards in `automation.config.boards` since 18:00 yesterday.
- **Step 2** (`aggregate`) — count items grouped by `assigneeUid`.
- **Step 3** (`ai_step`) — Standup-Digest agent, render Markdown.
- **Step 4** (`integration_action`) — `nextcloud_talk_send_message` to `#standup`.

### Generated-media patterns

Image, video, audio, and transcription tools all return a file URL. Wire that URL into a downstream Drive upload, Gmail attachment, Talk message, or Notification.

```
ai_step (subject)  ─▶  generate_image (prompt: subject)  ─▶  notification (body: {{steps.img.output.url}})
```

## Available actions

Every integration the chat assistant can call is also an `integration_action` step. Highlights:

- **Nextcloud** — Files, Calendar, Contacts, Deck, Talk, Tasks, Notes, Mail, Activity, Notifications, Status.
- **Google** — Gmail, Calendar, Drive, Docs, **Sheets**, **Slides**, Contacts, Keep, Groups, Maps.
- **Microsoft** — Outlook (full + read-only), Calendar, OneDrive, Contacts.
- **Generated media** — `generate_image`, `generate_video`, `elevenlabs_tts`, `elevenlabs_music`, `elevenlabs_sfx`, `transcribe_audio`.
- **DevOps & collab** — GitHub, YouTrack, SignRequest, Fireflies, Gamma, n8n.
- **Data & search** — Web Search, Knowledge-base search, Webpages.

Full list: [Integrations](../integrations/index.md).

## Webhook trigger format

```http
POST /api/automation/webhook/{automationId}
Authorization: Bearer <webhook_token>
Content-Type: application/json

{ "any": "json", "you": "want" }
```

The webhook token is generated when you select `webhook` as the trigger and rotates only on explicit request. The body is available to the first step as `trigger.payload`.

## Tier limits

- **Pro** — up to 100 active automations per org. Min cron interval: 5 min.
- **Enterprise** — unlimited active automations. Min cron interval: 1 min. Approval steps. Webhook IP-allowlist.
- **Full** — same as Enterprise plus white-labelled webhook URLs.

## Where to next

- [Studio overview](../studio/index.md) — where automations live in the UI.
- [Integrations](../integrations/index.md) — every action a step can call.
- [API → REST reference](../api/rest.md) — programmatic creation.
- [Admin → Audit & compliance](../admin/audit-and-compliance.md) — exporting run logs.
