---
title: Shortcut decorators (`--password`, `--yes`, `--version`, `--help`)
triggers:
  - "adding a --version flag to a CLI"
  - "asking for confirmation before a destructive command"
  - "adding a password prompt with confirmation"
  - "version_option raises RuntimeError about not finding the package"
---

# Shortcut decorators

Docs: https://click.palletsprojects.com/en/stable/option-decorators/

Ready-made combinations of the keywords in `options.md` and `prompting.md`. All are eager
and hide their value from the command function.

## `version_option`

```python
@click.command()
@click.version_option()                                  # infers version and package
@click.version_option("1.0.0", "-V", "--version")        # explicit version and decls
@click.version_option(package_name="my-dist", prog_name="mycli",
                      message="%(prog)s %(version)s")
def cli() -> None: ...
```

Signature: `version_option(version=None, *param_decls, package_name=None, prog_name=None,
message=None, **kwargs)`. With no `version`, Click resolves it from installed distribution
metadata. Since 8.4.2, a `package_name` that is not a distribution name is also tried as a
**top-level module** name via `importlib.metadata.packages_distributions()`, so `PIL`
(dist `Pillow`) and `jwt` (dist `PyJWT`) work without a `RuntimeError`. If it still cannot
resolve, pass `version=` or `package_name=` explicitly.

## `confirmation_option`

```python
@click.command()
@click.confirmation_option(prompt="Are you sure you want to drop the db?")
def dropdb() -> None:
    click.echo("Dropped all tables!")
```

Equivalent to a flag with `callback=abort_if_false, expose_value=False, prompt=...`.
Answering no raises `Abort` (exit code 1); passing `--yes` skips the prompt.

## `password_option`

```python
@click.command()
@click.password_option()
def encrypt(password: str) -> None: ...
```

Equivalent to `@click.option("--password", prompt=True, hide_input=True,
confirmation_prompt=True)`. Drop `confirmation_prompt` by writing the option out when the
value is being _entered_, not _set_.

## `help_option`

`@click.help_option("-h", "--help")` declares the help flag explicitly. Usually
unnecessary — set `context_settings={"help_option_names": ["-h", "--help"]}` instead
(`../help-pages.md`), which applies to a whole group.

## Common Anti-Patterns

- Hardcoding `@click.version_option("1.0.0")` next to a `pyproject.toml` version → drift;
  use the no-argument form and let metadata answer.
- `click.__version__` in a version message → that is _Click's_ version, and it is
  deprecated (`../public-api.md`).
- A hand-rolled `--yes` flag with an `abort_if_false` callback → `confirmation_option`.
- Expecting `password_option` to skip the confirmation → it confirms by default.
