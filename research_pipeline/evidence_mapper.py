from __future__ import annotations

from typing import Any


def assign_claim_ids(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"claim_id": f"C-{index:03d}", **claim} for index, claim in enumerate(claims, start=1)]

