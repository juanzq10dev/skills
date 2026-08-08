---
title: settingSources and CLAUDE.md
triggers:
  - "loading CLAUDE.md, project skills, filesystem hooks, or settings.json"
  - "the agent picks up the developer's local configuration and should not"
  - "isolating an agent for CI, tests, or multi-tenant deployment"
  - "which directory the SDK reads project files from"
---

# `settingSources` and CLAUDE.md

Docs: https://code.claude.com/docs/en/agent-sdk/claude-code-features

Omitting the option loads **user, project, and local** settings, matching the CLI:
`~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`,
CLAUDE.md files, `.claude/` skills, agents, and commands, `.mcp.json`, and shell
hooks. Pass `[]` to run on only what you configure programmatically.

```python
options = ClaudeAgentOptions(setting_sources=["user", "project"], allowed_tools=["Read", "Edit"])
```

```typescript
const options = {
  settingSources: ["user", "project"],
  allowedTools: ["Read", "Edit"],
};
```

| Source      | Loads                                                                              | From                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `"project"` | Project CLAUDE.md, `.claude/rules/*.md`, project skills and hooks, `settings.json` | `<cwd>/.claude/` for settings and hooks; `<cwd>` **and every parent** for CLAUDE.md and rules; `<cwd>` up to the repo root for skills |
| `"user"`    | User CLAUDE.md, `~/.claude/rules/*.md`, user skills and settings                   | `~/.claude/`                                                                                                                          |
| `"local"`   | `CLAUDE.local.md`, `.claude/settings.local.json`                                   | `<cwd>/.claude/`; `<cwd>` and parents for `CLAUDE.local.md`                                                                           |

`cwd` decides where project inputs come from. Project `settings.json` and hooks load
**only** from `<cwd>/.claude/`, with no parent fallback. CLAUDE.md in _subdirectories_
of cwd loads on demand when the agent reads a file there.

CLAUDE.md levels are additive with **no precedence rule** between them — if project
and user instructions conflict, the outcome depends on interpretation. Write
non-conflicting rules, or state precedence explicitly in the more specific file.

## What `settingSources` does NOT control

Read regardless of its value — this is the multi-tenant trap:

| Input                                                                                   | To disable                                                                                             |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Managed policy settings (MDM plist, registry, managed file) and server-managed settings | Remove the host policy; server-managed settings are org-controlled and cannot be disabled from the SDK |
| `~/.claude.json` global config                                                          | Relocate with `CLAUDE_CONFIG_DIR` in `env`                                                             |
| Auto memory at `~/.claude/projects/<project>/memory/`                                   | `autoMemoryEnabled: false`, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in `env`                            |
| claude.ai MCP connectors (when authenticated with a claude.ai login)                    | `strictMcpConfig: true`, `disableClaudeAiConnectors: true`, or `ENABLE_CLAUDEAI_MCP_SERVERS=false`     |

For multi-tenant work, run each tenant in its own filesystem with
`settingSources: []` **plus** `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` and a per-tenant
`CLAUDE_CONFIG_DIR` (`../production/hosting.md`). Passing `mcpServers: {}` does not
suppress connectors.

## Common Anti-Patterns

- Setting `settingSources` explicitly and dropping `"project"` → CLAUDE.md,
  `.mcp.json`, project skills, `.claude/settings.json` permission rules, and shell
  hooks all stop loading at once.
- Python ≤ 0.1.59 with `setting_sources=[]` → treated the same as omitting it.
  Upgrade before relying on isolation.
- Expecting auto-memory writes without `Write`/`Edit` → the agent saves memories
  with the standard file tools, so they must be enabled.
