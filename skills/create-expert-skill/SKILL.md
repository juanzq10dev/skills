---
name: create-expert-skill
description: >
  Use when asked to create, generate, regenerate, or update a "library expert" skill
  from a documentation URL, docs site, llms.txt, or GitHub repository — i.e. any request
  like "make a skill for <library>", "build a <library>-expert skill", "turn these docs
  into a skill", or "update the <library> skill to the new version".
---

# Create Expert Skill

Takes a documentation URL and emits a conforming `<library>-expert` skill: a skill that makes
an agent competent at one library by routing it to distilled documentation instead of letting
it answer from parametric memory.

`references/spec.md` is the normative contract — layout, `SKILL.md` shape, front-matter
schema, content rules, conformance checklist. Read it before emitting anything.

Note: this generator ships `scripts/`, which the contract forbids. That rule constrains
*generated* expert skills, not the generator. Generated skills MUST NOT contain `scripts/`.

## Inputs

Required: a documentation URL, or a library name from which one can be resolved.

Optional, ask only if the answer is not derivable: target version, and output path
(default `skills/<library>-expert/`).

## Step 1 — Acquire

Tiered, cheapest first. Do not skip to a lower tier while a higher one is producing.
Full tactics in `references/acquisition.md`.

1. `<domain>/llms.txt` or `/llms-full.txt` — the convention exists precisely for this;
   many modern docs sites (Vercel, Stripe, Astro, Svelte, LangChain…) ship it. Try it
   before anything else.
2. `sitemap.xml` → filter to doc paths.
3. The GitHub repo: `README`, `CHANGELOG`, `docs/`, and the source/type stubs
   (`.d.ts`, `.pyi`) — signatures from source beat prose from docs.
4. Page-by-page `WebFetch` following nav, as a last resort.

Budget it: ~15–40 high-value pages, not the whole site. Prioritize getting-started, core
concepts, the API reference for main entry points, migration guides, and FAQ/troubleshooting
(troubleshooting pages are disproportionately valuable — they're a list of the traps).

Write the fetched corpus to a scratch directory, one file per source page, each recording
its source URL. The corpus is working material — it is **not** the skill, and copying it
into `references/` fails the anti-goal in `references/spec.md` §1.

## Step 2 — Determine version

Pin it. A library skill without a version is a liability. Resolve the exact version the
fetched docs describe, record it, and carry it into the generated skill. Resolution order
and provenance format: `references/versioning.md`.

## Step 3 — Emit

Derive the skeleton from the library's own table of contents, distill the corpus into
leaves and stubs, write the hub judgment prose, add front matter, then generate the
indexes. Procedure: `references/emit.md`. Index algorithm and marker rules:
`references/index-algorithm.md`.

The distillation and the hub judgment prose are the load-bearing parts. A structurally
perfect skill whose leaves are copied doc prose has failed.

## Step 4 — Lint

Run every invariant and iterate until clean:

```bash
python3 skills/create-expert-skill/scripts/skillgen.py validate <skill-root>
```

Reachability is the one that matters most — it proves the tree is a tree and not a pile of
files. The full list and the failure playbook: `references/invariants.md`.

## Rules

- **Never invent API surface.** Every fenced invocation must trace to a fetched page or to
  source read in step 1. If the corpus does not cover something, emit a stub with the
  upstream URL instead of guessing — a stub is a first-class outcome (`spec.md` §5.2).
- **Distill, do not mirror.** If output is mostly prose copied from upstream, start over.
- **Let the library's own table of contents pick the directories** (`spec.md` §7.1).
- **Generated skills ship no executable assets** (`spec.md` §3.1, §8).
- **Indexes are generated, never hand-written** (`references/index-algorithm.md`).
