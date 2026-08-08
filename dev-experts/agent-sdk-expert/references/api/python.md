---
title: Python SDK reference (upstream)
triggers:
  - "a Python symbol is not covered by the local files"
  - "the exact ClaudeAgentOptions dataclass definition"
  - "Transport, ToolsPreset, ThinkingConfig, or McpServerConfig shapes"
---

# Python SDK reference (upstream)

Docs: https://code.claude.com/docs/en/agent-sdk/python

The complete generated surface for `claude-agent-sdk`: the full
`ClaudeAgentOptions` dataclass, `ClaudeSDKClient` methods, `@tool` and
`create_sdk_mcp_server`, all message and content-block classes, error classes, the
hook input/output types, and per-tool input/output schemas. Fetch it when a symbol
is not in the local files.

Also on that page: `list_sessions()`, `get_session_messages()`, `get_session_info()`,
`rename_session()`, `tag_session()`, and the `query()` vs `ClaudeSDKClient`
comparison.
