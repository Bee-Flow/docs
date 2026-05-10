# Automations

:::warning[Pro tier feature]

Requires a Pro or higher licence key. See [Tiers](../getting-started/tiers.md).

:::

Automations are trigger-based workflows. When something happens, run an agent (or a more complex pipeline) and act on the output.

## Anatomy

```
Trigger ─▶ Filter ─▶ Step 1 ─▶ Step 2 ─▶ ... ─▶ Action
                       │
                       └─ logs every step in `automation_run_steps`
```

## Trigger types

| Type | When it fires | Config |
|------|---------------|--------|
| `schedule` | A cron expression (with timezone). | `schedule_cron`, `schedule_tz` |
| `webhook` | A POST to `/api/automation/webhook/{automationId}` lands. | URL is generated; copy + paste into the source system. |
| `event` | A subscribed app event happens (Nextcloud event poller every 30 s, integration webhooks). | Pick the event in the builder. |
| `manual` | A user clicks "Run now" in the UI. | None. |

The next-run time is computed via `cron.js`. Due jobs are claimed atomically by the runner with `SELECT … FOR UPDATE SKIP LOCKED` so multiple server replicas can share the load without double-firing.

## Step types

The runner (`server/core/automationRunner.js`) supports:

| Step type | What it does |
|-----------|--------------|
| `ai_step` | Calls an agent (or a bare model) with the previous step's output as input. |
| Tool invocation | Calls any integration tool directly (no LLM). E.g. "send Talk message", "create Deck card". |
| `code_step` | Runs JavaScript in a sandboxed worker. Useful for transforming data between steps. |
| `approval_step` | Pauses the run; an admin (or specified user) must approve before it continues. |
| `condition_step` | Branches based on an expression evaluated against the previous step's output. |
| `loop_step` | Iterates over an array, running the inner steps for each element. |

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
| `trigger_payload` | The exact payload the trigger received (for webhooks / events). |
| `mode` | `dry_run` (test, side-effects skipped) or `live`. |
| `status` | See diagram. |
| `started_at`, `finished_at`, `duration_ms` | Timing. |
| `error` | Error message, if any. |
| `summary` | Short LLM-generated one-liner. |
| `parent_run_id` | Set when a run was retried from a step. |
| `awaiting_step_id` | Set when paused on approval. |
| `cancel_requested` | Boolean cancellation flag. |

Step rows (`automation_run_steps`) record `step_id`, `step_type`, `attempts`, `status`, `started_at`, `finished_at`, `input_json`, `output_json`, `error`.

## Validation flow

1. Author drafts the automation (`is_draft=true`).
2. The first time a draft is run, the user is asked to confirm — `needs_first_run_confirm=true`.
3. Live runs honour `run_timeout_ms` (default 5 minutes, max 1 hour).
4. A reaper job resets stuck runs older than `REAPER_FLOOR_MS` (6 minutes).
5. Failed runs can be **retried from a specific step** via `resumeFromStep()`. The retry creates a child run linked via `parent_run_id`.

## Three worked examples

### 1. Inbox triage every 10 minutes

- **Trigger** — `schedule`, cron `*/10 * * * *`, tz `Europe/Amsterdam`.
- **Filter** — last run-time stored in `automation.last_seen_at`.
- **Step 1** — `nc_mail_search` for messages newer than `last_seen_at` tagged `urgent`.
- **Step 2** — `ai_step` with the **Inbox Triage** agent: "Summarise these emails. Highlight any with action verbs in subject."
- **Step 3** — `nc_talk_send_message` posting the summary in `#triage` Talk room.

### 2. Meeting prep 30 minutes before every event

- **Trigger** — `event`, NC calendar event upcoming-30 min.
- **Step 1** — `nc_calendar_get` to fetch the event details.
- **Step 2** — `nc_contacts_search` for each attendee's recent context.
- **Step 3** — `ai_step` with **Meeting Prep** agent: "Brief me on this meeting in 6 bullets."
- **Step 4** — `nc_notes_append` to today's "Meeting prep" notebook entry.

### 3. Daily standup digest at 09:00

- **Trigger** — `schedule`, cron `0 9 * * 1-5`.
- **Step 1** — `nc_deck_list_changes` for boards mentioned in `automation.config.boards` since 18:00 yesterday.
- **Step 2** — `code_step`: group changes by user.
- **Step 3** — `ai_step` with **Standup Digest** agent: render as Markdown.
- **Step 4** — `nc_talk_send_message` to `#standup`.

## Builder

Automations are authored in a visual dataflow graph in **Studio → Routines** (URL: `/app/routines`). Drag nodes, connect them, validate.

![Automation visual graph editor](../img/screenshots/features/automation-builder/)

The validation pill highlights:

- Disconnected outputs
- Tools the user lacks access to
- Steps with missing required config
- Cyclic graphs (not allowed)

## Recent runs

Every fired automation logs a run with input, output, and per-step timing. Drill in to:

- Replay the same trigger payload against the latest version
- Resume from a failed step
- Diff the run against the previous one
- Export run logs as JSON (Enterprise+)

## Webhook trigger format

```http
POST /api/automation/webhook/{automationId}
Authorization: Bearer <webhook_token>
Content-Type: application/json

{ "any": "json", "you": "want" }
```

The webhook token is generated when you select `webhook` as the trigger and rotates only on explicit request. The body is available as `trigger.payload` to the first step.

## Tier limits

- **Pro** — up to 100 active automations per org. Min cron interval: 5 min.
- **Enterprise** — unlimited active automations. Min cron interval: 1 min. Approval steps. Webhook IP-allowlist.
- **Full** — same as Enterprise plus white-labelled webhook URLs.

## Where to next

- [Studio overview](../studio/index.md) — where automations live in the UI.
- [API → REST reference](../api/rest.md) — programmatic creation.
- [Admin → Audit & compliance](../admin/audit-and-compliance.md) — exporting run logs.
