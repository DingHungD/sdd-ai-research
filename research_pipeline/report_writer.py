from __future__ import annotations

from pathlib import Path
from typing import Any

from .io_utils import iso_now, read_json, write_json


LANGUAGE_LABELS = {
    "zh-TW": {
        "report_info": "報告資訊",
        "report_id": "報告 ID",
        "version": "版本",
        "generated_at": "產生時間",
        "data_cutoff": "資料截止時間",
        "overall_confidence": "整體信心",
        "quality_score": "品質分數",
        "structural_score": "結構分數",
        "summary": "執行摘要",
        "quality_metrics": "品質指標",
        "questions": "研究問題",
        "scope": "研究範圍",
        "audience": "讀者",
        "regions": "地區",
        "languages": "語言",
        "date_range": "時間範圍",
        "include": "納入範圍",
        "exclude": "排除範圍",
        "methodology": "方法論",
        "findings": "關鍵發現",
        "claim": "主張",
        "type": "類型",
        "importance": "重要性",
        "confidence": "信心",
        "reason": "理由",
        "supporting_sources": "支持來源",
        "opposing_sources": "反向或限制來源",
        "notes": "備註",
        "none": "無",
        "limitations": "限制",
        "conflicts_unknowns": "衝突與未知",
        "resolved_conflicts": "已解決衝突",
        "open_unknowns": "未解未知",
        "resolution_matrix": "解決矩陣",
        "conflict_resolutions": "衝突解決項目",
        "unknown_resolutions": "未知解決項目",
        "status": "狀態",
        "decision": "決策",
        "resolution_method": "解決方法",
        "next_action": "下一步",
        "closure_criteria": "收斂條件",
        "conclusion": "結論",
        "recommendations": "建議",
        "sources": "來源",
        "source_catalog": "來源目錄與文件大綱",
        "source_metadata": "完整機器可讀來源 metadata",
        "source_snapshot_note": "請透過來源目錄開啟個別 summary 與 metadata；raw snapshot 預設只保留本地。",
        "source_count_summary": "本報告引用 `{total}` 個來源；其中 `{high_quality}` 個為 A/B 級來源，`{immutable}` 個包含 immutable version link。",
        "changelog": "變更紀錄",
        "other_recommendations": "其他建議",
    },
    "en": {
        "report_info": "Report Information",
        "report_id": "Report ID",
        "version": "Version",
        "generated_at": "Generated At",
        "data_cutoff": "Data Cutoff",
        "overall_confidence": "Overall Confidence",
        "quality_score": "Quality Score",
        "structural_score": "Structural Score",
        "summary": "Executive Summary",
        "quality_metrics": "Quality Metrics",
        "questions": "Research Questions",
        "scope": "Scope",
        "audience": "Audience",
        "regions": "Regions",
        "languages": "Languages",
        "date_range": "Date Range",
        "include": "Included Scope",
        "exclude": "Excluded Scope",
        "methodology": "Methodology",
        "findings": "Key Findings",
        "claim": "Claim",
        "type": "Type",
        "importance": "Importance",
        "confidence": "Confidence",
        "reason": "Reason",
        "supporting_sources": "Supporting Sources",
        "opposing_sources": "Opposing or Limiting Sources",
        "notes": "Notes",
        "none": "none",
        "limitations": "Limitations",
        "conflicts_unknowns": "Conflicts and Unknowns",
        "resolved_conflicts": "Resolved Conflicts",
        "open_unknowns": "Open Unknowns",
        "resolution_matrix": "Resolution Matrix",
        "conflict_resolutions": "Conflict Resolutions",
        "unknown_resolutions": "Unknown Resolutions",
        "status": "Status",
        "decision": "Decision",
        "resolution_method": "Resolution Method",
        "next_action": "Next Action",
        "closure_criteria": "Closure Criteria",
        "conclusion": "Conclusion",
        "recommendations": "Recommendations",
        "sources": "Sources",
        "source_catalog": "Source catalog and document outlines",
        "source_metadata": "Complete machine-readable source metadata",
        "source_snapshot_note": "Use the source catalog to open individual summaries and metadata. Raw snapshots are local by default.",
        "source_count_summary": "This report cites `{total}` sources; `{high_quality}` are A/B-tier sources and `{immutable}` include immutable version links.",
        "changelog": "Changelog",
        "other_recommendations": "Other Recommendations",
    },
}


def _labels(language: str | None) -> dict[str, str]:
    return LANGUAGE_LABELS.get(language or "zh-TW", LANGUAGE_LABELS["zh-TW"])


