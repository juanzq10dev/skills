---
title: System prompts
triggers:
  - "the agent lost Claude Code's coding conventions or tone"
  - "adding product-specific instructions without losing built-in behavior"
  - "building a non-coding agent with its own identity"
  - "prompt cache misses across machines or working directories"
  - "a long custom prompt fails at process spawn in Python"
---

# System prompts

Docs: https://code.claude.com/docs/en/agent-sdk/modifying-system-prompts

Three starting points. **The default is a minimal prompt** covering tool calling
only — unlike `claude -p`, which uses the full Claude Code prompt.

| You're building                                                           | Use                                              |
| ------------------------------------------------------------------------- | ------------------------------------------------ |
| A CLI/IDE-like coding tool where Claude Code's defaults are what you want | `claude_code` preset                             |
| The same, plus product rules (standards, format, domain context)          | preset + `append` — lowest risk, nothing removed |
| A different surface, identity, or permission model, or a non-coding agent | custom prompt string                             |
| A thin tool-calling loop with all behavior in the user prompt             | omit the option                                  |

```typescript
options: { systemPrompt: {
  type: "preset", preset: "claude_code",
  append: "Always include detailed docstrings and type hints in Python code."
}}
```

```python
options = ClaudeAgentOptions(system_prompt={
    "type": "preset", "preset": "claude_code",
    "append": "Always include detailed docstrings and type hints in Python code.",
})
```

"Different from Claude Code" means: output not read in a terminal by the person who
triggered it; the agent shouldn't present as Claude Code; it runs without a human
approving steps; or the work isn't coding (most of the preset is coding guidance,
which competes with your instructions).

Unattended coding automation — a CI job fixing lint or reviewing diffs — still fits
the preset.

## Prompt caching across users and machines

The preset embeds per-session context (cwd, git-repo flag, platform, shell, OS
version, auto-memory paths) **ahead of** your `append` text, so two sessions in
different directories can't share a cache entry. Set `excludeDynamicSections: true`
(Python: `"exclude_dynamic_sections": True`) to move that context into the first
user message, leaving an identical system prompt.

Tradeoff: the environment context still reaches Claude, but instructions in a user
message carry marginally less weight than in the system prompt. Requires TS
v0.2.98+ / Python v0.1.58+, and only applies to the preset object form.

## Other levers

**CLAUDE.md** does not change the system prompt at all — the SDK injects it into the
_conversation_ as project context, so it works with any prompt configuration. It
loads via setting sources (`setting-sources.md`).

**Output styles** are markdown files in `~/.claude/output-styles/` or
`.claude/output-styles/` that modify the system prompt and are reusable across CLI
and SDK. By default a custom style replaces the preset's software-engineering
instructions; `keep-coding-instructions: true` in the frontmatter layers instead.
Select one in TypeScript inside `settings` (`{ settings: { outputStyle: "Explanatory" } }`);
the guide states this is not a top-level option, though the `Options` type reference
also lists one — prefer the `settings` form. Python has no programmatic selector, so
use `append` or a custom string there.

## Common Anti-Patterns

- Expecting Claude Code behavior by default → v0.1.0 removed it (`../migration.md`).
- A long `system_prompt` string in Python → it is passed as one CLI argument and can
  exceed the OS limit (`Argument list too long`). Use
  `system_prompt={"type": "file", "path": "..."}`.
- `excludeDynamicSections` with a plain string prompt → no effect; preset form only.
- Expecting CLAUDE.md to load with `settingSources: []` → it doesn't.
