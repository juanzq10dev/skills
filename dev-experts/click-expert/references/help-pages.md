---
title: Help pages and usage text
triggers:
  - "customizing what --help prints for a command or group"
  - "help text is re-wrapped and the formatting is destroyed"
  - "adding -h as an alias for --help"
  - "documenting a positional argument that has no help= keyword"
---

# Help pages

Docs: https://click.palletsprojects.com/en/stable/documentation/

Text is customizable; **layout is not**. Click owns the sections and their order.

## Sources of help text

| Element                             | Source                                                       |
| ----------------------------------- | ------------------------------------------------------------ |
| Command description                 | function docstring, or `help=` on the decorator              |
| One-line summary in a group listing | first sentence of the docstring, or `short_help=`            |
| Trailing section                    | `epilog=`                                                    |
| Option description                  | `help=` on `@click.option`                                   |
| Argument description                | the command docstring — `@click.argument` has **no** `help=` |

```python
@click.command(epilog="See https://example.com for more details.")
@click.argument("filename")
@click.option("--count", default=1, show_default=True, help="How many times.")
def touch(filename: str, count: int) -> None:
    """Touch FILENAME.

    FILENAME is the path to create.
    """
```

## Wrapping escapes

Click ignores single newlines and re-wraps each paragraph to the terminal width (max 80).

- A line containing only `\b` disables re-wrapping for the **following** paragraph. The
  `\b` itself is removed from the output.
- `\f` truncates the help text at that point — everything after it stays in the docstring
  but is never shown.
- Both live inside the docstring, so the docstring must be a raw string or escape the
  backslashes.

```python
@click.command()
def cli() -> None:
    """First paragraph.

    \b
    This block
    keeps its
    line breaks.
    \f
    Internal notes never shown in --help.
    """
```

Widen output with `cli(max_content_width=120)` or `context_settings={"max_content_width": 120}`.

## Metavars and defaults

```python
@click.command(options_metavar="[[options]]")
@click.option("--count", default=1, metavar="<int>", show_default="one")
@click.argument("name", metavar="<name>")
def hello(name: str, count: int) -> None: ...
```

- `show_default=True` prints `[default: …]`; `show_default="current user"` prints that
  string instead (useful with a callable default). Set it globally with
  `context_settings={"show_default": True}`.
- `show_envvar=True` prints the environment variable name in the help record.
- A single boolean flag whose default is `False` never shows a default, even with
  `show_default=True`.

## Usage-line bracket convention

An element is optional exactly when it is bracketed: `FOO` required, `[FOO]` optional,
`[FOO]...` optional and repeatable. `[OPTIONS]` is always bracketed. A `Group` with
`invoke_without_command=True` renders `[COMMAND]` instead of `COMMAND`. A chained group
renders `[COMMAND2 [ARGS]...]...`.

## Changing the help option

```python
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
def cli() -> None: ...
```

Declaring your own parameter named `help` suppresses the automatic one. Error hints
(`Try '... --help'`) pick the longest non-shadowed help option name.

## Common Anti-Patterns

- `@click.argument("name", help="...")` → `TypeError`; document arguments in the docstring
  (`parameters/arguments.md`).
- Hand-indenting a docstring to control layout → use `\b`; indentation is stripped.
- Building the whole help string yourself to add examples → use `epilog=`.
- Marking a required or prompted parameter `deprecated=` → Click raises; deprecation is
  incompatible with `required=True` and with prompting.
