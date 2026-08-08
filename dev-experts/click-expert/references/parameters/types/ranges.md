---
title: `IntRange` and `FloatRange`
triggers:
  - "constraining a numeric option to a minimum, a maximum, or both"
  - "an out-of-range value should be silently clamped instead of rejected"
  - "an upper or lower bound should be exclusive"
---

# Numeric ranges

Docs: https://click.palletsprojects.com/en/stable/parameter-types/

`IntRange` extends `INT`, `FloatRange` extends `FLOAT`. Both take
`(min=None, max=None, min_open=False, max_open=False, clamp=False)`.

```python
@click.command()
@click.option("--count", type=click.IntRange(0, 20, clamp=True))
@click.option("--digit", type=click.IntRange(0, 9))
@click.option("--port", type=click.IntRange(1024, None))          # unbounded above
@click.option("--ratio", type=click.FloatRange(0, 1, min_open=True))
def cli(count, digit, port, ratio) -> None: ...
```

- Omitting `min` or `max` leaves that side **unbounded**.
- Bounds are **closed** by default; `min_open` / `max_open` exclude the boundary.
- `clamp=True` pins out-of-range input to the nearest bound instead of failing — with
  `IntRange(0, 20, clamp=True)`, `--count=100` becomes `20`.
- `FloatRange` allows `clamp` only when both bounds are closed.
- The accepted range appears in the help page automatically.

## Common Anti-Patterns

- `type=int` then `if not 0 <= n <= 9: raise` → the range type says it in the help page too.
- `clamp=True` on a value where silent correction hides a user mistake → prefer failing;
  reserve clamping for cosmetic values like widths and counts.
- `FloatRange(0, 1, max_open=True, clamp=True)` → rejected; clamping needs closed bounds.
