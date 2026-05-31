from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import iso_now, read_json, write_json


def sync_supported_claim_ids(topic_dir: Path, report: dict[str, Any]) -> None:
    backlinks: dict[str, set[str]] = {source["source_id"]: set() for source in report.get("sources", [])}
    for claim in report.get("claims", []):
        for source_id in claim.get("supporting_source_ids", []):
            backlinks.setdefault(source_id, set()).add(claim["claim_id"])

    for source in report.get("sources", []):
        source_id = source["source_id"]
        source["supported_claim_ids"] = sorted(backlinks.get(source_id, set()))
        local_path = topic_dir / "sources" / source_id / "source.json"
        if local_path.exists():
            local_source = read_json(local_path)
            local_source["supported_claim_ids"] = source["supported_claim_ids"]
            write_json(local_path, local_source)


def _append_scope(lines: list[str], report: dict[str, Any]) -> None:
    lines.extend(["", "## 研究問題", ""])
    lines.extend(f"- {item}" for item in report.get("questions", []))
    scope = report.get("scope", {})
    lines.extend(["", "## 研究範圍", ""])
    if scope.get("audience"):
        lines.append(f"- 目標受眾：{scope['audience']}")
    if scope.get("regions"):
        lines.append(f"- 地區：{', '.join(scope['regions'])}")
    if scope.get("languages"):
        lines.append(f"- 語言：{', '.join(scope['languages'])}")
    if scope.get("date_range"):
        lines.append(f"- 時間範圍：{scope['date_range']}")
    lines.extend(["", "### 包含範圍", ""])
    lines.extend(f"- {item}" for item in scope.get("include", []))
    lines.extend(["", "### 排除範圍", ""])
    lines.extend(f"- {item}" for item in scope.get("exclude", []))


def _append_quality_metrics(lines: list[str], report: dict[str, Any]) -> None:
    metrics = report.get("quality_metrics", {})
    if not metrics:
        return
    lines.extend(["", "## 品質指標", ""])
    for label, key in [
        ("關鍵主張覆蓋率", "critical_claim_coverage"),
        ("高品質證據分數", "source_quality"),
        ("雙向可追溯性分數", "traceability"),
        ("衝突與未知處理分數", "limitations_and_resolutions"),
        ("新鮮度與可重現性分數", "freshness_and_reproducibility"),
    ]:
        if key in metrics:
            lines.append(f"- {label}：`{metrics[key]}`")
    if metrics.get("notes"):
        lines.append(f"- 說明：{metrics['notes']}")


