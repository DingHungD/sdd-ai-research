# 自動化 Pipeline

## 1. 執行入口

```text
python scripts/research_pipeline.py <command>
```

## 2. 模組對應

| 模組 | 實作 | 用途 |
| --- | --- | --- |
| `request_parser` | `research_pipeline/request_parser.py` | 驗證與補全研究請求 |
| `query_planner` | `research_pipeline/query_planner.py` | 建立研究問題計畫 |
| `crawl_queue` | `research_pipeline/crawl_queue.py` | 維護只追加佇列與 Markdown 表格 |
| `source_collector` | `research_pipeline/source_collector.py` | 下載 URL |
| `source_normalizer` | `research_pipeline/source_normalizer.py` | 清理 URL 與追蹤參數 |
| `snapshot_store` | `research_pipeline/snapshot_store.py` | 保存 snapshot 與 SHA-256 |
| `source_metadata` | `research_pipeline/source_metadata.py` | 回填 hash、freshness 與 GitHub commit permalink |
| `document_curator` | `research_pipeline/document_curator.py` | 建立初步摘要並保存 agent 覆核摘要 |
| `local_retriever` | `research_pipeline/local_retriever.py` | 依索引搜尋本地來源 |
| `source_evaluator` | `research_pipeline/source_evaluator.py` | 產生初步來源評級 |
| `claim_extractor` | `research_pipeline/claim_extractor.py` | 從覆核摘要建立主張草稿 |
| `evidence_mapper` | `research_pipeline/evidence_mapper.py` | 配置穩定主張 ID |
| `report_writer` | `research_pipeline/report_writer.py` | 同步雙向 backlinks，產生 JSON 與 Markdown 報告 |
| `quality_gate` | `research_pipeline/quality_gate.py` | 計算 evidence-aware 品質分數與結構完整度 |

## 3. 工作流

1. 以 `status` 取得下一筆候選來源。
2. 搜尋項目由 agent 執行，值得保存的 URL 使用 `queue-add` 追加。
3. URL 項目使用 `collect-url` 下載、正規化、保存 snapshot、建立初步摘要並更新索引。
4. agent 讀取 snapshot，產生覆核摘要批次檔。
5. 使用 `curate-batch` 保存覆核摘要與索引。
6. 使用 `local-search` 重用既有來源。
7. 舊資料升級時，使用 `python scripts/backfill_source_metadata.py <topic_id>` 回填來源 metadata。
8. agent 建立 synthesis JSON，使用 `write-report` 同步 backlinks 並輸出報告。
9. 使用 `quality-check`、`validate_report.py` 與 `validate_crawl_queue.py` 執行品質檢查。

## 4. 邊界

- `source_evaluator` 與初步摘要是 heuristic，不可直接當成發布品質。
- `structural_score` 只代表必要章節與機器契約完整；研究可信度以 `quality_score` 與各面向分數判讀。
- 技術內容、衝突證據、證據層級與建議仍需要 agent 覆核。
- 網路搜尋結果摘要只能用於發現 URL，正式報告引用本地 snapshot 對應的原始 URL。
