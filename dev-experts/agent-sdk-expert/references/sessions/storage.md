---
title: SessionStore adapters
triggers:
  - "resuming a session on a different host, container, or lambda"
  - "mirroring transcripts to S3, Redis, or Postgres"
  - "writing or testing a custom session store"
---

# `SessionStore` adapters

Docs: https://code.claude.com/docs/en/agent-sdk/session-storage

Session files are local to the machine that wrote them. A `SessionStore` mirrors
transcripts to your own backend so any host can resume them.

```typescript
import { query, InMemorySessionStore } from "@anthropic-ai/claude-agent-sdk";

const store = new InMemorySessionStore();
for await (const message of query({
  prompt: "List the TS files under src/",
  options: { sessionStore: store },
})) {
  if (message.type === "result") sessionId = message.session_id;
}
// later, possibly on another host
query({
  prompt: "Summarize what those files do",
  options: { sessionStore: store, resume: sessionId },
});
```

```python
from claude_agent_sdk import InMemorySessionStore
options = ClaudeAgentOptions(session_store=InMemorySessionStore(), resume=session_id)
```

## The interface

`SessionKey` is `{ projectKey, sessionId, subpath? }` (Python: `project_key`,
`session_id`, `subpath`).

| Method                             | Required | Called when                                                                                          |
| ---------------------------------- | -------- | ---------------------------------------------------------------------------------------------------- |
| `append(key, entries)`             | yes      | After each batch of transcript entries is written locally                                            |
| `load(key)`                        | yes      | Before the subprocess spawns when `resume` is set; return `null` if unknown                          |
| `listSessions(projectKey)`         | no       | By `listSessions({sessionStore})` and by `continue: true` — **without it, `continue: true` throws**  |
| `listSessionSummaries(projectKey)` | no       | Reads metadata for all sessions in one call; maintain summaries inside `append`                      |
| `delete(key)`                      | no       | By `deleteSession()`. Deleting the main key must cascade to subkeys **and** remove the summary entry |
| `listSubkeys(key)`                 | no       | During resume, to discover subagent transcripts — without it only the main transcript is restored    |

Reference adapters live in the TypeScript SDK repo under
`examples/session-stores/` (S3, Redis, Postgres). Python ships a conformance
harness:

```python
from claude_agent_sdk.testing import run_session_store_conformance

@pytest.mark.anyio
async def test_my_store_conformance():
    await run_session_store_conformance(MyRedisStore)
```

## Behavior notes

Writes are **dual**: the Claude Code subprocess still writes to local disk first and
mirror writes are best-effort. If the local copy must be ephemeral, point
`CLAUDE_CONFIG_DIR` at a temp directory in `options.env`.

The alternative, often more robust than shipping transcripts around, is not to
resume at all: capture the results you need as application state and pass them into
a fresh session's prompt.
