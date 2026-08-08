---
title: Editors, launching apps, and raw terminal input
triggers:
  - "asking the user for multi-line input, like a commit message"
  - "opening a file in the user's editor from a command"
  - "opening a URL or a file in the system's default application"
  - "reading a single keypress without waiting for Enter"
  - "pausing until the user presses a key"
---

# Editor, launch, raw input

Docs: https://click.palletsprojects.com/en/stable/utils/

## `click.edit`

Opens `$VISUAL`/`$EDITOR` (or a sensible fallback). Returns the edited text, or `None` if
the user quit without saving.

```python
def get_commit_message() -> str | None:
    MARKER = "# Everything below is ignored\n"
    message = click.edit("\n\n" + MARKER)
    if message is not None:
        return message.split(MARKER, 1)[0].rstrip("\n")
    return None
```

`edit(text=None, editor=None, env=None, require_save=True, extension=".txt",
filename=None)`. Passing `filename` edits files in place and always returns `None`; since
8.2 it accepts an iterable of filenames for editors that open several at once. Passing
`bytes` as `text` defaults `require_save` to `False` and returns `bytes`.

The editor command is split with `shlex.split` and run without a shell (8.3.3).

## `click.launch`

```python
click.launch("https://click.palletsprojects.com/")
click.launch("/my/downloaded/file.txt", locate=True)   # reveal in the file manager
```

`launch(url, wait=False, locate=False)`. On Windows this uses `os.startfile` (8.4.0), which
also fixed paths containing spaces (8.4.1).

## Raw terminal input

```python
click.echo("Continue? [yn] ", nl=False)
c = click.getchar()
click.echo()
```

`getchar(echo=False)` reads one character, **always from the terminal** even when stdin is
a pipe. Arrow keys arrive as the platform's raw escape sequence; only `^C` and `^D` are
translated, into `KeyboardInterrupt` and `EOFError`.

`click.pause(info=None, err=False)` waits for any key, and is a no-op when not interactive —
useful because `cmd.exe` closes its window when a command finishes.

`click.clear()` clears the screen portably.

## Common Anti-Patterns

- `os.system(f"$EDITOR {path}")` → `click.edit(filename=path)`; no shell, works on Windows.
- `webbrowser.open` for a local file → `click.launch` handles files, URLs and `locate`.
- `click.getchar()` in a test → it reads the terminal, not `CliRunner`'s `input`; use a
  prompt instead (`../parameters/prompting.md`).
- `input("Press enter…")` in a script that may run non-interactively → `click.pause()`
  becomes a no-op there.
