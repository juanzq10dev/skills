---
title: Public API (index files and the @x notation)
triggers:
  - "writing or reviewing a slice index.ts"
  - "an import reaches inside another slice instead of through its index"
  - "two entities need to reference each other's types"
  - "barrel files cause circular imports, slow dev server or broken tree-shaking"
  - "a server-only module leaks into the client bundle through index.ts"
---

# Public API

A contract between a slice and its consumers, and a gate: only what is re-exported is reachable.

```js
// pages/auth/index.js
export { LoginPage } from "./ui/LoginPage";
export { RegisterPage } from "./ui/RegisterPage";
```

Three goals: (1) the app is insulated from refactors inside the slice, (2) behavior changes that
break expectations show up in the public API, (3) **only the necessary parts are exposed**.

```js
// ❌ features/comments/index.js — wildcard re-exports
export * from "./ui/Comment";
export * from "./model/comments";
```

Wildcards destroy discoverability (you cannot tell what the slice's interface is) and leak
internals that consumers then start depending on.

On slice-less layers the granularity inverts: **Shared defines one public API per segment**
(`shared/ui/index.ts`, `shared/api/index.ts`); **sliced layers define one per slice**, and should
_not_ also add per-segment index files inside it.

## The `@x` notation for cross-imports

When entity B must import from entity A, A declares a public API dedicated to B:

```text
entities/
├── song/
│   ├── @x/
│   │   ├── artist.ts   ← public API only for entities/artist/
│   │   └── playlist.ts ← public API only for entities/playlist/
│   ├── model/song.ts
│   └── index.ts        ← the regular public API
```

```ts
// entities/song/@x/artist.ts
export type { Song } from "../model/song.ts";
```

```ts
// entities/artist/model/artist.ts
import type { Song } from "entities/song/@x/artist";

export interface Artist {
  name: string;
  songs: Array<Song>;
}
```

Read `A/@x/B` as "A crossed with B". **Use it only on the Entities layer**, and only as a last
resort — see `issues/cross-imports.md` for what to try first.

## Environment-specific public APIs

`index.ts` should be the public API and should not be customized freely. The one sanctioned
exception is a genuine runtime boundary: when a server-only module exported from `index.ts` drags
server side effects into the client graph, add a second entry point.

```text
pages/dashboard/
├── index.ts          ← client-safe
└── index.server.ts   ← Server Components, `server-only` data access
```

## Known problems with barrel files, and their fixes

| Problem                                                                                   | Fix                                                                                                                                                        |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Circular imports** — `ui/HomePage.jsx` imports `"../"`, which imports `ui/HomePage.jsx` | Inside one slice always use **relative** imports with the full path; between slices always use **absolute** (aliased) imports                              |
| **Broken tree-shaking / huge bundles** from one big `shared/ui/index.ts`                  | Give each component or library its own index: `shared/ui/button/index.js`, imported as `@/shared/ui/button`                                                |
| **Slow dev server** on large projects                                                     | Same per-module indexes; drop redundant per-segment indexes inside sliced layers; for very large apps, split into monorepo packages, each its own FSD root |
| **Nothing stops a direct import** past the index (IDE auto-import especially)             | Run Steiger — `fsd/no-public-api-sidestep` catches it (`tooling/steiger-rules.md`)                                                                         |

Docs: <https://feature-sliced.design/docs/reference/public-api>
