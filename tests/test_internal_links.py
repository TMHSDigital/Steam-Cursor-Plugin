"""Verify all relative markdown links in .md and .mdc files resolve to existing files."""

import re
from pathlib import Path

import pytest

from conftest import REPO_ROOT


LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTTP_PATTERN = re.compile(r"^https?://")
ANCHOR_PATTERN = re.compile(r"^#")


def _collect_md_files():
    """Find all .md and .mdc files in the repo."""
    files = list(REPO_ROOT.rglob("*.md"))
    files += list(REPO_ROOT.rglob("*.mdc"))
    files = [f for f in files if ".git" not in f.parts and "node_modules" not in f.parts]
    return sorted(files)


MD_FILES = _collect_md_files()


def _extract_relative_links(filepath: Path) -> list[tuple[str, str, Path]]:
    """Extract (link_text, raw_path, resolved_target) for relative links."""
    text = filepath.read_text(encoding="utf-8")
    results = []
    for match in LINK_PATTERN.finditer(text):
        link_text, raw_path = match.groups()
        if HTTP_PATTERN.match(raw_path):
            continue
        if ANCHOR_PATTERN.match(raw_path):
            continue
        if raw_path.startswith("mailto:"):
            continue
        clean = raw_path.split("#")[0].split("?")[0]
        if not clean:
            continue
        target = (filepath.parent / clean).resolve()
        results.append((link_text, raw_path, target))
    return results


def _build_test_cases():
    """Build (file, link_text, raw_path, target) tuples for parametrization."""
    cases = []
    for md_file in MD_FILES:
        for link_text, raw_path, target in _extract_relative_links(md_file):
            rel = md_file.relative_to(REPO_ROOT)
            cases.append(pytest.param(
                md_file, link_text, raw_path, target,
                id=f"{rel}::[{link_text}]({raw_path})"
            ))
    return cases


LINK_CASES = _build_test_cases()


@pytest.mark.skipif(not LINK_CASES, reason="No relative links found")
@pytest.mark.parametrize("md_file,link_text,raw_path,target", LINK_CASES)
def test_relative_link_resolves(md_file, link_text, raw_path, target):
    assert target.exists(), (
        f"Broken link in {md_file.relative_to(REPO_ROOT)}: "
        f"[{link_text}]({raw_path}) -> {target}"
    )
