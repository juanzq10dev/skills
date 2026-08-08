---
title: Testing a Click app with CliRunner
triggers:
  - "writing tests for a command line application"
  - "asserting on the output or exit code of a CLI"
  - "feeding input to a prompt inside a test"
  - "output from a library or subprocess is missing from the captured result"
  - "result.stderr or result.output does not behave as it used to"
---

# Testing

Docs: https://click.palletsprojects.com/en/stable/testing/

`CliRunner` mutates global interpreter state. It is **not thread-safe** and is for tests
only.

```python
from click.testing import CliRunner

from myapp import cli


def test_sync() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "sync"])
    assert result.exit_code == 0
    assert "Syncing" in result.stdout
```

## `Result` attributes

| Attribute                | Meaning                                                         |
| ------------------------ | --------------------------------------------------------------- |
| `exit_code`              | `0` success, `1` uncaught exception or `Abort`, `2` usage error |
| `stdout` / `stderr`      | the two streams, independent, as `str`                          |
| `output`                 | both streams interleaved, as the user would see in a terminal   |
| `exception` / `exc_info` | the exception, when `catch_exceptions=True` (the default)       |
| `return_value`           | what the command callback returned                              |

Since 8.2 `stdout` and `stderr` are always separate and `stderr` never raises; `output`
is no longer an alias for `stdout`. There is no `mix_stderr` parameter.

## `invoke` keywords

```python
result = runner.invoke(
    cli,
    ["sync"],
    input="yes\n",            # stdin, for prompts
    env={"MYAPP_TOKEN": "x"}, # extra environment
    catch_exceptions=False,   # let exceptions propagate — best for debugging a failing test
    terminal_width=60,        # any extra kwarg is forwarded to the Context
)
```

Prompts echo the supplied input into the output stream, except when `hide_input=True`.

## Filesystem isolation

```python
def test_cat() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("hello.txt", "w") as f:
            f.write("Hello World!")
        result = runner.invoke(cat, ["hello.txt"])
        assert result.output == "Hello World!\n"
```

Passing a path (`isolated_filesystem(tmp_path)`) uses that directory and leaves cleanup to
the caller — the way to hand control to pytest's `tmp_path`.

## Capture modes (8.4.0+)

| `capture=`        | Captures                                                       | Use when          |
| ----------------- | -------------------------------------------------------------- | ----------------- |
| `"sys"` (default) | Python-level writes: `print`, `click.echo`, `sys.stdout.write` | almost always     |
| `"fd"`            | OS file descriptors 1 and 2 via `os.dup2`                      | output is missing |

Choose `"fd"` when output is produced by a stale `from sys import stdout` reference, by
`logging`/`structlog` holding the original stream, or by a C extension or subprocess
writing straight to fd 1.

```python
runner = CliRunner(capture="fd")
result = runner.invoke(cli)
assert "expected output" in result.stdout
```

`capture="fd"` is **not available on Windows**. In `"sys"` mode `sys.stdout.fileno()`
raises `io.UnsupportedOperation`.

## Common Anti-Patterns

- `assert result.output == ...` when only stdout matters → use `result.stdout`; `output`
  interleaves stderr.
- Assigning `sys.stdin = io.StringIO(...)` by hand → use `invoke(..., input=...)`; see
  `platform/unicode.md` for why a bare `StringIO` is unsupported.
- Debugging a failing test through `result.exception` → re-run with
  `catch_exceptions=False` and get the real traceback.
- Reaching for `capture="fd"` first → it is slower and Windows-incompatible; only switch
  when `"sys"` demonstrably loses output.
- Sharing one `CliRunner` across threads or parallel tests → it patches global state.
