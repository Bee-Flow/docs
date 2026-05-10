# Privacy shield

The Privacy Shield is the in-tenant filter that scans every prompt and tool result before it reaches the language model. It's available in **every tier**, including Community.

## Detected categories

Bee Flow detects 19+ categories of sensitive data. Detection runs against outbound prompts (user → model) and inbound tool results (e.g. file contents the agent fetched).

| Category | Examples |
|----------|----------|
| Person | "Alice Johnson" |
| PersonType | "CEO", "GP", "Lawyer" |
| Age | "42 years old" |
| DateOfBirth | "1985-03-12" |
| PhoneNumber | `+31 6 12345678`, `(555) 123-4567` |
| Email | `alice@example.com` |
| Address | "Keizersgracht 123, 1015 CJ Amsterdam" |
| CreditCardNumber | `4111 1111 1111 1111` |
| BankAccountNumber | (generic) |
| IBAN | `NL91 ABNA 0417 1643 00` |
| ABARoutingNumber | `021000021` |
| SWIFTCode | `ABNANL2A` |
| SSN | US Social Security Numbers |
| PassportNumber | (locale-aware) |
| DriversLicenseNumber | (locale-aware) |
| IPAddress | `192.168.1.1`, `2001:db8::1` |
| URL | including credentialed URLs (`https://user:pass@host`) |
| Azure CosmosDB Key | (high-confidence pattern) |
| Azure Storage Key | (high-confidence pattern) |
| Organization | "Bee Flow B.V.", "Acme Corp" |
| EUNationalIdentificationNumber (BSN) | Dutch Burgerservicenummer |

The list is enforced server-side regardless of the level setting; the level controls **which categories are active** (see below).

## Detection backends

Two detection paths run in tandem with priority:

1. **Azure AI Text Analytics** (`recognizePiiEntities`) — primary if `AZURE_PII_ENDPOINT` + `AZURE_PII_KEY` are set. Highest accuracy, multilingual.
2. **Local CPU model** (GLiNER multi-PII v1) — runs in the optional `guard-service` container at `GUARD_SERVICE_URL`. Apache-2.0 licensed. Falls back here automatically if Azure is unavailable. Default-on for self-hosters who don't want to send data to Azure.

A configurable confidence threshold (default 0.7) filters out low-confidence matches. Lower it for stricter detection (more false positives), raise it for more permissive.

![Privacy Shield settings panel](../img/screenshots/features/privacy-shield-settings/)

## Levels

| Level | Active categories |
|-------|-------------------|
| **Off** | None — prompts go to the model untouched. |
| **Standard** (default) | Email, PhoneNumber, IBAN, BSN, CreditCardNumber, IPAddress, URL (with credentials), Azure keys |
| **Strict** | All Standard + Person, PersonType, DateOfBirth, Address, Organization, PassportNumber, DriversLicenseNumber, SSN, BankAccountNumber, SWIFTCode, ABARoutingNumber |
| **Custom** | Define your own regex categories. Useful for project codenames, internal classification labels (`PROJ-CODENAME-7`). |

Set per-org in **Settings → Organisation → Privacy**, or per-agent in **Studio → Agents** (overrides org default). The org-level config is stored in the `org_privacy_shield_<orgId>` JSONB record.

## Org-level config fields

| Field | Default | What it controls |
|-------|:-------:|-------------------|
| `enabled` | `true` | Master toggle. |
| `dlpEnabled` | `false` | Activates the [DLP gate](dlp.md) (Enterprise+). |
| `dlpMode` | `ask` | `ask` / `auto_redact` / `block`. |
| `azurePiiEnabled` | `true` if env set | Use Azure detection. |
| `localPiiEnabled` | `true` | Use local CPU model. |
| `piiDetectionConfidenceThreshold` | `0.7` | Min confidence (0–1). |
| `moderationEnabled` | `false` | Azure Content Safety on outputs. |
| `showRawPayload` | `false` | Emit tokenised prompt + token map as SSE events for transparency (debug). |
| `euModeEnabled` | `false` | GDPR-aware data handling (logs minimised). |
| `webSearchGuardEnabled` | `true` | Apply PII filter to web-search results before injection. |
| `customSensitiveTerms` | `[]` | Org-defined regex patterns. |

## How redaction works

1. Detect — matches in the outbound payload.
2. Replace each match with a stable placeholder: `[email_1]`, `[iban_1]`, `[person_2]`, …
3. Store the placeholder ↔ original mapping in tenant memory only (`conversationTokenMaps` map, conversation-scoped).
4. Send the redacted payload to the model.
5. On the response, restore placeholders to original values **only on your screen**.

The model never sees the originals. The model provider's logs never contain the originals.

## Token map storage

| | Value |
|---|---|
| Scope | Per-conversation (in-memory `Map`) |
| Per-message | Tokens merged into the conversation's map |
| Token format | `[<category>_<index>]` — e.g. `[email_1]`, `[phone_2]` |
| Cap | 500 tokens per conversation (LRU eviction) |
| TTL | 5 minutes since last access (eviction is purely an LRU + TTL cache; the durable record is the redacted message in Postgres) |

The map lives in memory on the active server replica. With Redis configured, tokens migrate via Redis so that follow-up turns can hit a different replica and still resolve placeholders.

## Showing the user what was redacted

The chat UI shows a small **shield** indicator next to each message that contained redactions. Hover to see counts per category ("3 emails, 1 phone"). Click to expand a side pane showing the per-token mapping (admin-only by default; users can opt in via Settings → Privacy → Show my own redactions).

## Custom regex (Custom level)

Add patterns under **Settings → Organisation → Privacy → Custom terms**:

```
Name:     ProjectCodename
Pattern:  PROJ-[A-Z]+-\d+
Category: project
Action:   redact
```

These run alongside the built-in detectors with the same placeholder mechanism (`[project_1]`).

## Limits and caveats

- Detection is regex- and ML-based, not perfect. Context can slip through (e.g. `our customer Jane lives at...` may not always tag the address depending on confidence).
- Strict-level detection adds ~80–150 ms latency per turn (one extra Azure round-trip or local-model inference).
- Detection runs on the **server**, not the connector — so for Nextcloud users, redaction happens after the connector forwards the prompt.

## Where to next

- [DLP & guardrails](dlp.md) — interactive blocking, audit log, moderation (Enterprise+).
- [Privacy & data flow](../connector/privacy.md) — what's sent at the connector hop.
