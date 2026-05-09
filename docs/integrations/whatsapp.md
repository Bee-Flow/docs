# WhatsApp

Send WhatsApp messages via the Twilio backend.

## Setup

1. Provision a Twilio account and a WhatsApp-enabled sender (sandbox or production).
2. Set environment:
   ```bash
   WHATSAPP_TWILIO_SID=ACxxxxxxxx
   WHATSAPP_TWILIO_TOKEN=...
   WHATSAPP_FROM_NUMBER=whatsapp:+14155238886   # sandbox example
   ```
3. Restart server.

## Tools

| Tool | Purpose |
|------|---------|
| `whatsapp_send_message` | Send a text message. |
| `whatsapp_send_template` | Send a pre-approved template (production only). |

## Sandbox vs production

Twilio's WhatsApp sandbox is fine for testing — recipients must opt-in by texting a join phrase first. For production messaging, you must apply for a WhatsApp Business profile through Twilio (24+ hour review).

## Use cases

- (Automation) Notify on-call engineer's WhatsApp on a critical incident.
- (Customer support) Forward a Bee Flow chat conversation to a customer's WhatsApp.

## Privacy

Bodies pass through the Privacy Shield. Phone numbers in the recipient list are *the* destination — they're not redacted (a placeholder wouldn't deliver). The phone number is logged in the audit trail with the rest of the call metadata.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `21408 Permission denied` | Recipient hasn't opted in (sandbox) | Have them text the sandbox join phrase. |
| `63016 No template` (production) | Free-text outside 24h session | Use a pre-approved template. |
| `21610 Unsubscribed` | Recipient blocked your number | They re-opt in. |
