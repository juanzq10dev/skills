---
title: Code smells and issues
triggers:
  - "reviewing an FSD codebase for architectural problems"
  - "Steiger reported a violation and it needs interpreting and fixing"
  - "the structure feels wrong but the specific rule broken is unclear"
  - "deciding whether an existing violation is worth refactoring now"
type: index
---

# Code smells and issues

The four recurring failure modes of FSD codebases. All four are _smells_, not compile errors: the
code runs, and the cost shows up later as coupling and refactor pain.

## Which one is it?

Diagnose with the **first** question that answers yes:

1. Does a file import a **sibling slice on its own layer**? → `cross-imports.md`
2. Is there a folder or file named for what code **is** (`components/`, `utils/`, `types.ts`)
   rather than what it is **for**? → `desegmentation.md`
3. Does `entities/` hold CRUD, auth tokens, or slices used by exactly one page?
   → `excessive-entities.md`
4. Are URLs or redirect logic hardcoded **below** the Pages layer? → `routing.md`

## Rules for acting on them

- **NEVER "fix" a cross-import by adding `@x` outside the Entities layer.** `@x` is an Entities-only
  escape hatch and a last resort even there; on Features and Widgets the answer is one of merge,
  push-down, or compose-from-above (`cross-imports.md`).
- **ALWAYS prefer merging upward over adding an abstraction.** A slice used once should be absorbed
  into its single consumer, not wrapped. Duplication is not automatically an architectural error —
  copy-pasting UI is often more correct than a premature shared module. Business logic is the
  exception: do not duplicate that.
- **ALWAYS run `npx steiger ./src` before proposing a refactor** and after applying one. Several of
  these smells (single-reference slices, excessive slicing, public-API sidesteps) are invisible
  from the directory tree and only show up in the import graph.
- **How strict to be is a team decision, not a universal.** Early-stage products may accept some
  cross-imports as a deliberate speed trade-off; long-lived or regulated systems should not. When
  a violation is kept, it must be deliberate, documented, and revisited — not silent.

<!-- BEGIN GENERATED INDEX -->

- [Cross-imports](./cross-imports.md) — one slice imports another slice on the same layer; features or widgets have become coupled to each other; Steiger reports fsd/forbidden-imports or fsd/no-cross-imports; two entities genuinely reference each other in the domain; choosing between merging slices, pushing logic down, or composing from a page
- [Desegmentation (grouping by technical role)](./desegmentation.md) — the project has components/, utils/, constants/ or stores/ folders at the top; a slice contains types.ts, utils.ts or helpers.ts; porting a Next.js or Nuxt default layout into FSD; Steiger reports fsd/segments-by-purpose or fsd/no-reserved-folder-names
- [Excessive entities](./excessive-entities.md) — the entities layer has grown large or ambiguous; deciding whether to create an entity for a piece of business logic; where to put CRUD calls or the authenticated user and token; entities cross-import each other and @x is spreading; asking whether a project can skip the entities layer
- [Routing leaked below the Pages layer](./routing.md) — URLs or paths are hardcoded inside entities, features or widgets; changing a route requires edits scattered across layers; deciding where redirect logic belongs

<!-- END GENERATED INDEX -->
