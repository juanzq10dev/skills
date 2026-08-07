#!/usr/bin/env python3
"""skillgen — index generator and validator for library-expert skills.

Implements references/index-algorithm.md and the mechanically checkable invariants from
references/invariants.md (1, 2, 3, 4, 7). Standard library only.

    skillgen.py generate <skill-root> [--check | --validate-only]
    skillgen.py validate <skill-root>
"""

from __future__ import annotations

import argparse
import sys
from collections import deque
from pathlib import Path
from re import compile as re_compile

BEGIN_MARKER = "<!-- BEGIN GENERATED INDEX -->"
END_MARKER = "<!-- END GENERATED INDEX -->"

ALLOWED_KEYS = {"title", "triggers", "type"}
# spec.md §4.2, §7: canonical instance (dagster-expert) SKILL.md is 78 lines, 7.2 KB.
SKILL_MD_MAX_LINES = 120
SKILL_MD_MAX_BYTES = 8 * 1024

# Markdown inline links: [text](target). Reference-style links are not used by the template.
LINK_RE = re_compile(r"\[[^\]]*\]\(([^)\s]+)")


class SkillError(Exception):
    """A conformance failure. The message is the user-facing diagnostic."""


# --------------------------------------------------------------------------- front matter


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_front_matter(path: Path) -> dict[str, str | list[str]] | None:
    """Parse the leading YAML front matter block, or return None if absent.

    Deliberately handles only the front-matter schema shape: flat `key: value` scalars and
    `key:` followed by indented `- item` lists. Anything else is a conformance error
    rather than a parser feature.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        raise SkillError(f"{path}: front matter opened but never closed")

    data: dict[str, str | list[str]] = {}
    current_key: str | None = None

    for lineno, raw in enumerate(text[4:end].split("\n"), start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t":
            item = raw.strip()
            if not item.startswith("- "):
                raise SkillError(f"{path}:{lineno}: expected a `- ` list item, got {raw.strip()!r}")
            if current_key is None:
                raise SkillError(f"{path}:{lineno}: list item before any key")
            bucket = data[current_key]
            if not isinstance(bucket, list):
                raise SkillError(f"{path}:{lineno}: `{current_key}` has both a value and list items")
            bucket.append(_strip_quotes(item[2:]))
            continue
        key, sep, value = raw.partition(":")
        if not sep:
            raise SkillError(f"{path}:{lineno}: not a `key: value` line: {raw.strip()!r}")
        current_key = key.strip()
        data[current_key] = _strip_quotes(value) if value.strip() else []

    return data


def validate_front_matter(path: Path, data: dict[str, str | list[str]] | None) -> None:
    """Enforce the reference front-matter schema on one file. Raises on the first violation."""
    if data is None:
        raise SkillError(f"{path}: missing YAML front matter")

    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        raise SkillError(f"{path}: unknown front-matter keys: {', '.join(unknown)}")

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        raise SkillError(f"{path}: `title` is required and must be a non-empty string")

    triggers = data.get("triggers")
    if not isinstance(triggers, list) or len(triggers) == 0:
        raise SkillError(f"{path}: `triggers` is required and must be a non-empty list")
    if any(not isinstance(t, str) or not t.strip() for t in triggers):
        raise SkillError(f"{path}: every `triggers` entry must be a non-empty string")

    if "type" in data:
        if data["type"] != "index":
            raise SkillError(f"{path}: `type` may only be the literal `index`")
        if path.name != "INDEX.md":
            raise SkillError(f"{path}: `type: index` is legal on INDEX.md only")

    # Without `type: index`, the walk does not descend and the subtree is
    # silently dropped from every index.
    if path.name == "INDEX.md" and data.get("type") != "index":
        if any(child.is_dir() for child in path.parent.iterdir()):
            raise SkillError(
                f"{path}: directory contains subdirectories, so `type: index` is required "
                f"(otherwise the subtree is dropped from all indexes)"
            )


# --------------------------------------------------------------------------- walk


def _entry(data: dict[str, str | list[str]], link: str) -> str:
    title = data["title"]
    triggers = data.get("triggers") or []
    suffix = f" — {'; '.join(triggers)}" if triggers else ""
    return f"- [{title}]({link}){suffix}"


def _link(link_prefix: str, rel: str, name: str) -> str:
    parts = [p for p in (link_prefix.strip("/"), rel.strip("/"), name) if p]
    return "./" + "/".join(parts)


def _md_files(directory: Path) -> list[Path]:
    return sorted(p for p in directory.glob("*.md") if p.name != "INDEX.md")


def walk(directory: Path, rel: str, link_prefix: str) -> tuple[list[str], dict[Path, list[str]]]:
    """The walk. Returns (lines for the current index, {hub path: its child lines})."""
    lines: list[str] = []
    deferred: dict[Path, list[str]] = {}

    for leaf in _md_files(directory):
        lines.append(_entry(parse_front_matter(leaf), _link(link_prefix, rel, leaf.name)))

    for sub in sorted(p for p in directory.iterdir() if p.is_dir()):
        index_path = sub / "INDEX.md"
        data = parse_front_matter(index_path) if index_path.is_file() else None

        if data is None:
            # Transparent directory: children flatten into the current index.
            sub_lines, sub_deferred = walk(sub, f"{rel}/{sub.name}".strip("/"), link_prefix)
            lines.extend(sub_lines)
            deferred.update(sub_deferred)
            continue

        lines.append(_entry(data, _link(link_prefix, rel, f"{sub.name}/INDEX.md")))

        if data.get("type") == "index":
            child_lines, child_deferred = walk(sub, "", "")
            deferred[index_path] = child_lines
            deferred.update(child_deferred)
        else:
            # Non-index INDEX.md: siblings flatten into the current index, and the walk
            # does not descend (known limitation, guarded in validate_front_matter).
            for sibling in _md_files(sub):
                lines.append(_entry(parse_front_matter(sibling), _link(link_prefix, rel, f"{sub.name}/{sibling.name}")))

    return lines, deferred


def render(path: Path, lines: list[str]) -> str:
    """Return `path`'s text with the generated block replaced. Raises if markers are absent."""
    text = path.read_text(encoding="utf-8")
    begin = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if begin == -1 or end == -1:
        raise SkillError(f"{path}: missing BEGIN/END GENERATED INDEX markers")
    if end < begin:
        raise SkillError(f"{path}: END marker precedes BEGIN marker")
    body = "\n".join(lines)
    return text[: begin + len(BEGIN_MARKER)] + "\n" + (body + "\n" if body else "") + text[end:]


