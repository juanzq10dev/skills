---
title: Commands, groups and context
type: index
triggers:
  - "structuring a CLI with subcommands or nested subcommands"
  - "sharing configuration or a connection between a group and its subcommands"
  - "a group's own options are not visible to its subcommands"
  - "customizing how a group finds or lists its commands"
---

# Commands and groups

Docs: https://click.palletsprojects.com/en/stable/commands-and-groups/

`Command` wraps a function; `Group` is a `Command` that holds other commands; `Context`
carries per-invocation state and links parent to child.

## Choosing a structure — use the FIRST that applies

1. One job, no modes → a single `@click.command()`.
2. Several related jobs → `@click.group()` with `@cli.command()` subcommands.
3. Subcommands that must run **in sequence in one invocation** → `chain=True`
   (`chaining.md`).
4. Subcommands discovered at runtime (plugins, entry points, a directory) → a `Group`
   subclass overriding `get_command`/`list_commands` (`custom-classes.md`).
5. A large CLI whose imports are slow → the same subclass, loading lazily
   (`lazy-loading.md`).
6. Merging the commands of several independent groups → `CommandCollection`
   (`invoking.md`).

## Sharing state — use the FIRST that applies

1. The subcommand needs one object the group built → `ctx.obj` plus `@click.pass_obj`.
2. Several object types are in play, or a plugin may sit in between → `pass_repo =
click.make_pass_decorator(Repo)`, which searches up the context chain.
3. The subcommand needs the context itself (`ctx.invoke`, `ctx.exit`, `ctx.args`) →
   `@click.pass_context`.
4. Only a deeply nested helper needs it → `click.get_current_context()`.

Details and the resource-cleanup rules: `context.md`.

## Rules

- **Parameters do not inherit.** A group's options belong to the group; they must be
  written _before_ the subcommand name on the command line, and they are not passed to
  the subcommand's function. Share values through `ctx.obj`, not by redeclaring them.
- **A group callback runs whenever a subcommand runs** — put setup there, but nothing that
  should happen only for a bare invocation.
- **NEVER** call one command's function directly from another. Use `ctx.invoke` /
  `ctx.forward` (`invoking.md`), which handle `pass_context` correctly. Even that is
  discouraged: factor the shared work into a plain function instead.
- `no_args_is_help` defaults to `True` for `Group` and `False` for `Command`, and since 8.2
  the help it prints exits **2**, not 0 (`../errors-and-exit-codes.md`).
- `tool --help sub` is not `tool sub --help`; the first is the group's own help and exits
  before the subcommand is resolved.

<!-- BEGIN GENERATED INDEX -->

- [Command chaining and pipelines](./chaining.md) — running several subcommands in a single invocation, like `app validate build upload`; each subcommand should process the result of the previous one; post-processing all subcommand return values in one place; a chained group stopped parsing after a variadic argument
- [Context, `ctx.obj` and resource cleanup](./context.md) — passing a config object or database connection from a group to its subcommands; a subcommand needs a value that was parsed by its parent group; opening a connection in a group that subcommands must use and that must be closed; reaching the current context from a helper function; settings such as terminal width or token normalization should apply to a whole CLI
- [Custom `Group` subclasses, aliases and plugins](./custom-classes.md) — accepting an abbreviation or alias for a subcommand; discovering subcommands from a directory, entry points or a plugin registry; changing how a group lists or resolves its commands; applying shared behavior to every command in a CLI
- [Groups and nesting](./groups.md) — adding subcommands to a CLI; nesting subcommands more than one level deep; splitting commands across several Python modules; a group should do something when invoked without a subcommand; renaming a command or marking it deprecated
- [Invoking commands programmatically](./invoking.md) — calling one Click command from inside another; running a Click CLI from Python without letting it call sys.exit; using a command's return value; combining commands from two independent CLIs into one program
- [Lazily loading subcommands](./lazy-loading.md) — a CLI is slow to start because every subcommand's imports run up front; deferring a heavy import until the subcommand actually runs; understanding when a lazily loaded subcommand is actually imported

<!-- END GENERATED INDEX -->
