---
title: `click.File`
triggers:
  - "a command reads from a file or from stdin interchangeably"
  - "writing output to a file or to stdout with the same parameter"
  - "a file handle is already closed when the code tries to use it"
  - "an output file is truncated even though the command failed later"
---

# File

Docs: https://click.palletsprojects.com/en/stable/handling-files/

`File(mode="r", encoding=None, errors="strict", lazy=None, atomic=False)` — delivers an
open file object, and treats `-` as stdin (reading) or stdout (writing).

```python
@click.command()
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def inout(input, output) -> None:
    """Copy INPUT to OUTPUT. Either may be '-'."""
    while chunk := input.read(1024):
        output.write(chunk)
```

## Opening behavior

- Files opened for **reading**, and the standard streams, open immediately — the user gets
  an error before the command body runs.
- Files opened for **writing** open lazily, on the first IO operation, so a command that
  fails during argument parsing does not truncate the target.
- `lazy=True` forces lazy mode; failures then surface as `FileError` at first IO. Only
  disable laziness on a write handle when truncation-on-open is genuinely intended.
- `atomic=True` writes to a sibling temp file and moves it into place on completion — use
  it when other processes read the file while it is being rewritten.

## Lifetime

Click closes the context — and the files it opened — after each command callback returns.
In a **chained group**, the result-callback and any processor functions run after that
point, so a `File` parameter is already closed there. Open those manually with
`click.open_file` (`../../utils/streams-and-paths.md`, `../../commands/chaining.md`).

## Common Anti-Patterns

- `open(filename)` in the command body → loses `-` support, the early error, and the
  encoding handling.
- `type=click.File("w")` for a path you only want to validate → use `Path`
  (`path.md`); `File` will create the file.
- Returning a `File` handle from a chained subcommand for later use → it is closed by then.
- `type=click.File("r")` plus `.read()` on a large input when streaming would do → iterate
  the handle.
