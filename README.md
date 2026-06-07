# Reusable Research Report Pipeline

這是一套 local-first 的研究報告系統。`Codex` Main Research Agent 會控制研究流程，並透過 project-scoped `subagent` 分工處理來源搜尋、來源整理、GitHub repo 深讀、evidence mapping、雙語報告與 quality gate。完整中文介紹請見 [`docs/PROJECT_INTRO.md`](docs/PROJECT_INTRO.md)。

The system turns a research topic into trusted, traceable, bilingual reports. The canonical JSON report is the evidence store; Markdown files are localized renderings.

## Output Contract

Each completed research topic should produce:

- One canonical JSON report: `reports/<report_set_id>.json`
- One Chinese report: `reports/<report_set_id>.zh-TW.md`
- One English report: `reports/<report_set_id>.en.md`
- A source catalog: `sources/CATALOG.md`
- Source records and curated summaries under `sources/S-xxx/`

Chinese reports keep technical proper nouns in their original form, such as `A2A`, `MCP`, `LangGraph`, and `OpenAI Agents SDK`, while explanations, limitations, and recommendations use Traditional Chinese.

## Main Workflow

1. Create or inspect `knowledge-base/topics/<topic_id>/research-request.json`.
2. Search local knowledge first with `local-search`.
3. Maintain `crawl-queue.json`; append new candidates instead of reordering.
4. Collect URL sources into stable `S-xxx` folders.
5. Curate every source summary before using it for important claims.
6. Deep-read GitHub repositories with selected files and immutable commit permalinks.
7. Build a claim-evidence matrix with stable `C-xxx` claim IDs.
8. Write a bilingual report set.
9. Run quality gates and `doctor`.
10. Commit and publish only curated metadata, summaries, reports, and hashes.

Raw snapshots and large archives stay local unless explicitly approved.

## CLI

```text
python scripts/research_pipeline.py run <topic_id>
python scripts/research_pipeline.py status <topic_id>
python scripts/research_pipeline.py queue-add <topic_id> --type url --target <url> --reason <reason>
python scripts/research_pipeline.py collect-url <topic_id> <queue_id> --url <url> --title <title>
python scripts/research_pipeline.py local-search <topic_id> <query>
python scripts/research_pipeline.py curate-batch <topic_id> --input <reviewed-summaries.json>
python scripts/research_pipeline.py curate-sources <topic_id>
python scripts/research_pipeline.py catalog <topic_id>
python scripts/research_pipeline.py write-bilingual-report <topic_id> --input <synthesis.json>
python scripts/research_pipeline.py quality-check <topic_id> <report_set_id>
python scripts/research_pipeline.py task-create <topic_id> --agent <role> --objective <text>
python scripts/research_pipeline.py task-list <topic_id>
python scripts/research_pipeline.py task-start <topic_id> <task_id>
python scripts/research_pipeline.py task-block <topic_id> <task_id> --reason <text>
python scripts/research_pipeline.py task-fail <topic_id> <task_id> --reason <text>
python scripts/research_pipeline.py task-validate <topic_id> <task_id>
python scripts/research_pipeline.py task-complete <topic_id> <task_id> --result <json>
python scripts/research_pipeline.py task-backlog-summary-gate <topic_id>
python scripts/research_pipeline.py repo-manifest <topic_id> <source_id>
python scripts/research_pipeline.py doctor <topic_id>
python scripts/validate_workflow_alignment.py
python scripts/validate_report.py --report-set knowledge-base/topics/<topic_id>/reports <report_set_id>
python scripts/validate_crawl_queue.py knowledge-base/topics/<topic_id>/crawl-queue.json
python -m unittest tests.test_research_pipeline
```

`run` is a main-agent checkpoint command. It reports the next crawl item, summary quality issues, agent task counts, existing reports, and the next safe action. `doctor` aggregates workflow alignment, crawl queue, summary, task, report, and Git publication risk checks without modifying files.

## Codex Agent Contract

`AGENTS.md` is the repository-level Main Research Agent rule source. Project-scoped subagent definitions live in `.codex/agents/*.toml`, following the Codex custom agent style.

| Subagent | Responsibility | Required output |
| --- | --- | --- |
| Source Hunter Agent | Find candidate URLs and append-only queue items. | Queue additions with reason and related question IDs. |
| Source Curator Agent | Read one source snapshot and write a reviewed summary. | `summary.json` and `summary.md` passing summary gates. |
| GitHub Repo Analyst Agent | Deep-read a repository source. | `repo_analysis` with reviewed files, features, architecture, boundaries, and locators. |
| Evidence Mapper Agent | Map claims to supporting/opposing sources. | Stable claim IDs and backlink-ready source IDs. |
| Report Writer Agent | Produce localized report content. | Canonical synthesis JSON with `localized_content`. |
| Quality Gate Agent | Validate report, summaries, and bilingual outputs. | Pass/fail list with concrete file/source/claim IDs. |

Detailed role, model, workflow, quality, and do/don't rules live in [`docs/AGENT_ORCHESTRATION.md`](docs/AGENT_ORCHESTRATION.md). Chinese rendering rules live in [`docs/I18N.md`](docs/I18N.md). Spec alignment is tracked in [`docs/WORKFLOW_ALIGNMENT.md`](docs/WORKFLOW_ALIGNMENT.md).

## Quality Gates

Before publishing:

- Validate the crawl queue.
- Validate source summaries with `curate-sources`.
- Validate report consistency with `validate_report.py`.
- Validate bilingual output files with `--report-set`.
- Validate workflow alignment with `validate_workflow_alignment.py`.
- Run `doctor <topic_id>`.
- Confirm every critical claim has sources.
- Confirm source backlinks match claim backlinks.
- Confirm conflicts and unknowns have resolution items.
- Confirm raw snapshots and large archives are not staged accidentally.

## Key Files

- `AGENTS.md`
- `.codex/agents/*.toml`
- `docs/PROJECT_INTRO.md`
- `docs/RESEARCH_WORKFLOW.md`
- `docs/AUTOMATION_PIPELINE.md`
- `docs/WORKFLOW_ALIGNMENT.md`
- `docs/AGENT_ORCHESTRATION.md`
- `docs/I18N.md`
- `schemas/research-request.schema.json`
- `schemas/source-record.schema.json`
- `schemas/document-summary.schema.json`
- `schemas/report.schema.json`
- `schemas/agent-profile.schema.json`
- `schemas/subagent-task.schema.json`
- `research_pipeline/`
- `scripts/research_pipeline.py`
- `scripts/validate_workflow_alignment.py`
- `scripts/validate_report.py`
- `scripts/validate_crawl_queue.py`
