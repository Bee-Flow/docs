---
title: REST reference
---

# REST reference

The most-used endpoints, grouped by area. Auth column abbreviations: **P** = public · **U** = user JWT · **A** = admin JWT · **S** = signed (HMAC / AppAPI).

## Health

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/health` | P | `{status, version, tier}` |
| GET | `/api` | P | API info |
| GET | `/metrics` | P¹ | Prometheus metrics (gated by `METRICS_BASIC_AUTH`) |

¹ Optional Basic-auth via `METRICS_BASIC_AUTH=user:pass`.

## Auth & sessions

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/auth/setup-status` | P | Is the org bootstrapped? OAuth providers configured? Available locales |
| POST | `/auth/setup` | P | First-time admin password setup (one-shot) |
| POST | `/auth/admin-login` | P | Username/password login |
| POST | `/auth/signup` | P | User registration (if enabled) |
| GET | `/auth/invite/:token` | P | Resolve invite token |
| POST | `/auth/logout` | U | End session |
| GET | `/auth/user` | U | Current user record |
| GET | `/auth/my-permissions` | U | Permissions, groups, orgs, beta features |
| POST | `/auth/update-profile` | U | Update profile (name, avatar, language) |
| POST | `/api/session-token` | U | Issue popup→iframe session token |
| GET | `/auth/admin/signup-settings` | A | Read signup config |
| PUT | `/auth/admin/signup-settings` | A | Write signup config |
| GET | `/auth/admin/waitlist` | A | List pending signups |
| POST | `/auth/admin/waitlist/:userId/approve` | A | Approve waitlist entry |
| POST | `/auth/admin/waitlist/:userId/reject` | A | Reject waitlist entry |
| POST | `/auth/pending-signup` | P | Add to waitlist |
| GET | `/auth/organizations/public` | P | Public organisations (for embedded chat) |

## OAuth & SSO

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/auth/google/login` | P | Start Google OAuth |
| GET | `/auth/google/callback` | P | Google OAuth callback |
| GET | `/auth/microsoft/login` | P | Start Microsoft OAuth |
| GET | `/auth/microsoft/callback` | P | Microsoft OAuth callback |
| GET | `/auth/github/login` | P | Start GitHub OAuth |
| GET | `/auth/github/callback` | P | GitHub OAuth callback |
| GET | `/auth/nextcloud/login` | P | Start NC OAuth (standalone) |
| GET | `/auth/nextcloud/callback` | P | NC OAuth callback |
| GET | `/auth/saml/metadata` | P | SAML SP metadata XML |
| POST | `/auth/saml/acs` | P | SAML assertion consumer |
| GET | `/auth/login-pickup` | P | OAuth callback redirect handler |

## Connector handshake

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| POST | `/auth/connector/bootstrap` | S | NC connector → SaaS first-time tenant provisioning |
| GET | `/auth/nc-handshake` | S | NC SPA → SaaS short-lived JWT issuance |
| POST | `/auth/webhook/nc-user-sync` | S | NC events forwarded by the connector |
| POST | `/auth/nc-consent` | U | Record user's first-load privacy consent |

## Users & API keys

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/users` | A | List org users |
| POST | `/api/users` | A | Invite user |
| PATCH | `/api/users/:id` | A | Update user |
| DELETE | `/api/users/:id` | A | Delete user (soft) |
| GET | `/api/api-keys` | U | List my keys |
| POST | `/api/api-keys` | U | Create new key (returned once) |
| DELETE | `/api/api-keys/:id` | U | Revoke key |

## Organisations

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/organisation` | U | Current org settings |
| PATCH | `/api/organisation` | A | Update org settings |
| GET | `/api/organisation/groups` | U | List groups |
| POST | `/api/organisation/groups` | A | Create group |
| PATCH | `/api/organisation/groups/:id` | A | Update group |
| DELETE | `/api/organisation/groups/:id` | A | Delete group |
| POST | `/api/organisation/groups/:id/members` | A | Add member |
| DELETE | `/api/organisation/groups/:id/members/:userId` | A | Remove member |

## Agents

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/agents` | U | List visible agents |
| POST | `/api/agents` | U | Create agent |
| GET | `/api/agents/:id` | U | Read agent |
| PATCH | `/api/agents/:id` | U | Update agent |
| DELETE | `/api/agents/:id` | U | Delete agent |
| POST | `/api/agents/:id/publish` | U | Publish to Marketplace |
| POST | `/api/agents/:id/duplicate` | U | Fork an existing agent |
| GET | `/api/agents/:id/tools` | U | Resolved tool list for this agent + user |
| GET | `/api/marketplace/agents` | P | Browse public agents |

