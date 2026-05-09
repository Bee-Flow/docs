# Knowledge bases (Studio)

This page is the UI walkthrough. For the technical underpinnings (embeddings, chunking, search modes), see [Features → Knowledge bases](../features/knowledge.md).

URL: `/app/notebooks` (Knowledge Bases live alongside Notebooks under the same shell).

![Knowledge bases list](../img/screenshots/studio/knowledge-bases-list/)

## Creating a KB

1. **Studio → Knowledge bases → New**.
2. Pick a name + visibility:
   - **Private** — just for you.
   - **Group** — multi-select groups.
   - **Org** — every agent in the org can use.
3. Pick the storage mode:
   - **Local** (Community+) — fast for ≤50 docs.
   - **Vector** (Pro+) — for >50 docs and multi-user.
4. Pick the embedding model — default `bge-m3`. You can switch later (re-ingest cost applies).
5. Click **Create**.

## Adding documents

Three ways:

| Source | UX |
|--------|----|
| Upload | Drag-drop PDF / Markdown / TXT / DOCX / HTML / EML / CSV. |
| URL | Paste a URL — Bee Flow fetches and ingests. |
| Nextcloud folder | Pick a folder; ingestion is recursive. Tracks the folder for future re-ingest. |

Ingestion runs in the background. Each document shows a progress bar with chunk count + embedding status.

## Browsing chunks

Click a document to see its chunks. Each chunk shows:

- The text
- A "found in N searches" counter
- A button to re-embed just that chunk (after edits)

## Attaching a KB to an agent

In the [Agent Designer → Knowledge tab](agent-designer.md#tab-4-knowledge):

- **Auto-search** — KB is searched on every turn.
- **Tool-mediated** — KB is exposed as a `kb_search` tool the agent calls when needed.

Auto-search is faster but always retrieves; tool-mediated is more efficient (no retrieval on small-talk turns) but adds one round-trip for the model to decide to search.

## Pinning a KB at chat time

```
@kb:product-docs what's our refund policy?
```

The `@kb:` prefix scopes retrieval to a single KB for that turn. Without it, the agent's auto-attached KBs are searched.

## KB Marketplace

Pre-built KBs are installable from the **Marketplace** tab:

| KB | Content |
|----|---------|
| Bee Flow Docs | This entire docs site. |
| GDPR text | Articles + recitals of the EU GDPR. |
| Nextcloud Admin Manual | The full NC admin docs. |
| AI ethics frameworks | OECD, EU AI Act, NIST RMF. |

Installs are read-only at first — you can fork them to edit.

## Settings

Per-KB settings:

| Setting | Notes |
|---------|-------|
| Embedding model | Switch model, triggers re-embed. |
| Chunk size | Override `KB_PER_CHUNK_TOKEN_CAP`. |
| Search mode | Vector / BM25 / Hybrid / Reranked. |
| Reranker | Azure / Cohere / local cross-encoder. |
| Retention | "Forever" / "auto-delete after N days". |

## Sharing

A KB shared at org level is visible to every agent in the org. Per-agent attachment is still required — sharing makes it *eligible* to attach, not auto-attached.

## Deleting

Soft-delete (30-day recovery window) or hard-delete (immediate). Deleting a KB removes its chunks but does **not** delete the original documents stored in NC / Drive — Bee Flow only ever held copies.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Ingestion stuck at 0% | Document parser couldn't read the file | Check the format; fall back to text export. |
| Searches return nothing relevant | KB hasn't ingested yet, or query mode mismatch | Wait for ingestion; switch to Hybrid. |
| Agent doesn't cite KB | Auto-search off, or `kb_search` tool not in allow-list | Toggle in Agent Designer. |
