---
title: Tools and permissions
triggers:
  - "deciding how to give an agent a new capability"
  - "the agent can see a tool but never calls it"
  - "locking down what an agent is allowed to do"
  - "tool definitions are eating the context window"
type: index
---

# Tools and permissions

## Which mechanism

Use the **first** option that applies:

1. **A built-in already does it** (`Read`, `Edit`, `Write`, `Bash`, `Glob`, `Grep`,
   `WebSearch`, `WebFetch`, `Agent`, `Skill`, `AskUserQuestion`, …) → enable it. Do
   not wrap a built-in in a custom tool. See `built-in.md`.
2. **A maintained MCP server already does it** (filesystem, GitHub, Slack,
   Postgres) → configure `mcpServers`. Do not reimplement it. See `mcp.md`.
3. **It is your own function, API, or domain logic** → define a custom tool on an
   in-process SDK MCP server. See `custom-tools.md`.

Then, always: **grant permission explicitly.** A tool Claude can see but has no
allow rule for falls through to the permission mode or `canUseTool`, which in a
headless agent usually means denied.

## Availability is not permission

Two different layers, and conflating them is the most common bug in this area:

| Lever                                      | Layer        | Effect                                                      |
| ------------------------------------------ | ------------ | ----------------------------------------------------------- |
| `tools: [...]`                             | availability | Only these built-ins exist in Claude's context              |
| `disallowedTools: ["Bash"]` (bare name)    | availability | Removes the tool from context entirely                      |
| `allowedTools: [...]`                      | permission   | Listed calls run without prompting; others still exist      |
| `disallowedTools: ["Bash(rm *)"]` (scoped) | permission   | Denies matching calls in **every** mode, tool stays visible |

To stop Claude attempting something, remove it from context. To stop a _specific_
call, scope a deny rule.

## Rules that hold everywhere

- **ALWAYS prefer `allowedTools` over a broad permission mode for MCP access.**
  `acceptEdits` does not auto-approve MCP tools at all, and `bypassPermissions`
  approves everything, which is far broader than needed. A wildcard like
  `mcp__github__*` grants exactly one server.
- **NEVER rely on `allowedTools` to constrain `bypassPermissions`.** Unlisted tools
  are not matched by any allow rule, fall through to the mode, and are approved.
  Use `disallowedTools` if you need blocks in that mode.
- **NEVER put a security check only in `canUseTool`.** Anything auto-approved
  earlier — by an allow rule, `acceptEdits`, or `bypassPermissions` — skips the
  callback silently. Checks that must always run belong in a `PreToolUse` hook
  (`../hooks.md`), which runs before every other step and whose deny wins even in
  `bypassPermissions`.
- **Tool search is on by default** and defers tool schemas until needed. Leave it on
  above ~10 tools; turn it off below that (`tool-search.md`).

<!-- BEGIN GENERATED INDEX -->

- [Built-in tools](./built-in.md) — choosing which tools an agent needs for a task; making an agent read-only, or giving it shell access; removing a built-in tool from the agent entirely; tool calls running one at a time when they could be parallel
- [Custom tools (SDK MCP server)](./custom-tools.md) — letting the agent call your own function, API, or database; defining a tool with a schema and an async handler; returning an image, a file, or machine-readable JSON from a tool; controlling the error message the model sees when a tool fails; an optional tool parameter
- [MCP servers](./mcp.md) — connecting the agent to GitHub, Slack, a database, or another external service; choosing stdio vs http vs sse transport; passing an API key or bearer token to an MCP server; a server shows failed, pending, or needs-auth at init; MCP tools exist but Claude never calls them; MCP connection timeouts, or tool output exceeding the token limit
- [Permission modes and rules](./permissions.md) — choosing a permission mode for an agent; a tool is blocked or auto-approved unexpectedly; canUseTool is never called; running an agent headless with no prompts; changing how permissive the agent is mid-session; subagents inheriting dangerous permissions
- [Tool search](./tool-search.md) — dozens or hundreds of tools, and tool selection is degrading; tool definitions consuming too much of the context window; an extra ToolSearch call appears before the agent uses a tool; turning tool deferral off for a small tool set

<!-- END GENERATED INDEX -->
