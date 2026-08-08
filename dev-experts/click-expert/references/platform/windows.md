---
title: Windows console behavior
triggers:
  - "a CLI prints garbage or loses characters on the Windows console"
  - "a quoted argument containing $, ~ or * is expanded unexpectedly on Windows"
  - "colored output works on Linux but not on Windows"
---

# Windows console

Docs: https://click.palletsprojects.com/en/stable/wincmd/ and
https://click.palletsprojects.com/en/stable/faqs/

Click emulates the output stream on Windows, dispatching to the cmd.exe Unicode APIs when a
console is attached (internally `utf-16-le`) and behaving like any other platform when
output is redirected.

- Unicode support covers `click.echo`, `click.prompt` and `click.get_text_stream` **only**.
  `print` is not covered, and because the raw stream is switched to binary mode globally,
  mixing `print` with `click.echo` can reorder output. Use `click.echo` throughout.
- Colors work through `colorama`, which Click uses without requiring `colorama.init()`.
- The default console fonts cover international letters but not emoji.
- Windows 7 and below cannot write more than 64k characters per binary-mode call; Click
  wraps `sys.stdout`/`sys.stderr` to work around it.
- Unicode parameters are extracted from `sys.argv` directly. If `sys.argv` was modified
  before Click ran, only the code-page subset is available.

## Argument expansion

The Windows shell performs no `*`, `~` or `$ENV` expansion and does not distinguish single
from double quotes. Click emulates the Unix behavior so apps act the same on both
platforms — which means `'$M0/path'` **is** expanded even though the user quoted it.

Turn it off when the app must receive arguments verbatim:

```python
if __name__ == "__main__":
    main(windows_expand_args=False)
```

## Common Anti-Patterns

- Calling `colorama.init()` before a Click app → unnecessary, and it can double-wrap the
  stream.
- Assuming `capture="fd"` works in tests on Windows → it does not (`../testing.md`).
- Reporting mangled output without first replacing every `print` with `click.echo`.
