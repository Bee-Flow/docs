# Fair-code FAQ

## What is "fair-code"?

Fair-code is source code that:

- Is freely available
- Can be modified and self-hosted
- Has restrictions on commercial use by third parties

It's not OSI-approved "open source", but it preserves most of the freedoms developers care about.

## What can I do?

✅ Self-host Bee Flow for your own company / nonprofit / personal use, free of charge.

✅ Modify the source. Fork the repos. Submit PRs.

✅ Use it commercially **inside** your organisation — to serve your own employees / customers via your own product.

✅ Audit every line of code that runs against your data.

## What can't I do?

❌ Run Bee Flow as a paid SaaS for third parties (e.g. you can't spin up "Acme Bee Flow" and resell it).

❌ Use the "Bee Flow" name or bee logo on a fork — those are trademarks.

❌ Strip the licence headers / attribution from source files.

## Can I contribute?

Yes — bug reports, feature requests and PRs are welcome on GitHub. By submitting a contribution, you agree to license it under the same terms as the project.

## Why not pure AGPL or MIT?

- **MIT** would let competitors take the code and resell Bee Flow as their own SaaS — that funds nothing back into the project.
- **AGPL** requires anyone hosting a modified version to publish their changes, which scares off enterprise self-hosters who can't legally publish their internal patches.

The Sustainable Use Licence threads the needle: maximally permissive for end-users and self-hosters, narrowly restricted on third-party SaaS resale.

## Why is the connector AGPL-3.0?

The Nextcloud App Store requires AGPL or compatible. The connector is small enough (proxy + lifecycle hooks) that AGPL is fine.

## Where do I email about licensing?

<tomkooy@beeflow.nl>.
