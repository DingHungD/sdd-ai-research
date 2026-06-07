from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import iso_now, next_prefixed_id, read_json, write_json


AGENT_DEFAULTS: dict[str, dict[str, Any]] = {
    "source_hunter_agent": {
        "model": "gpt-5.4-mini",
        "reasoning_effort": "medium",
        "artifact_type": "crawl_queue_items",
        "schema": "schemas/source-crawl-queue.schema.json",
        "required_fields": ["target_type", "target", "reason"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/crawl-queue.json"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/reports/*", "knowledge-base/topics/<topic_id>/sources/S-*/summary.json"],
        "checks": ["crawl queue item has reason", "no duplicate URL without justification"],
        "done_when": ["new candidates are appended or remaining source gaps are documented"],
    },
    "source_curator_agent": {
        "model": "gpt-5.4",
        "reasoning_effort": "medium",
        "artifact_type": "document_summary",
        "schema": "schemas/document-summary.schema.json",
        "required_fields": ["document_purpose", "summary", "key_points", "keywords", "limitations"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/sources/S-*/summary.json", "knowledge-base/topics/<topic_id>/sources/S-*/summary.md"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/crawl-queue.json", "knowledge-base/topics/<topic_id>/reports/*"],
        "checks": ["summary gate passes", "key_points have locators"],
        "done_when": ["summary can support bounded claims or limitations are documented"],
    },
    "github_repo_analyst_agent": {
        "model": "gpt-5.4",
        "reasoning_effort": "medium",
        "artifact_type": "repo_analysis",
        "schema": "schemas/document-summary.schema.json#repo_analysis",
        "required_fields": ["commit_sha", "files_reviewed", "files_not_reviewed", "feature_inventory", "architecture_summary", "capability_boundaries"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/sources/S-*/source.json", "knowledge-base/topics/<topic_id>/sources/S-*/summary.json"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/reports/*"],
        "checks": ["commit SHA or immutable URL exists", "repo_analysis is not README-only"],
        "done_when": ["repo can support bounded implementation claims or limitations are explicit"],
    },
    "evidence_mapper_agent": {
        "model": "gpt-5.4",
        "reasoning_effort": "medium",
        "artifact_type": "claim_evidence_matrix",
        "schema": "schemas/report.schema.json#claims",
        "required_fields": ["claim_id", "supporting_source_ids", "confidence", "confidence_reason"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/reports/*.json", "knowledge-base/topics/<topic_id>/sources/S-*/source.json"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/sources/S-*/summary.json"],
        "checks": ["critical claims have support", "backlinks are symmetric"],
        "done_when": ["claim-evidence matrix is ready for report writing"],
    },
    "report_writer_agent": {
        "model": "gpt-5.5",
        "reasoning_effort": "medium",
        "artifact_type": "bilingual_synthesis",
        "schema": "schemas/report.schema.json",
        "required_fields": ["report_set_id", "localized_content", "claims", "sources"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/reports/*"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/crawl-queue.json", "knowledge-base/topics/<topic_id>/sources/S-*/*"],
        "checks": ["localized content exists", "evidence mapping unchanged"],
        "done_when": ["canonical JSON and localized Markdown are ready for quality gate"],
    },
    "quality_gate_agent": {
        "model": "gpt-5.4",
        "reasoning_effort": "medium",
        "artifact_type": "quality_gate_result",
        "schema": "schemas/report.schema.json",
        "required_fields": ["status", "errors", "warnings"],
        "allowed_paths": ["knowledge-base/topics/<topic_id>/agent-tasks/*"],
        "forbidden_paths": ["knowledge-base/topics/<topic_id>/sources/S-*/*", "knowledge-base/topics/<topic_id>/reports/*"],
        "checks": ["schema validation", "summary gate", "report gate", "crawl queue validation"],
        "done_when": ["publication blockers are listed or the report set passes"],
    },
}


def tasks_dir(topic_dir: Path) -> Path:
    return topic_dir / "agent-tasks"


def list_tasks(topic_dir: Path) -> list[dict[str, Any]]:
    directory = tasks_dir(topic_dir)
    if not directory.exists():
        return []
    return [read_json(path) for path in sorted(directory.glob("T-*.json"))]


def _next_task_id(topic_dir: Path) -> str:
    return next_prefixed_id([task["task_id"] for task in list_tasks(topic_dir)], "T")


def create_task(
    topic_dir: Path,
    *,
    topic_id: str,
    agent_role: str,
    objective: str,
    paths_or_urls: list[str] | None = None,
    questions: list[str] | None = None,
    constraints: list[str] | None = None,
    source_ids: list[str] | None = None,
    claim_ids: list[str] | None = None,
    status: str = "pending",
    human_escalation_reason: str | None = None,
) -> dict[str, Any]:
    if agent_role not in AGENT_DEFAULTS:
        raise ValueError(f"unknown agent role: {agent_role}")
    defaults = AGENT_DEFAULTS[agent_role]
    task_id = _next_task_id(topic_dir)
    task: dict[str, Any] = {
        "task_id": task_id,
        "topic_id": topic_id,
        "agent_role": agent_role,
        "model": defaults["model"],
        "reasoning_effort": defaults["reasoning_effort"],
        "objective": objective,
        "input": {
            "paths_or_urls": paths_or_urls or [],
            "source_ids": source_ids or [],
            "claim_ids": claim_ids or [],
            "questions": questions or [objective],
            "constraints": constraints or [],
        },
        "expected_output": {
            "artifact_type": defaults["artifact_type"],
            "schema": defaults["schema"],
            "required_fields": defaults["required_fields"],
        },
        "write_scope": {
            "allowed_paths": [path.replace("<topic_id>", topic_id) for path in defaults["allowed_paths"]],
            "forbidden_paths": [path.replace("<topic_id>", topic_id) for path in defaults["forbidden_paths"]],
        },
        "quality_gate": {
            "checks": defaults["checks"],
            "done_when": defaults["done_when"],
        },
        "status": status,
        "created_at": iso_now(),
        "updated_at": iso_now(),
    }
    if human_escalation_reason:
        task["human_escalation_reason"] = human_escalation_reason
    write_json(tasks_dir(topic_dir) / f"{task_id}.json", task)
    return task


def validate_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "task_id",
        "topic_id",
        "agent_role",
        "model",
        "reasoning_effort",
        "objective",
        "input",
        "expected_output",
        "write_scope",
        "quality_gate",
        "status",
    ):
        if field not in task:
            errors.append(f"missing required field: {field}")
    role = task.get("agent_role")
    if role not in AGENT_DEFAULTS:
        errors.append(f"invalid agent_role: {role}")
    if task.get("status") not in {"pending", "in_progress", "completed", "failed", "blocked"}:
        errors.append(f"invalid status: {task.get('status')}")
    input_data = task.get("input", {})
    if not isinstance(input_data, dict):
        errors.append("input must be an object")
    else:
        for field in ("paths_or_urls", "questions", "constraints"):
            if field not in input_data:
                errors.append(f"input missing required field: {field}")
        if not input_data.get("questions"):
            errors.append("input.questions must be non-empty")
        if role == "github_repo_analyst_agent" and not (input_data.get("source_ids") or input_data.get("paths_or_urls")):
            errors.append("github_repo_analyst_agent task requires source_ids or paths_or_urls")
    expected = task.get("expected_output", {})
    if not isinstance(expected, dict):
        errors.append("expected_output must be an object")
    else:
        for field in ("artifact_type", "schema", "required_fields"):
            if field not in expected:
                errors.append(f"expected_output missing required field: {field}")
    return errors


