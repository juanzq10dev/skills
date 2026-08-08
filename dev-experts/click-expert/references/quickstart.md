---
title: Quickstart — first command
triggers:
  - "starting a new Python CLI from scratch and needing the canonical skeleton"
  - "adding Click to an existing project for the first time"
  - "the command name on the command line is not the name that was expected"
  - "deciding between print() and click.echo()"
---

# Quickstart

Docs: https://click.palletsprojects.com/en/stable/quickstart/

```console
$ pip install click
```

## Canonical single command

```python
import click


@click.command()
@click.option("--count", default=1, show_default=True, help="Number of greetings.")
@click.argument("name")
def hello(count: int, name: str) -> None:
    """Greet NAME COUNT times."""
    for _ in range(count):
        click.echo(f"Hello {name}!")


if __name__ == "__main__":
    hello()
```

The docstring becomes `--help` text; the function parameter names must match the parameter
names Click derives from the decorators (see `parameters/INDEX.md`).

## Canonical group

```python
import click


@click.group()
def cli() -> None:
    """Manage the database."""


@cli.command()
def initdb() -> None:
    """Create the tables."""
    click.echo("Initialized the database")


@cli.command()
def dropdb() -> None:
    """Drop the tables."""
    click.echo("Dropped the database")
```

Use `@cli.command()` to declare and attach in one step. Use plain `@click.command()` plus
`cli.add_command(other)` when the subcommand lives in another module.

## Command name derivation

The command name is the function name with `_` → `-`, **and** with a trailing `_command`,
`_cmd`, `_group`, or `_grp` stripped (since 8.2). Pass a name explicitly when in doubt:

| Function                                       | Command name |
| ---------------------------------------------- | ------------ |
| `def sync_all()`                               | `sync-all`   |
| `def sync_cmd()`                               | `sync`       |
| `@click.command("say-hello")` on `def hello()` | `say-hello`  |

## Common Anti-Patterns

- `print("...")` → `click.echo("...")`. `echo` strips ANSI codes when not writing to a
  terminal, handles the Windows console, and never dies on a misconfigured locale.
- `python app.py` as the documented invocation → install an entry point
  (`packaging/entry-points.md`). Shell completion only works through an entry point.
- `import click; click.__version__` → deprecated in 8.2, removed in 9.1. Use
  `importlib.metadata.version("click")`, or prefer feature detection
  (`migration/multi-version-support.md`).
- Calling the group function directly in library code → it parses `sys.argv` and calls
  `sys.exit`. To invoke it programmatically see `commands/invoking.md`.
