# LinkedIn

Read-only LinkedIn lookups via OAuth.

## Setup

1. Create a LinkedIn Developer App at [https://www.linkedin.com/developers/apps](https://www.linkedin.com/developers/apps).
2. Add redirect URI: `https://your-host/auth/linkedin/callback`.
3. Set environment:
   ```bash
   OAUTH_LINKEDIN_CLIENT_ID=...
   OAUTH_LINKEDIN_CLIENT_SECRET=...
   ```
4. Restart server.

## Scopes

| Scope | Purpose |
|-------|---------|
| `r_liteprofile` | Basic profile info |
| `r_emailaddress` | User's email |

(LinkedIn no longer permits broad search via OAuth for new apps. The `r_basicprofile` scope is grandfathered for some apps.)

## Tools

| Tool | Purpose |
|------|---------|
| `linkedin_get_profile` | Read the connected user's own profile. |

This integration is intentionally minimal. It exists so the assistant can ground answers in the user's actual current job title / company without manual entry. We don't expose tools that would scrape other users' profiles — LinkedIn's TOS forbid that.

## Use cases

- "Sign me up to the demo with my title and company."
- (Onboarding) Pre-fill the org admin's "headline" from LinkedIn.

## Privacy

Profile data is held in the user's session only — not persisted. Re-fetched on demand.
