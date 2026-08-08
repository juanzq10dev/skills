---
title: Sessions
triggers:
  - "sending a follow-up prompt that needs earlier context"
  - "recovering from a turn or budget limit"
  - "branching to try an alternative approach"
  - "resuming after a process restart, or on another host"
  - "stopping the SDK writing transcripts to disk"
type: index
---

# Sessions

Docs: https://code.claude.com/docs/en/agent-sdk/sessions

A session is the conversation transcript the SDK writes to disk automatically.
Returning to one restores the files the agent read, the analysis it did, and the
decisions it made. **Sessions persist the conversation, not the filesystem** — to
revert file changes use `checkpointing.md`.

## Which mechanism

Use the **first** that applies:

1. **One prompt, no follow-up** → nothing. A single `query()` already takes as many
   turns as it needs, and permission prompts and `AskUserQuestion` are handled
   in-loop without ending the call.
2. **Multi-turn in one process** → `ClaudeSDKClient` (Python) or `continue: true`
   (TypeScript). No ID handling.
3. **Picking up after a process restart, one conversation at a time** →
   `continue: true` / `continue_conversation=True`; it finds the most recent session
   in the directory.
4. **A specific past session, or many sessions (one per user)** → capture
   `session_id` and pass `resume`.
5. **Trying an alternative without losing the original** → `resume` +
   `forkSession` / `fork_session`.
6. **Another host, container, or serverless** → a `SessionStore` adapter
   (`storage.md`). Do not ship transcript files around by hand.
7. **Nothing may touch disk** → `persistSession: false` (TypeScript only), or
   `CLAUDE_CODE_SKIP_PROMPT_HISTORY` in `env` for Python.

```typescript
let sessionId: string | undefined;
for await (const message of query({ prompt: "Analyze the auth module" })) {
  if (message.type === "result") sessionId = message.session_id;
}
// later
query({ prompt: "Now implement it", options: { resume: sessionId } });
// or branch, leaving the original untouched
query({
  prompt: "Try OAuth2 instead",
  options: { resume: sessionId, forkSession: true },
});
```

```python
options = ClaudeAgentOptions(resume=session_id, fork_session=True)
```

Read the ID from `ResultMessage.session_id` — present on **every** result, success or
error. TypeScript also exposes it on the init `SystemMessage`; Python nests it in
`SystemMessage.data`.

## Rules

- **NEVER resume without catching the error a limit produces.** A single-shot
  `query()` raises after yielding an `error_max_turns` / `error_max_budget_usd`
  result, and resuming with a higher limit is exactly the recovery — but only if the
  ID was captured before the raise (`../api/errors.md`).
- **NEVER treat a fork as a filesystem branch.** A forked agent's edits are real and
  visible to any session in the same directory.
- Transcripts live at `~/.claude/projects/<encoded-cwd>/*.jsonl` (or under
  `CLAUDE_CONFIG_DIR`), where `<encoded-cwd>` is the absolute path with every
  non-alphanumeric character replaced by `-`. Same machine only.

Both SDKs expose `listSessions()` / `list_sessions()`,
`getSessionMessages()` / `get_session_messages()`, `getSessionInfo()`,
`renameSession()`, and `tagSession()` for pickers, cleanup, and transcript viewers.

<!-- BEGIN GENERATED INDEX -->

- [File checkpointing and rewind](./checkpointing.md) — undoing file changes the agent made; a restore point before a risky refactor; user messages have no uuid, or no checkpoint was found; ProcessTransport is not ready for writing
- [SessionStore adapters](./storage.md) — resuming a session on a different host, container, or lambda; mirroring transcripts to S3, Redis, or Postgres; writing or testing a custom session store

<!-- END GENERATED INDEX -->
