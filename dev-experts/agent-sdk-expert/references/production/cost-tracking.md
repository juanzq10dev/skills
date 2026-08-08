---
title: Cost and token usage
triggers:
  - "reporting what a run cost"
  - "token counts don't add up, or subagent spend seems missing"
  - "accumulating spend across many calls"
  - "per-model or per-step usage breakdown"
  - "extending the prompt cache TTL"
---

# Cost and token usage

Docs: https://code.claude.com/docs/en/agent-sdk/cost-tracking

```typescript
for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type === "result")
    console.log(`Total cost: $${message.total_cost_usd}`);
}
```

```python
async for message in query(prompt="Summarize this project"):
    if isinstance(message, ResultMessage):
        print(f"Total cost: ${message.total_cost_usd or 0}")
```

## Subagents are counted inconsistently — this is the trap

| Field                        | Subagent activity                       |
| ---------------------------- | --------------------------------------- |
| `usage`                      | **Excluded.** Top-level agent loop only |
| `total_cost_usd`             | **Included**                            |
| `modelUsage` / `model_usage` | **Included**, broken down by model      |

So reconstructing cost from `usage` under-reports any run that delegated. Use
`total_cost_usd` for spend and `modelUsage` for attribution.

## Per-step and per-model

```typescript
if (message.type === "assistant") {
  const id = message.message.id;
  if (!seenIds.has(id)) {
    // parallel tool calls share an ID
    seenIds.add(id);
    totalInputTokens += message.message.usage.input_tokens;
    totalOutputTokens += message.message.usage.output_tokens;
  }
}
```

```typescript
for (const [modelName, usage] of Object.entries(message.modelUsage)) {
  console.log(
    modelName,
    usage.costUSD,
    usage.inputTokens,
    usage.outputTokens,
    usage.cacheReadInputTokens,
    usage.cacheCreationInputTokens,
  );
}
```

## Common Anti-Patterns

- Counting every `AssistantMessage` → messages from parallel tool calls share a
  message ID; dedupe on it or you double-count.
- Skipping cost on failed runs → **every** result subtype carries `total_cost_usd`,
  so a run that hit a limit still spent money. In Python it is optional and may be
  `None` — guard before formatting.
- Losing cost when `query()` raises → the result message is yielded before the
  raise, so accumulate inside the loop and let the `except` block continue to the
  next call (`../api/errors.md`).

Cap spend rather than only measuring it: `maxBudgetUsd` / `max_budget_usd` stops the
loop at a threshold and covers subagent spend (`../agent-loop.md`).

## Prompt cache TTL

Stable content (system prompt, tool definitions, CLAUDE.md) is prompt-cached
automatically. To extend the TTL to one hour on Bedrock:

```python
options = ClaudeAgentOptions(env={"CLAUDE_CODE_USE_BEDROCK": "1",
                                  "ENABLE_PROMPT_CACHING_1H": "1"})
```

Cache reuse across machines depends on the system prompt being byte-identical —
see `excludeDynamicSections` in `../config/system-prompts.md`.
