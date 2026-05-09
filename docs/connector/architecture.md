# Architecture

## Routes and access levels

The connector serves a strict allow-list of paths declared in [`appinfo/info.xml`](https://github.com/Bee-Flow/connector/blob/main/appinfo/info.xml). Anything not matched is rejected by AppAPI before it reaches the connector.

| Path | Verb | Access | Purpose |
|------|------|--------|---------|
| `^$`, `^index.html`, `^favicon.ico`, `^assets/`, `^js/`, `^img/`, `^bee-flow-logo.*` | GET | PUBLIC | Static SPA shell |
| `^api/` | GET / POST / PUT / DELETE / PATCH | PUBLIC | SaaS-proxied REST + SSE |
| `^auth/` | GET / POST / PUT / DELETE / PATCH | PUBLIC | SaaS-proxied auth + OAuth flows |
| `^heartbeat$` | GET | PUBLIC | AppAPI liveness probe |
| `^init$` | POST | ADMIN | AppAPI lifecycle install hook |
| `^enabled$` | PUT | ADMIN | AppAPI lifecycle enable/disable hook |
| `^webhook/` | POST | ADMIN | NC events_listener forwarder |
| `^nc/` | GET / POST / PUT / DELETE / PATCH / PROPFIND / REPORT / MKCOL / MOVE / COPY | PUBLIC | HMAC-signed reverse proxy back to NC |

`PUBLIC` here means *the route is reachable without an admin role* — not that authentication is skipped. AppAPI signs every call regardless of access level.

## Lifecycle

Per the [NC AppAPI spec](https://nextcloud.github.io/app_api/notes_for_developers/ExAppLifecycle.html):

```
Install → POST /init           ─▶ HTTP 200 immediately
       ⌙                          background work runs in setImmediate()
       PUT /ocs/v2.php/apps/app_api/ex-app/status {progress: N}
       PUT /ocs/v2.php/apps/app_api/ex-app/status {progress: 100}

Up    → GET /heartbeat          ─▶ {"status":"ok"}     (every ~10s by AppAPI)

Enable/disable → PUT /enabled?enabled=0|1
```

### `/init`

1. Returns `{"status":"ok"}` within ~50 ms.
2. Schedules `runInitInBackground()` via `setImmediate`.
3. Background work in three phases:
   - **25%** — bootstrap (provision tenant key if `BEEFLOW_TENANT_KEY=auto`).
   - **60%** — register top-bar entry + embed script (parallel).
   - **100%** — register 5 event listeners (parallel, with the AppAPI-33.0.0 short-circuit).
4. Errors during background setup → `reportInitProgress(0, errorMessage)` so the AppAPI deploy log surfaces them.

### `/heartbeat`

Unauthenticated, returns `{status:'ok'}`. Nextcloud requires the connector to respond within 10 minutes of startup. Zero side effects.

### `/enabled?enabled={0|1}`

Authenticated. Logs the state change. Reserved for future suspend / resume hooks; no immediate action today.

## AppAPI signature on inbound calls

Every AppAPI-proxied call carries:

```
AUTHORIZATION-APP-API: base64(<userId>:<APP_SECRET>)
EX-APP-ID: bee_flow
EX-APP-VERSION: 0.1.0
EX-APP-USER-ID: <ncUid or empty>
```

The connector validates the shared secret on every request and rejects with 401 on mismatch. `EX-APP-USER-ID` is empty for service-level calls (e.g. `/init`) and populated for user-attributed calls (e.g. an API call originated by a logged-in user).

## HMAC `/nc/*` reverse-proxy

The Bee Flow service can call back into Nextcloud through a separate proxy. Used for any API the assistant needs (Files via WebDAV, Mail via the Mail app REST API, Calendar via CalDAV, etc.).

### Allowed paths

| Path prefix | Used for |
|-------------|----------|
| `/ocs/*` | Provisioning, capabilities, user info |
| `/remote.php/dav/*` | WebDAV, CalDAV, CardDAV |
| `/index.php/apps/*` | Mail, Deck, Notes, Talk, Activity |

Anything else returns 404.

### Signature

```
message = "{unixSeconds}\n{HTTP_METHOD}\n{path}\n{ncUid}"
sig     = HMAC-SHA256(message, tenantKey)
header  = X-Beeflow-Sig: {unixSeconds}.{hexSig}
```

Required headers:

- `X-Beeflow-Sig` — timestamp + HMAC signature
- `X-Beeflow-NC-Uid` — Nextcloud user ID to impersonate (empty for service-level)

Verification (server side):

1. Reject if `unixSeconds` is outside ±300s clock skew (`BEEFLOW_SIG_SKEW_SECONDS`).
2. Recompute HMAC with the loaded tenant key.
3. Constant-time compare with `timingSafeEqual`.
4. Return 401 if the tenant key isn't loaded yet (bootstrap incomplete).

### Tenant key source

| Source | Priority |
|--------|----------|
| `BEEFLOW_TENANT_KEY` env var | 1 (highest) — used if not literal `auto` |
| `${APP_PERSISTENT_STORAGE}/tenant-key.json` | 2 — cached after first bootstrap, file mode `0600` |
| Bootstrap call to SaaS | 3 — issued on first `/init` |

## Bootstrap flow

Triggered on startup and again on `/init` if no cache is found.

1. **Skip if explicit** — if `BEEFLOW_TENANT_KEY` is not `auto`, use that key directly.
2. **Cache check** — read the persistent file at `APP_PERSISTENT_STORAGE/tenant-key.json`.
3. **Gather metadata** — anonymous OCS call to fetch the NC instance ID, version, and theming name.
4. **Discover admin**:
   - **Fast path** — `GET /ocs/v2.php/cloud/groups/admin/users`, single round-trip.
   - **Fallback** — walk `/ocs/v2.php/cloud/users` in parallel batches of 5, looking for first user in the `admin` group.
5. **Call SaaS bootstrap** — `POST {apiBaseUrl}/auth/connector/bootstrap` with NC instance metadata in headers.
6. **Anti-spoofing** — the SaaS independently re-fetches NC capabilities to confirm the metadata matches.
7. **Persist** — store the returned `{tenantKey, organizationId, organizationName}` in the cache file.

If any step fails, the connector logs the error and continues; the admin sees "ExApp unhealthy" in NC, which surfaces the misconfiguration.

## Event subscriptions

The connector subscribes to 5 NC events on first init:

| Event class | NC event | Mapped to webhook event |
|-------------|----------|--------------------------|
| `OCP\User\Events\UserCreatedEvent` | User added | `user.created` |
| `OCP\User\Events\UserDeletedEvent` | User removed | `user.deleted` |
| `OCP\User\Events\UserChangedEvent` | User updated (mail, name) | `user.updated` |
| `OCP\Group\Events\UserAddedEvent` | User joined a group | `group.member_added` |
| `OCP\Group\Events\UserRemovedEvent` | User left a group | `group.member_removed` |

Per-call timeout: 3 seconds. Calls run in parallel. NC enforces unique `(appId, eventType, actionHandler)` and returns 409 on duplicate (idempotent re-init). NC 33.0.0's broken `EventsListenerController` returns 500 — the connector probes the first call and skips the rest if it sees the controller-missing error message.

## Webhook `/webhook/nc-events`

NC's events listener POSTs to this path on every fired event. Payload (best-effort field extraction):

```json
{
  "eventType": "OCP\\User\\Events\\UserCreatedEvent",
  "userId": "alice",
  "groupId": "engineering"
}
```

The connector maps the event class to `user.created` / `user.deleted` / `user.updated` / `group.member_added` / `group.member_removed` and forwards to the SaaS at `POST /auth/webhook/nc-user-sync`, signed with the same tenant-key HMAC. 10s timeout, best-effort — failures log a warning and return 200 to NC (NC won't retry).

## Connector environment variables

Set by AppAPI / Dockerfile (you don't normally touch these):

| Var | Default | Purpose |
|-----|---------|---------|
| `APP_ID` | `bee_flow` | ExApp identifier |
| `APP_SECRET` | (required) | AppAPI shared secret |
| `APP_VERSION` | `0.0.0` | Version string |
| `APP_HOST` | `0.0.0.0` | Always bound to all interfaces (HaRP compat) |
| `APP_PORT` | `8080` | Internal listen port |
| `APP_PERSISTENT_STORAGE` | `/data` | Tenant-key cache directory |
| `NEXTCLOUD_URL` | (required) | Base URL of the NC instance |

Admin-configurable via `occ app_api:app:setenv`:

| Var | Default | Purpose |
|-----|---------|---------|
| `BEEFLOW_TENANT_KEY` | `auto` | Tenant key, or literal `auto` for one-click install |
| `BEEFLOW_API_BASE_URL` | `https://api.beeflow.ai` | Bee Flow service URL — override for staging / on-prem |
| `BEEFLOW_JWT_TTL_SECONDS` | `300` | JWT expiry (short on purpose) |
| `BEEFLOW_SIG_SKEW_SECONDS` | `300` | HMAC clock-skew tolerance (±5 min) |

## Why returning 200 immediately matters

Earlier versions of the connector ran every step of `/init` synchronously — including ~21 sequential event-listener registrations (10s timeout each). Worst-case install was ~5 minutes; AppAPI's `--wait-finish` polled forever. The current implementation returns within ~50 ms and runs setup in `setImmediate`, reporting progress to AppAPI via `PUT /ocs/v2.php/apps/app_api/ex-app/status`. This is the spec — see [NC AppAPI lifecycle docs](https://nextcloud.github.io/app_api/notes_for_developers/ExAppLifecycle.html).
