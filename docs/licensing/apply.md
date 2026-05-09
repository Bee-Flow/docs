# Applying a license key

After purchase, you receive a JWT in your inbox. To apply:

1. Open Bee Flow as an organisation admin.
2. Go to **Settings → Organisation → License & usage**.
3. Paste the JWT into the **License key** field and click **Apply**.

The server verifies the signature against the bundled public key and updates the active tier immediately. Premium features become available without a restart.

![Applying a license key](../img/screenshots/license-apply.png)

## Verifying the active tier

```bash
curl https://beeflow.example.com/api/license/status
```

```json
{
  "tier": "pro",
  "expiresAt": "2027-05-09T00:00:00Z",
  "features": ["automations", "voice", "..."],
  "limits": {"users": 25, "agents": 20, "messages": 50000}
}
```

## Rotating

Paste a new key at any time — it overwrites the old one.

## Removing

Clear the field and click **Apply**. The org reverts to the Community tier; premium features become unavailable but data is preserved.

## Troubleshooting

- **"Invalid signature"** — the key was tampered with, or you pasted a key for a different deployment.
- **"License expired"** — renewal time. Reach out to <tomkooy@beeflow.nl>.
- **"Tier limit exceeded"** — you have more users/agents/messages than your tier allows. Either upgrade, or trim down.
