---
title: Agent Skills
triggers:
  - "giving the agent domain expertise it loads only when relevant"
  - "skills are not found or never invoked"
  - "enabling only some skills, or disabling all of them"
  - "registering a skill programmatically"
---

# Agent Skills

Docs: https://code.claude.com/docs/en/agent-sdk/skills

Markdown files that load **on demand**: descriptions are in context from startup,
full content only when relevant. Unlike CLAUDE.md, which loads every session.

Skills are **filesystem artifacts only** — `.claude/skills/<name>/SKILL.md`. There is
no programmatic registration API. They are discovered through `settingSources`, then
filtered by the `skills` option.

```python
options = ClaudeAgentOptions(
    cwd=os.getcwd(),                          # .claude/skills/ here or in a parent
    setting_sources=["user", "project"],      # discovery
    skills="all",                             # or ["pdf", "docx"], or [] to disable
    allowed_tools=["Read", "Write", "Bash"],
)
```

```typescript
const options = {
  cwd: process.cwd(),
  settingSources: ["user", "project"],
  skills: "all",
  allowedTools: ["Read", "Write", "Bash"],
};
```

Omitting `skills` enables all discovered user and project skills with the Skill tool
available, matching the CLI. When `skills` **is** set, the SDK adds `Skill` to
`allowedTools` automatically — but if you also pass an explicit `tools` list, include
`"Skill"` there yourself or Claude cannot invoke any.

## Common Anti-Patterns

- `setting_sources=[]` with `skills="all"` → nothing is discovered, so nothing is
  enabled. Discovery and enablement are separate steps.
- Wrong `cwd` → skills load from `<cwd>` up to the repository root; point `cwd` at
  the directory containing `.claude/skills/`. Verify with
  `ls .claude/skills/*/SKILL.md` and `ls ~/.claude/skills/*/SKILL.md`.
- Passing an explicit `tools` list without `"Skill"` → skills load but are
  uninvocable.

Skills also arrive through plugins, namespaced as `plugin-name:skill-name`
(`plugins.md`), and can be preloaded into a subagent's context via
`AgentDefinition.skills` (`subagents.md`).
