from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import read_json
from .quality_gate import PRIMARY_SOURCE_TYPES


def build_catalog(topic_dir: Path) -> str:
    index = read_json(topic_dir / "index.json")
    rows: list[dict[str, Any]] = []
    for item in sorted(index.get("sources", []), key=lambda value: value["source_id"]):
        source = read_json(topic_dir / item["source_path"])
        summary = read_json(topic_dir / item["summary_path"])
        rows.append(
            {
                "source_id": source["source_id"],
                "title": source["title"],
                "role": summary.get("role_in_ecosystem") or ", ".join(summary.get("categories", [])),
                "outline": summary["summary"],
                "summary_path": item["summary_path"],
                "url": source["url"],
                "source_type": source["source_type"],
                "evidence_tier": source["evidence_tier"],
                "immutable_url": source.get("immutable_url", ""),
            }
        )
    primary_count = sum(row["source_type"] in PRIMARY_SOURCE_TYPES for row in rows)
    high_quality_count = sum(row["evidence_tier"] in {"A", "B"} for row in rows)
    immutable_count = sum(bool(row["immutable_url"]) for row in rows)
    lines = [
        "# SDD AI 自動開發來源總目錄",
        "",
        (
            f"目前共 `{len(rows)}` 筆來源，其中 `{primary_count}` 筆為主要來源、"
            f"`{high_quality_count}` 筆為 A/B 層級、`{immutable_count}` 筆保存固定版本連結。"
            "此目錄提供 `S-001` 到最新來源的導航與大綱。"
        ),
        "",
        "## 技術地圖",
        "",
        "| 層級 | 用途 | 代表來源 |",
        "| --- | --- | --- |",
        "| 規格與 traceability | 保存需求、設計、task、approval 與 drift | Spec Kit、OpenSpec、SpecDD、Kiro、cc-sdd、Specs CLI、MCP workflows |",
        "| Context 與 brownfield | 讓 agent 理解既有 repository，或反向產生 living spec | Kata、OpenLore、GSD |",
        "| Task graph 與 autonomous loop | 將工作切割、排序、重試並保存 iteration memory | Taskmaster、Flow Next、Smart Ralph、Ralph variants |",
        "| 多 agent orchestration | 專業分工、handoff、wave execution 與 quality gate | BMAD、Swarms、Metaswarm、Maestro |",
        "| Workspace 與 runtime | 隔離平行工作、管理 session、retry 與 observability | Symphony、Rover、Worktrunk、workmux、Codexia |",
        "| Governance 與 security | 將規則、安全限制與 threat model 放進驗證鏈 | Constitutional SDD、AI Governor、Threatspec |",
        "| Requirements assurance | 將需求、設計、code、test、hazard 與 defect 雙向追溯 | NASA SWE-052、SWE-059、SWE-067、R2Code、ReqToCode |",
        "| Policy as code | 將規則寫成可版本控制、可測試、可在 CI 阻擋違規的 policy | OPA、Rego、Conftest、OWASP DevGuard |",
        "| Secure SDLC assurance | 以控制框架與驗證層級管理安全需求與 evidence | NIST SSDF、NCCoE DevSecOps、OWASP ASVS、AISVS、SCVS、CISA |",
        "| 文章、案例與 benchmark | 補足採用經驗、反例、風險與可量測評估 | GitHub Blog、Thoughtworks、AWS、Tessl、InfoQ、Anthropic、ContextBench、OmniCode、SWE Atlas |",
        "",
        "## 來源清單",
        "",
        "| Source ID | 層級 | 來源 | 生態角色 | 大綱 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        outline = row["outline"].replace("|", "\\|").replace("\n", " ")
        if len(outline) > 240:
            outline = outline[:237] + "..."
        role = row["role"].replace("|", "\\|").replace("\n", " ")
        title = row["title"].replace("|", "\\|")
        lines.append(
            f"| [`{row['source_id']}`]({row['source_id']}/summary.md) | `{row['evidence_tier']}` | "
            f"[{title}]({row['url']}) | {role} | {outline} |"
        )
    lines.extend(
        [
            "",
            "## 使用方式",
            "",
            "- 先由本目錄選出相關來源。",
            "- 快速理解時閱讀各來源的 `summary.md`。",
            "- 形成重要結論前回讀 `raw/` snapshot 與原始 URL。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_catalog(topic_dir: Path) -> Path:
    path = topic_dir / "sources" / "CATALOG.md"
    path.write_text(build_catalog(topic_dir), encoding="utf-8")
    return path
