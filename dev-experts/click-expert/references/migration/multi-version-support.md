---
title: Supporting several Click versions from one library
triggers:
  - "a library must work with both Click 8.1 and 8.2+"
  - "a ParamType override breaks because a method gained a ctx argument"
  - "choosing a Click version constraint for a package"
---

# Supporting multiple Click versions

Docs: https://click.palletsprojects.com/en/stable/support-multiple-versions/ and
https://palletsprojects.com/versions

Most of Click is stable across releases. The rule Click states for the rest:

> **Prefer feature detection.** Looking at the version is tempting but more brittle and
> produces more complicated code. Use `if` or `try` blocks to decide between the new and
> old pattern.

When a version really is needed, use `importlib.metadata.version("click")` — never
`click.__version__`, which is deprecated (`../public-api.md`).

## The 8.2 `ParamType` signature change

In 8.2 several `ParamType` methods gained a `ctx: click.Context` argument, which changes
the override signature. This decorator supplies `ctx` on 8.1 so one override works on both:

```python
import functools
import typing as t

import click

F = t.TypeVar("F", bound=t.Callable[..., t.Any])


def add_ctx_arg(f: F) -> F:
    @functools.wraps(f)
    def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:
        if "ctx" not in kwargs:
            kwargs["ctx"] = click.get_current_context(silent=True)

        return f(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


class CommaDelimitedString(click.ParamType[str]):
    @add_ctx_arg
    def get_metavar(self, param: click.Parameter, ctx: click.Context | None) -> str:
        return "TEXT,TEXT,..."
```

The same technique applies to the other methods that gained `ctx`, such as
`get_missing_message`.

Note the `ParamType[str]` parameterization is 8.4-only syntax at type-check time; under
older Click it is still valid at runtime only if the type checker is configured against the
version you actually install.

## Choosing a constraint

- An **application** should pin a narrow range and upgrade deliberately: `click>=8.4,<9`.
- A **library** should accept the widest range it actually supports and feature-detect,
  since the application owns the resolution.
- Do not require `>=8.2` for a feature that also exists earlier — check the per-version
  files in this directory before widening the floor.

## Common Anti-Patterns

- `if click.__version__ >= "8.2":` → deprecated attribute, and string comparison is wrong
  for versions anyway.
- `try: from click import MultiCommand except ImportError:` → it still imports on 8.2+,
  just warns; detect the capability, not the name.
- Pinning `click==8.x.y` exactly in a library → forces conflicts on every consumer.
