---
title: Astro
triggers:
  - "adding FSD to an Astro project"
  - "Astro requires routes in src/pages which collides with the FSD pages layer"
  - "an Astro integration such as Starlight demands its own content folder"
---

# Usage with Astro

Astro's route directory is **not** relocatable, so rename the FSD layer: routes stay in
`src/pages`, the FSD pages layer becomes `src/_pages`.

```text
src/
├── pages/            ← Astro routing (thin entry points only)
│   ├── index.astro
│   └── 404.astro
└── _pages/           ← FSD pages layer
    └── home/{ui/HomePage.astro, index.ts}
```

```astro
---
// src/pages/index.astro
import { HomePage } from '@/_pages/home';
---

<HomePage />
```

```json
// tsconfig.json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "paths": { "@/*": ["./src/*"] }
  }
}
```

## Integrations

Integrations such as Starlight expect content in fixed locations (`src/content/docs`). If the root
path is not configurable, leave it — content-collection folders do not collide with FSD layer
names and can sit beside `_pages/` and `shared/`. Let the integration own its routing and
rendering; FSD manages the application-specific code.

Docs: <https://feature-sliced.design/docs/guides/tech/with-astro>
