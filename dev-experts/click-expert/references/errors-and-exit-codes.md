---
title: Errors, exceptions and exit codes
triggers:
  - "reporting a user-facing error from a command without a traceback"
  - "choosing or explaining the exit code a CLI returns"
  - "aborting a command from inside a parameter callback"
  - "wrapping a Click command so exceptions propagate instead of exiting"
---

# Errors and exit codes

Docs: https://click.palletsprojects.com/en/stable/exceptions/ and
https://click.palletsprojects.com/en/stable/command-line-reference/

## Exit codes

| Code | Meaning                                                                                 |
| ---- | --------------------------------------------------------------------------------------- |
| `0`  | success, and also an explicitly requested `--help`                                      |
| `1`  | `Abort` (including `EOFError` / `KeyboardInterrupt`), or an uncaught exception          |
| `2`  | usage error — bad parameter, unknown option, or help shown because of `no_args_is_help` |

Since 8.2, help shown because `no_args_is_help` fired exits `2`, not `0`. `no_args_is_help`
defaults to `True` on `Group` and `False` on `Command`; set `no_args_is_help=False` on a
group to get a plain usage error instead of the help page.

## Raising errors

```python
import click


@click.command()
@click.option("--port", type=int)
def serve(port: int) -> None:
    if port is not None and port < 1024:
        raise click.BadParameter("must be >= 1024", param_hint="--port")
```

| Exception                                              | Use for                                                         | Exit code |
| ------------------------------------------------------ | --------------------------------------------------------------- | --------- |
| `ClickException`                                       | any message Click should print to stderr and exit on            | `1`       |
| `UsageError`                                           | the user invoked the command wrongly; prints usage              | `2`       |
| `BadParameter`                                         | a specific parameter is invalid; auto-annotated with its name   | `2`       |
| `MissingParameter`                                     | a required parameter was not supplied                           | `2`       |
| `NoSuchOption` / `BadOptionUsage` / `BadArgumentUsage` | parser-level problems                                           | `2`       |
| `NoSuchCommand`                                        | unknown subcommand; carries "did you mean" suggestions (8.4.0+) | `2`       |
| `FileError`                                            | `click.File` could not open the file                            | `1`       |
| `Abort`                                                | stop now, print `Aborted!`                                      | `1`       |

Every `ClickException` has `exit_code` and a `show(file=None)` method.

## From a context

```python
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.fail("cannot continue")   # UsageError, exit 2
    ctx.abort()                   # Abort, exit 1
    ctx.exit(0)                   # exit with a chosen code
```

Inside a custom `ParamType.convert`, call `self.fail(msg, param, ctx)` rather than raising
(`parameters/types/custom-types.md`).

## Disabling Click's error handling

`Command.main` is what catches `ClickException`, prints, and calls `sys.exit`. Turn it off
to embed a command in a larger program:

```python
result = cli.main(["sync", "--force"], standalone_mode=False)
```

With `standalone_mode=False`, exceptions propagate and the callback's return value is
returned instead of discarded. For full manual control see `commands/invoking.md`.

## Common Anti-Patterns

- `print("error: ..."); sys.exit(1)` → `raise click.ClickException("...")`; it writes to
  stderr and sets the exit code for you.
- `raise SystemExit(2)` for a bad value → `raise click.BadParameter(...)`, which prints the
  usage line and the parameter name.
- Catching `Abort` to keep going → `Abort` exists precisely to stop; catch the underlying
  `KeyboardInterrupt` instead if that is really the intent.
- Asserting `exit_code == 0` in a test after triggering `--help` on a group with no args →
  it is `2`.
