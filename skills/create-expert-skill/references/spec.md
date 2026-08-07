# The library-expert contract

Normative. Keywords **MUST**, **SHOULD**, **MAY** carry their usual force. This file defines
what a conforming `<library>-expert` skill *is*; the step files define how to produce one.

Derived by generalization from `dagster-expert` v1.13.1 (173 markdown files, ~208 KB), which
is treated throughout as the canonical instance.

Companion normative files: `index-algorithm.md` (index generation) and `invariants.md` (the
seven conformance invariants).

## Contents

1. [Design thesis](#1-design-thesis)
2. [Terminology](#2-terminology)
3. [Layout](#3-layout)
4. [`SKILL.md` contract](#4-skillmd-contract)
5. [Reference file contract](#5-reference-file-contract)
6. [Conformance checklist](#6-conformance-checklist)
7. [Canonical instance](#7-canonical-instance)
8. [Non-goals](#8-non-goals)

## 1. Design thesis

Four ideas. Output that drops any of them looks like the template but does not work like it.

1. **Progressive disclosure.** Exactly one file is always in context (`SKILL.md`, ~7 KB).
   Every other byte is loaded on demand, by an explicit read, only when the task needs it.
   A 208 KB corpus costs ~7 KB of baseline context.
2. **Routing over recall.** `SKILL.md` is not a tutorial. It is a dispatcher: a short
   behavioral preamble plus a generated index of entry points, each annotated with the
   situations that should trigger reading it.
3. **Distillation, not mirroring.** Reference files are compressed operational knowledge —
   invocations, decision rules, anti-patterns — not scraped documentation pages. Median leaf
   is ~430 bytes. The upstream URL is retained so the agent can escalate to full docs when
   the local file is insufficient.
4. **Mechanical structure.** The path layout mirrors the library's own namespace (command
   tree, module tree, integration list), so a name the user says maps to a file path without
   a search.

**The anti-goal:** this is not a documentation mirror, an `llms.txt` dump, or a RAG corpus.
If the output is mostly prose copied from upstream pages, it has failed regardless of
structural conformance.

## 2. Terminology

| Term | Meaning |
| --- | --- |
| **Skill root** | Directory containing `SKILL.md` and `references/`. The unit this contract defines. |
| **Entry point** | A file listed in `SKILL.md`'s generated index. Reachable in one hop. |
| **Hub** | An `INDEX.md` that owns a subtree and carries its own generated index. Declared with `type: index`. |
| **Stub** | A leaf `INDEX.md` that is title + triggers + upstream URL and little else. |
| **Leaf** | A non-index reference file holding actual content. |
| **Trigger** | A front-matter phrase describing *when* to read a file. Becomes the index annotation. |
| **Transparent directory** | A directory with no `INDEX.md`; its children are flattened into the parent's index. |

## 3. Layout

### 3.1 Skill core (normative)

```
<library>-expert/                     # skill root; name MUST be kebab-case
├── SKILL.md                          # REQUIRED — the only always-loaded file
└── references/                       # REQUIRED — every other file lives here
    ├── <topic>.md                    # flat leaf, top-level concept
    ├── <topic>/
    │   ├── INDEX.md                  # hub (type: index) or stub (no type)
    │   └── <subtopic>.md
    └── <namespace>/                  # mirrors the library's own namespace
        └── <command-or-module>/
            ├── INDEX.md
            └── <operation>.md
```

- The skill root **MUST** contain `SKILL.md` and `references/`, and no other top-level entries.
- All reference content **MUST** live under `references/`. No sibling `docs/`, `examples/`,
  or `templates/` — they create a second routing mechanism that `SKILL.md` does not describe.
- Executable assets (`scripts/`, binaries) **MUST NOT** be included. This is a
  documentation-routing skill; it ships no code the agent runs.
- Directory nesting under `references/` **SHOULD NOT** exceed 3 levels (canonical instance:
  max 3, i.e. `references/cli/api/asset/get.md`).
- Hub files **MUST** be named `INDEX.md` (uppercase). The generator keys on this exact name.

### 3.2 Packaging wrapper (optional)

Distribution as a plugin adds a wrapper *around* the skill root. The core layout is
unchanged; this is packaging only, and the core **MUST** be emittable without it.

```
<library>-expert/                     # plugin root
├── .claude-plugin/plugin.json        # { name, description, version }
├── .cursor-plugin/plugin.json        # + displayName, author, publisher, homepage,
│                                     #   repository, license, logo, keywords, skills: "./skills/"
└── skills/<library>-expert/          # ← the skill root from §3.1
```

Keep logo assets inside the plugin root, so the plugin directory stays self-contained when
copied. (The canonical instance points `logo` outside its plugin root; do not copy that.)

For a plain skills repository, place the skill root at `skills/<library>-expert/` directly.

## 4. `SKILL.md` contract

### 4.1 Front matter

```yaml
---
name: <library>-expert
description: >
  Expert guidance for working with <Library> [and the <cli> CLI].
  ALWAYS use before doing any task that requires knowledge specific to <Library>,
  or that references <domain nouns: 3-6 terms the user is likely to say>.
  Common tasks may include <4-8 task phrasings>.
---
```

- `name` **MUST** equal the skill root directory name.
- `description` is the *only* selection signal available before the skill loads. It **MUST**
  contain (a) an ALWAYS-use directive, (b) the library's distinctive domain nouns, and (c)
  concrete task phrasings. Optimize for recall against user wording, not brevity. Canonical
  instance: 4 lines, ~430 characters.

### 4.2 Body sections

In order. REQUIRED sections **MUST** be present.

| # | Section | Req. | Content |
| --- | --- | --- | --- |
| 1 | `## Core <Library> Concepts` | REQUIRED | 2–5 one-line definitions of terms used throughout the index. Definitions only — explicitly deferring detail to reference files. |
| 2 | `## <Primary Workflow>` | SHOULD | The one workflow the library is mostly used for, as a pointer to a hub. |
| 3 | `## <CLI or Primary Interface>` | SHOULD | Which tool is canonical, how it is installed, and machine-readable output flags (`--json`) to prefer. Omit for library-only targets. |
| 4 | `## <Environment / Toolchain>` | MAY | Package-manager or runtime conventions. |
| 5 | `## CRITICAL: Always Read Reference Files Before Answering` | REQUIRED | Anti-hallucination rule, §4.3. |
| 6 | `## Reference Index` | REQUIRED | The generated block. |

Budget: **SHOULD** be ≤ 120 lines / ≤ 8 KB including the generated index (canonical: 78
lines, 7.2 KB). If the generated index alone exceeds ~40 entries, promote subtrees to hubs
(§5.3) rather than growing the file.

### 4.3 Required behavioral rules

**MUST** appear, adapted in wording but not in force:

1. **No answering from memory.** "NEVER answer from memory or guess at commands, APIs, or
   syntax. ALWAYS read the relevant reference file(s) from the Reference Index below before
   responding. For every question, identify which reference file(s) are relevant using the
   index descriptions, read them, then answer based on what you read."
2. **Prefer the library's own tooling** over ad-hoc file reading, where the library ships a
   CLI or introspection API.
3. **Do not explore the project unless necessary.** Listing and reading user files is
   wasteful when the library's tooling already reports structure.

Rules 2 and 3 apply only to libraries with a CLI/introspection surface; omit them otherwise.
Rule 1 is unconditional — it is the reason the skill exists.

## 5. Reference file contract

### 5.1 Front matter schema

Every `.md` under `references/` **MUST** begin with YAML front matter. Unknown keys are an
error.

```yaml
---
title: string            # REQUIRED. Human-readable; becomes the index link text.
triggers:                # REQUIRED. Non-empty list of strings.
  - "when to read this"  # Situation phrases, semicolon-joined into the index annotation.
type: index              # OPTIONAL. Literal "index" only. Legal on INDEX.md only.
---
```

- `title` **SHOULD** match the user-facing name of the thing documented (command name, API
  name, concept name), so index text matches user vocabulary.
- `triggers` entries **MUST** be phrased as *situations*, not as descriptions of contents.
  They are the retrieval keys; comma-separated keyword runs are acceptable when the surface
  is broad.
- `type: index` **MUST** be set on any `INDEX.md` that should own a generated child index,
  and **MUST NOT** be set on leaves.

### 5.2 File taxonomy

| Kind | Front matter | Body | Typical size |
| --- | --- | --- | --- |
| **Leaf** | title, triggers | `##` sections, fenced invocations, decision rules, anti-patterns | 300 B – 4 KB |
| **Hub** (`type: index`) | title, triggers, type | Orientation prose + decision hierarchy + generated child index | 1 – 10 KB |
| **Stub** | title, triggers | `# <name>` + `Docs: <upstream URL>` | ~110 – 250 B |

Stubs are a first-class outcome, not a failure. The canonical instance ships 56 of them (one
per integration library). A stub asserts *"this exists, here is its exact name and its
upstream docs"* — the fact the model most often lacks — without paying context for content
it usually does not need.

### 5.3 When to create a hub

Create `INDEX.md` with `type: index` for a directory when **any** holds:

- it contains ≥ 4 sibling files, **or**
- it contains subdirectories, **or**
- choosing among its children requires a decision rule the children cannot state individually.

Otherwise leave the directory transparent (no `INDEX.md`) and let its children surface
directly in the parent index.

A hub's prose **SHOULD** carry what no leaf can: selection hierarchies ("use the FIRST option
that applies: 1… 2… 3…"), preference rules ("ALWAYS prefer X over Y unless…"), and blanket
prohibitions ("NEVER build a custom Z when a library Z exists"). This is the highest-value
content in the whole skill — it is judgment, and it is what upstream docs least often state.

### 5.4 Content rules

- **Distill, do not mirror.** A leaf answers "how do I do X" in the fewest tokens that stay
  correct. Strip narrative, marketing, changelogs, and duplicated conceptual preamble.
- **Show the invocation.** Every leaf documenting an operation **MUST** contain at least one
  fenced code block with a runnable form, including the flags that matter.
- **Retain the escape hatch.** Files derived from upstream docs **SHOULD** carry the
  canonical URL, so the agent can fetch full docs when the local file is insufficient.
- **State anti-patterns explicitly.** Where the library has common misuse, a
  `## Common Anti-Patterns` list of `wrong → right` pairs is worth more than added prose.
- **No duplication across files.** A fact lives in exactly one file; others link to it. The
  reachability invariant makes cross-links safe.
- **Annotate uncheckable code fences.** Where a validation harness type-checks fenced blocks,
  fragments opt out via fence info strings — `nocheck` (skip entirely) and
  `nocheckundefined` (allow undefined names, still syntax/type-check).

## 6. Conformance checklist

```
Structure
  [ ] skill root = SKILL.md + references/ only; no scripts/, no executables
  [ ] directory nesting under references/ ≤ 3 levels
  [ ] hubs named exactly INDEX.md
Front matter
  [ ] every references/**/*.md has title + non-empty triggers, no unknown keys
  [ ] type: index only on INDEX.md, and on every INDEX.md owning subdirectories
  [ ] triggers phrased as situations, not as content descriptions
SKILL.md
  [ ] name matches directory; description has ALWAYS directive + domain nouns + task phrasings
  [ ] Core Concepts section (definitions only)
  [ ] CRITICAL "never answer from memory / always read references" rule present
  [ ] exactly one BEGIN/END GENERATED INDEX marker pair
  [ ] ≤ 120 lines / ≤ 8 KB
Content
  [ ] every operation leaf has ≥ 1 runnable fenced invocation
  [ ] hub prose carries selection hierarchies / preference rules / prohibitions
  [ ] upstream URL retained on doc-derived files
  [ ] no fact duplicated across files
Validation
  [ ] all relative links resolve
  [ ] BFS from SKILL.md reaches 100% of files (zero orphans)
  [ ] generator --check reports no drift
  [ ] code blocks pass lint/type-check or are explicitly annotated
```

## 7. Canonical instance

`dagster-expert` v1.13.1. Use as the worked example when instantiating.

| Element | Canonical instance |
| --- | --- |
| Skill root | `skills/dagster-expert/` (inside plugin wrapper) |
| `SKILL.md` | 78 lines, 7.2 KB, 31 indexed entry points |
| Core Concepts | Asset, Component (2 one-line definitions) |
| Primary workflow | "When integrating with ANY external tool, read `references/integrations/INDEX.md`" |
| Primary interface | `dg` CLI; `--json` preferred; `uv run` prefix |
| Corpus | 172 reference files, ~200 KB; 80 `INDEX.md` (18 hubs, 62 stubs), 92 leaves |
| Namespace mirror | `references/cli/api/<resource>/<verb>.md` ↔ `dg api <resource> <verb>` |
| Ecosystem section | `references/integrations/` — hub with a 4-level selection hierarchy + 56 stubs + 1 promoted hub |
| Transparent dirs | `automation/`, `cli/`, `components/`, `deployment/` |
| Sizes | leaf median 432 B, p90 3.7 KB, max 11.4 KB |
| Reachability | passes at 173/173 files |
| Evals | 9 benchmark tasks with JSON baselines |

Size budgets to target: median leaf ~430 B, p90 ~3.7 KB, max ~11 KB, total corpus ~200 KB.
Split any single file over ~12 KB.

### 7.1 Instantiation sketch

For a hypothetical `fastapi-expert`:

```
SKILL.md                       Core Concepts: Path Operation, Dependency, Router
                               CRITICAL rule; index of ~20 entry points
references/
  routing/INDEX.md             hub: path ops, params, response models
  dependencies/INDEX.md        hub: Depends, sub-dependencies, yield, security scopes
  cli/                         transparent — fastapi dev/run leaves
  integrations/INDEX.md        hub: selection rule (SQLModel vs SQLAlchemy vs raw)
    <adapter>/INDEX.md         stubs: pydantic, starlette, sqlmodel, alembic, …
  deployment/config-files.md   uvicorn/gunicorn, workers, ASGI settings
  migration/INDEX.md           pydantic v1 → v2, on_event → lifespan
```

Same shape, different namespace. Section names are not fixed by this contract — the mapping
rule is: **let the library's own table of contents pick the directories.**

## 8. Non-goals

- Not a documentation mirror or full-text search index.
- Ships no executable assets; the agent runs the library's real tooling, not skill code.
- Does not encode project-specific or user-specific conventions — those belong in
  `CLAUDE.md` or a separate skill, not in a library expert.
- Not version-parametric. One generated skill documents one version range; the version is
  recorded and the skill regenerated on upgrade.
