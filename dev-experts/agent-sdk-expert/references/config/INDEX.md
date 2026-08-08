---
title: Behavior and project configuration
triggers:
  - "shaping how the agent behaves beyond the prompt"
  - "choosing between CLAUDE.md, a system prompt, a skill, and a subagent"
  - "the agent ignores project conventions"
  - "isolating an agent from the developer's local configuration"
type: index
---

# Behavior and project configuration

## Which mechanism

| Goal                                              | Use                            | Surface                                               |
| ------------------------------------------------- | ------------------------------ | ----------------------------------------------------- |
| Conventions the agent always follows in a project | CLAUDE.md                      | `settingSources: ["project"]` (`setting-sources.md`)  |
| Reference material loaded only when relevant      | Skills                         | `settingSources` + `skills` (`skills.md`)             |
| A reusable workflow a user invokes                | User-invocable skill / command | `skills.md`, `slash-commands.md`                      |
| An isolated subtask in a fresh context            | Subagents                      | `agents` + `allowedTools: ["Agent"]` (`subagents.md`) |
| Product-wide identity, tone, or safety posture    | System prompt                  | `system-prompts.md`                                   |
| Bundling several of the above for distribution    | Plugins                        | `plugins.md`                                          |
| Deterministic logic on tool calls                 | Hooks                          | `../hooks.md`                                         |
| Structured access to an external service          | MCP                            | `../tools/mcp.md`                                     |

Rules of thumb:

- **ALWAYS start from the `claude_code` preset when the product is a coding agent a
  human watches and steers**; add `append` for product rules. Write a custom prompt
  only when the surface, identity, or permission model genuinely differs — you then
  own the tool guidance and safety instructions the preset was carrying.
- **NEVER put persistent rules in the first user prompt.** Compaction summarizes
  early history away. CLAUDE.md is re-injected on every request.
- **NEVER rely on default `query()` options for multi-tenant isolation.** Managed
  policy settings, `~/.claude.json`, auto-memory, and claude.ai connectors are read
  regardless of `settingSources` (`setting-sources.md`, `../production/secure-deployment.md`).
- Every feature you enable costs context. Scope subagent tool sets, and prefer
  on-demand skills over always-loaded CLAUDE.md text for large material.

<!-- BEGIN GENERATED INDEX -->

- [Plugins](./plugins.md) — bundling skills, agents, hooks, and MCP servers into one loadable unit; loading a plugin by local path; a plugin's skills or commands do not appear
- [settingSources and CLAUDE.md](./setting-sources.md) — loading CLAUDE.md, project skills, filesystem hooks, or settings.json; the agent picks up the developer's local configuration and should not; isolating an agent for CI, tests, or multi-tenant deployment; which directory the SDK reads project files from
- [Agent Skills](./skills.md) — giving the agent domain expertise it loads only when relevant; skills are not found or never invoked; enabling only some skills, or disabling all of them; registering a skill programmatically
- [Slash commands](./slash-commands.md) — sending /compact or /clear from the SDK; listing which commands a session supports; defining a custom command with frontmatter, arguments, or shell context
- [Subagents](./subagents.md) — delegating an isolated subtask to keep the main context small; running several analyses in parallel; giving one part of the work a different model, prompt, or tool set; Claude never delegates to a defined subagent; resuming a subagent to ask a follow-up
- [System prompts](./system-prompts.md) — the agent lost Claude Code's coding conventions or tone; adding product-specific instructions without losing built-in behavior; building a non-coding agent with its own identity; prompt cache misses across machines or working directories; a long custom prompt fails at process spawn in Python

<!-- END GENERATED INDEX -->
