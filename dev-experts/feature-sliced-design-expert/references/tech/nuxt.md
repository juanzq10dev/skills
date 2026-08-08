---
title: Nuxt
triggers:
  - "adding FSD to a Nuxt project"
  - "moving Nuxt file routing out of pages/ so the FSD pages layer can use it"
  - "placing Nuxt layouts in an FSD project"
---

# Usage with Nuxt

Nuxt defaults to no `src/` folder and owns `pages/` for file routing. Both are configurable, so
**relocate Nuxt's directories rather than renaming FSD layers**.

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  alias: { "@": "../src" },
  dir: {
    pages: "./src/app/routes", // file routing moves inside the FSD app layer
    layouts: "./src/app/layouts", // layouts too
  },
});
```

```text
src/
├── app/
│   ├── routes/index.vue     ← route: thin wrapper
│   └── layouts/
└── pages/
    └── home/{ui/home-page.vue, index.ts}   ← FSD pages layer, untouched
```

```ts
// src/pages/home/index.ts
export { default as HomePage } from "./ui/home-page";
```

```html
<!-- src/app/routes/index.vue -->
<script setup>
  import { HomePage } from "@/pages/home";
</script>

<template>
  <HomePage />
</template>
```

## Config-based routing instead

If you prefer `router.options.ts` over file routing, put it on the App layer and omit `dir.pages`:

```ts
// src/app/router.options.ts
import type { RouterConfig } from "@nuxt/schema";

export default <RouterConfig>{
  routes: (_routes) => [
    {
      name: "home",
      path: "/",
      component: () => import("@/pages/home.vue").then((r) => r.default || r),
    },
  ],
};
```

Scaffold the slice with `fsd pages home` (`../tooling/fsd-cli.md`).

Docs: <https://feature-sliced.design/docs/guides/tech/with-nuxtjs>
