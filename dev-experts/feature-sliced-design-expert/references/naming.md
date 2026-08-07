---
title: Naming conventions and FSD term collisions
triggers:
  - "choosing a name for a layer, slice or segment folder"
  - "the business vocabulary collides with FSD words like page, process or model"
  - "a team debates calling a folder store, views, ui-kit or core"
  - "Steiger reports fsd/typo-in-layer-name or fsd/inconsistent-naming"
---

# Naming

FSD fixes the vocabulary deliberately: teams otherwise call the same thing `ui` / `components` /
`ui-kit` / `views`, or `store` / `model` / `state` / `services`. Sticking to the standard terms is
what makes a project legible to a newcomer and what lets you ask the community for help.

```text
layers    app  processes(deprecated)  pages  widgets  features  entities  shared
segments  ui  model  lib  api  config
```

Layer names are **exact** — Steiger's `fsd/typo-in-layer-name` fails on `page/`, `entity/`,
`share/`. Slice names are yours, but keep pluralization consistent across a layer
(`fsd/inconsistent-naming`, `fsd/repetitive-naming`). Avoid slice names that collide with a
Shared segment name (`fsd/ambiguous-slice-names`).

Segment naming is governed by the purpose-not-essence test in `slices-segments.md`.

## Term collisions with the business domain

FSD words overlap with product words: `FSD#process` vs. a simulated process, `FSD#page` vs. a log
page, `FSD#model` vs. a car model. A developer reading "process" then loses time working out which
one is meant.

- **With the team:** prefix the methodology term — _"we can put this process on the FSD features
  layer."_
- **With non-technical stakeholders:** drop FSD terminology entirely and don't describe the
  internal structure of the codebase.

Docs: <https://feature-sliced.design/docs/about/understanding/naming>
