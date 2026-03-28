"""Verify version and count consistency across all documentation files."""

import re

from conftest import REPO_ROOT


# ── Helpers ─────────────────────────────────────────────────────────


def _extract_numbers(pattern, text):
    """Extract all integer matches for a regex with one capture group."""
    return [int(m) for m in re.findall(pattern, text)]


# ── Version Consistency ─────────────────────────────────────────────


class TestVersionConsistency:
    def test_readme_badge_version(self, plugin_manifest, readme_text):
        version = plugin_manifest["version"]
        assert f"version-{version}-green" in readme_text, (
            f"README badge does not show version {version}"
        )

    def test_roadmap_current_version(self, plugin_manifest, roadmap_text):
        version = plugin_manifest["version"]
        assert f"v{version}" in roadmap_text and "Current" in roadmap_text, (
            f"ROADMAP.md does not list v{version} as current"
        )

    def test_claude_md_version(self, plugin_manifest, claude_text):
        version = plugin_manifest["version"]
        assert f"v{version}" in claude_text or version in claude_text, (
            f"CLAUDE.md does not mention version {version}"
        )

    def test_changelog_has_current_version(self, plugin_manifest, changelog_text):
        version = plugin_manifest["version"]
        assert f"[{version}]" in changelog_text, (
            f"CHANGELOG.md has no entry for version {version}"
        )


# ── Skill Count Consistency ─────────────────────────────────────────


class TestSkillCountConsistency:
    def test_readme_skill_count(self, skill_count, readme_text):
        m = re.search(r"(?:\*\*|<strong>)(\d+)\s+skills(?:\*\*|</strong>)", readme_text)
        assert m, "README.md stats line missing skill count"
        assert int(m.group(1)) == skill_count, (
            f"README says {m.group(1)} skills, disk has {skill_count}"
        )

    def test_claude_md_skill_count(self, skill_count, claude_text):
        m = re.search(r"Skills\s*\((\d+)\s+total\)", claude_text)
        assert m, "CLAUDE.md missing skills total in header"
        assert int(m.group(1)) == skill_count, (
            f"CLAUDE.md says {m.group(1)} skills, disk has {skill_count}"
        )

    def test_contributing_skill_count(self, skill_count, contributing_text):
        m = re.search(r"\*\*(\d+)\s+skills\*\*", contributing_text)
        assert m, "CONTRIBUTING.md missing skill count"
        assert int(m.group(1)) == skill_count, (
            f"CONTRIBUTING.md says {m.group(1)} skills, disk has {skill_count}"
        )


# ── Rule Count Consistency ──────────────────────────────────────────


class TestRuleCountConsistency:
    def test_readme_rule_count(self, rule_count, readme_text):
        m = re.search(r"(?:\*\*|<strong>)(\d+)\s+rules(?:\*\*|</strong>)", readme_text)
        assert m, "README.md stats line missing rule count"
        assert int(m.group(1)) == rule_count, (
            f"README says {m.group(1)} rules, disk has {rule_count}"
        )

    def test_claude_md_rule_count(self, rule_count, claude_text):
        m = re.search(r"Rules\s*\((\d+)\s+total\)", claude_text)
        assert m, "CLAUDE.md missing rules total in header"
        assert int(m.group(1)) == rule_count, (
            f"CLAUDE.md says {m.group(1)} rules, disk has {rule_count}"
        )

    def test_contributing_rule_count(self, rule_count, contributing_text):
        m = re.search(r"\*\*(\d+)\s+rules\*\*", contributing_text)
        assert m, "CONTRIBUTING.md missing rule count"
        assert int(m.group(1)) == rule_count, (
            f"CONTRIBUTING.md says {m.group(1)} rules, disk has {rule_count}"
        )


# ── Feature Table Coverage ──────────────────────────────────────────


class TestFeatureTableCoverage:
    def _name_found_in_text(self, kebab_name: str, text_lower: str) -> bool:
        """Check if a kebab-case component name appears in text under any variant."""
        if kebab_name in text_lower:
            return True
        stripped = kebab_name.replace("steam-", "").replace("steamworks-", "")
        words = stripped.split("-")
        spaced = " ".join(words)
        if spaced in text_lower:
            return True
        titled = " ".join(w.capitalize() for w in words)
        if titled.lower() in text_lower:
            return True
        hyphenated = "-".join(words)
        if hyphenated in text_lower:
            return True
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                chunk = " ".join(words[i:j])
                if len(chunk) >= 6 and chunk in text_lower:
                    return True
        return False

    def test_all_skills_in_readme(self, skill_dirs, readme_text):
        readme_lower = readme_text.lower()
        for skill_dir in skill_dirs:
            name = skill_dir.name
            assert self._name_found_in_text(name, readme_lower), (
                f"skill '{name}' not found in README features table"
            )

    def test_all_rules_in_readme(self, rule_files, readme_text):
        readme_lower = readme_text.lower()
        for rule_file in rule_files:
            stem = rule_file.stem
            assert self._name_found_in_text(stem, readme_lower), (
                f"rule '{stem}' not found in README features table"
            )
