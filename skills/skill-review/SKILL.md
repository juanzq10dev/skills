---
name: skill-review
description: >
  Evaluates an Agent Skill against a six-criterion analytic rubric and returns per-criterion
  scores (1-4), the evidence behind each score, and a prioritized list of fixes. Use when
  asked to review, score, grade, critique, audit, or give feedback on a skill or SKILL.md,
  when asked whether a skill is good enough to ship, or after authoring a skill to check it
  before use.
---

# Skill Review

Scores a skill on six independent criteria and returns located, fixable feedback. Analytic,
not holistic: the deliverable is _where_ it fell short, not an overall impression.

## The rubric

Six criteria, four levels (`4 Exemplary` · `3 Proficient` · `2 Developing` · `1 Novice`).

| #   | Criterion                              | Failure it catches                                  |
| --- | -------------------------------------- | --------------------------------------------------- |
| C1  | Discovery & Activation                 | Skill never loads, or loads for the wrong task      |
| C2  | Instructional Clarity & Concision      | Loads, but spends context on what the model knows   |
| C3  | Information Architecture               | Content exists but is unreachable or read partially |
| C4  | Actionability & Guidance Calibration   | Readable, but the agent still cannot act            |
| C5  | Executable Assets & Operational Safety | Bundled scripts fail, mislead, or damage            |
| C6  | Evaluation & Maintainability           | No evidence the skill improves anything             |

The 24 level descriptors, the `N/A` rule for C5, the scoring math, and the gate rule live in
[references/rubric.md](references/rubric.md). **Read it before scoring** — scoring from this
table alone produces impressions, which is the exact failure this skill exists to prevent.

## Review workflow

Copy this checklist into the response and check items off:

```
Review Progress:
- [ ] Step 1: Inventory the target skill
- [ ] Step 2: Read the rubric
- [ ] Step 3: Run mechanical checks
- [ ] Step 4: Read the reference files
- [ ] Step 5: Score, evidence first
- [ ] Step 6: Compute band and verdict
- [ ] Step 7: Emit the report
- [ ] Step 8: Verify the report
```

**Step 1 — Inventory.** Read the target `SKILL.md` in full. List everything under the skill
root (`find <root> -type f`). Note whether it ships scripts, or directs inline shell/code
commands with no script files present — either decides C5 applicability (rubric.md).

**Step 2 — Read the rubric.** [references/rubric.md](references/rubric.md), in full.

**Step 3 — Mechanical checks.** Run
[scripts/evidence-checks.sh](scripts/evidence-checks.sh) against the target root:
`bash scripts/evidence-checks.sh <root>`. It produces the objective half of the evidence: line
counts, front-matter limits, link resolution, reference depth. Read
[references/evidence-checks.md](references/evidence-checks.md) for what each section means
and cannot tell you. Skip only when the user asked for a quick review.

**Step 4 — Read the references.** Read every reference file in the target skill. If the skill
totals over 2,000 lines across `SKILL.md` and its references, say so in the report and name
which files were sampled — never let an unread file go unmentioned.

**Step 5 — Score, evidence first.** For each criterion: write the evidence (`file:line` plus
the quoted text), _then_ pick the level whose descriptor that evidence matches. Never pick a
number and hunt for support.

**Step 6 — Band and verdict.** Mean of applicable criteria, then apply the gate rule from
`rubric.md`. `N/A` criteria leave the numerator and the denominator.

**Step 7 — Report.** Use [references/report-template.md](references/report-template.md).

**Step 8 — Verify.** Re-read the draft against `report-template.md`'s rules. Pass condition:
every finding below 4 has evidence, why-this-level, and one highest-value change, and every
criticism names a `file:line`. Drop or locate any claim that fails.

## Rules

- **Every criticism cites a location.** A claim without a `file:line` is not admissible in the
  report. This is the rule that separates a review from a reaction.
- **Score the skill as written, not as intended.** If the description promises coverage the
  files do not contain, that is a C1 defect, not a rounding error.
- **Report; do not rewrite.** Fixes are proposed as edits with file and line. Apply them only
  when the user asks for that as a separate action.
- **Domain correctness is out of scope.** Whether an htmx skill's htmx advice is true is not
  scored. Whether it is discoverable, concise, routable, actionable, safe, and tested is.
- **State the gate when it fires.** A capped band is the most surprising output this skill
  produces; it must never appear without the reason next to it.
- **N/A is only for C5**, and only when the skill ships no scripts, drives no external
  tooling, and directs no inline shell/code commands (rubric.md). Every other criterion
  applies to every skill.
