---
title: TypeScript SDK reference (upstream)
triggers:
  - "a TypeScript symbol is not covered by the local files"
  - "the exact input or output schema of a built-in tool"
  - "the full HookInput or HookJSONOutput union"
---

# TypeScript SDK reference (upstream)

Docs: https://code.claude.com/docs/en/agent-sdk/typescript

The complete generated surface for `@anthropic-ai/claude-agent-sdk`: every `Options`
property, the full `SDKMessage` union, all `HookEvent` / `HookInput` /
`HookJSONOutput` variants, `PermissionResult`, `McpServerConfig`, `SdkPluginConfig`,
`AgentDefinition`, and per-tool **`ToolInputSchemas` / `ToolOutputSchemas`** for
every built-in tool. Fetch it when a symbol is not in the local files.

Also on that page: `listSessions()`, `getSessionMessages()`, `getSessionInfo()`,
`renameSession()`, `tagSession()`, `resolveSettings()`, and compiling an agent to a
single executable.
