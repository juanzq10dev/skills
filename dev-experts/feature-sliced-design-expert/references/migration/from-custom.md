---
title: Migrating from a custom architecture
triggers:
  - "converting a components/containers/reducers project to FSD"
  - "asking what order to do an FSD migration in"
  - "a Shared layer has become a dumping ground during migration"
---

# From a custom architecture

Typical starting point: `src/{actions, api, components, containers, constants, i18n, modules,
helpers, routes, utils, reducers, selectors, styles}`.

First, set up an alias for `src` (`@` is assumed below). Then work the steps in order.

## Step 1 — Divide by pages

If you only have `routes/`, create `pages/` and move as much component code out of the routes as
possible: a tiny route, a larger page. It is fine at this stage for pages to reference each other.

```js
// src/routes/products.[id].js
export { ProductPage as default } from "@/pages/product";
```

```js
// src/pages/product/index.js
export { ProductPage } from "./ProductPage.jsx";
```

## Step 2 — Separate everything else from pages

Create `src/shared` and move everything that does **not** import from `pages`/`routes`. Create
`src/app` and move everything that **does**, including the routes themselves. Shared has no
slices, so its segments importing each other is fine.

## Step 3 — Remove cross-imports between pages

For each page-to-page import, either copy-paste the code into the depending page, or move it to
`shared/ui` (UI kit), `shared/config` (constants) or `shared/api` (backend). **Copy-pasting is not
architecturally wrong** — shared parts of pages often drift apart, and duplication beats a
dependency there. Do not copy-paste _business logic_, though; that you would have to fix twice.

## Step 4 — Unpack Shared

Shared is now bloated, and it is a dependency of every layer, so change there is the riskiest.
Find everything used on exactly one page and move it into that page's slice — **including actions,
reducers and selectors.** There is no benefit in grouping all actions together; there is benefit in
colocating them with their usage.

## Step 5 — Organize by technical purpose

Introduce segments (`ui`, `api`, `model`, `lib`, `config`) inside the pages, and dissolve the
essence-named folders in Shared:

```text
components/, containers/  → shared/ui/
helpers/, utils/          → shared/lib/<focused-library>/   (grouped by function: dates, …)
constants/                → shared/config/
```

Never create segments that group by what code _is_ (`components`, `actions`, `types`, `utils`).

## Optional steps

6. **Redux slices used on several pages** become Entities (business nouns) or Features (things
   users do). API functions can stay in `shared/api`. For inherent connections between entities,
   see `../guides/types.md`.
7. **`modules/`** is usually already feature-shaped → Features; large UI chunks like an app header
   → Widgets.
8. **Clean `shared/ui`** — strip business logic out of the ex-`components`/`containers`, pushing it
   to higher layers, copy-pasting where it isn't widely used.

Docs: <https://feature-sliced.design/docs/guides/migration/from-custom>
