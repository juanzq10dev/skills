# Step 3 — Emit

Turns the scratch corpus into a conforming skill root. Read `spec.md` alongside this file —
it is the contract; this is the order of operations.

Output path: `skills/<library>-expert/`, kebab-case, containing exactly `SKILL.md` and
`references/`. Nothing else. No `scripts/`, no `examples/`, no `templates/` (`spec.md` §3.1).

## Contents

- [3a — Derive the skeleton](#3a--derive-the-skeleton)
- [3b — Distill](#3b--distill)
- [3c — Author judgment](#3c--author-judgment)
- [3d — Front matter pass](#3d--front-matter-pass)
- [3e — Generate the indexes](#3e--generate-the-indexes)

## 3a — Derive the skeleton

Let the library's own table of contents pick the directories. The whole point of mirroring
the library's namespace is that a name the user says maps to a file path without a search.
Inventing a taxonomy destroys that property.

Sources for the namespace, in order: `llms.txt` section headings → docs nav → sitemap path
segments → the CLI command tree → the module/export tree.

Recurring shapes:

| Directory | Create when | Shape |
| --- | --- | --- |
| `cli/` | the library ships a CLI | one file per command, mirroring the command tree |
| `<core-concept>/` | there are 1–3 central abstractions | hub + pattern/advanced leaves |
| `integrations/`, `plugins/` | there is an adapter ecosystem | hub with selection hierarchy + one stub per adapter |
| `automation/`, `deployment/`, `config/` | there are distinct operational modes | hub per mode |
| `migration/` | there are deprecated → current paths | one leaf per migration |

Constraints: nesting ≤ 3 levels; hubs named exactly `INDEX.md`.

Decide hub vs. transparent per directory using `spec.md` §5.3 — a hub is warranted at ≥ 4
sibling files, or any subdirectories, or when choosing among children needs a rule the
children cannot state individually. Otherwise leave the directory transparent (no `INDEX.md`)
and let its children surface directly in the parent index.

**Hard requirement:** any `INDEX.md` whose directory contains subdirectories MUST have
`type: index`. Without it the walk does not descend and the subtree silently vanishes from
every index (`index-algorithm.md`). `validate` catches this, but get it right when scaffolding.

## 3b — Distill

Per file, answer "how do I do X" in the fewest tokens that stay correct. Strip narrative,
marketing, changelog prose, and conceptual preamble already stated elsewhere. Full content
rules: `spec.md` §5.4.

Decide leaf vs. stub by expected demand.

**Leaf** — a surface the agent will actually need to operate. `##` sections, at least one
fenced runnable invocation *including the flags that matter*, decision rules, anti-patterns.
300 B – 4 KB.

**Stub** — a long-tail enumeration entry: title, triggers, `# <name>`, `Docs: <url>`.
~110–250 B. Stubs are a first-class outcome, not a failure — a stub asserts *"this exists,
here is its exact name and its upstream docs"*, which is the fact the model most often lacks,
without paying context for content it usually does not need.

Size budget: median leaf ~430 B, p90 ~3.7 KB, max ~11 KB, total corpus ~200 KB. Split
anything over ~12 KB.

The rules violated most often in practice:

- **No fact lives in two files.** Link instead. Reachability makes cross-links safe.
- **Every operation leaf has ≥ 1 fenced invocation.** A leaf that only describes an
  operation in prose has not been distilled.
- **Keep the upstream URL** on every doc-derived file.
- **State anti-patterns explicitly.** A `## Common Anti-Patterns` list of `wrong → right`
  pairs is worth more than added prose, and the troubleshooting pages fetched in step 1 are
  where they come from.
- **Never invent.** If the corpus does not cover it, emit a stub with the upstream URL.

## 3c — Author judgment

This stage is not extractive. It is the stage a naive scraper skips and the one that
determines whether the skill is useful.

**Hub prose** carries what no leaf can, and what upstream docs least often state:

- selection hierarchies — "use the FIRST option that applies: 1… 2… 3…"
- preference rules — "ALWAYS prefer X over Y unless…"
- blanket prohibitions — "NEVER build a custom Z when a library Z exists"

If a hub's prose is a summary of its children rather than a rule for choosing among them, it
is not doing its job.

**`SKILL.md` body** — six sections in the order fixed by `spec.md` §4.2: Core Concepts →
Primary Workflow → Primary Interface → Environment → the CRITICAL rule → Reference Index.
Section 5 must appear with its force intact — it is the reason the skill exists:

> NEVER answer from memory or guess at commands, APIs, or syntax. ALWAYS read the relevant
> reference file(s) from the Reference Index below before responding. For every question,
> identify which reference file(s) are relevant using the index descriptions, read them, then
> answer based on what you read.

Add "prefer the library's own tooling over ad-hoc file reading" and "do not explore the
project unless necessary" only when the library has a CLI or introspection surface.

Budget: ≤ 120 lines / ≤ 8 KB including the generated index. If the index alone exceeds ~40
entries, promote subtrees to hubs rather than growing the file.

**Front matter for `SKILL.md`** — `name` MUST equal the directory name. `description` is the
only selection signal available before the skill loads, so optimize it for recall against
user wording, not brevity: an ALWAYS-use directive, the library's distinctive domain nouns
(3–6 terms the user is likely to say), and 4–8 concrete task phrasings (`spec.md` §4.1).

## 3d — Front matter pass

Every file under `references/` gets `title` + non-empty `triggers`, plus `type: index` on
hubs. Unknown keys are an error. Schema and constraints: `spec.md` §5.1.

`title` should match the user-facing name of the thing documented, so index text matches user
vocabulary.

`triggers` are the retrieval keys, and they are what the index annotation is built from.
Phrase them as **situations**, drafted from anticipated user phrasings — not as descriptions
of file contents, and not from the file's own title.

```yaml
# right
triggers:
  - "validating project configuration or definitions"
  - "CI check fails and the cause is unclear"

# wrong
triggers:
  - "documentation for the check command"
```

## 3e — Generate the indexes

Never hand-write an index. Add the marker pair to `SKILL.md` and to every `type: index` hub:

```markdown
<!-- BEGIN GENERATED INDEX -->
<!-- END GENERATED INDEX -->
```

Then run the generator:

```bash
python3 skills/create-expert-skill/scripts/skillgen.py generate skills/<library>-expert
```

Algorithm and the three directory behaviors: `index-algorithm.md`. Then go to step 4 and
validate.
