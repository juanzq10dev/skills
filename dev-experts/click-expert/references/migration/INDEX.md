---
title: Upgrading across Click versions
type: index
triggers:
  - "behavior changed after upgrading Click"
  - "tests broke after a Click upgrade, especially around stderr or flags"
  - "a library must work with more than one Click version"
  - "deciding which Click version to require"
---

# Migration

Docs: https://click.palletsprojects.com/en/stable/upgrade-guides/ and
https://github.com/pallets/click/blob/main/CHANGES.md

Target of this skill: **8.4.2**. Python >= 3.10 since 8.2.

## Which file to read

1. Coming from **8.1 or earlier** → `to-8-2.md` first. That is the only release in this
   range with removals and behavior changes large enough to break working code.
2. Something around **flags, `flag_value` or `default`** changed → `to-8-3.md` then
   `to-8-4.md`; this area was reworked twice.
3. Something around **`CliRunner`, capture or `fileno()`** changed → `to-8-4.md`.
4. Writing a **library** that must support several Click versions →
   `multi-version-support.md`.

## Rules

- **NEVER pin behavior to a version number when a feature check will do.** Click's own
  guidance is to use `if`/`try` and only fall back to
  `importlib.metadata.version("click")` when detection is impractical.
- **NEVER use `click.__version__`** — deprecated in 8.2, removed in 9.1.
- Deprecated-but-present names (`BaseCommand`, `MultiCommand`, `OptionParser`,
  `Context.protected_args`) are all scheduled for **9.0**. Replace them now; the
  replacements exist in 8.x (`../public-api.md`).
- The `upgrade-guides` page upstream currently documents only the **8.3 → 9.0** path, and
  is a placeholder until 9.0 ships. `CHANGES.md` is the authoritative record for 8.x.

<!-- BEGIN GENERATED INDEX -->

- [Supporting several Click versions from one library](./multi-version-support.md) — a library must work with both Click 8.1 and 8.2+; a ParamType override breaks because a method gained a ctx argument; choosing a Click version constraint for a package
- [Upgrading 8.1 → 8.2](./to-8-2.md) — code written for Click 8.1 or 8.0 stops working after an upgrade; CliRunner tests fail on result.output or a missing mix_stderr argument; BaseCommand, MultiCommand or OptionParser now warns; a group that used to print help and exit 0 now exits 2
- [Upgrading 8.2 → 8.3.x](./to-8-3.md) — a flag's default value reaches the function differently after upgrading to 8.3; an option receives Sentinel.UNSET instead of None; a variadic argument should have a default; checking how explicitly a parameter value was provided
- [Upgrading 8.3 → 8.4.x](./to-8-4.md) — type checking a ParamType or Choice subclass fails after upgrading to 8.4; output written by a subprocess or logging handler is missing from CliRunner results; a feature switch group picks a different option than it used to; version_option raises RuntimeError for a package whose module name differs; Fish or Zsh completion broke after an upgrade

<!-- END GENERATED INDEX -->
