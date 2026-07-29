# Step 2 — Determine version

Pin it. A library skill without a version is a liability: the agent cannot tell whether a
leaf describes the API it is about to call, and a skill that silently describes a superseded
major version is worse than no skill, because it is confidently wrong.

`spec.md` §8 is explicit that a generated skill is not version-parametric. One skill documents
one version range.

## Resolution order

Use the first that yields an exact version.

1. **The user said so.** If a version was named in the request, that is the target — fetch
   the docs for it, including switching to a versioned docs path (`/v2/`, `/1.13.1/`) if the
   site offers one.
2. **The docs site's version selector.** Most docs sites expose the current version in the
   nav or in the URL. Read it from the fetched pages.
3. **The registry.** The authoritative current release:
   - npm — `https://registry.npmjs.org/<pkg>/latest` → `.version`
   - PyPI — `https://pypi.org/pypi/<pkg>/json` → `.info.version`
   - crates.io — `https://crates.io/api/v1/crates/<crate>` → `.crate.max_stable_version`
   - Go — `https://proxy.golang.org/<module>/@latest` → `.Version`
4. **The GitHub latest release tag** — `/releases/latest`. Use when the package is not
   published to a registry, or is CLI-only.

If tiers 2–4 disagree, the docs site wins for *content* and the registry wins for the
*number*; note the mismatch, because it usually means the docs are ahead of or behind the
release, and that is itself something the skill should say.

## What "pin it" means concretely

Record the version in three places:

- **`SKILL.md`, in the description or a one-line header** — so it is visible before any
  reference file is read.
- **The plugin manifest** (`.claude-plugin/plugin.json` `version`), if the packaging wrapper
  in `spec.md` §3.2 is used; the version is recorded here and regenerated on upgrade.
- **Per-file source URLs**, pinned to the version where the docs site supports versioned
  paths, so a stale leaf is detectable by fetching its own URL.

Also record the **range**, not just the point release, when the API surface is stable across
it — `1.13.x`, or `>=0.115,<0.116`. The point release is what was read; the range is what the
content is actually true for. State it as a range only when the changelog supports it.

## Version boundaries become content

A migration guide crossing a major version is the single highest-value input in the corpus,
because it is precisely where parametric memory is stale. When one exists, `references/migration/`
is mandatory, with one leaf per migration path (`emit.md` §3a).

Where the previous major version is still widely deployed, name it explicitly in the leaf —
"in v1 this was `X`; in v2 it is `Y`" — rather than silently documenting only the current
form. The `wrong → right` anti-pattern form from `spec.md` §5.4 fits this exactly.

## Regeneration

On a library upgrade, do not hand-edit. Re-run the whole pipeline against the new version
and diff the output; the pinned per-file source URLs make the changed surface obvious.
