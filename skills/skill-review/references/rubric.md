# The skill-review analytic rubric

## Contents

- How to use this rubric
- Levels
- C1 — Discovery & Activation
- C2 — Instructional Clarity & Concision
- C3 — Information Architecture
- C4 — Actionability & Guidance Calibration
- C5 — Executable Assets & Operational Safety
- C6 — Evaluation & Maintainability
- Scoring math
- Gate rule and verdicts
- Resolving criterion overlap

## How to use this rubric

For each criterion, read the descriptors from `4` downward and stop at the first level the
skill **meets**; that level is the score. Descriptors are conjunctive — every clause must hold
for that level to apply.

Collect the evidence before choosing the number. Evidence is a `file:line` reference plus the
text it points at, or the output of a command from `evidence-checks.md`. A criterion scored
without evidence is not scored.

## Levels

| Level | Name       | Meaning                                                                                |
| ----- | ---------- | -------------------------------------------------------------------------------------- |
| 4     | Exemplary  | Meets the guidance and would survive review by the skill's own author six months later |
| 3     | Proficient | Meets the guidance with gaps that cost efficiency, not correctness                     |
| 2     | Developing | A real defect that will change agent behavior for the worse                            |
| 1     | Novice     | The criterion's purpose is not served at all                                           |

No midpoint. A skill that seems to sit between 2 and 3 is a 2 — the defect is real.

## Source of the numeric limits

The 64-char name limit, 1024-char description limit, 500-line `SKILL.md` limit, 100-line
table-of-contents threshold, and "at least three evaluations" bar are not house rules — they
are Anthropic's stated Agent Skills requirements and authoring guidance, at
`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` (frontmatter field
requirements) and `.../agent-skills/best-practices` (token budgets, table-of-contents
guidance, and the "at least three evaluations created" checklist item). Re-check these two
pages before treating a count-based clause as stale.

---

## C1 — Discovery & Activation

Judged on `name`, `description`, and whether the trigger surface the description claims
matches what the skill actually contains.

**4 — Exemplary.** `name` is kebab-case, at most 64 characters, free of reserved words
(`anthropic`, `claude`), and names the activity rather than a category. `description` is
written in third person and states both what the skill does and the situations that trigger
it, using the concrete nouns and task phrasings a user would actually type. The trigger
surface matches the contents: every situation the description claims is covered by content in
the skill, and every major content area is reachable from a claimed trigger. The skill covers
one coherent job.

**3 — Proficient.** `name` is valid and descriptive. `description` is third person and covers
both what and when, but its trigger vocabulary is generic ("when working with documents") or
omits phrasings a user would plausibly type. Contents match the claimed scope with at most
minor gaps.

**2 — Developing.** `name` is format-valid but vague (`helper`, `utils`, `tools`, `data`).
`description` states what the skill does but not when to use it, or is written in first or
second person ("I can help you…", "You can use this to…"). Or the skill spans two unrelated
jobs, or the description claims coverage the files do not contain.

**1 — Novice.** `name` violates the format rules (uppercase, spaces, over 64 characters,
reserved word) or carries no meaning. Or `description` is missing, empty, over 1024
characters, or a bare label ("Helps with documents", "Processes data") that cannot
distinguish this skill from a hundred others.

---

## C2 — Instructional Clarity & Concision

Judged on whether the loaded tokens carry knowledge the model does not already have.

**4 — Exemplary.** Every section adds context specific to this domain, tool, or house
convention; explanations of things the model already knows are absent. One fixed term per
concept throughout. Examples are concrete, with real inputs and real outputs. No instruction
is keyed to a date or a "before/after" condition; superseded guidance, if present, sits in a
clearly labeled legacy or deprecated section.

**3 — Proficient.** Content is mostly load-bearing, with isolated paragraphs of general
background that could be cut without loss. Terminology is consistent apart from one or two
synonym drifts. Examples are concrete but sparse in places. No time-keyed instructions in the
main flow.

**2 — Developing.** Substantial passages explain what the model already knows (what the file
format is, how HTTP works, why testing matters). Or terminology alternates between synonyms
for the same concept ("field" / "box" / "element"). Or examples are abstract placeholders
(`foo`, `do the thing`, `# process data here`). Or a main-flow instruction is conditioned on a
date or version window.

**1 — Novice.** Content is generic prose carrying no skill-specific knowledge — a reader
finishes it knowing nothing they did not know before. Or instructions contradict each other,
so following the skill produces different behavior depending on which section was read.

---

## C3 — Information Architecture

Judged on whether the right bytes reach context at the right time.

**4 — Exemplary.** `SKILL.md` is under 500 lines and reads as a router: it carries the rules
needed on every invocation and points elsewhere for detail. Every reference file is linked
directly from `SKILL.md` — one level deep, no reference-to-reference chains. Filenames name
their contents (`form-validation-rules.md`, not `doc2.md`). Files are split by domain, so a
task touching one domain loads none of the others. Reference files over 100 lines open with a
table of contents. All paths use forward slashes.

**3 — Proficient.** `SKILL.md` is under 500 lines and mostly routes, with some detail that
would be better split out. All references are one level deep and descriptively named. One or
more reference files over 100 lines lack a table of contents.

**2 — Developing.** `SKILL.md` carries detail that belongs in reference files, or approaches
or exceeds 500 lines. Or at least one reference file is reachable only through another
reference file, so it will be read partially or previewed with `head`. Or filenames do not
indicate contents. Or domains are mixed in one file, so an unrelated task pays for all of them.

**1 — Novice.** Everything is in one oversized `SKILL.md` with no split at all, or the
reference tree is two or more levels deep with no direct links from `SKILL.md`, or links
point at files that do not exist.

---

## C4 — Actionability & Guidance Calibration

