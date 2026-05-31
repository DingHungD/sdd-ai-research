from __future__ import annotations

from typing import Any


def build_question_plan(topic: dict[str, Any]) -> list[dict[str, str]]:
    plan: list[dict[str, str]] = []
    for item in topic.get("questions", []):
        if isinstance(item, str):
            plan.append({"question_id": f"RQ-{len(plan) + 1:03d}", "text": item})
        else:
            plan.append({"question_id": item["question_id"], "text": item["text"]})
    return plan

