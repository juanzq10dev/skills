---
title: MCP servers
triggers:
  - "connecting the agent to GitHub, Slack, a database, or another external service"
  - "choosing stdio vs http vs sse transport"
  - "passing an API key or bearer token to an MCP server"
  - "a server shows failed, pending, or needs-auth at init"
  - "MCP tools exist but Claude never calls them"
  - "MCP connection timeouts, or tool output exceeding the token limit"
---

# MCP servers

Docs: https://code.claude.com/docs/en/agent-sdk/mcp

Pick the transport from the server's docs: a **command to run** → stdio; a **URL** →
`http` (or `sse`); **your own code** → an in-process SDK server (`custom-tools.md`).

```typescript
for await (const message of query({
  prompt: "List the 3 most recent issues in anthropics/claude-code",
  options: {
    mcpServers: {
      github: {
        type: "http",
        url: "https://api.githubcopilot.com/mcp/",
        headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` },
      },
      filesystem: {
        command: "npx",
        args: [
          "-y",
          "@modelcontextprotocol/server-filesystem",
          "/Users/me/projects",
        ],
      },
    },
    allowedTools: ["mcp__github__list_issues", "mcp__filesystem__*"],
  },
})) {
  /* … */
}
```

```python
options = ClaudeAgentOptions(
    mcp_servers={"github": {"type": "http", "url": "https://api.githubcopilot.com/mcp/",
                            "headers": {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}}},
    allowed_tools=["mcp__github__*"],
)
```

Tools are named `mcp__<server>__<tool>`; wildcards work after a **literal** server
segment (`mcp__github__get_*`). A bare `allowedTools: ["*"]` or `["mcp__*"]` is
ignored with a startup warning and auto-approves nothing.

Credentials: `env` for stdio servers, `headers` for HTTP/SSE. The SDK runs **no
interactive OAuth flow** — complete it in your app and pass the access token in
`headers`; an unauthenticated server reports `needs-auth` and the run continues
without its tools.

## From a config file

A `.mcp.json` at the project root loads when the `project` setting source is enabled
(the default). `"streamable-http"` is accepted there as an alias for `"http"`; the
programmatic option accepts only `"http"`. `${VAR}` expands at runtime.

## Connection timing and status

The `system`/`init` message reports per-server `status`: `pending`, `connected`,
`failed`, `needs-auth`, `disabled`. **Do not treat `pending` as failure** — it means
either not-yet-connected (normal for settings-file servers, which don't get the
first-turn wait) or a cached tool list serving tools with a deferred connect. Check
for `failed` or `needs-auth`:

```typescript
if (message.type === "system" && message.subtype === "init") {
  const unavailable = message.mcp_servers.filter(
    (s) => s.status === "failed" || s.status === "needs-auth",
  );
  if (unavailable.length) console.warn("Unavailable MCP servers:", unavailable);
}
```

Servers that fail to connect do **not** throw. For later status use
`mcpServerStatus()` (TS) or `get_mcp_status()` (Python).

stdio servers and HTTP/SSE servers without a cached tool list delay the first turn
until they connect, capped by `MCP_TIMEOUT` (30s default). In-process SDK servers
never delay it. `alwaysLoad: true` on a server config makes its full schemas
available on the first turn, exempt from tool-search deferral.

## Common Anti-Patterns

- Reaching for `permissionMode` to enable MCP tools → `acceptEdits` does not
  auto-approve them at all. Use `allowedTools` (`INDEX.md`).
- Tool output over 25,000 tokens → the full output is written to a file and the
  result is replaced by an error naming the path, so the agent can read it in parts.
  Raise `MAX_MCP_OUTPUT_TOKENS` if that is wrong for your case.
- Slow-starting servers → raise `MCP_TIMEOUT` (milliseconds), pre-warm the server,
  or use a lighter one.
