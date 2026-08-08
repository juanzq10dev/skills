---
title: Custom `Group` subclasses, aliases and plugins
triggers:
  - "accepting an abbreviation or alias for a subcommand"
  - "discovering subcommands from a directory, entry points or a plugin registry"
  - "changing how a group lists or resolves its commands"
  - "applying shared behavior to every command in a CLI"
---

# Custom command classes

Docs: https://click.palletsprojects.com/en/stable/extending-click/

Two methods carry almost all customization: `Group.get_command(ctx, name)` resolves a name,
`Group.list_commands(ctx)` enumerates for help and completion. Attach the subclass with
`cls=`:

```python
@click.group(cls=PluginGroup, plugin_folder="commands")
def cli() -> None: ...
```

Any extra keyword on the decorator is forwarded to the class constructor.

## Aliases and prefix matching

```python
class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always report the full command name in help and errors
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args
```

Deliberately do **not** override `list_commands` here: aliases should not be enumerated in
the help page, or the listing becomes noise.

For a fixed alias with no subclass at all, register the same command twice:
`cli.add_command(status, name="st")` (`groups.md`).

## Plugin discovery

```python
import importlib.util
import os

import click


class PluginGroup(click.Group):
    def __init__(self, name=None, plugin_folder="commands", **kwargs):
        super().__init__(name=name, **kwargs)
        self.plugin_folder = plugin_folder

    def list_commands(self, ctx):
        return sorted(f[:-3] for f in os.listdir(self.plugin_folder) if f.endswith(".py"))

    def get_command(self, ctx, name):
        path = os.path.join(self.plugin_folder, f"{name}.py")
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.cli
```

The same shape works over `importlib.metadata.entry_points()` for pip-installed plugins.
When the goal is only to avoid slow imports of commands you already know about, use the
declarative form in `lazy-loading.md` instead.

## Custom `Command`

Subclass `click.Command` and pass `cls=` to `@click.command()` for cross-cutting behavior —
a shared `--verbose`, uniform error formatting, extra help sections. Useful overrides:
`format_options`, `get_help_option_names`, `parse_args`, `invoke`.

Before writing one, check `ecosystem/INDEX.md`: option groups, constraints, aliases and
themed help are already solved by `cloup` and `click-extra`.

## Common Anti-Patterns

- Overriding `list_commands` to include aliases → they show up as duplicate entries in
  `--help`.
- Returning a non-`Command` from `get_command` → fails deep inside Click; validate and
  raise a clear error at load time.
- Scanning the plugin folder in `get_command` on every call → cache it; `get_command` is
  hit by resolution, help rendering and completion.
- Writing a custom group to add option groups or colored help → use `cloup` /
  `click-extra`.
