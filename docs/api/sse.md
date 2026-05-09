# Streaming (SSE)

Chat responses stream over Server-Sent Events. The connection stays open until the assistant finishes its turn (including tool calls).

## Request

```http
POST /api/chat
Accept: text/event-stream
Authorization: Bearer <jwt>

{ "agentId": "asst_default", "messages": [ ... ] }
```

## Event types

```
event: token
data: {"text": "Yes"}

event: token
data: {"text": ", here's"}

event: tool_call
data: {"id": "tc_1", "name": "nc_files_search", "args": {"query": "Q3 report"}}

event: tool_result
data: {"id": "tc_1", "result": [{"path":"/Reports/Q3.pdf"}, ...]}

event: token
data: {"text": " a summary..."}

event: done
data: {"messageId": "msg_abc", "usage": {"input": 1234, "output": 567}}
```

## Cancelling

Close the EventSource client-side, or send:

```http
POST /api/chat/:messageId/cancel
```

## JS example

```js
const es = new EventSource('/api/chat?token=' + jwt);
es.addEventListener('token', e => console.log(JSON.parse(e.data).text));
es.addEventListener('tool_call', e => console.log('🛠', JSON.parse(e.data)));
es.addEventListener('done', () => es.close());
```
