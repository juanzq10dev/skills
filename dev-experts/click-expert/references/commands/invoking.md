---
title: Invoking commands programmatically
triggers:
  - "calling one Click command from inside another"
  - "running a Click CLI from Python without letting it call sys.exit"
  - "using a command's return value"
  - "combining commands from two independent CLIs into one program"
---

# Invoking commands programmatically

Docs: https://click.palletsprojects.com/en/stable/advanced/ and
https://click.palletsprojects.com/en/stable/exceptions/

Calling a decorated function directly does **not** call your code — it parses `sys.argv`
and exits. Use one of the forms below.

## From another command

```python
cli = click.Group()


@cli.command()
@click.option("--count", default=1)
def test(count: int) -> None:
    click.echo(f"Count: {count}")


@cli.command()
@click.option("--count", default=1)
@click.pass_context
def dist(ctx: click.Context, count: int) -> None:
    ctx.forward(test)            # reuse this command's matching parameters
    ctx.invoke(test, count=42)   # supply them explicitly
```

`ctx.invoke` passes what you give it; `ctx.forward` fills from the current command's
params first. Both handle `pass_context` correctly and bubble the return value.

This is discouraged as an architecture: extract the shared work into a plain function and
have both commands call it. Reach for `invoke`/`forward` when the other command is not
yours to refactor.

## From plain Python

```python
result = cli.main(["sync", "--force"], standalone_mode=False)
```

`standalone_mode=False` disables Click's exception handling and the implicit `sys.exit`,
and returns the callback's value. For total control, build the context yourself:

```python
ctx = command.make_context("command-name", ["args", "go", "here"])
with ctx:
    result = command.invoke(ctx)
```

Nothing is caught in that form — `ClickException` propagates as an ordinary exception.

In tests, prefer `CliRunner` over both (`../testing.md`).

## Return values

- A command's return value comes back from `Command.invoke`.
- A group returns its subcommand's value — unless it ran with `invoke_without_command` and
  no subcommand, in which case it returns the group callback's value.
- A chained group returns the list of all subcommand values, which is what
  `result_callback` receives (`chaining.md`).
- `Command.main` **discards** the return value unless `standalone_mode=False`.

Click never interprets return values itself.

## `CommandCollection`

Merge several independent groups into one CLI — the pattern for a framework that absorbs
another tool's commands:

```python
cli = click.CommandCollection(sources=[web_cli, worker_cli])
```

Later sources fill in names the earlier ones do not define.

## Common Anti-Patterns

- `hello()` inside library code to "run the command" → it parses `sys.argv` and exits.
- `subprocess.run(["mycli", ...])` from a sibling command → `ctx.invoke`, or the shared
  function.
- `ctx.invoke(test)` expecting the caller's `--count` to carry over → that is
  `ctx.forward`.
- `try: cli() except SystemExit:` → pass `standalone_mode=False`.
