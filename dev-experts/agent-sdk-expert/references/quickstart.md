---
title: Install and run a first agent
triggers:
  - "setting up the Agent SDK in a new or existing project"
  - "API key not found, auth fails, or the key is in a .env file"
  - "no bundled Claude Code binary, CLINotFoundError on install"
  - "pointing the SDK at Bedrock, Vertex, Foundry, or Claude Platform on AWS"
---

# Install and run a first agent

Docs: https://code.claude.com/docs/en/agent-sdk/quickstart

Node 18+ or Python 3.10+.

```bash
# TypeScript — top-level await needs "type": "module" (or name the file agent.mts)
npm install @anthropic-ai/claude-agent-sdk
npm install --save-dev tsx
npx tsx agent.ts

# Python
pip install claude-agent-sdk        # or: uv add claude-agent-sdk
python agent.py
```

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review utils.py for crash bugs and fix them.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],
    permissionMode: "acceptEdits",
  },
})) {
  if (message.type === "result") console.log(message.subtype, message.result);
}
```

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for crash bugs and fix them.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"], permission_mode="acceptEdits"
        ),
    ):
        if isinstance(message, ResultMessage):
            print(message.subtype, message.result)

asyncio.run(main())
```

## Authentication

`ANTHROPIC_API_KEY` must be in the environment of the process that runs the agent.
**The SDK does not load `.env` files** — load them yourself (e.g. `dotenv`) first.

Third-party providers are selected by environment variable, not by an option:
`CLAUDE_CODE_USE_BEDROCK=1`, `CLAUDE_CODE_USE_VERTEX=1`, `CLAUDE_CODE_USE_FOUNDRY=1`,
or `CLAUDE_CODE_USE_ANTHROPIC_AWS=1` + `ANTHROPIC_AWS_WORKSPACE_ID`, each with that
cloud's own credentials configured.

## Common Anti-Patterns

- claude.ai login for a third-party product → **not permitted** without prior
  Anthropic approval; use API-key auth.
- Assuming the binary is always bundled → a pip **source** install (e.g. ARM64
  Windows) and `npm ci --omit=optional` both ship no binary. Install Claude Code
  natively, or set `pathToClaudeCodeExecutable` / `cli_path`.
- Top-level `await` in a CommonJS TS project → name the file `agent.mts`.

Next: `../agent-loop.md` for what the loop yields; `../tools/INDEX.md` before
granting capabilities.
