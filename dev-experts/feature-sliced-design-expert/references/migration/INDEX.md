---
title: Migration
triggers:
  - "moving an existing codebase to Feature-Sliced Design"
  - "upgrading a project from FSD v1 or v2.0"
  - "deciding whether adopting FSD is worth it for this project"
type: index
---

# Migration

## Which path

- Coming from a **custom / no architecture** (`components/`, `containers/`, `reducers/`) →
  `from-custom.md`
- Coming from **FSD v1 / feature-slices** → `from-v1.md` (breaking changes)
- Coming from **FSD v2.0** → `from-v2-1.md` (no breaking changes, mental-model shift only)

## Rules

- **ALWAYS migrate incrementally.** FSD adoption never requires halting feature work, and a
  big-bang restructure is the most common way it fails. Shape App and Shared first, spread the
  existing UI across Pages/Widgets with broad strokes even where imports still violate the rules,
  then resolve violations gradually.
- **NEVER adopt FSD against the team's will**, even as the lead — first convince them the benefit
  outweighs the migration and learning cost. Architectural change is invisible to management
  unless you explain it first.
- **Check the current architecture is actually causing trouble** before migrating: new members
  slow to become productive, unrelated code breaking on every change, new functionality hard to
  add because of everything you must keep in mind. If the current architecture works, it may not
  be worth changing.
- **Refrain from adding new large entities while refactoring**, and refactor only part of the
  project at a time.
- **Run `npx steiger ./src` as the progress meter** (`../tooling/steiger.md`) rather than judging
  by eye — it names the remaining violations.

<!-- BEGIN GENERATED INDEX -->

- [Migrating from a custom architecture](./from-custom.md) — converting a components/containers/reducers project to FSD; asking what order to do an FSD migration in; a Shared layer has become a dumping ground during migration
- [Migrating from FSD v1 (feature-slices)](./from-v1.md) — a project uses the pre-v2 feature-slices layout; ui, lib and api sit at the src root instead of under shared; translating old folder names like flows, screens, views, containers or services
- [Migrating from FSD v2.0 to v2.1](./from-v2-1.md) — a project was built on the v2.0 entities-and-features-first model; the entities and features layers are crowded with single-use slices; standardizing existing ad-hoc cross-imports

<!-- END GENERATED INDEX -->
