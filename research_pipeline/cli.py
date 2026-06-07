from __future__ import annotations

import argparse
from pathlib import Path

from .agent_tasks import block_task, complete_task, create_task, fail_task, list_tasks, load_task, start_task, validate_task
from .claim_extractor import extract_claim_drafts
from .crawl_queue import append_item, next_pending, update_item
from .document_curator import save_reviewed_summary
from .evidence_mapper import assign_claim_ids
from .io_utils import iso_now, read_json
from .local_retriever import retrieve
from .quality_gate import evaluate_report_details
from .repo_manifest import build_repo_manifest
from .report_writer import sync_supported_claim_ids, write_bilingual_report, write_report
from .source_catalog import write_catalog
from .source_collector import fetch_url
from .summary_quality import validate_summary, validate_topic_summaries
from .workflow import register_snapshot, topic_dir


ROOT = Path(__file__).resolve().parents[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local-first research workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status")
    status.add_argument("topic_id")

    run = sub.add_parser("run")
    run.add_argument("topic_id")

    add_queue = sub.add_parser("queue-add")
    add_queue.add_argument("topic_id")
    add_queue.add_argument("--type", required=True, choices=["search_query", "url", "domain_seed", "local_gap"])
    add_queue.add_argument("--target", required=True)
    add_queue.add_argument("--reason", required=True)
    add_queue.add_argument("--question", action="append", default=[])
    add_queue.add_argument("--step", default="manual")
    add_queue.add_argument("--from-queue")

    queue_update = sub.add_parser("queue-update")
    queue_update.add_argument("topic_id")
    queue_update.add_argument("queue_id")
    queue_update.add_argument("--status", required=True, choices=["pending", "in_progress", "completed", "failed", "skipped"])
    queue_update.add_argument("--notes", default="")

    collect = sub.add_parser("collect-url")
    collect.add_argument("topic_id")
    collect.add_argument("queue_id")
    collect.add_argument("--url", required=True)
    collect.add_argument("--title", required=True)
    collect.add_argument("--source-type", default="official_documentation")
    collect.add_argument("--author", default="")
    collect.add_argument("--publisher", default="")

    search = sub.add_parser("local-search")
    search.add_argument("topic_id")
    search.add_argument("query")

    report = sub.add_parser("draft-report")
    report.add_argument("topic_id")
    report.add_argument("--report-id", required=True)

    quality = sub.add_parser("quality-check")
    quality.add_argument("topic_id")
    quality.add_argument("report_id")

    curate_sources = sub.add_parser("curate-sources")
    curate_sources.add_argument("topic_id")

    curate_batch = sub.add_parser("curate-batch")
    curate_batch.add_argument("topic_id")
    curate_batch.add_argument("--input", required=True)

    write_report_command = sub.add_parser("write-report")
    write_report_command.add_argument("topic_id")
    write_report_command.add_argument("--input", required=True)

    write_bilingual = sub.add_parser("write-bilingual-report")
    write_bilingual.add_argument("topic_id")
    write_bilingual.add_argument("--input", required=True)

    catalog = sub.add_parser("catalog")
    catalog.add_argument("topic_id")

    task_create = sub.add_parser("task-create")
    task_create.add_argument("topic_id")
    task_create.add_argument("--agent", required=True)
    task_create.add_argument("--objective", required=True)
    task_create.add_argument("--path", action="append", default=[])
    task_create.add_argument("--question", action="append", default=[])
    task_create.add_argument("--constraint", action="append", default=[])
    task_create.add_argument("--source", action="append", default=[])
    task_create.add_argument("--claim", action="append", default=[])
    task_create.add_argument("--status", default="pending", choices=["pending", "in_progress", "completed", "failed", "blocked"])
    task_create.add_argument("--human-escalation-reason")

    task_list = sub.add_parser("task-list")
    task_list.add_argument("topic_id")

    task_validate = sub.add_parser("task-validate")
    task_validate.add_argument("topic_id")
    task_validate.add_argument("task_id")

    task_complete = sub.add_parser("task-complete")
    task_complete.add_argument("topic_id")
    task_complete.add_argument("task_id")
    task_complete.add_argument("--result", required=True)

    task_start = sub.add_parser("task-start")
    task_start.add_argument("topic_id")
    task_start.add_argument("task_id")

    task_block = sub.add_parser("task-block")
    task_block.add_argument("topic_id")
    task_block.add_argument("task_id")
    task_block.add_argument("--reason", required=True)

    task_fail = sub.add_parser("task-fail")
    task_fail.add_argument("topic_id")
    task_fail.add_argument("task_id")
    task_fail.add_argument("--reason", required=True)

    backlog = sub.add_parser("task-backlog-summary-gate")
    backlog.add_argument("topic_id")
    backlog.add_argument("--limit", type=int, default=0)

    repo_manifest = sub.add_parser("repo-manifest")
    repo_manifest.add_argument("topic_id")
    repo_manifest.add_argument("source_id")

    doctor = sub.add_parser("doctor")
    doctor.add_argument("topic_id")

    return parser


def _load_report_sources(directory: Path, report_data: dict) -> None:
    source_ids = report_data.pop("source_ids", [])
    if "sources" not in report_data:
        report_data["sources"] = [
            read_json(directory / "sources" / source_id / "source.json") for source_id in source_ids
        ]


def _score_report(directory: Path, report_data: dict) -> tuple[dict, list[str]]:
    sync_supported_claim_ids(directory, report_data)
    metrics, errors = evaluate_report_details(report_data)
    report_data["quality_score"] = metrics["quality_score"]
    report_data["structural_score"] = metrics["structural_score"]
    report_data["quality_metrics"] = metrics
    return metrics, errors


def _command_run(directory: Path, topic_id: str) -> int:
    item = next_pending(directory)
    summary_errors = validate_topic_summaries(directory)
    reports_dir = directory / "reports"
    reports = sorted(reports_dir.glob("*.json")) if reports_dir.exists() else []
    tasks = list_tasks(directory)
    pending_tasks = [task for task in tasks if task.get("status") in {"pending", "blocked"}]

    print(f"Topic: {topic_id}")
    print("Next crawl item: none" if item is None else f"Next crawl item: {item['queue_id']} {item['target_type']} {item['target']}")
    print(f"Summary gate: {'passed' if not summary_errors else f'{len(summary_errors)} issue(s)'}")
    print(f"Reports: {len(reports)} JSON report(s)")
    print(f"Agent tasks: {len(tasks)} total, {len(pending_tasks)} pending/blocked")
    print("Main-agent next actions:")
    if item is not None:
        print("- Process the next crawl queue item or append discovered URLs to the queue.")
    if summary_errors:
        print("- Fix curated summaries before using affected sources for critical claims.")
        print("- Run task-backlog-summary-gate to create traceable remediation tasks.")
    if pending_tasks:
        print("- Dispatch or resolve pending/blocked agent tasks.")
    if not reports:
        print("- Build synthesis JSON and run write-bilingual-report when evidence mapping is ready.")
    if item is None and not summary_errors and reports and not pending_tasks:
        print("- Run quality-check and publish.")
    for error in summary_errors[:20]:
        print(f"SUMMARY ERROR: {error}")
    if len(summary_errors) > 20:
        print(f"SUMMARY ERROR: ... {len(summary_errors) - 20} more")
    return 1 if summary_errors else 0


def _command_draft_report(directory: Path, report_id: str) -> int:
    topic = read_json(directory / "topic.json")
    index = read_json(directory / "index.json")
    summaries = [read_json(directory / item["summary_path"]) for item in index.get("sources", [])]
    sources = [read_json(directory / item["source_path"]) for item in index.get("sources", [])]
    claims = assign_claim_ids(extract_claim_drafts(summaries))
    report = {
        "report_id": report_id,
        "version": "0.1.0-draft",
        "title": topic["title"],
        "generated_at": iso_now(),
        "data_cutoff": iso_now(),
        "overall_confidence": "low",
        "quality_score": 0,
        "executive_summary": "This is a pipeline-generated draft that requires agent review before publication.",
        "questions": [item["text"] if isinstance(item, dict) else item for item in topic["questions"]],
        "scope": {
            "audience": topic.get("audience", ""),
            "regions": topic.get("scope", {}).get("regions", []),
            "languages": topic.get("scope", {}).get("languages", []),
            "date_range": topic.get("scope", {}).get("date_range", ""),
            "include": topic.get("scope", {}).get("include", []),
            "exclude": topic.get("scope", {}).get("exclude", []),
        },
        "methodology": "Local-first pipeline draft from curated snapshots.",
        "claims": claims,
        "sources": sources,
        "conflicts": [],
        "unknowns": [],
        "resolution_matrix": {
            "summary": "Draft resolution matrix pending agent review.",
            "conflict_resolutions": [],
            "unknown_resolutions": [],
        },
        "limitations": ["This draft requires agent review before publication."],
        "conclusion": "Draft conclusion pending agent review.",
        "recommendation_sections": {
            "implementability": {"summary": "", "items": []},
            "open_source_options": {
                "summary": "",
                "single_tool_recommendations": {"summary": "", "items": []},
                "multi_tool_recommendations": {"summary": "", "items": []},
            },
            "future_directions": {"summary": "", "items": []},
        },
        "recommendations": [],
        "changelog": ["0.1.0-draft: generated from local curated snapshots."],
    }
    metrics, errors = _score_report(directory, report)
    write_report(directory, report)
    print(f"Drafted {report_id} with score {metrics['quality_score']}.")
    for error in errors:
        print(f"WARNING: {error}")
    return 0


def _command_task_backlog(directory: Path, topic_id: str, limit: int) -> int:
    errors = validate_topic_summaries(directory)
    by_source: dict[str, list[str]] = {}
    for error in errors:
        source_id = error.split(":", 1)[0]
        by_source.setdefault(source_id, []).append(error)
    existing_sources = {
        source_id
        for task in list_tasks(directory)
        if task.get("status") in {"pending", "in_progress", "blocked"}
        for source_id in task.get("input", {}).get("source_ids", [])
        if str(task.get("objective", "")).startswith("Fix summary gate issues")
    }
    created = 0
    skipped = 0
    for source_id, source_errors in sorted(by_source.items()):
        if limit and created >= limit:
            break
        if source_id in existing_sources:
            skipped += 1
            continue
        role = "github_repo_analyst_agent" if any("repo_analysis" in error or "GitHub repository" in error for error in source_errors) else "source_curator_agent"
        source_path = f"knowledge-base/topics/{topic_id}/sources/{source_id}/source.json"
        summary_path = f"knowledge-base/topics/{topic_id}/sources/{source_id}/summary.json"
        create_task(
            directory,
            topic_id=topic_id,
            agent_role=role,
            objective=f"Fix summary gate issues for {source_id}.",
            paths_or_urls=[source_path, summary_path],
            questions=source_errors,
            constraints=[
                "Do not change source_id.",
                "Do not reorder crawl queue.",
                "Preserve provenance and add locators for every key point.",
            ],
            source_ids=[source_id],
        )
        created += 1
    print(f"Created {created} summary-gate backlog task(s).")
    if skipped:
        print(f"Skipped {skipped} source(s) that already have active backlog tasks.")
    return 0 if created or skipped or not errors else 1


def _command_doctor(directory: Path, topic_id: str) -> int:
    blocking: list[str] = []
    warnings: list[str] = []
    recommendations: list[str] = []

    try:
        from scripts.validate_workflow_alignment import main as validate_alignment

        if validate_alignment() != 0:
            blocking.append("workflow alignment validation failed")
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        blocking.append(f"cannot run workflow alignment validation: {exc}")

    queue_path = directory / "crawl-queue.json"
    if queue_path.exists():
        try:
            from scripts.validate_crawl_queue import validate as validate_crawl_queue

            for error in validate_crawl_queue(read_json(queue_path)):
                blocking.append(f"crawl queue: {error}")
        except Exception as exc:  # pragma: no cover - defensive CLI boundary
            blocking.append(f"cannot validate crawl queue: {exc}")
    else:
        warnings.append("crawl-queue.json is missing")

    summary_errors = validate_topic_summaries(directory)
    if summary_errors:
        warnings.append(f"summary gate has {len(summary_errors)} issue(s)")
        recommendations.append("Run task-backlog-summary-gate or dispatch existing source curator / GitHub repo analyst tasks.")

    for task in list_tasks(directory):
        for error in validate_task(task):
            blocking.append(f"{task.get('task_id', '<unknown>')}: {error}")

    reports_dir = directory / "reports"
    report_paths = sorted(reports_dir.glob("*.json")) if reports_dir.exists() else []
    if report_paths:
        try:
            from scripts.validate_report import validate_report_set

            for report_path in report_paths:
                report_id = report_path.stem
                for error in validate_report_set(reports_dir, report_id):
                    blocking.append(f"{report_id}: {error}")
        except Exception as exc:  # pragma: no cover - defensive CLI boundary
            blocking.append(f"cannot validate report sets: {exc}")
    else:
        warnings.append("reports directory has no JSON reports")

    if (ROOT / "outputs").exists():
        warnings.append("outputs/ exists; keep it out of Git unless explicitly approved")
    if list(ROOT.rglob("__pycache__")):
        warnings.append("__pycache__ directories exist; remove generated caches before publication")
    raw_dirs = list((directory / "sources").glob("S-*/raw")) if (directory / "sources").exists() else []
    if raw_dirs:
        warnings.append("source raw/ snapshots exist; do not stage them unless redistribution is approved")

    print(f"Doctor: {topic_id}")
    print("Status: failed" if blocking else "Status: passed with warnings" if warnings else "Status: passed")
    for item in blocking:
        print(f"BLOCKING: {item}")
    for item in warnings[:30]:
        print(f"WARNING: {item}")
    if len(warnings) > 30:
        print(f"WARNING: ... {len(warnings) - 30} more")
    for item in recommendations:
        print(f"RECOMMENDED: {item}")
    return 1 if blocking else 0


def main() -> int:
    args = build_parser().parse_args()
    directory = topic_dir(ROOT, args.topic_id)

    if args.command == "status":
        item = next_pending(directory)
        print("No pending crawl queue items." if item is None else f"Next: {item['queue_id']} {item['target_type']} {item['target']}")
        return 0
    if args.command == "run":
        return _command_run(directory, args.topic_id)
    if args.command == "queue-add":
        item = append_item(
            directory,
            target_type=args.type,
            target=args.target,
            reason=args.reason,
            related_question_ids=args.question,
            added_by_step=args.step,
            discovered_from=args.from_queue,
        )
        print(f"Added {item['queue_id']}.")
        return 0
    if args.command == "queue-update":
        item = update_item(directory, args.queue_id, status=args.status, notes=args.notes)
        print(f"Updated {item['queue_id']} to {item['status']}.")
        return 0
    if args.command == "collect-url":
        document = fetch_url(args.url)
        source = register_snapshot(
            ROOT,
            topic_id=args.topic_id,
            queue_id=args.queue_id,
            title=args.title,
            url=document.final_url,
            content=document.content,
            content_type=document.content_type,
            source_type=args.source_type,
            author_or_organization=args.author,
            publisher=args.publisher,
        )
        print(f"Saved {source['source_id']}.")
        return 0
    if args.command == "local-search":
        for match in retrieve(directory, args.query):
            print(f"{match['source_id']}\t{match['score']}\t{match.get('title', '')}")
        return 0
    if args.command == "draft-report":
        return _command_draft_report(directory, args.report_id)
    if args.command == "quality-check":
        report_path = directory / "reports" / f"{args.report_id}.json"
        report = read_json(report_path)
        metrics, errors = evaluate_report_details(report)
        if report.get("report_set_id"):
            expected = [directory / "reports" / f"{report['report_set_id']}.{language}.md" for language in report.get("languages", [])]
            for path in expected:
                if not path.exists():
                    errors.append(f"missing localized markdown output: {path.name}")
        print(f"Quality score: {metrics['quality_score']}")
        print(f"Structural score: {metrics['structural_score']}")
        for key in (
            "critical_claim_coverage",
            "source_quality",
            "traceability",
            "limitations_and_resolutions",
            "freshness_and_reproducibility",
        ):
            print(f"{key}: {metrics[key]}")
        for error in errors:
            print(f"ERROR: {error}")
        return 1 if errors else 0
    if args.command == "curate-sources":
        errors = validate_topic_summaries(directory)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("All source summaries passed quality gates.")
        return 0
    if args.command == "curate-batch":
        from .workflow import update_index

        summaries = read_json(Path(args.input))["summaries"]
        for summary in summaries:
            source = read_json(directory / "sources" / summary["source_id"] / "source.json")
            errors = validate_summary(source, summary)
            if errors:
                for error in errors:
                    print(f"ERROR: {error}")
                return 1
            save_reviewed_summary(directory, summary)
            update_index(directory, source, summary)
        print(f"Saved {len(summaries)} reviewed summaries.")
        return 0
    if args.command == "write-report":
        report_data = read_json(Path(args.input))
        _load_report_sources(directory, report_data)
        metrics, errors = _score_report(directory, report_data)
        write_report(directory, report_data)
        print(f"Saved {report_data['report_id']} with score {metrics['quality_score']}.")
        for error in errors:
            print(f"WARNING: {error}")
        return 1 if errors else 0
    if args.command == "write-bilingual-report":
        report_data = read_json(Path(args.input))
        _load_report_sources(directory, report_data)
        report_data.setdefault("report_set_id", report_data["report_id"])
        report_data.setdefault("primary_language", "zh-TW")
        report_data.setdefault("languages", ["zh-TW", "en"])
        _, errors = _score_report(directory, report_data)
        json_path, md_paths = write_bilingual_report(directory, report_data)
        print(f"Saved {json_path}")
        for path in md_paths:
            print(f"Saved {path}")
        for error in errors:
            print(f"WARNING: {error}")
        return 1 if errors else 0
    if args.command == "catalog":
        path = write_catalog(directory)
        print(f"Saved {path}.")
        return 0
    if args.command == "task-create":
        task = create_task(
            directory,
            topic_id=args.topic_id,
            agent_role=args.agent,
            objective=args.objective,
            paths_or_urls=args.path,
            questions=args.question or [args.objective],
            constraints=args.constraint,
            source_ids=args.source,
            claim_ids=args.claim,
            status=args.status,
            human_escalation_reason=args.human_escalation_reason,
        )
        print(f"Created {task['task_id']} for {task['agent_role']}.")
        return 0
    if args.command == "task-list":
        for task in list_tasks(directory):
            print(f"{task['task_id']}\t{task['status']}\t{task['agent_role']}\t{task['objective']}")
        return 0
    if args.command == "task-validate":
        errors = validate_task(load_task(directory, args.task_id))
        for error in errors:
            print(f"ERROR: {error}")
        print("Task validation passed." if not errors else f"Task validation failed: {len(errors)} issue(s).")
        return 1 if errors else 0
    if args.command == "task-complete":
        try:
            task = complete_task(directory, args.task_id, read_json(Path(args.result)))
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Updated {task['task_id']} to {task['status']}.")
        return 0
    if args.command == "task-start":
        try:
            task = start_task(directory, args.task_id)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Updated {task['task_id']} to {task['status']}.")
        return 0
    if args.command == "task-block":
        try:
            task = block_task(directory, args.task_id, args.reason)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Updated {task['task_id']} to {task['status']}.")
        return 0
    if args.command == "task-fail":
        try:
            task = fail_task(directory, args.task_id, args.reason)
        except ValueError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(f"Updated {task['task_id']} to {task['status']}.")
        return 0
    if args.command == "task-backlog-summary-gate":
        return _command_task_backlog(directory, args.topic_id, args.limit)
    if args.command == "repo-manifest":
        manifest = build_repo_manifest(directory, args.source_id)
        print(f"Saved repo manifest for {manifest['source_id']}.")
        return 0
    if args.command == "doctor":
        return _command_doctor(directory, args.topic_id)
    raise AssertionError("unhandled command")


if __name__ == "__main__":
    raise SystemExit(main())
