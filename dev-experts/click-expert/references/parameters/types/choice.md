---
title: `click.Choice`
triggers:
  - "restricting an option to a fixed list of allowed values"
  - "using a Python Enum as the set of accepted CLI values"
  - "accepting a choice case-insensitively"
  - "customizing the message shown for an invalid choice"
---

# Choice

Docs: https://click.palletsprojects.com/en/stable/parameter-types/

`Choice(choices, case_sensitive=True)` — `choices` is any iterable.

```python
import enum

import click


class HashType(enum.Enum):
    MD5 = enum.auto()
    SHA1 = enum.auto()


@click.command()
@click.option("--hash-type", type=click.Choice(HashType, case_sensitive=False))
@click.option("--mode", type=click.Choice(["fast", "slow"]), default="fast")
def digest(hash_type: HashType, mode: str) -> None: ...
```

Key behaviors:

- Passing an `Enum` uses the **member names** as the accepted strings and delivers the
  **member** to the function. Since 8.2, `Choice` accepts any iterable, not just `str`.
- The value delivered is always one of the originally passed choices, never the raw string
  the user typed — normalization and `case_sensitive=False` can make the two differ. The
  normalization rule is `Choice.normalize_choice`; choices must be unique after it.
- Works with `multiple=True`; then `default` must be a list or tuple of valid choices.
- The choices are listed in `--help` and offered by shell completion. `show_choices=False`
  hides them and shows the type's `name` instead.
- Override `Choice.get_invalid_choice_message` (8.2+) to customize the error text.
- Since 8.4.0, `Choice` is generic: annotate `click.Choice[HashType]` or `click.Choice[str]`.

For enum defaults, the enum **value** is what is rendered in the help page (8.2.2+).

## Common Anti-Patterns

- `type=str` plus `if value not in ALLOWED: raise` → `Choice` gives the error, the help
  listing and completion for free.
- `click.Choice([e.value for e in HashType])` → pass `HashType` itself and get the member
  back instead of a string you must re-look-up.
- Duplicate choices after case folding with `case_sensitive=False` → they must be unique
  post-normalization.
