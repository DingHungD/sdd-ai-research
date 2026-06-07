from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

AGENT_DISPLAY_NAMES = {
    "Main Research Agent": None,
    "Source Hunter Agent": "source_hunter_agent",
    "Source Curator Agent": "source_curator_agent",
    "GitHub Repo Analyst Agent": "github_repo_analyst_agent",
    "Evidence Mapper Agent": "evidence_mapper_agent",
    "Report Writer Agent": "report_writer_agent",
    "Quality Gate Agent": "quality_gate_agent",
}

TOML_NAME_TO_ROLE = {
    "source-hunter": "source_hunter_agent",
    "source-curator": "source_curator_agent",
    "github-repo-analyst": "github_repo_analyst_agent",
    "evidence-mapper": "evidence_mapper_agent",
    "report-writer": "report_writer_agent",
    "quality-gate": "quality_gate_agent",
}

CORE_DOCS = [
    "README.md",
    "AGENTS.md",
    "docs/PROJECT_INTRO.md",
    "docs/RESEARCH_WORKFLOW.md",
    "docs/AUTOMATION_PIPELINE.md",
    "docs/AGENT_ORCHESTRATION.md",
    "docs/WORKFLOW_ALIGNMENT.md",
]

PATH_ALIGNMENT_DOCS = [
    "README.md",
    "docs/PROJECT_INTRO.md",
    "docs/RESEARCH_WORKFLOW.md",
    "docs/AUTOMATION_PIPELINE.md",
]

CORE_PATHS = [
    "AGENTS.md",
    ".codex/agents",
    "docs/RESEARCH_WORKFLOW.md",
    "docs/AUTOMATION_PIPELINE.md",
    "docs/WORKFLOW_ALIGNMENT.md",
    "schemas/subagent-task.schema.json",
    "scripts/research_pipeline.py",
    "knowledge-base/topics/<topic_id>/",
]

MOJIBAKE_MARKERS = ["\ufffd"] + [
    chr(codepoint)
    for codepoint in (
        0x929D,
        0x8754,
        0x5697,
        0x64A0,
        0x6470,
        0x96BF,
        0x969E,
        0x9758,
    )
]


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)} is not valid UTF-8: {exc}")
        return ""


def check_agent_mentions(errors: list[str]) -> None:
    agents = read_text(ROOT / "AGENTS.md", errors)
    intro = read_text(ROOT / "docs" / "PROJECT_INTRO.md", errors)
    for display_name in list(AGENT_DISPLAY_NAMES)[1:]:
        if display_name not in agents:
            errors.append(f"AGENTS.md does not mention {display_name}.")
    for display_name in AGENT_DISPLAY_NAMES:
        if display_name not in intro:
            errors.append(f"docs/PROJECT_INTRO.md does not mention {display_name}.")


def check_toml_agents(errors: list[str]) -> set[str]:
    agent_dir = ROOT / ".codex" / "agents"
    if not agent_dir.exists():
        errors.append(".codex/agents directory is missing.")
        return set()

    roles: set[str] = set()
    files = sorted(agent_dir.glob("*.toml"))
    if len(files) != 6:
        errors.append(f".codex/agents should contain 6 TOML files, found {len(files)}.")

    for path in files:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)} cannot be parsed as TOML: {exc}")
            continue

        for key in ("name", "description", "developer_instructions"):
            if not data.get(key):
                errors.append(f"{path.relative_to(ROOT)} is missing {key}.")

        name = data.get("name")
        role = TOML_NAME_TO_ROLE.get(name)
        if not role:
            errors.append(f"{path.relative_to(ROOT)} has unmapped name {name!r}.")
            continue
        roles.add(role)

    return roles


def check_schema_roles(agent_roles: set[str], errors: list[str]) -> None:
    schema_path = ROOT / "schemas" / "subagent-task.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    role_enum = set(schema["properties"]["agent_role"]["enum"])
    expected = {role for role in AGENT_DISPLAY_NAMES.values() if role}
    if role_enum != expected:
        errors.append(
            "schemas/subagent-task.schema.json agent_role enum does not match expected roles: "
            f"expected={sorted(expected)} actual={sorted(role_enum)}"
        )
    if agent_roles and agent_roles != role_enum:
        errors.append(
            ".codex/agents role mapping does not match subagent-task schema: "
            f"toml={sorted(agent_roles)} schema={sorted(role_enum)}"
        )


def check_core_paths(errors: list[str]) -> None:
    for doc in PATH_ALIGNMENT_DOCS:
        text = read_text(ROOT / doc, errors)
        for core_path in CORE_PATHS:
            if core_path not in text:
                errors.append(f"{doc} does not reference {core_path}.")


def check_encoding_and_mojibake(errors: list[str]) -> None:
    paths: list[Path] = []
    paths.extend(ROOT.glob("*.md"))
    paths.extend((ROOT / "docs").glob("*.md"))
    paths.extend((ROOT / ".codex" / "agents").glob("*.toml"))
    paths.extend((ROOT / "research_pipeline").glob("*.py"))
    paths.extend((ROOT / "scripts").glob("*.py"))

    for path in sorted(set(paths)):
        text = read_text(path, errors)
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                errors.append(f"{path.relative_to(ROOT)} contains mojibake marker {marker!r}.")
                break


def table_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current.append(stripped)
            continue
        if current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)
    return blocks


def pipe_count(line: str) -> int:
    return len(re.findall(r"(?<!\\)\|", line))


def check_markdown_tables(errors: list[str]) -> None:
    for doc in CORE_DOCS:
        path = ROOT / doc
        text = read_text(path, errors)
        for index, block in enumerate(table_blocks(text), start=1):
            counts = {pipe_count(line) for line in block}
            if len(counts) > 1:
                errors.append(f"{doc} table #{index} has inconsistent column counts: {sorted(counts)}.")
            if len(block) >= 2:
                separator_cells = [cell.strip() for cell in block[1].strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator_cells):
                    errors.append(f"{doc} table #{index} has an invalid separator row.")


def main() -> int:
    errors: list[str] = []
    check_agent_mentions(errors)
    agent_roles = check_toml_agents(errors)
    check_schema_roles(agent_roles, errors)
    check_core_paths(errors)
    check_encoding_and_mojibake(errors)
    check_markdown_tables(errors)

    if errors:
        print("Workflow alignment validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Workflow alignment validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
