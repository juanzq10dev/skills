---
title: Tuples, `DateTime`, `UUID` and `UNPROCESSED`
triggers:
  - "one flag should take several values of different types"
  - "parsing a date or timestamp argument"
  - "a value must reach the function without any string conversion"
  - "accepting a UUID on the command line"
---

# Tuple, DateTime, UUID, UNPROCESSED

Docs: https://click.palletsprojects.com/en/stable/parameter-types/ and
https://click.palletsprojects.com/en/stable/api/

## `Tuple`

For one flag taking several values of **different** types. Writing a tuple literal as
`type` is the idiomatic form — it sets `nargs` and builds the `Tuple` for you:

```python
@click.option("--item", type=(str, int))                       # preferred
@click.option("--item", nargs=2, type=click.Tuple([str, int])) # equivalent
```

For several values of the **same** type, use `nargs=n` with a plain type; for a repeatable
flag, use `multiple=True` (`../options.md`).

## `DateTime`

`DateTime(formats=None)` tries each format in turn and delivers a `datetime.datetime`. The
defaults are `%Y-%m-%d`, `%Y-%m-%dT%H:%M:%S`, `%Y-%m-%d %H:%M:%S`.

```python
@click.option("--since", type=click.DateTime(formats=["%Y-%m-%d"]))
```

The accepted formats are shown in the help page.

## `click.UUID`

Accepts a UUID string and delivers `uuid.UUID`. Never inferred — ask for it explicitly.

```python
@click.argument("run_id", type=click.UUID)
```

## `click.UNPROCESSED`

Passes the value through with no conversion at all. Two uses:

1. Collecting passthrough arguments destined for another program
   (`../arguments.md`).
2. Feeding a `callback` that does its own parsing from the raw string
   (`../callbacks.md`).

Since 8.4.0 you rarely need it on a flag: a `flag_value` that is not `str`/`int`/`float`/
`bool` auto-selects `UNPROCESSED` (`../flags.md`).

## Common Anti-Patterns

- `type=click.Tuple([str, int])` without `nargs=2` when writing `Tuple` explicitly → the
  tuple literal form avoids the mistake entirely.
- `multiple=True` with `nargs=2` expecting a flat list → you get a tuple of 2-tuples.
- `datetime.strptime(value, ...)` in the command body → `DateTime` reports the accepted
  formats in the error and the help page.
- `type=click.UNPROCESSED` "to be safe" on ordinary options → you lose conversion,
  validation and completion.
