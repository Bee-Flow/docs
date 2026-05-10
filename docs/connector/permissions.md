---
title: "Permissions & scopes"
---

# Permissions & scopes

The connector declares its data-access scopes in [`appinfo/info.xml`](https://github.com/Bee-Flow/connector/blob/main/appinfo/info.xml). AppAPI surfaces these to the admin at install time. Reviewers and auditors can read the manifest to audit exactly what access the connector requests, before installing.

## Scopes the connector declares

```xml
<scopes>
    <required>
        <value>FILES</value>
        <value>USER_INFO</value>
        <value>GROUPS</value>
    </required>
    <optional>
        <value>NOTIFICATIONS</value>
        <value>CALENDAR</value>
        <value>CONTACTS</value>
        <value>MAIL</value>
        <value>TALK</value>
        <value>DAV</value>
    </optional>
</scopes>
```

### Required scopes

The connector cannot start without these — AppAPI blocks the install if the admin declines.

| Scope | What it grants | OCS / DAV endpoints touched |
|-------|----------------|------------------------------|
| `FILES` | Read/write on user files (only items the user explicitly points the assistant at). | `PROPFIND /remote.php/dav/files/<uid>/...`, `GET/PUT/DELETE` for individual items, `POST /ocs/v2.php/apps/files_sharing/api/v1/shares` for sharing. |
| `USER_INFO` | Nextcloud user ID, email, display name. | `GET /ocs/v2.php/cloud/users/<uid>`, `GET /ocs/v2.php/cloud/user`. |
| `GROUPS` | Group memberships, used for tenant identification and group-based permissions. | `GET /ocs/v2.php/cloud/groups`, `GET /ocs/v2.php/cloud/groups/<gid>/users`. |

### Optional scopes

The admin can decline any of these at install time. Declining a scope disables the corresponding integration silently — the assistant simply won't have access to that tool group.

| Scope | What it grants | Used by integration |
|-------|----------------|---------------------|
| `NOTIFICATIONS` | Send native NC notifications. | [Notifications](../integrations/nextcloud-notifications.md) |
| `CALENDAR` | Read/write calendar items the user references. | [Calendar](../integrations/nextcloud-calendar.md) |
| `CONTACTS` | Read contacts the user references. | [Contacts](../integrations/nextcloud-contacts.md) |
| `MAIL` | Read/draft mail the user references (via the Mail app). | [Mail](../integrations/nextcloud-mail.md) |
| `TALK` | Read/post Talk messages the user references. | [Talk](../integrations/nextcloud-talk.md) |
| `DAV` | WebDAV / CalDAV / CardDAV. | Files, Calendar, Contacts, Tasks |

## What the assistant can and cannot do

| Bee Flow can | Bee Flow cannot |
|--------------|------------------|
| Read a specific file you ask it to summarise | Bulk-export your file system |
| Draft a reply to an email you point at | Read your entire inbox uninvited |
| Create a calendar event you describe | Walk your calendar in the background |
| Search files / mail / contacts on your behalf, scoped to your account | Access another user's data |
| Post a Talk message in a room you specify | Spam every channel |
| Dismiss a notification you point at | Delete or modify any item without an instruction |

The connector enforces "scoped to your account" structurally: every NC API call is signed with `EX-APP-USER-ID: <yourUid>`, which AppAPI uses to switch the request context server-side. There is no shared service account.

## Group admins can disable optional scopes per-group

In **Admin → Nextcloud integrations** an org admin can:

- **Set the default org-level integrations** — the list of integrations that's enabled for new users.
- **Override per group** — disable specific integrations for the members of a group (e.g. interns get no Talk, finance group gets no Mail).

The rule: **enable wins**. A user gets access if **at least one** of their groups still allows it. If every group the user belongs to disables an integration, the integration is denied for that user. See [Admin → Nextcloud integrations](../admin/nc-integrations.md).

## What the admin sees on install

When you click **Install** on the App Store listing, AppAPI shows a confirmation dialog like:

```
Bee Flow requires the following scopes:

  FILES         (Required) Files & WebDAV
  USER_INFO     (Required) User info (id, mail, displayname)
  GROUPS        (Required) Group memberships

  NOTIFICATIONS (Optional) Send native NC notifications
  CALENDAR      (Optional) Read/write calendar
  CONTACTS      (Optional) Read contacts
  MAIL          (Optional) Read/send mail
  TALK          (Optional) Read/post Talk messages
  DAV           (Optional) WebDAV / CalDAV / CardDAV

[ Decline ]   [ Approve ]
```

You approve once at install time; users never see this dialog.

## How to revoke

Three levels:

| Level | Action | Effect |
|-------|--------|--------|
| Org admin | Disable a specific integration org-wide via **Admin → NC integrations** | Removes that tool from every user's agent. Data already in Bee Flow stays. |
| User | **Settings → Account → Integrations** in the SPA | Removes that tool for just you. |
| Nextcloud admin | **Apps → Disable Bee Flow** in NC | Stops the connector. The bee icon disappears for everyone. The Bee Flow tenant data is **not** auto-deleted (use the Danger zone to do that). |

## Audit trail

Every NC OCS / DAV call made by the connector is recorded in the standard NC `data/nextcloud.log` with the `app_api` source. Filter for `bee_flow` to see exactly which user attribution was used:

```bash
tail -f data/nextcloud.log | grep '"app":"app_api"' | grep bee_flow
```

For tool-call-level auditing (which agent ran which tool when), see [Admin → Audit & compliance](../admin/audit-and-compliance.md).
