---
title: `click.Path`
triggers:
  - "a parameter takes a file or directory path"
  - "the CLI should fail early when a path does not exist"
  - "restricting a parameter to a directory, or to a writable location"
  - "receiving a pathlib.Path instead of a string"
---

# Path

Docs: https://click.palletsprojects.com/en/stable/handling-files/

`Path(exists=False, file_okay=True, dir_okay=True, writable=False, readable=True,
resolve_path=False, allow_dash=False, path_type=None, executable=False)`

Use `Path` when the command inspects, creates, or hands the path to another library. Use
`File` when the command just reads or writes it (`file.md`).

```python
@click.command()
@click.argument("src", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.argument("dst", type=click.Path(file_okay=False, writable=True))
def copy(src: str, dst: str) -> None: ...
```

| Keyword                                | Effect                                                         |
| -------------------------------------- | -------------------------------------------------------------- |
| `exists=True`                          | fail if the path is missing (checked before the callback runs) |
| `file_okay=False`                      | directories only                                               |
| `dir_okay=False`                       | files only                                                     |
| `readable` / `writable` / `executable` | permission checks                                              |
| `resolve_path=True`                    | make absolute and resolve symlinks                             |
| `allow_dash=True`                      | accept `-` as a value (pair with `click.open_file`)            |
| `path_type=pathlib.Path`               | deliver that type instead of `str`                             |

```python
import pathlib

@click.option("--out", type=click.Path(dir_okay=False, path_type=pathlib.Path))
def cli(out: pathlib.Path) -> None: ...
```

Error messages run through `click.format_filename`, so undecodable bytes print safely
(`../../platform/unicode.md`). `Path` splits environment-variable values on `os.pathsep`
rather than whitespace (`../value-resolution.md`).

## Common Anti-Patterns

- `type=str` then `if not os.path.exists(p): raise` → `Path(exists=True)`; the error
  arrives as a usage error with the parameter name.
- `Path(exists=True)` on an output path → the file will not exist yet; use
  `file_okay=..., writable=True` instead.
- `pathlib.Path(value)` inside the function → `path_type=pathlib.Path`.
- Using `Path` and then `open()` for a plain read/write → `click.File` handles `-`, lazy
  opening, encodings and atomic writes (`file.md`).
