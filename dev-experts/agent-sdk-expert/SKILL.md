---
name: agent-sdk-expert
description: >
  Expert guidance for working with the Claude Agent SDK (TypeScript
  @anthropic-ai/claude-agent-sdk 0.3.x, Python claude-agent-sdk 0.2.x) — Claude Code
  packaged as a library. ALWAYS use before doing any task that requires knowledge
  specific to the Agent SDK, or that references query(), ClaudeSDKClient,
  ClaudeAgentOptions, allowedTools, permissionMode, canUseTool, settingSources,
  hooks, subagents, sdk mcp servers, or ResultMessage. Common tasks may include
  building or debugging an agent, choosing a permission mode, pre-approving or
  blocking tools, defining custom tools, connecting MCP servers, writing PreToolUse
  hooks, defining subagents, resuming or forking a session, getting structured JSON
  output, streaming partial messages, tracking cost, hosting the SDK in a container,
  or migrating from claude-code-sdk.
---

# Claude Agent SDK

Version: TypeScript `@anthropic-ai/claude-agent-sdk` **0.3.224**, Python
`claude-agent-sdk` **0.2.132**. Docs fetched 2026-08-07. Both packages bundle a
native Claude Code binary and drive it as a subprocess.

## Core Agent SDK Concepts

- **Agent loop** — Claude evaluates, calls tools, reads results, repeats until it
  answers with no tool calls. The SDK runs it for you. See `references/agent-loop.md`.
- **Turn** — one round trip inside that loop (assistant output with tool calls →
  tools execute → results feed back). Capped by `maxTurns` / `maxBudgetUsd`.
- **`query()`** — the entry point. Returns an async iterator of messages.
- **Options** — `Options` (TS) / `ClaudeAgentOptions` (Python): the whole
  configuration surface. Field map: `references/api/options.md`.
- **Session** — the persisted conversation transcript, resumable and forkable.

## Not the same as the Claude API SDK

The Agent SDK (`claude-agent-sdk`) ships the Claude Code harness: built-in tools,
the agent loop, context management, hooks, subagents, permissions, sessions. The
Anthropic API SDK (`anthropic` / `@anthropic-ai/sdk`) and its Tool Runner are a
different package where you supply every tool; Managed Agents is a hosted REST
product. Do not substitute one for another.

## Primary workflow

Building any agent starts at `references/quickstart.md` (install, auth, first
`query()`), then `references/agent-loop.md` for what the loop yields and how to
bound it. Before granting an agent any capability, read `references/tools/INDEX.md`.

## Packages and languages

```bash
npm install @anthropic-ai/claude-agent-sdk     # TypeScript / JavaScript
pip install claude-agent-sdk                   # Python 3.10+
```

Node 18+ or Python 3.10+. Auth is `ANTHROPIC_API_KEY` in the process environment —
the SDK does **not** read `.env` files. The SDK is Python and TypeScript only; from
any other language run the CLI as a subprocess with `-p --output-format json`.

## CRITICAL: Always Read Reference Files Before Answering

NEVER answer from memory or guess at SDK functions, option names, message fields, or
event names. Option names differ by language (`allowedTools` vs `allowed_tools`) and
several fields keep camelCase in Python; guesses are wrong more often than right.
ALWAYS read the relevant reference file(s) from the Reference Index below before
responding. For every question, identify which reference file(s) are relevant using
the index descriptions, read them, then answer based on what you read.

Prefer the SDK's own introspection over guessing: the `system`/`init` message lists
the session's real `tools`, `slash_commands`, `skills`, `plugins`, and
`mcp_servers`, and `Query.supportedCommands()` / `supportedModels()` /
`mcpServerStatus()` report live state. Do not explore the user's project when the
init message or a reference file already answers the question.

## Reference Index

<!-- BEGIN GENERATED INDEX -->

- [The agent loop, turns, and results](./references/agent-loop.md) — deciding which messages to handle in the stream; the agent runs too long, too expensive, or never stops; checking whether a run succeeded, and reading cost or session id off the result; query() threw after the loop finished; context window filling up, compaction, or losing early instructions; choosing an effort level
- [Hooks](./references/hooks.md) — running custom code before or after a tool call; blocking a dangerous command, or auditing every tool use; rewriting a tool's arguments before it executes; a hook never fires, or its matcher matches nothing; archiving the transcript before compaction; tracking subagent start/stop; a check must run on every tool call regardless of permission mode
- [Migrate from the Claude Code SDK](./references/migration.md) — code imports claude_code_sdk or @anthropic-ai/claude-code; ClaudeCodeOptions is undefined or not exported; the agent stopped following Claude Code's coding conventions after upgrading
- [Install and run a first agent](./references/quickstart.md) — setting up the Agent SDK in a new or existing project; API key not found, auth fails, or the key is in a .env file; no bundled Claude Code binary, CLINotFoundError on install; pointing the SDK at Bedrock, Vertex, Foundry, or Claude Platform on AWS
- [Streaming input vs single message](./references/streaming-input.md) — sending more than one prompt, or attaching an image; interrupting the agent mid-task, or queueing messages; canUseTool never fires in Python; choosing between a one-shot query and a live session
- [Stream partial responses](./references/streaming-output.md) — showing text token-by-token in a UI as the agent works; rendering a spinner or status while a tool runs; watching a tool's input JSON assemble incrementally
- [Structured JSON output](./references/structured-outputs.md) — the agent's answer must be validated JSON, not prose; using Zod or Pydantic to type an agent's final result; error_max_structured_output_retries, or the schema was ignored
- [Todo and task progress](./references/todo-tracking.md) — rendering the agent's task list or a progress bar; TodoWrite tool_use blocks never appear in the stream; migrating a TodoWrite watcher to TaskCreate / TaskUpdate
- [Errors by message](./references/troubleshooting.md) — an exact SDK error string needs diagnosing; CLINotFoundError, or Claude Code not found at a path; Refusing to execute batch script on Windows; the run says success but structured_output is missing
- [Approval prompts and clarifying questions](./references/user-input.md) — surfacing a tool request to a human for approval; implementing an allow / deny / always-allow prompt; handling AskUserQuestion, or the agent asking a multiple-choice question; rewriting a tool's arguments at approval time
- [API reference](./references/api/INDEX.md) — looking up an exact function, option, message field, or method name; choosing between query(), ClaudeSDKClient, and startup(); translating an option name between TypeScript and Python; catching SDK errors
- [Behavior and project configuration](./references/config/INDEX.md) — shaping how the agent behaves beyond the prompt; choosing between CLAUDE.md, a system prompt, a skill, and a subagent; the agent ignores project conventions; isolating an agent from the developer's local configuration
- [Running in production](./references/production/INDEX.md) — deploying an agent to a container, Kubernetes, or serverless; isolating tenants or untrusted code; monitoring, tracing, or budgeting a fleet of agents; sizing hosts for concurrent agents
- [Sessions](./references/sessions/INDEX.md) — sending a follow-up prompt that needs earlier context; recovering from a turn or budget limit; branching to try an alternative approach; resuming after a process restart, or on another host; stopping the SDK writing transcripts to disk
- [Tools and permissions](./references/tools/INDEX.md) — deciding how to give an agent a new capability; the agent can see a tool but never calls it; locking down what an agent is allowed to do; tool definitions are eating the context window

<!-- END GENERATED INDEX -->
