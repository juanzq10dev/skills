---
title: Todo and task progress
triggers:
  - "rendering the agent's task list or a progress bar"
  - "TodoWrite tool_use blocks never appear in the stream"
  - "migrating a TodoWrite watcher to TaskCreate / TaskUpdate"
---

# Todo and task progress

Docs: https://code.claude.com/docs/en/agent-sdk/todo-tracking

Progress is visible as ordinary `tool_use` blocks in `AssistantMessage`s — there is
no separate todo API. Current builds use the **Task tools**; `TodoWrite` only
appears when tasks are disabled.

```typescript
for await (const message of query({ prompt, options: { maxTurns: 15 } })) {
  if (message.type !== "assistant") continue;
  for (const block of message.message.content) {
    if (block.type !== "tool_use") continue;
    if (block.name === "TaskCreate")
      console.log(`+ ${(block.input as any).subject}`);
    else if (block.name === "TaskUpdate") {
      const i = block.input as any;
      const taskId = i.taskId ?? i.id ?? i.task_id;
      if (taskId && i.status) console.log(`  ${taskId} -> ${i.status}`);
    }
  }
}
```

```python
for block in message.content:
    if isinstance(block, ToolUseBlock) and block.name == "TaskCreate":
        print(f"+ {block.input['subject']}")
```

| With `TodoWrite`                           | With Task tools                                                                                                  |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| One call rewrites the whole `todos` array  | `TaskCreate` adds one item; `TaskUpdate` patches one by `taskId`                                                 |
| Item shape `{content, status, activeForm}` | `TaskCreate`: `{subject, description, activeForm?, metadata?}`; `TaskUpdate`: `{taskId, status?, subject?, ...}` |
| Render `block.input.todos` directly        | Accumulate across calls, or read a `TaskList` tool result                                                        |

`status` is `"pending"`, `"in_progress"`, or `"completed"`; `TaskUpdate` with
`status: "deleted"` removes the item.

## Common Anti-Patterns

- Watching for `TodoWrite` on a current build → nothing matches. Either migrate to
  the Task tools, or set `CLAUDE_CODE_ENABLE_TASKS: "0"` in `env` to re-enable
  `TodoWrite`. In TypeScript `env` **replaces** the subprocess environment, so
  spread `...process.env`; in Python it merges.
- Assuming `TaskUpdate` always spells the id `taskId` → accept `id` and `task_id` too.
