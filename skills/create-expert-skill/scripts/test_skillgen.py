#!/usr/bin/env python3
"""Unit tests for skillgen.py. Standard library only — run with:

    python3 skills/create-expert-skill/scripts/test_skillgen.py

or `python3 -m unittest test_skillgen` from this directory.
"""

from __future__ import annotations

import io
import contextlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillgen  # noqa: E402


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _leaf(title: str, trigger: str) -> str:
    return f"---\ntitle: {title}\ntriggers:\n  - \"{trigger}\"\n---\n\n# {title}\n"


def _skill_md(body: str = "") -> str:
    return (
        "# Example Skill\n\n"
        f"{body}"
        f"{skillgen.BEGIN_MARKER}\n{skillgen.END_MARKER}\n"
    )


def build_conforming_root(root: Path) -> None:
    """A minimal but structurally complete skill root, exercising every walk() branch:
    a root leaf, a transparent subdirectory (patterns/, flattens into its parent hub),
    a hub (guide/, type: index), and a non-index INDEX.md (aside/, siblings flatten
    into the root index).
    """
    _write(root / "SKILL.md", _skill_md())

    _write(root / "references/intro.md", _leaf("Intro", "getting started"))

    _write(
        root / "references/guide/INDEX.md",
        "---\ntitle: Guide\ntriggers:\n  - \"guide topics\"\ntype: index\n---\n\n"
        f"# Guide\n\n{skillgen.BEGIN_MARKER}\n{skillgen.END_MARKER}\n",
    )
    _write(root / "references/guide/basics.md", _leaf("Basics", "basics"))
    _write(root / "references/guide/advanced.md", _leaf("Advanced", "advanced use"))
    _write(root / "references/guide/patterns/deep.md", _leaf("Deep pattern", "deep pattern"))

    _write(root / "references/aside/INDEX.md", _leaf("Aside", "aside topics"))
    _write(root / "references/aside/one.md", _leaf("One", "one"))
    _write(root / "references/aside/two.md", _leaf("Two", "two"))


class SkillgenTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)


# --------------------------------------------------------------------------- front matter


