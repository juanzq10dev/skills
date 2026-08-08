---
title: Standalone native builds with Briefcase
triggers:
  - "shipping a CLI to users who do not have Python installed"
  - "producing a .msi, .pkg, .deb or .rpm installer for a command line tool"
  - "the packaged app fails to start with no obvious error"
---

# Briefcase

Docs: https://click.palletsprojects.com/en/stable/standalone-apps/ and
https://briefcase.beeware.org/en/stable/how-to/building/cli-apps/

Bundles a Python interpreter plus all dependencies into a platform-native installer:
`.pkg` on macOS, `.msi` on Windows, `.deb`/`.rpm` on Linux.

```console
$ pip install briefcase
```

```toml
[tool.briefcase]
project_name = "Hello CLI"
bundle = "com.example"
version = "0.0.1"
license.file = "LICENSE"
author = "Your Name"
author_email = "you@example.com"

[tool.briefcase.app.hello-cli]
formal_name = "Hello CLI"
description = "My first application"
sources = ["src/hello_cli"]
console_app = true
requires = ["click"]
```

`console_app = true` is what makes Briefcase treat the project as a terminal app rather
than a GUI.

Briefcase launches the app with `python -m <package>`, so a `__main__.py` **must** exist in
the package or the app will not start:

```python
# src/hello_cli/__main__.py
from hello_cli.app import main

if __name__ == "__main__":
    main()
```

```console
$ briefcase dev -- World --count 2   # run from source; args go after --
$ briefcase create
$ briefcase build
$ briefcase package
```

## Common Anti-Patterns

- Omitting `__main__.py` → the packaged app silently fails to launch.
- Leaving `console_app` unset → Briefcase builds a GUI bundle with no terminal.
- Forgetting `requires = ["click", ...]` → the dependency is not bundled.
- `briefcase dev World` without `--` → the arguments are consumed by Briefcase itself.
