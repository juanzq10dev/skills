---
title: Writing a custom `ParamType`
triggers:
  - "converting a command line string into a domain object"
  - "reusing one validation rule across several commands"
  - "a custom type needs to offer its own shell completion suggestions"
  - "a ParamType subclass breaks after upgrading Click"
---

# Custom parameter types

Docs: https://click.palletsprojects.com/en/stable/parameter-types/

Subclass `ParamType`, set `name`, override `convert`. Since 8.4.0 `ParamType` is a
**generic abstract base class** — parameterize it with the converted value type.

```python
import click


class BasedIntParamType(click.ParamType[int]):
    name = "integer"

    def convert(self, value, param, ctx) -> int:
        if isinstance(value, int):
            return value
        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            if value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)


BASED_INT = BasedIntParamType()
```

Rules that matter:

- **Call `self.fail(msg, param, ctx)`** on failure — do not raise `ValueError`. `param` and
  `ctx` may be `None` (for example when the type is used from `click.prompt`), so never
  dereference them unconditionally.
- **Guard for already-converted values.** `convert` also sees defaults and values passed
  from Python, which may already be the target type — hence the `isinstance` check.
- `name` is what the help page and error messages show.
- Instantiate once at module level and reuse; types are stateless.

## Completion

Override `shell_complete` to make the type suggest values everywhere it is used:

```python
import os

from click.shell_completion import CompletionItem


class EnvVarType(click.ParamType[str]):
    name = "envvar"

    def shell_complete(self, ctx, param, incomplete):
        return [CompletionItem(n) for n in os.environ if n.startswith(incomplete)]
```

See `../../shell-completion.md` for per-parameter overrides and item types.

## Version notes

- **8.2** added a `ctx` argument to several `ParamType` methods (`get_metavar`,
  `get_missing_message`, …). Supporting 8.1 and 8.2 from one codebase needs a shim —
  `../../migration/multi-version-support.md`.
- **8.4.0** made `ParamType` generic and abstract, narrowed `convert` return types on all
  concrete types, and made `to_info_dict` return `TypedDict` subclasses. `CompositeParamType`
  and the number-range base are generic with abstract methods.

## Common Anti-Patterns

- `type=my_function` (a bare callable raising `ValueError`) → supported but discouraged: no
  `name`, no completion, worse errors. Subclass `ParamType`.
- Forgetting the `isinstance` guard → the type crashes on its own default value.
- `raise click.BadParameter(...)` inside `convert` → use `self.fail`, which attaches the
  parameter and context for you.
- Instantiating the type inside the decorator call in a loop → make one module-level
  singleton.
