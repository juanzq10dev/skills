# Mechanical evidence checks

## Contents

- How to use these checks
- Running the script
- C1 — front matter and activation
- C2 — clarity and concision
- C3 — architecture and reachability
- C4 — actionability
- C5 — executable assets
- C6 — evaluation record
- What these checks cannot tell you

## How to use these checks

[../scripts/evidence-checks.sh](../scripts/evidence-checks.sh) produces the objective half of the
evidence. It locates candidates; the rubric decides the score. A failing check is evidence for
a level, never the level itself — a skill can pass every check here and still score `2` on C2
for being full of background the model knows.

The numeric limits it enforces (64/1024/500/100/3) come from Anthropic's published Agent
Skills requirements — see `rubric.md`'s "Source of the numeric limits" for the two pages to
re-check if a count-based clause is ever in doubt.

## Running the script

```bash
bash scripts/evidence-checks.sh path/to/skill-under-review
```

It prints one `=== section ===` per check, in the order below. Skip running it only when the
user asked for a quick review — otherwise run it once and read every section; do not re-derive
these checks by hand.

If you change `evidence-checks.sh`, re-run its regression tests before trusting it again:

```bash
bash scripts/test-evidence-checks.sh
```

It builds synthetic fixture skills, asserts specific checks fire or don't (dead links,
reference-relative resolution, description-length measurement, the `[^)h]`-class regression),
and exits non-zero on any failure — unlike `evidence-checks.sh` itself, which always exits `0`
since it only gathers evidence.

## C1 — front matter and activation

- **`C1 — front matter`** — the raw YAML block, for quoting in evidence.
- **`C1 — name format`** — kebab-case, ≤64 chars, no reserved words, and matches the directory
  name (a mismatch means the skill will not resolve).
- **`C1 — description length (max 1024) and person`** — the byte count, plus any first-/second-
  person hits. First- or second-person hits _inside the description_ are a C1 defect; the same
  phrasing in the body is not — only the description is injected for selection.

## C2 — clarity and concision

- **`C2 — placeholder examples`** — abstract stand-ins (`foo`, `do the thing`) instead of real
  inputs/outputs.
- **`C2 — time-keyed instructions`** — main-flow guidance conditioned on a date or version
  window.
- **`C2 — terminology drift`** — edit the word list in the script for this skill's own central
  nouns. Multiple synonyms with comparable counts is the signal; one dominant term is fine.

## C3 — architecture and reachability

- **`C3 — SKILL.md line count`** — against the 500-line limit.
- **`C3 — reference-to-reference chains`** — links from `SKILL.md` are level one; any link
  _inside_ a reference file pointing at another local file is a level-two chain and a defect.
- **`C3 — dead links`** — every link target must exist, resolved relative to the file that
  contains it (not the skill root).
- **`C3 — orphaned reference files`** — files that exist but are linked from nowhere.
- **`C3 — long reference files missing a table of contents`** — over the 100-line threshold.
- **`C3 — Windows-style paths`** — backslash path separators.
- **`C3 — non-descriptive filenames`** — `doc1.md`, `notes.md`, and the like.

## C4 — actionability

- **`C4 — numbered or checklist-driven procedures`** — absence is a candidate defect for any
  skill whose task is multi-step.
- **`C4 — option buffets with no stated default`** — "or you can", "alternatively", with no
  recommended path.
- **`C4 — validation loops`** — presence of a validate → fix → re-validate pattern for
  quality-critical steps.

## C5 — executable assets

- **`C5 — script files on disk`** — this does not by itself decide `N/A`; see rubric.md's C5
  N/A trigger, which also covers skills that direct inline shell/code commands with no script
  files present.
- **`C5 — unjustified constants`** — a numeric assignment with no comment on or above its line.
- **`C5 — bare open/subprocess calls`** — Python file or network calls with no visible error
  handling nearby.
- **`C5 — scripts never referenced`** — a script that exists but that no `SKILL.md` or
  `references/*.md` file points to.
- **`C5 — MCP tools named without server prefix`** — inspect each hit; a `Server:tool_name`
  qualifier should be present.

## C6 — evaluation record

- **`C6 — evaluation scenarios, expected behaviors, baselines`** — greps for the vocabulary of
  recorded evaluations, plus a filename search for `*eval*`/`*test*`. A skill can mention the
  word "evaluation" in prose without having any — read the actual hits before crediting this.
- **`C6 — provenance for version- and source-dependent claims`** — URLs or dotted version
  numbers backing any factual claim the skill enforces on others. A skill full of
  version-specific claims and no URLs is a C6 candidate at `2`.

## What these checks cannot tell you

No section of the script decides:

- whether the description's trigger vocabulary matches how users actually phrase requests (C1),
- whether a paragraph teaches the model something it did not know (C2),
- whether the freedom level fits the fragility of the task (C4),
- whether the recorded expected behaviors are observable (C6).

Those are read-and-judge, every time. If the report's evidence consists only of script output,
the review has measured the skill without reading it.
