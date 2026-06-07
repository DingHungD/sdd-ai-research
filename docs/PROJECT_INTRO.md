# 專案介紹

## 1. 專案概述

本專案是一套可複用的研究報告系統，用 `Codex` Main Research Agent 控制研究流程，並用 project-scoped `subagent` 分工處理來源搜尋、來源整理、GitHub repo 深讀、evidence mapping、雙語報告撰寫與 quality gate。

系統目標是把「研究題目」轉成可追溯、可重跑、可審查的可信報告。每個重要結論都要能回到來源、claim、resolution 與品質檢查結果；中文內容遵守 `docs/I18N.md`，技術專有名詞保留英文，例如 `Codex`, `AGENTS.md`, `subagent`, `A2A`, `MCP`, `GitHub`, `repo_analysis`。

## 2. 研究工作流

研究工作流由 `Main Research Agent` 控制：

1. 接收研究主題與研究請求。
2. 檢查本地知識庫、目前 topic state 與既有來源。
3. 判斷下一個最小可執行任務。
4. 必要時分派給合適的 `subagent`。
5. `subagent` 回傳結構化結果。
6. `Main Research Agent` 驗收結果，整合 evidence mapping、品質檢查與報告輸出。
7. 若發現缺口，新增後續任務或 crawl queue 項目。
8. 只在研究目標不明、repo 深讀範圍不明、授權風險或採用決策證據不足時詢問人類。

本章只描述流程與調度邏輯，不展開各 `subagent` 產生的檔案。

## 3. Main Agent 如何調度 subagents

`Main Research Agent` 不把整個專案丟給 `subagent`。它會先讀取 `index.json`, `sources/CATALOG.md`, `crawl-queue.json`, `research-request.json` 等狀態檔，再根據缺口建立明確任務。

調度原則：

- 任務要小，輸入範圍要明確。
- 每個任務要指定 `agent_role`, model, reasoning effort, objective, input, expected output, write scope 與 quality gate。
- `subagent` 只處理被分派的產物，不接管 source ID、claim ID、report set ID 或最終採用決策。
- 若 `subagent` 發現新來源需求，只能回報或追加 queue item，不能重排既有 queue。
- 若 evidence 不足，Main Agent 應降權、標成 unknown 或建立 backlog，而不是強行產生結論。

## 4. Agent 與 Subagent 用途表

| Agent | 用途 | 邊界 |
| --- | --- | --- |
| Main Research Agent | 控制完整研究流程，管理 topic state、任務分派、驗收、evidence mapping、品質檢查與 publish decision。 | 不把未驗證來源直接寫成可信結論。 |
| Source Hunter Agent | 找候選來源，補搜尋關鍵字，追加 crawl queue。 | 不產生最終 claim，不整理 source summary。 |
| Source Curator Agent | 將單一來源整理成可重用摘要，補上 purpose、key points、locators、limitations。 | 不做 final recommendation，不深讀 GitHub repo 實作細節。 |
| GitHub Repo Analyst Agent | 對 GitHub repo 做 selected-files 深讀，產生 repo 功能、架構、邊界與品質訊號分析。 | 不預設 clone 或閱讀整個 repo，不把 README 當成熟度證據。 |
| Evidence Mapper Agent | 將整理後的 evidence 拆成 atomic claims，建立 claim-source backlinks、conflicts 與 unknowns。 | 不新增來源，不改寫 summary，不寫最終報告 prose。 |
| Report Writer Agent | 根據 canonical synthesis 產生中英雙語報告內容。 | 不改變 claim/source/resolution mapping。 |
| Quality Gate Agent | 檢查 schema、summary gate、repo depth、backlinks、雙語輸出與 publication readiness。 | 不默默修內容；只回報 blocking errors、warnings 與修正方向。 |

## 5. Agent 與 Subagent 輸入輸出表

| Agent | 概念輸入 | 概念輸出 |
| --- | --- | --- |
| Main Research Agent | 研究主題、research request、topic state、本地知識庫、品質檢查結果。 | 任務分派、整合後研究狀態、下一步、publish decision。 |
| Source Hunter Agent | 研究問題、證據缺口、既有 queue、既有 source catalog。 | 候選來源項目、搜尋理由、去重結果、剩餘缺口。 |
| Source Curator Agent | 單一來源、source metadata、snapshot 或 immutable source。 | 可重用摘要、key points、limitations、來源可支撐與不可支撐的範圍。 |
| GitHub Repo Analyst Agent | GitHub repo source、研究問題、repo metadata、selected files。 | repo 深讀分析、feature inventory、architecture summary、capability boundaries、quality signals。 |
| Evidence Mapper Agent | curated evidence、source records、研究問題、既有 report JSON。 | claim-evidence matrix、conflicts、unknowns、resolution items、backlink-ready references。 |
| Report Writer Agent | canonical synthesis、claim-evidence matrix、sources、resolution matrix。 | 雙語 localized content、canonical report JSON 與 Markdown 報告內容。 |
| Quality Gate Agent | report set、source summaries、crawl queue、schemas、Git 狀態。 | pass/fail 結果、blocking errors、warnings、修正清單。 |

## 6. Agent 與 Subagent 紀錄與溝通用途表

