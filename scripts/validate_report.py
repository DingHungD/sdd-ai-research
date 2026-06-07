#!/usr/bin/env python3
"""Run dependency-free consistency checks for a structured research report."""

from __future__ import annotations

import json
import argparse
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from research_pipeline.quality_gate import evaluate_report_details
from research_pipeline.summary_quality import is_github_repo_source, validate_summary


REQUIRED_REPORT_FIELDS = {
    "report_id",
    "version",
    "title",
    "generated_at",
    "data_cutoff",
    "overall_confidence",
    "quality_score",
    "structural_score",
    "quality_metrics",
    "executive_summary",
    "questions",
    "scope",
    "methodology",
    "claims",
    "sources",
    "conflicts",
    "unknowns",
    "resolution_matrix",
    "limitations",
    "conclusion",
    "recommendation_sections",
    "changelog",
}

ALLOWED_REPORT_FIELDS = REQUIRED_REPORT_FIELDS | {
    "minimum_sources",
    "minimum_primary_sources",
    "minimum_high_quality_sources",
    "recommendations",
    "report_set_id",
    "primary_language",
    "languages",
    "localized_content",
}

REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "title",
    "url",
    "canonical_url",
    "content_hash",
    "locator",
    "retrieved_at",
    "local_snapshots",
    "freshness",
    "source_type",
    "evidence_tier",
    "quality",
    "evidence_chain",
    "supported_claim_ids",
}

RECOMMENDATION_ITEM_FIELDS = {
    "implementability": {
        "title",
        "objective",
        "technologies",
        "workflow",
        "minimum_deliverable",
        "acceptance_criteria",
        "supporting_source_ids",
        "research_prompt",
    },
    "single_tool_recommendations": {
        "rank",
        "tool",
        "recommendation_reason",
        "suitable_for",
        "strengths",
        "gaps",
        "minimum_adoption",
        "supporting_source_ids",
        "research_prompt",
    },
    "multi_tool_recommendations": {
        "rank",
        "title",
        "tools",
        "objective",
        "roles",
        "workflow",
        "recommendation_reason",
        "tradeoffs",
        "minimum_deliverable",
        "acceptance_criteria",
        "supporting_source_ids",
        "research_prompt",
    },
    "future_directions": {
        "title",
        "current_limitation",
        "direction",
        "trigger",
        "supporting_source_ids",
        "research_prompt",
    },
}



def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_source_linked_items(value):
    if isinstance(value, dict):
        if "supporting_source_ids" in value:
            yield value
        for nested in value.values():
            yield from iter_source_linked_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from iter_source_linked_items(nested)


def validate_recommendation_items(report: dict, source_id_set: set[str]) -> list[str]:
    errors: list[str] = []
    sections = report.get("recommendation_sections", {})
    if not isinstance(sections, dict):
        return ["recommendation_sections must be an object"]
    open_source_options = sections.get("open_source_options", {})
    if not isinstance(open_source_options, dict):
        open_source_options = {}
    paths = {
        "implementability": sections.get("implementability", {}),
        "single_tool_recommendations": open_source_options.get("single_tool_recommendations", {}),
        "multi_tool_recommendations": open_source_options.get("multi_tool_recommendations", {}),
        "future_directions": sections.get("future_directions", {}),
    }
    for section_name, section in paths.items():
        if not isinstance(section, dict):
            errors.append(f"recommendation_sections.{section_name} must be an object")
            continue
        items = section.get("items", [])
        if not isinstance(items, list):
            errors.append(f"recommendation_sections.{section_name}.items must be an array")
            continue
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"recommendation_sections.{section_name}.items[{index}] must be an object")
                continue
            missing = sorted(RECOMMENDATION_ITEM_FIELDS[section_name] - item.keys())
            if missing:
                errors.append(f"recommendation/{section_name}[{index}]: missing fields: {', '.join(missing)}")
            supporting_ids = item.get("supporting_source_ids", [])
            if not isinstance(supporting_ids, list):
                errors.append(f"recommendation/{section_name}[{index}]: supporting_source_ids must be an array")
                continue
            unknown = sorted(set(supporting_ids) - source_id_set)
            if unknown:
                errors.append(f"recommendation/{section_name}[{index}]: unknown supporting source ids: {', '.join(unknown)}")
    return errors


