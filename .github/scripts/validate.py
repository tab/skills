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
PLUGINS_ROOT = ROOT / "plugins"
README = ROOT / "README.md"
REVIEW_AGENT_DEFAULTS = (
    PLUGINS_ROOT / "workflow" / "skills" / "feature" / "references" / "review-agents.json"
)
REVIEW_GATES = {"plan", "code", "pr", "follow-up"}

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


def marketplace_plugins(
    marketplace: dict[str, Any], path: Path, problems: list[str]
) -> list[dict[str, Any]]:
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        problems.append(f"{path.relative_to(ROOT)} must contain plugins")
        return []

    valid_plugins: list[dict[str, Any]] = []
    names: set[str] = set()
    for plugin in plugins:
        if not isinstance(plugin, dict):
            problems.append(f"{path.relative_to(ROOT)} contains an invalid plugin entry")
            continue
        name = plugin.get("name")
        if not isinstance(name, str) or not name:
            problems.append(f"{path.relative_to(ROOT)} contains a plugin without a name")
            continue
        if name in names:
            problems.append(f"{path.relative_to(ROOT)} contains duplicate plugin: {name}")
            continue
        names.add(name)
        valid_plugins.append(plugin)

    return valid_plugins


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


def discover_skills(skills_root: Path, problems: list[str]) -> list[str]:
    if not skills_root.exists():
        return []

    names: list[str] = []
    for entry in sorted(skills_root.iterdir()):
        if not entry.is_dir():
            problems.append(f"unexpected file in {skills_root.relative_to(ROOT)}: {entry.name}")
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


