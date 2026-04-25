"""Validate ROADMAP.md integrity: current version, table consistency, completed section."""

import re

from conftest import REPO_ROOT


# ── Current Version ─────────────────────────────────────────────────


class TestRoadmapCurrentVersion:
    def test_exactly_one_current_in_table(self, roadmap_text):
        current_matches = re.findall(r"\(current\)", roadmap_text, re.IGNORECASE)
        assert len(current_matches) == 1, (
            f"Expected exactly 1 '(current)' in roadmap table, found {len(current_matches)}"
        )

    def test_current_line_version(self, plugin_manifest, roadmap_text):
        version = plugin_manifest["version"]
        m = re.search(r"\*\*Current:\*\*\s+v([\d.]+)", roadmap_text)
        assert m, "ROADMAP.md missing '**Current:** vX.Y.Z' line"
        assert m.group(1) == version, (
            f"Current line says v{m.group(1)}, plugin.json says {version}"
        )


# ── Table Row Counts ────────────────────────────────────────────────


class TestRoadmapTableCounts:
    def test_current_row_skill_count(self, plugin_manifest, roadmap_text, skill_count):
        version = plugin_manifest["version"]
        pattern = rf"v{re.escape(version)}\s*\(current\)\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*(\d+)\s*\|"
        m = re.search(pattern, roadmap_text)
        if m:
            assert int(m.group(1)) == skill_count, (
                f"Roadmap table says {m.group(1)} total skills for current version, "
                f"but found {skill_count} on disk"
            )

    def test_current_row_rule_count(self, plugin_manifest, roadmap_text, rule_count):
        version = plugin_manifest["version"]
        pattern = rf"v{re.escape(version)}\s*\(current\)\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\d+\s*\|\s*(\d+)\s*\|"
        m = re.search(pattern, roadmap_text)
        if m:
            assert int(m.group(1)) == rule_count, (
                f"Roadmap table says {m.group(1)} total rules for current version, "
                f"but found {rule_count} on disk"
            )


# ── Completed Section ───────────────────────────────────────────────


class TestRoadmapCompleted:
    def test_completed_items_checked(self, roadmap_text):
        completed_section = roadmap_text.split("## Completed")
        if len(completed_section) < 2:
            return
        completed = completed_section[1]
        unchecked = re.findall(r"^- \[ \]", completed, re.MULTILINE)
        assert len(unchecked) == 0, (
            f"Completed section has {len(unchecked)} unchecked items"
        )

    def test_no_duplicate_completed_entries(self, roadmap_text):
        completed_section = roadmap_text.split("## Completed")
        if len(completed_section) < 2:
            return
        completed = completed_section[1]
        entries = re.findall(r"`([^`]+)`\s+added in", completed)
        seen = set()
        dupes = []
        for entry in entries:
            if entry in seen:
                dupes.append(entry)
            seen.add(entry)
        assert len(dupes) == 0, f"Duplicate completed entries: {dupes}"
