---
title: Stream partial responses
triggers:
  - "showing text token-by-token in a UI as the agent works"
  - "rendering a spinner or status while a tool runs"
  - "watching a tool's input JSON assemble incrementally"
---

# Stream partial responses

Docs: https://code.claude.com/docs/en/agent-sdk/streaming-output

Off by default: the SDK yields whole `AssistantMessage`s. Set
`includePartialMessages` / `include_partial_messages` to also receive raw API stream
events. This is independent of streaming _input_ (`streaming-input.md`).

```typescript
for await (const message of query({
  prompt: "Explain how databases work",
  options: { includePartialMessages: true },
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (
      event.type === "content_block_delta" &&
      event.delta.type === "text_delta"
    ) {
      process.stdout.write(event.delta.text);
    }
  }
}
```

```python
from claude_agent_sdk import query, ClaudeAgentOptions
from claude_agent_sdk.types import StreamEvent

async for message in query(
    prompt="Explain how databases work",
    options=ClaudeAgentOptions(include_partial_messages=True),
):
    if isinstance(message, StreamEvent):
        delta = message.event.get("delta", {})
        if message.event.get("type") == "content_block_delta" and delta.get("type") == "text_delta":
            print(delta.get("text", ""), end="", flush=True)
```

Python yields a `StreamEvent` dataclass with `uuid`, `session_id`, `event` (a raw
dict), `parent_tool_use_id` (always `None`). TypeScript yields
`SDKPartialAssistantMessage` with `type: "stream_event"`, a typed `event`, `uuid`,
`session_id`, and `ttft_ms` on `message_start` events only.

Event types: `message_start`, `content_block_start`, `content_block_delta`,
`content_block_stop`, `message_delta`, `message_stop`. Order per turn is
`message_start` → per-block start/delta*/stop → `message_delta` → `message_stop` →
the complete `AssistantMessage` → tool execution → next turn → `ResultMessage`.

## Stream a tool call

`content_block_start` with `content_block.type === "tool_use"` names the tool;
`content_block_delta` with `delta.type === "input_json_delta"` carries
`partial_json` chunks to concatenate; `content_block_stop` completes it.

```typescript
if (
  event.type === "content_block_start" &&
  event.content_block.type === "tool_use"
) {
  process.stdout.write(`\n[Using ${event.content_block.name}...]`);
} else if (
  event.type === "content_block_delta" &&
  event.delta.type === "input_json_delta"
) {
  toolInput += event.delta.partial_json;
}
```

Accumulate `partial_json` before parsing — a chunk is not valid JSON on its own.