def build(root: Path) -> dict[Path, str]:
    """Validate front matter, then return {file path: new content} for every index."""
    references = root / "references"
    if not references.is_dir():
        raise SkillError(f"{root}: missing required `references/` directory")

    for md in sorted(references.rglob("*.md")):
        validate_front_matter(md, parse_front_matter(md))

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        raise SkillError(f"{root}: missing required SKILL.md")

    skill_lines, deferred = walk(references, "", "references/")
    rendered = {skill_md: render(skill_md, skill_lines)}
    for hub_path, hub_lines in deferred.items():
        rendered[hub_path] = render(hub_path, hub_lines)
    return rendered


# --------------------------------------------------------------------------- invariants


def check_links(root: Path) -> list[str]:
    """Invariant 2 — every relative markdown link resolves."""
    failures = []
    for md in sorted(root.rglob("*.md")):
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (md.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                failures.append(f"{md}: broken link -> {target}")
    return failures


def check_reachability(root: Path) -> list[str]:
    """Invariant 3 — BFS from SKILL.md reaches every file in the skill root."""
    start = (root / "SKILL.md").resolve()
    seen = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current.suffix != ".md" or not current.is_file():
            continue
        for target in LINK_RE.findall(current.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (current.parent / target.split("#", 1)[0]).resolve()
            if resolved.exists() and resolved not in seen:
                seen.add(resolved)
                queue.append(resolved)

    orphans = [p for p in sorted(root.rglob("*")) if p.is_file() and p.resolve() not in seen]
    return [f"{p}: unreachable from SKILL.md (orphan)" for p in orphans]


def check_budget(root: Path) -> list[str]:
    """Invariant 7 — SKILL.md <= 120 lines / 8 KB."""
    skill_md = root / "SKILL.md"
    raw = skill_md.read_bytes()
    failures = []
    line_count = raw.decode("utf-8").count("\n") + 1
    if line_count > SKILL_MD_MAX_LINES:
        failures.append(f"{skill_md}: {line_count} lines exceeds the {SKILL_MD_MAX_LINES}-line budget")
    if len(raw) > SKILL_MD_MAX_BYTES:
        failures.append(f"{skill_md}: {len(raw)} bytes exceeds the {SKILL_MD_MAX_BYTES}-byte budget")
    return failures


# --------------------------------------------------------------------------- commands


def cmd_generate(root: Path, check: bool, validate_only: bool) -> int:
    rendered = build(root)
    if validate_only:
        print(f"front matter OK ({len(list((root / 'references').rglob('*.md')))} files)")
        return 0

    drifted = [p for p, content in rendered.items() if p.read_text(encoding="utf-8") != content]
    if check:
        if drifted:
            for path in drifted:
                print(f"index drift: {path}", file=sys.stderr)
            print(f"\nrun: skillgen.py generate {root}", file=sys.stderr)
            return 1
        print("indexes up to date")
        return 0

    for path, content in rendered.items():
        path.write_text(content, encoding="utf-8")
    print(f"generated {len(rendered)} index block(s); {len(drifted)} changed")
    return 0


def cmd_validate(root: Path) -> int:
    failures: list[str] = []

    try:
        rendered = build(root)
    except SkillError as exc:
        print(f"FAIL invariant 1 (front matter): {exc}", file=sys.stderr)
        return 1
    print("PASS invariant 1 — front matter valid")

    link_failures = check_links(root)
    print(f"{'PASS' if not link_failures else 'FAIL'} invariant 2 — links resolve")
    failures += link_failures

    orphans = check_reachability(root)
    total = sum(1 for p in root.rglob("*") if p.is_file())
    print(f"{'PASS' if not orphans else 'FAIL'} invariant 3 — reachability {total - len(orphans)}/{total}")
    failures += orphans

    drifted = [f"{p}: index drift" for p, c in rendered.items() if p.read_text(encoding="utf-8") != c]
    print(f"{'PASS' if not drifted else 'FAIL'} invariant 4 — no index drift")
    failures += drifted

    budget = check_budget(root)
    print(f"{'PASS' if not budget else 'FAIL'} invariant 7 — SKILL.md budget")
    failures += budget

    print("SKIP invariants 5 & 6 — code-block and markdown checks need the host toolchain")

    if failures:
        print("", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="skillgen", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="regenerate the generated index blocks")
    gen.add_argument("root", type=Path)
    mode = gen.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="diff only; exit non-zero on drift")
    mode.add_argument("--validate-only", action="store_true", help="front-matter validation only")

    val = sub.add_parser("validate", help="run the mechanically checkable conformance invariants")
    val.add_argument("root", type=Path)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        print(f"no such skill root: {root}", file=sys.stderr)
        return 2

    try:
        if args.command == "generate":
            return cmd_generate(root, args.check, args.validate_only)
        return cmd_validate(root)
    except SkillError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
