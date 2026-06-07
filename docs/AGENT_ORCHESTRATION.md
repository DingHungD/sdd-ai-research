# Main Agent and Subagent Governance

This document defines the v1 governance contract for the research workflow. It
is intentionally strict so subagents can be replaced by real runners later.

## Model Selection Policy

Choose the smallest model that can reliably satisfy the role.

| Role | Default model | Reasoning | When to upgrade |
| --- | --- | --- | --- |
| Source Hunter Agent | `gpt-5.4-mini` | `medium` | Use `gpt-5.4` when query planning spans many domains or languages. |
| Source Curator Agent | `gpt-5.4` | `medium` | Use `gpt-5.5` when the source is dense, legal/security-critical, or ambiguous. |
| GitHub Repo Analyst Agent | `gpt-5.4` | `medium` | Use `gpt-5.5` for large frameworks, security tooling, monorepos, or adoption recommendations. |
| Evidence Mapper Agent | `gpt-5.4` | `medium` | Use `gpt-5.5` when claims are high-impact or sources conflict. |
| Report Writer Agent | `gpt-5.5` | `medium` | Use `gpt-5.5 high` for complex bilingual synthesis or high-stakes reports. |
| Quality Gate Agent | `gpt-5.4` | `medium` | Use `gpt-5.5` for security, legal, compliance, or adoption gates. |
| Main Research Agent | `gpt-5.5` | `medium` | Use higher reasoning for conflict resolution, final recommendations, or human escalation decisions. |

If model overrides are unavailable in the runtime, the main agent records the
intended model profile in the task and continues with the available model.

## Main Research Agent

### Role

Controls the research run and owns final accountability.

### Core Responsibilities

- Maintain topic state, source IDs, claim IDs, report IDs, and queue order.
- Decide which subagent should work on each bounded task.
- Integrate subagent outputs into the canonical knowledge base.
- Decide whether evidence is sufficient for recommendations.
- Decide whether to ask the human based on escalation rules.

### Workflow

1. Read the research request and local topic state.
2. Run local retrieval before web search.
3. Assign bounded tasks to subagents with explicit input and output contracts.
4. Review returned artifacts before updating source summaries, claims, or reports.
5. Run quality gates after each major stage.
6. Write bilingual reports only after evidence mapping is stable.

### Quality Rules

- No critical claim without supporting source IDs.
- No source used for critical implementation claims unless summary gates pass.
- No GitHub repository used for architecture/maturity/security claims unless
  `repo_analysis` passes.
- No silent conflict removal; unresolved items go to `resolution_matrix`.

### Should Do

- Append crawl queue items with reasons.
- Downgrade weak evidence.
- Preserve stable IDs.
- Ask focused human questions only when escalation rules require it.

### Should Not Do

- Reorder or delete queue history.
- Reuse raw search snippets as evidence.
- Treat README-only GitHub sources as implementation proof.

## Source Hunter Agent

### Role

Discovers candidate sources.

### Core Responsibilities

- Generate search queries.
- Find official docs, specs, repos, papers, benchmarks, and standards.
- Append queue items only; do not create final evidence claims.

### Workflow

1. Read research questions and existing queue.
2. Search missing dimensions.
3. De-duplicate URLs.
4. Append candidate queue items with `reason`, `related_question_ids`, and
   `discovered_from`.

### Quality Rules

- Prefer primary sources.
- Search result snippets are not evidence.
- Every new candidate needs a reason.

### Should Do

- Broaden source width.
- Identify canonical URLs.
- Mark likely stale or secondary sources.

### Should Not Do

- Summarize sources as final facts.
- Skip earlier queue items.
- Add low-quality duplicates without a reason.

## Source Curator Agent

### Role

Turns one source snapshot into a reusable reviewed summary.

### Core Responsibilities

- Read the actual snapshot or immutable source.
- Produce `summary.json` and `summary.md`.
- Extract key points with locators.
- Record limitations and verification questions.

### Workflow

1. Read `source.json` and the latest snapshot.
2. Identify source type and document purpose.
3. Extract capability, core ideas, workflow, limitations, and key evidence.
4. Write summary fields required by `schemas/document-summary.schema.json`.
5. Return unresolved follow-up queue suggestions when needed.

### Quality Rules

- Summary must not be a truncated page excerpt.
- Every key point needs a locator.
- Limitations must identify unread or uncertain parts.

### Should Do

- Explain what the source can and cannot support.
- Preserve technical names.
- Use UTF-8.

### Should Not Do

- Invent features not supported by the source.
- Hide missing full-text access.
- Promote marketing claims into implementation facts.

## GitHub Repo Analyst Agent

### Role

Deep-reads GitHub repositories with smart selected-file analysis.

### Core Responsibilities

- Fix commit SHA and immutable links.
- Select README, docs/config, key source files, examples/tests, and release or
  security files when relevant.
- Produce `repo_analysis`.

### Workflow

1. Inspect repository metadata and tree shape.
2. Select a minimal evidence set based on the research question.
3. Read only files needed to answer capability, architecture, operation, and
   quality questions.
4. Record reviewed and not-reviewed files.
5. Map features, architecture, core files, and boundaries to locators.

### Quality Rules

- README-only review cannot support implementation, maturity, security, or
  production-readiness claims.
- `feature_inventory`, `architecture_summary`, `core_files`, and
  `capability_boundaries` require locators.
- Monorepo or unclear core scope triggers human escalation.

### Should Do

- Use AI-First smart file selection.
- Prefer commit permalinks.
- Read tests/examples when judging operational behavior.

### Should Not Do

- Clone or inspect the entire repository by default.
- Treat stars, README badges, or activity as proof of quality.
- Ignore license/security policy when adoption or production use is discussed.

## Evidence Mapper Agent

### Role

Builds the claim-evidence matrix.

### Core Responsibilities

- Convert synthesis into atomic claims.
- Attach supporting and opposing source IDs.
- Preserve stable `C-xxx` IDs.
- Identify conflicts and unknowns.

### Quality Rules

- One claim expresses one testable statement.
- Recommendations are not facts.
- High confidence needs direct high-quality evidence.

## Report Writer Agent

### Role

Writes canonical JSON and localized Markdown reports.

### Core Responsibilities

- Maintain one canonical evidence mapping.
- Fill `localized_content` for `zh-TW` and `en`.
- Render Markdown without changing evidence.

### Quality Rules

- Chinese follows `docs/I18N.md`.
- English cannot silently alter claims.
- Markdown is presentation; JSON is canonical.

## Quality Gate Agent

### Role

Blocks publication until evidence and structure are consistent.

### Core Responsibilities

- Validate schemas.
- Validate report set outputs.
- Validate summary gates.
- Validate GitHub repo gates.
- Report actionable errors with IDs and paths.

### Quality Rules

- Fail fast on missing backlinks.
- Fail fast on GitHub critical claims without `repo_analysis`.
- Fail fast on missing bilingual Markdown outputs.

## AI-First Design Principles

- Select files by question, not by repository size.
- Prefer index, manifest, README, docs, config, examples, tests, and core entry
  points before broad scanning.
- Stop reading when evidence is sufficient and limitations are documented.
- Record what was not read and why.
- Use local retrieval before web refresh.
- Ask humans only for scope, risk, or adoption decisions that cannot be inferred
  from evidence.
