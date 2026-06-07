from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .io_utils import read_json


HTML_NOISE_RE = re.compile(
    r"(<!doctype|<html|navbar|sidebar|cookie|skip to content|github\s+navigation|"
    r"sign in|sign up|stylesheet|javascript)",
    re.IGNORECASE,
)


def is_github_repo_source(source: dict[str, Any]) -> bool:
    if source.get("repository"):
        return True
    url = source.get("canonical_url") or source.get("url") or ""
    parts = urlsplit(url)
    segments = [segment for segment in parts.path.split("/") if segment]
    return parts.netloc.lower() == "github.com" and len(segments) >= 2


def _is_truncated_or_noisy(summary_text: str) -> bool:
    normalized = " ".join(summary_text.split())
    if len(normalized) < 160:
        return True
    if HTML_NOISE_RE.search(normalized):
        return True
    return False


def validate_summary(source: dict[str, Any], summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_id = source.get("source_id", summary.get("source_id", "<unknown>"))
    if source_id != summary.get("source_id"):
        errors.append(f"{source_id}: summary.source_id does not match source record")
    summary_text = summary.get("summary", "")
    if not isinstance(summary_text, str) or _is_truncated_or_noisy(summary_text):
        errors.append(f"{source_id}: summary appears too short, truncated, or polluted by HTML/navigation noise")

    key_points = summary.get("key_points", [])
    if not isinstance(key_points, list) or not key_points:
        errors.append(f"{source_id}: summary requires at least one key_point with locator")
    else:
        for index, point in enumerate(key_points, start=1):
            if not isinstance(point, dict) or not point.get("locator"):
                errors.append(f"{source_id}: key_points[{index}] requires a locator")

    if not summary.get("document_purpose"):
        errors.append(f"{source_id}: document_purpose is required")
    if not summary.get("keywords"):
        errors.append(f"{source_id}: keywords must be non-empty")
    if not summary.get("limitations"):
        errors.append(f"{source_id}: limitations must be non-empty")

    if is_github_repo_source(source):
        errors.extend(validate_repo_analysis(source, summary))
    return errors


def validate_repo_analysis(source: dict[str, Any], summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_id = source.get("source_id", "<unknown>")
    repository = source.get("repository", {})
    if not source.get("commit_sha") and not source.get("immutable_url") and not repository.get("commit_sha"):
        errors.append(f"{source_id}: GitHub repository source requires commit_sha or immutable_url")

    analysis = summary.get("repo_analysis")
    if not isinstance(analysis, dict):
        errors.append(f"{source_id}: GitHub repository summary requires repo_analysis")
        return errors

    if not analysis.get("commit_sha"):
        errors.append(f"{source_id}: repo_analysis.commit_sha is required")

    files_reviewed = analysis.get("files_reviewed", [])
    if not isinstance(files_reviewed, list) or not files_reviewed:
        errors.append(f"{source_id}: repo_analysis.files_reviewed must be non-empty")
    else:
        readme_only = True
        for index, item in enumerate(files_reviewed, start=1):
            path = str(item.get("path", "")) if isinstance(item, dict) else ""
            if not isinstance(item, dict) or not item.get("permalink") or not item.get("evidence_used"):
                errors.append(f"{source_id}: repo_analysis.files_reviewed[{index}] requires path, permalink, and evidence_used")
            if "readme" not in path.lower():
                readme_only = False
        if readme_only:
            errors.append(f"{source_id}: GitHub repository deep-read cannot rely on README only")

    if "files_not_reviewed" not in analysis:
        errors.append(f"{source_id}: repo_analysis.files_not_reviewed is required")

    feature_inventory = analysis.get("feature_inventory", [])
    if not isinstance(feature_inventory, list) or not feature_inventory:
        errors.append(f"{source_id}: repo_analysis.feature_inventory must be non-empty")
    else:
        for index, item in enumerate(feature_inventory, start=1):
            if not isinstance(item, dict) or not item.get("evidence_locators"):
                errors.append(f"{source_id}: repo_analysis.feature_inventory[{index}] requires evidence_locators")

    architecture = analysis.get("architecture_summary", {})
    if not isinstance(architecture, dict) or not architecture.get("components") or not architecture.get("data_or_control_flow"):
        errors.append(f"{source_id}: repo_analysis.architecture_summary requires components and data_or_control_flow")

    core_files = analysis.get("core_files", [])
    if not isinstance(core_files, list) or not core_files:
        errors.append(f"{source_id}: repo_analysis.core_files must be non-empty")
    else:
        for index, item in enumerate(core_files, start=1):
            if not isinstance(item, dict) or not item.get("locators"):
                errors.append(f"{source_id}: repo_analysis.core_files[{index}] requires locators")

    boundaries = analysis.get("capability_boundaries", {})
    if not isinstance(boundaries, dict) or not any(boundaries.get(key) for key in ("supported", "not_supported", "unclear")):
        errors.append(f"{source_id}: repo_analysis.capability_boundaries must describe supported, not_supported, or unclear capabilities")

    coverage = analysis.get("evidence_coverage", {})
    if isinstance(coverage, dict) and coverage.get("readme") and not (coverage.get("source") or coverage.get("tests") or coverage.get("examples") or coverage.get("docs")):
        errors.append(f"{source_id}: GitHub evidence coverage must include more than README for implementation claims")
    elif not isinstance(coverage, dict):
        errors.append(f"{source_id}: repo_analysis.evidence_coverage is required")
    return errors


def validate_topic_summaries(topic_dir: Path) -> list[str]:
    errors: list[str] = []
    for source_path in sorted((topic_dir / "sources").glob("S-*/source.json")):
        source = read_json(source_path)
        summary_path = source_path.with_name("summary.json")
        if not summary_path.exists():
            errors.append(f"{source['source_id']}: missing summary.json")
            continue
        summary = read_json(summary_path)
        errors.extend(validate_summary(source, summary))
    return errors
