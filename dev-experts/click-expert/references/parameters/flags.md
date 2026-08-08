---
title: Boolean flags and feature switches
triggers:
  - "adding an on/off switch to a command"
  - "a flag should have an explicit --no- counterpart"
  - "several flags should write to the same variable, like --upper / --lower"
  - "a flag receives an unexpected value when it is not passed"
  - "a flag is controlled by an environment variable and the truthiness is wrong"
---

# Flags and feature switches

Docs: https://click.palletsprojects.com/en/stable/options/

## Pick the form — use the FIRST that applies

1. Plain on/off, default off → `is_flag=True`.
2. The user must be able to say "off" explicitly, or the default is dynamic → the **pair**
   form `--shout/--no-shout`. Click sets `is_flag=True` automatically.
3. Several mutually exclusive choices writing to one variable → `flag_value=` on each,
   sharing the destination name (a _feature switch group_).
4. Counting repetitions → `count=True` (`options.md`).

```python
@click.command()
@click.option("--shout", is_flag=True)
@click.option("--color/--no-color", default=True)
@click.option("--upper", "transformation", flag_value="upper", default="upper")
@click.option("--lower", "transformation", flag_value="lower")
def info(shout: bool, color: bool, transformation: str) -> None: ...
```

Aliasing only the off switch needs a leading space to disambiguate:
`@click.option("--shout/--no-shout", " /-N", default=False)`.

## How `default` and `flag_value` interact

The rule, in one sentence: **`default` is delivered literally, except that on a
non-boolean flag `default=True` is shorthand for "activate this flag", resolving to
`flag_value`.**

| Flag shape                                                    | `default=True` means      |
| ------------------------------------------------------------- | ------------------------- |
| bare boolean flag / `--x/--no-x` / boolean `flag_value`       | the literal Python `True` |
| non-boolean `flag_value` (`"upper"`, an enum member, a class) | the `flag_value` itself   |

```python
# These two are equivalent — prefer the second, it says what it means.
@click.option("--upper", "transformation", flag_value="upper", default=True)
@click.option("--upper", "transformation", flag_value="upper", default="upper")
```

Selected outcomes for a non-boolean switch group (`--upper`/`--lower`, `flag_value`
`"upper"`/`"lower"`):

| `default` on `--upper` | Neither passed | `--upper` | `--lower` |
| ---------------------- | -------------- | --------- | --------- |
| `True` or `"upper"`    | `"upper"`      | `"upper"` | `"lower"` |
| `None`                 | `None`         | `"upper"` | `"lower"` |
| absent on both options | `None`         | `"upper"` | `"lower"` |

`default=None` is the three-state pattern: distinguishable from either explicit choice.

For a **boolean** group, no substitution happens, so name the winner explicitly:

```python
@click.option("--without-xyz", "enable_xyz", flag_value=False)
@click.option("--with-xyz", "enable_xyz", flag_value=True, default=True)
```

With no `default` anywhere, a boolean group yields `False`; a non-boolean group yields
`None`.

## Type inference for flags

At construction, with no explicit `type=`:

1. `flag_value` is `True`/`False` → `BOOL`.
2. `flag_value` is `int`, `float` or `str` → that basic type.
3. `flag_value` is any other object (class, enum member, `frozenset`) → `UNPROCESSED`, so
   it passes through unchanged. Since 8.4.0 this is automatic; `type=click.UNPROCESSED`
   no longer has to be written by hand.
4. Otherwise inferred from `default`, falling back to `STRING`.

## Environment variables for flags

Values are stripped and case-folded, then:

- **Activate:** `true`, `1`, `yes`, `on`, `t`, `y` — or the flag's own `flag_value`.
- **Deactivate:** `false`, `0`, `no`, `off`, `f`, `n`, an empty string, a bare
  present-but-unset variable, and **anything else**.

There is no magic `NO_FLAG` variable for a `--flag/--no-flag` pair — only the name given to
`envvar=` is read. When `envvar` and `flag_value` are both set, the `flag_value` is used as
the value (8.2+).

## Common Anti-Patterns

- `flag_value=False, default=True` for a "disable" switch → use the pair form
  `--with-xyz/--without-xyz`; it is shorter and self-documenting.
- Expecting `default=True` on `--upper` (`flag_value="upper"`) to deliver Python `True` →
  it delivers `"upper"`.
- `@click.option("--debug", is_flag=True, default=None)` and then testing `if debug is
False` → `None` is a real explicit default here, not `False`.
- Reading an env var as truthy Python (`bool(os.environ["X"])`) alongside Click's own
  parsing → Click's rules above are stricter; let `envvar=` do it.
- Assuming the flag declared first wins a switch-group tie → arbitration is source-aware
  and the fallback is **last declared** (`value-resolution.md`).
