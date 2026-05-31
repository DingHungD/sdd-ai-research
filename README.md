# Reusable Research Report Pipeline

這個 repo 定義一套可複用的網路研究流程：輸入研究題目與條件，蒐集可追溯的網路資源，分析證據，輸出可信報告。

目前版本先建立「報告契約」與「品質規則」。後續可在同一套格式上加入搜尋、擷取、去重、評分、引用檢查與報告生成程式。

## 核心文件

- `docs/TRUSTED_REPORT_SPEC.md`：可信報告的定義、格式與評分規則。
- `docs/RESEARCH_WORKFLOW.md`：從題目到報告的標準流程與品質閘門。
- `docs/LOCAL_KNOWLEDGE_BASE.md`：保存來源快照、摘要與更新策略的本地研究資料庫規格。
- `docs/SOURCE_CRAWL_QUEUE.md`：規定 agent 爬取順序與後續追加方式。
- `docs/AUTOMATION_PIPELINE.md`：自動化模組、CLI 與人工覆核邊界。
- `templates/report-template.md`：供人員或 agent 直接填寫的 Markdown 報告範本。
- `schemas/research-request.schema.json`：研究任務的機器可讀輸入格式。
- `schemas/source-record.schema.json`：單一來源的機器可讀紀錄格式。
- `schemas/report.schema.json`：報告輸出的機器可讀格式。
- `schemas/topic.schema.json`：本地研究領域的機器可讀格式。
- `schemas/document-summary.schema.json`：文件整理 agent 的摘要輸出格式。
- `schemas/knowledge-index.schema.json`：每個研究領域的本地來源索引格式。
- `schemas/source-crawl-queue.schema.json`：追加式候選來源佇列格式。
- `examples/research-request.example.json`：可直接複製修改的任務範例。
- `examples/report.example.json`：可通過基本一致性檢查的最小報告樣本。
- `prompts/research-agent.md`：可交給研究 agent 執行的標準提示。
- `prompts/document-curator-agent.md`：將單一來源整理成本地可重用摘要的提示。
- `scripts/validate_report.py`：不依賴外部套件的報告一致性檢查。
- `scripts/validate_crawl_queue.py`：檢查候選來源佇列編號、順序與回指關係。
- `scripts/backfill_source_metadata.py`：為既有 snapshot 回填 hash、freshness 與 GitHub 固定版本資訊。
- `scripts/research_pipeline.py`：執行本地優先研究工作流的 CLI。

## 使用方式

1. 依 `schemas/research-request.schema.json` 建立研究任務。
2. 優先查詢 `knowledge-base/topics/<topic_id>/` 的既有快照與摘要。
3. 本地資料不足或過期時，依 `docs/RESEARCH_WORKFLOW.md` 搜尋與擷取來源。
4. 使用 `prompts/document-curator-agent.md` 將新來源整理至本地研究資料庫。
5. 使用 `templates/report-template.md` 撰寫可閱讀版本。
6. 同步產生符合 `schemas/report.schema.json` 的結構化報告，供後續自動化檢查或再利用。
7. 執行 `python scripts/validate_report.py <report.json>` 檢查主張與來源引用是否一致。
8. 執行 `python scripts/validate_crawl_queue.py <crawl-queue.json>` 檢查來源佇列是否維持可追溯順序。
9. 舊資料升級時，執行 `python scripts/backfill_source_metadata.py <topic_id>` 回填來源 metadata。

## Pipeline CLI

```text
python scripts/research_pipeline.py status <topic_id>
python scripts/research_pipeline.py queue-add <topic_id> --type url --target <url> --reason <reason>
python scripts/research_pipeline.py collect-url <topic_id> <queue_id> --url <url> --title <title>
python scripts/research_pipeline.py local-search <topic_id> <query>
python scripts/research_pipeline.py draft-report <topic_id> --report-id <report_id>
python scripts/research_pipeline.py quality-check <topic_id> <report_id>
python scripts/research_pipeline.py curate-batch <topic_id> --input <reviewed-summaries.json>
python scripts/research_pipeline.py write-report <topic_id> --input <report.json>
python scripts/research_pipeline.py catalog <topic_id>
python scripts/backfill_source_metadata.py <topic_id>
```

CLI 產生的摘要與報告是初步草稿。發布前仍需由 agent 依快照內容覆核主張、限制與證據層級。

`structural_score` 代表機器契約與章節是否完整；`quality_score` 另依關鍵主張覆蓋、來源品質、雙向 backlinks、衝突處理、freshness 與可重現性計算。兩者不可混用。

Markdown 報告的來源章節採精簡導航格式。完整來源 metadata 保存在同名 JSON 報告，文件大綱與 snapshot 入口集中於 `knowledge-base/topics/<topic_id>/sources/CATALOG.md`。

原始網頁與 PDF snapshot 預設只保存在本機，不上傳 GitHub。Git 版控保留 URL、固定版本連結、SHA-256 hash、摘要與索引；需要跨機器共享 raw snapshot 時，應另外使用有權限控管的 artifact storage，並先確認再散布權限。

## 最小可信門檻

一份報告至少要：

- 清楚描述研究問題、範圍與資料截止時間。
- 讓每個關鍵主張都能追溯至來源。
- 區分事實、推論、建議與未知事項。
- 優先使用第一手來源，並揭露來源品質與利益衝突。
- 呈現重要反例、衝突證據與限制。
- 避免把缺乏證據寫成確定結論。
