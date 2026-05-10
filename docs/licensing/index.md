# Licensing

Bee Flow uses **fair-code** licensing. The frontend (`hive`) and server (`beeflow`) are released under the **Sustainable Use Licence** (SUL). The Nextcloud connector (`connector`) is **AGPL-3.0-or-later**.

> **In short**: you can self-host Bee Flow for free for your own organisation. You cannot offer Bee Flow as a paid service to third parties without a commercial agreement.

## Component licence matrix

| Repo | Licence | Why |
|------|---------|-----|
| `Bee-Flow/hive` (frontend) | Sustainable Use Licence | Allows free self-hosting; protects against pure SaaS resale. |
| `Bee-Flow/beeflow` (server) | Sustainable Use Licence | Same. |
| `Bee-Flow/connector` (NC ExApp) | AGPL-3.0-or-later | Required by the Nextcloud App Store. |
| `Bee-Flow/docs` (this site) | Documentation: CC-BY-4.0 · Code samples: MIT | Encourage reuse of docs. |

## How feature gating works

```
            ┌───────────────────────────┐
            │ Bee Flow licence-server   │  (PRIVATE — Bee Flow only)
            │ Mints signed JWT licenses │
            │ ECDSA P-256 private key   │
            └─────────────┬─────────────┘
                          │ signs
                          ▼
        ┌─────────────────────────────────┐
        │ JWT (delivered by mail/dash)    │
        └─────────────────┬───────────────┘
                          │ admin pastes
                          ▼
   ┌───────────────────────────────────────────────────────┐
   │ Bee Flow server (PUBLIC, fair-code)                   │
   │ Verifies JWT against bundled-public-key.pem           │
   │ requireLicenseFeature(name) middleware enforces gates │
   └───────────────────────────────────────────────────────┘
```

The verification code is part of the open-source server — read it in [`server/license/`](https://github.com/Bee-Flow/beeflow/tree/main/license). Three files:

- `verify.js` — JWT signature verification against the bundled public key.
- `tiers.js` — feature-flag mapping per tier (source of truth).
- `middleware.js` — `requireLicenseFeature(name)` Express middleware.

A licence is a JWT with claims like:

```
{
  "tenantId": "org_abc",
  "tier": "pro",
  "limits": { "users": 25, "agents": 20, "messages": 50000 },
  "features": ["automations","webpages","meeting_notes",...],
  "exp": 1759276800
}
```

The server validates the signature, ensures `exp` is in the future, then exposes the tier + features to every request through `req.license`.

## What stops at the gate vs what degrades

| At the gate | Degrades |
|-------------|----------|
| Premium routes return **403 Forbidden** with `error: "tier_limit"`. | Tier limits (users / agents / messages) — UI stays visible but new-create returns 402. |
| UI nav items disappear (`<RequireTier>`). | Existing automations keep running until the org explicitly stops them — no surprise downgrade mid-run. |
| Webhook automations stop firing on tier downgrade. | Audit log keeps recording — never silently disabled. |

## Refresh policy

Licences are **valid offline** for their `exp` window. The server periodically pings `https://license.beeflow.ai/refresh` (default every 24h) to check for revocation. Set `BEEFLOW_LICENSE_REFRESH_URL=` (empty) to disable refresh entirely — useful for air-gapped deployments. The licence stays valid until `exp` regardless.

## Pages

- [Tiers](tiers.md) — what you get at each level.
- [Applying a licence key](apply.md) — paste the JWT you received.
- [Fair-code FAQ](faq.md) — what you can and can't do.

## Buying a key

Pricing and signup live at [https://beeflow.ai/pricing](https://beeflow.ai/pricing). For volume / non-profit / education discounts, email [tomkooy@beeflow.nl](mailto:tomkooy@beeflow.nl).
