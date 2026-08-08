---
title: Prompting for input
triggers:
  - "asking the user for a value that was not supplied on the command line"
  - "reading a password without echoing it"
  - "asking for yes/no confirmation before a destructive action"
  - "a prompt should offer a default computed at runtime"
  - "a prompt should appear only when the flag is given without a value"
---

# Prompting

Docs: https://click.palletsprojects.com/en/stable/prompts/

## Option-driven prompts

```python
@click.command()
@click.option("--name", prompt="Your name please")
def hello(name: str) -> None: ...
```

`prompt=True` uses the parameter name, title-cased, as the prompt text. The prompt fires
only when no more explicit source supplied a value (`value-resolution.md`), and the result
is recorded as `ParameterSource.PROMPT`.

| Keyword                              | Effect                                                 |
| ------------------------------------ | ------------------------------------------------------ |
| `prompt=True \| "text"`              | prompt when the value is missing                       |
| `prompt_required=False`              | prompt only when the flag is given **without** a value |
| `hide_input=True`                    | do not echo (passwords)                                |
| `confirmation_prompt=True \| "text"` | ask twice and compare                                  |
| `show_default=`                      | what the prompt advertises as the default              |

```python
@click.command()
@click.option("--name", prompt=True, prompt_required=False, default="Default")
def hello(name: str) -> None: ...
# (nothing)      -> "Default"
# --name Value   -> "Value"
# --name         -> prompts
```

With `required=True`, the option prompts both when absent and when the bare flag is given.

## Dynamic defaults

`auto_envvar_prefix` and `default_map` suppress the prompt, because they supply a value. To
keep the prompt while still offering a computed default, pass a **callable** default:

```python
import os

import click


@click.command()
@click.option(
    "--username",
    prompt=True,
    default=lambda: os.environ.get("USER", ""),
    show_default="current user",
)
def hello(username: str) -> None: ...
```

## Standalone prompts

```python
value = click.prompt("Enter a port", type=int, default=8080)
secret = click.prompt("Password", hide_input=True, confirmation_prompt=True)

if click.confirm("Do you want to continue?"):
    ...
click.confirm("Really drop the database?", abort=True)   # raises Abort on "no"
```

`click.prompt(text, default=None, hide_input=False, confirmation_prompt=False, type=None,
value_proc=None, prompt_suffix=": ", show_default=True, err=False, show_choices=True)`.
The type is inferred from `default` when not given. `confirm(text, default=False,
abort=False, prompt_suffix=": ", show_default=True, err=False)`.

Since 8.4.0 a failed `hide_input` prompt shows the type's own error message, with the
entered value masked, instead of a generic one.

For the ready-made `--password` and `--yes` decorators see `shortcut-decorators.md`.

## Common Anti-Patterns

- `@click.option("--tags", multiple=True, prompt=True)` → not supported in a useful way;
  prompt inside the function body instead.
- `input("Name: ")` → `click.prompt`, which handles types, defaults, retries and the
  Windows console.
- Prompting for a value that also has `envvar=` and expecting both → the environment wins
  and the prompt never fires; use a callable default.
- `getpass.getpass()` → `hide_input=True`, so `CliRunner` can drive it in tests.
- Marking a prompted parameter `deprecated=` → Click raises; the two are incompatible.
