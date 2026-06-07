# Automation Pipeline

This document maps the reusable research workflow to runnable commands and
module responsibilities. v1 implements a single main workflow entry with clear
subagent contracts; future versions can replace those contracts with parallel
workers.

## 1. CLI Entry Points

```text
python scripts/research_pipeline.py run <topic_id>
python scripts/research_pipeline.py status <topic_id>
python scripts/research_pipeline.py queue-add <topic_id> --type <type> --target <target> --reason <reason>
python scripts/research_pipeline.py queue-update <topic_id> <queue_id> --status <status>
python scripts/research_pipeline.py collect-url <topic_id> <queue_id> --url <url> --title <title>
python scripts/research_pipeline.py local-search <topic_id> <query>
python scripts/research_pipeline.py curate-batch <topic_id> --input <reviewed-summaries.json>
python scripts/research_pipeline.py curate-sources <topic_id>
python scripts/research_pipeline.py catalog <topic_id>
python scripts/research_pipeline.py draft-report <topic_id> --report-id <report_id>
python scripts/research_pipeline.py write-report <topic_id> --input <synthesis.json>
python scripts/research_pipeline.py write-bilingual-report <topic_id> --input <synthesis.json>
python scripts/research_pipeline.py quality-check <topic_id> <report_set_id>
```

`run` is the main agent's checkpoint command. It reports:

- next pending crawl item
- source summary gate status
- existing report count
- next safe actions

It does not overwrite source IDs or reports.

## 2. Module Map

| Module | Path | Responsibility |
| --- | --- | --- |
| `request_parser` | `research_pipeline/request_parser.py` | Normalize research requests and output language aliases. |
| `query_planner` | `research_pipeline/query_planner.py` | Build candidate query dimensions. |
| `crawl_queue` | `research_pipeline/crawl_queue.py` | Append and update ordered queue items. |
| `source_collector` | `research_pipeline/source_collector.py` | Fetch URL content. |
| `source_normalizer` | `research_pipeline/source_normalizer.py` | Normalize URL and text content. |
| `snapshot_store` | `research_pipeline/snapshot_store.py` | Persist snapshots and hashes. |
| `source_metadata` | `research_pipeline/source_metadata.py` | Build `source.json`, including GitHub repository metadata. |
| `document_curator` | `research_pipeline/document_curator.py` | Save reviewed source summaries. |
| `summary_quality` | `research_pipeline/summary_quality.py` | Enforce summary and GitHub repo gates. |
| `local_retriever` | `research_pipeline/local_retriever.py` | Search local summaries and source metadata. |
| `source_evaluator` | `research_pipeline/source_evaluator.py` | Score source quality. |
| `source_catalog` | `research_pipeline/source_catalog.py` | Write `sources/CATALOG.md`. |
| `claim_extractor` | `research_pipeline/claim_extractor.py` | Draft atomic claims from summaries. |
| `evidence_mapper` | `research_pipeline/evidence_mapper.py` | Assign stable claim IDs and source mappings. |
| `report_writer` | `research_pipeline/report_writer.py` | Write canonical JSON and localized Markdown reports. |
| `quality_gate` | `research_pipeline/quality_gate.py` | Calculate report quality metrics. |

## 3. Automated Run Pattern

1. `run <topic_id>` to inspect current state.
2. If local evidence is insufficient, Source Hunter appends queue items with
   `queue-add`.
3. For URL items, `collect-url` creates or updates an `S-xxx` source folder.
4. Source Curator writes reviewed summaries.
5. `curate-batch` saves only summaries that pass the summary gate.
6. GitHub Repo Analyst fills `repository` metadata and `repo_analysis` for repo
   sources.
7. `catalog <topic_id>` refreshes `sources/CATALOG.md`.
8. Evidence Mapper creates claim-source mappings.
9. Report Writer prepares synthesis JSON with `localized_content`.
10. `write-bilingual-report` writes canonical JSON plus `zh-TW` and `en`
    Markdown.
11. Quality Gate runs `curate-sources`, `quality-check`,
    `validate_report.py --report-set`, and `validate_crawl_queue.py`.
12. Main agent commits only curated artifacts.

## 4. Subagent Execution Contract

Subagents are not long-running services in v1. They are task contracts controlled
by the Main Research Agent. Each task should record:

- agent role
- intended model
- reasoning effort
- task input
- expected output
- write scope
- quality gate

Agent profiles validate against `schemas/agent-profile.schema.json`. Detailed
role definitions live in `docs/AGENT_ORCHESTRATION.md`.

## 5. Input And Output Schemas

Canonical schemas:

- `schemas/research-request.schema.json`
- `schemas/source-crawl-queue.schema.json`
- `schemas/source-record.schema.json`
- `schemas/document-summary.schema.json`
- `schemas/report.schema.json`
- `schemas/agent-profile.schema.json`
- `schemas/subagent-task.schema.json`

Report output set:

```text
reports/<report_set_id>.json
reports/<report_set_id>.zh-TW.md
reports/<report_set_id>.en.md
```

The JSON file is the canonical evidence store. Markdown files must share the
same `claim_id`, `source_id`, and `resolution_id` mappings.

## 6. GitHub Repository Automation

GitHub repo handling should avoid full-repo inspection by default.

Automation steps:

1. Capture owner, name, default branch, and commit SHA.
2. Build immutable permalinks for reviewed files.
3. Select files by question:
   - README or overview
   - docs
   - config/build files
   - source entry points
   - examples
   - tests
   - license, security policy, release notes when relevant
4. Fill `repo_analysis`.
5. Record files not reviewed and why.
6. Downgrade README-only sources to positioning evidence.

## 7. Quality Automation

Summary gate:

- rejects missing `document_purpose`
- rejects empty or truncated `summary`
- requires `key_points[].locator`
- requires `keywords`
- requires `limitations`
- requires GitHub `repo_analysis` for GitHub repo sources

Report gate:

- critical claims need supporting sources
- sources and claims need symmetric backlinks
- conflicts and unknowns need resolution items
- bilingual files must exist when `languages` includes both languages
- Markdown outputs cannot alter evidence mapping

Crawl queue gate:

- queue structure validates
- completed items reference source outputs
- skipped and failed items include notes
- IDs remain stable

## 8. Human Stop Conditions

Automation continues without asking for routine research work. It stops only
when the next decision changes scope, legal risk, or adoption judgment:

- objective is unclear
- repo deep-read scope cannot be inferred
- access, license, robots, or redistribution is uncertain
- README and source code conflict materially
- adoption recommendation lacks maturity, safety, or benchmark evidence
- security or compliance conclusion lacks required policy/test evidence

## 9. Publication Checklist

Before Git publication:

- Run schema and CLI tests.
- Run summary gates.
- Run report gates.
- Run crawl queue validation.
- Check `git status --short`.
- Confirm raw snapshots, archives, local outputs, caches, and temporary plan
  files are not staged.
