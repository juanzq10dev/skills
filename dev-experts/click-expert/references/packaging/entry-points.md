---
title: Entry points and `project.scripts`
triggers:
  - "making a Click command installable as an executable name"
  - "writing the pyproject.toml for a CLI project"
  - "the installed command is not on PATH after installing"
  - "shipping several executables from one package"
---

# Entry points

Docs: https://click.palletsprojects.com/en/stable/entry-points/

```text
hello-project/
    src/
        hello/
            __init__.py
            hello.py
    pyproject.toml
```

```python
# src/hello/hello.py
import click


@click.command()
def cli() -> None:
    """Prints a greeting."""
    click.echo("Hello, World!")
```

```toml
[project]
name = "hello"
version = "1.0.0"
description = "Hello CLI"
requires-python = ">=3.11"
dependencies = ["click>=8.1"]

[project.scripts]
hello = "hello.hello:cli"

[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

`[project.scripts]` maps **executable name** → `import.path:callable`. Add one line per
executable. The installer generates the wrapper for every OS, so the command works on
Windows and inside a non-activated virtualenv.

```console
$ python -m venv .venv
$ . .venv/bin/activate
$ pip install -e .
$ hello
Hello, World!
```

`-e` (editable) keeps the wrapper pointing at the source tree, so code edits take effect
without reinstalling — but **adding or renaming an entry point requires reinstalling**.

Any PEP 517 backend works (`flit_core`, `hatchling`, `setuptools`); Click's own docs use
`flit_core`. The legacy `setup.py` `entry_points={"console_scripts": [...]}` form is
equivalent and still supported.

## Common Anti-Patterns

- `hello = "hello.hello:cli()"` → drop the parentheses; the target is the object, not a
  call.
- Pointing at a wrapper function that calls `cli()` → point at `cli` directly, so
  `standalone_mode` and `prog_name` behave.
- Installing with `pip install .` during development → use `-e`.
- Adding a new `[project.scripts]` entry and expecting it to appear → reinstall.
- Assuming shell completion works from `python -m hello` → it needs the executable
  (`../shell-completion.md`).
