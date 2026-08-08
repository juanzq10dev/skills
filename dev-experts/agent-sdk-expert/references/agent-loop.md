---
title: The agent loop, turns, and results
triggers:
  - "deciding which messages to handle in the stream"
  - "the agent runs too long, too expensive, or never stops"
  - "checking whether a run succeeded, and reading cost or session id off the result"
  - "query() threw after the loop finished"
  - "context window filling up, compaction, or losing early instructions"
  - "choosing an effort level"
---

# The agent loop, turns, and results

Docs: https://code.claude.com/docs/en/agent-sdk/agent-loop

`SystemMessage(subtype:"init")` → repeat { `AssistantMessage` (text + tool calls) →
tools run → `UserMessage` (tool results) } → final `AssistantMessage` with no tool
calls → `ResultMessage`. One repeat is a **turn**.

Five message types drive the loop: `SystemMessage`, `AssistantMessage`,
`UserMessage`, `StreamEvent` (only with partial messages on), `ResultMessage`.
Full shapes and the SDK-specific access patterns: `api/messages.md`.

## Bound the loop

| Option                            | Effect                                                 | Default       |
| --------------------------------- | ------------------------------------------------------ | ------------- |
| `maxTurns` / `max_turns`          | Max tool-use round trips                               | no limit      |
| `maxBudgetUsd` / `max_budget_usd` | Stop at a spend threshold; **includes subagent spend** | no limit      |
| `effort`                          | `"low"`…`"max"` reasoning depth                        | model default |

Setting a budget is the right default for production agents. `effort: "xhigh"` is
the recommended setting for coding and agentic tasks on Fable 5, Opus 4.7+, and
Sonnet 5; `"low"` for file lookups and listings.

## Handle the result

```typescript
if (message.type === "result") {
  if (message.subtype === "success") console.log(message.result);
  else console.log(`Stopped: ${message.subtype}`); // result field is absent
  console.log(message.total_cost_usd, message.num_turns, message.session_id);
}
```

`subtype` is `success`, `error_max_turns`, `error_max_budget_usd`,
`error_during_execution`, or `error_max_structured_output_retries`. **`result` is
only present on `success`** — always branch on `subtype` first. Every subtype
carries `total_cost_usd`, `usage`, `num_turns`, and `session_id` (in Python
`total_cost_usd` and `usage` are optional and may be `None`).

`stop_reason` reports why the model stopped its final turn: `end_turn`,
`max_tokens`, `refusal`.

## Common Anti-Patterns

- Not wrapping a single-shot `query()` in try/catch → a run that ends on an error
  result **yields the result and then raises/throws**. A streaming-input session
  stays alive instead.
- `break`ing out of the loop on `ResultMessage` → trailing system events such as
  `prompt_suggestion` arrive after it; iterate to completion.
- Putting persistent rules in the first prompt → compaction replaces old messages
  with a summary. Persistent rules belong in CLAUDE.md, which is re-injected every
  request (`config/setting-sources.md`).
- Treating `effort` as extended thinking → they are independent; `effort` sets
  reasoning depth per response, `thinking.display` controls whether you receive
  thinking text.

## Keep context efficient

Delegate subtasks to subagents (fresh context, only the summary returns —
`config/subagents.md`), scope tool sets, keep tool search on (`tools/tool-search.md`),
and lower `effort` for routine work. Compaction fires automatically and emits a
`system` message with `subtype: "compact_boundary"`; `/compact` triggers it manually.
