---
title: Options (`@click.option`)
triggers:
  - "declaring a --flag that takes a value"
  - "an option should accept several values or be repeatable"
  - "combining short options like -abc or -vn5 on the command line"
  - "making an option required, hidden or deprecated"
  - "an option's value should be optional after the flag itself"
---

# Options

Docs: https://click.palletsprojects.com/en/stable/options/

```python
@click.command()
@click.option("--count", "-c", default=1, show_default=True, help="How many.")
def repeat(count: int) -> None: ...
```

Most-used keywords: `default`, `help`, `type`, `required`, `nargs`, `multiple`, `envvar`,
`show_default`, `metavar`, `hidden`, `deprecated`. Flag-specific keywords live in
`flags.md`; value sources in `value-resolution.md`.

## Type and default

With no `type=`, the type is inferred from `default` (falling back to `STRING`). An option
that is never passed and has no default yields `None`.

```python
@click.option("--n", default=1)          # inferred INT
@click.option("--ratio", type=float)     # explicit
```

## Several values

| Need                     | Declaration           | Value received                         |
| ------------------------ | --------------------- | -------------------------------------- |
| Fixed count, one type    | `nargs=2, type=float` | `tuple[float, float]`                  |
| Fixed count, mixed types | `type=(str, int)`     | `tuple[str, int]`                      |
| Repeatable               | `multiple=True`       | `tuple[...]`, one entry per occurrence |
| Count occurrences        | `count=True`          | `int` (0 when absent)                  |

```python
@click.command()
@click.option("--pos", nargs=2, type=float)
@click.option("--item", type=(str, int))
@click.option("--message", "-m", multiple=True)
@click.option("-v", "--verbose", count=True)
def cli(pos, item, message, verbose): ...
```

`nargs` accepts any positive integer but **not** `-1` (that is arguments-only). A tuple
literal as `type` sets `nargs` automatically and is equivalent to
`nargs=2, type=click.Tuple([str, int])` (`types/tuple-and-multiple.md`). With
`multiple=True`, `default` must be a list or tuple — a string default is read as a list of
characters.

## Short option stacking

Single-character short options combine POSIX-style: `-abc` is `-a -b -c`, which is why
`-vvv` works for `count=True`. A trailing value-taking option can attach its value:
`-vn 5`, `-vn5` and `-v -n 5` are all equivalent.

**Multi-character short names are not supported.** `-dbg` is parsed as `-d -b -g` and
fails with `No such option: -d`. Use a long option (`--debug`) instead.

## Optional value

`is_flag=False, flag_value=...` lets the flag be given with or without a value:

```python
@click.command()
@click.option("--name", is_flag=False, flag_value="Flag", default="Default")
def hello(name: str) -> None: ...
# (no flag)      -> "Default"
# --name Value   -> "Value"
# --name         -> "Flag"
```

Combined with `prompt=True, prompt_required=False`, a bare `--name` prompts instead
(`prompting.md`).

## Alternative prefixes

`/` and `+` work as prefixes (`+w/-w`). With `/` in the name, split the on/off pair with
`;` instead: `@click.option("/debug;/no-debug")`. Use sparingly — non-POSIX.

## Common Anti-Patterns

- `@click.option("--items", multiple=True, default="abc")` → `default=["abc"]`; a string
  default becomes `("a", "b", "c")`.
- `@click.option("-verbose")` expecting a long option → that is the short option `-v`
  stacked with `-e -r -b -o -s -e`. Write `--verbose`.
- `@click.option("--n", nargs=-1)` → invalid for options; use `multiple=True`, or an
  argument with `nargs=-1` (`arguments.md`).
- Re-implementing `-v -vv -vvv` with three flags → `count=True`.
- `required=True` together with a `default` → the default can never be reached.
