---
title: Errors by message
triggers:
  - "an exact SDK error string needs diagnosing"
  - "CLINotFoundError, or Claude Code not found at a path"
  - "Refusing to execute batch script on Windows"
  - "the run says success but structured_output is missing"
---

# Errors by message

Docs: https://code.claude.com/docs/en/agent-sdk/troubleshooting

## `CLINotFoundError: Claude Code not found`

The Python SDK launches the `claude` CLI as a subprocess and couldn't find it.
Install Claude Code; if you set `cli_path`, confirm that file exists and is the
executable. When relying on `PATH`, check `claude --version` works **in the same
environment the app runs in** — IDE- and service-manager-launched processes often
have a different `PATH`.

## `CLIConnectionError: Refusing to execute batch script`

Windows-only, deliberate hardening: the resolved CLI path is a `.bat`/`.cmd` (such
as npm's `claude.cmd` shim), which Windows runs through `cmd.exe`, where argument
values can inject commands. Fix by giving the SDK a native executable:

```powershell
irm https://claude.ai/install.ps1 | iex     # native install
```

or point `ClaudeAgentOptions(cli_path=...)` at a `claude.exe`, or install the
`claude-agent-sdk` wheel on x64 Windows (it bundles `claude.exe`). Setting
`cli_path` **skips discovery**, so a native install alone won't take effect while
it's set. Before `claude-agent-sdk` 0.2.124 this check did not exist.

## `structured_output` is `None` but the result says `success`

The run completed without producing validated output — for example, an unsatisfiable
schema (conflicting length constraints) ends with no validation error and no output.
Treat it as a failure: check **both** that `subtype == "success"` **and** that
`structured_output` is present. If it recurs on a schema you believe is correct,
verify the schema is satisfiable, simplify it, then reintroduce constraints one at a
time. See `structured-outputs.md`.

## Elsewhere

Other symptoms are diagnosed next to the feature that causes them: MCP server
`failed`/`needs-auth` status and connection timeouts in `tools/mcp.md`, hooks not
firing in `hooks.md`, subagents not being delegated to in `config/subagents.md`,
skills not discovered in `config/skills.md`, checkpoint errors in
`sessions/checkpointing.md`.

Unlisted errors: file an issue on `anthropics/claude-agent-sdk-typescript` or
`anthropics/claude-agent-sdk-python` with the full error text and SDK version.
