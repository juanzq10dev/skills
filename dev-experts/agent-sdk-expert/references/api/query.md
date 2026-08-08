---
title: query() and startup()
triggers:
  - "writing the call that actually runs an agent"
  - "the exact signature or return type of query()"
  - "pre-warming the subprocess to cut first-call latency"
  - "calling interrupt, setModel, or setPermissionMode in TypeScript"
---

# `query()` and `startup()`

Docs: https://code.claude.com/docs/en/agent-sdk/typescript#query and
https://code.claude.com/docs/en/agent-sdk/python#query

```typescript
function query({
  prompt,
  options,
}: {
  prompt: string | AsyncIterable<SDKUserMessage>;
  options?: Options;
}): Query; // extends AsyncGenerator<SDKMessage, void>
```

```python
async def query(
    *, prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None,
) -> AsyncIterator[Message]
```

Each `query()` call starts a fresh session unless you pass `continue`/
`continue_conversation` or `resume`.

## The `Query` object (TypeScript)

The returned iterator also carries mid-session controls. Those marked streaming-only
require an async-iterable prompt.

| Method                                                                                              | Purpose                                                                  |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `interrupt()`                                                                                       | Stop the query (streaming input only)                                    |
| `setPermissionMode(mode)`                                                                           | Change permission mode mid-session (streaming input only)                |
| `setModel(model?)`                                                                                  | Change model; `undefined` or `"default"` resets                          |
| `rewindFiles(userMessageId, options?)`                                                              | Restore files; `{dryRun:true}` previews. Needs `enableFileCheckpointing` |
| `initializationResult()` / `reinitialize()`                                                         | Full init result; re-send `initialize` after a transport gap             |
| `supportedCommands()` / `supportedModels()` / `supportedAgents()`                                   | Live capability lists                                                    |
| `mcpServerStatus()` / `reconnectMcpServer(n)` / `toggleMcpServer(n, on)` / `setMcpServers(servers)` | MCP state                                                                |
| `getContextUsage()`                                                                                 | Context breakdown, same data as `/context`                               |
| `streamInput(stream)` / `stopTask(taskId)` / `close()`                                              | Feed input, stop a background task, terminate                            |
| `applyFlagSettings(settings)`                                                                       | Merge settings at runtime (streaming input only)                         |

`setMaxThinkingTokens()` is deprecated — use the `thinking` option.

## `startup()` (TypeScript)

```typescript
import { startup } from "@anthropic-ai/claude-agent-sdk";

const warm = await startup({ options: { maxTurns: 3 } }); // pay spawn cost at boot
for await (const message of warm.query("What files are here?"))
  console.log(message);
```

`startup(params?: { options?: Options; initializeTimeoutMs?: number })` spawns the
subprocess and completes the initialize handshake before a prompt exists;
`initializeTimeoutMs` defaults to 60000 and rejects on timeout.

Python's equivalent multi-call surface is `ClaudeSDKClient` — see `client.md`.
Session-oriented functions (`listSessions`, `getSessionMessages`, `renameSession`,
`tagSession`, and their Python snake_case twins) are covered in
`../sessions/INDEX.md`.
