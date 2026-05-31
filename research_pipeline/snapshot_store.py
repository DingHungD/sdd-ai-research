from __future__ import annotations

from pathlib import Path

from .io_utils import sha256_bytes, snapshot_id


EXTENSIONS = {
    "application/json": ".json",
    "application/pdf": ".pdf",
    "text/html": ".html",
    "text/markdown": ".md",
    "text/plain": ".txt",
}


def save_snapshot(topic_dir: Path, source_id: str, content: bytes, content_type: str) -> dict[str, str]:
    identifier = snapshot_id()
    extension = EXTENSIONS.get(content_type, ".bin")
    relative_path = Path("sources") / source_id / "raw" / f"{identifier}{extension}"
    absolute_path = topic_dir / relative_path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    absolute_path.write_bytes(content)
    return {
        "snapshot_id": identifier,
        "local_path": relative_path.as_posix(),
        "content_hash": sha256_bytes(content),
        "mime_type": content_type,
    }