def _localized(report: dict[str, Any], language: str | None, key: str, fallback: Any = "") -> Any:
    if language:
        localized = report.get("localized_content", {}).get(language, {})
        if key in localized:
            return localized[key]
    return report.get(key, fallback)


def _localized_claim_value(report: dict[str, Any], language: str | None, claim: dict[str, Any], key: str) -> str:
    claim_id = claim.get("claim_id", "")
    localized = report.get("localized_content", {}).get(language or "", {})
    if key == "text":
        return localized.get("claim_text", {}).get(claim_id) or claim.get("text") or claim.get("statement") or ""
    if key == "reason":
        return localized.get("claim_reasoning", {}).get(claim_id) or claim.get("confidence_reason") or claim.get("reasoning") or ""
    return ""


def _append_text_or_list(lines: list[str], value: Any) -> None:
    if isinstance(value, list):
        lines.extend(f"- {item}" for item in value)
    elif value:
        lines.append(str(value))


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


def _append_quality_metrics(lines: list[str], report: dict[str, Any], language: str | None = None) -> None:
    metrics = report.get("quality_metrics", {})
    if not metrics:
        return
    labels = _labels(language)
    metric_labels = {
        "zh-TW": {
            "critical_claim_coverage": "critical claim coverage",
            "source_quality": "source quality",
            "traceability": "traceability",
            "limitations_and_resolutions": "limitations and resolutions",
            "freshness_and_reproducibility": "freshness and reproducibility",
            "notes": "備註",
        },
        "en": {
            "critical_claim_coverage": "Critical claim coverage",
            "source_quality": "Source quality",
            "traceability": "Traceability",
            "limitations_and_resolutions": "Limitations and resolutions",
            "freshness_and_reproducibility": "Freshness and reproducibility",
            "notes": "Notes",
        },
    }[language or "zh-TW"]
    lines.extend(["", f"## {labels['quality_metrics']}", ""])
    for key in (
        "critical_claim_coverage",
        "source_quality",
        "traceability",
        "limitations_and_resolutions",
        "freshness_and_reproducibility",
    ):
        if key in metrics:
            lines.append(f"- {metric_labels[key]}: `{metrics[key]}`")
    if metrics.get("notes"):
        lines.append(f"- {metric_labels['notes']}: {metrics['notes']}")


def _append_scope(lines: list[str], report: dict[str, Any], language: str | None = None) -> None:
    labels = _labels(language)
    lines.extend(["", f"## {labels['questions']}", ""])
    lines.extend(f"- {item}" for item in report.get("questions", []))
    scope = report.get("scope", {})
    lines.extend(["", f"## {labels['scope']}", ""])
    for label_key, scope_key in (
        ("audience", "audience"),
        ("regions", "regions"),
        ("languages", "languages"),
        ("date_range", "date_range"),
    ):
        value = scope.get(scope_key)
        if isinstance(value, list):
            value = ", ".join(value)
        if value:
            lines.append(f"- {labels[label_key]}: {value}")
    if scope.get("include"):
        lines.extend(["", f"### {labels['include']}", ""])
        lines.extend(f"- {item}" for item in scope.get("include", []))
    if scope.get("exclude"):
        lines.extend(["", f"### {labels['exclude']}", ""])
        lines.extend(f"- {item}" for item in scope.get("exclude", []))


