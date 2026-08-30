#!/usr/bin/env python3
"""Validate the marketplace, plugin metadata and skill layout."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
PLUGIN_ROOT = ROOT / "plugins/tab"
CODEX_MANIFEST = PLUGIN_ROOT / ".codex-plugin/plugin.json"
CLAUDE_MANIFEST = PLUGIN_ROOT / ".claude-plugin/plugin.json"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
README = ROOT / "README.md"

SHARED_PLUGIN_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)


def load_json(path: Path, problems: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(f"missing file: {path.relative_to(ROOT)}")
        return {}
    except json.JSONDecodeError as error:
        problems.append(f"invalid JSON in {path.relative_to(ROOT)}: {error}")
        return {}

    if not isinstance(value, dict):
        problems.append(f"expected a JSON object in {path.relative_to(ROOT)}")
        return {}
    return value


def one_plugin(marketplace: dict[str, Any], path: Path, problems: list[str]) -> dict[str, Any]:
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        problems.append(f"{path.relative_to(ROOT)} must contain one plugin")
        return {}
    return plugins[0]


def frontmatter(path: Path, problems: list[str]) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        problems.append(f"{path.relative_to(ROOT)} must start with YAML frontmatter")
        return {}

    try:
        end = lines.index("---", 1)
    except ValueError:
        problems.append(f"{path.relative_to(ROOT)} has unterminated frontmatter")
        return {}

    fields: dict[str, str] = {}
    current = ""
    for line in lines[1:end]:
        if line and not line[0].isspace() and ":" in line:
            current, value = line.split(":", 1)
            current = current.strip()
            fields[current] = value.strip()
        elif current and line.strip():
            fields[current] = f"{fields[current]}\n{line.strip()}".strip()
    return fields


def discover_skills(problems: list[str]) -> list[str]:
    if not SKILLS_ROOT.exists():
        return []

    names: list[str] = []
    for entry in sorted(SKILLS_ROOT.iterdir()):
        if not entry.is_dir():
            problems.append(f"unexpected file in {SKILLS_ROOT.relative_to(ROOT)}: {entry.name}")
            continue

        skill_file = entry / "SKILL.md"
        if not skill_file.is_file():
            problems.append(f"missing {skill_file.relative_to(ROOT)}")
            continue

        fields = frontmatter(skill_file, problems)
        name = fields.get("name", "").strip("\"'")
        description = fields.get("description", "")

        if name != entry.name:
            problems.append(
                f"{skill_file.relative_to(ROOT)} name must match its folder: {entry.name}"
            )
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            problems.append(f"invalid skill name in {skill_file.relative_to(ROOT)}: {name or '<empty>'}")
        if description in {"", ">", ">-", "|", "|-"}:
            problems.append(f"missing description in {skill_file.relative_to(ROOT)}")

        names.append(entry.name)
        check_links(entry, problems)

    return names


def check_links(skill_root: Path, problems: list[str]) -> None:
    for markdown in sorted(skill_root.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = raw_target.strip().strip("<>")
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            resolved = (markdown.parent / target).resolve()
            if not resolved.is_relative_to(skill_root.resolve()):
                problems.append(
                    f"link leaves the skill folder in {markdown.relative_to(ROOT)}: {raw_target}"
                )
            elif not resolved.exists():
                problems.append(f"broken link in {markdown.relative_to(ROOT)}: {raw_target}")


def readme_skills(problems: list[str]) -> list[str]:
    try:
        text = README.read_text(encoding="utf-8")
    except FileNotFoundError:
        problems.append("missing file: README.md")
        return []

    section = re.search(r"^## Skills\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not section:
        return []
    return re.findall(r"^\|\s*`([^`]+)`\s*\|", section.group(1), re.MULTILINE)


def validate() -> list[str]:
    problems: list[str] = []
    codex_marketplace = load_json(CODEX_MARKETPLACE, problems)
    claude_marketplace = load_json(CLAUDE_MARKETPLACE, problems)
    codex_manifest = load_json(CODEX_MANIFEST, problems)
    claude_manifest = load_json(CLAUDE_MANIFEST, problems)

    codex_plugin = one_plugin(codex_marketplace, CODEX_MARKETPLACE, problems)
    claude_plugin = one_plugin(claude_marketplace, CLAUDE_MARKETPLACE, problems)

    if codex_marketplace.get("name") != claude_marketplace.get("name"):
        problems.append("Claude Code and Codex marketplace names must match")

    for field in SHARED_PLUGIN_FIELDS:
        if codex_manifest.get(field) != claude_manifest.get(field):
            problems.append(f"plugin manifest field must match: {field}")

    plugin_name = codex_manifest.get("name")
    if plugin_name != PLUGIN_ROOT.name:
        problems.append("plugin manifest name must match the plugin folder")
    if codex_plugin.get("name") != plugin_name or claude_plugin.get("name") != plugin_name:
        problems.append("marketplace plugin names must match the plugin manifest")

    codex_source = codex_plugin.get("source")
    codex_path = codex_source.get("path") if isinstance(codex_source, dict) else None
    claude_path = claude_plugin.get("source")
    if codex_path != claude_path:
        problems.append("Claude Code and Codex marketplace plugin paths must match")
    elif isinstance(codex_path, str):
        source_path = (ROOT / codex_path).resolve()
        if source_path != PLUGIN_ROOT.resolve() or not source_path.is_dir():
            problems.append("marketplace plugin path must point to the plugin folder")
    else:
        problems.append("marketplace plugin path is missing")

    skills = discover_skills(problems)
    documented_skills = readme_skills(problems)
    if documented_skills != sorted(documented_skills):
        problems.append("README skills must be sorted alphabetically")
    if documented_skills != skills:
        problems.append("README skills must match the plugin skills")

    skills_path = codex_manifest.get("skills")
    if skills and skills_path != "./skills/":
        problems.append("Codex plugin manifest must use ./skills/ when skills exist")
    if not skills and skills_path is not None:
        problems.append("Codex plugin manifest must omit skills when the plugin is empty")

    version = codex_manifest.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        problems.append("plugin version must use semantic versioning")

    release_tag = os.environ.get("RELEASE_TAG")
    if release_tag and release_tag != f"v{version}":
        problems.append(f"release tag must be v{version}, got {release_tag}")

    return problems


def main() -> int:
    problems = validate()
    if problems:
        print("Repository validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    skill_count = len(discover_skills([]))
    print(f"Repository validation passed ({skill_count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
