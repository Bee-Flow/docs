# Licensing

Bee Flow uses **fair-code** licensing. The frontend and server are open-source under the **Sustainable Use Licence**; the Nextcloud connector is **AGPL-3.0-or-later**.

> **In short**: you can self-host Bee Flow for free for your own organisation. You cannot offer Bee Flow as a paid service to third parties without a commercial agreement.

## How feature gating works

```
            ┌───────────────────────────┐
            │ Bee Flow licence-server   │  (PRIVATE — Bee Flow only)
            │ Mints signed JWT licenses │
            │ ECDSA private key         │
            └─────────────┬─────────────┘
                          │ signs
                          ▼
        ┌─────────────────────────────────┐
        │ JWT (delivered by mail)         │
        └─────────────────┬───────────────┘
                          │ admin pastes
                          ▼
   ┌───────────────────────────────────────────────────────┐
   │ Bee Flow server (PUBLIC, fair-code)                   │
   │ Verifies JWT against bundled-public-key.pem           │
   │ requireLicenseFeature(name) middleware enforces gates │
   └───────────────────────────────────────────────────────┘
```

You can read the verification code in [`server/license/`](https://github.com/Bee-Flow/beeflow/tree/main/license) — it's part of the open-source server.

## Pages

- [Tiers](tiers.md) — what you get at each level.
- [Applying a license key](apply.md) — paste the JWT you received.
- [Fair-code FAQ](faq.md) — what you can and can't do.

## Buying a key

Pricing and signup live at [beeflow.ai/pricing](https://beeflow.ai/pricing).
