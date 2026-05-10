---
title: n8n
---

# n8n

[n8n](https://n8n.io) is a fair-code workflow automation platform. Bee Flow can list and trigger n8n workflows — useful for orchestrating cross-system pipelines that go beyond Bee Flow's built-in [Automations](../features/automations.md).

## Setup

1. Get your n8n base URL + API key.
2. Set environment variables:
   ```bash
   N8N_BASE_URL=https://n8n.example.com
   N8N_API_KEY=<api_key>
   ```
3. Restart server.

n8n API key creation: in your n8n UI, **Settings → API → Create API key**.

## Tools

| Tool | Purpose |
|------|---------|
| `n8n_list_workflows` | List all workflows. |
| `n8n_search_workflows` | Filter by name / tag / active state. |
| `n8n_get_workflow` | Read workflow definition. |
| `n8n_trigger_workflow` | Run a workflow with a payload. |
| `n8n_get_execution` | Read past execution detail. |
| `n8n_list_executions` | Recent runs. |

## Triggering

```
n8n_trigger_workflow({
  workflowId: "abc123",
  payload: { customerId: "cust_42", action: "refund" }
})
```

The workflow must have a Webhook node configured. Bee Flow POSTs to that webhook URL with the supplied payload.

## Use cases

- "Trigger the `Onboard new customer` workflow with this customer's data."
- "Show me the last 10 failed runs of the `Sync CRM` workflow."
- (Automation) On NC `UserCreatedEvent`, fire an n8n `Onboard employee` workflow.

## Auth flow

n8n's API uses static API keys — no OAuth dance. The key is stored in `.env` (server-wide) by default, or per-user (overrides server) when set in **Settings → Account → Integrations**.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | API key wrong | Check `N8N_API_KEY` matches n8n's. |
| `404 Not Found` workflow | ID stale | Re-list. |
| `Webhook not active` | Workflow not enabled | Toggle "Active" in n8n. |
| Slow trigger response | n8n cold-start | n8n's worker scaling. Out of Bee Flow's control. |