def _append_recommendation_sections(lines: list[str], report: dict[str, Any]) -> None:
    sections = report.get("recommendation_sections", {})
    if not sections:
        return

    implementability = sections.get("implementability", {})
    open_source_options = sections.get("open_source_options", {})
    future_directions = sections.get("future_directions", {})

    if implementability:
        lines.extend(["### 1. 可實作性", "", implementability.get("summary", ""), ""])
        for item in implementability.get("items", []):
            lines.extend([
                f"#### {item.get('title', '')}",
                "",
                f"- 目標: {item.get('objective', '')}",
                f"- 技術: {', '.join(item.get('technologies', []))}",
                f"- 流程: {item.get('workflow', '')}",
                f"- 最小可交付: {item.get('minimum_deliverable', '')}",
                f"- 驗收條件: {item.get('acceptance_criteria', '')}",
                f"- 支持來源: {', '.join(item.get('supporting_source_ids', []))}",
                f"- 後續研究 prompt: `{item.get('research_prompt', '')}`",
                "",
            ])

    if open_source_options:
        lines.extend(["### 2. 開源工具組合", "", open_source_options.get("summary", ""), ""])
        single_tools = open_source_options.get("single_tool_recommendations", {})
        if single_tools:
            lines.extend(["#### 2.1 只使用一個開源工具", "", single_tools.get("summary", ""), ""])
            for item in single_tools.get("items", []):
                lines.extend([
                    f"##### 第 {item.get('rank')} 名: {item.get('tool', '')}",
                    "",
                    f"- 推薦理由: {item.get('recommendation_reason', '')}",
                    f"- 適合情境: {item.get('suitable_for', '')}",
                    f"- 優勢: {', '.join(item.get('strengths', []))}",
                    f"- 缺口: {item.get('gaps', '')}",
                    f"- 最小導入方式: {item.get('minimum_adoption', '')}",
                    f"- 支持來源: {', '.join(item.get('supporting_source_ids', []))}",
                    f"- 後續研究 prompt: `{item.get('research_prompt', '')}`",
                    "",
                ])

        multi_tool_stacks = open_source_options.get("multi_tool_recommendations", {})
        if multi_tool_stacks:
            lines.extend(["#### 2.2 多個開源工具配合", "", multi_tool_stacks.get("summary", ""), ""])
            for item in multi_tool_stacks.get("items", []):
                lines.extend([
                    f"##### 第 {item.get('rank')} 名: {item.get('title', '')}",
                    "",
                    f"- 工具: {', '.join(item.get('tools', []))}",
                    f"- 目標: {item.get('objective', '')}",
                    f"- 分工: {item.get('roles', '')}",
                    f"- 流程: {item.get('workflow', '')}",
                    f"- 推薦理由: {item.get('recommendation_reason', '')}",
                    f"- 取捨: {item.get('tradeoffs', '')}",
                    f"- 最小可交付: {item.get('minimum_deliverable', '')}",
                    f"- 驗收條件: {item.get('acceptance_criteria', '')}",
                    f"- 支持來源: {', '.join(item.get('supporting_source_ids', []))}",
                    f"- 後續研究 prompt: `{item.get('research_prompt', '')}`",
                    "",
                ])

    if future_directions:
        lines.extend(["### 3. 未來性", "", future_directions.get("summary", ""), ""])
        for item in future_directions.get("items", []):
            lines.extend([
                f"#### {item.get('title', '')}",
                "",
                f"- 當前限制: {item.get('current_limitation', '')}",
                f"- 方向: {item.get('direction', '')}",
                f"- 觸發條件: {item.get('trigger', '')}",
                f"- 支持來源: {', '.join(item.get('supporting_source_ids', []))}",
                f"- 後續研究 prompt: `{item.get('research_prompt', '')}`",
                "",
            ])


def _append_resolution_matrix(lines: list[str], report: dict[str, Any], language: str | None = None) -> None:
    labels = _labels(language)
    matrix = report.get("resolution_matrix", {})
    sections = [
        (labels["conflict_resolutions"], matrix.get("conflict_resolutions", [])),
        (labels["unknown_resolutions"], matrix.get("unknown_resolutions", [])),
    ]
    if not any(items for _, items in sections):
        return

    lines.extend(["", f"### {labels['resolution_matrix']}", "", matrix.get("summary", ""), ""])
    for title, items in sections:
        if not items:
            continue
        lines.extend([f"#### {title}", ""])
        for item in items:
            lines.extend([
                f"##### `{item.get('resolution_id', '')}` {item.get('title', '')}",
                "",
                f"- {labels['status']}: `{item.get('status', '')}`",
                f"- {labels['decision']}: {item.get('decision', '')}",
                f"- {labels['resolution_method']}: {item.get('resolution_method', '')}",
                f"- {labels['supporting_sources']}: {', '.join(item.get('supporting_source_ids', []))}",
                f"- {labels['next_action']}: {item.get('next_action', '')}",
                f"- {labels['closure_criteria']}: {item.get('closure_criteria', '')}",
                "",
            ])


def _append_source_navigation(lines: list[str], report: dict[str, Any], language: str | None = None) -> None:
    labels = _labels(language)
    sources = report.get("sources", [])
    high_quality = sum(source.get("evidence_tier") in {"A", "B"} for source in sources)
    immutable = sum(bool(source.get("immutable_url")) for source in sources)
    lines.extend([
        "",
        f"## {labels['sources']}",
        "",
        "- " + labels["source_count_summary"].format(total=len(sources), high_quality=high_quality, immutable=immutable),
        f"- [{labels['source_catalog']}](../sources/CATALOG.md)",
        f"- [{labels['source_metadata']}]({report.get('report_set_id', report['report_id'])}.json)",
        f"- {labels['source_snapshot_note']}",
    ])


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


