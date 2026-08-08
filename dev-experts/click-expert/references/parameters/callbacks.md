---
title: Parameter callbacks, validation and eagerness
triggers:
  - "validating a value beyond what a type can express"
  - "a flag should print something and exit immediately, like --version"
  - "a parameter should not be passed to the command function"
  - "one parameter's default should depend on another parameter"
  - "the order in which parameter callbacks run matters"
---

# Callbacks and eagerness

Docs: https://click.palletsprojects.com/en/stable/advanced/ and
https://click.palletsprojects.com/en/stable/click-concepts/

A callback is `f(ctx, param, value)`, called **after** type conversion, for every source
including prompts and defaults. It may transform the value (whatever it returns is what the
function receives) or raise.

## Validation

```python
import click


def validate_rolls(ctx, param, value):
    if isinstance(value, tuple):
        return value
    try:
        rolls, _, dice = value.partition("d")
        return int(dice), int(rolls)
    except ValueError:
        raise click.BadParameter("format must be 'NdM'")


@click.command()
@click.option("--rolls", type=click.UNPROCESSED, callback=validate_rolls, default="1d6")
def roll(rolls: tuple[int, int]) -> None: ...
```

`BadParameter` is auto-annotated with the parameter name. The `isinstance` guard is the
standard shape: the callback also sees already-converted defaults, not only user strings.

## Eager, exiting flags

```python
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 1.0")
    ctx.exit()


@click.command()
@click.option("--version", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello() -> None: ...
```

Three parts, all required:

- `is_eager=True` — run before non-eager parameters, so a missing required option does not
  error first.
- `expose_value=False` — keep the value out of the function signature.
- the `ctx.resilient_parsing` guard — during shell completion Click parses without side
  effects; without the guard the flag would print and exit mid-completion.

For a real `--version`, use `click.version_option()` (`shortcut-decorators.md`) rather than
this; the example above is the pattern for other exiting flags.

## Evaluation order

Callbacks fire in the order the **user** wrote the parameters, with three exceptions:

1. **Eager** parameters all run first, still in user order — so whichever of `--help` and
   `--version` comes first on the command line wins.
2. A **repeated** parameter fires once, at the position of its first occurrence, with all
   its values.
3. **Missing** parameters fire last, which lets their defaults depend on parameters that
   were supplied.

A non-`multiple` option given twice keeps the **last** value (so a shell alias can set a
default that the user overrides).

## Fabricating extra values

`ctx.params` is the dict handed to the command function, so a callback can write into it —
but this bypasses the per-parameter pipeline: `get_parameter_source` returns `None`, no
`ParamType` conversion runs, and a name collision loses source information. Prefer
returning a wrapper object:

```python
import urllib.request


class URL:
    def __init__(self, url, fp):
        self.url = url
        self.fp = fp


def open_url(ctx, param, value):
    if value is not None:
        return URL(value, urllib.request.urlopen(value))


@click.command()
@click.option("--url", callback=open_url)
def cli(url: URL | None) -> None: ...
```

## Common Anti-Patterns

- `raise ValueError("bad")` in a callback → shows a traceback; raise `click.BadParameter`.
- A `--version` callback without `is_eager=True` → a required option can error first.
- A callback that exits without the `ctx.resilient_parsing` guard → breaks shell completion.
- Validation logic in the command body when it applies to one parameter → put it in the
  callback, or better, in a `ParamType` (`types/custom-types.md`), which also gives you
  completion.
- Assuming a callback does not run when the option is absent → it does, with the default.
