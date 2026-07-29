# Report format

## Contents

- Template
- Rules for filling it in
- Worked example

## Template

```markdown
# Skill review — <skill-name>

`<path/to/skill>` · reviewed <YYYY-MM-DD> · depth: full | quick

## Scores

| Criterion                       | Score | Level      | Justification    |
| ------------------------------- | ----- | ---------- | ---------------- |
| C1 Discovery & Activation       | 4     | Exemplary  | <one line>       |
| C2 Clarity & Concision          | 3     | Proficient | <one line>       |
| C3 Information Architecture     | 3     | Proficient | <one line>       |
| C4 Actionability                | 2     | Developing | <one line>       |
| C5 Executable Assets            | N/A   | —          | Ships no scripts |
| C6 Evaluation & Maintainability | 2     | Developing | <one line>       |

**Overall: 2.80 / 4 — Proficient.** Ship after the fixes below.
<If the gate fired: "**Gate:** C6 scored 1; band capped at Developing regardless of the mean.">

## Findings

### C2 — Proficient (3)

**Evidence.** `SKILL.md:41` — "PDF files are a common file format that contains text…"

**Why this level.** Content is mostly load-bearing, but this passage explains a format the
model already knows, which is the Proficient descriptor's "isolated paragraphs of general
background".

**Highest-value change.** Delete lines 41–47; open the section at the extraction snippet.

### C4 — Developing (2)

<same three parts>

## Prioritized fixes

1. **`SKILL.md:3`** — rewrite the description to name trigger situations, not just the
   capability. Lifts C1 2 → 3. (5 minutes)
2. **`SKILL.md:24`** — define `handlePromise` and `safeAsync` with real bodies, or link a file
   that does. Lifts C4 2 → 3. (20 minutes)
3. **new `evals/`** — record three scenarios with observable expected behaviors. Lifts C6
   1 → 3. (1 hour)

## Re-score condition

Re-run after fixes 1 and 2 land. Expect ≥ 3.00 (Proficient). The Exemplary band needs fix 3,
because the gate stays armed while C6 sits at 1.
```

## Rules for filling it in

- **One row per criterion, always six rows.** `N/A` appears as a row, never as an omission.
- **Findings only for criteria below 4.** A criterion at 4 needs no defense beyond its
  one-line justification in the table.
- **Every finding has all three parts** — evidence, why this level, highest-value change — in
  that order. Evidence is `file:line` plus quoted text, or the command and its output.
- **One highest-value change per finding.** A list of six suggestions is a rewrite, not a
  review; the prioritized-fix section is where breadth goes.
- **Order fixes by score gain per unit of effort**, not by criterion number. Include a rough
  time estimate — it is what makes the ordering actionable.
- **Name the gate whenever it fires**, next to the overall score, with the criterion that
  triggered it.
- **State sampling.** If the skill was too large to read exhaustively, say which files were
  read and which were sampled, before the score table.

## Worked example

Reviewing `skills/ts-code-writing` in this repository — a real, short skill, scored against the
rubric.

```markdown
# Skill review — ts-code-writing

`skills/ts-code-writing` · reviewed 2026-07-29 · depth: full

## Scores

| Criterion                       | Score | Level      | Justification                                                                        |
| ------------------------------- | ----- | ---------- | ------------------------------------------------------------------------------------ |
| C1 Discovery & Activation       | 2     | Developing | Description states when, not what; claims all of TypeScript, covers four conventions |
| C2 Clarity & Concision          | 2     | Developing | Every code example is a placeholder body                                             |
| C3 Information Architecture     | 4     | Exemplary  | 39 lines, single file, correctly unsplit at this size                                |
| C4 Actionability                | 2     | Developing | Two async helpers offered with no rule for choosing, and neither is defined          |
| C5 Executable Assets            | N/A   | —          | Ships no scripts                                                                     |
| C6 Evaluation & Maintainability | 1     | Novice     | No evaluations, no baseline, no provenance                                           |

**Overall: 2.20 / 4 — Developing.** Revise and re-score before use.
**Gate:** C6 scored 1; band capped at Developing regardless of the mean. Here the mean was
already Developing, so the cap changed nothing — but C6 must reach 2 before any higher band is
reachable.

## Findings

### C1 — Developing (2)

**Evidence.** `SKILL.md:3` — "Use when making a software implementation using typescript
language."

**Why this level.** The description states _when_ but never _what the skill does_, and its
claimed scope is all TypeScript implementation work while the body covers four conventions
(functional style, no `any`, const arrow functions, async helpers). That is the Developing
descriptor twice over: what-without-when inverted, and coverage claimed beyond the contents.

**Highest-value change.** Rewrite as: "Applies this project's TypeScript conventions —
functional style, immutability, no `any`, const arrow functions, and the `safeAsync` /
`handlePromise` error-handling wrappers. Use when writing or refactoring TypeScript."

### C2 — Developing (2)

**Evidence.** `SKILL.md:19` — `const fn = () => {};`; `SKILL.md:28-30` — `() => {}, // promise`
/ `() => {}, // on success` / `(err) => {}, // on failure`.

**Why this level.** Every fenced example is an empty placeholder body. The Developing
descriptor names abstract placeholders explicitly. The surrounding rules are genuinely
non-obvious house convention, which is why this is a 2 and not a 1.

**Highest-value change.** Replace the `handlePromise` block with one real call — an actual
fetch, an actual success handler, an actual error branch.

### C4 — Developing (2)

**Evidence.** `SKILL.md:24` — "Create the helpers if they do not exists."; `SKILL.md:27` and
`SKILL.md:35` present `handlePromise` and `safeAsync` with no selection rule.

**Why this level.** Two alternatives are offered with no stated default, which is the
Developing descriptor's "alternatives offered without a default". The instruction to create the
helpers is also unexecutable as written — no signature, no semantics, no return contract — but
the code fences give enough shape to keep this above Novice.

**Highest-value change.** State the rule ("use `safeAsync` by default; use `handlePromise`
when the call sites differ per branch") and give both helpers real implementations.

### C6 — Novice (1)

**Evidence.** `find skills/ts-code-writing -iname '*eval*' -o -iname '*test*'` returns nothing;
no URL or version appears in any file.

**Why this level.** No evaluation scenarios, no baseline, no record of testing, and no claim
traceable to a source — the Novice descriptor in full.

**Highest-value change.** Record three scenarios ("implement a paginated fetch", "refactor a
`Promise.all` chain", "type a discriminated union reducer") with observable expected behaviors.

## Prioritized fixes

1. **`SKILL.md:3`** — rewrite the description per C1 above. Lifts C1 2 → 4. (5 minutes)
2. **`SKILL.md:24-39`** — define both helpers and state the selection rule. Lifts C4 2 → 4 and
   C2 2 → 3 together. (30 minutes)
3. **`SKILL.md:20`, `SKILL.md:28-30`** — replace placeholder bodies with real calls. Lifts C2
   3 → 4. (15 minutes)
4. **new `evals/ts-code-writing.json`** — three scenarios with expected behaviors. Lifts C6
   1 → 3 and disarms the gate. (1 hour)

## Re-score condition

Re-run after fixes 1–3. Expect 3.00 (Proficient) once the gate is disarmed by fix 4; without
fix 4 the band stays capped at Developing no matter how high C1–C4 go.
```

Note what the example demonstrates: `N/A` on C5 without penalty, a gate that fires without
changing the band, a fix that lifts two criteria at once, and evidence that is a command's
output rather than a line citation where no line exists.
