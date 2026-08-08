---
title: Packaging and distributing a Click CLI
type: index
triggers:
  - "turning a Click script into an installable command"
  - "the CLI should be runnable as a name, not as `python app.py`"
  - "shipping a CLI to users who do not have Python"
  - "setting up a development environment for a CLI project"
---

# Packaging

Docs: https://click.palletsprojects.com/en/stable/entry-points/

Click's documentation assumes the app is distributed as a package with an entry point.
That is not cosmetic: **shell completion only works through an installed executable**
(`../shell-completion.md`), the entry-point wrapper is what makes the CLI work on Windows
and inside a non-activated virtualenv, and `prog_name` in help and errors is derived from
it.

## Choosing a distribution route — use the FIRST that applies

1. Users have Python and install with pip/uv/pipx → a wheel with `[project.scripts]`
   (`entry-points.md`). This is the default answer.
2. Users must not need Python at all → a native bundle with Briefcase
   (`briefcase.md`).
3. Only you run it, during development → `pip install -e .` inside a virtualenv
   (`virtualenv.md`) — still an entry point, just editable.

## Rules

- **ALWAYS** develop inside a virtualenv, and **ALWAYS** install the project itself
  (`pip install -e .`) rather than running the module path directly.
- **NEVER** document `python app.py` as the user-facing invocation.
- Keep the `if __name__ == "__main__": cli()` block if you like — it is harmless — but the
  entry point is the contract.
- `[project.scripts]` maps `name = "import.path:callable"`; the callable is the Click
  command or group object, not a wrapper function.

<!-- BEGIN GENERATED INDEX -->

- [Standalone native builds with Briefcase](./briefcase.md) — shipping a CLI to users who do not have Python installed; producing a .msi, .pkg, .deb or .rpm installer for a command line tool; the packaged app fails to start with no obvious error
- [Entry points and `project.scripts`](./entry-points.md) — making a Click command installable as an executable name; writing the pyproject.toml for a CLI project; the installed command is not on PATH after installing; shipping several executables from one package
- [Virtual environments for CLI development](./virtualenv.md) — setting up a fresh project to build a Click CLI; installing Click without touching the system Python; the installed command is not found after installing the project

<!-- END GENERATED INDEX -->
