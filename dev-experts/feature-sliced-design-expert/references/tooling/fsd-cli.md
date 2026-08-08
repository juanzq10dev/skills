---
title: fsd CLI — scaffolding layers, slices and segments
triggers:
  - "generating a new slice with its index file and segments"
  - "creating a slice inside a slice group from the command line"
  - "scaffolding the shared layer's segments"
---

# `@feature-sliced/cli`

Generates layer/slice/segment folders and index files. Not required — creating them by hand is
equally valid.

```bash
npm add -g @feature-sliced/cli   # provides the global `fsd` binary; or install locally + npx
```

```bash
fsd entities client --segments ui api    # long form
fsd e client -s ui,api                   # short form — layer, slice, segments
```

Layer names accept singular/plural/abbreviated forms (`e`/`entity`/`entities`,
`w`/`widget`/`widgets`, `f`/`feat`/`feature`, `p`/`page`/`pages`, `s`/`shared`). Segments accept
spaces or commas.

The CLI locates the **FSD root** automatically if the project already has at least one slice;
otherwise it generates in the current folder, or wherever `--root`/`-r` points.

```bash
fsd w bottom-bar -s ui api -r src
# → src/widgets/bottom-bar/index.(js|ts)   (extension inferred from the project)
#   src/widgets/bottom-bar/ui/
#   src/widgets/bottom-bar/api/

fsd f employee/employee-record
# → features/employee/employee-record/index.(js|ts)   — a slice inside a slice group

fsd p edit-note note-list -s ui,api
# → pages/edit-note/{index, ui/, api/} and pages/note-list/{index, ui/, api/}

fsd s ui api
# → shared/ui/index.(js|ts) and shared/api/index.(js|ts)   — one index per segment
```

Note the last case: on Shared the CLI produces **one public API per segment**, matching the rule
in `../public-api.md`.

Docs: <https://github.com/feature-sliced/cli>