def write_bilingual_report(topic_dir: Path, report: dict[str, Any]) -> tuple[Path, list[Path]]:
    reports_dir = topic_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report.setdefault("generated_at", iso_now())
    report.setdefault("report_set_id", report["report_id"])
    report.setdefault("primary_language", "zh-TW")
    report.setdefault("languages", ["zh-TW", "en"])
    sync_supported_claim_ids(topic_dir, report)

    json_path = reports_dir / f"{report['report_set_id']}.json"
    write_json(json_path, report)
    markdown_paths: list[Path] = []
    for language in report.get("languages", []):
        md_path = reports_dir / f"{report['report_set_id']}.{language}.md"
        md_path.write_text(to_markdown(report, language=language), encoding="utf-8")
        markdown_paths.append(md_path)
    return json_path, markdown_paths


def to_markdown(report: dict[str, Any], language: str | None = None) -> str:
    labels = _labels(language)
    title = _localized(report, language, "title", report.get("title", "Research Report"))
    lines = [
        f"# {title}",
        "",
        f"## {labels['report_info']}",
        "",
        f"- {labels['report_id']}: `{report['report_id']}`",
        f"- {labels['version']}: `{report['version']}`",
        f"- {labels['generated_at']}: `{report['generated_at']}`",
        f"- {labels['data_cutoff']}: `{report['data_cutoff']}`",
        f"- {labels['overall_confidence']}: `{report['overall_confidence']}`",
        f"- {labels['quality_score']}: `{report.get('quality_score', 'N/A')}/100`",
        f"- {labels['structural_score']}: `{report.get('structural_score', 'N/A')}/100`",
        "",
        f"## {labels['summary']}",
        "",
    ]
    _append_text_or_list(lines, _localized(report, language, "executive_summary", ""))
    _append_quality_metrics(lines, report, language=language)
    _append_scope(lines, report, language=language)
    lines.extend(["", f"## {labels['methodology']}", ""])
    _append_text_or_list(lines, _localized(report, language, "methodology", report.get("methodology", "")))
    lines.extend(["", f"## {labels['findings']}", ""])
    for claim in report["claims"]:
        lines.extend([
            f"### `{claim['claim_id']}`",
            "",
            f"- {labels['claim']}: {_localized_claim_value(report, language, claim, 'text')}",
            f"- {labels['type']}: `{claim.get('type', '')}`",
            f"- {labels['importance']}: `{claim['importance']}`",
            f"- {labels['confidence']}: `{claim['confidence']}`",
            f"- {labels['reason']}: {_localized_claim_value(report, language, claim, 'reason')}",
            f"- {labels['supporting_sources']}: {', '.join(claim['supporting_source_ids'])}",
            f"- {labels['opposing_sources']}: {', '.join(claim.get('opposing_source_ids', [])) or labels['none']}",
            f"- {labels['notes']}: {claim.get('notes', '') or labels['none']}",
            "",
        ])
    lines.extend([f"## {labels['limitations']}", ""])
    _append_text_or_list(lines, _localized(report, language, "limitations", report.get("limitations", [])))
    lines.extend(["", f"## {labels['conflicts_unknowns']}", ""])
    matrix = report.get("resolution_matrix", {})
    unresolved = [
        item
        for item in matrix.get("unknown_resolutions", [])
        if item.get("status") in {"open", "partially_resolved"}
    ]
    if matrix:
        resolved_conflicts = sum(item.get("status") == "resolved" for item in matrix.get("conflict_resolutions", []))
        lines.append(f"- {labels['resolved_conflicts']}: `{resolved_conflicts}`")
        lines.append(f"- {labels['open_unknowns']}: `{len(unresolved)}`")
        lines.extend(f"- `{item.get('resolution_id', '')}` `{item.get('status', '')}`: {item.get('title', '')}" for item in unresolved)
    else:
        lines.extend(f"- {item}" for item in report.get("conflicts", []))
        lines.extend(f"- {item}" for item in report.get("unknowns", []))
    _append_resolution_matrix(lines, report, language=language)
    lines.extend(["", f"## {labels['conclusion']}", ""])
    _append_text_or_list(lines, _localized(report, language, "conclusion", report.get("conclusion", "")))
    lines.extend(["", f"## {labels['recommendations']}", ""])
    localized_recommendations = _localized(report, language, "recommendations", report.get("recommendations", []))
    if language == "en" and localized_recommendations:
        _append_text_or_list(lines, localized_recommendations)
    else:
        _append_recommendation_sections(lines, report)
        if report.get("recommendation_sections") and report.get("recommendations"):
            lines.extend([f"### {labels['other_recommendations']}", ""])
        lines.extend(f"- {item}" for item in report.get("recommendations", []))
    _append_source_navigation(lines, report, language=language)
    lines.append("")
    lines.extend([f"## {labels['changelog']}", ""])
    lines.extend(f"- {item}" for item in report.get("changelog", []))
    return "\n".join(lines) + "\n"
