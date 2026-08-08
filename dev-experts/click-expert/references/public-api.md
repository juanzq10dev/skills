---
title: Public API surface (what exists in `click`)
triggers:
  - "checking whether a name is importable from click before using it"
  - "an import from click raises AttributeError or a DeprecationWarning"
  - "reviewing code that uses BaseCommand, MultiCommand, OptionParser or click.__version__"
---

# Public API surface

Docs: https://click.palletsprojects.com/en/stable/api/

Everything below is exported from the top-level `click` package in 8.4.2. If a name is not
here, it is not public — do not invent it.

## Decorators

`command`, `group`, `argument`, `option`, `password_option`, `confirmation_option`,
`version_option`, `help_option`, `pass_context`, `pass_obj`, `make_pass_decorator`
(plus `click.decorators.pass_meta_key`). See `parameters/shortcut-decorators.md`.

## Core classes

`Command`, `Group`, `CommandCollection`, `Context`, `Parameter`, `Option`, `Argument`,
`ParameterSource`. See `commands/INDEX.md`.

## Types

`ParamType`, `STRING`, `INT`, `FLOAT`, `BOOL`, `UUID`, `UNPROCESSED`, `Choice`, `DateTime`,
`File`, `Path`, `IntRange`, `FloatRange`, `Tuple`. See `parameters/types/INDEX.md`.

## Terminal and IO

`echo`, `secho`, `style`, `unstyle`, `echo_via_pager`, `get_pager_file`, `prompt`,
`confirm`, `progressbar`, `clear`, `pause`, `getchar`, `edit`, `launch`,
`get_binary_stream`, `get_text_stream`, `open_file`, `get_app_dir`, `format_filename`.
See `utils/INDEX.md`.

## Exceptions and formatting

`ClickException`, `UsageError`, `BadParameter`, `MissingParameter`, `FileError`,
`NoSuchCommand`, `NoSuchOption`, `BadOptionUsage`, `BadArgumentUsage`, `Abort`,
`HelpFormatter`, `wrap_text`. See `errors-and-exit-codes.md`.

## Other modules

- `click.testing` — `CliRunner`, `Result` (`testing.md`).
- `click.shell_completion` — `CompletionItem`, `ShellComplete`, `add_completion_class`,
  `split_arg_string` (`shell-completion.md`).
- `click.globals` — `get_current_context` (re-exported as `click.get_current_context`).

## Deprecated names

These still import but emit `DeprecationWarning`:

| Deprecated                                       | Replacement                               | Removed in |
| ------------------------------------------------ | ----------------------------------------- | ---------- |
| `click.BaseCommand`                              | `click.Command`                           | 9.0        |
| `click.MultiCommand`                             | `click.Group`                             | 9.0        |
| `click.OptionParser` / the `click.parser` module | none — parsing is internal now            | 9.0        |
| `click.__version__`                              | `importlib.metadata.version("click")`     | 9.1        |
| `Context.protected_args`                         | `Context.args`                            | 9.0        |
| `Parameter.add_to_parser`                        | none — no separate parser is built        | 9.0        |
| `click.parser.split_arg_string`                  | `click.shell_completion.split_arg_string` | 9.0        |

## Escape hatch

When a signature is not covered by these reference files, read the annotated source rather
than guessing — Click ships `py.typed`, so the installed package is authoritative:

```console
$ python -c "import click, inspect; print(inspect.signature(click.Option.__init__))"
```
