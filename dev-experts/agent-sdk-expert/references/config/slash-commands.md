---
title: Slash commands
triggers:
  - "sending /compact or /clear from the SDK"
  - "listing which commands a session supports"
  - "defining a custom command with frontmatter, arguments, or shell context"
---

# Slash commands

Docs: https://code.claude.com/docs/en/agent-sdk/slash-commands

Commands are ordinary SDK inputs — send the command as the `prompt` string, not
through a special API.

```typescript
for await (const message of query({
  prompt: "/compact",
  options: { continue: true, maxTurns: 1 },
})) {
  if (message.type === "system" && message.subtype === "compact_boundary") {
    console.log(
      "Pre-compaction tokens:",
      message.compact_metadata.pre_tokens,
      "Trigger:",
      message.compact_metadata.trigger,
    );
  }
}
```

```python
async for message in query(prompt="/compact",
                           options=ClaudeAgentOptions(continue_conversation=True, max_turns=1)):
    if isinstance(message, SystemMessage) and message.subtype == "compact_boundary":
        print(message.data["compact_metadata"]["pre_tokens"])
```

`/compact` and `/clear` need existing history, so they belong on a `continue`d or
`resume`d call, not a fresh session.

Discover what a session supports from the init message: `message.slash_commands`
(TypeScript) / `message.data["slash_commands"]` (Python). The list includes built-ins
plus bundled skills plus your custom commands. TypeScript can also call
`Query.supportedCommands()`.

## Custom commands

Markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (user),
loaded through `settingSources` (`setting-sources.md`). Subdirectories namespace the
listing but the invocation stays flat (`frontend/component.md` → `/component`).

```markdown
---
allowed-tools: Bash(git add *), Bash(git status *), Bash(git commit *)
argument-hint: [issue-number] [priority]
description: Create a git commit
model: claude-opus-4-8
---

## Context

- Current status: !`git status`
- Current diff: !`git diff HEAD`

Fix issue #$0 with priority $1.
```

`$0`, `$1`, … are positional arguments; `$ARGUMENTS` is the whole string. A
`` !`cmd` `` line runs a shell command and injects its output; `@path` injects a
file's contents.

New skills are the preferred form for reusable workflows (`skills.md`); commands
remain for CLI-style invocations.
