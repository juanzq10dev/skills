---
title: Streams, file opening and app directories
triggers:
  - "opening a file where `-` should mean stdin or stdout"
  - "needing a binary stream when stdout is text"
  - "deciding where to store a config file for the application"
  - "printing a filename that may contain undecodable bytes"
  - "opening a file outside the parameter-parsing phase"
---

# Streams, files and app dirs

Docs: https://click.palletsprojects.com/en/stable/utils/

## `click.open_file`

The logic behind `click.File`, exposed for use anywhere — including places where a `File`
parameter would already be closed, such as a chained group's result callback
(`../commands/chaining.md`).

```python
with click.open_file(filename, "w") as f:
    f.write("Hello World!\n")
```

`open_file(filename, mode="r", encoding=None, errors="strict", lazy=False, atomic=False)`.
`-` means stdin (read) or stdout (write); the standard streams come back wrapped so the
`with` block does **not** close them, making the two cases interchangeable.

## Standard streams

```python
stdin_text = click.get_text_stream("stdin")
stdout_binary = click.get_binary_stream("stdout")
```

Consistent across platforms and terminal configurations, and correct on the Windows
console — unlike touching `sys.stdout` directly (`../platform/windows.md`).

## `click.get_app_dir`

```python
import configparser
import os

cfg = os.path.join(click.get_app_dir("My Application"), "config.ini")
parser = configparser.RawConfigParser()
parser.read([cfg])
```

`get_app_dir(app_name, roaming=True, force_posix=False)` returns the conventional per-user
config location for the OS. Pair it with `default_map` to make the file supply CLI defaults
(`../parameters/value-resolution.md`).

## `click.format_filename`

Best-effort conversion of a filename to text; never raises, so it is safe in error
messages.

```python
click.echo(f"Path: {click.format_filename(b'foo.txt')}")
```

`format_filename(filename, shorten=False)`.

## Common Anti-Patterns

- `open(path)` in a command that documents `-` as stdin → `click.open_file`.
- `os.path.expanduser("~/.myapp")` → `click.get_app_dir("myapp")`, which is right on
  Windows and macOS too.
- `sys.stdout.buffer` for binary output → `click.get_binary_stream("stdout")`.
- `str(filename)` in an error message → `click.format_filename(filename)`.
