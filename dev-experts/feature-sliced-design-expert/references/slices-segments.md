---
title: Slices and segments
triggers:
  - "naming a new folder inside a layer"
  - "deciding whether something is a slice or a segment"
  - "wondering if a folder called components, hooks, types or utils is acceptable"
  - "a slice has files sitting directly in it with no segment folder"
  - "explaining cohesion and coupling in an FSD project"
---

# Slices and segments

**Slice** = second level, groups code by _meaning for the business_. **Segment** = third level,
groups code by _technical purpose_.

```text
entities/            ← layer      (name is standardized)
└── post/            ← slice      (name is yours: the business domain)
    ├── ui/          ← segment    (name describes purpose)
    ├── model/
    ├── api/
    └── index.ts     ← public API
```

Slice names are never standardized — a photo gallery has `photo`, `effects`, `gallery-page`; a
social network has `post`, `comments`, `news-feed`. **Shared and App have no slices** and hold
segments directly.

## The two rules slices must satisfy

1. **Import rule on layers** (`layers.md`) — a slice may not import a sibling slice on its own
   layer. That is a _cross-import_; see `issues/cross-imports.md`.
2. **Public API rule on slices** — every slice (and every segment on a slice-less layer) must
   declare a public API, and outside code may reference only that. See `public-api.md`.

Together they produce the goal: **zero coupling between slices, high cohesion inside one**.

## Standard segment names

| Segment  | Contents                                                    |
| -------- | ----------------------------------------------------------- |
| `ui`     | UI display: components, formatters, styles                  |
| `api`    | backend interaction: request functions, data types, mappers |
| `model`  | the data model: schemas, interfaces, stores, business logic |
| `lib`    | library code this slice needs                               |
| `config` | configuration files and feature flags                       |

Custom segments are allowed, most usefully on App and Shared (`shared/auth`, `shared/db`,
`shared/ipc`, `app/styles`).

## The naming test

> A segment name must describe the **purpose** of its contents (_why_), not their **essence**
> (_what_).

```text
shared/lib/dates/      ✅ purpose
shared/lib/utils/      ❌ essence — becomes a dump
features/x/ui/         ✅
features/x/components/ ❌ essence  (Steiger: fsd/segments-by-purpose)
entities/y/types.ts    ❌ essence  (see issues/desegmentation.md)
```

Banned by convention: `components`, `hooks`, `types`, `utils`, `helpers`, `constants`, `assets`.
A slice with **no** segments at all is also flagged (`fsd/no-segmentless-slices`), as are segments
placed directly on a sliced layer, e.g. `features/ui/` (`fsd/no-segments-on-sliced-layers`).

## Slice groups

Closely related slices may be nested in a grouping folder for navigation only. A group is **not**
a slice: no segments, no `index.ts`, and **no shared code inside it**. See `slice-groups.md`.

Docs: <https://feature-sliced.design/docs/reference/slices-segments>