def validate_task_result(task: dict[str, Any], result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(result, dict):
        return ["result must be an object"]

    result_status = result.get("status", "completed")
    if result_status not in {"completed", "failed", "blocked"}:
        errors.append("result.status must be completed, failed, or blocked")

    if result_status == "completed":
        required_fields = task.get("expected_output", {}).get("required_fields", [])
        for field in required_fields:
            if field not in result or result[field] in (None, "", []):
                errors.append(f"result missing required field for completed task: {field}")

    if result_status in {"failed", "blocked"} and not (
        result.get("errors")
        or result.get("warnings")
        or result.get("human_escalation_reason")
        or result.get("blocker")
    ):
        errors.append("failed or blocked result must include errors, warnings, blocker, or human_escalation_reason")

    if task.get("agent_role") == "github_repo_analyst_agent" and result_status == "completed":
        if not (result.get("commit_sha") or result.get("immutable_url")):
            errors.append("completed GitHub repo analysis requires commit_sha or immutable_url")
        if not result.get("files_reviewed"):
            errors.append("completed GitHub repo analysis requires files_reviewed")
        if not result.get("files_not_reviewed"):
            errors.append("completed GitHub repo analysis requires files_not_reviewed")

    return errors


def load_task(topic_dir: Path, task_id: str) -> dict[str, Any]:
    return read_json(tasks_dir(topic_dir) / f"{task_id}.json")


def update_task(topic_dir: Path, task_id: str, **changes: Any) -> dict[str, Any]:
    task = load_task(topic_dir, task_id)
    task.update(changes)
    task["updated_at"] = iso_now()
    write_json(tasks_dir(topic_dir) / f"{task_id}.json", task)
    return task


def start_task(topic_dir: Path, task_id: str) -> dict[str, Any]:
    task = load_task(topic_dir, task_id)
    if task.get("status") not in {"pending", "blocked"}:
        raise ValueError(f"cannot start task from status: {task.get('status')}")
    return update_task(topic_dir, task_id, status="in_progress")


def block_task(topic_dir: Path, task_id: str, reason: str) -> dict[str, Any]:
    if not reason:
        raise ValueError("blocked task requires a reason")
    return update_task(
        topic_dir,
        task_id,
        status="blocked",
        human_escalation_reason=reason,
        result={"status": "blocked", "blocker": reason},
    )


def fail_task(topic_dir: Path, task_id: str, reason: str) -> dict[str, Any]:
    if not reason:
        raise ValueError("failed task requires a reason")
    return update_task(
        topic_dir,
        task_id,
        status="failed",
        result={"status": "failed", "errors": [reason]},
    )


def complete_task(topic_dir: Path, task_id: str, result: dict[str, Any]) -> dict[str, Any]:
    task = load_task(topic_dir, task_id)
    errors = validate_task(task) + validate_task_result(task, result)
    if errors:
        raise ValueError("; ".join(errors))
    return update_task(topic_dir, task_id, status=result.get("status", "completed"), result=result)
