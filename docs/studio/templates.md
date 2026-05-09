# Templates

Templates are pre-built agent recipes. Each one ships with a name, prompt, recommended tool set, and (optionally) a starter KB.

URL: `/app/templates`.

![Templates marketplace](../img/screenshots/studio/templates-marketplace/)

## Browsing

Templates are organised by category:

| Category | Examples |
|----------|----------|
| Sales | Cold-email writer, lead-research scout, deal-summary |
| Marketing | Blog draft, social post, content calendar |
| Engineering | PR reviewer, bug triager, doc generator |
| Operations | Standup digest, inbox triage, meeting prep |
| HR | Onboarding host, policy QA, leave request triage |
| Customer support | Ticket responder, FAQ resolver, escalation routing |
| Internal | Decision log, OKR tracker, budget approval |

## Installing a template

1. Click the template card.
2. Preview the prompt + tool set.
3. Click **Install**. A copy is created in your library; the upstream is unaffected.
4. Tweak in the [Agent Designer](agent-designer.md).

Installation is a deep clone — system prompt, tool selection, attached KB IDs (if pre-built KBs are available in your org), starter prompts.

## Saving your own as templates

1. In the Agent Designer, click **Save as template**.
2. Choose visibility:
   - **Just me** — private template, used for cloning your own agents.
   - **Team** — group-shared templates.
   - **Org** — anyone in the org can install.
   - **Public marketplace** — submit for review (admin approval if your org has the policy on).
3. Add a category, description, and example prompts.

## Versioning

Templates are immutable once published. To "update" a public template, publish a new version — installations are not auto-upgraded; users see an "update available" badge.

## Forking

Click **Fork** on any template (yours or someone else's) to create an editable copy. Editing the fork doesn't affect the original; share the fork as a new template if useful.

## Curated templates

A growing library of curated templates ships out of the box at every install. Updates land via the docs repo at <https://github.com/Bee-Flow/templates> (PRs welcome).
