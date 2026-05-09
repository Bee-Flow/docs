# Privacy shield

The Privacy Shield is the in-tenant filter that scans every prompt and tool result before it reaches the language model.

## Detected patterns

| Category | Examples |
|----------|----------|
| Email | `alice@example.com` |
| Phone | `+31 6 12345678`, `(555) 123-4567` |
| IBAN | `NL91 ABNA 0417 1643 00` |
| BSN (NL) | `123456789` |
| BTW / VAT | `NL123456789B01` |
| Credit card | `4111 1111 1111 1111` |
| Passport / ID | configurable per locale |

## How it works

1. Detect → matches in the outbound payload.
2. Replace each match with a stable placeholder: `[EMAIL_1]`, `[IBAN_1]`, …
3. Store the placeholder ↔ original mapping in tenant memory only.
4. Send the redacted payload to the model.
5. On the response, restore placeholders to original values **only on your screen**.

The model never sees the originals. The model provider's logs never contain the originals.

## Levels

- **Off** — no redaction.
- **Standard** (default) — emails, phones, IBANs, BSNs, credit cards.
- **Strict** — adds names, addresses, dates of birth.
- **Custom** — define your own regex categories.

Set per-org in **Settings → Organisation → Privacy**, or per-agent in **Studio → Agents**.
