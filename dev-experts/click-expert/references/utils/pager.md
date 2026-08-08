---
title: Paging long output
triggers:
  - "output is longer than a screen and should scroll like `git log`"
  - "the pager shows nothing until the command finishes"
  - "writing to a pager from code that cannot produce one iterable"
  - "an I/O operation on closed file error after paging"
---

# Pager

Docs: https://click.palletsprojects.com/en/stable/utils/

Always writes to stdout, through a pager when one is available.

```python
click.echo_via_pager("\n".join(f"Line {i}" for i in range(200)))
```

For large or slow output, pass a **generator** (or a generator function) so the pager
streams instead of waiting for the whole string:

```python
def _generate_output():
    for i in range(50_000):
        yield f"Line {i}\n"


@click.command()
def less() -> None:
    click.echo_via_pager(_generate_output())
```

When the text cannot be expressed as one iterable, take the file object instead
(`get_pager_file`, added in 8.4.0):

```python
@click.command()
def less() -> None:
    with click.get_pager_file() as pager:
        for i in range(50_000):
            print(i, file=pager)
```

Behavior worth knowing:

- Since 8.4.2, `echo_via_pager` flushes after each write, so a generator streams
  incrementally rather than staying hidden until the pipe buffer fills.
- `echo_via_pager` and `get_pager_file` no longer close a borrowed stdout when no external
  pager runs (fixing `ValueError: I/O operation on closed file`, 8.4.2).
- The pager command is split with `shlex.split` and run without a shell (8.3.3), so
  `PAGER="less -R"` keeps its arguments.
- `KeyboardInterrupt` is **not** swallowed (8.2+): Ctrl-C aborts the program while the
  pager is open, as expected.

## Common Anti-Patterns

- `subprocess.run(["less"], input=text)` → `echo_via_pager` handles the missing-pager case,
  Windows, and cleanup.
- Building a multi-megabyte string then paging it → pass a generator.
- Assuming color survives → pass `color=True` to keep ANSI codes for a pager that renders
  them.
