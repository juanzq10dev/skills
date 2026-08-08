---
title: Shell completion (bash, zsh, fish)
triggers:
  - "adding tab completion to a CLI"
  - "pressing TAB suggests nothing for an installed command"
  - "suggesting dynamic values such as remote names or environment variables"
  - "supporting a shell Click does not ship support for"
---

# Shell completion

Docs: https://click.palletsprojects.com/en/stable/shell-completion/

Built-in shells: **bash (>= 4.4), zsh, fish**. Completion suggests command names, option
names (only after at least one `-` is typed), and values for `Choice`, `File` and `Path`.
Hidden commands and options are never suggested.

## Requirement

Completion works **only for a program installed as an entry point**, never for
`python app.py` (`packaging/entry-points.md`). Click enters completion mode when invoked
with `_{PROG_NAME}_COMPLETE` set — the executable name uppercased with `-` → `_`.

## Enabling it (program `foo-bar`)

```bash
# bash — ~/.bashrc
eval "$(_FOO_BAR_COMPLETE=bash_source foo-bar)"
```

```bash
# zsh — ~/.zshrc
eval "$(_FOO_BAR_COMPLETE=zsh_source foo-bar)"
```

```fish
# fish — ~/.config/fish/completions/foo-bar.fish
_FOO_BAR_COMPLETE=fish_source foo-bar | source
```

`eval` runs the program on every shell start. Prefer generating once and sourcing the file,
and ship the generated files with the package:

```bash
_FOO_BAR_COMPLETE=bash_source foo-bar > ~/.foo-bar-complete.bash
echo '. ~/.foo-bar-complete.bash' >> ~/.bashrc
```

A new shell is required after editing the config.

## Custom value completion

Per parameter, with `shell_complete=` — this **replaces** the type's completion:

```python
import os

import click


def complete_env_vars(ctx, param, incomplete):
    return [k for k in os.environ if k.startswith(incomplete)]


@click.command()
@click.argument("name", shell_complete=complete_env_vars)
def cli(name: str) -> None:
    click.echo(os.environ[name])
```

The callback takes `(ctx, param, incomplete)` and returns `CompletionItem` objects or, as a
shortcut, plain strings. `incomplete` may be `""`.

For a reusable rule, override `ParamType.shell_complete` on a custom type instead
(`parameters/types/custom-types.md`).

```python
from click.shell_completion import CompletionItem


class EnvVarType(click.ParamType[str]):
    name = "envvar"

    def shell_complete(self, ctx, param, incomplete):
        return [CompletionItem(n) for n in os.environ if n.startswith(incomplete)]
```

`CompletionItem.type` is usually `"plain"`; `"file"` or `"dir"` hands path completion to
the shell, which does it better than Click.

## Adding a new shell

Subclass `click.shell_completion.ShellComplete`, register it with `@add_completion_class`,
and implement `source_template`, `get_completion_args()` (returns `(args, incomplete)`) and
`format_completion(item)`. `source_template` is `%`-formatted with `complete_func`,
`complete_var` and `foo_bar`. Check PyPI first — the shell may already be supported.

## Common Anti-Patterns

- Documenting `eval "$(_APP_COMPLETE=bash_source python app.py)"` → completion needs the
  installed executable name, not an interpreter invocation.
- Guessing the variable name for a hyphenated program → `foo-bar` becomes `_FOO_BAR_COMPLETE`.
- Returning `(value, help)` tuples → return `CompletionItem(value, help=...)`.
- Assuming an option is suggested on a bare `<TAB>` → options appear only after a `-`.
