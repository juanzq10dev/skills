---
title: Parameter types (`type=`)
type: index
triggers:
  - "choosing what to pass as type= on an option or argument"
  - "restricting a value to a fixed set, a numeric range, or an existing file"
  - "converting user input into a domain object"
  - "the help page should advertise the accepted values"
---

# Parameter types

Docs: https://click.palletsprojects.com/en/stable/parameter-types/

A `ParamType` does four jobs at once: converts the string, produces the error message,
labels the help page, and drives shell completion. That is why a type beats validating in
the command body.

## Choosing a type — use the FIRST that applies

1. A **fixed set of values** → `Choice` (pass an `Enum` directly for typed values).
2. A **filesystem path you will open immediately** → `File`; a path you will inspect,
   create, or hand to another library → `Path`.
3. A **bounded number** → `IntRange` / `FloatRange`.
4. A **timestamp** → `DateTime`; a UUID → `click.UUID`.
5. **Several values of different types in one flag** → a tuple literal, e.g.
   `type=(str, int)`.
6. The value must reach the function **untouched** (passthrough args, arbitrary objects) →
   `click.UNPROCESSED`.
7. A **domain object** or any custom parsing → subclass `ParamType`.
8. Otherwise pass the plain Python callable `str`, `int`, `float`, `bool` — or nothing at
   all and let Click infer from `default`.

## Rules

- **NEVER** write a `ParamType` for something the built-ins already cover — `Path(exists=True)`
  replaces an `os.path.exists` check, and its error message is better than yours.
- **NEVER** pass a bare function as a type when a `ParamType` subclass is practical. Click
  supports "a callable that raises `ValueError`", but explicitly discourages it: no `name`,
  no completion, worse errors.
- **ALWAYS** make `convert` idempotent — it also sees defaults and Python-supplied values,
  which may already be the target type.
- Built-in singletons are `click.STRING`, `click.INT`, `click.FLOAT`, `click.BOOL`,
  `click.UUID`, `click.UNPROCESSED`. `BOOL` accepts `1/true/t/yes/y/on` and
  `0/false/f/no/n/off`.

## Typing (8.4.0+)

`ParamType` is a **generic abstract base class** parameterized by the converted value type,
and `Choice` is generic over its choice type. Write `ParamType[int]`, `Choice[HashType]`,
`Choice[str]` so `convert`'s return type flows to consumers.

<!-- BEGIN GENERATED INDEX -->

- [`click.Choice`](./choice.md) — restricting an option to a fixed list of allowed values; using a Python Enum as the set of accepted CLI values; accepting a choice case-insensitively; customizing the message shown for an invalid choice
- [Writing a custom `ParamType`](./custom-types.md) — converting a command line string into a domain object; reusing one validation rule across several commands; a custom type needs to offer its own shell completion suggestions; a ParamType subclass breaks after upgrading Click
- [`click.File`](./file.md) — a command reads from a file or from stdin interchangeably; writing output to a file or to stdout with the same parameter; a file handle is already closed when the code tries to use it; an output file is truncated even though the command failed later
- [`click.Path`](./path.md) — a parameter takes a file or directory path; the CLI should fail early when a path does not exist; restricting a parameter to a directory, or to a writable location; receiving a pathlib.Path instead of a string
- [`IntRange` and `FloatRange`](./ranges.md) — constraining a numeric option to a minimum, a maximum, or both; an out-of-range value should be silently clamped instead of rejected; an upper or lower bound should be exclusive
- [Tuples, `DateTime`, `UUID` and `UNPROCESSED`](./tuple-and-multiple.md) — one flag should take several values of different types; parsing a date or timestamp argument; a value must reach the function without any string conversion; accepting a UUID on the command line

<!-- END GENERATED INDEX -->
