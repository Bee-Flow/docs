---
title: Google Workspace
---

# Google Workspace

Bee Flow connects to Google Workspace via OAuth 2.0. Each Workspace service is a separate integration ID with its own OAuth scopes.

## Setup

1. Create a Google Cloud project at [https://console.cloud.google.com](https://console.cloud.google.com).
2. Enable the APIs you want: Gmail, Calendar, Drive, Docs, Keep, People, Admin SDK.
3. **APIs & Services → Credentials → Create OAuth client ID** — type Web Application.
4. Add redirect URI: `https://your-host/auth/google/callback`.
5. Set environment variables:
   ```bash
   OAUTH_GOOGLE_CLIENT_ID=...apps.googleusercontent.com
   OAUTH_GOOGLE_CLIENT_SECRET=...
   ```
6. Restart the server. Users will see "Connect Google" buttons in **Settings → Account → Integrations**.

For org-wide Workspace deployments, register Bee Flow as an internal app in the Google Workspace admin console.

## Integrations & scopes

| Integration ID | Scope(s) | Tools |
|----------------|----------|-------|
| `gmail` | `gmail.readonly`, `gmail.compose`, `gmail.send` | `gmail_search`, `gmail_read`, `gmail_read_attachment`, `gmail_compose`, `gmail_send`, `gmail_reply` |
| `google-calendar` | `calendar` | `gcal_list`, `gcal_search`, `gcal_create_event`, `gcal_update_event`, `gcal_delete_event` |
| `google-drive` | `drive.readonly`, `drive.file` | `gdrive_list`, `gdrive_search`, `gdrive_read`, `gdrive_upload` |
| `google-docs` | `documents.readonly` | `gdocs_read`, `gdocs_create`, `gdocs_update` |
| `google-keep` | `keep` | `gkeep_list`, `gkeep_create`, `gkeep_search` |
| `google-contacts` | `contacts.readonly` | `gcontacts_list`, `gcontacts_search` |
| `google-groups` | (delegated admin) | `ggroups_list_members` |

The minimum-scope principle applies: Bee Flow asks only for what's needed by the integrations you enable.

## Per-tool detail

### Gmail

- **Reading** — `gmail_search` accepts the same query syntax as the Gmail UI (`from:alice subject:invoice newer_than:7d`).
- **Composing** — `gmail_compose` creates a draft. Sending requires `gmail.send` scope and an explicit `gmail_send` call. This split is intentional — agents can suggest replies without auto-sending.
- **Replies** — `gmail_reply` preserves `In-Reply-To` and `References` headers so threading works.

### Calendar

- All-day vs timed events handled correctly.
- Recurrence supported via RRULE.
- Conference link generation (Google Meet) on create when `conferenceData.createRequest` is set.

### Drive

- Read includes Google-native formats (Docs / Sheets / Slides) — they're exported to plain text / Markdown for the model.
- Upload sends the binary; `mimeType` auto-detected.
- Shared-with-me + My Drive both searchable.

### Docs

- Read returns the document content as plain text + structured headings.
- Update applies a list of edits (insert / replace / delete ranges).

### Keep

- Notes only (not "Reminders" — those are part of Google Tasks).

### Contacts

- Returns name, email, phone, organisation, photo URL.

### Groups

- Workspace admin-only — used by automations that need to enumerate group members.

## Auto-refresh

The Google Auth library auto-refreshes access tokens on 401. Refresh tokens are stored AES-encrypted in Postgres (using `BEEFLOW_ENCRYPTION_KEY`).

## Privacy

All bodies retrieved from Gmail / Drive / Docs flow through the Privacy Shield. With Strict mode, contact names, email addresses and phone numbers are tokenised.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_grant` on refresh | Token revoked / user changed password | User reconnects in Settings → Integrations. |
| `403 insufficient scope` | App requested fewer scopes than the tool needs | Add the scope and have the user reconnect. |
| `429 quota exceeded` | Per-day API quota | Raise quota in Google Cloud Console or throttle. |
| `Drive item too large` | >`BEEFLOW_REQUEST_BODY_LIMIT` | Raise limit or skip body and use metadata only. |
