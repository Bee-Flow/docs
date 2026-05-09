# Authentication

Bee Flow accepts session JWTs in either:

- An `Authorization: Bearer <jwt>` header
- A `bf_session` cookie (set by `/auth/login`)

Both work; the header is recommended for non-browser clients.

## Three ways to obtain credentials

| Method | When to use | Lifetime |
|--------|-------------|----------|
| Username / password | Self-hosted standalone, no NC | 14 days, sliding |
| Nextcloud session | Embedded in Nextcloud (connector flow) | 1 hour, transparently re-issued |
| API key | Server-to-server / scripts | until revoked |
| OAuth (Google/MS) | Standalone with social login | 14 days, sliding |
| SAML SSO | Enterprise, IdP-driven | matches IdP session |

## Username / password

```http
POST /auth/admin-login
Content-Type: application/json

{ "email": "alice@example.com", "password": "..." }
```

Response:

```json
{
  "token": "eyJhbG...",
  "user": {
    "id": "u_abc",
    "email": "alice@example.com",
    "displayName": "Alice",
    "role": "admin"
  }
}
```

Pass the token in subsequent requests:

```http
GET /api/agents
Authorization: Bearer eyJhbG...
```

The first admin password is set during the install wizard via `POST /auth/setup`. After that, additional users sign up through `POST /auth/signup` (if signup is enabled) or are invited by an admin.

## Nextcloud session

When Bee Flow is embedded inside Nextcloud, the [connector](../connector/index.md) handshakes the user's NC session for a short-lived Bee Flow JWT. There's no explicit login from the SPA.

```
┌────────┐   AppAPI signed call      ┌──────────┐  HMAC-signed       ┌────────┐
│ NC SPA │ ───────────────────────▶  │ Connector│ ─────────────────▶ │ Server │
│        │   GET /auth/nc-handshake  │          │                    │        │
└────────┘                           └──────────┘                    └────────┘
                                                                        │
                                              ┌─── short-lived JWT ─────┘
                                              ▼
                                          { token, user }
```

The JWT carries `tenantId`, `ncUid`, `roles`, `exp`. TTL is `BEEFLOW_JWT_TTL_SECONDS` (default 300 s — short on purpose). The SPA auto-refreshes on 401.

## API keys (server-to-server)

For scripts, automations, integrations:

1. **Settings → Organisation → API keys → Create**.
2. Pick a name + scope (full / read-only).
3. Copy the key — it's shown once.

```http
GET /api/agents
Authorization: Bearer bfk_<long_random_string>
```

API keys never expire automatically. Rotate via the same panel; revoking takes effect within 60 s.

API keys belong to the user who created them and inherit their permissions. Org-admin keys can manage org settings; user keys can only manage their own resources.

## OAuth (social login)

Configure Google / Microsoft / GitHub OAuth in `.env` (see [env reference](../self-hosting/env.md)). The login screen shows a button per configured provider:

```http
GET /auth/google/login    → 302 to Google
                          → callback /auth/google/callback
                          → sets bf_session cookie + redirects to /app
```

The first user to log in via OAuth becomes a regular user in the org indicated by the email domain (or in a fallback "default" org if no domain match).

## SAML SSO (Enterprise)

In **Settings → Organisation → SSO** paste your IdP metadata XML. Bee Flow exposes:

- ACS URL: `https://your-host/auth/saml/acs`
- Entity ID: `https://your-host/auth/saml/metadata`

Required attributes: `email`, `displayName`. Optional: `groups` (mapped to NC-style group memberships for integration gating).

Once SAML is enabled, the username/password form is hidden by default — set `ALLOW_PASSWORD_LOGIN=true` to keep it as a fallback for break-glass access.

## Token lifetime

| Token type | Lifetime | Renewal |
|------------|----------|---------|
| Username/password JWT | 14 days, sliding | refreshed on every successful API call |
| NC handshake JWT | 1 hour | re-issued via `/auth/nc-handshake` |
| API key | until revoked | manual rotation |
| OAuth session JWT | 14 days, sliding | refreshed on activity |
| SAML SSO JWT | matches IdP `notOnOrAfter` | per-IdP behaviour |

## Header / cookie precedence

If both are present, **`Authorization` header wins**. This lets a browser session coexist with API-key calls from the same origin.

## Logout

```http
POST /auth/logout
```

Clears the cookie + records the JWT in a server-side denylist for its remaining lifetime. API keys are not affected — revoke them in the UI.

## Inspecting your token

```http
GET /auth/user
Authorization: Bearer <jwt>
```

Returns the user record + the resolved tier features:

```json
{
  "id": "u_abc",
  "email": "alice@example.com",
  "displayName": "Alice",
  "role": "admin",
  "organizationId": "org_xyz",
  "tier": "pro",
  "features": ["automations", "voice", "..."],
  "limits": { "users": 25, "agents": 20, "messages": 50000 }
}
```

## Common errors

| Status | `error` | Meaning |
|--------|---------|---------|
| 401 | `missing_token` | No `Authorization` or `bf_session`. |
| 401 | `invalid_token` | JWT signature mismatch or revoked. |
| 401 | `expired_token` | `exp` in the past. Re-login or refresh. |
| 403 | `forbidden` | Auth ok, role insufficient. |
| 403 | `license_feature_required` | Tier doesn't include the feature. |
