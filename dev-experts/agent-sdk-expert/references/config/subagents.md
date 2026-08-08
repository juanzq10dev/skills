---
title: Subagents
triggers:
  - "delegating an isolated subtask to keep the main context small"
  - "running several analyses in parallel"
  - "giving one part of the work a different model, prompt, or tool set"
  - "Claude never delegates to a defined subagent"
  - "resuming a subagent to ask a follow-up"
---

# Subagents

Docs: https://code.claude.com/docs/en/agent-sdk/subagents

Separate agent instances with their own fresh conversation. Only the final message
returns to the parent, so a subagent can read dozens of files without any of it
landing in the main context. Define them programmatically with `agents`.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Agent"],       # Agent auto-approves invocation
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code review specialist. Use for quality and security reviews.",
            prompt="You are a code review specialist. Identify security vulnerabilities…",
            tools=["Read", "Grep", "Glob"],                # read-only
            model="sonnet",
        ),
    },
)
```

```typescript
const options = {
  allowedTools: ["Read", "Grep", "Glob", "Agent"],
  agents: {
    "code-reviewer": {
      description:
        "Expert code review specialist. Use for quality and security reviews.",
      prompt:
        "You are a code review specialist. Identify security vulnerabilities…",
      tools: ["Read", "Grep", "Glob"],
      model: "sonnet",
    },
  },
};
```

`AgentDefinition` fields: `description` and `prompt` (both required), `tools`,
`disallowedTools`, `model` (`'fable'`, `'opus'`, `'sonnet'`, `'haiku'`, `'inherit'`,
or a full ID), `skills`, `memory`, `mcpServers`, `initialPrompt`, `maxTurns`,
`background`, `effort`, `permissionMode`.

**In Python, the multi-word fields keep camelCase** (`disallowedTools`,
`mcpServers`, `initialPrompt`, `maxTurns`, `permissionMode`) to match the wire
format — they are not snake_case.

Claude picks a subagent from its `description`, so write it as "when to use this".
Name it in the prompt ("Use the code-reviewer agent to…") to force it.

## What a subagent inherits

| Receives                                            | Does not receive                                  |
| --------------------------------------------------- | ------------------------------------------------- |
| Its own `prompt` + the Agent tool's prompt string   | The parent's conversation history or tool results |
| Project CLAUDE.md (via `settingSources`)            | Preloaded skill content unless listed in `skills` |
| Tool definitions (inherited, or the `tools` subset) | The parent's system prompt                        |

**The Agent tool's prompt string is the only channel from parent to subagent** — put
every file path, error message, and decision it needs directly in there.

## Common Anti-Patterns

- Omitting `Agent` from `allowedTools` → invocations fall through to `canUseTool`,
  or are denied in `dontAsk`, and Claude appears to "refuse to delegate".
- Assuming a subagent's `permissionMode` wins → subagents inherit the parent's, and
  `bypassPermissions`, `acceptEdits`, and `auto` cannot be overridden per subagent
  (`../tools/permissions.md`).
- Matching only `"Task"` in `tool_use` blocks → renamed to `"Agent"` in Claude Code
  v2.1.63. Current releases emit `"Agent"` in blocks but still say `"Task"` in the
  init tools list and in `result.permission_denials[].tool_name` — match both.
- Expecting a subagent's text verbatim → the parent may summarize it; instruct
  otherwise in the main prompt. Since v2.1.210 the final message is also scanned for
  instruction-shaped patterns and neutralized in place with a `[harness: …]` marker.
- Expecting synchronous runs → since v2.1.198 subagents run in the **background** by
  default when `run_in_background` is omitted. Nesting defaults to three layers
  below the main conversation; change with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`.

## Resume a subagent

Capture `session_id` from the messages and `agentId: <id>` from the Agent tool
result text, then pass `resume: sessionId` with the same `agents` definitions and
name the agent id in the prompt. The built-in `Explore` and `Plan` agents are
one-shot and return no `agentId`.

For runs coordinating dozens to hundreds of agents, use the `Workflow` tool instead
(TypeScript SDK v0.3.149+; include `Workflow` in `allowedTools`).
