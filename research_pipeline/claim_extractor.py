from __future__ import annotations

from typing import Any


def extract_claim_drafts(summaries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    for summary in summaries:
        for point in summary.get("key_points", []):
            claims.append(
                {
                    "text": point["text"],
                    "type": "fact",
                    "importance": "supporting",
                    "confidence": "medium",
                    "confidence_reason": "Draft extracted from one curated local source; cross-source review required.",
                    "supporting_source_ids": [summary["source_id"]],
                    "opposing_source_ids": [],
                    "notes": point.get("locator", ""),
                }
            )
    return claims

