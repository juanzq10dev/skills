---
title: Terminal output and utilities
type: index
triggers:
  - "printing output from a CLI, with or without color"
  - "showing progress for a long-running operation"
  - "paging long output, opening an editor, or launching a browser"
  - "finding the right place to store a config file for the app"
---

# Terminal utilities

Docs: https://click.palletsprojects.com/en/stable/utils/

Click's non-parsing helpers. All are exported from the top-level `click` package.

## Rules

- **ALWAYS use `click.echo` instead of `print`.** It strips ANSI codes when the stream is
  not a terminal, routes through the Windows console APIs, and does not die on a
  misconfigured locale (`../platform/windows.md`, `../platform/unicode.md`).
- **Errors and diagnostics go to stderr:** `click.echo(msg, err=True)`. Only the command's
  actual output belongs on stdout, so the CLI stays pipeable.
- **NEVER hand-write ANSI escape sequences.** `click.style` / `click.secho` emit them and
  Click removes them when the output is redirected; a hardcoded escape survives into log
  files.
- **NEVER guess a config path.** `click.get_app_dir(name)` gives the per-OS location.
- Reach for a third-party library when Click's helper is not enough — the docs point at
  `tqdm` for richer progress bars and `rich-click` for styled help
  (`../ecosystem/INDEX.md`).

## Picking the output helper

1. One line of output → `click.echo`.
2. Colored or styled → `click.secho`, or `click.style` when composing a longer string.
3. Output longer than a screen → `click.echo_via_pager`, or `click.get_pager_file` when
   the text cannot be produced as one iterable (`pager.md`).
4. A long-running loop the user should see progress for → `click.progressbar`.
5. Multi-line input from the user → `click.edit`; single values → `click.prompt`
   (`../parameters/prompting.md`).

<!-- BEGIN GENERATED INDEX -->

- [`echo`, `secho` and `style`](./echo-and-style.md) — printing output from a Click command; adding color or bold to terminal output; writing a message to stderr instead of stdout; colors leak as escape codes into a redirected file or log; printing bytes rather than text
- [Editors, launching apps, and raw terminal input](./editor-and-launch.md) — asking the user for multi-line input, like a commit message; opening a file in the user's editor from a command; opening a URL or a file in the system's default application; reading a single keypress without waiting for Enter; pausing until the user presses a key
- [Paging long output](./pager.md) — output is longer than a screen and should scroll like `git log`; the pager shows nothing until the command finishes; writing to a pager from code that cannot produce one iterable; an I/O operation on closed file error after paging
- [`click.progressbar`](./progressbar.md) — showing progress while a command processes many items; advancing a progress bar from an irregular or external loop; a progress bar shows no ETA; suppressing the progress bar in non-interactive runs
- [Streams, file opening and app directories](./streams-and-paths.md) — opening a file where `-` should mean stdin or stdout; needing a binary stream when stdout is text; deciding where to store a config file for the application; printing a filename that may contain undecodable bytes; opening a file outside the parameter-parsing phase

<!-- END GENERATED INDEX -->
