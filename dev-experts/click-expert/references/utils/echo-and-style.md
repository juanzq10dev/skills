---
title: `echo`, `secho` and `style`
triggers:
  - "printing output from a Click command"
  - "adding color or bold to terminal output"
  - "writing a message to stderr instead of stdout"
  - "colors leak as escape codes into a redirected file or log"
  - "printing bytes rather than text"
---

# echo and style

Docs: https://click.palletsprojects.com/en/stable/utils/

```python
click.echo("Hello World!")
click.echo("something went wrong", err=True)   # stderr
click.echo("no newline", nl=False)
click.echo(b"\xe2\x98\x83", nl=False)          # bytes are fine
```

`echo(message=None, file=None, nl=True, err=False, color=None)`. It writes through Click's
own streams, so Unicode works on the Windows console and ANSI codes are stripped when the
target is not a terminal. `color=True` forces codes through anyway (for a pager, or a CI
log that renders them); `color=False` always strips.

## Styling

```python
click.echo(click.style("Hello World!", fg="green"))
click.secho("Some more text", bg="blue", fg="white")
click.secho("ATTENTION", blink=True, bold=True)
```

`secho` is `echo` + `style` in one call and takes the same style keywords.

`style(text, fg=None, bg=None, bold=None, dim=None, underline=None, overline=None,
italic=None, blink=None, reverse=None, strikethrough=None, reset=True)`

Color names: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`,
`reset`, and the `bright_*` variants of the first eight. `fg`/`bg` also accept a 256-color
integer or an `(r, g, b)` tuple.

`click.unstyle(text)` removes the codes from an already-styled string.

`reset=False` leaves the style open so several `style` calls can be concatenated; the last
one should reset.

On Windows this goes through `colorama`, without needing `colorama.init()`.

## Common Anti-Patterns

- `print(f"\033[32m{msg}\033[0m")` → `click.secho(msg, fg="green")`; the escape codes are
  stripped automatically when output is redirected.
- Progress or status messages on stdout → `err=True`, so `mycli > out.txt` captures only
  the real output.
- `sys.stderr.write(msg + "\n")` → `click.echo(msg, err=True)`.
- Styling a string that will be compared in a test → style at the edge, assert on the
  unstyled value (`CliRunner` invokes with `color=False` by default).
