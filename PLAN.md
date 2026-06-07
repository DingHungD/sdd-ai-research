# 研究工作流 v1 穩定化計畫

## Summary

本計畫將目前的「聊天式研究」收斂成 `Codex Main Research Agent + project-scoped subagents + task lifecycle` 的 v1 穩定工作流。目標是讓研究流程可重跑、可追蹤、可驗收，並讓新舊資料的差異被明確標記，不因舊資料尚未補齊而阻塞 CLI。

## Key Changes

### 1. 建立單一工作流真相來源

- [x] `AGENTS.md` 作為 Main Research Agent 的最高層操作規則。
- [x] `.codex/agents/*.toml` 作為 subagent 執行規格來源。
- [x] `docs/RESEARCH_WORKFLOW.md` 作為研究流程來源。
- [x] `docs/AUTOMATION_PIPELINE.md` 作為 CLI 與模組行為來源。
- [x] `docs/PROJECT_INTRO.md` 作為人類導覽文件，不承擔規格決策。
- [x] `docs/WORKFLOW_ALIGNMENT.md` 作為規格、實作、驗證方式與狀態的對齊表。

### 2. 補齊 Main Agent 到 Subagent 的任務執行層

- [x] 新增 topic-level task storage：`knowledge-base/topics/<topic_id>/agent-tasks/T-xxx.json`。
- [x] 任務格式遵守 `schemas/subagent-task.schema.json`。
- [x] 新增 `task-create`。
- [x] 新增 `task-list`。
- [x] 新增 `task-start`。
- [x] 新增 `task-block`。
- [x] 新增 `task-fail`。
- [x] 新增 `task-complete`。
- [x] 新增 `task-validate`。
- [x] `task-complete` 會驗證 subagent result required fields。
- [x] v1 使用可追蹤 task lifecycle，不實作真正 parallel worker。

### 3. 補齊 GitHub Repo Manifest Collector

- [x] 新增 `repo-manifest <topic_id> <source_id>`。
- [x] 記錄 owner、name、default branch、commit SHA、immutable tree URL。
- [x] 記錄 selected-files strategy。
- [x] 記錄 `candidate_files`、`selected_files`、`selection_reasons`。
- [x] 記錄 `files_reviewed` 與 `files_not_reviewed`。
- [x] 未 pin commit 時標記 `needs_commit_pin`。
- [x] repo 疑似 monorepo 或 scope 不明時建立 `github_repo_analyst_agent` 的 `blocked` task。
- [x] 不 clone 全 repo，不做完整 repo 掃描。

### 4. 加入一致性與品質檢查

- [x] 新增 `scripts/validate_workflow_alignment.py`。
- [x] 檢查 `AGENTS.md` 是否提到 6 個 subagents。
- [x] 檢查 `.codex/agents/*.toml` 是否可 parse，且包含 `name`, `description`, `developer_instructions`。
- [x] 檢查 `docs/PROJECT_INTRO.md` 是否涵蓋 7 個 agents。
- [x] 檢查 `schemas/subagent-task.schema.json` role enum 是否與 `.codex/agents/*.toml` 對齊。
- [x] 檢查 README / intro / workflow / automation docs 是否指向同一批核心路徑。
- [x] 檢查 UTF-8、mojibake marker、Markdown table 欄位數。
- [x] 新增 `doctor <topic_id>` 聚合 workflow、queue、summary、task、report、Git 風險檢查。

### 5. 升級既有研究資料

- [x] 針對 `a2a-agent-communication-ai-coding-team` 建立 summary-gate 修復 backlog。
- [x] 缺 `key_points[].locator` 的來源交給 Source Curator。
- [x] GitHub repo 缺 `repo_analysis` 的來源交給 GitHub Repo Analyst。
- [x] HTML/sidebar polluted summary 交給 Source Curator 重整。
- [x] 不改 source ID，不重排 crawl queue。
- [ ] 實際完成 45 個 A2A source 修復 task。此項屬於後續 backlog 執行，不納入 v1 穩定化完成條件。

## Test Plan

- [x] `python -m unittest tests.test_research_pipeline`
- [x] `python scripts/validate_workflow_alignment.py`
- [x] `python scripts/validate_crawl_queue.py knowledge-base/topics/a2a-agent-communication-ai-coding-team/crawl-queue.json`
- [x] `python scripts/validate_report.py --report-set knowledge-base/topics/a2a-agent-communication-ai-coding-team/reports a2a-agent-communication-ai-coding-team-20260607-v1`
- [x] `python scripts/research_pipeline.py task-validate a2a-agent-communication-ai-coding-team T-001`
- [x] `python scripts/research_pipeline.py doctor a2a-agent-communication-ai-coding-team`

## Future Work

- [ ] 真正 parallel subagent worker runner。
- [ ] GitHub selected-file content fetcher。
- [ ] benchmark / PoC runner。
- [ ] 批次執行 A2A source summary 修復。

## Assumptions

- v1 完成的是可追蹤 task lifecycle，不是常駐或並行 worker。
- GitHub repo analysis 採 selected-files strategy，不預設 clone 全 repo。
- 舊單語 report 保持可驗證；新 request 若宣告雙語，才強制雙語 report set。
- A2A source 修復是 backlog，不阻塞工作流穩定化。
