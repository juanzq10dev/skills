---
title: Hooks
triggers:
  - "running custom code before or after a tool call"
  - "blocking a dangerous command, or auditing every tool use"
  - "rewriting a tool's arguments before it executes"
  - "a hook never fires, or its matcher matches nothing"
  - "archiving the transcript before compaction; tracking subagent start/stop"
  - "a check must run on every tool call regardless of permission mode"
---

# Hooks

Docs: https://code.claude.com/docs/en/agent-sdk/hooks

Callbacks that fire at points in the agent lifecycle. They run **in your process**,
so they cost no context, and they run **before every other permission step** — a
hook deny applies even in `bypassPermissions` mode. That makes a `PreToolUse` hook
the only reliable place for a check that must run on every call (`tools/permissions.md`).

```python
from claude_agent_sdk import ClaudeAgentOptions, HookMatcher

async def protect_env_files(input_data, tool_use_id, context):
    if input_data["tool_input"].get("file_path", "").split("/")[-1] == ".env":
        return {"hookSpecificOutput": {
            "hookEventName": input_data["hook_event_name"],
            "permissionDecision": "deny",
            "permissionDecisionReason": "Cannot modify .env files",
        }}
    return {}   # empty = allow

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Write|Edit", hooks=[protect_env_files])]}
)
```

```typescript
import {
  query,
  HookCallback,
  PreToolUseHookInput,
} from "@anthropic-ai/claude-agent-sdk";

const protectEnvFiles: HookCallback = async (input, toolUseID, { signal }) => {
  const pre = input as PreToolUseHookInput;
  const toolInput = pre.tool_input as Record<string, unknown>;
  if ((toolInput?.file_path as string)?.split("/").pop() === ".env") {
    return {
      hookSpecificOutput: {
        hookEventName: pre.hook_event_name,
        permissionDecision: "deny",
        permissionDecisionReason: "Cannot modify .env files",
      },
    };
  }
  return {};
};

query({
  prompt: "…",
  options: {
    hooks: {
      PreToolUse: [{ matcher: "Write|Edit", hooks: [protectEnvFiles] }],
    },
  },
});
```

Callback signature is `(input, toolUseId, context)` in both SDKs. All inputs carry
`session_id`, `cwd`, `hook_event_name`; `agent_id` / `agent_type` are set when the
hook fires inside a subagent.

## Events

Both SDKs: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `UserPromptSubmit`,
`Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PermissionRequest`,
`Notification`.

TypeScript only: `PostToolBatch`, `UserPromptExpansion`, `MessageDisplay`,
`StopFailure`, `PostCompact`, `PermissionDenied`, `SessionStart`, `SessionEnd`,
`Setup`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `Elicitation`,
`ElicitationResult`, `ConfigChange`, `InstructionsLoaded`, `WorktreeCreate`,
`WorktreeRemove`, `CwdChanged`, `FileChanged`, `DirectoryAdded`.

In Python, `SessionStart` / `SessionEnd` exist only as shell-command hooks in
`settings.json`, loaded via `setting_sources` (`config/setting-sources.md`).

## Outputs

Top-level: `systemMessage` (shown to the user, not the model), `continue`
(`continue_` in Python), `async` (`async_` in Python) + `asyncTimeout` for
fire-and-forget side effects.

`hookSpecificOutput` controls the operation. For `PreToolUse`:
`permissionDecision` (`"allow"` | `"deny"` | `"ask"` | `"defer"`),
`permissionDecisionReason`, `updatedInput`. For `PostToolUse`: `additionalContext`
to append to the tool result, `updatedToolOutput` to replace it.

Across hooks and rules, precedence is `deny` > `defer` > `ask` > `allow`. All
matching hooks run in parallel with non-deterministic completion order — write each
to act independently.

## Matchers

A matcher of only letters, digits, `_`, `-`, spaces, `,`, `|` is an **exact** match
with `|`/`,` alternatives (`Write|Edit`). Anything else is an **unanchored regex**
(`^mcp__`, `Edit.*`). Omitting the matcher, `*`, or `""` matches every event.

`mcp__memory` therefore matches nothing (exact-match path, no such tool) — write
`mcp__memory__.*`. `StopFailure` and `FileChanged` use a narrower exact set
(letters, digits, `_`, `|` only), so use `rate_limit|overloaded`, not commas.

## Common Anti-Patterns

- `updatedInput` at the top level → it must be inside `hookSpecificOutput`, and it
  is dropped when paired with `permissionDecision: "defer"`.
- Filtering by file path in the matcher → matchers only see the tool name; check
  `tool_input.file_path` inside the callback.
- Letting an exception escape a hook → it can interrupt the agent. Catch inside.
- Expecting `systemMessage` in the stream → only `SessionStart` and `Setup` surface
  by default; set `includeHookEvents` / `include_hook_events`, or return
  `additionalContext` to reach the model instead.
- Case-typo event names (`preToolUse`) → they are case-sensitive and silently never fire.

Timeouts default to 600s (30s for `UserPromptSubmit`, 10s for `MessageDisplay`); set
`timeout` in seconds on the `HookMatcher`. A timed-out `PreToolUse` skips the tool
and tells Claude the hook didn't respond.
