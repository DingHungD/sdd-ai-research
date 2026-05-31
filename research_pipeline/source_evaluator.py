from __future__ import annotations

from urllib.parse import urlsplit


def evaluate(url: str, source_type: str, immutable_url: str = "") -> tuple[str, dict[str, str]]:
    host = urlsplit(url).netloc.lower()
    primary = source_type in {
        "official",
        "official_documentation",
        "release_note",
        "law_or_regulation",
        "dataset",
        "research_paper",
        "institutional_report",
    }
    repository_file = source_type == "repository_file"
    reproducibility = "high" if immutable_url or ("/commit/" in url or "/blob/" in url and "/main/" not in url) else "medium"
    tier = "A" if primary else "B" if repository_file else "C"
    quality = {
        "authority": "high" if primary else "medium",
        "directness": "high" if primary or repository_file else "medium",
        "recency": "medium",
        "transparency": "high" if primary or "github.com" in host else "medium",
        "independence": "medium",
        "reproducibility": reproducibility,
        "notes": (
            "Heuristic initial evaluation. Agent review is required before publication. "
            "Repository default-branch pages remain provisional unless an immutable permalink is stored."
        ),
    }
    return tier, quality
