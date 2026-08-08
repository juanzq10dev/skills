---
title: Framework and library integration
triggers:
  - "setting up FSD in a Next.js, Nuxt, SvelteKit, Astro or Electron project"
  - "the framework reserves the folder names app or pages and they collide with FSD layers"
  - "configuring path aliases or router directories for FSD"
  - "organizing TanStack Query keys and mutations"
type: index
---

# Framework integration

FSD imposes no framework. Every conflict below is the _same_ conflict: meta-frameworks reserve the
directory names `app` and `pages` for file-based routing, which collide with FSD's layer names.

## The resolution rule

Use the **first** option the framework supports:

1. **Point the framework's route directory somewhere else via config** — Nuxt (`dir.pages`),
   SvelteKit (`kit.files.routes`). Put routing inside `src/app/routes/`, which is where FSD says
   it belongs anyway. Preferred: FSD layer names stay untouched.
2. **Rename the FSD layers with an underscore prefix** — Next.js (`_app`, `_pages`), Astro
   (`_pages`). Use when the framework's route directory is not configurable.
3. Never rename the _framework's_ folders, and never merge the two roles into one directory.

## Rules that hold across all of them

- **ALWAYS keep the route file a thin re-export.** A route under the framework's directory should
  contain one `export { X as default } from '@/…'` line and nothing else; all page code lives in
  the FSD pages slice.
- **ALWAYS add a `@/*` → `src/*` path alias.** FSD's absolute-import convention between slices
  (`../public-api.md`) depends on it.
- **Prefixed layer names (`_app`, `_pages`) are recognized by Steiger** — you do not lose linting
  by renaming.
- **Do not fight folders the framework owns.** `public/`, `middleware.js`, `instrumentation.js`
  and content-collection directories stay where the framework demands; they are outside the FSD
  structure and cause no collision.
- **FSD is a frontend methodology.** Backend route handlers can be housed in an `api-routes`
  segment on the App layer, but if the API surface is large, move it to its own monorepo package
  rather than growing it inside the FSD tree.

<!-- BEGIN GENERATED INDEX -->

- [Astro](./astro.md) — adding FSD to an Astro project; Astro requires routes in src/pages which collides with the FSD pages layer; an Astro integration such as Starlight demands its own content folder
- [Electron](./electron.md) — applying FSD to an Electron app with main, preload and renderer processes; typing and organizing IPC channels between processes
- [Next.js](./nextjs.md) — adding FSD to a Next.js project, App Router or Pages Router; the Next.js app/ and pages/ folders collide with FSD layers; server-only code leaks into the client bundle through a slice index; placing Route Handlers, middleware or instrumentation
- [Nuxt](./nuxt.md) — adding FSD to a Nuxt project; moving Nuxt file routing out of pages/ so the FSD pages layer can use it; placing Nuxt layouts in an FSD project
- [SvelteKit](./sveltekit.md) — adding FSD to a SvelteKit project; SvelteKit expects routing in src/routes and everything else in src/lib
- [TanStack Query (React Query)](./tanstack-query.md) — placing query keys, query factories and mutations in an FSD project; setting up QueryClientProvider or a Suspense boundary on the app layer; implementing pagination, infinite scroll or useMutationState under FSD

<!-- END GENERATED INDEX -->
