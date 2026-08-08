---
title: Lazily loading subcommands
triggers:
  - "a CLI is slow to start because every subcommand's imports run up front"
  - "deferring a heavy import until the subcommand actually runs"
  - "understanding when a lazily loaded subcommand is actually imported"
---

# Lazy subcommand loading

Docs: https://click.palletsprojects.com/en/stable/complex/

Worth doing only when startup time is measurably dominated by imports. Lazy loading trades
it for harder-to-trace bugs, circular imports and order dependence — pair it with a test
that runs `--help` on **every** subcommand, which is enough to prove each one imports.

## Declarative lazy group

```python
# lazy_group.py
import importlib

import click


class LazyGroup(click.Group):
    def __init__(self, *args, lazy_subcommands=None, **kwargs):
        super().__init__(*args, **kwargs)
        # {command-name: "module.path.command_object"}
        self.lazy_subcommands = lazy_subcommands or {}

    def list_commands(self, ctx):
        return super().list_commands(ctx) + sorted(self.lazy_subcommands)

    def get_command(self, ctx, cmd_name):
        if cmd_name in self.lazy_subcommands:
            return self._lazy_load(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _lazy_load(self, cmd_name):
        import_path = self.lazy_subcommands[cmd_name]
        modname, cmd_object_name = import_path.rsplit(".", 1)
        cmd_object = getattr(importlib.import_module(modname), cmd_object_name)
        if not isinstance(cmd_object, click.Command):
            raise ValueError(f"Lazy loading of {import_path} returned a non-command")
        return cmd_object
```

```python
# main.py
@click.group(cls=LazyGroup, lazy_subcommands={"foo": "foo.cli", "bar": "bar.cli"})
def cli() -> None:
    """Main CLI."""
```

A lazily loaded subcommand may itself be a `LazyGroup`, so the tree stays lazy at every
level.

## What triggers a load

1. **Resolution** — `cli bar baz` loads `bar`, then `baz`.
2. **Help rendering** — `cli --help` loads every _direct_ child to read its short help, but
   not their children.
3. **Shell completion** — completing the subcommands of `cli` loads them.

So `--help` at the root is the worst case, and it is exactly what the recommended test
exercises.

## Deferring the body instead

Simpler, and often enough: declare the command eagerly and import inside the callback. Help
text, options and completion all keep working, because Click builds them from the
decorators, not the body.

```python
@click.command()
@click.option("-n", type=int)
def foo(n: int) -> None:
    from mylibrary import foo_concrete

    foo_concrete(n)
```

## Common Anti-Patterns

- Lazy-loading a CLI whose imports are already fast → pure complexity.
- Skipping the `isinstance(cmd_object, click.Command)` check → a typo in the import path
  surfaces as a confusing failure far from its cause.
- Assuming `--help` stays lazy → it loads every direct child.
- Deferring imports without a per-subcommand `--help` test → a broken import is only found
  when a user runs that subcommand.
