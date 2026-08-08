---
title: Command chaining and pipelines
triggers:
  - "running several subcommands in a single invocation, like `app validate build upload`"
  - "each subcommand should process the result of the previous one"
  - "post-processing all subcommand return values in one place"
  - "a chained group stopped parsing after a variadic argument"
---

# Chaining and pipelines

Docs: https://click.palletsprojects.com/en/stable/commands/

```python
@click.group(chain=True)
def cli() -> None: ...


@cli.command("validate")
def validate() -> None:
    click.echo("validate")


@cli.command("build")
def build() -> None:
    click.echo("build")
```

```console
$ my-app validate build
validate
build
```

## Restrictions

- Only the **last** command may use `nargs=-1`; otherwise the parser cannot find the next
  command name.
- Groups **cannot** be nested below a chain group.
- Per command, options must come before that command's arguments.
- `ctx.invoked_subcommand` is `"*"` — the parser does not yet know the full list.

## Passing state along the chain

The direct way — a shared namespace object (`context.md`):

```python
pass_ns = click.make_pass_decorator(dict, ensure=True)


@click.group(chain=True)
@click.argument("name")
@pass_ns
def cli(ns: dict, name: str) -> None:
    ns["name"] = name


@cli.command
@pass_ns
def lower(ns: dict) -> None:
    ns["name"] = ns["name"].lower()


@cli.command
@pass_ns
def show(ns: dict) -> None:
    click.echo(ns["name"])
```

## Result callback

Each subcommand returns a value; `result_callback` receives the list of them plus the
group's own parameters:

```python
@click.group(chain=True, invoke_without_command=True)
@click.argument("fin", type=click.File("r"))
def cli(fin) -> None:
    pass


@cli.result_callback()
def process_pipeline(processors, fin) -> None:
    iterator = (line.rstrip("\r\n") for line in fin)
    for processor in processors:
        iterator = processor(iterator)
    for item in iterator:
        click.echo(item)


@cli.command("upper")
def make_uppercase():
    def processor(iterator):
        for line in iterator:
            yield line.upper()
    return processor
```

`invoke_without_command=True` is required, or an empty pipeline prints help instead of
running the callback.

**Files are already closed** by the time the result callback and the processors run — Click
closes the context after each callback. Take a `click.Path` and use `click.open_file`
inside the callback instead of a `click.File` parameter
(`../parameters/types/file.md`, `../utils/streams-and-paths.md`).

Outside chain mode, `result_callback` receives the single return value.

## Common Anti-Patterns

- `@cli.group()` under a `chain=True` group → not supported.
- A `click.File` parameter read inside a processor function → closed; open it manually.
- `nargs=-1` on a non-final chained command → the parser stops finding commands.
- Reaching for chaining when the commands are independent → plain subcommands invoked twice
  are simpler and compose better with shell tooling.
