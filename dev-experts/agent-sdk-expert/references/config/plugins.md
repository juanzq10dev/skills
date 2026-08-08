---
title: Plugins
triggers:
  - "bundling skills, agents, hooks, and MCP servers into one loadable unit"
  - "loading a plugin by local path"
  - "a plugin's skills or commands do not appear"
---

# Plugins

Docs: https://code.claude.com/docs/en/agent-sdk/plugins

A plugin packages skills, agents, hooks, and MCP servers in one directory, loaded by
**local path** (the SDK has no registry install).

```typescript
options: {
  plugins: [
    { type: "local", path: "./my-plugin" },
    { type: "local", path: "/absolute/path/to/another-plugin" },
  ];
}
```

```python
options = ClaudeAgentOptions(plugins=[{"type": "local", "path": "./my-plugin"}])
```

Verify from the init message — `plugins`, `skills`, and `slash_commands` (direct
fields in TypeScript, under `message.data` in Python). Plugin skills and commands are
**namespaced with the plugin name**: `my-plugin:greet`. Invoke one by that full name:

```python
async for message in query(prompt="/my-plugin:greet",
                           options=ClaudeAgentOptions(plugins=[{"type": "local", "path": "./my-plugin"}])):
    ...
```

Structure (components are auto-discovered; the manifest is optional):

```text
my-plugin/
├── .claude-plugin/plugin.json
├── skills/<name>/SKILL.md
├── agents/<name>.md
├── hooks/hooks.json
└── .mcp.json
```

`commands/` still works but is legacy — use `skills/`.

In ESM TypeScript, resolve a script-relative plugin path with
`fileURLToPath(new URL("./plugins/my-plugin", import.meta.url))`; `__dirname` does
not exist there.
