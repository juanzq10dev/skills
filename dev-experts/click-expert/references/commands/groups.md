---
title: Groups and nesting
triggers:
  - "adding subcommands to a CLI"
  - "nesting subcommands more than one level deep"
  - "splitting commands across several Python modules"
  - "a group should do something when invoked without a subcommand"
  - "renaming a command or marking it deprecated"
---

# Groups

Docs: https://click.palletsprojects.com/en/stable/commands-and-groups/

```python
import click


@click.group()
def cli() -> None:
    """Top-level tool."""


@cli.group()
def session() -> None:
    """Session management."""
    click.echo("Starting session")


@session.command()
def initdb() -> None:
    click.echo("Initialized the database")
```

Invoked as `cli session initdb`. Nesting is unlimited; every level must be named on the
command line. Use `@cli.group()` (not `@click.group()`) so the subgroup is registered.

## Attaching later

```python
# commands/sync.py
@click.command()
def sync() -> None: ...


# cli.py
from commands.sync import sync

cli.add_command(sync)
cli.add_command(sync, name="synchronise")   # register under a different name
```

This is the way to split a CLI across modules. Registration order does not change behavior;
the help listing is sorted.

## Group keywords

`Group(name=None, commands=None, invoke_without_command=False, no_args_is_help=None,
subcommand_metavar=None, chain=False, result_callback=None, **command_kwargs)`

| Keyword                       | Effect                                                      |
| ----------------------------- | ----------------------------------------------------------- |
| `invoke_without_command=True` | run the group callback even with no subcommand              |
| `no_args_is_help=False`       | a bare invocation is a usage error instead of the help page |
| `chain=True`                  | allow several subcommands in one invocation (`chaining.md`) |
| `cls=`                        | use a `Group` subclass (`custom-classes.md`)                |

```python
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        click.echo("I was invoked without subcommand")
    else:
        click.echo(f"I am about to invoke {ctx.invoked_subcommand}")
```

`ctx.invoked_subcommand` is `"*"` in a chained group, because the parser does not yet know
the full list.

## Command keywords

`@click.command(name=None, cls=None, help=..., epilog=..., short_help=...,
options_metavar="[OPTIONS]", add_help_option=True, no_args_is_help=False, hidden=False,
deprecated=False, context_settings=None)`

```python
@click.command("say-hello", deprecated=True)
def hello() -> None: ...

@click.command(deprecated="use `say-hello` instead")   # custom message, 8.2+
def greet() -> None: ...
```

`deprecated` renders `help (DEPRECATED)` in the listing and emits a warning when used. It
can also be set on options and arguments since 8.2, but not on required or prompted ones.
`hidden=True` removes the command from the help listing and from completion while keeping
it callable.

Naming: the function name with `_` → `-` and a trailing `_command`/`_cmd`/`_group`/`_grp`
stripped (`../quickstart.md`).

## Common Anti-Patterns

- `@click.group()` instead of `@cli.group()` for a nested group → it is never attached.
- Re-declaring the group's `--verbose` on every subcommand → declare it once on the group
  and pass it down via `ctx.obj` (`context.md`).
- Expecting `mytool --verbose sub` and `mytool sub --verbose` to be interchangeable → each
  parameter belongs to exactly one command level.
- Deleting a command outright for a rename → keep it with `deprecated=` for a release, and
  `add_command(cmd, name="old-name")` for the alias.