Judged on whether an agent holding only this skill can act, and whether the specificity fits
the fragility of the task.

**4 — Exemplary.** Multi-step work is broken into numbered sequential steps, with a copyable
checklist for anything long enough to lose track of. Freedom matches fragility: exact commands
where operations are fragile or order-dependent, direction only where many paths succeed. Each
decision has one stated default, with a named escape hatch for the exception ("use X; for
scanned inputs use Y instead"). Quality-critical steps carry a validate → fix → re-validate
loop with an explicit pass condition. Required output shapes are given as templates.

**3 — Proficient.** Steps are ordered and followable. Freedom is broadly appropriate to the
task. Defaults are stated for most decisions. Validation is mentioned but its pass condition
is implicit ("check the output looks right").

**2 — Developing.** Multi-step work is presented as a flat list of facts with no ordering. Or
freedom is mismatched — rigid exact scripts for open-ended judgment work, or vague direction
for fragile sequences that must run in order. Or alternatives are offered without a default
("you can use A, or B, or C"). Or no verification step exists for work where errors are silent.

**1 — Novice.** No procedure at all — the reader learns what the domain is but not what to do.
Or the instructions cannot be executed as written: steps reference files, commands, or
variables that are never defined.

---

## C5 — Executable Assets & Operational Safety

**Score `N/A`** when the skill ships no scripts, directs no external tooling, and gives no inline
shell/code commands for the agent to run. `N/A` is correct, not a penalty and not a free 4.
(`evidence-checks.md`'s C5 file-finder only locates script files on disk — it does not decide
N/A by itself; a skill with inline commands and no script files still gets scored here.)

**4 — Exemplary.** Scripts handle their own error conditions — missing file, bad permission,
absent field — and recover or report actionably instead of raising to the caller. Every
configuration constant carries a comment justifying its value. All paths use forward slashes.
Required packages are named with install commands and are available in the target runtime. MCP
tools are referenced by fully qualified `Server:tool_name`. Each asset states whether it is to
be executed or read as reference. Destructive operations are gated behind a validation step.

**3 — Proficient.** Scripts handle the common failure paths; paths and dependencies are
correct. Minor gaps: an unexplained constant, or execute-versus-read intent left implicit.

**2 — Developing.** Scripts raise on ordinary conditions and leave recovery to the agent. Or
magic numbers appear with no justification (`TIMEOUT = 47`). Or packages are assumed present
with no install instruction. Or MCP tools are named without the server prefix. Or a
destructive operation runs with no validation ahead of it.

**1 — Novice.** Scripts are broken, or are never referenced from `SKILL.md` so nothing invokes
them. Or paths use Windows-style backslashes. Or instructions reference assets that do not
exist. Or a destructive operation is instructed with no confirmation and no reversal path.

---

## C6 — Evaluation & Maintainability

Judged on whether there is evidence the skill closes a real gap, and whether its claims can be
re-verified later.

**4 — Exemplary.** At least three evaluation scenarios are recorded, each with the query, the
input files, and observable expected behaviors — and each targets a gap the skill was written
to close. Baseline behavior without the skill is documented, so the delta is visible. The
record states what the skill was tested against (which models, which real tasks). Version- or
source-dependent claims cite their provenance.

**3 — Proficient.** Evaluation scenarios exist but number fewer than three, or their expected
behaviors are stated as outcomes ("produces a good summary") rather than observable criteria.
Some record of real-usage testing exists. Provenance is stated for most factual claims.

**2 — Developing.** Testing is asserted but not recorded — no scenarios, no expected
behaviors, no baseline, so no one can re-run it. Or factual claims (versions, API shapes,
flags) carry no source, so they cannot be re-verified when upstream changes.

**1 — Novice.** No evidence of testing of any kind, and no claim in the skill can be traced to
a source. Nothing distinguishes the content from something invented in one pass.

---

## Scoring math

- Each applicable criterion scores an integer `1`–`4`. C5 may instead be `N/A`.
- Overall score = arithmetic mean of the **applicable** criteria, to two decimals. An `N/A`
  criterion leaves both the numerator and the denominator — it is never counted as `0` and
  never counted as `4`. A markdown-only skill is therefore scored out of five criteria.
- Do not weight the criteria. Equal weights keep the argument on the evidence.

## Gate rule and verdicts

**Gate:** any criterion scored `1` caps the overall band at **Developing**, regardless of the
mean. One fatal flaw is not offset by five strong criteria. When the gate fires, the report
must say so and name the criterion that triggered it.

| Band       | Mean        | Verdict                                            |
| ---------- | ----------- | -------------------------------------------------- |
| Exemplary  | ≥ 3.50      | Ship.                                              |
| Proficient | 2.75 – 3.49 | Ship after the listed minor fixes.                 |
| Developing | 2.00 – 2.74 | Revise and re-score before use.                    |
| Novice     | < 2.00      | Rebuild from the gaps, not from the current draft. |

## Resolving criterion overlap

Criteria are independent by the failure they cause, not by the section text appears in. When
one passage triggers two criteria, score it under each for the distinct defect:

| Symptom                                           | Criterion  | Why                                  |
| ------------------------------------------------- | ---------- | ------------------------------------ |
| 900-line `SKILL.md`                               | C3         | Wrong bytes in context; split it     |
| …full of general background                       | C2 as well | Those bytes teach nothing; cut them  |
| Description promises what files lack              | C1         | Activation surface is wrong          |
| Steps exist but reference a missing script        | C4 and C5  | Unexecutable procedure; broken asset |
| Long reference file with no table of contents     | C3         | Partial reads lose scope             |
| "Always filter test accounts" stated once, buried | C4         | Rule not prominent enough to fire    |

Never score the same defect twice under one criterion to inflate its severity — use the fix
list ordering to convey urgency instead.
