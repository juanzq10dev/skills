---
title: Context, `ctx.obj` and resource cleanup
triggers:
  - "passing a config object or database connection from a group to its subcommands"
  - "a subcommand needs a value that was parsed by its parent group"
  - "opening a connection in a group that subcommands must use and that must be closed"
  - "reaching the current context from a helper function"
  - "settings such as terminal width or token normalization should apply to a whole CLI"
---

# Context

Docs: https://click.palletsprojects.com/en/stable/commands/ and
https://click.palletsprojects.com/en/stable/complex/

A `Context` is created per command invocation and linked to its parent, forming a chain up
to the root. It holds parsed params, the shared `obj`, defaults, and resources to clean up.

## Sharing an object

```python
import click


class Repo:
    def __init__(self, home: str, debug: bool) -> None:
        self.home = home
        self.debug = debug


@click.group()
@click.option("--repo-home", envvar="REPO_HOME", default=".repo")
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx: click.Context, repo_home: str, debug: bool) -> None:
    ctx.obj = Repo(repo_home, debug)


pass_repo = click.make_pass_decorator(Repo)


@cli.command()
@pass_repo
def clone(repo: Repo) -> None:
    click.echo(repo.home)
```

| Decorator                             | Passes                          | Use when                                      |
| ------------------------------------- | ------------------------------- | --------------------------------------------- |
| `@click.pass_context`                 | the `Context`                   | you need `ctx.invoke`, `ctx.exit`, `ctx.args` |
| `@click.pass_obj`                     | `ctx.obj` verbatim              | exactly one object type, no intermediaries    |
| `make_pass_decorator(T)`              | the nearest `T` up the chain    | a plugin may set its own `ctx.obj`            |
| `make_pass_decorator(T, ensure=True)` | ditto, creating `T()` if absent | the command must also run standalone          |

`ensure=True` requires a no-argument constructor and may shadow an object set further up.
`ctx.ensure_object(dict)` is the same idea inline, and is the standard opener for a group
that may be called by means other than `cli(obj={})`.

`click.get_current_context()` reaches the context from a helper without threading it
through. It is **thread-local**: to use it in a spawned thread, enter the context there —
`with ctx: ...` — and treat it as read-only, since most of the context is not thread-safe.

## Resource cleanup

A `with` block in a group would close before the subcommand runs. Register with the context
instead:

```python
@click.group()
@click.option("--repo-home", default=".repo")
@click.pass_context
def cli(ctx: click.Context, repo_home: str) -> None:
    ctx.obj = ctx.with_resource(Repo(repo_home))     # Repo is a context manager
```

```python
@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.obj = db = open_db("repo.db")

    @ctx.call_on_close
    def close_db() -> None:
        db.save()
        db.close()
```

Since 8.2, `Context.close` runs on CLI exit, so both `with_resource` and `call_on_close`
now fire on exit — earlier versions did not call them.

## Context settings

Anything accepted by `Context.__init__` can be preset per command:

```python
CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 120,
    "token_normalize_func": str.lower,     # case-insensitive option and command names
    "ignore_unknown_options": True,
    "allow_extra_args": True,
    "default_map": {"runserver": {"port": 5000}},
    "auto_envvar_prefix": "MYAPP",
    "show_default": True,
}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None: ...
```

`token_normalize_func` normalizes option names, choice values and command names.
`allow_extra_args` puts leftovers in `ctx.args` (`../parameters/arguments.md`);
`ctx.protected_args` is deprecated and unnecessary.

Useful methods: `ctx.find_root()`, `ctx.find_object(T)`, `ctx.ensure_object(T)`,
`ctx.lookup_default(name)`, `ctx.get_parameter_source(name)`
(`../parameters/value-resolution.md`), `ctx.fail`/`ctx.abort`/`ctx.exit`
(`../errors-and-exit-codes.md`), `ctx.invoke`/`ctx.forward` (`invoking.md`).

## Common Anti-Patterns

- A module-level global for shared state → works, but breaks `CliRunner` isolation and
  nesting; use `ctx.obj`.
- `@click.pass_obj` when a plugin group sits in between → it hands you the plugin's object;
  use `make_pass_decorator(Repo)`.
- `ctx.obj["key"]` without `ctx.ensure_object(dict)` → `TypeError` when the group is
  invoked without `obj={}`.
- `with open_db() as db:` in a group callback → closed before the subcommand runs; use
  `ctx.with_resource`.
- Passing a `Context` to another thread and mutating it → read-only, and only inside
  `with ctx:`.
