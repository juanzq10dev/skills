---
title: Steiger rule reference
triggers:
  - "Steiger reported a rule name that needs explaining"
  - "deciding which rules to enable or disable for a project"
  - "looking for the rule that detects a specific FSD violation"
---

# Steiger rules (`@feature-sliced/steiger-plugin`)

Rules marked _[off]_ are disabled in `fsd.configs.recommended`.

| Rule                                  | Checks                                                                               | Fix                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------ | -------------------------------------------------------- |
| `fsd/forbidden-imports`               | imports from higher layers **and** cross-imports between slices on one layer         | `../layers.md`, `../issues/cross-imports.md`             |
| `fsd/no-cross-imports` _[off]_        | cross-imports only — the narrower half of the above                                  | `../issues/cross-imports.md`                             |
| `fsd/no-higher-level-imports` _[off]_ | higher-layer imports only — the other half                                           | `../layers.md`                                           |
| `fsd/public-api`                      | every slice (and every segment on a slice-less layer) declares a public API          | `../public-api.md`                                       |
| `fsd/no-public-api-sidestep`          | imports reaching past a slice's index into its internals                             | `../public-api.md`                                       |
| `fsd/no-layer-public-api`             | index files at the **layer** level                                                   | delete them; indexes belong on slices/segments           |
| `fsd/insignificant-slice`             | slices with one reference or none                                                    | merge into the single consumer — `../decomposition.md`   |
| `fsd/excessive-slicing`               | too many ungrouped slices, or too many in one group (threshold ~20)                  | merge, or introduce a slice group — `../slice-groups.md` |
| `fsd/no-segmentless-slices`           | slices with no segment folders at all                                                | `../slices-segments.md`                                  |
| `fsd/no-segments-on-sliced-layers`    | `ui`/`lib`/`api` sitting directly in `entities/`, `features/`, …                     | move them inside a slice                                 |
| `fsd/segments-by-purpose`             | segment names describing essence (`components`, `utils`, `types`)                    | `../issues/desegmentation.md`                            |
| `fsd/no-reserved-folder-names`        | subfolders inside a segment named after another segment                              | rename                                                   |
| `fsd/shared-lib-grouping`             | too many ungrouped modules in `shared/lib`                                           | group into focused libraries                             |
| `fsd/no-ui-in-app`                    | a `ui` segment on the App layer                                                      | move it to Widgets/Shared — `../layers.md`               |
| `fsd/no-processes`                    | use of the deprecated Processes layer                                                | move to `features` and `app`                             |
| `fsd/typo-in-layer-name`              | misspelled layer folders (`page/`, `share/`)                                         | `../naming.md`                                           |
| `fsd/inconsistent-naming`             | inconsistent pluralization across slice names                                        | `../naming.md`                                           |
| `fsd/repetitive-naming`               | a repeated part in every slice name on a layer (`pages/homePage`, `pages/aboutPage`) | drop the redundant suffix — `../naming.md`               |
| `fsd/ambiguous-slice-names`           | slice names matching a Shared segment name                                           | rename the slice                                         |
| `fsd/import-locality` _[off]_         | same-slice imports must be relative, cross-slice absolute                            | `../public-api.md`                                       |

Notes on the two most-misread rules:

- **`insignificant-slice`** exempts pages (they are entry points) and slices used only from the
  App layer (App shouldn't hold UI, so the code legitimately stays lower).
- **`excessive-slicing`**'s ~20 threshold is explicitly arbitrary upstream; treat a violation as a
  prompt to reconsider decomposition, not as a hard limit.

Docs: <https://github.com/feature-sliced/steiger#rules>
