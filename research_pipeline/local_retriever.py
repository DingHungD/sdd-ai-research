from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import read_json


def retrieve(topic_dir: Path, query: str) -> list[dict[str, Any]]:
    index = read_json(topic_dir / "index.json")
    terms = {term.lower() for term in query.split() if term}
    matches: list[dict[str, Any]] = []
    for source in index.get("sources", []):
        haystack = " ".join([source.get("title", ""), *source.get("keywords", []), *source.get("categories", [])]).lower()
        score = sum(1 for term in terms if term in haystack)
        if score:
            matches.append({**source, "score": score})
    return sorted(matches, key=lambda item: item["score"], reverse=True)

