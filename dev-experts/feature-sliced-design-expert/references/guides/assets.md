---
title: Static assets, images, fonts and global styles
triggers:
  - "adding an image, icon, font or stylesheet to an FSD project"
  - "someone proposes an assets/ segment or folder"
  - "deciding between public/ and a slice folder"
---

# Assets

Assets follow the same placement rules as code: group by use case, keep them next to what uses
them, and move to `shared` only on real reuse.

**Do not create an `assets` segment.** It is a common habit and it violates cohesion and locality
the same way `components/` does (`../issues/desegmentation.md`).

```text
pages/home/ui/
├── hero-image.jpg          ← used by exactly one page
├── previews/               ← many images? a subfolder inside ui/ is fine
│   ├── cake.jpg
│   └── pizza.jpg
└── HomePage.tsx
```

An asset that is part of **business logic** rather than UI goes in `model`, next to the code it is
coupled to:

```text
features/billing/model/
├── invoice-template.pdf
└── create-invoice.ts
```

## Summary

| Asset                             | Location                                                                                                 |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Used by one slice                 | inside that slice (`pages/home/ui/`)                                                                     |
| Reused icons and images           | `shared/ui/` — including files owned by a shared component, e.g. `shared/ui/{Dropdown.tsx, chevron.svg}` |
| Global styles (reset, global.css) | `app/styles/`                                                                                            |
| Fonts                             | `app/fonts/`, `public/` or `app/public`                                                                  |
| Static files, favicon             | `public/` or `app/public`                                                                                |

The bundler's `public/` folder is **not part of the FSD structure** and causes no naming
collision. Some tools (Vite) let you relocate it; others (Astro) do not — leaving it at the
project root is fine either way.

Docs: <https://feature-sliced.design/docs/guides/examples/handling-assets>
