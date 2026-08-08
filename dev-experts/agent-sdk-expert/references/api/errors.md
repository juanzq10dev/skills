---
title: Error types (Python)
triggers:
  - "writing except clauses around an SDK call"
  - "catching a turn-limit or budget failure"
  - "distinguishing a process crash from an error result"
---

# Error types (Python)

Docs: https://code.claude.com/docs/en/agent-sdk/python#error-types

```python
class ClaudeSDKError(Exception): ...              # base
class CLIConnectionError(ClaudeSDKError): ...     # failed to connect
class CLINotFoundError(CLIConnectionError):       # .cli_path
    def __init__(self, message="Claude Code not found", cli_path=None): ...
class ProcessError(ClaudeSDKError):               # .exit_code, .stderr
    def __init__(self, message, exit_code=None, stderr=None): ...
class CLIJSONDecodeError(ClaudeSDKError):         # .line, .original_error
    def __init__(self, line, original_error): ...
```

## The one that catches people

When a single-shot `query()` ends on an **error result** (`error_max_turns`,
`error_max_budget_usd`, …), the SDK yields the result message and then raises a
**plain `Exception`**, not a `ClaudeSDKError` subclass. So `except ClaudeSDKError`
will not catch a turn-limit failure — match `Exception`:

```python
try:
    async for message in query(prompt="…", options=ClaudeAgentOptions(max_turns=5)):
        if isinstance(message, ResultMessage):
            session_id = message.session_id      # captured before the raise
except Exception as error:
    print(f"Session ended with an error: {error}")
```

The underlying Claude Code process also exits nonzero. A streaming-input session
stays alive instead of raising, and you can keep sending messages.

Because the raise happens **after** the result message is yielded, anything you
captured inside the loop (session id, checkpoint id, partial results) is still
available in the `except` block. Connection or process failures yield no result
message at all, so those values stay unset.

TypeScript throws rather than raising typed classes here; the same
yield-then-throw ordering applies. Error-message-keyed diagnoses:
`../troubleshooting.md`.
