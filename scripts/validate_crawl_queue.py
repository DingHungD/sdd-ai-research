#!/usr/bin/env python3
"""Run dependency-free consistency checks for a source crawl queue."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(queue: dict) -> list[str]:
    errors: list[str] = []
    items = queue.get("items", [])
    if not isinstance(items, list):
        return ["items must be an array"]

    queue_ids = [item.get("queue_id") for item in items if isinstance(item, dict)]
    sequences = [item.get("sequence") for item in items if isinstance(item, dict)]
    queue_id_set = {queue_id for queue_id in queue_ids if queue_id}

    if len(queue_ids) != len(queue_id_set):
        errors.append("queue_id values must be unique and non-empty")
    if len(sequences) != len(set(sequences)):
        errors.append("sequence values must be unique")
    if sequences != sorted(sequences):
        errors.append("items must be ordered by ascending sequence")
    if sequences and sequences != list(range(1, len(sequences) + 1)):
        errors.append("sequence values must be contiguous and start at 1")

    seen_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("each queue item must be an object")
            continue
        queue_id = item.get("queue_id", "<unknown>")
        discovered_from = item.get("discovered_from")
        if discovered_from and discovered_from not in seen_ids:
            errors.append(f"{queue_id}: discovered_from must reference an earlier queue item")
        seen_ids.add(queue_id)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_crawl_queue.py <crawl-queue.json>")
        return 2

    path = Path(sys.argv[1])
    try:
        queue = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read crawl queue: {exc}")
        return 2

    errors = validate(queue)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Crawl queue consistency checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

