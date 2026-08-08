---
name: feature-sliced-design-expert
description: >
  Expert guidance for working with Feature-Sliced Design (FSD) v2.1 — the frontend architectural
  methodology — and its Steiger linter and `fsd` CLI.
  ALWAYS use before doing any task that requires knowledge specific to Feature-Sliced Design, or
  that references FSD, layers, slices, segments, app/pages/widgets/features/entities/shared,
  public API or index.ts barrels, cross-imports, the `@x` notation, slice groups, or Steiger.
  Common tasks may include scaffolding an FSD project, deciding which layer or segment a new file
  belongs on, reviewing a diff for import-rule violations, removing a cross-import between two
  slices, designing or splitting a slice's public API, migrating an existing codebase to FSD,
  resolving the Next.js/Nuxt/SvelteKit/Astro `pages` and `app` folder-name conflict, placing API
  requests, auth tokens, types or assets, configuring Steiger, or explaining a Steiger violation.
---

# Feature-Sliced Design v2.1

FSD is a **methodology**, not a package: there is nothing to `npm install` into the app itself.
It is a set of naming and dependency conventions plus two optional dev tools (Steiger, `fsd`).

## Core FSD Concepts

- **Layer** — one of 7 standardized top-level folders (`app`, `processes` (deprecated), `pages`,
  `widgets`, `features`, `entities`, `shared`). Names are fixed; adding layers is not allowed.
- **Slice** — a folder inside a layer, named after a business domain (`post`, `cart`). App and
  Shared have **no** slices.
- **Segment** — a folder inside a slice, named after technical purpose (`ui`, `api`, `model`,
  `lib`, `config`). Names describe _why_, never _what_.
- **Public API** — the `index.ts` a slice (or a Shared/App segment) exposes; nothing outside may
  reach past it.
- **Import rule on layers** — a file in a slice may only import slices on layers _strictly below_.

Definitions only. Read `references/layers.md` and `references/slices-segments.md` before applying
any of them.

## Deciding where code goes

This is the question FSD is asked most often, and guessing it wrong is the main way projects
degrade. **Start from `references/decomposition.md`** — it carries the v2.1 pages-first procedure
and the "which layer?" hierarchy. Only after the layer is settled does the segment question
(`references/slices-segments.md`) apply.

## Tooling

Two separate packages, neither required by the methodology:

```bash
npm i -D steiger @feature-sliced/steiger-plugin   # architectural linter
npx steiger ./src                                 # zero-config; add --watch to iterate
npm add -g @feature-sliced/cli                    # scaffolding: `fsd pages home -s ui,api`
```

Prefer running `npx steiger ./src` over eyeballing the folder tree — it reports the real import
graph, including violations that are invisible from the directory listing alone. Do not list and
read project files looking for architecture problems until Steiger has reported. Details:
`references/tooling/INDEX.md`.

## CRITICAL: Always Read Reference Files Before Answering

NEVER answer from memory or guess at layer semantics, segment names, folder conventions, or
notation. FSD changed meaningfully between v1, v2.0 and v2.1, and parametric memory is usually
stuck on the v2.0 "entities-and-features-first" model, which v2.1 explicitly moved away from.
ALWAYS read the relevant reference file(s) from the Reference Index below before responding. For
every question, identify which reference file(s) are relevant using the index descriptions, read
them, then answer based on what you read.

## Reference Index

<!-- BEGIN GENERATED INDEX -->

- [Deciding which layer code goes on (v2.1 pages-first)](./references/decomposition.md) — starting a new FSD project and laying out the folders; deciding whether something should be a feature, an entity, a widget or stay in the page; asking whether a project needs an entities layer at all; a reviewer says the decomposition is too fine-grained; adding a new screen or a new piece of UI and unsure where to put it
- [Layers and the import rule](./references/layers.md) — deciding which of the 7 layers a file or folder belongs on; checking whether an import is legal in FSD; an import goes sideways or upwards and needs to be fixed; explaining what app, pages, widgets, features, entities or shared are for; someone asks about the processes layer
- [Naming conventions and FSD term collisions](./references/naming.md) — choosing a name for a layer, slice or segment folder; the business vocabulary collides with FSD words like page, process or model; a team debates calling a folder store, views, ui-kit or core; Steiger reports fsd/typo-in-layer-name or fsd/inconsistent-naming
- [Public API (index files and the @x notation)](./references/public-api.md) — writing or reviewing a slice index.ts; an import reaches inside another slice instead of through its index; two entities need to reference each other's types; barrel files cause circular imports, slow dev server or broken tree-shaking; a server-only module leaks into the client bundle through index.ts
- [Slice groups](./references/slice-groups.md) — a layer has grown too many slices to scan at a glance; wanting to nest related slices in a subfolder; asking whether a grouping folder can hold shared code or its own index.ts; Steiger reports fsd/excessive-slicing
- [Slices and segments](./references/slices-segments.md) — naming a new folder inside a layer; deciding whether something is a slice or a segment; wondering if a folder called components, hooks, types or utils is acceptable; a slice has files sitting directly in it with no segment folder; explaining cohesion and coupling in an FSD project
- [Placing common concerns](./references/guides/INDEX.md) — deciding where a specific kind of code goes: requests, tokens, types, assets, layouts; adding a new API call, form, image or shared type to an FSD project; asking whether something belongs in shared or in a slice
- [Code smells and issues](./references/issues/INDEX.md) — reviewing an FSD codebase for architectural problems; Steiger reported a violation and it needs interpreting and fixing; the structure feels wrong but the specific rule broken is unclear; deciding whether an existing violation is worth refactoring now
- [Migration](./references/migration/INDEX.md) — moving an existing codebase to Feature-Sliced Design; upgrading a project from FSD v1 or v2.0; deciding whether adopting FSD is worth it for this project
- [Framework and library integration](./references/tech/INDEX.md) — setting up FSD in a Next.js, Nuxt, SvelteKit, Astro or Electron project; the framework reserves the folder names app or pages and they collide with FSD layers; configuring path aliases or router directories for FSD; organizing TanStack Query keys and mutations
- [Tooling (Steiger and the fsd CLI)](./references/tooling/INDEX.md) — checking an FSD project for violations automatically; adding an architectural linter to CI or a pre-commit hook; scaffolding layers, slices or segments; configuring or disabling an FSD lint rule

<!-- END GENERATED INDEX -->
