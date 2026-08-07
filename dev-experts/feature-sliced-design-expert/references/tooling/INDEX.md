---
title: Tooling (Steiger and the fsd CLI)
triggers:
  - "checking an FSD project for violations automatically"
  - "adding an architectural linter to CI or a pre-commit hook"
  - "scaffolding layers, slices or segments"
  - "configuring or disabling an FSD lint rule"
type: index
---

# Tooling

Two independent, optional dev-dependencies. Neither is part of the methodology, and neither ships
runtime code.

| Tool        | Package                                      | Purpose                                                                  |
| ----------- | -------------------------------------------- | ------------------------------------------------------------------------ |
| **Steiger** | `steiger` + `@feature-sliced/steiger-plugin` | architecture linter — checks the real import graph against the FSD rules |
| **fsd CLI** | `@feature-sliced/cli`                        | scaffolds layer/slice/segment folders and index files                    |

## Rules

- **ALWAYS run `npx steiger ./src` before making architectural claims about a project.** Layer
  violations, single-reference slices and public-API sidesteps live in the import graph and are
  invisible in a directory listing. Do not list and read project files hunting for them first.
- **Steiger is zero-config** — do not write `steiger.config.ts` unless a specific rule must be
  turned off for specific paths.
- **Turn a rule off with scoped config, never globally**, and never by restructuring correct code
  to satisfy a rule the team has decided not to follow.
- **The CLI creates folders, not code.** It is a convenience for getting the index files and
  segment folders right; hand-creating them is equally valid.
- Steiger is **beta** — APIs may change, and v0.5.0 changed the config file format (a codemod
  exists in the repo's migration guide).

<!-- BEGIN GENERATED INDEX -->

- [fsd CLI — scaffolding layers, slices and segments](./fsd-cli.md) — generating a new slice with its index file and segments; creating a slice inside a slice group from the command line; scaffolding the shared layer's segments
- [Steiger rule reference](./steiger-rules.md) — Steiger reported a rule name that needs explaining; deciding which rules to enable or disable for a project; looking for the rule that detects a specific FSD violation
- [Steiger — installing, running and configuring](./steiger.md) — setting up the FSD linter in a project or in CI; running the architecture check in watch mode; disabling a rule for a folder such as shared; upgrading a steiger config from the 0.4 format

<!-- END GENERATED INDEX -->
