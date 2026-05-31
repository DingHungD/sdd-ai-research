from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


TIER_WEIGHT = {"A": 1.0, "B": 0.8, "C": 0.5, "D": 0.1}
PRIMARY_SOURCE_TYPES = {
    "official",
    "official_documentation",
    "repository_file",
    "release_note",
    "law_or_regulation",
    "dataset",
    "research_paper",
    "institutional_report",
}


def _iter_source_linked_items(value: Any):
    if isinstance(value, dict):
        if "supporting_source_ids" in value:
            yield value
        for nested in value.values():
            yield from _iter_source_linked_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _iter_source_linked_items(nested)


def _is_fresh_or_stable(source: dict[str, Any]) -> bool:
    freshness = source.get("freshness", {})
    if freshness.get("mode") == "stable":
        return True
    recheck_after = freshness.get("recheck_after")
    if not recheck_after:
        return False
    try:
        parsed = datetime.fromisoformat(recheck_after.replace("Z", "+00:00"))
        return parsed >= datetime.now(timezone.utc)
    except (AttributeError, ValueError):
        return False


def _structural_score(report: dict[str, Any], errors: list[str]) -> int:
    required = {
        "report_id",
        "version",
        "title",
        "generated_at",
        "data_cutoff",
        "overall_confidence",
        "executive_summary",
        "questions",
        "scope",
        "claims",
        "sources",
        "conflicts",
        "unknowns",
        "limitations",
        "conclusion",
        "changelog",
    }
    score = 70 if required <= report.keys() else 40
    score += 10 if report.get("methodology") else 0
    score += 10 if report.get("resolution_matrix") else 0
    score += 10 if report.get("recommendation_sections") else 0
    return max(0, min(100, score - min(30, 5 * len(errors))))


def evaluate_report_details(report: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    source_map = {
        source["source_id"]: source
        for source in report.get("sources", [])
        if isinstance(source, dict) and source.get("source_id")
    }
    sources = set(source_map)
    claims = [claim for claim in report.get("claims", []) if isinstance(claim, dict)]
    critical = [claim for claim in claims if claim.get("importance") == "critical"]
    covered = [claim for claim in critical if claim.get("supporting_source_ids")]

    for claim in claims:
        unknown = sorted(set(claim.get("supporting_source_ids", [])) - sources)
        if unknown:
            errors.append(f"{claim['claim_id']}: unknown source ids: {', '.join(unknown)}")
        opposing_unknown = sorted(set(claim.get("opposing_source_ids", [])) - sources)
        if opposing_unknown:
            errors.append(f"{claim['claim_id']}: unknown opposing source ids: {', '.join(opposing_unknown)}")
    for item in _iter_source_linked_items(report.get("recommendation_sections", {})):
        unknown = sorted(set(item.get("supporting_source_ids", [])) - sources)
        if unknown:
            title = item.get("title", item.get("tool", "<unknown>"))
            errors.append(f"recommendation/{title}: unknown source ids: {', '.join(unknown)}")
    for item in _iter_source_linked_items(report.get("resolution_matrix", {})):
        unknown = sorted(set(item.get("supporting_source_ids", [])) - sources)
        if unknown:
            errors.append(f"resolution/{item.get('resolution_id', '<unknown>')}: unknown source ids: {', '.join(unknown)}")

    if len(covered) != len(critical):
        errors.append("not all critical claims have supporting sources")

    minimum_sources = report.get("minimum_sources", 0)
    if minimum_sources and len(sources) < minimum_sources:
        errors.append(f"report requires at least {minimum_sources} sources, found {len(sources)}")
    primary_sources = [source for source in source_map.values() if source.get("source_type") in PRIMARY_SOURCE_TYPES]
    minimum_primary_sources = report.get("minimum_primary_sources", 0)
    if minimum_primary_sources and len(primary_sources) < minimum_primary_sources:
        errors.append(f"report requires at least {minimum_primary_sources} primary sources, found {len(primary_sources)}")
    high_quality_sources = [source for source in source_map.values() if source.get("evidence_tier") in {"A", "B"}]
    minimum_high_quality_sources = report.get("minimum_high_quality_sources", 0)
    if minimum_high_quality_sources and len(high_quality_sources) < minimum_high_quality_sources:
        errors.append(
            f"report requires at least {minimum_high_quality_sources} high-quality sources, found {len(high_quality_sources)}"
        )

    expected_backlinks: dict[str, set[str]] = {source_id: set() for source_id in sources}
    for claim in claims:
        for source_id in claim.get("supporting_source_ids", []):
            expected_backlinks.setdefault(source_id, set()).add(claim["claim_id"])
    backlink_matches = sum(
        set(source_map[source_id].get("supported_claim_ids", [])) == expected
        for source_id, expected in expected_backlinks.items()
        if source_id in source_map
    )

    critical_claim_coverage = 30 if not critical else round(30 * len(covered) / len(critical))
    critical_support_sources = [
        source_map[source_id]
        for claim in critical
        for source_id in claim.get("supporting_source_ids", [])
        if source_id in source_map
    ]
    source_quality = (
        round(25 * sum(TIER_WEIGHT.get(source.get("evidence_tier", "D"), 0.0) for source in critical_support_sources) / len(critical_support_sources))
        if critical_support_sources
        else 0
    )
    backlink_ratio = backlink_matches / len(source_map) if source_map else 0
    snapshot_ratio = (
        sum(bool(source.get("content_hash") or source.get("local_snapshots")) for source in source_map.values()) / len(source_map)
        if source_map
        else 0
    )
    traceability = round(12 * backlink_ratio + 8 * snapshot_ratio)

    matrix = report.get("resolution_matrix", {})
    matrix = matrix if isinstance(matrix, dict) else {}
    resolutions = matrix.get("conflict_resolutions", []) + matrix.get("unknown_resolutions", [])
    status_weight = {"resolved": 1.0, "partially_resolved": 0.6, "open": 0.25}
    resolution_ratio = (
        sum(status_weight.get(item.get("status"), 0.0) for item in resolutions) / len(resolutions) if resolutions else 0
    )
    limitations_and_resolutions = round((5 if report.get("limitations") else 0) + 10 * resolution_ratio)

    freshness_ratio = (
        sum(_is_fresh_or_stable(source) for source in source_map.values()) / len(source_map) if source_map else 0
    )
    immutable_ratio = (
        sum(bool(source.get("immutable_url") or source.get("content_hash")) for source in source_map.values()) / len(source_map)
        if source_map
        else 0
    )
    freshness_and_reproducibility = round(6 * freshness_ratio + 4 * immutable_ratio)

    quality_score = (
        critical_claim_coverage
        + source_quality
        + traceability
        + limitations_and_resolutions
        + freshness_and_reproducibility
    )
    metrics = {
        "quality_score": quality_score,
        "structural_score": _structural_score(report, errors),
        "critical_claim_coverage": f"{critical_claim_coverage}/30",
        "source_quality": f"{source_quality}/25",
        "traceability": f"{traceability}/20",
        "limitations_and_resolutions": f"{limitations_and_resolutions}/15",
        "freshness_and_reproducibility": f"{freshness_and_reproducibility}/10",
        "notes": (
            f"{len(source_map)} 筆來源；{len(primary_sources)} 筆主要來源；{len(high_quality_sources)} 筆 A/B 層級來源；"
            f"{sum(item.get('status') == 'open' for item in resolutions)} 個 open resolution items。"
        ),
    }
    return metrics, errors


def evaluate_report(report: dict[str, Any]) -> tuple[int, list[str]]:
    metrics, errors = evaluate_report_details(report)
    return metrics["quality_score"], errors
