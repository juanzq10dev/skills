---
title: Parameters — options and arguments
type: index
triggers:
  - "adding an input to a command, choosing between an option and a positional argument"
  - "the function argument name does not match the declared flag"
  - "a parameter should be required, repeatable, or accept several values"
  - "validating or converting user input before the callback runs"
---

# Parameters

Docs: https://click.palletsprojects.com/en/stable/parameters/

Click has exactly two parameter kinds, by design: **Option** (`--name`, optional,
self-documenting) and **Argument** (positional, documented by hand).

## Choosing the kind — use the FIRST that applies

1. It names a **subcommand** → it is not a parameter at all; make it a `Group`
   (`../commands/INDEX.md`).
2. It is the **thing the command acts on** — a file, a path, a URL, a source/destination
   pair → `@click.argument`, and make it `required` (the default).
3. Anything else → `@click.option`. This is the default answer.

Click's own design guidance: positional arguments should be used **sparingly** and, when
used, should be required. Each extra positional makes the invocation harder to read, and
optional or variadic positionals are filled left-to-right in a way users cannot see.

## Non-negotiable rules

- **NEVER** pass `help=` to `@click.argument` — it does not accept one. Document arguments
  in the command docstring (`../help-pages.md`).
- **NEVER** rely on the inferred function-parameter name when the decls are unusual. Pass
  the destination explicitly: `@click.option("-f", "--filename", "dest")`.
- **ALWAYS** prefer a `type=` over hand-validating in the callback body. A type gives you
  the error message, the help text and shell completion for free
  (`types/INDEX.md`).
- **ALWAYS** prefer `--x/--no-x` over a single flag with `flag_value=False, default=True`
  (`flags.md`).
- Do **not** combine `prompt=` with `multiple=True`; prompt inside the function instead
  (`prompting.md`).
- Two parameters resolving to the same name is a feature switch group, not a mistake — but
  it warns (`UserWarning`) unless deliberate. Read `value-resolution.md` before doing it.

## Name inference

Without an explicit destination, Click picks a declaration and normalizes it: lowercase,
strip a leading `-`/`--`, remaining `-` → `_`.

1. A decl that is already a valid Python identifier (no dashes) wins.
2. Otherwise the **first** decl prefixed with `--`.
3. Otherwise the first decl prefixed with `-`.

| Decls                        | Function parameter |
| ---------------------------- | ------------------ |
| `"-f", "--foo-bar"`          | `foo_bar`          |
| `"-x"`                       | `x`                |
| `"-f", "--filename", "dest"` | `dest`             |
| `"--CamelCase"`              | `camelcase`        |
| `"-f", "-fb"`                | `f`                |

## Where to go next

<!-- BEGIN GENERATED INDEX -->

- [Arguments (`@click.argument`)](./arguments.md) — declaring a positional input such as a filename or source/destination pair; a command should accept an arbitrary number of trailing values; a filename that starts with a dash is parsed as an option; forwarding unrecognized flags through to another program; documenting a positional parameter that has no help keyword
- [Parameter callbacks, validation and eagerness](./callbacks.md) — validating a value beyond what a type can express; a flag should print something and exit immediately, like --version; a parameter should not be passed to the command function; one parameter's default should depend on another parameter; the order in which parameter callbacks run matters
- [Boolean flags and feature switches](./flags.md) — adding an on/off switch to a command; a flag should have an explicit --no- counterpart; several flags should write to the same variable, like --upper / --lower; a flag receives an unexpected value when it is not passed; a flag is controlled by an environment variable and the truthiness is wrong
- [Options (`@click.option`)](./options.md) — declaring a --flag that takes a value; an option should accept several values or be repeatable; combining short options like -abc or -vn5 on the command line; making an option required, hidden or deprecated; an option's value should be optional after the flag itself
- [Prompting for input](./prompting.md) — asking the user for a value that was not supplied on the command line; reading a password without echoing it; asking for yes/no confirmation before a destructive action; a prompt should offer a default computed at runtime; a prompt should appear only when the flag is given without a value
- [Shortcut decorators (`--password`, `--yes`, `--version`, `--help`)](./shortcut-decorators.md) — adding a --version flag to a CLI; asking for confirmation before a destructive command; adding a password prompt with confirmation; version_option raises RuntimeError about not finding the package
- [Where a parameter value comes from](./value-resolution.md) — reading option values from environment variables; loading CLI defaults from a configuration file; checking whether the user actually passed a value or a default was used; two parameters share a name and the wrong one wins; an environment variable is set but the default is used anyway
- [Parameter types (`type=`)](./types/INDEX.md) — choosing what to pass as type= on an option or argument; restricting a value to a fixed set, a numeric range, or an existing file; converting user input into a domain object; the help page should advertise the accepted values

<!-- END GENERATED INDEX -->
