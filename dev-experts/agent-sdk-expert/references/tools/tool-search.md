---
title: Tool search
triggers:
  - "dozens or hundreds of tools, and tool selection is degrading"
  - "tool definitions consuming too much of the context window"
  - "an extra ToolSearch call appears before the agent uses a tool"
  - "turning tool deferral off for a small tool set"
---

# Tool search

Docs: https://code.claude.com/docs/en/agent-sdk/tool-search

**On by default.** Tool definitions are withheld from context; Claude gets a summary
and searches when it needs a capability, loading up to five relevant tools that then
stay available. Applies to every registered tool — remote MCP and in-process SDK
servers alike.

It fixes two problems that appear as tool sets grow: 50 tools can consume 10–20K
tokens, and selection accuracy degrades past 30–50 loaded tools. It costs one extra
round trip the first time a tool is discovered, so **below ~10 tools, loading
everything upfront is faster** — turn it off there.

Configure through the `ENABLE_TOOL_SEARCH` environment variable in `env`:

```typescript
options: {
  mcpServers: { "enterprise-tools": { type: "http", url: "https://tools.example.com/mcp" } },
  allowedTools: ["mcp__enterprise-tools__*"],
  env: { ...process.env, ENABLE_TOOL_SEARCH: "auto:5" }   // TS: env replaces, so spread
}
```

```python
options = ClaudeAgentOptions(
    allowed_tools=["mcp__enterprise-tools__*"],
    env={"ENABLE_TOOL_SEARCH": "auto:5"},                 # Python: env merges
)
```

| Value    | Behavior                                                  |
| -------- | --------------------------------------------------------- |
| unset    | On, with the fallbacks below                              |
| `true`   | Always on (sends the beta header through proxies)         |
| `auto`   | On when tool definitions exceed 10% of the context window |
| `auto:N` | Same with a custom percentage; `auto:5` activates sooner  |
| `false`  | Off; all definitions load every turn                      |

## When it silently falls back to upfront loading

`ENABLE_TOOL_SEARCH` cannot override any of these:

- Models on the SDK's unsupported list (needs Sonnet 4.5, Haiku 4.5, Opus 4.5 or later).
- Google Cloud's Agent Platform on models earlier than the Claude 4.5 generation —
  their serving stacks reject the required beta header.
- Microsoft Foundry deployments hosted on Azure, which reject it server-side.
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, which strips the beta header entirely.

It is also disabled by default when `ANTHROPIC_BASE_URL` points at a non-first-party
host, since most proxies don't forward `tool_reference` blocks — `true` overrides
that, and requests fail on proxies that can't handle them.

## Make tools discoverable

Search matches names and descriptions. `search_slack_messages` surfaces for more
requests than `query_slack`; "Search Slack messages by keyword, channel, or date
range" beats "Query Slack". You can also list tool categories via the system prompt:

```python
system_prompt={"type": "preset", "preset": "claude_code",
               "append": "You can search for tools to interact with Slack, GitHub, and Jira."}
```

Limits: 10,000 tools per catalog, five results per search. In TypeScript,
`alwaysLoad: true` in `tool()`'s extras or `createSdkMcpServer()`'s options keeps a
tool's full schema in the initial prompt.
