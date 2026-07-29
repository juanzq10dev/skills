# Step 4 — Lint

Normative. A conforming skill **MUST** satisfy all seven invariants below.
`scripts/skillgen.py validate` enforces 1, 2, 3, 4 and 7 directly; 5 and 6 need the host
repo's toolchain. Iterate until clean — a skill that fails an invariant is not conforming,
regardless of how good its prose is.

```bash
python3 skills/create-expert-skill/scripts/skillgen.py validate skills/<library>-expert
```

| # | Invariant | Checked by |
| --- | --- | --- |
| 1 | Front matter valid — parses, non-empty `triggers`, no unknown keys | `validate` |
| 2 | Every relative markdown link resolves | `validate` |
| 3 | BFS from `SKILL.md` reaches every file — zero orphans | `validate` |
| 4 | No index drift | `validate` (and `generate --check`) |
| 5 | Fenced code blocks syntax- and type-check | host toolchain |
| 6 | `markdownlint` + formatter over all `.md` | host toolchain |
| 7 | `SKILL.md` ≤ 120 lines / ≤ 8 KB | `validate` |

## Invariant 3 is the load-bearing one

It proves the progressive-disclosure tree is actually a tree, and not a pile of files with an
index that happens to sit on top. An unreachable file is dead weight the agent can never
load — it costs repository size and zero capability. The canonical instance passes at
173/173.

Orphans almost always trace to one of:

- an `INDEX.md` with subdirectories but no `type: index` — the subtree was dropped by the
  walk (`index-algorithm.md`); fix by adding `type: index`
- a file added by hand after the last `generate` run — re-run `generate`
- a hub missing its marker pair, so its children were computed and then discarded
- a directory whose `INDEX.md` front matter fails to parse; the walk treats it as transparent,
  which can be silent — invariant 1 catches the parse failure

## Invariant 5 — code blocks

Fenced blocks in the library's primary language are syntax- and type-checked, with the
library's canonical import auto-prepended. For Python: `ruff` `F821` (undefined names) plus
`pyright --level error`.

Fragments that cannot be checked opt out via the fence info string:

- `nocheck` — skip entirely
- `nocheckundefined` — allow undefined names, still syntax/type-check

Use the narrower one where possible. A block marked `nocheck` is an unverified claim about
the library's API, which is exactly what this skill exists to avoid.

## Beyond the invariants

Structural conformance does not mean the skill works. A behavioral harness is RECOMMENDED,
and it is the only check that measures whether the skill *helps*:

- one test per representative task, prompt prefixed with the skill invocation
- **functional assertion first** — run the library's own tooling against the produced
  artifact to prove the task actually succeeded
- **then a baseline comparison** — persist a JSON baseline per task recording `cost_usd`,
  `execution_time_ms`, input/output tokens, `tools_used`, and a narrative of the steps taken

`tools_used` and the narrative are the diagnostic that matters: they show *which* reference
files the agent read, which is direct evidence about whether triggers are routing correctly.
**A task solved without reading any reference file means the index failed to trigger** — the
fix is the `triggers` phrasing in step 3d, not more content.

## Final pass

Walk the conformance checklist in `spec.md` §6 before declaring done. The two items a
generator most often fails are not mechanical: hub prose carrying real selection hierarchies
rather than summaries, and no fact duplicated across files.

The repository hosting generated skills SHOULD also wire `generate --check` into pre-commit
and CI, so invariant 4 cannot regress silently.
