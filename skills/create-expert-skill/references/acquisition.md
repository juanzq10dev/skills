# Step 1 — Acquisition

Goal: a scratch corpus of 15–40 high-value pages, each tagged with its source URL. Stop as
soon as the corpus covers the library's namespace. More pages is not better — the corpus is
input to distillation, and every extra page is a page someone has to compress or discard.

## Tier 1 — `llms.txt`

Try before anything else. Two files, both at the docs domain root:

```
https://<domain>/llms.txt        # curated index: titles + URLs + one-line summaries
https://<domain>/llms-full.txt   # entire docs corpus inlined, often 100 KB – 5 MB
```

Also try the docs subpath (`https://<domain>/docs/llms.txt`) — some sites mount it there.

`llms.txt` is usually the better input even when `llms-full.txt` exists: it *is* the
library's own table of contents, which is exactly what the skeleton step needs, and it maps
1:1 onto the `references/` skeleton. Fetch `llms-full.txt` for content only after the
skeleton is settled, and read it in slices — do not load a multi-megabyte file whole.

A 404 or an HTML error page means no `llms.txt`; fall through immediately.

## Tier 2 — `sitemap.xml`

```
https://<domain>/sitemap.xml
https://<domain>/sitemap_index.xml   # follow the child sitemaps it lists
```

Filter to doc paths (`/docs/`, `/guide/`, `/api/`, `/reference/`) and drop blog, changelog
archives, marketing, and localized duplicates (`/es/`, `/zh/`). The remaining URL path
structure is a usable proxy for the library's namespace when there is no `llms.txt`.

## Tier 3 — GitHub

Reach for this when the docs site is thin, JavaScript-rendered, or marketing-heavy.

| Source | Yields |
| --- | --- |
| `README` | install command, canonical hello-world, positioning |
| `CHANGELOG` | breaking changes, version boundaries, migration content |
| `docs/` | the docs site's actual markdown, without the site chrome |
| `.d.ts`, `.pyi`, `__init__.py` exports | the real public surface and exact signatures |
| `--help` output committed in docs, or CLI source | the command tree for `references/cli/` |

Signatures from source beat prose from docs. When the two disagree, source wins; note the
discrepancy in the relevant leaf.

Prefer raw fetches over the HTML UI:

```
https://raw.githubusercontent.com/<org>/<repo>/<ref>/README.md
```

Pin `<ref>` to the version tag resolved in step 2, not to `main`.

## Tier 4 — Page-by-page `WebFetch`

Last resort. Start at the docs landing page, extract the nav, and fetch depth-first through
the sections that matter. Hard-cap the count; do not crawl breadth-first.

If a fetch returns an empty shell or nav-only content, the site is client-rendered — stop
and go back to tier 3.

## Prioritization

Fetch in this order and stop when the budget is spent:

1. **Getting started / installation** — the canonical setup, and the package name.
2. **Core concepts** — the 1–3 central abstractions. These become `SKILL.md` §Core Concepts
   and the top-level hubs.
3. **API reference for main entry points** — only the entry points; long-tail API pages
   become stubs, not fetches.
4. **Migration guides** — every breaking change here is content the model would otherwise
   get wrong from memory. Highest value per byte in the whole corpus.
5. **FAQ / troubleshooting** — disproportionately valuable; they're a list of the traps, and
   they feed `## Common Anti-Patterns` sections (`spec.md` §5.4) and hub prohibitions.
6. **Integrations / plugins index** — fetch the *list*, not each entry. Each entry becomes a
   stub carrying its exact name and upstream URL.

Skip: blog posts, release announcements, conference talks, contributor guides, code of
conduct, and anything under `/about/`.

## Recording provenance

Each corpus file starts with the URL it came from and the fetch date. That URL is what gets
carried into the generated leaf as its escape hatch (`spec.md` §5.4), and it is what makes
regeneration on the next library release mechanical rather than archaeological.

```markdown
<!-- source: https://docs.example.com/guide/routing | fetched: 2026-07-28 -->
```
