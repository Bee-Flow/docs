# Knowledge bases

A **Knowledge Base** (KB) is a collection of documents the assistant can search. Drop in PDFs, Markdown, Word, plain text, HTML, or point at a Nextcloud folder — Bee Flow chunks, embeds, indexes, and serves citations.

## Two flavours

| Type | Tier | Storage | Search | Notes |
|------|:----:|---------|--------|-------|
| **Local KB** | Community+ | Postgres (`kb_chunks`) | Exact / BM25 | Single user, ≤50 docs. Fast, no extra infra. |
| **Vector KB** | Pro+ | pgvector (or external Qdrant via search-service) | Vector + BM25 + RRF + reranker | Multi-user, unlimited docs, hybrid search. |

The toggle is per-KB at creation time. The path is determined by your server config — local if `SEARCH_SERVICE_URL` is unset, hosted otherwise.

## Embedding model

Default: **`bge-m3`** — multilingual, 1024-dim vectors. Works well across English, Dutch, German, French and most Asian languages. Override per-KB via the `embedding_model` field if you have a stronger candidate.

## Chunking

Documents are sliced with a sliding window:

| Knob | Default | Env var |
|------|---------|---------|
| Per-chunk token cap | 800 tokens | `KB_PER_CHUNK_TOKEN_CAP` |
| Total tokens injected into prompt | 4000 | `KB_GLOBAL_INJECT_TOKEN_CAP` |
| Dedup similarity threshold | 0.85 (Jaccard) | `KB_DEDUP_THRESHOLD` |

After chunking, the ingestion pipeline:

1. Hashes each chunk for content dedup.
2. Computes simhash for near-duplicate dedup (threshold above).
3. Embeds with `bge-m3`.
4. Inserts into `kb_chunks` (or upserts the search-service index).

Re-ingesting an unchanged document is a no-op.

## Supported file types

| Format | Notes |
|--------|-------|
| PDF | Layout-aware extraction. Falls back to LLM-based extraction for scanned PDFs. |
| Plain text (.txt) | UTF-8 expected. |
| Markdown (.md) | Headings preserved as chunk anchors. |
| HTML | Stripped of `<script>` / `<style>`; whitespace normalised. |
| Email (.eml) | Headers and body extracted separately; `From:` / `Subject:` / `Date:` retained as metadata. |
| Word (.docx) | Paragraph and heading-aware. |
| CSV | Each row becomes a small chunk with column headers prefixed. |
| URL (web page) | Fetched, HTML-cleaned, then ingested as HTML. |
| Nextcloud folder | Recursive ingestion of supported types within. |

Max file size is gated by `BEEFLOW_REQUEST_BODY_LIMIT` (default 10 MB). Increase for very large PDFs.

## Search modes

The runtime picks the best available mode given your config:

1. **Vector** — embeddings cosine similarity. Default.
2. **BM25** — keyword retrieval (Postgres `tsvector` or search-service Lucene).
3. **Hybrid (RRF)** — Reciprocal Rank Fusion combines vector + BM25 results. Most robust general-purpose mode.
4. **Reranked** — top-K from vector / hybrid sent to a cross-encoder reranker (Azure or local) for final ordering. Highest quality, ~150 ms slower per query.

Search is preceded by a **query-cleaning** pass that strips greetings, politeness markers and filler words ("Could you please find me…" → "find Q3 reports").

## Citations

Sources are returned to the agent as numbered blocks:

```
### Source 1: Q3-2025-Report.pdf
…3 sentences from the chunk…

### Source 2: Strategy-meeting-notes.md
…3 sentences…
```

If the agent's `config.includeSourceReferences = true`, citations are rendered as a separate UI block (cards) below the answer, and the agent is instructed not to inline `[1]`-style markers in prose.

Click a citation card to jump to the original document.

![KB-cited reply with source cards](../img/screenshots/features/knowledge-citations/)

## Pinning a KB to a conversation

```
@kb:product-docs what's our refund policy?
```

The `@kb:` prefix scopes retrieval to a single KB for that turn. Without it, the agent's auto-attached KBs (`config.knowledge_base_ids`) are searched.

## Marketplace

Pre-built KBs (Bee Flow docs themselves, Nextcloud admin manual, GDPR text, etc.) are installable from the **KB Marketplace** in Studio. Installs are read-only — re-ingest happens on the publisher's side.

## Operational notes

- **Re-embedding**: switching the `embedding_model` on an existing KB triggers a background re-embed of all chunks.
- **Storage**: ~1 KB per chunk in Postgres + 4 KB per chunk for the embedding (1024-dim float32). 100k chunks ≈ 500 MB.
- **Cost**: most teams pay $0–5/mo for embedding calls if using a hosted provider; free with self-hosted models.
- **Privacy**: chunks live alongside your Postgres. Nothing is sent to the embedding provider beyond the chunk text — no metadata, no IDs.

## Where to next

- [Studio → Knowledge bases](../studio/knowledge-bases.md) — UI walkthrough.
- [Privacy shield](privacy-shield.md) — what's redacted before chunks reach the embedding provider.
