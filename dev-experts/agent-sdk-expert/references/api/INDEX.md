---
title: API reference
triggers:
  - "looking up an exact function, option, message field, or method name"
  - "choosing between query(), ClaudeSDKClient, and startup()"
  - "translating an option name between TypeScript and Python"
  - "catching SDK errors"
type: index
---

# API reference

The entry point is always `query()`. Pick the surface with the **first** rule that
applies:

1. **One prompt, no follow-up** → `query()` with a string prompt. Nothing else needed.
2. **You need interrupts, images, queued messages, or `canUseTool`** → streaming
   input: `query()` with an async iterable (TS), or `ClaudeSDKClient` (Python). See
   `../streaming-input.md`.
3. **Multi-turn in one process** → `ClaudeSDKClient` (Python, tracks the session
   ID for you) or `continue: true` on each `query()` (TypeScript). See
   `../sessions/INDEX.md`.
4. **Subprocess spawn latency is on the critical path** → `startup()` (TypeScript)
   at boot, then `.query()` on the returned `WarmQuery`.

Two rules that hold across the whole surface:

- **NEVER assume an option name transliterates.** Most are camelCase in TypeScript
  and snake_case in Python, but several Python fields keep camelCase to match the
  wire format (`AgentDefinition.disallowedTools`, `mcpServers`). Check
  `options.md` before writing one.
- **NEVER read `result` without checking `subtype` first**, and never assume the
  callable surface is the same in both languages — TypeScript mid-session control
  lives on the `Query` object, Python's on `ClaudeSDKClient`.

The two language references are the full generated API surface and are far larger
than anything here; escalate to them by URL when a symbol is not in these files.

<!-- BEGIN GENERATED INDEX -->

- [ClaudeSDKClient (Python)](./client.md) — multi-turn Python agent that keeps context across calls; interrupting a running Python agent; changing model or permission mode mid-session in Python; checking MCP server status from Python
- [Error types (Python)](./errors.md) — writing except clauses around an SDK call; catching a turn-limit or budget failure; distinguishing a process crash from an error result
- [Message and content block types](./messages.md) — reading text or tool calls out of a streamed message; message.content is undefined in TypeScript; getting the session id, tool list, or MCP status out of the init message; detecting compaction, or messages coming from inside a subagent
- [Options / ClaudeAgentOptions](./options.md) — finding the option that configures a behavior; translating an option name between TypeScript and Python; an option is rejected or silently ignored; passing an environment variable through to the subprocess
- [Python SDK reference (upstream)](./python.md) — a Python symbol is not covered by the local files; the exact ClaudeAgentOptions dataclass definition; Transport, ToolsPreset, ThinkingConfig, or McpServerConfig shapes
- [query() and startup()](./query.md) — writing the call that actually runs an agent; the exact signature or return type of query(); pre-warming the subprocess to cut first-call latency; calling interrupt, setModel, or setPermissionMode in TypeScript
- [V2 session API (removed)](./typescript-v2-preview.md) — code calls unstable_v2_createSession, unstable_v2_prompt, or unstable_v2_resumeSession; createSession() with send/stream is undefined
- [TypeScript SDK reference (upstream)](./typescript.md) — a TypeScript symbol is not covered by the local files; the exact input or output schema of a built-in tool; the full HookInput or HookJSONOutput union

<!-- END GENERATED INDEX -->
