---
title: Message and content block types
triggers:
  - "reading text or tool calls out of a streamed message"
  - "message.content is undefined in TypeScript"
  - "getting the session id, tool list, or MCP status out of the init message"
  - "detecting compaction, or messages coming from inside a subagent"
---

# Message and content block types

Docs: https://code.claude.com/docs/en/agent-sdk/typescript#message-types and
https://code.claude.com/docs/en/agent-sdk/python#message-types

## The shape difference that breaks code

TypeScript `SDKAssistantMessage` / `SDKUserMessage` **wrap** the raw API message, so
content is at `message.message.content`. Python's `AssistantMessage` exposes
`message.content` directly.

```typescript
if (message.type === "assistant") {
  for (const block of message.message.content) {
    // note: .message.content
    if (block.type === "text") console.log(block.text);
    if (block.type === "tool_use") console.log(block.name, block.input);
  }
}
```

```python
if isinstance(message, AssistantMessage):
    for block in message.content:                     # note: .content
        if isinstance(block, TextBlock):
            print(block.text)
        elif isinstance(block, ToolUseBlock):
            print(block.name, block.input)
```

Discriminate by `message.type` string in TypeScript, by `isinstance()` against
classes imported from `claude_agent_sdk` in Python.

Content blocks: `TextBlock`, `ThinkingBlock`, `ToolUseBlock`, `ToolResultBlock`.

## `SystemMessage` with `subtype: "init"`

Carries the session's real capability inventory — prefer it over guessing: `tools`,
`slash_commands`, `skills`, `plugins`, `mcp_servers`, `session_id`.

```typescript
if (message.type === "system" && message.subtype === "init") {
  console.log(message.session_id, message.tools, message.mcp_servers);
}
```

```python
if isinstance(message, SystemMessage) and message.subtype == "init":
    print(message.data.get("tools"), message.data.get("mcp_servers"))
```

**Python nests these under `message.data`; TypeScript exposes them as direct
fields.** Other `SystemMessage` subtypes are `compact_boundary`, `informational`,
`worker_shutting_down` — in TypeScript each non-`init` subtype is its own type in
the `SDKMessage` union (e.g. `SDKCompactBoundaryMessage`), not a subtype of
`SDKSystemMessage`.

## `ResultMessage`

`subtype`, `result` (success only), `total_cost_usd`, `usage`, `modelUsage` /
`model_usage`, `num_turns`, `session_id`, `stop_reason`, `structured_output`,
`errors`. Branching rules: `../agent-loop.md`. Usage semantics: `../production/cost-tracking.md`.

## Other messages

`UserMessage` (tool results, and inputs you stream in; `uuid` is the checkpoint id —
`../sessions/checkpointing.md`), `StreamEvent` / `SDKPartialAssistantMessage`
(`../streaming-output.md`), `SDKUserMessageReplay`, `SDKPermissionDeniedMessage`,
`RateLimitEvent`, `TaskStartedMessage` / `TaskProgressMessage` /
`TaskNotificationMessage`, `SDKPluginInstallMessage`, `SDKWorkerShuttingDownMessage`.

`parent_tool_use_id` is set on messages originating inside a subagent.

## Common Anti-Patterns

- `message.content` in TypeScript → `undefined`; it is `message.message.content`.
- `message.tools` in Python → it is `message.data["tools"]`.
- Assuming Python types are all dataclasses → `@dataclass` types (`ResultMessage`,
  `TextBlock`, `AgentDefinition`) support attribute access; `TypedDict` types
  (`ThinkingConfigEnabled`, `McpStdioServerConfig`, `SyncHookJSONOutput`) are plain
  dicts at runtime and need `config["key"]`.
