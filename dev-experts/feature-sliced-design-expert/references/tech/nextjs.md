---
title: Next.js
triggers:
  - "adding FSD to a Next.js project, App Router or Pages Router"
  - "the Next.js app/ and pages/ folders collide with FSD layers"
  - "server-only code leaks into the client bundle through a slice index"
  - "placing Route Handlers, middleware or instrumentation"
---

# Usage with Next.js

**Rename both FSD layers to `_app` and `_pages`, regardless of which router you use.** Steiger
recognizes the prefixed names. Keep Next.js's own `app`/`pages` at the project root so `src/`
holds only FSD code.

```text
app/                      ← Next.js App Router (route files only)
├── api/get-example/route.ts
└── example/page.tsx
src/
├── _app/                 ← FSD app layer
│   └── api-routes/
├── _pages/               ← FSD pages layer
│   └── example/{index.ts, ui/example.tsx}
├── widgets/  features/  entities/  shared/
```

```tsx
// app/example/page.tsx — thin re-export
export { ExamplePage as default, metadata } from "@/_pages/example";
```

Pages Router is identical in shape; routes live in the root `pages/` folder:

```tsx
// pages/example/index.tsx
export { Example as default } from "@/_pages/example";
```

```tsx
// pages/_app.tsx — Custom App component lives in src/_app/custom-app
export { App as default } from "@/_app/custom-app";
```

## Server and client public APIs

In the App Router a slice can hold both client-usable and server-only modules. If a server-only
module is exported from `index.ts`, its side effects propagate into the client module graph as
soon as a Client Component imports the slice — often a build error. When that happens, add a
second entry point:

- `index.ts` — client-safe
- `index.server.ts` — Server Components and `server-only` data access

## Route Handlers

Put handlers in an `api-routes` segment on the `_app` layer and re-export them from the framework
folder.

```tsx
// src/_app/api-routes/get-example-data.ts  (App Router)
import { getExamplesList } from "@/shared/db";

export const getExampleData = () => {
  try {
    return Response.json({ examplesList: getExamplesList() });
  } catch {
    return Response.json(null, {
      status: 500,
      statusText: "Ouch, something went wrong",
    });
  }
};
```

```tsx
// app/api/example/route.ts
export { getExampleData as GET } from "@/_app/api-routes";
```

Pages Router handlers export `{ config, handler }` from the segment and the route file re-splits
them into `export const config` and `export default`.

## Other

- `middleware.js` and `instrumentation.js` **must** stay in the project root, beside `app`/`pages`.
- Use a `db` segment in `shared` for database queries; keep caching/revalidation logic with the
  queries themselves.

Docs: <https://feature-sliced.design/docs/guides/tech/with-nextjs>
