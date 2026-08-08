---
title: Hosting and scaling
triggers:
  - "packaging an agent into a container or serverless function"
  - "choosing between ephemeral and long-running sessions"
  - "how many agents fit on a host"
  - "isolating tenants from each other"
  - "a session runs forever, or memory grows over a long run"
---

# Hosting and scaling

Docs: https://code.claude.com/docs/en/agent-sdk/hosting

The SDK spawns the Claude Code CLI as a subprocess. Three kinds of state live on
local disk:

| State                       | Default location                                                        |
| --------------------------- | ----------------------------------------------------------------------- |
| Session transcripts         | `~/.claude/projects/`, or `projects/` under `CLAUDE_CONFIG_DIR`         |
| `CLAUDE.md` memory          | `~/.claude/CLAUDE.md` (user tier), the working directory (project tier) |
| Working-directory artifacts | The session's `cwd`                                                     |

Give each session its own working directory:

```typescript
query({ prompt, options: { cwd: "/work/session-a" } });
```

```python
query(prompt=prompt, options=ClaudeAgentOptions(cwd="/work/session-a"))
```

## Session patterns

- **Ephemeral** — one container per task, no persistence. Bound it with `maxTurns`.
- **Long-running** — a container that survives across turns.
- **Hybrid** — stateless hosts plus a `SessionStore`, so any host can resume:

```typescript
for await (const message of query({
  prompt: userInput,
  options: { resume: sessionId, sessionStore }, // S3, Redis, Postgres, or your own
})) {
  /* … */
}
```

See `../sessions/storage.md` for the adapter interface.

## Multi-tenant isolation

```python
options = ClaudeAgentOptions(
    cwd=tenant_dir,
    setting_sources=[],
    env={"CLAUDE_CONFIG_DIR": config_dir, "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"},
)
```

```typescript
options: { cwd: tenantDir, settingSources: [],
           env: { ...process.env, CLAUDE_CONFIG_DIR: configDir,
                  CLAUDE_CODE_DISABLE_AUTO_MEMORY: "1" } }
```

`settingSources: []` alone is not enough — several inputs bypass it entirely
(`../config/setting-sources.md`). Server-managed settings are fetched whenever the
process authenticates with an organization credential, and filesystem isolation does
not remove them.

## Known limitations

| Limitation                                     | What to do                                                                                                                                                  |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| No top-level session timeout                   | Bound with `maxTurns`; a session never stops on its own                                                                                                     |
| Memory growth over long sessions               | Cap session length or recycle subprocesses periodically                                                                                                     |
| Wide parallel-subagent fanouts hit rate limits | Batch the work instead of one wide dispatch                                                                                                                 |
| No per-subagent wall-clock deadline            | `maxTurns` in each `AgentDefinition`. For background subagents, `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` is a **stall** watchdog, not a total-runtime deadline |

Capacity planning:
`agents per host = (host RAM - overhead) / (per-session RAM ceiling)`.
