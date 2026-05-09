# Architecture

```
                                  Browser
                                    │
                                    │ Nextcloud session cookie
                                    ▼
                     ┌──────────────────────────────┐
                     │  Nextcloud (your instance)   │
                     │  AppAPI signed proxy         │
                     └──────────────┬───────────────┘
                                    │ EX-APP-USER-ID + AppAPI signature
                                    ▼
                     ┌──────────────────────────────┐
                     │  Bee Flow connector (ExApp)  │
                     │  ghcr.io/bee-flow/connector  │
                     └───────┬───────────────┬──────┘
                             │               │
                  static SPA │               │ HMAC-signed
                  (hive)     │               │ /nc/* reverse proxy
                             ▼               ▼
                    ┌────────────────┐    ┌──────────────────┐
                    │  Browser SPA   │    │   Nextcloud APIs │
                    └────────┬───────┘    │  Files / Mail /  │
                             │            │  Calendar / ...  │
                             │ REST + SSE └──────────────────┘
                             ▼
                  ┌──────────────────────┐
                  │  Bee Flow service    │
                  │  api.beeflow.ai or   │
                  │  self-hosted server  │
                  └──────────────────────┘
```

## Routes

The connector serves a strict allow-list of paths (declared in `appinfo/info.xml`):

| Path | Purpose |
|------|---------|
| `^$`, `^index.html`, `^assets/`, `^js/`, `^img/` | Static SPA shell |
| `^api/`, `^auth/` | SaaS-proxied REST + SSE |
| `^heartbeat`, `^init`, `^enabled` | AppAPI lifecycle hooks |
| `^webhook/nc-events` | Forwarded NC events (user/group changes) |
| `^nc/` | HMAC-signed reverse proxy back to NC |

Anything not matched is rejected by AppAPI before reaching the connector.

## Async lifecycle

Per the [NC AppAPI spec](https://nextcloud.github.io/app_api/notes_for_developers/ExAppLifecycle.html), `/init` returns HTTP 200 immediately and reports progress asynchronously via `PUT /ocs/v2.php/apps/app_api/ex-app/status`. Background setup (bootstrap, top-bar registration, embed-script registration, event subscriptions) runs in `setImmediate` after the response.
