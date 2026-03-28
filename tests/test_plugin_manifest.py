"""Validate .cursor-plugin/plugin.json structure and consistency."""

import re

from conftest import REPO_ROOT


def test_required_keys(plugin_manifest):
    required = ["name", "displayName", "version", "description", "skills", "rules", "logo"]
    for key in required:
        assert key in plugin_manifest, f"plugin.json missing required key: {key}"


def test_version_is_semver(plugin_manifest):
    assert re.fullmatch(r"\d+\.\d+\.\d+", plugin_manifest["version"]), (
        f"version '{plugin_manifest['version']}' is not valid semver"
    )


def test_skills_directory_exists(plugin_manifest):
    skills_path = REPO_ROOT / plugin_manifest["skills"].lstrip("./")
    assert skills_path.is_dir(), f"skills path '{skills_path}' does not exist"


def test_rules_directory_exists(plugin_manifest):
    rules_path = REPO_ROOT / plugin_manifest["rules"].lstrip("./")
    assert rules_path.is_dir(), f"rules path '{rules_path}' does not exist"


def test_logo_exists(plugin_manifest):
    logo_path = REPO_ROOT / plugin_manifest["logo"]
    assert logo_path.is_file(), f"logo '{logo_path}' does not exist"


def test_skill_count_in_description(plugin_manifest, skill_count):
    m = re.search(r"(\d+)\s+skills", plugin_manifest["description"])
    assert m, "plugin.json description does not mention skill count"
    assert int(m.group(1)) == skill_count, (
        f"description says {m.group(1)} skills, but found {skill_count} on disk"
    )


def test_rule_count_in_description(plugin_manifest, rule_count):
    m = re.search(r"(\d+)\s+rules", plugin_manifest["description"])
    assert m, "plugin.json description does not mention rule count"
    assert int(m.group(1)) == rule_count, (
        f"description says {m.group(1)} rules, but found {rule_count} on disk"
    )


def test_keywords_nonempty(plugin_manifest):
    kw = plugin_manifest.get("keywords", [])
    assert isinstance(kw, list) and len(kw) > 0, "keywords should be a non-empty list"
    for item in kw:
        assert isinstance(item, str), f"keyword '{item}' is not a string"
