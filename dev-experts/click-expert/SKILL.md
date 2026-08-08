---
name: click-expert
description: >
  Expert guidance for working with Click 8.4.x, the Python "Command Line Interface Creation
  Kit" used to build CLIs from decorated functions.
  ALWAYS use before doing any task that requires knowledge specific to Click, or that
  references click.command, click.group, click.option, click.argument, Context, pass_context,
  pass_obj, ParamType, Choice, click.Path, click.File, click.echo, CliRunner, shell
  completion, or entry points / console_scripts for a Python CLI.
  Common tasks may include starting a new Python CLI, adding an option or positional argument,
  building nested subcommands or a command group, sharing state between a group and its
  subcommands, defining a boolean flag or a --x/--no-x pair, reading values from environment
  variables or a config file, validating or converting a parameter, prompting for input,
  writing a custom parameter type, coloring terminal output or showing a progress bar,
  testing a CLI with CliRunner, enabling tab completion, packaging the CLI as an installable
  command, or upgrading a CLI across Click 8.1 → 8.2 → 8.3 → 8.4.
---

# Click expert

Target version: **Click 8.4.2** (content true for 8.4.x; requires Python >= 3.10).
Reference files cite `https://click.palletsprojects.com/en/stable/…`.

## Core Click Concepts

- **Command** — a Python function wrapped by `@click.command()`; its docstring becomes the
  help text and its parameters become the CLI surface.
- **Group** — a `Command` that holds subcommands (`@click.group()`), nestable arbitrarily.
- **Parameter** — either an **Option** (`--flag`, optional, self-documenting) or an
  **Argument** (positional, documented by hand). See `references/parameters/INDEX.md`.
- **Context** — per-invocation state, linked parent-to-child; carries `ctx.obj`, defaults,
  and resource cleanup. It is how a group talks to its subcommands.
- **ParamType** — the converter/validator behind `type=` (`click.Choice`, `click.Path`, …),
  which also drives help text and shell completion.

## Primary workflow

Nearly every task is "declare a parameter" or "structure the commands". Start at
`references/parameters/INDEX.md` for anything on the parameter surface (it carries the
option-vs-argument decision), and at `references/commands/INDEX.md` for command/group
structure and state sharing.

## Inspecting a Click app

Click ships **no CLI of its own** — the artifact is the user's program. To learn what an
existing Click app does, run it (`mycli --help`, `mycli sub --help`) or drive it with
`click.testing.CliRunner` (`references/testing.md`) rather than reading its source. Do not
explore or list project files when `--help` already answers the question.

## Environment

`pip install click` into a virtualenv; no runtime dependencies (`colorama` on Windows
only). Install the CLI itself via an entry point — `python app.py` works but disables shell
completion and gives a misleading `prog_name`. See `references/packaging/INDEX.md`.

## CRITICAL: Always Read Reference Files Before Answering

NEVER answer from memory or guess at decorator keywords, parameter-resolution rules, type
constructor arguments, or `CliRunner` attributes. Click's flag/`default`/`flag_value`
semantics, its `CliRunner` output attributes, and several public names changed across 8.2,
8.3 and 8.4, so recalled answers are frequently wrong for this version. ALWAYS read the
relevant reference file(s) from the Reference Index below before responding. For every
question, identify which reference file(s) are relevant using the index descriptions, read
them, then answer based on what you read.

## Reference Index

<!-- BEGIN GENERATED INDEX -->

- [Errors, exceptions and exit codes](./references/errors-and-exit-codes.md) — reporting a user-facing error from a command without a traceback; choosing or explaining the exit code a CLI returns; aborting a command from inside a parameter callback; wrapping a Click command so exceptions propagate instead of exiting
- [Help pages and usage text](./references/help-pages.md) — customizing what --help prints for a command or group; help text is re-wrapped and the formatting is destroyed; adding -h as an alias for --help; documenting a positional argument that has no help= keyword
- [Public API surface (what exists in `click`)](./references/public-api.md) — checking whether a name is importable from click before using it; an import from click raises AttributeError or a DeprecationWarning; reviewing code that uses BaseCommand, MultiCommand, OptionParser or click.**version**
- [Quickstart — first command](./references/quickstart.md) — starting a new Python CLI from scratch and needing the canonical skeleton; adding Click to an existing project for the first time; the command name on the command line is not the name that was expected; deciding between print() and click.echo()
- [Shell completion (bash, zsh, fish)](./references/shell-completion.md) — adding tab completion to a CLI; pressing TAB suggests nothing for an installed command; suggesting dynamic values such as remote names or environment variables; supporting a shell Click does not ship support for
- [Testing a Click app with CliRunner](./references/testing.md) — writing tests for a command line application; asserting on the output or exit code of a CLI; feeding input to a prompt inside a test; output from a library or subprocess is missing from the captured result; result.stderr or result.output does not behave as it used to
- [Commands, groups and context](./references/commands/INDEX.md) — structuring a CLI with subcommands or nested subcommands; sharing configuration or a connection between a group and its subcommands; a group's own options are not visible to its subcommands; customizing how a group finds or lists its commands
- [Click ecosystem and extensions](./references/ecosystem/INDEX.md) — Click is missing a feature such as option groups, constraints or colored help; choosing between Click and Typer for a new CLI; adding a --config or --verbosity option without writing it from scratch; scaffolding a new CLI project
- [Upgrading across Click versions](./references/migration/INDEX.md) — behavior changed after upgrading Click; tests broke after a Click upgrade, especially around stderr or flags; a library must work with more than one Click version; deciding which Click version to require
- [Packaging and distributing a Click CLI](./references/packaging/INDEX.md) — turning a Click script into an installable command; the CLI should be runnable as a name, not as `python app.py`; shipping a CLI to users who do not have Python; setting up a development environment for a CLI project
- [Parameters — options and arguments](./references/parameters/INDEX.md) — adding an input to a command, choosing between an option and a positional argument; the function argument name does not match the declared flag; a parameter should be required, repeatable, or accept several values; validating or converting user input before the callback runs
- [Unicode, locales and stream encoding](./references/platform/unicode.md) — a CLI aborts with a RuntimeError about ASCII encoding under cron, systemd or SSH; filenames with non-ASCII bytes break a command; replacing sys.stdin or sys.stdout with StringIO does not work
- [Windows console behavior](./references/platform/windows.md) — a CLI prints garbage or loses characters on the Windows console; a quoted argument containing $, ~ or * is expanded unexpectedly on Windows; colored output works on Linux but not on Windows
- [Terminal output and utilities](./references/utils/INDEX.md) — printing output from a CLI, with or without color; showing progress for a long-running operation; paging long output, opening an editor, or launching a browser; finding the right place to store a config file for the app

<!-- END GENERATED INDEX -->
