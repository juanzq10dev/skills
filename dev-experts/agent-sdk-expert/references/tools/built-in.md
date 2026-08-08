---
title: Built-in tools
triggers:
  - "choosing which tools an agent needs for a task"
  - "making an agent read-only, or giving it shell access"
  - "removing a built-in tool from the agent entirely"
  - "tool calls running one at a time when they could be parallel"
---

# Built-in tools

Docs: https://code.claude.com/docs/en/agent-sdk/agent-loop#built-in-tools

The SDK ships the same tools that power Claude Code.

| Category        | Tools                                                           |
| --------------- | --------------------------------------------------------------- |
| File operations | `Read`, `Edit`, `Write`                                         |
| Search          | `Glob`, `Grep`                                                  |
| Execution       | `Bash`                                                          |
| Web             | `WebSearch`, `WebFetch`                                         |
| Discovery       | `ToolSearch`                                                    |
| Orchestration   | `Agent`, `Skill`, `AskUserQuestion`, `TaskCreate`, `TaskUpdate` |

Common capability sets:

```typescript
{
  allowedTools: ["Read", "Glob", "Grep"];
} // read-only analysis
{
  allowedTools: ["Read", "Edit", "Glob"];
} // analyze and modify code
{
  allowedTools: ["Read", "Edit", "Bash", "Glob", "Grep"];
} // full automation
```

```python
ClaudeAgentOptions(allowed_tools=["Read", "Grep", "Glob", "Agent"])   # + subagents
```

Include `Agent` whenever subagents should be invoked without a prompt
(`../config/subagents.md`), and `Skill` when you pass an explicit `tools` list and
still want skills invocable (`../config/skills.md`).

## Remove a tool completely

`tools: ["Read", "Grep"]` leaves only those built-ins in context (`tools: []`
removes all of them, leaving MCP tools). A bare `disallowedTools: ["Bash"]` does the
same for one tool. `disallowedTools: ["*"]` removes every tool definition;
`"mcp__*"` removes every MCP tool.

Prefer removing over deny-scoping when Claude should never attempt the tool — a
scoped deny leaves it visible, so Claude can waste a turn trying it.

## Path-scoped rules

`Read(...)` and `Edit(...)` rules take a path pattern. **`Edit(path)` governs every
built-in that writes files**, including `Write` and `NotebookEdit` — a `Write(path)`
rule is never matched by the file permission checks.

Use `//path` for an absolute filesystem path: `Edit(//secrets/**)` blocks writes
under `/secrets` on disk. A single leading slash (`Edit(/secrets/**)`) anchors at
the rule's source, which for `allowedTools`/`disallowedTools` is the session's
working directory.

## Parallel execution

Read-only tools (`Read`, `Glob`, `Grep`, and MCP tools marked read-only) can run
concurrently; state-modifying tools (`Edit`, `Write`, `Bash`) are serialized.
Custom tools default to **sequential** — set `readOnlyHint: true` in their
annotations to let Claude batch them (`custom-tools.md`).
