from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlsplit


CURRENT_OID_RE = re.compile(r'"currentOid":"([0-9a-f]{40})"')
DEFAULT_BRANCH_RE = re.compile(r'"defaultBranch":"([^"]+)"')


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _iso_after(value: str, days: int) -> str:
    return (_parse_timestamp(value) + timedelta(days=days)).isoformat(timespec="seconds")


def freshness_for(source_type: str, retrieved_at: str) -> dict[str, Any]:
    if source_type in {"law_or_regulation", "dataset", "research_paper"}:
        return {
            "mode": "stable",
            "recheck_after": None,
            "reason": "Captured publication is treated as stable; refresh only when a newer version is relevant.",
        }
    if source_type in {"news", "issue_or_discussion", "pull_request", "release_note"}:
        return {
            "mode": "volatile",
            "recheck_after": _iso_after(retrieved_at, 7),
            "reason": "Volatile source; refresh before relying on it for current-state claims.",
        }
    return {
        "mode": "periodic",
        "recheck_after": _iso_after(retrieved_at, 30),
        "reason": "Living documentation or repository page; refresh before relying on current-state claims.",
    }


def _github_permalink(url: str, content: bytes) -> tuple[str | None, str | None, str | None]:
    parts = urlsplit(url)
    if parts.netloc.lower() != "github.com":
        return None, None, None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) < 2:
        return None, None, None

    text = content.decode("utf-8", errors="ignore")
    match = CURRENT_OID_RE.search(text)
    if not match:
        return None, None, None
    commit_sha = match.group(1)
    owner, repo = segments[:2]

    if len(segments) >= 5 and segments[2] == "blob":
        file_path = "/".join(segments[4:])
        immutable_url = f"https://github.com/{owner}/{repo}/blob/{commit_sha}/{file_path}"
        return commit_sha, immutable_url, file_path

    if len(segments) >= 4 and segments[2] == "tree":
        tree_path = "/".join(segments[4:])
        suffix = f"/{tree_path}" if tree_path else ""
        immutable_url = f"https://github.com/{owner}/{repo}/tree/{commit_sha}{suffix}"
        return commit_sha, immutable_url, tree_path or "repository tree"

    immutable_url = f"https://github.com/{owner}/{repo}/tree/{commit_sha}"
    return commit_sha, immutable_url, "repository tree"


def _github_repository_metadata(url: str, content: bytes) -> dict[str, Any] | None:
    parts = urlsplit(url)
    if parts.netloc.lower() != "github.com":
        return None
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) < 2:
        return None
    owner, repo = segments[:2]
    text = content.decode("utf-8", errors="ignore")
    commit_match = CURRENT_OID_RE.search(text)
    branch_match = DEFAULT_BRANCH_RE.search(text)
    metadata: dict[str, Any] = {
        "owner": owner,
        "name": repo,
        "capture_scope": "readme_only",
        "selection_reason": "Initial GitHub repository capture; deep-read curation must select README, docs/config, source, examples, and tests before using this source for implementation claims.",
    }
    if branch_match:
        metadata["default_branch"] = branch_match.group(1)
    if commit_match:
        commit_sha = commit_match.group(1)
        metadata["commit_sha"] = commit_sha
        metadata["tree_url"] = f"https://github.com/{owner}/{repo}/tree/{commit_sha}"
    return metadata


def apply_source_metadata(source: dict[str, Any], content: bytes) -> dict[str, Any]:
    snapshots = source.get("local_snapshots", [])
    if not snapshots:
        return source
    latest = snapshots[-1]
    source["content_hash"] = latest.get("content_hash", "")
    source["locator"] = source.get("locator") or f"local snapshot {latest.get('snapshot_id', '')}"
    source["freshness"] = freshness_for(source["source_type"], source["retrieved_at"])

    commit_sha, immutable_url, locator = _github_permalink(source["url"], content)
    if commit_sha and immutable_url:
        source["commit_sha"] = commit_sha
        source["immutable_url"] = immutable_url
        source["locator"] = locator or source["locator"]
    repository = _github_repository_metadata(source["url"], content)
    if repository:
        if source.get("commit_sha") and "commit_sha" not in repository:
            repository["commit_sha"] = source["commit_sha"]
        if source.get("immutable_url") and "tree_url" not in repository:
            repository["tree_url"] = source["immutable_url"]
        source["repository"] = repository
    return source
