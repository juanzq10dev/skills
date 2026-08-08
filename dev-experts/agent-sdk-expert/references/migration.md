---
title: Migrate from the Claude Code SDK
triggers:
  - "code imports claude_code_sdk or @anthropic-ai/claude-code"
  - "ClaudeCodeOptions is undefined or not exported"
  - "the agent stopped following Claude Code's coding conventions after upgrading"
---

# Migrate from the Claude Code SDK

Docs: https://code.claude.com/docs/en/agent-sdk/migration-guide

The Claude Code SDK was renamed to the Claude Agent SDK at v0.1.0.

|                     | Old                         | New                              |
| ------------------- | --------------------------- | -------------------------------- |
| TypeScript package  | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| Python package      | `claude-code-sdk`           | `claude-agent-sdk`               |
| Python import       | `claude_code_sdk`           | `claude_agent_sdk`               |
| Python options type | `ClaudeCodeOptions`         | `ClaudeAgentOptions`             |

```bash
npm uninstall @anthropic-ai/claude-code && npm install @anthropic-ai/claude-agent-sdk
pip uninstall -y claude-code-sdk && pip install claude-agent-sdk
```

## Breaking change: the system prompt is no longer Claude Code's by default

v0.0.x used Claude Code's full system prompt. v0.1.0+ uses a **minimal** prompt that
covers tool calling only. To restore the old behavior, ask for the preset:

```python
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"}
)
```

```typescript
const options = { systemPrompt: { type: "preset", preset: "claude_code" } };
```

See `config/system-prompts.md` for when the preset is the right starting point.

## Not a breaking change: `settingSources`

v0.1.0 briefly defaulted to loading no filesystem settings; that was reverted. Today
omitting `settingSources` loads user, project, and local settings — matching the
CLI. Pass `[]` to isolate. Python ≤ 0.1.59 treated `setting_sources=[]` the same as
omitting it, so upgrade before relying on it. Details: `config/setting-sources.md`.
