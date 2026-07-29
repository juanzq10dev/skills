# Index generation

Normative. `scripts/skillgen.py` implements this file; read it when scaffolding by hand or
debugging generator output. The file contract it operates on is `spec.md` §5.

## Markers

`SKILL.md` and every `type: index` hub contain exactly one marker pair. Content between the
markers is replaced wholesale on every run — never edit it by hand, the next run discards it.

```markdown
<!-- BEGIN GENERATED INDEX -->
<!-- END GENERATED INDEX -->
```

A file that requires markers and lacks them is a hard error, not a skip.

## Entry format

```
- [{title}]({link}) — {"; ".join(triggers)}
```

The ` — {triggers}` suffix is omitted when `triggers` is empty. Links are relative:
`./references/…` from `SKILL.md`, `./…` from within a hub.

## Walk

```
generate(skill_root):
    refs = skill_root/"references"
    validate_frontmatter(refs)          # every .md parses and satisfies spec.md §5.1; else fail
    skill_lines, deferred = walk(refs, rel="", link_prefix="references/")
    inject(skill_root/"SKILL.md", skill_lines)
    for hub_path, lines in deferred: inject(hub_path, lines)

walk(dir, rel, link_prefix) -> (lines, deferred):
    files = sorted(*.md in dir, excluding INDEX.md)
    dirs  = sorted(subdirs of dir)

    for f in files:
        emit(f, rel/f.name)                                  # leaf → entry in current index

    for d in dirs:
        if no d/INDEX.md or its front matter is unparseable:
            recurse into d, appending to the CURRENT index    # transparent directory
        elif d/INDEX.md has type == "index":
            emit(d/INDEX.md, rel/d.name/"INDEX.md")           # hub link in current index
            child_lines = walk(d, rel="", link_prefix="")     # children go to the hub
            deferred[d/INDEX.md] = child_lines
        else:
            emit(d/INDEX.md, rel/d.name/"INDEX.md")           # non-index INDEX.md
            for sibling in sorted(*.md in d, excluding INDEX.md):
                emit(sibling, rel/d.name/sibling.name)        # flattened into current index
```

## The three directory behaviors

All three must be implemented; each is used by real skills.

| `INDEX.md` state | Effect |
| --- | --- |
| absent | Directory is invisible; children recurse into the parent's index. |
| present, `type: index` | Directory becomes a hub; parent gets one link; children are injected into the hub. |
| present, no `type` | Parent gets the `INDEX.md` link **plus** flattened `.md` siblings. |

**Trap, inherited from the canonical implementation.** In the third case the walk does not
descend into subdirectories, so any nested directory under a non-`type: index` `INDEX.md` is
silently dropped from every index — the files still exist, nothing errors, and they become
permanently unreachable. Avoid it by setting `type: index` on any `INDEX.md` whose directory
contains subdirectories; `skillgen.py` hard-errors on the condition rather than silently
dropping the subtree. Reachability (`invariants.md`, invariant 3) is the backstop.

## Modes

```bash
skillgen.py generate <root>                   # regenerate and write in place
skillgen.py generate <root> --validate-only   # front-matter validation only, no writes
skillgen.py generate <root> --check           # regenerate in memory, diff, non-zero on drift
```

`--check` is the CI and pre-commit mode.
