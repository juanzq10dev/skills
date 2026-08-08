---
title: Streaming input vs single message
triggers:
  - "sending more than one prompt, or attaching an image"
  - "interrupting the agent mid-task, or queueing messages"
  - "canUseTool never fires in Python"
  - "choosing between a one-shot query and a live session"
---

# Streaming input vs single message

Docs: https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode

Two input modes. **Streaming input is the recommended default**: pass an async
iterable as `prompt` instead of a string, and the agent becomes a long-lived process
that accepts queued messages, images, interrupts, and mid-session control calls.

Single-message input takes a plain string. Use it only for one-shot responses in
stateless environments (lambdas, CI). It does **not** support image attachments,
message queueing, real-time interruption, or natural multi-turn.

```typescript
import { query, type SDKUserMessage } from "@anthropic-ai/claude-agent-sdk";
import { readFile } from "fs/promises";

async function* generateMessages(): AsyncGenerator<SDKUserMessage> {
  yield {
    type: "user",
    parent_tool_use_id: null,
    message: {
      role: "user",
      content: "Analyze this codebase for security issues",
    },
  };
  yield {
    type: "user",
    parent_tool_use_id: null,
    message: {
      role: "user",
      content: [
        { type: "text", text: "Review this architecture diagram" },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "image/png",
            data: await readFile("diagram.png", "base64"),
          },
        },
      ],
    },
  };
}

for await (const message of query({
  prompt: generateMessages(),
  options: { maxTurns: 10 },
})) {
  if (message.type === "result" && message.subtype === "success")
    console.log(message.result);
}
```

In Python, streaming input goes through `ClaudeSDKClient` (`api/client.md`) or a
generator passed as `prompt=`:

```python
async def message_generator():
    yield {"type": "user", "message": {"role": "user", "content": "Analyze this codebase"}}

async with ClaudeSDKClient(ClaudeAgentOptions(max_turns=10)) as client:
    await client.query(message_generator())
    async for message in client.receive_response():
        print(message)
```

## Common Anti-Patterns

- Expecting interrupts or `canUseTool` prompts from a string prompt → they require
  streaming input.
- A throwing message generator → in TypeScript the stream ends with
  `Claude Code process aborted by user`, masking the real error (check your
  generator first, and read to the end of the output past the minified line). In
  Python the exception is logged at debug level and the session **stalls silently**.
- Assuming Python's `receive_response()` drains everything → it ends at the first
  result message; use one `query()`/`receive_response()` pair per message.

With streaming input, a message that arrives while a turn is running stays queued
when that turn hits `maxTurns`, and starts its own turn with its own limit.
