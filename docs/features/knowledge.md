# Knowledge bases

A **Knowledge Base** is a collection of documents the assistant can search. Drop in PDFs, Markdown, Word, plain text, or point at a Nextcloud folder — Bee Flow chunks, embeds, and indexes them.

## Two flavours

| Type | Tier | Storage | Notes |
|------|------|---------|-------|
| **Local KB** | Community | In-memory or SQLite | Single user, ≤ 50 docs. Fast, no infra. |
| **Vector KB** | Pro+ | pgvector or external (Qdrant) | Multi-user, unlimited docs, hybrid search. |

## Asking questions

Pin a KB to your conversation:

```
@kb:product-docs what's our refund policy?
```

The assistant retrieves the top-N chunks, cites them inline, and answers from those snippets only.

## Sources & citations

Every answer that uses retrieval shows source cards:

![Citations](../img/screenshots/kb-citations.png)

Click a card to jump to the original document.
