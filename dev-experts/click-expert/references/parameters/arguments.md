---
title: Arguments (`@click.argument`)
triggers:
  - "declaring a positional input such as a filename or source/destination pair"
  - "a command should accept an arbitrary number of trailing values"
  - "a filename that starts with a dash is parsed as an option"
  - "forwarding unrecognized flags through to another program"
  - "documenting a positional parameter that has no help keyword"
---

# Arguments

Docs: https://click.palletsprojects.com/en/stable/arguments/

Positional, required by default, `STRING` unless a `type=` or a typed `default` says
otherwise. `@click.argument` accepts `default`, `nargs`, `type`, `required`, `envvar`,
`metavar`, `callback`, `shell_complete` — but **not** `help`.

```python
@click.command()
@click.argument("src", nargs=1)
@click.argument("dsts", nargs=-1)
def copy(src: str, dsts: tuple[str, ...]) -> None:
    """Copy SRC into each of DSTS."""
```

## `nargs`

| `nargs`       | Value received                                                      |
| ------------- | ------------------------------------------------------------------- |
| `1` (default) | a single value                                                      |
| `n > 1`       | a tuple of exactly `n`                                              |
| `-1`          | a tuple of any length, possibly empty — **at most one per command** |

A variadic argument is not "required" in any useful sense; it is empty when nothing is
given. Since 8.3, `default` may be set on an `Argument` with `nargs=-1`.

Click's guidance is to keep positionals few and required. Optional and variadic positionals
are filled left-to-right, which users cannot see from the usage line.

## Values that look like options

Users pass `--` first:

```console
$ touch -- -foo.txt bar.txt
```

To accept them without the separator, turn off unknown-option checking for the command:

```python
@click.command(context_settings={"ignore_unknown_options": True})
@click.argument("files", nargs=-1, type=click.Path())
def touch(files: tuple[str, ...]) -> None: ...
```

## Forwarding to another program

The wrapper pattern — swallow everything unrecognized and hand it off:

```python
from subprocess import call

import click


@click.command(context_settings={"ignore_unknown_options": True})
@click.option("-v", "--verbose", is_flag=True)
@click.argument("timeit_args", nargs=-1, type=click.UNPROCESSED)
def cli(verbose: bool, timeit_args: tuple[str, ...]) -> None:
    """A wrapper around python -mtimeit."""
    cmdline = ["python", "-mtimeit", *timeit_args]
    if verbose:
        click.echo(f"Invoking: {' '.join(cmdline)}")
    call(cmdline)
```

`type=click.UNPROCESSED` stops Click from coercing the passthrough values to `str`.

Limits worth knowing:

- Unknown **long** options pass through untouched, but the parser cannot know whether
  `--foo bar` takes a value, so `bar` may be split off as an argument.
- Unknown **short** options are partially consumed: with `-v` declared, `-va` gives `-v` to
  Click and leaves `-a`.
- `allow_interspersed_args=False` (a context setting) stops options and arguments from
  being mixed, which sometimes improves results.

The alternative to `nargs=-1` is `pass_context` plus `allow_extra_args=True`, which puts
the leftovers in `ctx.args` (`../commands/context.md`).

Structurally, forwarding a whole subcommand to another program beats interleaving your own
options with someone else's.

## Environment variables

Arguments read only **explicitly named** variables — there is no `auto_envvar_prefix`
support for them.

```python
@click.argument("src", envvar=["SRC", "SRC_2"], type=click.File("r"))
```

The first variable found wins.

## Common Anti-Patterns

- `@click.argument("name", help="the name")` → `TypeError`; document it in the docstring as
  `NAME is …` (`../help-pages.md`).
- Two `nargs=-1` arguments on one command → only one is allowed.
- `required=True` on every positional "for safety" → Click's guidance is that CLIs should
  degrade gracefully when a wildcard expands to nothing.
- Using `nargs=-1` on a non-final command in a chained group → the parser can no longer
  find the next command (`../commands/chaining.md`).