class ParseFrontMatterTests(SkillgenTestCase):
    def test_no_front_matter_returns_none(self) -> None:
        path = self.root / "f.md"
        _write(path, "# just a heading\n")
        self.assertIsNone(skillgen.parse_front_matter(path))

    def test_scalar_and_list_values(self) -> None:
        path = self.root / "f.md"
        _write(path, _leaf("Foo", "trig one"))
        data = skillgen.parse_front_matter(path)
        self.assertEqual(data["title"], "Foo")
        self.assertEqual(data["triggers"], ["trig one"])

    def test_quotes_are_stripped(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\ntitle: 'Quoted'\ntriggers:\n  - \"a trigger\"\n---\n")
        data = skillgen.parse_front_matter(path)
        self.assertEqual(data["title"], "Quoted")
        self.assertEqual(data["triggers"], ["a trigger"])

    def test_unterminated_front_matter_raises(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\ntitle: Foo\n")
        with self.assertRaisesRegex(skillgen.SkillError, "never closed"):
            skillgen.parse_front_matter(path)

    def test_list_item_before_any_key_raises(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\n  - orphan item\n---\n")
        with self.assertRaisesRegex(skillgen.SkillError, "list item before any key"):
            skillgen.parse_front_matter(path)

    def test_scalar_key_followed_by_list_item_raises(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\nfoo: bar\n  - baz\n---\n")
        with self.assertRaisesRegex(skillgen.SkillError, "both a value and list items"):
            skillgen.parse_front_matter(path)

    def test_non_key_value_line_raises(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\nnot a key value line\n---\n")
        with self.assertRaisesRegex(skillgen.SkillError, "not a `key: value` line"):
            skillgen.parse_front_matter(path)

    def test_malformed_list_item_raises(self) -> None:
        path = self.root / "f.md"
        _write(path, "---\ntriggers:\n  * not a dash item\n---\n")
        with self.assertRaisesRegex(skillgen.SkillError, "expected a `- ` list item"):
            skillgen.parse_front_matter(path)


class ValidateFrontMatterTests(SkillgenTestCase):
    def test_missing_data_raises(self) -> None:
        with self.assertRaisesRegex(skillgen.SkillError, "missing YAML front matter"):
            skillgen.validate_front_matter(self.root / "f.md", None)

    def test_unknown_key_raises(self) -> None:
        data = {"title": "T", "triggers": ["t"], "bogus": "x"}
        with self.assertRaisesRegex(skillgen.SkillError, "unknown front-matter keys"):
            skillgen.validate_front_matter(self.root / "f.md", data)

    def test_missing_title_raises(self) -> None:
        data = {"triggers": ["t"]}
        with self.assertRaisesRegex(skillgen.SkillError, "`title` is required"):
            skillgen.validate_front_matter(self.root / "f.md", data)

    def test_empty_triggers_raises(self) -> None:
        data = {"title": "T", "triggers": []}
        with self.assertRaisesRegex(skillgen.SkillError, "`triggers` is required"):
            skillgen.validate_front_matter(self.root / "f.md", data)

    def test_blank_trigger_entry_raises(self) -> None:
        data = {"title": "T", "triggers": ["ok", "   "]}
        with self.assertRaisesRegex(skillgen.SkillError, "every `triggers` entry"):
            skillgen.validate_front_matter(self.root / "f.md", data)

    def test_type_index_on_non_index_filename_raises(self) -> None:
        data = {"title": "T", "triggers": ["t"], "type": "index"}
        with self.assertRaisesRegex(skillgen.SkillError, "legal on INDEX.md only"):
            skillgen.validate_front_matter(self.root / "leaf.md", data)

    def test_type_with_non_index_value_raises(self) -> None:
        data = {"title": "T", "triggers": ["t"], "type": "hub"}
        with self.assertRaisesRegex(skillgen.SkillError, "literal `index`"):
            skillgen.validate_front_matter(self.root / "INDEX.md", data)

    def test_index_with_subdirs_and_no_type_raises(self) -> None:
        directory = self.root / "sect"
        (directory / "child").mkdir(parents=True)
        path = directory / "INDEX.md"
        data = {"title": "T", "triggers": ["t"]}
        with self.assertRaisesRegex(skillgen.SkillError, "type: index.*is required"):
            skillgen.validate_front_matter(path, data)

    def test_index_without_subdirs_and_no_type_is_fine(self) -> None:
        directory = self.root / "sect"
        directory.mkdir(parents=True)
        (directory / "sibling.md").write_text("x", encoding="utf-8")
        path = directory / "INDEX.md"
        data = {"title": "T", "triggers": ["t"]}
        skillgen.validate_front_matter(path, data)  # must not raise


# --------------------------------------------------------------------------- walk / build


class BuildTests(SkillgenTestCase):
    def test_missing_references_dir_raises(self) -> None:
        _write(self.root / "SKILL.md", _skill_md())
        with self.assertRaisesRegex(skillgen.SkillError, "missing required `references/`"):
            skillgen.build(self.root)

    def test_missing_skill_md_raises(self) -> None:
        (self.root / "references").mkdir()
        with self.assertRaisesRegex(skillgen.SkillError, "missing required SKILL.md"):
            skillgen.build(self.root)

    def test_hub_missing_markers_raises(self) -> None:
        build_conforming_root(self.root)
        hub = self.root / "references/guide/INDEX.md"
        _write(hub, "---\ntitle: Guide\ntriggers:\n  - \"guide topics\"\ntype: index\n---\n\n# Guide\n")
        with self.assertRaisesRegex(skillgen.SkillError, "missing BEGIN/END"):
            skillgen.build(self.root)

    def test_root_and_hub_entries_generated(self) -> None:
        build_conforming_root(self.root)
        rendered = skillgen.build(self.root)

        skill_md = self.root / "SKILL.md"
        guide_index = self.root / "references/guide/INDEX.md"
        self.assertIn(skill_md, rendered)
        self.assertIn(guide_index, rendered)

        root_body = rendered[skill_md]
        self.assertIn("[Intro](./references/intro.md)", root_body)
        self.assertIn("[Aside](./references/aside/INDEX.md)", root_body)
        self.assertIn("[One](./references/aside/one.md)", root_body)
        self.assertIn("[Guide](./references/guide/INDEX.md)", root_body)

        hub_body = rendered[guide_index]
        self.assertIn("[Basics](./basics.md)", hub_body)
        self.assertIn("[Advanced](./advanced.md)", hub_body)
        self.assertIn("[Deep pattern](./patterns/deep.md)", hub_body)

    def test_non_index_hub_is_not_deferred(self) -> None:
        build_conforming_root(self.root)
        rendered = skillgen.build(self.root)
        aside_index = self.root / "references/aside/INDEX.md"
        self.assertNotIn(aside_index, rendered)


# --------------------------------------------------------------------------- render


class RenderTests(SkillgenTestCase):
    def test_missing_markers_raises(self) -> None:
        path = self.root / "SKILL.md"
        _write(path, "# no markers here\n")
        with self.assertRaisesRegex(skillgen.SkillError, "missing BEGIN/END"):
            skillgen.render(path, ["- a line"])

    def test_end_before_begin_raises(self) -> None:
        path = self.root / "SKILL.md"
        _write(path, f"{skillgen.END_MARKER}\n{skillgen.BEGIN_MARKER}\n")
        with self.assertRaisesRegex(skillgen.SkillError, "END marker precedes BEGIN"):
            skillgen.render(path, ["- a line"])

    def test_replaces_body_between_markers(self) -> None:
        path = self.root / "SKILL.md"
        _write(path, f"before\n{skillgen.BEGIN_MARKER}\nstale\n{skillgen.END_MARKER}\nafter\n")
        result = skillgen.render(path, ["- fresh"])
        self.assertIn("- fresh", result)
        self.assertNotIn("stale", result)
        self.assertIn("before\n", result)
        self.assertIn("after\n", result)


# --------------------------------------------------------------------------- invariant checks


class CheckLinksTests(SkillgenTestCase):
    def test_valid_relative_link_passes(self) -> None:
        _write(self.root / "a.md", "see [b](./b.md)\n")
        _write(self.root / "b.md", "target\n")
        self.assertEqual(skillgen.check_links(self.root), [])

    def test_broken_relative_link_flagged(self) -> None:
        _write(self.root / "a.md", "see [missing](./nope.md)\n")
        failures = skillgen.check_links(self.root)
        self.assertEqual(len(failures), 1)
        self.assertIn("nope.md", failures[0])

    def test_http_mailto_and_anchor_links_ignored(self) -> None:
        _write(
            self.root / "a.md",
            "[web](https://example.com) [mail](mailto:x@example.com) [anchor](#section)\n",
        )
        self.assertEqual(skillgen.check_links(self.root), [])


class CheckReachabilityTests(SkillgenTestCase):
    def test_fully_linked_tree_has_no_orphans(self) -> None:
        build_conforming_root(self.root)
        for path, content in skillgen.build(self.root).items():
            path.write_text(content, encoding="utf-8")
        self.assertEqual(skillgen.check_reachability(self.root), [])

    def test_unlinked_file_is_an_orphan(self) -> None:
        build_conforming_root(self.root)
        for path, content in skillgen.build(self.root).items():
            path.write_text(content, encoding="utf-8")
        stray = self.root / "references/guide/diagram.png"
        _write(stray, "not a real image, just a stray file")

        orphans = skillgen.check_reachability(self.root)
        self.assertEqual(len(orphans), 1)
        self.assertIn("diagram.png", orphans[0])


class CheckBudgetTests(SkillgenTestCase):
    def test_within_budget_passes(self) -> None:
        _write(self.root / "SKILL.md", _skill_md())
        self.assertEqual(skillgen.check_budget(self.root), [])

    def test_over_line_budget_flagged(self) -> None:
        _write(self.root / "SKILL.md", _skill_md("x\n" * 200))
        failures = skillgen.check_budget(self.root)
        self.assertTrue(any("lines exceeds" in f for f in failures))

    def test_over_byte_budget_flagged(self) -> None:
        _write(self.root / "SKILL.md", _skill_md("x" * (9 * 1024) + "\n"))
        failures = skillgen.check_budget(self.root)
        self.assertTrue(any("bytes exceeds" in f for f in failures))


# --------------------------------------------------------------------------- CLI commands


class CommandTests(SkillgenTestCase):
    def _run(self, func, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = func(*args)
        return code, out.getvalue(), err.getvalue()

    def test_generate_validate_only(self) -> None:
        build_conforming_root(self.root)
        code, out, _ = self._run(skillgen.cmd_generate, self.root, False, True)
        self.assertEqual(code, 0)
        self.assertIn("front matter OK", out)
        # validate-only must not write anything.
        self.assertNotIn(skillgen.BEGIN_MARKER + "\n- ", (self.root / "SKILL.md").read_text())

    def test_generate_check_detects_drift_then_clears(self) -> None:
        build_conforming_root(self.root)
        code, _, err = self._run(skillgen.cmd_generate, self.root, True, False)
        self.assertEqual(code, 1)
        self.assertIn("index drift", err)

        code, out, _ = self._run(skillgen.cmd_generate, self.root, False, False)
        self.assertEqual(code, 0)
        self.assertIn("generated", out)

        code, out, _ = self._run(skillgen.cmd_generate, self.root, True, False)
        self.assertEqual(code, 0)
        self.assertIn("up to date", out)

    def test_validate_passes_on_conforming_root(self) -> None:
        build_conforming_root(self.root)
        self._run(skillgen.cmd_generate, self.root, False, False)
        code, out, _ = self._run(skillgen.cmd_validate, self.root)
        self.assertEqual(code, 0)
        self.assertIn("PASS invariant 1", out)
        self.assertIn("PASS invariant 2", out)
        self.assertIn("PASS invariant 3", out)
        self.assertIn("PASS invariant 4", out)
        self.assertIn("PASS invariant 7", out)

    def test_validate_fails_on_orphan(self) -> None:
        build_conforming_root(self.root)
        self._run(skillgen.cmd_generate, self.root, False, False)
        _write(self.root / "references/guide/diagram.png", "stray")
        code, out, err = self._run(skillgen.cmd_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL invariant 3", out)
        self.assertIn("diagram.png", err)

    def test_validate_fails_on_bad_front_matter(self) -> None:
        build_conforming_root(self.root)
        _write(self.root / "references/intro.md", "---\ntriggers:\n  - \"x\"\n---\n")
        code, _, err = self._run(skillgen.cmd_validate, self.root)
        self.assertEqual(code, 1)
        self.assertIn("FAIL invariant 1", err)


class MainTests(SkillgenTestCase):
    def _run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = skillgen.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_no_such_root(self) -> None:
        code, _, err = self._run_main(["validate", str(self.root / "nope")])
        self.assertEqual(code, 2)
        self.assertIn("no such skill root", err)

    def test_generate_and_validate_round_trip(self) -> None:
        build_conforming_root(self.root)
        code, _, _ = self._run_main(["generate", str(self.root)])
        self.assertEqual(code, 0)
        code, out, _ = self._run_main(["validate", str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("PASS invariant 4", out)


if __name__ == "__main__":
    unittest.main()
