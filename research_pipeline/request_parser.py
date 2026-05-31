from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import read_json


def parse_request(path: Path) -> dict[str, Any]:
    request = read_json(path)
    for field in ("topic", "objective", "questions"):
        if not request.get(field):
            raise ValueError(f"research request is missing required field: {field}")
    request.setdefault("knowledge_base", {})
    request["knowledge_base"].setdefault("local_first", True)
    request["knowledge_base"].setdefault("allow_web_refresh", True)
    request["knowledge_base"].setdefault("refresh_expired_sources", True)
    request["knowledge_base"].setdefault("force_web_refresh", False)
    request.setdefault("output", {"language": "zh-TW", "format": ["markdown", "json"]})
    return request