def readme_skills(problems: list[str]) -> list[tuple[str, str]]:
    try:
        text = README.read_text(encoding="utf-8")
    except FileNotFoundError:
        problems.append("missing file: README.md")
        return []

    section = re.search(r"^## Skills\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not section:
        return []
    return re.findall(
        r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|",
        section.group(1),
        re.MULTILINE,
    )


def validate_review_agent_defaults(problems: list[str]) -> None:
    config = load_json(REVIEW_AGENT_DEFAULTS, problems)
    if not config:
        return

    allowed_fields = {"version", "default", "reviewers"}
    unknown_fields = set(config) - allowed_fields
    if unknown_fields:
        problems.append(
            "review agent defaults contain unknown fields: " + ", ".join(sorted(unknown_fields))
        )

    if type(config.get("version")) is not int or config["version"] != 1:
        problems.append("review agent defaults must use version 1")

    default = config.get("default")
    if not isinstance(default, dict):
        problems.append("review agent defaults must contain a default object")
        return
    unknown_default_fields = set(default) - {"reviewer", "gates"}
    if unknown_default_fields:
        problems.append(
            "review agent default contains unknown fields: "
            + ", ".join(sorted(unknown_default_fields))
        )
    if set(default) != {"reviewer", "gates"}:
        problems.append("review agent default must contain reviewer and gates")

    reviewers = config.get("reviewers")
    if not isinstance(reviewers, dict):
        problems.append("review agent defaults must contain a reviewers object")
        return

    default_reviewer = default.get("reviewer")
    if not isinstance(default_reviewer, str) or not default_reviewer.strip():
        problems.append("review agent default must use a non-empty reviewer")
    elif default_reviewer in reviewers:
        problems.append("default reviewer must not be repeated in reviewers")

    default_gates = default.get("gates")
    if not isinstance(default_gates, dict) or set(default_gates) != REVIEW_GATES:
        problems.append("review agent default must configure every review gate")
        default_gates = {}

    def validate_settings(settings: Any, label: str) -> dict[str, str]:
        if not isinstance(settings, dict) or not settings:
            problems.append(f"{label} must set model, effort or both")
            return {}
        unknown = set(settings) - {"model", "effort"}
        if unknown:
            problems.append(f"{label} contains unknown fields: " + ", ".join(sorted(unknown)))
        valid: dict[str, str] = {}
        for field in ("model", "effort"):
            if field not in settings:
                continue
            value = settings[field]
            if not isinstance(value, str) or not value.strip():
                problems.append(f"{label} must use a non-empty {field}")
            else:
                valid[field] = value
        return valid

    validated_default_gates = {
        gate: validate_settings(settings, f"default gate {gate}")
        for gate, settings in default_gates.items()
        if gate in REVIEW_GATES
    }
    for gate, settings in validated_default_gates.items():
        if set(settings) != {"model", "effort"}:
            problems.append(f"default gate {gate} must set model and effort")

    for reviewer, reviewer_config in reviewers.items():
        if not isinstance(reviewer, str) or not reviewer:
            problems.append("review agent defaults contain an invalid reviewer name")
            continue
        if not isinstance(reviewer_config, dict) or set(reviewer_config) != {"gates"}:
            problems.append(f"reviewer {reviewer} must contain only gates")
            continue

        gates = reviewer_config.get("gates")
        if not isinstance(gates, dict) or not gates:
            problems.append(f"reviewer {reviewer} gates must be a non-empty object")
            continue
        unknown_gates = set(gates) - REVIEW_GATES
        if unknown_gates:
            problems.append(
                f"reviewer {reviewer} contains unknown gates: "
                + ", ".join(sorted(unknown_gates))
            )

        validated_gates = {
            gate: validate_settings(settings, f"reviewer {reviewer} gate {gate}")
            for gate, settings in gates.items()
            if gate in REVIEW_GATES
        }
        for gate in REVIEW_GATES:
            resolved = dict(validated_default_gates.get(gate, {}))
            resolved.update(validated_gates.get(gate, {}))
            if set(resolved) != {"model", "effort"}:
                problems.append(f"reviewer {reviewer} gate {gate} must resolve model and effort")


def validate() -> list[str]:
    problems: list[str] = []
    validate_review_agent_defaults(problems)
    codex_marketplace = load_json(CODEX_MARKETPLACE, problems)
    claude_marketplace = load_json(CLAUDE_MARKETPLACE, problems)
    codex_plugins = marketplace_plugins(codex_marketplace, CODEX_MARKETPLACE, problems)
    claude_plugins = marketplace_plugins(claude_marketplace, CLAUDE_MARKETPLACE, problems)

    if codex_marketplace.get("name") != claude_marketplace.get("name"):
        problems.append("Claude Code and Codex marketplace names must match")

    codex_names = [plugin["name"] for plugin in codex_plugins]
    claude_names = [plugin["name"] for plugin in claude_plugins]
    if codex_names != claude_names:
        problems.append("Claude Code and Codex marketplace plugins must match in order")

    plugin_dirs = sorted(path.name for path in PLUGINS_ROOT.iterdir() if path.is_dir())
    if sorted(codex_names) != plugin_dirs:
        problems.append("marketplace plugins must match the plugin directories")

    claude_by_name = {plugin["name"]: plugin for plugin in claude_plugins}
    skill_plugins: list[tuple[str, str]] = []
    versions: set[str] = set()
    for codex_plugin in codex_plugins:
        plugin_name = codex_plugin["name"]
        plugin_root = PLUGINS_ROOT / plugin_name
        codex_manifest = load_json(plugin_root / ".codex-plugin/plugin.json", problems)
        claude_manifest = load_json(plugin_root / ".claude-plugin/plugin.json", problems)
        claude_plugin = claude_by_name.get(plugin_name, {})

        for field in SHARED_PLUGIN_FIELDS:
            if codex_manifest.get(field) != claude_manifest.get(field):
                problems.append(f"{plugin_name} manifest field must match: {field}")

        if codex_manifest.get("name") != plugin_root.name:
            problems.append(f"{plugin_name} manifest name must match the plugin folder")
        if claude_manifest.get("name") != plugin_name:
            problems.append(f"{plugin_name} Claude manifest name must match the plugin folder")
        if claude_plugin.get("description") != codex_manifest.get("description"):
            problems.append(f"{plugin_name} marketplace description must match the manifest")

        codex_source = codex_plugin.get("source")
        codex_path = codex_source.get("path") if isinstance(codex_source, dict) else None
        claude_path = claude_plugin.get("source")
        if codex_path != claude_path:
            problems.append(f"{plugin_name} marketplace paths must match")
        elif isinstance(codex_path, str):
            source_path = (ROOT / codex_path).resolve()
            if source_path != plugin_root.resolve() or not source_path.is_dir():
                problems.append(f"{plugin_name} marketplace path must point to its plugin folder")
        else:
            problems.append(f"{plugin_name} marketplace path is missing")

        skills = discover_skills(plugin_root / "skills", problems)
        skill_plugins.extend((skill, plugin_name) for skill in skills)

        skills_path = codex_manifest.get("skills")
        if skills and skills_path != "./skills/":
            problems.append(f"{plugin_name} Codex manifest must use ./skills/")
        if not skills and skills_path is not None:
            problems.append(f"{plugin_name} Codex manifest must omit skills")

        version = codex_manifest.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            problems.append(f"{plugin_name} version must use semantic versioning")
        else:
            versions.add(version)

    documented_skills = readme_skills(problems)
    sort_key = lambda item: (item[1], item[0])
    if documented_skills != sorted(documented_skills, key=sort_key):
        problems.append("README skills must be sorted by plugin and skill name")
    if documented_skills != sorted(skill_plugins, key=sort_key):
        problems.append("README skills must match the plugin skills")

    skill_names = [skill for skill, _ in skill_plugins]
    if len(skill_names) != len(set(skill_names)):
        problems.append("skill names must be unique across plugins")

    if len(versions) > 1:
        problems.append("all plugin manifests must use the same version")

    release_tag = os.environ.get("RELEASE_TAG")
    if release_tag and len(versions) == 1:
        version = next(iter(versions))
        if release_tag != f"v{version}":
            problems.append(f"release tag must be v{version}, got {release_tag}")

    return problems


def main() -> int:
    problems = validate()
    if problems:
        print("Repository validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    plugin_roots = [path for path in PLUGINS_ROOT.iterdir() if path.is_dir()]
    skill_count = sum(len(discover_skills(path / "skills", [])) for path in plugin_roots)
    print(f"Repository validation passed ({len(plugin_roots)} plugins, {skill_count} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
