---
title: ClaudeSDKClient (Python)
triggers:
  - "multi-turn Python agent that keeps context across calls"
  - "interrupting a running Python agent"
  - "changing model or permission mode mid-session in Python"
  - "checking MCP server status from Python"
---

# `ClaudeSDKClient` (Python)

Docs: https://code.claude.com/docs/en/agent-sdk/python#claudesdkclient

Holds one session across many `query()` calls, so you never handle session IDs. It
is also the Python path to streaming input, interrupts, and `can_use_tool`.

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ResultMessage

async def main():
    async with ClaudeSDKClient(options=ClaudeAgentOptions(allowed_tools=["Read", "Edit"])) as client:
        await client.query("Analyze the auth module")
        async for message in client.receive_response():
            if isinstance(message, ResultMessage):
                print(message.result)

        await client.query("Now refactor it to use JWT")   # same session, full context
        async for message in client.receive_response():
            print(message)

asyncio.run(main())
```

| Method                                                                           | Description                                                 |
| -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `connect(prompt=None)` / `disconnect()`                                          | Manual lifecycle; the context manager does both             |
| `query(prompt, session_id="default")`                                            | Send a request in streaming mode                            |
| `receive_messages()`                                                             | All messages, as an async iterator                          |
| `receive_response()`                                                             | Messages up to **and including** the next `ResultMessage`   |
| `interrupt()`                                                                    | Stop the current task (streaming mode only)                 |
| `set_permission_mode(mode)` / `set_model(model=None)`                            | Change mid-session; `None` resets the model                 |
| `rewind_files(user_message_id)`                                                  | Restore files; needs `enable_file_checkpointing=True`       |
| `get_mcp_status()` / `reconnect_mcp_server(n)` / `toggle_mcp_server(n, enabled)` | MCP state                                                   |
| `stop_task(task_id)`                                                             | Stop a background task; a `TaskNotificationMessage` follows |
| `get_server_info()`                                                              | Session ID and capabilities                                 |

## Common Anti-Patterns

- `break`ing out of a `receive_messages()` / `receive_response()` loop → causes
  asyncio cleanup issues. Let iteration finish, or set a flag.
- Sending a new query right after `interrupt()` and reading one response →
  `interrupt()` does **not** clear the buffer. The interrupted task's messages,
  including its `ResultMessage` (with `terminal_reason` `"aborted_streaming"` or
  `"aborted_tools"`), are still queued. Drain them first.
- Calling `query()` once and expecting `receive_response()` to cover later turns →
  pair one `receive_response()` with each `query()`.

TypeScript has no client object; use `query()` plus the `Query` methods in
`query.md`, and `continue: true` for multi-turn.