def _append_recommendation_sections(lines: list[str], report: dict[str, Any]) -> None:
    sections = report.get("recommendation_sections", {})
    implementability = sections.get("implementability", {})
    open_source_options = sections.get("open_source_options", {})
    future_directions = sections.get("future_directions", {})

    if implementability:
        lines.extend(["### 1. 可實作性", "", implementability.get("summary", ""), ""])
        for item in implementability.get("items", []):
            lines.extend(
                [
                    f"#### {item['title']}",
                    "",
                    f"- 目的：{item.get('objective', '')}",
                    f"- 技術組合：{', '.join(item.get('technologies', []))}",
                    f"- 實作流程：{item.get('workflow', '')}",
                    f"- 最小交付物：{item.get('minimum_deliverable', '')}",
                    f"- 驗收標準：{item.get('acceptance_criteria', '')}",
                    f"- 依據來源：{', '.join(item.get('supporting_source_ids', []))}",
                    f"- 後續研究提示詞：`{item.get('research_prompt', '')}`",
                    "",
                ]
            )

    if open_source_options:
        lines.extend(["### 2. 開源工具選型", "", open_source_options.get("summary", ""), ""])
        single_tools = open_source_options.get("single_tool_recommendations", {})
        if single_tools:
            lines.extend(["#### 2.1 只使用一個開源工具：前三種推薦", "", single_tools.get("summary", ""), ""])
            for item in single_tools.get("items", []):
                lines.extend(
                    [
                        f"##### 第 {item['rank']} 名：{item['tool']}",
                        "",
                        f"- 推薦理由：{item.get('recommendation_reason', '')}",
                        f"- 適用情境：{item.get('suitable_for', '')}",
                        f"- 主要能力：{', '.join(item.get('strengths', []))}",
                        f"- 必須接受的缺口：{item.get('gaps', '')}",
                        f"- 最小導入方式：{item.get('minimum_adoption', '')}",
                        f"- 依據來源：{', '.join(item.get('supporting_source_ids', []))}",
                        f"- 後續研究提示詞：`{item.get('research_prompt', '')}`",
                        "",
                    ]
                )

        multi_tool_stacks = open_source_options.get("multi_tool_recommendations", {})
        if multi_tool_stacks:
            lines.extend(["#### 2.2 多個開源工具配合：前三種推薦", "", multi_tool_stacks.get("summary", ""), ""])
            for item in multi_tool_stacks.get("items", []):
                lines.extend(
                    [
                        f"##### 第 {item['rank']} 名：{item['title']}",
                        "",
                        f"- 工具組合：{', '.join(item.get('tools', []))}",
                        f"- 目標：{item.get('objective', '')}",
                        f"- 角色分工：{item.get('roles', '')}",
                        f"- 實作流程：{item.get('workflow', '')}",
                        f"- 推薦理由：{item.get('recommendation_reason', '')}",
                        f"- 取捨：{item.get('tradeoffs', '')}",
                        f"- 最小交付物：{item.get('minimum_deliverable', '')}",
                        f"- 驗收標準：{item.get('acceptance_criteria', '')}",
                        f"- 依據來源：{', '.join(item.get('supporting_source_ids', []))}",
                        f"- 後續研究提示詞：`{item.get('research_prompt', '')}`",
                        "",
                    ]
                )

    if future_directions:
        lines.extend(["### 3. 未來性", "", future_directions.get("summary", ""), ""])
        for item in future_directions.get("items", []):
            lines.extend(
                [
                    f"#### {item['title']}",
                    "",
                    f"- 當前缺點：{item.get('current_limitation', '')}",
                    f"- 演進方向：{item.get('direction', '')}",
                    f"- 啟動條件：{item.get('trigger', '')}",
                    f"- 依據來源：{', '.join(item.get('supporting_source_ids', []))}",
                    f"- 後續研究提示詞：`{item.get('research_prompt', '')}`",
                    "",
                ]
            )


def _append_resolution_matrix(lines: list[str], report: dict[str, Any]) -> None:
    matrix = report.get("resolution_matrix", {})
    sections = [
        ("衝突解決矩陣", matrix.get("conflict_resolutions", [])),
        ("未知事項解決矩陣", matrix.get("unknown_resolutions", [])),
    ]
    if not any(items for _, items in sections):
        return

    lines.extend(["", "### 解決矩陣", "", matrix.get("summary", ""), ""])
    for title, items in sections:
        if not items:
            continue
        lines.extend([f"#### {title}", ""])
        for item in items:
            lines.extend(
                [
                    f"##### `{item['resolution_id']}` {item['title']}",
                    "",
                    f"- 狀態：`{item['status']}`",
                    f"- 判斷：{item.get('decision', '')}",
                    f"- 解決方式：{item.get('resolution_method', '')}",
                    f"- 依據來源：{', '.join(item.get('supporting_source_ids', []))}",
                    f"- 下一步：{item.get('next_action', '')}",
                    f"- 關閉條件：{item.get('closure_criteria', '')}",
                    "",
                ]
            )


