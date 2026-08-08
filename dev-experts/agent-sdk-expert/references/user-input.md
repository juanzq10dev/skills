---
title: Approval prompts and clarifying questions
triggers:
  - "surfacing a tool request to a human for approval"
  - "implementing an allow / deny / always-allow prompt"
  - "handling AskUserQuestion, or the agent asking a multiple-choice question"
  - "rewriting a tool's arguments at approval time"
---

# Approval prompts and clarifying questions

Docs: https://code.claude.com/docs/en/agent-sdk/user-input

`canUseTool` / `can_use_tool` is the interactive step of the permission flow: it
runs only when no earlier step resolved the call (`tools/permissions.md`).

Callback args: `toolName`, `input`, then `options` (TS, with `signal: AbortSignal`
and optional `suggestions`) / `context` (Python, a `ToolPermissionContext`).

```typescript
const options = {
  canUseTool: async (toolName, input) => {
    const ok = await askUser(`Allow ${toolName}?`);
    return ok
      ? { behavior: "allow", updatedInput: input }
      : { behavior: "deny", message: "User declined" };
  },
};
```

```python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

async def can_use_tool(tool_name, input_data, context):
    if await ask_user(f"Allow {tool_name}?"):
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User declined")
```

`updatedInput` / `updated_input` lets you approve a **modified** call — e.g. rewrite
a Bash command to stay inside a sandbox path. The `deny` `message` is what Claude
reads, so use it to redirect ("compress them into an archive instead") rather than
just refuse.

For an "always allow" choice, persist the SDK's proposed rules instead of
re-prompting:

```typescript
canUseTool: async (toolName, input, { suggestions = [] }) => {
  const persist = suggestions.filter((s) => s.destination === "localSettings");
  return {
    behavior: "allow",
    updatedInput: input,
    updatedPermissions: persist,
  };
};
```

## AskUserQuestion

Claude asks a multiple-choice question through the `AskUserQuestion` tool, which
always reaches `canUseTool` — even when an allow rule matches. Route it in the
callback and answer by returning the **original questions plus an `answers` map**:

```python
if tool_name == "AskUserQuestion":
    return PermissionResultAllow(updated_input={
        "questions": input_data.get("questions", []),
        "answers": {"How should I format the output?": "Summary"},
    })
```

Question fields: `question`, `header` (≤12 chars), `options` (2–4 entries of
`label` + `description`), `multiSelect`. Response fields: `questions` (pass through,
required), `answers` (keys are the question text, values are selected labels), and
optional `response` for free text the user typed instead. TypeScript can request
rendered option previews with `toolConfig: { askUserQuestion: { previewFormat: "html" } }`
(or `"markdown"`); the SDK strips `<script>`, `<style>`, and `<!DOCTYPE>` first.

## Common Anti-Patterns

- Putting a tool in `allowedTools` **and** gating it in `canUseTool` → an allow rule
  approves it first and the callback never runs. Use a `PreToolUse` hook for checks
  that must always run (`hooks.md`).
- Python: calling `can_use_tool` with a plain string prompt → it needs streaming
  input, plus a no-op `PreToolUse` `HookMatcher` to keep the stream open:

```python
async def dummy_hook(input_data, tool_use_id, context):
    return {"continue_": True}

options = ClaudeAgentOptions(
    can_use_tool=can_use_tool,
    hooks={"PreToolUse": [HookMatcher(matcher=None, hooks=[dummy_hook])]},
)
```

- Dropping `questions` from the `AskUserQuestion` response → the tool cannot process
  the answer without them.
