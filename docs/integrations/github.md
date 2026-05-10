---
title: GitHub
---

# GitHub

Bee Flow connects to GitHub via OAuth or a personal access token.

## Setup (OAuth)

1. **Settings → Developer settings → OAuth Apps → New OAuth App** at [https://github.com/settings/developers](https://github.com/settings/developers).
2. Authorisation callback URL: `https://your-host/auth/github/callback`.
3. Set environment:
   ```bash
   OAUTH_GITHUB_CLIENT_ID=...
   OAUTH_GITHUB_CLIENT_SECRET=...
   ```
4. Restart server.

OAuth scopes requested by default: `repo`, `read:user`, `read:org`. For private-repo write operations, `repo` is the minimum.

## Setup (PAT — alternative)

For users in orgs where OAuth apps are restricted, the user can paste a fine-grained personal access token in **Settings → Account → Integrations → GitHub → Token**. The token is AES-encrypted at rest.

## Tools

| Tool | Purpose |
|------|---------|
| `github_list_repos` | List repos the user has access to. |
| `github_search_code` | Code search across visible repos. |
| `github_get_file` | Read a file by `owner/repo/path@ref`. |
| `github_list_issues` | List issues. |
| `github_get_issue` | Read one issue + comments. |
| `github_create_issue` | Open an issue. |
| `github_comment_issue` | Comment. |
| `github_list_pulls` | List PRs. |
| `github_get_pull` | Read a PR + reviews. |
| `github_create_pull` | Open a PR (requires `repo` scope). |
| `github_list_commits` | Commit history with optional path filter. |
| `github_get_commit` | One commit, diff included. |

## Use cases

- "Find all open issues mentioning `regression` in `Bee-Flow/beeflow`."
- "Summarise the last 5 PRs merged to `main`."
- "Open an issue titled 'Docs: clarify license refresh' with a description from this conversation."
- (Automation) On a Talk message containing `bug:`, open a GitHub issue.

## Rate limits

GitHub's standard 5000 requests/hour applies to the whole org's traffic through the OAuth app. For high-volume automations, use a GitHub App instead of OAuth — the limits are per-installation.

## Privacy

Code snippets pulled by `github_get_file` and search results flow through the Privacy Shield. Custom regex categories (e.g. project codenames, secrets that lint-tools missed) are particularly useful here.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Resource not accessible by integration` | Token / OAuth scope missing `repo` | Reconnect with `repo` scope. |
| `404 Not Found` on private repo | User isn't a collaborator | Org owner adds them. |
| `422 Validation Failed` on issue create | Required field missing | Provide `title` (mandatory). |
