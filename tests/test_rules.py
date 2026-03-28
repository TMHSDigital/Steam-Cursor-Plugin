"""Validate all .mdc rule files for structure and content."""

import re

import pytest

from conftest import RULES_DIR, parse_frontmatter


def _rule_files():
    return sorted(RULES_DIR.glob("*.mdc"))


RULE_FILES = _rule_files()


@pytest.fixture(params=RULE_FILES, ids=[f.stem for f in RULE_FILES])
def rule_path(request):
    return request.param


@pytest.fixture
def rule_content(rule_path):
    return rule_path.read_text(encoding="utf-8")


@pytest.fixture
def rule_fm(rule_content):
    fm, _ = parse_frontmatter(rule_content)
    return fm


@pytest.fixture
def rule_body(rule_content):
    _, body = parse_frontmatter(rule_content)
    return body


# ── Frontmatter ─────────────────────────────────────────────────────


class TestRuleFrontmatter:
    def test_has_frontmatter(self, rule_content):
        assert rule_content.startswith("---"), ".mdc must start with YAML frontmatter ---"

    def test_description_present(self, rule_fm):
        assert "description" in rule_fm, "frontmatter missing 'description'"

    def test_description_nonempty(self, rule_fm):
        assert len(rule_fm.get("description", "")) > 0, "description is empty"

    def test_always_apply_present(self, rule_fm):
        assert "alwaysApply" in rule_fm, "frontmatter missing 'alwaysApply'"

    def test_always_apply_is_bool(self, rule_fm):
        assert isinstance(rule_fm.get("alwaysApply"), bool), (
            f"alwaysApply should be boolean, got {type(rule_fm.get('alwaysApply'))}"
        )


# ── Globs ───────────────────────────────────────────────────────────


class TestRuleGlobs:
    def test_non_global_has_globs(self, rule_fm, rule_path):
        if rule_fm.get("alwaysApply") is False:
            globs = rule_fm.get("globs", [])
            assert isinstance(globs, list) and len(globs) > 0, (
                f"{rule_path.stem}: alwaysApply=false but no globs defined"
            )

    def test_glob_patterns_have_path_context(self, rule_fm, rule_path):
        for pattern in rule_fm.get("globs", []):
            assert isinstance(pattern, str), f"glob pattern is not a string: {pattern}"
            assert len(pattern) > 1, f"glob pattern too short: '{pattern}'"


# ── Body ────────────────────────────────────────────────────────────


class TestRuleBody:
    def test_body_not_empty(self, rule_body, rule_path):
        lines = [l for l in rule_body.splitlines() if l.strip()]
        assert len(lines) >= 5, (
            f"{rule_path.stem}: body has only {len(lines)} non-empty lines (need >= 5)"
        )

    def test_has_h1_heading(self, rule_body, rule_path):
        assert re.search(r"^# .+", rule_body, re.MULTILINE), (
            f"{rule_path.stem}: missing H1 heading"
        )
