---
title: V2 session API (removed)
triggers:
  - "code calls unstable_v2_createSession, unstable_v2_prompt, or unstable_v2_resumeSession"
  - "createSession() with send/stream is undefined"
---

# V2 session API (removed)

Docs: https://code.claude.com/docs/en/agent-sdk/typescript-v2-preview

The experimental TypeScript V2 session API — `unstable_v2_createSession()`,
`unstable_v2_resumeSession()`, `unstable_v2_prompt()`, and the `SDKSession`
`send()`/`stream()`/`close()` shape — was **removed in TypeScript Agent SDK
0.3.142**. It only exists on `@anthropic-ai/claude-agent-sdk@0.2`.

Port it to `query()`: a one-shot `unstable_v2_prompt` becomes a `query()` loop
reading the result message; `createSession` + repeated `send`/`stream` becomes
either `continue: true` per call or a single `query()` fed by an async generator;
`resumeSession(id)` becomes `options: { resume: sessionId }`. See
`../sessions/INDEX.md` and `../streaming-input.md`. The upstream page has
side-by-side before/after for each pattern.
