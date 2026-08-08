---
title: Options / ClaudeAgentOptions
triggers:
  - "finding the option that configures a behavior"
  - "translating an option name between TypeScript and Python"
  - "an option is rejected or silently ignored"
  - "passing an environment variable through to the subprocess"
---

# `Options` (TS) / `ClaudeAgentOptions` (Python)

Docs: https://code.claude.com/docs/en/agent-sdk/typescript#options and
https://code.claude.com/docs/en/agent-sdk/python#claudeagentoptions

Options are a nested object in TypeScript and a dataclass in Python:

```typescript
query({
  prompt: "…",
  options: { allowedTools: ["Read"], permissionMode: "acceptEdits" },
});
```

```python
query(prompt="…", options=ClaudeAgentOptions(
    allowed_tools=["Read"], permission_mode="acceptEdits"))
```

Names below are `typescript` / `python`. Where only one is shown, both spell it the
same. This is the shared surface; the language references are authoritative for
exact types and for TypeScript-only fields.

## Tools and permissions → `../tools/INDEX.md`

`tools` (list of built-ins available at all, or a `ToolsPreset`), `allowedTools` /
`allowed_tools`, `disallowedTools` / `disallowed_tools`, `permissionMode` /
`permission_mode`, `canUseTool` / `can_use_tool`, `permissionPromptToolName` /
`permission_prompt_tool_name`, `toolConfig`, `toolAliases`,
`allowDangerouslySkipPermissions` (TS; required alongside `bypassPermissions`).

## Model and reasoning

`model`, `fallbackModel` / `fallback_model`, `effort`, `thinking`, `taskBudget` /
`task_budget`, `betas`, `maxTurns` / `max_turns`, `maxBudgetUsd` / `max_budget_usd`.
`maxThinkingTokens` / `max_thinking_tokens` is deprecated — use `thinking`.

## Prompt and project context → `../config/INDEX.md`

`systemPrompt` / `system_prompt` (string, `{type:"preset",preset:"claude_code",append?,excludeDynamicSections?}`,
or Python `{type:"file",path}`), `settingSources` / `setting_sources`, `settings`,
`managedSettings`, `strictMcpConfig` / `strict_mcp_config`, `skills`, `agents`,
`plugins`, `outputStyle` (TS; also settable inside `settings`), `planModeInstructions`.

## Sessions → `../sessions/INDEX.md`

`continue` / `continue_conversation`, `resume`, `resumeSessionAt`, `forkSession` /
`fork_session`, `sessionId` / `session_id`, `sessionStore` / `session_store`,
`sessionStoreFlush`, `persistSession` (TS only),
`enableFileCheckpointing` / `enable_file_checkpointing`.

## Process and I/O

`cwd`, `additionalDirectories` (TS) / `add_dirs` (Python), `env`,
`pathToClaudeCodeExecutable` (TS) / `cli_path` (Python), `executable`,
`executableArgs`, `extraArgs` / `extra_args`, `abortController` (TS), `stderr`,
`debug` / `debugFile`, `maxBufferSize` / `max_buffer_size`, `loadTimeoutMs`, `user`,
`sandbox`, `title`.

## Streaming and output

`includePartialMessages` / `include_partial_messages`, `includeHookEvents` /
`include_hook_events`, `outputFormat` / `output_format`, `hooks`, `mcpServers` /
`mcp_servers`, `onElicitation`, `agentProgressSummaries`, `forwardSubagentText`,
`promptSuggestions`.

## Common Anti-Patterns

- `env` treated the same in both languages → in **TypeScript it replaces** the
  subprocess environment (spread `...process.env` to keep `PATH` and
  `ANTHROPIC_API_KEY`); in **Python it merges** onto the inherited environment.
- Expecting every Python field to be snake_case → `AgentDefinition` keeps camelCase
  for `disallowedTools`, `mcpServers`, `initialPrompt`, `maxTurns`, and
  `permissionMode` to match the wire format (`../config/subagents.md`).
- Setting `outputStyle` at the top level in TypeScript → the guide says to put it
  inside `settings` (`{ settings: { outputStyle: "Explanatory" } }`), while the
  `Options` type reference also lists a top-level `outputStyle`. **Upstream docs
  disagree; prefer the `settings` form**, which is the one the guide documents.
- Passing a huge `system_prompt` string in Python → it becomes one CLI argument and
  can exceed the OS limit (`Argument list too long`); use
  `{"type": "file", "path": ...}`.
- Confusing `tools` with `allowedTools` → `tools` controls **availability** (what
  Claude sees at all); `allowedTools` controls **permission** (what runs without a
  prompt).
