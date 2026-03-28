"""Shared fixtures for Steam Cursor Plugin test suite."""

import json
import re
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent

SKILLS_DIR = REPO_ROOT / "skills"
RULES_DIR = REPO_ROOT / "rules"
PLUGIN_JSON = REPO_ROOT / ".cursor-plugin" / "plugin.json"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (frontmatter_dict, body_str)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return fm, body


def get_markdown_sections(body: str) -> dict[str, str]:
    """Extract H1/H2 sections from markdown body. Returns {heading: content}."""
    sections: dict[str, str] = {}
    current_heading = None
    current_lines: list[str] = []

    for line in body.splitlines():
        m = re.match(r"^(#{1,2})\s+(.+)$", line)
        if m:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = m.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return sections


# ── Fixtures ────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def plugin_manifest():
    return json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def skill_dirs():
    """Return list of skill directory paths that contain SKILL.md."""
    return sorted(
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


@pytest.fixture(scope="session")
def rule_files():
    """Return list of .mdc rule file paths."""
    return sorted(RULES_DIR.glob("*.mdc"))


@pytest.fixture(scope="session")
def skill_count(skill_dirs):
    return len(skill_dirs)


@pytest.fixture(scope="session")
def rule_count(rule_files):
    return len(rule_files)


@pytest.fixture(scope="session")
def readme_text():
    return (REPO_ROOT / "README.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def claude_text():
    return (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def contributing_text():
    return (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def changelog_text():
    return (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def roadmap_text():
    return (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
