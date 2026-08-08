---
title: Click ecosystem and extensions
type: index
triggers:
  - "Click is missing a feature such as option groups, constraints or colored help"
  - "choosing between Click and Typer for a new CLI"
  - "adding a --config or --verbosity option without writing it from scratch"
  - "scaffolding a new CLI project"
---

# Ecosystem

Docs: https://click.palletsprojects.com/en/stable/contrib/

Click's maintainers deliberately keep experimental or hard-to-generalize features out of
core, and point at the [click-contrib](https://github.com/click-contrib/) organization and
the third-party projects below. Their quality and stability are **not** guaranteed by
Pallets.

## Choosing — use the FIRST that applies

1. The need is **option groups, mutual-exclusion constraints, command aliases, help
   themes or suggestions** → `cloup.md`. Do not hand-roll these; they are the single most
   commonly rebuilt wheel on top of Click.
2. The need is **`--config`, `--verbosity`, `--show-params`, colored help** on top of the
   above → `click-extra.md` (it builds on Cloup).
3. The need is only **prettier `--help`** → `rich-click.md`, which is a drop-in import
   swap.
4. Starting a **new** CLI and willing to drive the API from type hints → `typer.md`. It is
   built on Click, so this skill's concepts still apply underneath.
5. Starting a new project and wanting the packaging laid out → `click-app.md`.
6. None of the above → extend Click yourself (`../commands/custom-classes.md`).

## Rules

- **NEVER build a custom `Group` for option groups, constraints or themed help** when
  Cloup or Click Extra already ships it.
- Adding one of these is a dependency decision: they wrap Click's classes, so a Click
  upgrade can outpace them. Check the project's recent activity before adopting.
- Typer is a **different authoring API**, not a plugin — do not mix Typer and Click
  decorators in one command.

<!-- BEGIN GENERATED INDEX -->

- [click-app](./click-app.md) — scaffolding a new Click CLI project with packaging and tests already wired; looking for a project template for a command line tool
- [Click Extra](./click-extra.md) — adding a --config option that loads defaults from a file; adding a ready-made --verbosity or --show-params option; wanting Cloup's features plus colored help in one dependency
- [Cloup](./cloup.md) — grouping options into sections in the help page; declaring that two options are mutually exclusive or required together; adding command aliases or did-you-mean suggestions without subclassing Group
- [rich-click](./rich-click.md) — making --help output look better with panels, colors and tables; working in a codebase that imports rich_click as click
- [Typer](./typer.md) — building a CLI where parameters are declared with Python type hints; deciding whether to use Typer instead of Click directly; working in a codebase that imports typer

<!-- END GENERATED INDEX -->
