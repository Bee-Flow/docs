# Bee Flow — Documentation

Source for [docs.beeflow.ai](https://docs.beeflow.ai).

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Local development

```bash
pip install -r requirements.txt
mkdocs serve
```

Open <http://localhost:8000>.

## Structure

```
docs/
├── index.md                 Landing page
├── getting-started/         Install + first-run
├── connector/               Nextcloud connector deep-dive
├── self-hosting/            Docker, Kubernetes, env vars
├── features/                Chat, agents, automations, privacy
├── licensing/               Tiers + how to apply a key
├── api/                     REST + SSE reference
└── img/                     Screenshots and diagrams
```

## Contributing

Fork → branch → PR. Each page has an "Edit this page" link in the top-right.

Screenshots: PNG, max 1600px wide, drop in `docs/img/<section>/`.

## License

Documentation is CC-BY-4.0. Code samples are MIT.
