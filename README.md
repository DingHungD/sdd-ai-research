# Reusable Research Report Pipeline

This repository stores a local-first research workflow for producing trusted,
traceable reports from a research topic. The v1 workflow is designed for a main
agent that controls the run and delegates bounded work to subagents.

## Output Contract

Each completed research topic should produce:

- One canonical JSON report: `reports/<report_set_id>.json`
- One Chinese report: `reports/<report_set_id>.zh-TW.md`
- One English report: `reports/<report_set_id>.en.md`
- A source catalog: `sources/CATALOG.md`
- Source records and curated summaries under `sources/S-xxx/`

The JSON report is the evidence store. Markdown files are localized renderings.
Chinese reports keep technical proper nouns in their original form, such as
`A2A`, `MCP`, `LangGraph`, and `OpenAI Agents SDK`, while explanations,
limitations, and recommendations use Chinese.

## Main Workflow

1. Create or inspect `knowledge-base/topics/<topic_id>/research-request.json`.
2. Search local knowledge first with `local-search`.
3. Maintain `crawl-queue.json`; append new candidates instead of reordering.
4. Collect URL sources into stable `S-xxx` folders.
5. Curate every source summary before using it for important claims.
6. Deep-read GitHub repositories with README, docs/config, key source files,
   examples/tests when available, and immutable commit permalinks.
7. Build a claim-evidence matrix with stable `C-xxx` claim IDs.
8. Write a bilingual report set.
9. Run quality gates.
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
python scripts/research_pipeline.py write-bilingual-report <topic_id> --input <synthesis.json>
python scripts/research_pipeline.py quality-check <topic_id> <report_set_id>
python scripts/validate_report.py --report-set knowledge-base/topics/<topic_id>/reports <report_set_id>
python scripts/validate_crawl_queue.py knowledge-base/topics/<topic_id>/crawl-queue.json
```

`run` is a main-agent status gate. It does not replace research judgment; it
shows the next crawl item, summary quality issues, existing reports, and the
next safe action.

## Subagent Contract

The main agent owns the topic state, source IDs, claim IDs, final synthesis, and
human-escalation decisions. Subagents receive bounded tasks and return structured
artifacts.

Detailed role, model, workflow, quality, and do/don't rules live in
[`docs/AGENT_ORCHESTRATION.md`](docs/AGENT_ORCHESTRATION.md). Chinese rendering
rules live in [`docs/I18N.md`](docs/I18N.md).

| Subagent | Responsibility | Required output |
| --- | --- | --- |
| Source Hunter Agent | Find candidate URLs and append-only queue items. | Queue additions with reason and related question IDs. |
| Source Curator Agent | Read one source snapshot and write a reviewed summary. | `summary.json` and `summary.md` passing summary gates. |
| GitHub Repo Analyst Agent | Deep-read a repository source. | `repo_analysis` with reviewed files, features, architecture, boundaries, and locators. |
| Evidence Mapper Agent | Map claims to supporting/opposing sources. | Stable claim IDs and backlink-ready source IDs. |
| Report Writer Agent | Produce localized report content. | Canonical synthesis JSON with `localized_content`. |
| Quality Gate Agent | Validate report, summaries, and bilingual outputs. | Pass/fail list with concrete file/source/claim IDs. |

Subagents must not reorder source IDs, delete queue history, or silently upgrade
evidence confidence. If a subagent discovers a new source need, it appends a new
queue item with `discovered_from` and a reason.

### Model Selection

Use the smallest model that can reliably complete the assigned role:

- `gpt-5.4-mini medium`: source discovery and narrow queue work.
- `gpt-5.4 medium`: source curation, GitHub selected-file analysis, evidence mapping, and standard quality checks.
- `gpt-5.5 medium`: main orchestration, final synthesis, bilingual report writing, high-impact conflict resolution, adoption decisions.
- `gpt-5.5 high`: only for complex security/legal/compliance synthesis or difficult cross-source conflicts.

When runtime model overrides are unavailable, record the intended model profile
in the task and continue with the available model.

## Human Escalation Rules

Ask the human only when a decision changes research scope, legal/redistribution
risk, or adoption judgment:

- The research objective cannot be inferred from the request.
- A repository is too large or is a monorepo and the core deep-read scope is
  ambiguous.
- License, visibility, robots, paywall, or redistribution terms are unclear.
- README and source code materially conflict.
- The user asks for an adoption recommendation, but evidence only proves that a
  project exists.
- Security or compliance conclusions need organization policy, threat model, or
  benchmark evidence that is not public.

Do not ask the human for routine work:

- Query expansion and source discovery.
- URL de-duplication and canonicalization.
- Commit permalink and snapshot hash capture.
- Downgrading weak sources.
- Marking unresolved items as open in the resolution matrix.
- Creating follow-up research prompts or backlog items.

## AI-First File Selection

Agents must not force themselves to read an entire project by default. They
select files based on the question:

- Start with manifests, README, docs, config, examples, tests, and obvious entry
  points.
- Use repository tree shape to choose a minimal evidence set.
- Read additional files only when a claim cannot be supported by the selected
  set.
- Record `files_reviewed` and `files_not_reviewed`.
- Stop once evidence is sufficient and limitations are documented.

## Source Summary Gate

Every reviewed source summary must include:

- `document_purpose`
- A non-truncated `summary`
- `key_points[]` with locators
- `keywords[]`
- `limitations[]`

Initial machine extraction is not enough for publication. A source summary that
looks like HTML navigation, a sidebar, or the first 1200 characters of a page
must be replaced by a reviewed summary.

## GitHub Repository Gate

GitHub repository sources need repository metadata and `repo_analysis` before
they can support critical implementation, architecture, maturity, or security
claims. The minimum deep-read is:

- README or project overview
- docs or config/build files when available
- key source files
- examples or tests when available
- release, changelog, license, or security policy when relevant

The repo summary must record:

- Fixed `commit_sha` or immutable URL
- `files_reviewed` and `files_not_reviewed`
- feature inventory with evidence locators
- architecture summary
- core files and their roles
- supported, unsupported, and unclear capability boundaries
- operational model and quality signals

README-only sources can support project positioning claims, but not claims that
the implementation is mature, secure, or production-ready.

## Quality Gates

Before publishing:

- Validate the crawl queue.
- Validate source summaries with `curate-sources`.
- Validate report consistency with `validate_report.py`.
- Validate bilingual output files with `--report-set`.
- Confirm every critical claim has sources.
- Confirm source backlinks match claim backlinks.
- Confirm conflicts and unknowns have resolution items.
- Confirm raw snapshots and large archives are not staged accidentally.

## Key Files

- `docs/TRUSTED_REPORT_SPEC.md`
- `docs/RESEARCH_WORKFLOW.md`
- `docs/AUTOMATION_PIPELINE.md`
- `docs/AGENT_ORCHESTRATION.md`
- `docs/I18N.md`
- `schemas/research-request.schema.json`
- `schemas/source-record.schema.json`
- `schemas/document-summary.schema.json`
- `schemas/report.schema.json`
- `schemas/agent-profile.schema.json`
- `schemas/subagent-task.schema.json`
- `prompts/research-agent.md`
- `prompts/document-curator-agent.md`
- `scripts/research_pipeline.py`
- `scripts/validate_report.py`
- `scripts/validate_crawl_queue.py`
