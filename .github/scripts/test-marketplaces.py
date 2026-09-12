#!/usr/bin/env python3
"""Install the local marketplace with Claude Code and Codex."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLUGINS_ROOT = ROOT / "plugins"
REVIEW_RESOLVER = (
    PLUGINS_ROOT / "workflow" / "skills" / "feature" / "scripts" / "resolve-review-agent.py"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"command failed: {' '.join(command)}\n{detail}")
    return result.stdout


def plugin_files(path: Path) -> set[str]:
    return {
        file.relative_to(path).as_posix()
        for file in path.rglob("*")
        if file.is_file() and file.name not in {".DS_Store"}
    }


def assert_package(plugin_root: Path, installed_path: str) -> None:
    expected = plugin_files(plugin_root)
    installed = plugin_files(Path(installed_path))
    if expected != installed:
        missing = sorted(expected - installed)
        extra = sorted(installed - expected)
        raise RuntimeError(f"installed package differs from source: missing={missing}, extra={extra}")


def resolve_review_config(project_root: Path, gate: str, reviewer: str | None = None) -> dict[str, Any]:
    command = [
        sys.executable,
        str(REVIEW_RESOLVER),
        "--project-root",
        str(project_root),
        "--gate",
        gate,
    ]
    if reviewer:
        command.extend(["--reviewer", reviewer])

    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def test_review_config() -> None:
    with tempfile.TemporaryDirectory(prefix="skills-review-config-") as test_dir:
        test_root = Path(test_dir)
        project_root = test_root / "project"
        project_root.mkdir()

        expected_defaults = {
            "codex": {
                "plan": ("gpt-5.6-terra", "high"),
                "code": ("gpt-5.6-luna", "high"),
                "pr": ("gpt-5.6-luna", "high"),
                "follow-up": ("gpt-5.6-luna", "medium"),
            },
            "claude": {
                "plan": ("opus", "high"),
                "code": ("opus", "high"),
                "pr": ("sonnet", "high"),
                "follow-up": ("sonnet", "medium"),
            },
        }
        for reviewer, gates in expected_defaults.items():
            selected_reviewer = None if reviewer == "codex" else reviewer
            for gate, (model, effort) in gates.items():
                resolved = resolve_review_config(project_root, gate, selected_reviewer)
                expected = {
                    "effort": effort,
                    "gate": gate,
                    "model": model,
                    "reviewer": reviewer,
                    "sources": (
                        ["default"]
                        if reviewer == "codex"
                        else ["default", f"reviewers.{reviewer}"]
                    ),
                }
                if resolved != expected:
                    raise RuntimeError(f"unexpected default {reviewer} {gate} config: {resolved}")

        codex_dir = project_root / ".codex"
        codex_dir.mkdir()
        (codex_dir / "feature-review.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "gates": {"code": {"model": "gpt-5.6-sol", "effort": "low"}},
                }
            ),
            encoding="utf-8",
        )
        code_review = resolve_review_config(project_root, "code")
        if code_review != {
            "effort": "low",
            "gate": "code",
            "model": "gpt-5.6-sol",
            "reviewer": "codex",
            "sources": ["default", ".codex/feature-review.json"],
        }:
            raise RuntimeError(f"Codex project override was not applied: {code_review}")

        claude_dir = project_root / ".claude"
        claude_dir.mkdir()
        (claude_dir / "feature-review.json").write_text(
            json.dumps(
                {
                    "version": 1,
                    "gates": {"pr": {"model": "project-model", "effort": "low"}},
                }
            ),
            encoding="utf-8",
        )
        pr_review = resolve_review_config(project_root, "pr", "claude")
        if pr_review != {
            "effort": "low",
            "gate": "pr",
            "model": "project-model",
            "reviewer": "claude",
            "sources": ["default", "reviewers.claude", ".claude/feature-review.json"],
        }:
            raise RuntimeError(f"Claude project override was not applied: {pr_review}")

        (codex_dir / "feature-review.json").write_text(
            json.dumps({"version": 1, "gates": {"unknown": {"model": "test"}}}),
            encoding="utf-8",
        )
        invalid = subprocess.run(
            [
                sys.executable,
                str(REVIEW_RESOLVER),
                "--project-root",
                str(project_root),
                "--gate",
                "code",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if invalid.returncode != 2 or "unknown gate" not in invalid.stderr:
            raise RuntimeError("invalid project review config did not stop resolution")

        outside_config = test_root / "outside.json"
        outside_config.write_text(
            json.dumps({"version": 1, "gates": {"code": {"effort": "high"}}}),
            encoding="utf-8",
        )
        (codex_dir / "feature-review.json").unlink()
        (codex_dir / "feature-review.json").symlink_to(outside_config)
        escaped = subprocess.run(
            [
                sys.executable,
                str(REVIEW_RESOLVER),
                "--project-root",
                str(project_root),
                "--gate",
                "code",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if escaped.returncode != 2 or "leaves the project root" not in escaped.stderr:
            raise RuntimeError("review config outside the project root was not rejected")

    print("Review config resolver tests passed")


def test_claude(plugins: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory(prefix="skills-claude-") as config_dir:
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = config_dir

        run(["claude", "plugin", "marketplace", "add", str(ROOT)], env)
        for plugin in plugins:
            run(
                ["claude", "plugin", "install", plugin["id"], "--scope", "user", "--yes"],
                env,
            )

        installed = json.loads(run(["claude", "plugin", "list", "--json"], env))
        for plugin in plugins:
            match = next((item for item in installed if item.get("id") == plugin["id"]), None)
            if not match or match.get("version") != plugin["version"]:
                raise RuntimeError(
                    f"Claude Code did not install {plugin['id']} at version {plugin['version']}"
                )
            assert_package(plugin["root"], match["installPath"])


def test_codex(plugins: list[dict[str, Any]]) -> None:
    with tempfile.TemporaryDirectory(prefix="skills-codex-") as config_dir:
        env = os.environ.copy()
        env["CODEX_HOME"] = config_dir

        run(["codex", "plugin", "marketplace", "add", str(ROOT), "--json"], env)
        install_results: dict[str, dict[str, Any]] = {}
        for plugin in plugins:
            install_results[plugin["name"]] = json.loads(
                run(["codex", "plugin", "add", plugin["id"], "--json"], env)
            )

        result = json.loads(run(["codex", "plugin", "list", "--json"], env))
        for plugin in plugins:
            match = next(
                (
                    item
                    for item in result.get("installed", [])
                    if item.get("pluginId") == plugin["id"]
                ),
                None,
            )
            if not match or match.get("version") != plugin["version"]:
                raise RuntimeError(
                    f"Codex did not install {plugin['id']} at version {plugin['version']}"
                )
            assert_package(plugin["root"], install_results[plugin["name"]]["installedPath"])

        if any(plugin["skills"] for plugin in plugins):
            prompt = json.loads(
                run(["codex", "debug", "prompt-input", "Use a repository skill."], env)
            )
            visible_text = json.dumps(prompt)
            for plugin in plugins:
                for skill in plugin["skills"]:
                    if f"- {plugin['name']}:{skill}:" not in visible_text:
                        raise RuntimeError(f"Codex did not discover {plugin['name']}:{skill}")


def main() -> int:
    for command in ("claude", "codex"):
        if shutil.which(command) is None:
            raise RuntimeError(f"required command not found: {command}")

    test_review_config()

    codex_marketplace = load_json(ROOT / ".agents/plugins/marketplace.json")
    marketplace_name = codex_marketplace["name"]
    plugins: list[dict[str, Any]] = []
    for entry in codex_marketplace["plugins"]:
        plugin_name = entry["name"]
        plugin_root = PLUGINS_ROOT / plugin_name
        manifest = load_json(plugin_root / ".codex-plugin/plugin.json")
        skills_root = plugin_root / "skills"
        skills = (
            sorted(path.parent.name for path in skills_root.glob("*/SKILL.md"))
            if skills_root.exists()
            else []
        )
        plugins.append(
            {
                "id": f"{plugin_name}@{marketplace_name}",
                "name": plugin_name,
                "root": plugin_root,
                "skills": skills,
                "version": manifest["version"],
            }
        )

    for plugin in plugins:
        test_claude([plugin])
        test_codex([plugin])

    test_claude(plugins)
    test_codex(plugins)
    skill_count = sum(len(plugin["skills"]) for plugin in plugins)
    print(
        "Standalone and combined marketplace tests passed for Claude Code and Codex "
        f"({len(plugins)} plugins, {skill_count} skills)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
