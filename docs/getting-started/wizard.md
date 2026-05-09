# First-run wizard

The first time an organisation admin opens Bee Flow, a 4-step wizard runs.

## Step 1 — User sync mode

Choose which Nextcloud users get a Bee Flow account:

- **All users** — every NC user is mirrored to Bee Flow.
- **Specific groups** — only members of selected groups (e.g. `bee-flow-users`).

You can change this later in **Settings → Organisation → User sync**.

![Step 1: user sync](../img/screenshots/wizard-01-sync.png)

## Step 2 — Default integrations

Tick which Nextcloud integrations are enabled for new users by default. Per-group overrides are configurable later.

Available integrations:

- Files
- Mail
- Calendar
- Contacts
- Deck
- Notes
- Tasks
- Talk
- Activity
- Notifications
- User Status

![Step 2: integrations](../img/screenshots/wizard-02-integrations.png)

## Step 3 — Privacy shield

The **Privacy Shield** detects emails, phone numbers, IBANs, BSNs, credit-card numbers and other sensitive data in your prompts and replaces them with placeholders before anything reaches the language model. The original values are restored in the reply, only on your screen.

Pick the strictness level — `standard` is the default and works for most teams.

![Step 3: privacy](../img/screenshots/wizard-03-privacy.png)

## Step 4 — License key (optional)

Stay on the free **Community** tier, or paste a license key from [beeflow.ai/pricing](https://beeflow.ai/pricing) to unlock automations, multi-user, DLP and other premium features.

![Step 4: license](../img/screenshots/wizard-04-license.png)

## Done

The wizard closes and Bee Flow opens for everyone in the chosen sync scope.
