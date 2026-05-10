---
title: Knowledge bases
---

# Knowledge bases

A **Knowledge Base** (KB) is a collection of documents the assistant can search. Drop in PDFs, Markdown, Word, plain text, HTML, or point at a Nextcloud folder — Bee Flow chunks, embeds, indexes, and serves citations.

## Two backends

KB ingestion + retrieval can run in either of two backends. Both expose the same `kb_search` tool to agents — choice is invisible to skills and routines.

| Backend | Storage | Pipeline | Best for |
|---|---|---|---|
| **Local (in-process)** — default | Postgres `kb_chunks` table with pgvector | Chunk + embed via global provider (or CPU fallback) + pgvector + BM25 (FTS) + RRF + reranker | Self-hosted setups, no GPU box |
| **Remote search-service** | External Postgres / Qdrant on the search-service host | Same pipeline but on a dedicated GPU machine | High-throughput tenants, BGE-M3 GPU embeddings |

Pick under **Admin → AI Configuratie → Limits & Self-host → Knowledge-base provider** (Auto / Local / Remote). See [Limits & Self-host](../admin/limits-and-self-host.md) for switching, vector-dim reconciliation, and re-ingest semantics.

## Embedding model

Picked under **Admin → AI Configuratie → Embeddings**. Common choices:

| Model | Provider | Dim | Notes |
|---|---|---|---|
| `mistral-embed` | Mistral | 1024 | Multilingual, default for most self-hosted setups |
| `text-embedding-3-small` | OpenAI / Azure OpenAI | 1536 | English-strong |
| `text-embedding-3-large` | OpenAI / Azure OpenAI | 3072 | Best quality, more expensive |
| `multilingual-e5-small` | In-process CPU (Xenova) | 384 | Used as fallback when no provider is configured. MIT, ~470 MB on disk |

The Web Search Inference panel can override per-feature so web-search and KB can use different embed models if needed.

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
3. Embeds via the configured embedding model (provider → CPU fallback).
4. Inserts into `kb_chunks` (or upserts the remote search-service index when `kb_provider = remote`).

Re-ingesting an unchanged document is a no-op. The local pipeline auto-detects the embedding dim on first ingest and ALTERs `kb_chunks.embedding` to match — no manual schema migration when switching models, as long as the table is empty or you re-ingest existing docs.

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
