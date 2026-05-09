# DLP & guardrails

!!! warning "Enterprise tier feature"
    Requires an Enterprise or higher licence key.

DLP (Data Loss Prevention) is the org-wide policy layer on top of the [Privacy Shield](privacy-shield.md). Where the Privacy Shield silently redacts, DLP can **block**, **alert**, or **interactively prompt**.

## What you can do

- **Block** prompts containing certain content (e.g. specific project codenames, internal classification labels).
- **Alert** org admins on policy hits via mail / Talk / webhook.
- **Export** an audit log of every blocked or redacted message for compliance review.
- **Per-group exceptions** — Legal can mention contract numbers, others can't.
- **Per-agent exceptions** — Customer-support agent never sees customer names plaintext.
- **External-vs-internal model classification** — different rules when the prompt goes to Anthropic SaaS vs your own self-hosted Ollama.

## Action types

DLP scans return one of four actions:

| Action | Effect |
|--------|--------|
| `allow` | Send prompt as-is to the model. |
| `redact` | Tokenise findings (using the Privacy Shield mechanism), send tokenised text, restore on response. |
| `block` | Hard-reject the turn. User sees an error: "Your message contains sensitive content (category) and was blocked by org policy." |
| `ask` | Interactive gate — show user findings, wait for them to choose redact / allow / block. |

## Modes

The org-level `dlpMode` field selects the default behaviour for findings:

| Mode | When you'd pick it |
|------|--------------------|
| `ask` | Knowledge-worker org. Users choose. |
| `auto_redact` | Customer-support / call-centre. Tokenise silently, never expose to model. |
| `block` | Legal / Finance / R&D. Refuse the turn entirely if forbidden content is found. |

A `dlpFailureMode` controls what happens if the DLP engine itself fails (network blip to Azure):

- `fail_open` — assume `allow`, log a warning. Default for `ask` mode.
- `fail_closed` — assume `block`. Default for `block` mode.

## Execution flow

1. User submits a turn.
2. `dlpRunner.scanOutbound()` runs the prompt through PII detection + custom-term scanner.
3. The runner classifies the target LLM provider (`classifyProvider()` — external vs internal vs known-region).
4. Org config (`dlpEnabled`, `dlpMode`, `dlpFailureMode`) is consulted.
5. Result `{action, findings, redactedText, tokenMap}` is returned.
6. The chat handler implements the action:
   - `allow` → forward the original.
   - `redact` → forward `redactedText`, stash `tokenMap`.
   - `block` → emit an error event to the SSE stream and stop.
   - `ask` → emit a `dlp_finding` event; wait for the user's `POST /api/chat/:msgId/dlp-decision`.

## Audit log

Every match is recorded in the `guardrail_events` table:

| Field | Notes |
|-------|-------|
| `id` | UUID |
| `organization_id` | Org tenant. |
| `user_id` | Who sent the prompt. |
| `agent_id` | Which agent. |
| `conversation_id` | Which conversation. |
| `violation_type` | `pii` / `custom_term` / `moderation` / `unicode_smuggling`. |
| `violation_categories` | Comma-joined labels (e.g. `email,phone,bsn`). |
| `direction` | `input` (prompt) or `output` (model reply / tool result). |
| `action_taken` | `block` / `redact` / `alert` / `stripped`. |
| `source` | `chat` / `automation` / `unknown`. |
| `model` | Provider + model name. |
| `timestamp` | UTC. |

The plaintext sensitive content is **never** stored — only the categories and the action.

## Querying the audit log

```http
GET /api/guardrails/events?org=<id>&from=2026-04-01&to=2026-05-01&type=pii
Authorization: Bearer <admin_jwt>
```

Filter by user, agent, type, action, time window. CSV export is available at `/api/guardrails/events.csv`.

## Webhook export to SIEM

Real-time push to your SIEM:

```bash
sudo -u www-data php occ ...   # not applicable — use Bee Flow admin UI
```

In **Settings → Organisation → Audit → Webhooks** add a target URL. Each event is POSTed there as JSON with HMAC signature using a shared secret. Retries 3× with exponential backoff.

## Web-search guardrail

If `webSearchGuardEnabled` is on (default), web-search results are passed through the same PII detector before they're injected into the agent's context. Useful when an agent searches news / Wikipedia and the snippets contain personal data — that data shouldn't reach the model unredacted.

## Unicode-smuggling protection

Some prompt-injection attacks use zero-width Unicode characters (U+200B–U+200F, U+2060) to hide instructions. Bee Flow strips these from incoming payloads and logs each occurrence as a `unicode_smuggling` event. No user-visible action; pure defence.

## Moderation backends

Optional output moderation runs every model reply through one of:

- **Llama Guard** — self-hosted (`LLAMA_GUARD_URL`), open-weight.
- **Azure Content Safety** — managed (`AZURE_CONTENT_SAFETY_*`).

If the moderator returns a violation, the reply is redacted (or blocked, depending on policy), and an `audit log` row is written. Useful for customer-facing agents where the org has reputational exposure.

## Policy editor

![DLP policy editor](../img/screenshots/features/dlp-policy-editor/)

Policies are defined in **Settings → Organisation → DLP**:

- Built-in PII categories — toggle each on / off, set action per category.
- Custom regex categories — name, pattern, category label, action.
- Per-group overrides — exempt a group from specific categories.
- Per-agent overrides — pin a specific policy to an agent.

The policy applies to **all chat + automation runs** in the org.

## Compliance use cases

- **GDPR Article 32** — demonstrate organisational measures by showing the full guardrail audit log.
- **HIPAA** — Standard mode + custom regex for ICD codes; export quarterly.
- **PCI-DSS** — auto-block credit-card numbers in any prompt, even if the user typed them by accident.
- **NDA-protected projects** — custom regex for codenames; block.

## Where to next

- [Privacy shield](privacy-shield.md) — the underlying detection engine.
- [Admin → Audit & compliance](../admin/audit-and-compliance.md) — UI + retention policy.
- [Reference → Telemetry](../reference/telemetry.md) — shipping events to your SIEM.
