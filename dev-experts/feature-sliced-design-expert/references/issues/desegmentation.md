---
title: Desegmentation (grouping by technical role)
triggers:
  - "the project has components/, utils/, constants/ or stores/ folders at the top"
  - "a slice contains types.ts, utils.ts or helpers.ts"
  - "porting a Next.js or Nuxt default layout into FSD"
  - "Steiger reports fsd/segments-by-purpose or fsd/no-reserved-folder-names"
---

# Desegmentation

Also called _horizontal slicing_ or _packaging by layer_: grouping files by technical role instead
of by the domain they serve. It is the default in Next/Nuxt starters because it enables
auto-imports and file routing, and it leaks into FSD codebases as generic folders and generic
files.

```text
❌ app/                     ❌ features/delivery/ui/components/
   components/              ❌ entities/recommendations/utils/
   actions/                 ❌ pages/delivery/model/types.ts
   composables/             ❌ pages/delivery/model/utils.ts
   constants/               ❌ pages/delivery/api/endpoints.ts
   utils/
   stores/
```

The file-level form is the one most often missed — a single `types.ts` quietly aggregates several
domains:

```ts
// ❌ pages/delivery/model/types.ts — two unrelated domains in one file
export interface DeliveryOption {
  id: string;
  name: string;
  price: number;
}
export interface UserInfo {
  id: string;
  name: string;
  avatar: string;
}
```

## Why it costs

- **Low cohesion** — one feature change edits files in several large folders.
- **Tight coupling** — unexpected dependency chains between unrelated components.
- **Hard refactors** — extracting one domain means manually picking it out of every bucket.

## Fix

Group everything for one domain in one place, and name folders and files after the domain:

```text
pages/delivery/
├── index.tsx
├── ui/
│   ├── DeliveryPage.tsx
│   ├── DeliveryCard.tsx
│   ├── DeliveryChoice.tsx
│   └── UserInfo.tsx
└── model/
    ├── delivery.ts
    └── user.ts
```

The same purpose-not-essence test that governs segment names (`../slices-segments.md`) governs
file names inside them.

Docs: <https://feature-sliced.design/docs/guides/issues/desegmented>
