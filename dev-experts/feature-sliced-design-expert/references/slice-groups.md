---
title: Slice groups
triggers:
  - "a layer has grown too many slices to scan at a glance"
  - "wanting to nest related slices in a subfolder"
  - "asking whether a grouping folder can hold shared code or its own index.ts"
  - "Steiger reports fsd/excessive-slicing"
---

# Slice groups

An **optional** navigational grouping: related slices nested in one folder inside a layer. It does
not change dependency rules, and each grouped slice stays as independent as before.

```text
entities/
├── payment/            ← slice group: no segments, no index.ts, no shared files
│   ├── invoice/        ← still a full, independent slice
│   │   ├── model/
│   │   ├── ui/
│   │   └── index.ts
│   ├── receipt/
│   └── transaction/
├── user/               ← ungrouped slices are fine alongside groups
└── product/
```

**A slice group is not a slice.** It has no `model`/`ui`/`api` segments, no public API, and code
shared by several slices in the group must **not** be placed in the group folder — push it down a
layer instead.

## When to introduce one

Introduce it when _all_ of these hold; otherwise leave the layer flat:

1. Several slices sharing one business context are scattered across the layer.
2. The names obviously suggest the same topic.
3. The layer has grown past what you can take in at a glance.

Do not introduce one when names alone already navigate well, when there is no natural grouping
criterion, or when only two or three slices would end up inside.

## Per layer

- **entities** — group by domain proximity (`payment/{invoice,receipt,transaction}`).
- **pages** — group by topic when you have list/detail/create/edit variants
  (`order/{list,detail,create}`).
- **features** — allowed, but hardest to get right: a feature usually spans several entities, so
  the criterion is often missing. A group like `features/cart/` without a clear criterion starts
  absorbing cart DTOs and mappers and quietly becomes a home for the whole domain, which breaks
  the rule that features are split by _use case_. Check first that there are enough slices, and
  that only feature slices — not stray entity code — ended up inside.

Scaffold one with the CLI by passing a slash path: `fsd f employee/employee-record`
(`tooling/fsd-cli.md`).

Docs: <https://feature-sliced.design/docs/reference/slice-groups>
