#!/usr/bin/env python3
"""Backfill reproducibility metadata for locally stored source snapshots."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from research_pipeline.io_utils import read_json, write_json
from research_pipeline.source_evaluator import evaluate
from research_pipeline.source_metadata import apply_source_metadata


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/backfill_source_metadata.py <topic_id>")
        return 2

    topic_dir = ROOT / "knowledge-base" / "topics" / sys.argv[1]
    index_path = topic_dir / "index.json"
    index = read_json(index_path)
    indexed = {item["source_id"]: item for item in index.get("sources", [])}
    updated = 0
    immutable = 0

    for source_path in sorted((topic_dir / "sources").glob("S-*/source.json")):
        source = read_json(source_path)
        latest = source.get("local_snapshots", [])[-1]
        content = (topic_dir / latest["local_path"]).read_bytes()
        apply_source_metadata(source, content)
        tier, quality = evaluate(source["url"], source["source_type"], source.get("immutable_url", ""))
        source["evidence_tier"] = tier
        source["quality"] = quality
        write_json(source_path, source)
        if source["source_id"] in indexed:
            indexed[source["source_id"]]["recheck_after"] = source.get("freshness", {}).get("recheck_after")
        immutable += bool(source.get("immutable_url"))
        updated += 1

    write_json(index_path, index)
    print(f"Updated {updated} source records; immutable permalinks: {immutable}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