def validate_language_metadata(report: dict) -> list[str]:
    errors: list[str] = []
    languages = report.get("languages")
    report_set_id = report.get("report_set_id")
    if languages is None and report_set_id is None and "localized_content" not in report:
        return errors
    if not report_set_id:
        errors.append("report_set_id is required for bilingual/localized reports")
    if not isinstance(languages, list) or not languages:
        errors.append("languages must be a non-empty array for bilingual/localized reports")
        languages = []
    if len(languages) != len(set(languages)):
        errors.append("languages must not contain duplicates")
    primary = report.get("primary_language")
    if primary and languages and primary not in languages:
        errors.append("primary_language must be included in languages")
    localized = report.get("localized_content", {})
    if not isinstance(localized, dict):
        errors.append("localized_content must be an object")
        return errors
    for language in languages:
        content = localized.get(language)
        if not isinstance(content, dict):
            errors.append(f"localized_content.{language} is required")
            continue
        for field in ("title", "executive_summary", "conclusion"):
            if field not in content or not content[field]:
                errors.append(f"localized_content.{language}.{field} is required")
    return errors


def validate_bilingual_files(report_path: Path, report: dict) -> list[str]:
    errors: list[str] = []
    report_set_id = report.get("report_set_id")
    languages = report.get("languages", [])
    if not report_set_id or not isinstance(languages, list):
        return errors
    for language in languages:
        path = report_path.parent / f"{report_set_id}.{language}.md"
        if not path.exists():
            errors.append(f"missing localized markdown output: {path.name}")
    return errors


