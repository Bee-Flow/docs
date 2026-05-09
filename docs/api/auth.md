# Authentication

Bee Flow accepts session JWTs in either:

- An `Authorization: Bearer <jwt>` header, or
- A `bf_session` cookie (set by `/auth/login`).

## Obtain a token

### Username / password

```bash
curl -X POST https://beeflow.example.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email": "alice@example.com", "password": "..."}'
```

```json
{ "token": "eyJhbG...", "user": { "id": "...", "email": "..." } }
```

### Nextcloud session

When Bee Flow is embedded inside Nextcloud, the connector signs the user's NC session and the server trusts it. There's no explicit login call from the SPA — the session is established via `/auth/nc-handshake`, called from the connector with an AppAPI signature.

### API key (machine-to-machine)

For server-to-server access:

1. **Settings → Organisation → API keys → Create**.
2. Use the long-lived key as a Bearer token.

API keys never expire automatically; rotate them yourself.

## Token lifetime

| Token type | Lifetime |
|------------|----------|
| Session JWT (browser) | 14 days, renewed on activity |
| API key | until revoked |
| NC handshake JWT | 1 hour, transparently re-issued |
