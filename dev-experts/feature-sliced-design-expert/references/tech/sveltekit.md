---
title: SvelteKit
triggers:
  - "adding FSD to a SvelteKit project"
  - "SvelteKit expects routing in src/routes and everything else in src/lib"
---

# Usage with SvelteKit

Two conflicts: SvelteKit puts routing in `src/routes` (FSD wants it on the `app` layer) and
everything else in `src/lib`. Both are config, so **move SvelteKit's directories**.

```ts
// svelte.config.ts
import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config}*/
const config = {
  preprocess: [vitePreprocess()],
  kit: {
    adapter: adapter(),
    files: {
      routes: "src/app/routes", // routing inside the app layer
      lib: "src",
      appTemplate: "src/app/index.html", // entry point inside the app layer
      assets: "public",
    },
    alias: { "@/*": "src/*" },
  },
};
export default config;
```

```text
src/
├── app/
│   ├── index.html
│   └── routes/+page.svelte
└── pages/
    └── home/{ui/home-page.svelte, index.ts}
```

```ts
// src/pages/home/index.ts
export { default as HomePage } from "./ui/home-page.svelte";
```

```html
<!-- src/app/routes/+page.svelte -->
<script>
  import { HomePage } from "@/pages/home";
</script>

<HomePage />
```

Scaffold the slice with `fsd pages home` (`../tooling/fsd-cli.md`).

Docs: <https://feature-sliced.design/docs/guides/tech/with-sveltekit>
