"""Validate all skill SKILL.md files for structure, content, and links."""

import re
from pathlib import Path

import pytest

from conftest import SKILLS_DIR, parse_frontmatter, get_markdown_sections


def _skill_files():
    """Discover all SKILL.md files for parametrization."""
    return sorted(
        d / "SKILL.md"
        for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


SKILL_FILES = _skill_files()
REQUIRED_SECTIONS = ["Trigger", "Required Inputs", "Workflow", "Example Interaction"]
RECOMMENDED_SECTIONS = ["MCP Usage", "Key References", "See Also"]


@pytest.fixture(params=SKILL_FILES, ids=[f.parent.name for f in SKILL_FILES])
def skill_path(request):
    return request.param


@pytest.fixture
def skill_content(skill_path):
    return skill_path.read_text(encoding="utf-8")


@pytest.fixture
def skill_fm(skill_content):
    fm, _ = parse_frontmatter(skill_content)
    return fm


@pytest.fixture
def skill_body(skill_content):
    _, body = parse_frontmatter(skill_content)
    return body


@pytest.fixture
def skill_sections(skill_body):
    return get_markdown_sections(skill_body)


# ── Frontmatter ─────────────────────────────────────────────────────


class TestSkillFrontmatter:
    def test_has_frontmatter(self, skill_content):
        assert skill_content.startswith("---"), "SKILL.md must start with YAML frontmatter ---"

    def test_name_present(self, skill_fm):
        assert "name" in skill_fm, "frontmatter missing 'name'"

    def test_name_matches_directory(self, skill_path, skill_fm):
        assert skill_fm["name"] == skill_path.parent.name, (
            f"frontmatter name '{skill_fm['name']}' != directory '{skill_path.parent.name}'"
        )

    def test_name_no_trailing_whitespace(self, skill_fm):
        name = skill_fm.get("name", "")
        assert name == name.strip(), "frontmatter name has trailing whitespace"

    def test_description_present(self, skill_fm):
        assert "description" in skill_fm, "frontmatter missing 'description'"

    def test_description_min_length(self, skill_fm):
        desc = skill_fm.get("description", "")
        assert len(desc) >= 20, f"description too short ({len(desc)} chars, need >= 20)"

    def test_description_no_trailing_whitespace(self, skill_fm):
        desc = skill_fm.get("description", "")
        assert desc == desc.strip(), "frontmatter description has trailing whitespace"


# ── Required Sections ───────────────────────────────────────────────


class TestSkillRequiredSections:
    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_required_section_exists(self, skill_sections, section, skill_path):
        assert section in skill_sections, (
            f"{skill_path.parent.name}: missing required section '## {section}'"
        )

    def test_has_h1_heading(self, skill_body):
        assert re.search(r"^# .+", skill_body, re.MULTILINE), "missing H1 heading"


# ── Recommended Sections (warnings, not failures) ──────────────────


class TestSkillRecommendedSections:
    @pytest.mark.parametrize("section", RECOMMENDED_SECTIONS)
    def test_recommended_section_exists(self, skill_sections, section, skill_path):
        if section not in skill_sections:
            pytest.skip(f"{skill_path.parent.name}: optional section '## {section}' not present")


# ── Content Quality ─────────────────────────────────────────────────


class TestSkillContentQuality:
    def test_minimum_length(self, skill_content, skill_path):
        lines = skill_content.splitlines()
        assert len(lines) >= 50, (
            f"{skill_path.parent.name}: only {len(lines)} lines (need >= 50)"
        )

    def test_no_empty_required_sections(self, skill_sections, skill_path):
        for section in REQUIRED_SECTIONS:
            if section in skill_sections:
                assert len(skill_sections[section].strip()) > 0, (
                    f"{skill_path.parent.name}: section '## {section}' is empty"
                )


# ── Internal Links ──────────────────────────────────────────────────


class TestSkillInternalLinks:
    def test_relative_links_resolve(self, skill_content, skill_path):
        link_pattern = re.compile(r"\[([^\]]+)\]\((\.[^)]+)\)")
        for match in link_pattern.finditer(skill_content):
            link_text, rel_path = match.groups()
            target = (skill_path.parent / rel_path).resolve()
            assert target.exists(), (
                f"broken link [{link_text}]({rel_path}) -> {target}"
            )
