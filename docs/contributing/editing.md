---
title: Editing this site
description: How to edit pages, add screenshots, and ship a change to docs.beeflow.ai — works the same whether you write code or not.
---

# Editing this site

You don't need to install anything. There are two ways to edit:

- **The visual editor at [/cms/](/docs/cms/)** — friendly UI with a rich-text editor, image uploads, and a side-by-side preview. Best for non-technical editors. *(One-time setup required by an admin — see the bottom of this page.)*
- **GitHub's editor** — every page has an **Edit this page** link at the bottom that opens GitHub's web editor. Best when you want to see the raw Markdown.

Either way, every save is a Git commit attributed to **your** GitHub user, and the live site rebuilds automatically a couple of minutes after merge.

This page covers the three things you'll actually do:

1. Edit text on an existing page
2. Add a screenshot
3. Create a brand-new page

If you've never used GitHub before, you'll need a free account at [github.com](https://github.com/signup) and someone on the Bee Flow team to add you to the `Bee-Flow/docs` repo.

---

## The visual editor (recommended for non-technical editors)

Go to [docs.beeflow.ai/cms/](/docs/cms/) and click **Log in with GitHub**. Once you authorize, you'll see all the docs sections in a sidebar, just like the navigation on the site itself.

For each section you can:

- Click an existing page → edit in a rich-text editor (bold, italic, links, lists, tables, code blocks, callout boxes — all without seeing Markdown syntax)
- Click **New page** → start a blank page with a title + body
- Drag-and-drop images straight into the editor — they're uploaded to the repo for you
- See a live **Preview** of how your page will look on the actual site
- Click **Save** when you're done — a Git commit happens behind the scenes

Logging in uses your existing GitHub account; access is whatever you have on the `Bee-Flow/docs` repo (no separate user list to manage).

---

## 1. Edit text on an existing page

The friendliest way:

1. Open the page you want to change.
2. Scroll to the bottom — click **Edit this page**.
3. GitHub opens an editor with the source of that page.
4. Make your changes. Use the **Preview** tab at the top of the editor to see what they'll look like.
5. Scroll down. Type a short note in the "Commit changes" box (for example, *"Fix typo on tiers page"*).
6. Click **Propose changes** → **Create pull request**.
7. Someone with merge rights reviews and merges. The site rebuilds automatically.

:::tip[Power-user shortcut]

On any page in the GitHub repository, press the `.` key. GitHub opens a full **VS Code editor** in your browser — same one developers use, with live Markdown preview, file tree, and search. No install needed. Works for non-technical users too — you'll just edit text. URL trick: replace `github.com` with `github.dev` in the address bar.

:::

---

## 2. Add a screenshot

Screenshots live next to the docs in [`docs/img/screenshots/`](https://github.com/Bee-Flow/docs/tree/main/docs/img/screenshots). Each *kind* of screenshot has its own folder — for example `connector/install-progress/` or `features/chat-empty-state/`.

To add or replace a screenshot:

1. Open the relevant folder on GitHub (browse `docs/img/screenshots/<area>/<topic>/`).
2. Drag your image file straight onto the page — GitHub uploads it and opens a commit dialog.
3. Type a short note like *"Add new install screenshot"* and click **Commit changes** → **Create pull request**.

There's no need to rename the file — the page that references this folder will automatically pick up the new image.

**File rules:**
- Format: `.png`, `.jpg`, `.webp`, `.gif`, or `.svg`
- Max width: 1600px (anything wider just makes the page slow)
- Avoid screenshots with personal data — names, emails, real customer info

To **reference** a screenshot from a Markdown page, use the folder path (with a trailing slash):

```markdown
![Install progress dialog](../img/screenshots/connector/install-progress/)
```

The build picks the first image in that folder automatically. If the folder is empty, the build still works — the spot is just blank until you drop an image in.

---

## 3. Create a brand-new page

1. Go to the GitHub repo: [github.com/Bee-Flow/docs](https://github.com/Bee-Flow/docs).
2. Navigate to the folder where the page belongs (e.g. `docs/features/`).
3. Click **Add file** → **Create new file**.
4. Name it `something-short.md` — lowercase, dashes instead of spaces.
5. Paste this template at the top:

   ```markdown
   ---
   title: Your page title
   description: One sentence shown in search results.
   ---

   # Your page title

   Write your content here.
   ```

6. Write your page (see the cheatsheet below).
7. Commit and open a pull request.
8. **Important last step:** ask someone to add this page to [`sidebars.ts`](https://github.com/Bee-Flow/docs/blob/main/sidebars.ts) — otherwise it won't show in the menu (it's still reachable by URL, just not navigable).

---

## Markdown cheatsheet

Markdown is a way of writing formatted text using plain characters. Here's what you'll actually use:

### Headings

```markdown
# Page title (one per page, at the top)
## Section heading
### Sub-section
```

### Bold and italic

```markdown
**bold text**
*italic text*
```

### Links

```markdown
[link text](https://example.com)              ← external link
[other page on this site](../features/chat)   ← internal link, no .md
```

### Lists

```markdown
- bullet one
- bullet two
  - nested item

1. numbered one
2. numbered two
```

### Tables

```markdown
| Column A | Column B |
|----------|----------|
| value 1  | value 2  |
| value 3  | value 4  |
```

### Code samples

For inline code, use backticks: `` `like this` ``.

For code blocks, fence with three backticks and the language:

````markdown
```bash
docker compose up -d
```
````

### Callout boxes (admonitions)

These render as the coloured "tip / warning / note" boxes you see on this site:

```markdown
:::tip[Optional title here]

Helpful nudge or shortcut.

:::

:::warning[Heads up]

Something readers shouldn't miss.

:::
```

Available types: `note`, `tip`, `info`, `warning`, `danger`.

### Images

```markdown
![Short description for accessibility](../img/screenshots/area/topic/)
```

---

## Previewing your changes

Two ways:

- **Quick preview**: GitHub's built-in **Preview** tab in the web editor. Renders Markdown, but doesn't show admonitions or this site's styling.
- **Real preview**: Once your pull request is merged, the site rebuilds. The new version is live at [docs.beeflow.ai](https://docs.beeflow.ai) within ~2 minutes — check the **Actions** tab on GitHub to see the deploy progress.

If you'd rather see styled previews before merging, ask the team to add a Netlify or Cloudflare Pages preview deploy — it adds a per-PR preview URL.

---

## Help

- Stuck? Open [github.com/Bee-Flow/docs](https://github.com/Bee-Flow/docs) and click **Issues** → **New issue** to ask.
- Made a mistake? Don't worry — every change goes through a pull request, and a teammate can fix it before it goes live.

---

## Admin: one-time CMS setup

The visual editor at [/cms/](/docs/cms/) uses [Sveltia CMS](https://github.com/sveltia/sveltia-cms) — a static admin UI that lives on GitHub Pages alongside the rest of the docs. The site itself is fully GitHub-Pages-hosted; the **only** external touchpoint is a tiny OAuth relay that handles the GitHub login handshake (GitHub's OAuth requires a server-side token exchange — there's no way around this for OAuth Apps).

You have two ways to run that relay. Pick one and follow only that section.

### Option A — Use Sveltia's shared relay (5 minutes, less control)

Easiest path. Editors see a generic "Sveltia CMS" permissions prompt on first login (instead of a "Bee Flow Docs" prompt), and you depend on `auth.sveltia.app` staying up.

1. Open [github.com/login/oauth/authorize](https://github.com/login/oauth/authorize?client_id=Iv1.6e54b4a14a8cc7e1) — this is Sveltia's pre-registered OAuth App. *(That's it for setup.)*
2. The current `static/cms/config.yml` already has `base_url: https://auth.sveltia.app` so logins will route there.
3. Tell editors to visit [/cms/](/docs/cms/) and click **Log in with GitHub**.

### Option B — Self-host the relay (30 minutes, full control)

Recommended for production. You own the OAuth App, you own the relay, no third-party dependency.

1. **Register a GitHub OAuth App** at [github.com/settings/developers](https://github.com/settings/developers) (or your org's developer settings):
   - **Application name**: *Bee Flow Docs CMS*
   - **Homepage URL**: `https://bee-flow.github.io/docs/`
   - **Authorization callback URL**: `https://your-relay.example.com/callback` (set this in the next step)
   - Copy the **Client ID** and generate a **Client secret**.
2. **Deploy the relay** — fork [sveltia/sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth) and run it on:
   - **Cloudflare Worker** — easiest, free tier covers thousands of logins/month. Drop the `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` as env vars.
   - or **Netlify Function**, **Vercel Function**, **Deno Deploy**, **Render**, etc.
3. **Update `static/cms/config.yml`** — replace `base_url: https://auth.sveltia.app` with your relay's URL, then commit.
4. Go back to your OAuth App and update the callback URL to `https://your-relay.example.com/callback`.

In either case the relay only handles the OAuth code-for-token swap; **no edits, page content, or repo data ever pass through it**. After login, the browser talks straight to `api.github.com`.

### Editor permissions

Whoever has write access to the `Bee-Flow/docs` repo can use the CMS. Remove someone from the repo → they can't edit. There is no separate user list to manage.

### Local testing

The CMS only works against a live deployment because GitHub OAuth needs a stable callback URL. To test on `localhost:3000`, register a second OAuth App with `http://localhost:3000/cms/` as its callback, deploy a second relay (or run sveltia-cms-auth locally with `wrangler dev`), and add a dev override of `base_url` in your config.
