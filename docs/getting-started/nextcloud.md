# Install on Nextcloud

!!! info "Requirements"
    - Nextcloud 31, 32, 33 or 34
    - [AppAPI](https://apps.nextcloud.com/apps/app_api) installed and a deployment daemon configured
    - Admin permissions on the Nextcloud instance

## 1. Install from the App Store

1. Open **Apps** in your Nextcloud admin area.
2. Search for **Bee Flow** in the **AI** category.
3. Click **Install**.

AppAPI will pull the connector image from `ghcr.io/bee-flow/connector` and deploy it next to your Nextcloud. The first install typically takes 30–60 seconds.

![App Store listing](../img/screenshots/01-appstore.png)

## 2. Open Bee Flow

After install, a **bee icon** appears in your Nextcloud top bar. Click it.

![Top-bar icon](../img/screenshots/02-topbar.png)

## 3. First-time consent

The first time **you** open Bee Flow, you'll see a privacy disclosure modal. Read it, then click **I agree — start Bee Flow**. Your acceptance is recorded so you only see this once.

## 4. First-time admin wizard

The first time **the organisation admin** opens Bee Flow, a 4-step onboarding wizard runs. Pick:

- User-sync mode (sync all NC users, or only specific groups)
- Default integrations enabled per group
- Privacy shield level
- Whether to apply a license key now or stay on the free Community tier

Other users see a "Setup in progress" screen until the admin finishes.

[Continue: First-run wizard walk-through :material-arrow-right:](wizard.md)
