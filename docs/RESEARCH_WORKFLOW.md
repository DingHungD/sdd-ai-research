# Research Workflow

This document defines the reusable workflow for turning a research topic into a
trusted, bilingual, evidence-backed report. The workflow is local-first: it
reuses existing topic sources before collecting new web material.

## 1. Research Request

Each topic starts from `knowledge-base/topics/<topic_id>/research-request.json`
and validates against `schemas/research-request.schema.json`.

Required intent fields:

- `topic`: research topic.
- `objective`: expected decision or report purpose.
- `questions`: research questions.
- `scope`: included and excluded boundaries.
- `source_preferences`: preferred source types, freshness, and depth.
- `output.languages`: output languages, usually `["zh-TW", "en"]`.
- `output.primary_language`: usually `"zh-TW"`.

`output.language` is preserved as a backward-compatible alias. New requests
should use `output.languages`.

## 2. Main Agent Flow

The Main Research Agent owns the end-to-end state and delegates bounded tasks to
subagents. It never gives a subagent ownership of source IDs, claim IDs, final
recommendations, or publication decisions.

Codex orchestration sources:

- `AGENTS.md`
- `.codex/agents/*.toml`
- `docs/RESEARCH_WORKFLOW.md`
- `docs/AUTOMATION_PIPELINE.md`
- `docs/WORKFLOW_ALIGNMENT.md`
- `schemas/subagent-task.schema.json`
- `scripts/research_pipeline.py`
- `knowledge-base/topics/<topic_id>/`

1. Read `research-request.json`, `topic.json`, `index.json`, and
   `crawl-queue.json`.
2. Search local sources first with `local-search`.
3. Decide the next bounded task.
4. Assign the task to the right subagent using `docs/AGENT_ORCHESTRATION.md`.
5. Validate the returned artifact before accepting it.
6. Update source records, summaries, claim matrix, or reports.
7. Run quality gates.
8. Ask the human only when escalation rules apply.

## 3. Crawl Queue

Candidate sources are stored in
`knowledge-base/topics/<topic_id>/crawl-queue.json` and validate against
`schemas/source-crawl-queue.schema.json`.

Rules:

- Add new items to the end of the queue.
- Do not reorder, delete, or renumber historical queue items.
- If later steps discover a missing source, append it with `discovered_from`.
- Completed items must reference their resulting source ID.
- Failed or skipped items need notes explaining why.

Queue item types:

- `search_query`: a query that should produce candidate URLs.
- `url`: a specific URL to collect.
- `domain_seed`: a canonical domain or repo to explore.
- `local_gap`: a locally discovered gap that needs more evidence.

## 4. Source Collection

URL collection creates stable source folders:

```text
knowledge-base/topics/<topic_id>/sources/S-001/
  source.json
  summary.json
  summary.md
  raw/
```

`raw/` snapshots are local by default and should not be committed unless a human
explicitly approves redistribution. `source.json` stores metadata, hashes,
freshness policy, canonical URL, immutable URL when available, and
`supported_claim_ids` backlinks.

## 5. Source Curation

Each source needs a reviewed summary before it can support important claims.
The summary must validate against `schemas/document-summary.schema.json`.

Minimum required fields:

- `document_purpose`
- `summary`
- `key_points[]` with `locator`
- `keywords[]`
- `limitations[]`

The summary gate rejects sidebar text, HTML navigation, raw snippets, and
truncated first-page excerpts. Curators must explain what the source can and
cannot support.

## 6. GitHub Repository Deep Read

GitHub repository sources require deeper handling because README claims are not
enough to support implementation, maturity, architecture, or security claims.

Minimum GitHub source record:

- `repository.owner`
- `repository.name`
- `repository.default_branch`
- `repository.commit_sha`
- `repository.immutable_url`
- `repository.capture_manifest_path`
- `repository.capture_scope`
- `repository.selection_reason`

Minimum `repo_analysis`:

- `commit_sha`
- `files_reviewed`
- `files_not_reviewed`
- `feature_inventory`
- `architecture_summary`
- `core_files`
- `capability_boundaries`
- `operational_model`
- `quality_signals`
- `evidence_coverage`
- `open_questions`

