# REST reference

The most-used endpoints, grouped by area. For exhaustive coverage, see the OpenAPI spec.

## Health

```http
GET /api/health
```

```json
{ "status": "ok", "version": "0.1.0", "tier": "community" }
```

## Chat

```http
POST /api/chat
Content-Type: application/json

{
  "agentId": "asst_default",
  "messages": [
    { "role": "user", "content": "Summarise yesterday's emails." }
  ]
}
```

Returns a streaming response — see [Streaming (SSE)](sse.md).

## Agents

```http
GET    /api/agents
POST   /api/agents
GET    /api/agents/:id
PATCH  /api/agents/:id
DELETE /api/agents/:id
```

## Knowledge bases

```http
GET    /api/knowledge
POST   /api/knowledge
POST   /api/knowledge/:id/documents
DELETE /api/knowledge/:id/documents/:docId
POST   /api/knowledge/:id/search
```

## Automations (Pro+)

```http
GET    /api/automations
POST   /api/automations
POST   /api/automations/:id/runs
GET    /api/automations/:id/runs
```

## License

```http
GET  /api/license/status
POST /api/license/apply
```
