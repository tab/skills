#!/usr/bin/env python3
"""Install the local marketplace with Claude Code and Codex."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins/tab"


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


def assert_package(installed_path: str) -> None:
    expected = plugin_files(PLUGIN_ROOT)
    installed = plugin_files(Path(installed_path))
    if expected != installed:
        missing = sorted(expected - installed)
        extra = sorted(installed - expected)
        raise RuntimeError(f"installed package differs from source: missing={missing}, extra={extra}")


def test_claude(plugin_id: str, version: str) -> None:
    with tempfile.TemporaryDirectory(prefix="tab-skills-claude-") as config_dir:
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = config_dir

        run(["claude", "plugin", "marketplace", "add", str(ROOT)], env)
        run(["claude", "plugin", "install", plugin_id, "--scope", "user", "--yes"], env)
        installed = json.loads(run(["claude", "plugin", "list", "--json"], env))
        match = next((item for item in installed if item.get("id") == plugin_id), None)
        if not match or match.get("version") != version:
            raise RuntimeError(f"Claude Code did not install {plugin_id} at version {version}")
        assert_package(match["installPath"])


def test_codex(plugin_id: str, plugin_name: str, version: str, skills: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="tab-skills-codex-") as config_dir:
        env = os.environ.copy()
        env["CODEX_HOME"] = config_dir

        run(["codex", "plugin", "marketplace", "add", str(ROOT), "--json"], env)
        install_result = json.loads(run(["codex", "plugin", "add", plugin_id, "--json"], env))
        result = json.loads(run(["codex", "plugin", "list", "--json"], env))
        match = next((item for item in result.get("installed", []) if item.get("pluginId") == plugin_id), None)
        if not match or match.get("version") != version:
            raise RuntimeError(f"Codex did not install {plugin_id} at version {version}")

        assert_package(install_result["installedPath"])

        if skills:
            prompt = json.loads(
                run(["codex", "debug", "prompt-input", "Use a repository skill."], env)
            )
            visible_text = json.dumps(prompt)
            for skill in skills:
                if f"- {plugin_name}:{skill}:" not in visible_text:
                    raise RuntimeError(f"Codex did not discover {plugin_name}:{skill}")


def main() -> int:
    for command in ("claude", "codex"):
        if shutil.which(command) is None:
            raise RuntimeError(f"required command not found: {command}")

    codex_marketplace = load_json(ROOT / ".agents/plugins/marketplace.json")
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin/plugin.json")
    plugin_name = manifest["name"]
    marketplace_name = codex_marketplace["name"]
    plugin_id = f"{plugin_name}@{marketplace_name}"
    version = manifest["version"]
    skills_root = PLUGIN_ROOT / "skills"
    skills = sorted(
        path.parent.name for path in skills_root.glob("*/SKILL.md")
    ) if skills_root.exists() else []

    test_claude(plugin_id, version)
    test_codex(plugin_id, plugin_name, version, skills)
    print(f"Marketplace tests passed for Claude Code and Codex ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