Selected-file strategy is mandatory. The GitHub Repo Analyst starts from README,
docs, config, entry points, examples, tests, releases, license, and security
policy when relevant. It reads more only when a claim still lacks support.

README-only repository sources may support project positioning, but not
implementation capability, maturity, security, or production readiness.

## 7. Source Catalog

Run:

```text
python scripts/research_pipeline.py catalog <topic_id>
```

This writes `sources/CATALOG.md`, which lists every `S-xxx`, title, source type,
purpose, category, quality signal, and outline. The report should link to this
catalog instead of embedding long source details in the report body.

## 8. Claim-Evidence Matrix

The Evidence Mapper turns findings into atomic claims:

- `C-xxx` stable claim IDs.
- One claim per testable statement.
- `supporting_source_ids`.
- `opposing_source_ids`.
- confidence and confidence reason.

Backlinks must be symmetric:

- Each claim lists supporting source IDs.
- Each source record lists `supported_claim_ids`.

Recommendations are not facts. They must cite the facts and constraints that
support the recommendation.

## 9. Conflicts And Unknowns

Conflicts and unknowns are first-class report objects:

- `conflicts[]`: contradictory or competing evidence.
- `unknowns[]`: unresolved evidence gaps.
- `resolution_matrix.conflict_resolutions[]`.
- `resolution_matrix.unknown_resolutions[]`.

Each resolution item must include:

- `resolution_id`
- `status`: `resolved`, `partially_resolved`, or `open`
- `decision`
- `resolution_method`
- `supporting_source_ids`
- `next_action`
- `closure_criteria`

Open items are acceptable when clearly scoped. They must not be hidden.

## 10. Canonical JSON Report

The canonical report is:

```text
reports/<report_set_id>.json
```

It validates against `schemas/report.schema.json` and stores shared evidence:

- report metadata
- quality metrics
- claims
- sources
- conflicts
- unknowns
- resolution matrix
- recommendation sections
- `localized_content`

Markdown reports are renderings. They must not change claim IDs, source IDs,
resolution IDs, or evidence mappings.

## 11. Bilingual Markdown Reports

Write report sets with:

```text
python scripts/research_pipeline.py write-bilingual-report <topic_id> --input <synthesis.json>
```

Outputs:

- `<report_set_id>.json`
- `<report_set_id>.zh-TW.md`
- `<report_set_id>.en.md`

Chinese follows `docs/I18N.md`: technical proper nouns remain in original form;
explanations, limitations, recommendations, and synthesis use Traditional
Chinese.

## 12. Quality Gates

Run before publishing:

```text
python scripts/research_pipeline.py curate-sources <topic_id>
python scripts/research_pipeline.py quality-check <topic_id> <report_set_id>
python scripts/validate_report.py --report-set knowledge-base/topics/<topic_id>/reports <report_set_id>
python scripts/validate_crawl_queue.py knowledge-base/topics/<topic_id>/crawl-queue.json
python scripts/research_pipeline.py doctor <topic_id>
```

The gates check:

- summary completeness
- GitHub repo depth
- critical claim source coverage
- claim/source backlink symmetry
- conflicts and unknowns
- bilingual Markdown existence
- shared evidence mapping
- crawl queue structure
- task lifecycle validity
- Git publication risks such as `outputs/`, caches, and raw snapshots

## 13. Human Escalation

Ask the human only for decisions the agent cannot responsibly infer:

- unclear objective
- unclear monorepo or large repo deep-read scope
- license, visibility, robots, paywall, or redistribution risk
- README/source-code conflict that changes the conclusion
- adoption decision where evidence only proves existence
- security or compliance conclusion lacking policy, benchmark, or test evidence

The agent handles routine work without asking:

- query expansion
- queue append
- URL de-duplication
- canonical URL and commit permalink capture
- weak source downgrade
- unknown labeling
- follow-up research backlog

## 14. Version Control

Commit only reusable research artifacts:

- schemas
- workflow docs
- prompts
- source metadata
- reviewed summaries
- source catalog
- canonical reports
- localized reports

Do not stage raw snapshots, large archives, local output folders, caches, or
temporary execution plans.
