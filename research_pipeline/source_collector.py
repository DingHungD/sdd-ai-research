from __future__ import annotations

from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass
class CollectedDocument:
    content: bytes
    content_type: str
    final_url: str


def fetch_url(url: str, timeout: int = 30) -> CollectedDocument:
    request = Request(url, headers={"User-Agent": "local-research-pipeline/0.1"})
    with urlopen(request, timeout=timeout) as response:
        return CollectedDocument(
            content=response.read(),
            content_type=response.headers.get_content_type(),
            final_url=response.geturl(),
        )

