---
title: Permission modes and rules
triggers:
  - "choosing a permission mode for an agent"
  - "a tool is blocked or auto-approved unexpectedly"
  - "canUseTool is never called"
  - "running an agent headless with no prompts"
  - "changing how permissive the agent is mid-session"
  - "subagents inheriting dangerous permissions"
---

# Permission modes and rules

Docs: https://code.claude.com/docs/en/agent-sdk/permissions

## Evaluation order

Every tool request walks these steps in order. Knowing the order explains nearly
every "why did that run / not run" question:

1. **Hooks** — a `PreToolUse` hook can deny outright. A hook `allow` does **not**
   skip the deny and ask rules below.
2. **Deny rules** (`disallowedTools` + `settings.json`) — block even in
   `bypassPermissions`. Bare-name denies removed the tool from context earlier, so
   only scoped rules like `Bash(rm *)` are evaluated here.
3. **Ask rules** (`settings.json`) — fall through to `canUseTool` even in
   `bypassPermissions`. `AskUserQuestion`, MCP tools marked
   `_meta["anthropic/requiresUserInteraction"]`, and org-set `ask` connector tools
   always land here, even when an allow rule matches.
4. **Permission mode** — `bypassPermissions` approves; `acceptEdits` approves file
   ops; `plan` routes file-edit and shell-write tools to `canUseTool` regardless of
   allow rules; others fall through.
5. **Allow rules** (`allowedTools` + `settings.json`) — approve.
6. **`canUseTool`** — your callback decides (`../user-input.md`). In `dontAsk` this
   step is skipped and the tool is denied.

## Modes

| Mode                | Behavior                                                                                                                                                                      |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | No auto-approvals; unmatched tools hit `canUseTool` (no callback ⇒ deny)                                                                                                      |
| `acceptEdits`       | Auto-approves `Edit`/`Write` and filesystem commands (`mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, `sed`) inside cwd/`additionalDirectories`; other Bash follows normal rules |
| `plan`              | Explore and plan; file edits are never auto-approved and always prompt                                                                                                        |
| `dontAsk`           | Anything not pre-approved is denied; `canUseTool` is never called                                                                                                             |
| `auto`              | A model classifier approves or denies prompts                                                                                                                                 |
| `bypassPermissions` | Approves everything reaching step 4. TS also needs `allowDangerouslySkipPermissions: true`. Cannot run as root on Unix                                                        |

Interactive apps: `default` + a `canUseTool` callback. Autonomous agent on a dev
machine: `acceptEdits`. Headless with a fixed tool surface: `allowedTools` +
`dontAsk` — a hard deny beats silently relying on `canUseTool` being absent. CI and
containers only: `bypassPermissions`.

```typescript
const options = {
  allowedTools: ["Read", "Glob", "Grep"],
  permissionMode: "dontAsk",
};
```

Change it mid-session with `setPermissionMode()` (TS `Query`) or
`set_permission_mode()` (Python `ClaudeSDKClient`) — e.g. start `default` and move
to `acceptEdits` once you trust the approach.

## Common Anti-Patterns

- **`allowedTools` + `bypassPermissions`** → does **not** restrict anything.
  Unlisted tools match no allow rule, fall to the mode, and are approved. Use
  `disallowedTools`.
- **Security checks in `canUseTool` for an allow-listed tool** → auto-approved calls
  skip the callback. A bare name like `Read` auto-approves every call to it; a
  scoped rule like `Bash(ls *)` only auto-approves matches, so other `Bash` calls
  still reach the callback. For universal checks use a `PreToolUse` hook.
- **Assuming a subagent honors its own `permissionMode`** → subagents inherit the
  parent's, and `bypassPermissions`, `acceptEdits`, and `auto` **cannot** be
  overridden per subagent. A subagent with a looser prompt then has full autonomous
  access (`../config/subagents.md`).
- **Ignoring the shadowed-callback warning** → from v2.1.198 TypeScript emits a
  Node process warning with code `CLAUDE_SDK_CAN_USE_TOOL_SHADOWED` when
  `bypassPermissions` or a bare `allowedTools` entry makes your callback
  unreachable. Listen with `process.on('warning', …)`.

Declarative allow/deny/ask rules can also live in `.claude/settings.json`, read when
the `project` setting source is enabled (`../config/setting-sources.md`).