def _append_source_navigation(lines: list[str], report: dict[str, Any]) -> None:
    sources = report.get("sources", [])
    high_quality = sum(source.get("evidence_tier") in {"A", "B"} for source in sources)
    immutable = sum(bool(source.get("immutable_url")) for source in sources)
    lines.extend(
        [
            "",
            "## 來源",
            "",
            f"- 本報告引用 `{len(sources)}` 筆來源，其中 `{high_quality}` 筆為 A/B 層級，`{immutable}` 筆保存固定版本連結。",
            "- [來源總目錄與各文件大綱](../sources/CATALOG.md)",
            f"- [完整機器可讀來源 metadata]({report['report_id']}.json)",
            "- 個別來源的摘要與 metadata 請由來源總目錄進入；原始 snapshot 預設只保存在本機。",
        ]
    )


def write_report(topic_dir: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    reports_dir = topic_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report.setdefault("generated_at", iso_now())
    sync_supported_claim_ids(topic_dir, report)
    json_path = reports_dir / f"{report['report_id']}.json"
    md_path = reports_dir / f"{report['report_id']}.md"
    write_json(json_path, report)
    md_path.write_text(to_markdown(report), encoding="utf-8")
    return json_path, md_path


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['title']}",
        "",
        "## 報告資訊",
        "",
        f"- 報告 ID：`{report['report_id']}`",
        f"- 版本：`{report['version']}`",
        f"- 產生時間：`{report['generated_at']}`",
        f"- 資料截止時間：`{report['data_cutoff']}`",
        f"- 整體可信度：`{report['overall_confidence']}`",
        f"- 品質分數：`{report.get('quality_score', 'N/A')}/100`",
        f"- 結構完整度：`{report.get('structural_score', 'N/A')}/100`",
        "",
        "## 摘要",
        "",
        report["executive_summary"],
    ]
    _append_quality_metrics(lines, report)
    _append_scope(lines, report)
    lines.extend(["", "## 方法", "", report.get("methodology", ""), "", "## 關鍵發現", ""])
    for claim in report["claims"]:
        lines.extend(
            [
                f"### `{claim['claim_id']}`",
                "",
                f"- 主張：{claim['text']}",
                f"- 類型：`{claim['type']}`",
                f"- 重要程度：`{claim['importance']}`",
                f"- 可信度：`{claim['confidence']}`",
                f"- 理由：{claim['confidence_reason']}",
                f"- 支持來源：{', '.join(claim['supporting_source_ids'])}",
                f"- 反對或限制來源：{', '.join(claim.get('opposing_source_ids', [])) or '無'}",
                f"- 備註：{claim.get('notes', '') or '無'}",
                "",
            ]
        )
    lines.extend(["## 限制", ""])
    lines.extend(f"- {item}" for item in report["limitations"])
    lines.extend(["", "## 衝突與未知", ""])
    matrix = report.get("resolution_matrix", {})
    unresolved = [
        item
        for item in matrix.get("unknown_resolutions", [])
        if item.get("status") in {"open", "partially_resolved"}
    ]
    if matrix:
        lines.append(f"- 已解決衝突：`{sum(item.get('status') == 'resolved' for item in matrix.get('conflict_resolutions', []))}`")
        lines.append(f"- 未關閉未知：`{len(unresolved)}`")
        lines.extend(f"- `{item['resolution_id']}` `{item['status']}`：{item['title']}" for item in unresolved)
    else:
        lines.extend(f"- 衝突：{item}" for item in report.get("conflicts", []))
        lines.extend(f"- 未知：{item}" for item in report.get("unknowns", []))
    _append_resolution_matrix(lines, report)
    lines.extend(["", "## 結論", "", report.get("conclusion", "")])
    lines.extend(["", "## 建議", ""])
    _append_recommendation_sections(lines, report)
    if report.get("recommendation_sections") and report.get("recommendations"):
        lines.extend(["### 其他建議", ""])
    lines.extend(f"- {item}" for item in report.get("recommendations", []))
    _append_source_navigation(lines, report)
    lines.append("")
    lines.extend(["## 變更紀錄", ""])
    lines.extend(f"- {item}" for item in report.get("changelog", []))
    return "\n".join(lines) + "\n"