## Conversations & messages

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/conversations` | U | List my conversations |
| POST | `/api/conversations` | U | Start a new conversation |
| GET | `/api/conversations/:id` | U | Read |
| DELETE | `/api/conversations/:id` | U | Soft delete |
| GET | `/api/conversations/:id/messages` | U | Paginated message history |
| POST | `/api/conversations/:id/title` | U | Re-generate title |
| POST | `/api/conversations/:id/branch` | U | Branch into a thread |

## Chat (streaming)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| POST | `/api/chat` | U | Stream a turn (SSE) — see [Streaming](sse.md) |
| POST | `/api/chat/:msgId/cancel` | U | Cancel an in-flight turn |
| POST | `/api/chat/:msgId/dlp-decision` | U | Resolve a `dlp_finding` (allow/redact/block) |
| POST | `/api/chat/:msgId/feedback` | U | Thumbs up/down + optional comment |

## Knowledge bases

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/knowledge` | U | List KBs |
| POST | `/api/knowledge` | U | Create KB |
| GET | `/api/knowledge/:id` | U | Read KB |
| PATCH | `/api/knowledge/:id` | U | Update settings |
| DELETE | `/api/knowledge/:id` | U | Delete KB |
| GET | `/api/knowledge/:id/documents` | U | List documents |
| POST | `/api/knowledge/:id/documents` | U | Add document (multipart) |
| DELETE | `/api/knowledge/:id/documents/:docId` | U | Remove document |
| POST | `/api/knowledge/:id/search` | U | Search query |
| POST | `/api/knowledge/:id/reindex` | U | Re-embed all chunks |
| GET | `/api/marketplace/knowledge` | P | Public KBs |

## Automations (Pro+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/automation` | U | List automations |
| POST | `/api/automation` | U | Create |
| GET | `/api/automation/:id` | U | Read |
| PATCH | `/api/automation/:id` | U | Update |
| DELETE | `/api/automation/:id` | U | Delete |
| POST | `/api/automation/:id/runs` | U | Trigger a manual run |
| GET | `/api/automation/:id/runs` | U | List runs |
| GET | `/api/automation/:id/runs/:runId` | U | Run detail (steps, logs) |
| POST | `/api/automation/:id/runs/:runId/cancel` | U | Cancel running |
| POST | `/api/automation/:id/runs/:runId/resume` | U | Resume from awaiting step |
| POST | `/api/automation/:id/runs/:runId/retry-from/:stepId` | U | Retry from a specific step |
| POST | `/api/automation/webhook/:id` | S¹ | Webhook trigger entry |
| POST | `/api/automation/builder/validate` | U | Validate a draft graph |

¹ Auth via webhook token in URL or header.

## Webpages (Pro+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/webpages` | U | List crawled pages |
| POST | `/api/webpages` | U | Add a URL to crawl |
| GET | `/api/webpages/:id` | U | Read |
| DELETE | `/api/webpages/:id` | U | Remove |

## Meeting notes & transcriptions (Pro+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/transcriptions` | U | List |
| POST | `/api/transcriptions` | U | Submit audio |
| GET | `/api/transcriptions/:id` | U | Read |
| POST | `/api/meet-bot/join` | U | Send the meeting bot to a URL |
| POST | `/api/meet-bot/:id/leave` | U | Recall the bot |

## Skills (Pro+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/skills` | U | List installed skills |
| POST | `/api/skills` | U | Install a skill |
| DELETE | `/api/skills/:id` | U | Uninstall |
| GET | `/api/marketplace/skills` | P | Browse public skills |

## Ticket assistant (Pro+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/ticket-assistant/tickets` | U | List tickets |
| POST | `/api/ticket-assistant/tickets` | U | Create from email |
| GET | `/api/email-kb/inbox` | U | Inbox view |

## Integrations

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/integrations` | U | List my connected integrations |
| POST | `/api/integrations/:id/connect` | U | Start OAuth/key flow |
| DELETE | `/api/integrations/:id` | U | Disconnect |
| GET | `/admin/:orgId/nc-integrations` | A | Org-level NC integration toggles |
| PUT | `/admin/:orgId/nc-integrations` | A | Update org-level toggles |
| GET | `/admin/:orgId/nc-integrations/groups` | A | Per-group disable lists |
| PUT | `/admin/:orgId/nc-integrations/groups/:groupId` | A | Update per-group disables |

## License

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/license/status` | U | Active tier + features + limits |
| POST | `/api/license/apply` | A | Apply a JWT licence key |
| DELETE | `/api/license` | A | Revert to Community |

## Audit & compliance (Enterprise+)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/guardrails/events` | A | Query the guardrail audit log |
| GET | `/api/guardrails/events.csv` | A | CSV export |
| GET | `/api/compliance/gdpr/requests` | A | List DSRs |
| POST | `/api/compliance/gdpr/requests` | A | Open a DSR |
| GET | `/api/compliance/gdpr/archive/:userId` | A | Archive download |

## Webhooks

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| POST | `/webhook/audit-events` | S | Receive SIEM-bound audit events (self) |
| POST | `/webhook/license-revocation` | S | Receive licence revocation push |

## Health & metrics (operations)

| Method | Path | Auth | Purpose |
|--------|------|:----:|---------|
| GET | `/api/health` | P | Liveness + readiness |
| GET | `/api/health/db` | A | Database connectivity check |
| GET | `/api/health/redis` | A | Redis connectivity check |
| GET | `/api/health/integrations` | A | Per-integration health |

## Notes

- All `POST` create endpoints accept `Idempotency-Key` ([details](index.md#idempotency)).
- Errors are JSON ([format](index.md#error-format)).
- Streaming endpoints (`/api/chat`, `/api/voice/turn`) speak SSE — see [Streaming](sse.md).
