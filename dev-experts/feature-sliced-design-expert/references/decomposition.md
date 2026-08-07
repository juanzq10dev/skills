---
title: Deciding which layer code goes on (v2.1 pages-first)
triggers:
  - "starting a new FSD project and laying out the folders"
  - "deciding whether something should be a feature, an entity, a widget or stay in the page"
  - "asking whether a project needs an entities layer at all"
  - "a reviewer says the decomposition is too fine-grained"
  - "adding a new screen or a new piece of UI and unsure where to put it"
---

# Decomposition: which layer?

FSD v2.1 replaced v2.0's mental model. **v2.0 said: find the entities and features first, then
compose pages out of them.** **v2.1 says: start at pages, and possibly stop there.** Most of the
UI and logic stays in each page, on top of a reusable Shared foundation; things move _down_ a
layer only when reuse actually forces it. Any pre-v2.1 instinct to open a new project by carving
out `entities/` and `features/` is the thing to unlearn.

## The procedure

Apply in order; stop at the first step that answers the question.

1. **List the pages.** Each screen becomes one slice on `pages/`. Near-identical screens (sign-in
   and sign-up) may share one slice. Non-reused UI belongs _inside_ the page — there is no size
   limit on a page slice as long as the team can still navigate it.
2. **Put the generic foundation in `shared/`.** The UI kit, the API client, env parsing, i18n,
   route constants. Shared is normally _extracted during development_, not planned up front.
3. **Only when a block is reused on several pages**, move it down to the layer that fits:
   - a large self-sufficient UI block → `widgets/`
   - an interaction users care to perform → `features/`
   - a real-world thing the business names → `entities/`
4. **Wiring, providers, routing, analytics** → `app/`.

If nothing was reused, three layers — App, Pages, Shared — is a complete, correct FSD project.

## Feature vs. entity vs. widget vs. page

- **Entity** is a _noun_ the business uses: User, Post, Order.
- **Feature** is a _verb_ the user performs on entities. Not everything is a feature — the test is
  that it is reused on **several pages**. Optimize for a newcomer discovering the project by
  reading `pages/` and `features/`; too many features drown out the important ones.
- **Widget** is a large self-sufficient UI block, useful when reused across pages, or when a page
  has several large independent blocks. If it is most of a page's content and never reused, it is
  **not** a widget — leave it in the page.
- **Page** is a screen. Under nested routing, use Widgets for router blocks the way flat routing
  uses Pages.

## Do you need an `entities/` layer at all?

Often no, and skipping it is not a violation — it simplifies the architecture and keeps the layer
free for later. A **thin client** (business logic mostly on the backend) usually needs none.
Prefer `shared/api` types plus a `model` segment on the current slice, and defer decomposition:
the later code moves down to Entities, the cheaper the refactor, because Entities is visible to
every layer above it. Details and the four specific traps: `issues/excessive-entities.md`.

## Signals you decomposed too early

- a slice referenced from exactly one place (Steiger: `fsd/insignificant-slice`)
- more than ~20 ungrouped slices on a layer (`fsd/excessive-slicing`)
- slices on one layer importing each other (`issues/cross-imports.md`)

Run `npx steiger ./src` rather than judging by eye. The fix for all three is the same direction:
**merge upward**, into the single page or widget that uses it.

## Migrating an existing codebase

Do not do the above bottom-up on a live project — follow the staged procedure in
`migration/from-custom.md`.

Docs: <https://feature-sliced.design/docs/get-started/tutorial> ·
<https://feature-sliced.design/docs/guides/migration/from-v2-0>
