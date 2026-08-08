---
title: Migrating from FSD v2.0 to v2.1
triggers:
  - "a project was built on the v2.0 entities-and-features-first model"
  - "the entities and features layers are crowded with single-use slices"
  - "standardizing existing ad-hoc cross-imports"
---

# From v2.0 to v2.1

**No breaking changes** — a valid v2.0 project is a valid v2.1 project. What changed is the mental
model for decomposing an interface, and the recommendation is to make minor adjustments rather
than a rewrite.

- **v2.0:** identify entities and features first, down to the smallest bits of entity
  representation and interactivity; build widgets and pages by composing them. Most logic ended up
  in entities and features, and pages were thin compositional layers.
- **v2.1:** start with pages, and possibly stop there. Most people already think in pages, and
  pages are where you start looking for a component. Keep most UI and logic in each page on top of
  a reusable Shared foundation, and move logic down only when several pages need it.

Full procedure: `../decomposition.md`.

## Step 1 — Merge slices

Steiger is built around the new model. Run it and act on two rules in particular:

```bash
npx steiger src
```

- `fsd/insignificant-slice` — an entity or feature used on only one page should be merged into
  that page entirely.
- `fsd/excessive-slicing` — too many slices on a layer means the decomposition is too fine-grained;
  merge or group them.

A layer is a **global namespace** for its slices. Just as you would not pollute a global namespace
with a variable used once, treat a place in a layer's namespace as valuable and spend it sparingly.

## Step 2 — Standardize cross-imports

v2.1 also standardized entity cross-imports with the `@x` notation:

```ts
// entities/B/some/file.ts
import type { EntityA } from "entities/A/@x/B";
```

If your project already had ad-hoc cross-imports, convert them — but read
`../issues/cross-imports.md` first, since merging the entities is often the better answer.

Docs: <https://feature-sliced.design/docs/guides/migration/from-v2-0>
