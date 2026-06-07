# Workflow Alignment

This document is the alignment table for the reusable research workflow. It does not replace the source documents; it shows which document owns each rule, which implementation currently supports it, and how to verify drift.

Status values:

- `implemented`: implemented and covered by a runnable check or CLI path.
- `specified only`: specified, but only partially automated or waiting for backlog execution.
- `future`: intentionally outside v1.

| 規格來源 | 對應實作 | 驗證方式 | 目前狀態 |
| --- | --- | --- | --- |
| `AGENTS.md` | Main Research Agent operating rules and escalation boundaries. | `python scripts/validate_workflow_alignment.py` checks required subagent mentions and core path references. | `implemented` |
| `.codex/agents/*.toml` | Project-scoped Codex subagent definitions. | TOML parse check plus required `name`, `description`, `developer_instructions`. | `implemented` |
| `schemas/subagent-task.schema.json` | Topic-level task contract for Main Agent to subagent dispatch. | Role enum alignment check against `.codex/agents/*.toml`; CLI `task-validate`. | `implemented` |
| `knowledge-base/topics/<topic_id>/agent-tasks/T-xxx.json` | Task lifecycle storage: `pending -> in_progress -> completed/failed/blocked`. | `task-create`, `task-start`, `task-block`, `task-fail`, `task-complete`, `task-validate`. | `implemented` |
| `docs/RESEARCH_WORKFLOW.md` | End-to-end research process source of truth. | Workflow alignment check plus CLI smoke tests. | `implemented` |
| `docs/AUTOMATION_PIPELINE.md` | CLI and module behavior source of truth. | CLI help, `doctor`, and module import checks. | `implemented` |
| `research_pipeline/repo_manifest.py` | GitHub repo selected-files manifest collector. | `repo-manifest <topic_id> <source_id>` creates `repo-manifest.json`, updates repository metadata, and creates blocked tasks for unclear scope. | `implemented` |
| `docs/PROJECT_INTRO.md` | Human-facing project introduction and navigation. | UTF-8, mojibake, Markdown table, and agent coverage checks. | `implemented` |
| `schemas/document-summary.schema.json` and `research_pipeline/summary_quality.py` | Source summary gate and GitHub repo depth gate. | `curate-sources` and `task-backlog-summary-gate`. | `implemented` |
| `schemas/report.schema.json`, `research_pipeline/quality_gate.py`, `scripts/validate_report.py` | Canonical report, backlinks, bilingual report set, quality metrics. | `quality-check` and `validate_report.py --report-set`. | `implemented` |
| `schemas/source-crawl-queue.schema.json` and `research_pipeline/crawl_queue.py` | Ordered crawl queue with stable append-only history. | `validate_crawl_queue.py` and CLI queue commands. | `implemented` |
| `docs/I18N.md` | Traditional Chinese and bilingual output rules. | Encoding/Markdown checks and report writer review. | `specified only` |
| A2A source quality remediation | Backlog generation for failing source summary gates. | `task-backlog-summary-gate a2a-agent-communication-ai-coding-team`. | `specified only` |
| Fixture-based automated test suite | Reusable ordinary-doc, GitHub repo, unpinned repo, monorepo, and README-only fixtures under `tests/fixtures/`. | `python -m unittest tests.test_research_pipeline`. | `implemented` |
| True parallel subagent workers | Future worker runtime that executes task files concurrently. | Not available in v1. | `future` |
| GitHub selected-file content fetcher | Optional future collector for immutable file contents without cloning the whole repo. | Not available in v1. | `future` |
| Benchmark / PoC runner | Optional future runner for executable evidence. | Not available in v1. | `future` |

## Drift Rules

- If `AGENTS.md` changes Main Agent behavior, update `docs/RESEARCH_WORKFLOW.md` or this alignment table in the same change.
- If a `.codex/agents/*.toml` role changes, update `schemas/subagent-task.schema.json` and `docs/AGENT_ORCHESTRATION.md` when the role name, responsibility, model, or quality gate changes.
- If a CLI command changes, update `docs/AUTOMATION_PIPELINE.md`, `README.md`, and `AGENTS.md`.
- If a path becomes canonical, add it to `docs/PROJECT_INTRO.md`.
- If a feature remains `specified only`, it must either have a backlog task or be clearly marked as future work.
