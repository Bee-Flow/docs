# Web search

Two providers are supported: **Bing** and **Tavily**. Either is enough — pick whichever you have an account for. Tavily is preferred for AI-tuned results; Bing for general-purpose web indexing.

## Setup — Bing

1. Subscribe to Microsoft Bing Search v7 in Azure.
2. Get the API key from the Azure portal.
3. Set environment:
   ```bash
   BING_SEARCH_API_KEY=<key>
   ```

## Setup — Tavily

1. Sign up at [https://tavily.com](https://tavily.com).
2. Get the API key.
3. Set environment:
   ```bash
   TAVILY_API_KEY=<key>
   ```

## Tools

| Tool | Provider | Purpose |
|------|----------|---------|
| `web_search` | whichever is configured | General web search. |
| `web_fetch_page` | (built-in) | Fetch a URL and return clean text. |
| `web_news_search` | Bing | Filter to news vertical. |
| `web_image_search` | Bing | Image results. |
| `tavily_search` | Tavily | Tavily's semantic-rerank search. |

If both providers are configured, the agent picks one based on the query type. You can pin a default in **Settings → Organisation → Defaults**.

## Use cases

- "What's the current EUR/USD rate?"
- "Find the most-cited paper on retrieval-augmented generation from 2024."
- "Pull this URL and summarise it: https://example.com/article".

## Privacy

Web results pass through the **web-search guardrail** (`webSearchGuardEnabled` in [Privacy Shield](../features/privacy-shield.md) config). Results are PII-scanned before injection into the agent's prompt — useful when search returns news articles with personal data.

## Caching

Bee Flow caches web results for 5 minutes per `(query, provider)` to reduce duplicate API spend. Toggle off with `WEB_SEARCH_CACHE_TTL=0`.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` (Bing) | Subscription expired | Renew Azure subscription. |
| `429 Rate limit` | Provider tier cap | Raise tier or switch provider. |
| `Empty results` | Query too narrow | Have the agent broaden it. |
