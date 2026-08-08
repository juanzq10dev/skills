---
title: Unicode, locales and stream encoding
triggers:
  - "a CLI aborts with a RuntimeError about ASCII encoding under cron, systemd or SSH"
  - "filenames with non-ASCII bytes break a command"
  - "replacing sys.stdin or sys.stdout with StringIO does not work"
---

# Unicode and locales

Docs: https://click.palletsprojects.com/en/stable/unicode-support/

## The locale abort

Click refuses to run when Python reports ASCII as the environment encoding, because it
cannot repair the interpreter's state after the fact:

```
RuntimeError: Click will abort further execution because Python was
  configured to use ASCII as encoding for the environment.
```

This bites CLIs launched by init systems, deployment tools and cron. Export a UTF-8 locale
**before** the interpreter starts:

```bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
```

Use a regional locale (`en_US.utf-8`, `de_DE.utf-8`) where `C.UTF-8` is unavailable;
`locale -a` lists what the system has. PEP 538/540 make this rare on modern Python, but a
misconfigured locale is still a misconfigured locale.

## Streams

`sys.stdin`/`sys.stdout`/`sys.stderr` are text by default; Click rediscovers the underlying
binary stream when it needs bytes. Replacing them with `io.StringIO` is **not supported**:

```python
import io
import sys

in_stream = io.BytesIO("Input here".encode())
sys.stdin = io.TextIOWrapper(in_stream, encoding="utf-8")
out_stream = io.BytesIO()
sys.stdout = io.TextIOWrapper(out_stream, encoding="utf-8")
# read results from out_stream.getvalue(), not sys.stdout.getvalue()
```

In tests, use `CliRunner` instead of doing any of this (`../testing.md`).

Prefer `click.get_text_stream("stdin")` / `click.get_binary_stream("stdout")` over touching
`sys.*` directly (`../utils/streams-and-paths.md`).

## Filenames

`sys.argv` is always text, so undecodable bytes arrive as surrogate escapes. Click uses the
OS filesystem encoding and supports surrogates, so `click.File` and `click.Path` still open
such files. Render them with `click.format_filename`, which never raises.

## Common Anti-Patterns

- Setting the locale from inside the Python process (`os.environ["LANG"] = ...`) → too
  late; Python already chose its encoding.
- `str(path_bytes)` in an error message → `click.format_filename(path_bytes)`.
- Catching the locale `RuntimeError` and continuing → the encoding is already wrong.
