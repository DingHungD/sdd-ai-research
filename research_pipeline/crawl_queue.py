from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import iso_now, next_prefixed_id, read_json, write_json


def load_queue(topic_dir: Path) -> dict[str, Any]:
    return read_json(topic_dir / "crawl-queue.json")


def save_queue(topic_dir: Path, queue: dict[str, Any]) -> None:
    queue["updated_at"] = iso_now()
    write_json(topic_dir / "crawl-queue.json", queue)
    write_markdown(topic_dir, queue)


def append_item(
    topic_dir: Path,
    *,
    target_type: str,
    target: str,
    reason: str,
    related_question_ids: list[str],
    added_by_step: str,
    discovered_from: str | None = None,
) -> dict[str, Any]:
    queue = load_queue(topic_dir)
    queue_id = next_prefixed_id([item["queue_id"] for item in queue["items"]], "Q")
    item = {
        "queue_id": queue_id,
        "sequence": len(queue["items"]) + 1,
        "target_type": target_type,
        "target": target,
        "reason": reason,
        "related_question_ids": related_question_ids,
        "added_by_step": added_by_step,
        "status": "pending",
        "priority_override": False,
        "discovered_from": discovered_from,
        "result_source_ids": [],
        "notes": "",
    }
    queue["items"].append(item)
    save_queue(topic_dir, queue)
    return item


def update_item(topic_dir: Path, queue_id: str, **changes: Any) -> dict[str, Any]:
    queue = load_queue(topic_dir)
    for item in queue["items"]:
        if item["queue_id"] == queue_id:
            item.update(changes)
            save_queue(topic_dir, queue)
            return item
    raise ValueError(f"unknown queue item: {queue_id}")


def next_pending(topic_dir: Path) -> dict[str, Any] | None:
    queue = load_queue(topic_dir)
    pending = [item for item in queue["items"] if item["status"] == "pending"]
    if not pending:
        return None
    overrides = [item for item in pending if item.get("priority_override")]
    return min(overrides or pending, key=lambda item: item["sequence"])


def write_markdown(topic_dir: Path, queue: dict[str, Any]) -> None:
    lines = [
        f"# {queue['topic_id']}：候選來源爬取佇列",
        "",
        "agent 依序處理。後續新增來源追加至表格尾端，不重編既有項目。",
        "",
        "| 順序 | Queue ID | 類型 | 目標 | 對應問題 | 新增步驟 | 狀態 | 原因 |",
        "| ---: | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in queue["items"]:
        questions = ", ".join(f"`{value}`" for value in item["related_question_ids"])
        target = item["target"].replace("|", "\\|")
        reason = item["reason"].replace("|", "\\|")
        lines.append(
            f"| {item['sequence']} | `{item['queue_id']}` | `{item['target_type']}` | "
            f"`{target}` | {questions} | `{item['added_by_step']}` | `{item['status']}` | {reason} |"
        )
    (topic_dir / "crawl-queue.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

