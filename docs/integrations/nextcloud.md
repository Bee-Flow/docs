---
title: "Nextcloud — Files & WebDAV"
---

# Nextcloud — Files & WebDAV

The umbrella Nextcloud integration. Backs all file operations the assistant performs against your Nextcloud.

| | |
|---|---|
| Integration ID | `nextcloud` |
| Auth | NC session (when embedded) **or** OAuth Bearer (standalone) **or** Basic + app password (fallback) |
| Required scope | `FILES`, `DAV` |
| Source | `server/integrations/nextcloudTools.js` (54 KB, comprehensive) |

## Tools exposed

| Tool | Purpose |
|------|---------|
| `nextcloud_list_files` | List files in a folder. |
| `nextcloud_search_files` | Full-text search. |
| `nextcloud_read_file` | Fetch the contents of a file. |
| `nextcloud_upload_file` | Upload a new file or overwrite. |
| `nextcloud_create_folder` | Create a folder. |
| `nextcloud_share_file` | Create an internal share or a public link. |
| `nextcloud_move_file` | Move / rename. |
| `nextcloud_copy_file` | Copy. |
| `nextcloud_delete_file` | Delete (moves to trashbin). |
| `nextcloud_get_file_versions` | Browse the version history. |
| `nextcloud_restore_file_version` | Restore a previous version. |

All tools take paths relative to the user's root (`/Documents/Foo.pdf`, not `/remote.php/dav/files/<uid>/Documents/Foo.pdf`).

## Auth details

### Embedded in Nextcloud (preferred)

Through the connector's HMAC `/nc/*` proxy. The Bee Flow service signs the call with the tenant key; the connector forwards it to NC with `EX-APP-USER-ID: <yourUid>`. AppAPI switches the request context server-side. **No password ever leaves Nextcloud**.

### Standalone (no connector)

OAuth 2.0 with Nextcloud:

```bash
OAUTH_NEXTCLOUD_CLIENT_ID=<app-id>
OAUTH_NEXTCLOUD_CLIENT_SECRET=<secret>
OAUTH_NEXTCLOUD_BASE_URL=https://nc.example.com
```

Register the OAuth client in NC at **Administration → Security → OAuth 2.0 clients**. Redirect URI: `https://your-host/auth/nextcloud/callback`.

### Basic + app password (fallback)

For users who didn't connect via OAuth. The user sets it in **Settings → Account → Integrations → Nextcloud → Add app password**. NC generates the password and stores it AES-encrypted in Postgres (`BEEFLOW_ENCRYPTION_KEY`).

## Scopes & permissions

All tools run under the calling user's NC permissions. The assistant cannot access other users' files; sharing tools require the user's existing share permissions.

## Privacy Shield interaction

File contents pulled via `nextcloud_read_file` are scanned by the Privacy Shield before injection into the prompt. If [DLP](../features/dlp.md) is in `block` mode, prompts referencing file contents with sensitive categories are refused.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | App password rotated | Re-add in user settings. |
| `403 Forbidden on share` | User lacks share permission | NC admin grants the share role. |
| `404 Not Found` | Path typo | Use absolute paths from user root. |
| `Quota exceeded` | NC quota | Free up space or raise quota in NC. |

## Group-level disable

Org admins can disable `nextcloud` at the org or per-group level. Disabling for a group removes all 11 file tools from that group's users. See [Admin → NC integrations](../admin/nc-integrations.md).