| Agent | 檔案名稱 | 用途 |
| --- | --- | --- |
| Main Research Agent | `AGENTS.md` | Codex repo-level 操作規則，定義 Main Agent 行為邊界與調度原則。 |
| Main Research Agent | `knowledge-base/topics/<topic_id>/research-request.json` | 記錄研究題目、目標、問題、範圍、來源偏好與輸出語言。 |
| Main Research Agent | `schemas/subagent-task.schema.json` | 定義 Main Agent 分派給 subagent 的 task contract。 |
| Main Research Agent | `knowledge-base/topics/<topic_id>/agent-tasks/T-xxx.json` | 記錄 subagent task lifecycle、input、expected output、write scope 與 quality gate。 |
| Main Research Agent | `knowledge-base/topics/<topic_id>/crawl-queue.json` | 維持候選來源探索順序與處理狀態。 |
| Source Hunter Agent | `.codex/agents/source-hunter.toml` | Source Hunter 的角色、職責、模型、流程與品質規則。 |
| Source Hunter Agent | `knowledge-base/topics/<topic_id>/crawl-queue.json` | 追加候選來源、搜尋理由與 discovered_from。 |
| Source Curator Agent | `.codex/agents/source-curator.toml` | Source Curator 的角色、職責、模型、流程與品質規則。 |
| Source Curator Agent | `knowledge-base/topics/<topic_id>/sources/S-xxx/summary.json` | 儲存 structured source summary，供 evidence mapping 與 report reuse。 |
| Source Curator Agent | `knowledge-base/topics/<topic_id>/sources/S-xxx/summary.md` | 儲存人類可讀的來源摘要。 |
| GitHub Repo Analyst Agent | `.codex/agents/github-repo-analyst.toml` | GitHub Repo Analyst 的角色、職責、模型、流程與品質規則。 |
| GitHub Repo Analyst Agent | `knowledge-base/topics/<topic_id>/sources/S-xxx/repo-manifest.json` | 記錄 selected-files strategy、reviewed/not reviewed files 與 immutable URL 狀態。 |
| GitHub Repo Analyst Agent | `knowledge-base/topics/<topic_id>/sources/S-xxx/summary.json` | 儲存或補齊 `repo_analysis`。 |
| Evidence Mapper Agent | `.codex/agents/evidence-mapper.toml` | Evidence Mapper 的角色、職責、模型、流程與品質規則。 |
| Evidence Mapper Agent | `knowledge-base/topics/<topic_id>/reports/<report_set_id>.json` | 儲存 claim-evidence matrix、conflicts、unknowns 與 resolution matrix。 |
| Report Writer Agent | `.codex/agents/report-writer.toml` | Report Writer 的角色、職責、模型、流程與品質規則。 |
| Report Writer Agent | `knowledge-base/topics/<topic_id>/reports/<report_set_id>.json` | 作為 canonical evidence store 與 bilingual content 來源。 |
| Report Writer Agent | `knowledge-base/topics/<topic_id>/reports/<report_set_id>.zh-TW.md` | 中文報告輸出。 |
| Report Writer Agent | `knowledge-base/topics/<topic_id>/reports/<report_set_id>.en.md` | 英文報告輸出。 |
| Quality Gate Agent | `.codex/agents/quality-gate.toml` | Quality Gate 的角色、職責、模型、流程與品質規則。 |
| Quality Gate Agent | `scripts/validate_workflow_alignment.py` | 檢查 agent 設定、schema enum、文件路徑、encoding 與 Markdown table。 |
| Quality Gate Agent | `scripts/validate_report.py` | 檢查 report schema、backlinks 與雙語 report set。 |
| Quality Gate Agent | `scripts/validate_crawl_queue.py` | 檢查 crawl queue 結構與 completed item source reference。 |

## 7. 路徑與檔案意義

| 路徑 | 意義 |
| --- | --- |
| `AGENTS.md` | Main Research Agent 的最高層操作規則。 |
| `.codex/agents/*.toml` | Codex project-scoped custom agents，也就是各 `subagent` 的執行規格。 |
| `docs/PROJECT_INTRO.md` | 人類導覽文件，說明專案用途、流程與重要路徑。 |
| `docs/RESEARCH_WORKFLOW.md` | 研究流程的規格來源。 |
| `docs/AUTOMATION_PIPELINE.md` | CLI 與模組行為的規格來源。 |
| `docs/WORKFLOW_ALIGNMENT.md` | 規格來源、對應實作、驗證方式與目前狀態的對齊表。 |
| `docs/AGENT_ORCHESTRATION.md` | Main Agent 與 subagents 的分工、模型與工作規則。 |
| `docs/I18N.md` | 中文與雙語輸出的 i18n 規則。 |
| `schemas/*.schema.json` | research request、source、summary、report、agent profile、subagent task 等結構規格。 |
| `research_pipeline/` | Python pipeline 模組實作。 |
| `scripts/research_pipeline.py` | pipeline CLI 入口。 |
| `knowledge-base/topics/<topic_id>/` | 單一研究題目的狀態與產物根目錄。 |
| `sources/S-xxx/` | 單一來源資料夾，使用穩定 source ID。 |
| `sources/CATALOG.md` | 來源目錄，用於快速理解每個來源的用途與大綱。 |
| `reports/<report_set_id>.*` | 報告輸出；JSON 是 canonical evidence store，Markdown 是語言化 rendering。 |

## 8. 品質與可追溯性設計

品質規則的核心是：所有重要結論都要能回到可檢查的 evidence。

- `Main Research Agent` 保留 source ID、claim ID、report set ID 的穩定性。
- 來源摘要必須通過 summary gate，不能只是 HTML sidebar 或截斷文字。
- GitHub repo 若支撐實作、架構、成熟度或安全性主張，必須有 `repo_analysis`。
- report 以 canonical JSON 作為 evidence store。
- 中英 Markdown 不得改變 evidence mapping。
- `Quality Gate Agent` 檢查 critical claims、backlinks、雙語輸出、conflicts、unknowns 與 crawl queue。
- raw snapshots、大型壓縮檔、local outputs 與 temporary plan 預設不進 Git。
