---
title: Where a parameter value comes from
triggers:
  - "reading option values from environment variables"
  - "loading CLI defaults from a configuration file"
  - "checking whether the user actually passed a value or a default was used"
  - "two parameters share a name and the wrong one wins"
  - "an environment variable is set but the default is used anyway"
---

# Value resolution

Docs: https://click.palletsprojects.com/en/stable/options/ and
https://click.palletsprojects.com/en/stable/commands-and-groups/

## Source precedence

The first source that produces a value wins:

1. **Command line** — `ParameterSource.COMMANDLINE`
2. **Environment variable** — `ENVIRONMENT` (`envvar=` or `auto_envvar_prefix`)
3. **`Context.default_map`** — `DEFAULT_MAP`
4. **Parameter `default`** — `DEFAULT`

If nothing explicit was found and the option declares `prompt=`, Click prompts and records
`ParameterSource.PROMPT`, which outranks all four for arbitration (`prompting.md`).

`ParameterSource` is an `IntEnum` ordered most- to least-explicit (8.3.3+), so it compares:

```python
source = ctx.get_parameter_source("port")
if source < click.ParameterSource.DEFAULT_MAP:
    ...  # explicitly provided: prompt, command line or environment
```

```python
@click.command()
@click.argument("port", nargs=1, default=8080, envvar="PORT")
@click.pass_context
def cli(ctx: click.Context, port: int) -> None:
    click.echo(f"Port came from {ctx.get_parameter_source('port').name}")
```

## Environment variables

```python
@click.option("--username", envvar="USERNAME")
@click.option("--username", envvar=["ALT_USERNAME", "USERNAME"])   # first found wins
```

Names are matched exactly, not stripped of whitespace, and are case-insensitive only on
Windows. For `multiple=True` or `nargs > 1`, the string is split by
`ParamType.split_envvar_value` — whitespace for most types, but `os.pathsep` (`:` on Unix,
`;` on Windows) for `File` and `Path`. Flag parsing rules are in `flags.md`; arguments only
honour explicitly named variables (`arguments.md`).

`auto_envvar_prefix` derives names automatically, and is passed **at invocation**:

```python
if __name__ == "__main__":
    cli(auto_envvar_prefix="GREETER")
```

The name is `PREFIX_COMMAND_PARAM`, uppercased with `_` separators, and the command segment
is included for subcommands: prefix `WEB` + command `run-server` + option `host` →
`WEB_RUN_SERVER_HOST`. Options only — never arguments.

## `default_map` (config files)

```python
if __name__ == "__main__":
    cli(default_map={"runserver": {"port": 5000}})
```

Nest one level per subcommand. Set it in the decorator instead when it is static:
`@click.group(context_settings={"default_map": {...}})`. A top-level command can also
assign `ctx.default_map` after loading a config file.

A string value for a parameter with `nargs > 1` or a `Tuple` type is **split** like an
environment variable (8.4.0+); pass an already-structured tuple to skip splitting.

```python
default_map = {"draw": {"point": "3 4", "color": "red"}}   # point -> ("3", "4")
default_map = {"draw": {"point": (3, 4)}}                  # used as-is
```

`Sentinel.UNSET` in an environment variable or a `default_map` entry is treated as absent
and falls through to the next source, rather than being delivered as a value.

## Shared-name arbitration

When several parameters resolve to the same name (a feature switch group), one wins:

1. **Most explicit source wins**, regardless of declaration order.
2. Within the default tier, an **explicit `default=` keyword beats an auto-derived** default.
3. Otherwise **the last declared** parameter keeps the slot.

Rule 3 reverted the 8.3.x first-wins behavior; rules 1 and 2 are new in 8.4.0
(`../migration/to-8-4.md`).

## Common Anti-Patterns

- `os.environ.get("MYAPP_PORT")` inside the callback → declare `envvar=`; you then get the
  right precedence, `show_envvar=True` help, and the error hint.
- Reading a config file and merging it by hand → set `ctx.default_map`.
- `if port == 8080:` to detect "user did not pass it" → `ctx.get_parameter_source("port")`.
- Expecting `auto_envvar_prefix` to be a decorator keyword → it is passed when the command
  is invoked, or via `context_settings`.
- Expecting `auto_envvar_prefix` to fill an `Argument` → options only.
