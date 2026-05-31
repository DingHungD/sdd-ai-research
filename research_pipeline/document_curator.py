from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from .io_utils import iso_now, write_json


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def text_from_snapshot(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "PDF snapshot saved locally. Semantic curation requires a PDF extraction step or agent review."
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".html":
        text = TAG_RE.sub(" ", text)
        text = html.unescape(text)
    return SPACE_RE.sub(" ", text).strip()


def curate(source: dict[str, Any], topic_dir: Path) -> dict[str, Any]:
    snapshot = source["local_snapshots"][-1]
    snapshot_path = topic_dir / snapshot["local_path"]
    text = text_from_snapshot(snapshot_path)
    excerpt = text[:1200] if text else "No readable text extracted."
    summary = {
        "source_id": source["source_id"],
        "snapshot_id": snapshot["snapshot_id"],
        "summarized_at": iso_now(),
        "document_purpose": f"Initial machine summary for {source['source_type']}. Agent review required.",
        "summary": excerpt,
        "categories": [],
        "key_points": [],
        "keywords": [],
        "entities": [],
        "limitations": ["This is an initial machine-generated extraction and must be reviewed by an agent."],
        "potential_questions": [],
    }
    source_dir = topic_dir / "sources" / source["source_id"]
    write_json(source_dir / "summary.json", summary)
    (source_dir / "summary.md").write_text(
        f"# {source['title']}\n\n{excerpt}\n\n## Limitations\n\n"
        "- This is an initial machine-generated extraction and must be reviewed by an agent.\n",
        encoding="utf-8",
    )
    return summary


def save_reviewed_summary(topic_dir: Path, summary: dict[str, Any]) -> dict[str, Any]:
    source_dir = topic_dir / "sources" / summary["source_id"]
    source = __import__("json").loads((source_dir / "source.json").read_text(encoding="utf-8"))
    write_json(source_dir / "summary.json", summary)
    lines = [
        f"# {summary['source_id']}",
        "",
        f"- 來源：[{source['title']}]({source['url']})",
        f"- 類型：`{source['source_type']}`",
        f"- Snapshot：`{summary['snapshot_id']}`",
        "",
        "## Introduction",
        "",
        summary["summary"],
        "",
        "## Ecosystem Role",
        "",
        summary.get("role_in_ecosystem", ""),
        "",
        "## Architecture Fit",
        "",
        summary.get("architecture_fit", ""),
        "",
        "## Typical Workflow",
        "",
    ]
    lines.extend(f"{index}. {item}" for index, item in enumerate(summary.get("workflow_outline", []), start=1))
    lines.extend([
        "",
        "## Key Features",
        "",
    ])
    lines.extend(f"- {item}" for item in summary.get("key_features", []))
    lines.extend(["", "## Key Technologies", ""])
    lines.extend(f"- {item}" for item in summary.get("key_technologies", []))
    lines.extend(["", "## Best For", ""])
    lines.extend(f"- {item}" for item in summary.get("best_for", []))
    lines.extend([
        "",
        "## Research Value",
        "",
        summary.get("research_value", ""),
        "",
        "## Verification Questions",
        "",
    ])
    lines.extend(f"- {item}" for item in summary.get("verification_questions", []))
    lines.extend([
        "",
        "## Key Points",
        "",
    ])
    for point in summary["key_points"]:
        lines.append(f"- {point['text']} (`{point['locator']}`)")
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in summary["limitations"])
    (source_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary
