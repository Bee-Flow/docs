# Privacy & data flow

When you act on a Nextcloud item, the connector sends the item to the Bee Flow service over TLS.

## Always sent

- Your Nextcloud user ID, email, display name
- Group memberships (used to identify your tenant and apply group-based permissions)

## Sent on demand

- The contents of items you explicitly point the assistant at (e.g. an email you ask it to summarise, a file you ask it to read)

## Never sent

Bee Flow does **not** bulk-export file contents, mail bodies, calendars or contacts. The connector forwards individual requests; nothing is copied, mirrored or indexed by default.

## Privacy Shield

Before any prompt leaves your tenant, the **Privacy Shield** scans for sensitive data and replaces matches with placeholders:

| Detected | Example | Replacement |
|----------|---------|-------------|
| Email | `alice@example.com` | `[EMAIL_1]` |
| Phone | `+31 6 12345678` | `[PHONE_1]` |
| IBAN | `NL91 ABNA 0417 1643 00` | `[IBAN_1]` |
| BSN | `123456789` | `[BSN_1]` |
| Credit card | `4111 1111 1111 1111` | `[CC_1]` |

The model only ever sees the placeholders. The original values are restored in the reply, only on your screen.

## Encryption in transit

All traffic between the connector and the Bee Flow service uses TLS 1.2+. Nextcloud-side traffic uses your existing HTTPS configuration.

## Full policy

See <https://beeflow.ai/privacy>.
