---
title: Migrating from FSD v1 (feature-slices)
triggers:
  - "a project uses the pre-v2 feature-slices layout"
  - "ui, lib and api sit at the src root instead of under shared"
  - "translating old folder names like flows, screens, views, containers or services"
---

# From v1 to v2

v1 preserved the same basic principles — a standardized structure, splitting by business logic
first, isolated features, and a public API with no reaching inside modules — but produced
boilerplate, non-obvious rules between abstractions, and implicit architectural decisions.

## Breaking changes

**Layers are now explicit at the top level**, and not everything is a feature or a page:

```text
app > processes > pages > features > entities > shared
```

The higher the layer, the more context it has; the lower the layer, the more dangerous a change to
it is, because lower layers are more widely used.

**Shared is now a real folder.** The infrastructure abstractions `ui/`, `lib/`, `api/` that used
to sit in the `src` root move under `src/shared/`. Business logic still does not belong in Shared —
lift it to `entities` or higher.

**Entities (and, then, Processes) were added** to reduce coupling. `entities` holds business
models (`user`, `order`, `blog`); `processes` held cross-page business flows.

> ⚠️ `processes` was introduced in v2 and has since been **deprecated**. Do not add it when
> migrating today — put router- and server-level logic in `app` instead (`../layers.md`).

## Renaming table

| v1 / other names                                                   | v2                                      |
| ------------------------------------------------------------------ | --------------------------------------- |
| `app`, `core`, `init`, `src/index`                                 | `app`                                   |
| `processes`, `flows`, `workflows`                                  | _(deprecated — use `features` + `app`)_ |
| `pages`, `screens`, `views`, `layouts`, `components`, `containers` | `pages`                                 |
| `features`, `components`, `containers`                             | `features`                              |
| `entities`, `models`, `shared`                                     | `entities`                              |
| `shared`, `common`, `lib`                                          | `shared`                                |
| `ui`, `components`, `view`                                         | `ui` segment                            |
| `model`, `store`, `state`, `services`, `controller`                | `model` segment                         |
| `lib`, `libs`, `utils`, `helpers`                                  | `lib` segment                           |
| `api`, `service`, `requests`, `queries`                            | `api` segment                           |
| `config`, `env`, `get-env`                                         | `config` segment                        |

After landing on v2, apply the v2.1 mental-model adjustment as well — `from-v2-1.md`.

Docs: <https://feature-sliced.design/docs/guides/migration/from-v1>
