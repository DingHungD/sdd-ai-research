from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .agent_tasks import create_task, list_tasks
from .io_utils import iso_now, read_json, write_json


DEFAULT_SELECTED_PATTERNS = [
    "README*",
    "docs/**",
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "src/**",
    "examples/**",
    "tests/**",
    "LICENSE*",
    "SECURITY*",
    "CHANGELOG*",
]


def _github_owner_name(url: str) -> tuple[str, str] | None:
    parts = urlsplit(url)
    if parts.netloc.lower() != "github.com":
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) < 2:
        return None
    return segments[0], segments[1]


def _default_branch(source: dict[str, Any]) -> str:
    repository = source.get("repository", {})
    return repository.get("default_branch") or "main"


def _looks_like_monorepo(source: dict[str, Any], owner: str, name: str) -> bool:
    repository = source.get("repository", {})
    if repository.get("is_monorepo") is True:
        return True
    if repository.get("repo_shape") == "monorepo":
        return True
    tags = {str(tag).lower() for tag in source.get("tags", [])}
    if "monorepo" in tags:
        return True
    monorepo_names = {
        ("langchain-ai", "langchain"),
        ("microsoft", "semantic-kernel"),
        ("google", "adk-python"),
    }
    return (owner.lower(), name.lower()) in monorepo_names


def _has_active_blocked_repo_task(topic_dir: Path, source_id: str) -> bool:
    for task in list_tasks(topic_dir):
        if task.get("agent_role") != "github_repo_analyst_agent":
            continue
        if task.get("status") not in {"pending", "in_progress", "blocked"}:
            continue
        if source_id in task.get("input", {}).get("source_ids", []):
            objective = str(task.get("objective", ""))
            if objective.startswith("Resolve GitHub repo deep-read scope"):
                return True
    return False


def _create_blocked_repo_task(topic_dir: Path, source_id: str, reason: str) -> None:
    source_path = f"knowledge-base/topics/{topic_dir.name}/sources/{source_id}/source.json"
    if _has_active_blocked_repo_task(topic_dir, source_id):
        return
    create_task(
        topic_dir,
        topic_id=topic_dir.name,
        agent_role="github_repo_analyst_agent",
        objective=f"Resolve GitHub repo deep-read scope for {source_id}.",
        paths_or_urls=[source_path],
        questions=[reason],
        constraints=[
            "Do not clone or read the full repository by default.",
            "Select only files needed for the research question.",
            "Return files_reviewed and files_not_reviewed before supporting critical implementation claims.",
        ],
        source_ids=[source_id],
        status="blocked",
        human_escalation_reason=reason,
    )


def build_repo_manifest(topic_dir: Path, source_id: str) -> dict[str, Any]:
    source_path = topic_dir / "sources" / source_id / "source.json"
    source = read_json(source_path)
    url = source.get("canonical_url") or source.get("url") or ""
    parsed = _github_owner_name(url)
    if not parsed:
        raise ValueError(f"{source_id} is not a GitHub repository source")
    owner, name = parsed
    repository = dict(source.get("repository") or {})
    repository.setdefault("owner", owner)
    repository.setdefault("name", name)
    repository.setdefault("default_branch", _default_branch(source))
    if source.get("commit_sha"):
        repository.setdefault("commit_sha", source["commit_sha"])
    commit_sha = repository.get("commit_sha") or source.get("commit_sha")

    needs_commit_pin = not bool(commit_sha)
    if commit_sha:
        tree_url = f"https://github.com/{owner}/{name}/tree/{commit_sha}"
        repository["tree_url"] = tree_url
        source.setdefault("immutable_url", tree_url)
    else:
        tree_url = f"https://github.com/{owner}/{name}/tree/{repository['default_branch']}"

    candidate_files = [
        {"pattern": pattern, "reason": "Candidate selected-file evidence path."}
        for pattern in DEFAULT_SELECTED_PATTERNS
    ]
    selected_files = [
        {
            "path": "README*",
            "permalink": tree_url,
            "selection_reason": "Project overview and positioning.",
            "claim_boundary": "Positioning only until paired with docs/config/source/examples/tests.",
        }
    ]
    blocked_reason = ""
    if needs_commit_pin:
        blocked_reason = "Repository source is not pinned to a commit SHA; capture a commit before critical claims."
    if _looks_like_monorepo(source, owner, name) and not repository.get("deep_read_scope"):
        blocked_reason = "Repository appears to be a monorepo or large repo and deep-read scope is not defined."

    manifest = {
        "source_id": source_id,
        "generated_at": iso_now(),
        "repository": {
            "owner": owner,
            "name": name,
            "default_branch": repository["default_branch"],
            "commit_sha": commit_sha,
            "tree_url": tree_url,
        },
        "capture_strategy": "selected_files",
        "needs_commit_pin": needs_commit_pin,
        "selected_file_patterns": DEFAULT_SELECTED_PATTERNS,
        "candidate_files": candidate_files,
        "selected_files": selected_files,
        "selection_reasons": [
            "Start with README for project positioning.",
            "Select docs/config/source/examples/tests before implementation, maturity, or security claims.",
        ],
        "files_reviewed": [
            {
                "path": "README*",
                "permalink": tree_url,
                "why_selected": "Project overview and positioning.",
                "evidence_used": "Use only for project positioning unless paired with source, docs, examples, or tests.",
            }
        ],
        "files_not_reviewed": [
            {
                "pattern_or_path": "**/*",
                "reason": "v1 manifest collector records selected-file intent without cloning or enumerating the full repository.",
            }
        ],
        "open_questions": [
            "Select concrete docs/config/source/examples/tests files before using this repository for implementation, maturity, or security claims."
        ],
        "blocked_reason": blocked_reason,
    }
    manifest_path = topic_dir / "sources" / source_id / "repo-manifest.json"
    write_json(manifest_path, manifest)

    repository["capture_scope"] = "selected_files"
    repository["capture_manifest_path"] = f"sources/{source_id}/repo-manifest.json"
    repository["selection_reason"] = "Selected-file manifest created for GitHub repo deep-read; review concrete files before critical implementation claims."
    repository["needs_commit_pin"] = needs_commit_pin
    if blocked_reason:
        repository["blocked_reason"] = blocked_reason
    source["repository"] = repository
    if commit_sha:
        source["commit_sha"] = commit_sha
    if source.get("immutable_url") is None and commit_sha:
        source["immutable_url"] = tree_url
    write_json(source_path, source)
    if blocked_reason:
        _create_blocked_repo_task(topic_dir, source_id, blocked_reason)
    return manifest