def validate_github_summary_gate(report_path: Path, report: dict) -> list[str]:
    errors: list[str] = []
    if "languages" not in report:
        return errors
    topic_dir = report_path.parent.parent
    for source in report.get("sources", []):
        if not isinstance(source, dict) or not is_github_repo_source(source):
            continue
        summary_path = topic_dir / "sources" / source["source_id"] / "summary.json"
        if not summary_path.exists():
            errors.append(f"{source['source_id']}: missing summary.json for GitHub source")
            continue
        try:
            summary = load_json(summary_path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{source['source_id']}: cannot read summary.json: {exc}")
            continue
        critical_claims = [
            claim
            for claim in report.get("claims", [])
            if source["source_id"] in claim.get("supporting_source_ids", []) and claim.get("importance") == "critical"
        ]
        if critical_claims:
            errors.extend(validate_summary(source, summary))
    return errors


def validate(report: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_REPORT_FIELDS - report.keys())
    if missing:
        errors.append(f"missing required report fields: {', '.join(missing)}")
    extra = sorted(report.keys() - ALLOWED_REPORT_FIELDS)
    if extra:
        errors.append(f"unknown report fields: {', '.join(extra)}")
    errors.extend(validate_language_metadata(report))

    claims = report.get("claims", [])
    sources = report.get("sources", [])
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        claims = []
    if not isinstance(sources, list):
        errors.append("sources must be an array")
        sources = []

    source_ids = [source.get("source_id") for source in sources if isinstance(source, dict)]
    source_id_set = {source_id for source_id in source_ids if source_id}
    if len(source_ids) != len(source_id_set):
        errors.append("source_id values must be unique and non-empty")

    claim_ids = [claim.get("claim_id") for claim in claims if isinstance(claim, dict)]
    claim_id_set = {claim_id for claim_id in claim_ids if claim_id}
    if len(claim_ids) != len(claim_id_set):
        errors.append("claim_id values must be unique and non-empty")

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("each claim must be an object")
            continue
        claim_id = claim.get("claim_id", "<unknown>")
        supporting_ids = claim.get("supporting_source_ids", [])
        if not isinstance(supporting_ids, list):
            errors.append(f"{claim_id}: supporting_source_ids must be an array")
            continue
        missing_sources = sorted(set(supporting_ids) - source_id_set)
        if missing_sources:
            errors.append(f"{claim_id}: unknown supporting source ids: {', '.join(missing_sources)}")
        opposing_ids = claim.get("opposing_source_ids", [])
        if not isinstance(opposing_ids, list):
            errors.append(f"{claim_id}: opposing_source_ids must be an array")
        else:
            missing_opposing = sorted(set(opposing_ids) - source_id_set)
            if missing_opposing:
                errors.append(f"{claim_id}: unknown opposing source ids: {', '.join(missing_opposing)}")
        if claim.get("importance") == "critical" and not supporting_ids:
            errors.append(f"{claim_id}: critical claim has no supporting source")

    errors.extend(validate_recommendation_items(report, source_id_set))

    allowed_resolution_statuses = {"resolved", "partially_resolved", "open"}
    matrix = report.get("resolution_matrix", {})
    if not isinstance(matrix, dict):
        errors.append("resolution_matrix must be an object")
        matrix = {}
    if not matrix.get("summary"):
        errors.append("resolution_matrix.summary must be non-empty")
    conflict_resolutions = matrix.get("conflict_resolutions", [])
    unknown_resolutions = matrix.get("unknown_resolutions", [])
    if not isinstance(conflict_resolutions, list) or not isinstance(unknown_resolutions, list):
        errors.append("resolution_matrix resolution groups must be arrays")
        conflict_resolutions = []
        unknown_resolutions = []
    resolutions = conflict_resolutions + unknown_resolutions
    resolution_ids = [item.get("resolution_id") if isinstance(item, dict) else None for item in resolutions]
    if len(resolution_ids) != len({item_id for item_id in resolution_ids if item_id}):
        errors.append("resolution_id values must be unique and non-empty")
    for item in resolutions:
        if not isinstance(item, dict):
            errors.append("each resolution item must be an object")
            continue
        resolution_id = item.get("resolution_id", "<unknown>")
        if item.get("status") not in allowed_resolution_statuses:
            errors.append(f"{resolution_id}: status must be resolved, partially_resolved, or open")
        if "supporting_source_ids" not in item:
            errors.append(f"{resolution_id}: missing supporting_source_ids")
        supporting_ids = item.get("supporting_source_ids", [])
        if not isinstance(supporting_ids, list):
            errors.append(f"{resolution_id}: supporting_source_ids must be an array")
            continue
        missing_sources = sorted(set(supporting_ids) - source_id_set)
        if missing_sources:
            errors.append(f"{resolution_id}: unknown supporting source ids: {', '.join(missing_sources)}")

    for source in sources:
        if not isinstance(source, dict):
            errors.append("each source must be an object")
            continue
        source_id = source.get("source_id", "<unknown>")
        missing_source_fields = sorted(REQUIRED_SOURCE_FIELDS - source.keys())
        if missing_source_fields:
            errors.append(f"{source_id}: missing source fields: {', '.join(missing_source_fields)}")
        if not source.get("locator"):
            errors.append(f"{source_id}: locator must be non-empty")
        if not source.get("evidence_chain"):
            errors.append(f"{source_id}: evidence_chain must be non-empty")
        content_hash = source.get("content_hash", "")
        if not isinstance(content_hash, str) or not content_hash.startswith("sha256:") or len(content_hash) != 71:
            errors.append(f"{source_id}: content_hash must be a SHA-256 value")
        snapshots = source.get("local_snapshots", [])
        if not isinstance(snapshots, list) or not snapshots:
            errors.append(f"{source_id}: local_snapshots must contain at least one snapshot")
        else:
            latest_hash = snapshots[-1].get("content_hash")
            if latest_hash != content_hash:
                errors.append(f"{source_id}: content_hash must match the latest snapshot")
        freshness = source.get("freshness", {})
        if not isinstance(freshness, dict):
            errors.append(f"{source_id}: freshness must be an object")
        elif freshness.get("mode") in {"periodic", "volatile"} and not freshness.get("recheck_after"):
            errors.append(f"{source_id}: periodic or volatile freshness requires recheck_after")
        supported_ids = source.get("supported_claim_ids", [])
        if not isinstance(supported_ids, list):
            errors.append(f"{source_id}: supported_claim_ids must be an array")
            continue
        missing_claims = sorted(set(supported_ids) - claim_id_set)
        if missing_claims:
            errors.append(f"{source_id}: unknown supported claim ids: {', '.join(missing_claims)}")

    expected_backlinks = {source_id: set() for source_id in source_id_set}
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        for source_id in claim.get("supporting_source_ids", []):
            expected_backlinks.setdefault(source_id, set()).add(claim.get("claim_id"))
    for source in sources:
        if not isinstance(source, dict):
            continue
        source_id = source.get("source_id", "<unknown>")
        actual = set(source.get("supported_claim_ids", []))
        expected = expected_backlinks.get(source_id, set())
        if actual != expected:
            errors.append(
                f"{source_id}: supported_claim_ids backlink mismatch; expected {sorted(expected)}, found {sorted(actual)}"
            )

    if len(conflict_resolutions) < len(report.get("conflicts", [])):
        errors.append("resolution_matrix must cover every conflict")
    if len(unknown_resolutions) < len(report.get("unknowns", [])):
        errors.append("resolution_matrix must cover every unknown")

    metrics = report.get("quality_metrics", {})
    if isinstance(metrics, dict):
        if metrics.get("quality_score") != report.get("quality_score"):
            errors.append("quality_metrics.quality_score must match quality_score")
        if metrics.get("structural_score") != report.get("structural_score"):
            errors.append("quality_metrics.structural_score must match structural_score")
    else:
        errors.append("quality_metrics must be an object")

    calculated_metrics, quality_errors = evaluate_report_details(report)
    if calculated_metrics.get("quality_score") != report.get("quality_score"):
        errors.append(
            f"quality_score must be recalculated; expected {calculated_metrics.get('quality_score')}, "
            f"found {report.get('quality_score')}"
        )
    if calculated_metrics.get("structural_score") != report.get("structural_score"):
        errors.append(
            f"structural_score must be recalculated; expected {calculated_metrics.get('structural_score')}, "
            f"found {report.get('structural_score')}"
        )
    for key in (
        "critical_claim_coverage",
        "source_quality",
        "traceability",
        "limitations_and_resolutions",
        "freshness_and_reproducibility",
        "notes",
    ):
        if isinstance(metrics, dict) and metrics.get(key) != calculated_metrics.get(key):
            errors.append(f"quality_metrics.{key} must be recalculated")
    for error in quality_errors:
        errors.append(f"quality gate: {error}")

    return errors


def validate_report_set(reports_dir: Path, report_set_id: str) -> list[str]:
    errors: list[str] = []
    json_path = reports_dir / f"{report_set_id}.json"
    if not json_path.exists():
        return [f"missing report set JSON: {json_path}"]
    report = load_json(json_path)
    errors.extend(validate(report))
    errors.extend(validate_bilingual_files(json_path, report))
    errors.extend(validate_github_summary_gate(json_path, report))
    required = {"zh-TW", "en"}
    languages = set(report.get("languages", []))
    missing = sorted(required - languages)
    if missing:
        errors.append(f"report set must include languages: {', '.join(missing)}")
    claim_ids = [claim.get("claim_id") for claim in report.get("claims", []) if isinstance(claim, dict)]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("report set claim IDs must be stable and unique")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a trusted research report.")
    parser.add_argument("report", nargs="?", help="Path to one report JSON file.")
    parser.add_argument("--report-set", nargs=2, metavar=("REPORTS_DIR", "REPORT_SET_ID"))
    args = parser.parse_args()

    if args.report_set:
        reports_dir = Path(args.report_set[0])
        report_set_id = args.report_set[1]
        try:
            errors = validate_report_set(reports_dir, report_set_id)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read report set: {exc}")
            return 2
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Report set consistency checks passed.")
        return 0

    if not args.report:
        print("Usage: python scripts/validate_report.py <report.json>")
        print("   or: python scripts/validate_report.py --report-set <reports_dir> <report_set_id>")
        return 2

    path = Path(args.report)
    try:
        report = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read report: {exc}")
        return 2

    errors = validate(report)
    errors.extend(validate_bilingual_files(path, report))
    errors.extend(validate_github_summary_gate(path, report))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Report consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
