from __future__ import annotations

from pathlib import Path
from typing import Any

from .crawl_queue import update_item
from .document_curator import curate
from .io_utils import iso_now, next_prefixed_id, read_json, write_json
from .snapshot_store import save_snapshot
from .source_evaluator import evaluate
from .source_metadata import apply_source_metadata
from .source_normalizer import normalize_url


def topic_dir(root: Path, topic_id: str) -> Path:
    return root / "knowledge-base" / "topics" / topic_id


def register_snapshot(
    root: Path,
    *,
    topic_id: str,
    queue_id: str,
    title: str,
    url: str,
    content: bytes,
    content_type: str,
    source_type: str,
    author_or_organization: str = "",
    publisher: str = "",
) -> dict[str, Any]:
    directory = topic_dir(root, topic_id)
    sources_dir = directory / "sources"
    existing = [path.name for path in sources_dir.glob("S-*") if path.is_dir()]
    source_id = next_prefixed_id(existing, "S")
    canonical_url = normalize_url(url)
    snapshot = save_snapshot(directory, source_id, content, content_type)
    captured_at = iso_now()
    snapshot["captured_at"] = captured_at
    source = {
        "source_id": source_id,
        "title": title,
        "url": canonical_url,
        "canonical_url": canonical_url,
        "author_or_organization": author_or_organization,
        "publisher": publisher,
        "retrieved_at": captured_at,
        "local_snapshots": [snapshot],
        "source_type": source_type,
        "conflict_of_interest": "",
        "evidence_chain": canonical_url,
        "supported_claim_ids": [],
    }
    apply_source_metadata(source, content)
    tier, quality = evaluate(canonical_url, source_type, source.get("immutable_url", ""))
    source["evidence_tier"] = tier
    source["quality"] = quality
    source_dir = sources_dir / source_id
    write_json(source_dir / "source.json", source)
    summary = curate(source, directory)
    update_index(directory, source, summary)
    update_item(directory, queue_id, status="completed", result_source_ids=[source_id])
    return source


def update_index(directory: Path, source: dict[str, Any], summary: dict[str, Any]) -> None:
    path = directory / "index.json"
    index = read_json(path)
    index["sources"] = [item for item in index.get("sources", []) if item["source_id"] != source["source_id"]]
    index["sources"].append(
        {
            "source_id": source["source_id"],
            "source_path": f"sources/{source['source_id']}/source.json",
            "summary_path": f"sources/{source['source_id']}/summary.json",
            "title": source["title"],
            "categories": summary.get("categories", []),
            "keywords": summary.get("keywords", []),
            "recheck_after": source.get("freshness", {}).get("recheck_after"),
        }
    )
    index["updated_at"] = iso_now()
    write_json(path, index)
