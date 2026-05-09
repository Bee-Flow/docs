# Permissions & scopes

The connector declares its data-access scopes in `appinfo/info.xml`. AppAPI surfaces these to the admin at install time.

## Required scopes

| Scope | What it grants |
|-------|----------------|
| `FILES` | Read/write on user files (only items the user explicitly points the assistant at). |
| `USER_INFO` | Nextcloud user ID, email, display name. |
| `GROUPS` | Group memberships, used for tenant identification and group-based permissions. |

## Optional scopes

| Scope | What it grants |
|-------|----------------|
| `NOTIFICATIONS` | Send native NC notifications. |
| `CALENDAR` | Read/write calendar items the user references. |
| `CONTACTS` | Read contacts the user references. |
| `MAIL` | Read/draft mail the user references (via the Mail app). |
| `TALK` | Read/post Talk messages the user references. |
| `DAV` | WebDAV access for Files/Calendar/Contacts integrations. |

## What the assistant can and cannot do

| Bee Flow can | Bee Flow cannot |
|--------------|------------------|
| Read a specific file you ask it to summarise | Bulk-export your file system |
| Draft a reply to an email you point at | Read your entire inbox uninvited |
| Create a calendar event you describe | Walk your calendar in the background |
| Search files/mail/contacts on your behalf, scoped to your account | Access another user's data |

Group admins can disable any optional scope per-group in **Settings → Organisation → Integrations**.
