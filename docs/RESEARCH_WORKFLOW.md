# 可複用研究流程

## 1. 任務定義

輸入使用 `schemas/research-request.schema.json`。至少需要：

- `topic`：研究題目。
- `objective`：報告用途。
- `questions`：希望回答的問題。

其餘條件如時間範圍、地區、語言、來源偏好與排除條件可選填。

## 2. 流程

### Step 1：查詢本地研究資料庫

- 依題目、`topic_id`、關鍵字與既有摘要尋找相關來源。
- 對重要主張回讀本地原始快照。
- 檢查來源是否過期，以及題目是否要求最新資訊。
- 本地資料足夠且仍有效時，可略過網路搜尋。

輸出：可重用來源、需更新來源與資料缺口清單。

### Step 2：拆解題目

- 將題目拆成可驗證的子問題。
- 辨識需要最新資訊的項目，例如價格、法規、人物職務、產品規格或市場數據。
- 定義完成條件：回答哪些問題才算完成。

輸出：研究問題清單與查詢計畫。

### Step 3：搜尋與建立候選來源

- 讀取 `knowledge-base/topics/<topic_id>/crawl-queue.json`，依 `sequence` 由小到大處理。
- 初始佇列先排定定義、官方文件、repository、工具探索、限制與案例等搜尋順序。
- 優先搜尋第一手來源。
- 以不同措辭、語言與時間條件搜尋。
- 將值得擷取的搜尋結果追加到佇列尾端，不立即視為證據。
- 對新聞或時效性議題，區分發布日期與事件發生日期。
- 後續步驟若發現缺口或新的引用文件，將項目追加到尾端，記錄新增步驟與原因。
- 除非人工設定 `priority_override`，否則 agent 不可刪除、重編、插隊或跳過前方待處理項目。

輸出：符合 `schemas/source-crawl-queue.schema.json` 的追加式候選來源佇列。

### Step 4：擷取與正規化來源

- 開啟最終頁面或原始文件。
- 記錄 URL、作者、發布者、日期、擷取時間與來源類型。
- 對 GitHub、官方文件與其他持續更新頁面，優先保存永久連結、文件版本、tag、commit SHA、檔案路徑與行號。
- 將下載快照保存至 `knowledge-base/topics/<topic_id>/sources/<source_id>/raw/`。
- 保存快照與來源紀錄的 SHA-256 `content_hash`，並依來源類型設定 `freshness.mode` 與 `recheck_after`。
- 去除追蹤參數並處理重複網址。
- 將轉載與引用關係記錄為同一證據鏈。

輸出：符合 `schemas/source-record.schema.json` 的來源紀錄。

### Step 5：整理文件與評估來源

- 依 `docs/TRUSTED_REPORT_SPEC.md` 判斷證據層級。
- 記錄直接性、時效性、透明度、獨立性與利益衝突。
- 對無法讀取全文、缺乏日期或無法識別作者的來源降低權重。
- 使用 `prompts/document-curator-agent.md` 產生 `summary.json` 與 `summary.md`。

輸出：附品質註記的來源集合。

### Step 6：建立主張與證據表

- 將研究結果寫成原子化主張，一個主張表達一件可判斷的事。
- 對每個主張連結支持來源、反對來源與限制。
- 將每個主張的 `claim_id` 回填至來源的 `supported_claim_ids`，形成雙向 backlinks。
- 標記事實、推論、建議或未知。
- 對重要主張判斷可信度。

輸出：claim-evidence matrix。

### Step 7：處理衝突

- 判斷來源是否討論相同定義、時間點與範圍。
- 優先採用更直接、更新且方法透明的來源。
- 無法消除的衝突要保留，不可靜默挑選較方便的答案。
- 為每個衝突與未知事項建立 resolution item，標記 `resolved`、`partially_resolved` 或 `open`。
- 若需要補證據，將 PoC、benchmark、安全政策映射或決策會議加入後續 crawl queue 或實作 backlog。
- 每個未關閉項目都要寫出可驗證的 closure criteria。

輸出：衝突與未知事項清單，以及 resolution matrix。

### Step 8：撰寫報告

- 先寫關鍵發現，再補方法、限制與背景。
- 使用 `templates/report-template.md`。
- 同步產出符合 `schemas/report.schema.json` 的 JSON，讓後續工具能檢查或更新。
- Markdown 報告只保留來源摘要與導航連結；完整來源 metadata、摘要與 snapshot 放在獨立來源目錄及 JSON 報告中。

輸出：Markdown 報告與結構化 JSON 報告。

### Step 9：品質閘門

發布前執行：

1. 檢查所有 `critical` 主張是否有來源。
2. 檢查數字、日期與最新資訊是否附來源及擷取日期。
3. 檢查來源是否實際讀取，而非只來自搜尋摘要。
4. 檢查多個來源是否其實來自同一證據鏈。
5. 檢查是否揭露重大反例、衝突、限制與未知事項。
6. 檢查結論是否超出證據可支持的範圍。
7. 分別計算 `structural_score` 與 evidence-aware `quality_score`，不可把格式完整度當成研究品質。
8. 檢查主張到來源、來源回指主張的 backlinks 是否對稱。
9. 檢查持續更新的技術來源是否有固定版本，或至少保存本地 snapshot hash、重新檢查日期與無法重現限制。

## 3. 建議的自動化模組

後續實作可拆成：

| 模組 | 職責 |
| --- | --- |
| `request_parser` | 驗證與補全研究任務 |
| `query_planner` | 拆解子問題並產生查詢 |
| `crawl_queue` | 維護只追加的候選來源佇列與處理順序 |
| `source_collector` | 搜尋與擷取候選來源 |
| `source_normalizer` | 清理 URL、去重、建立證據鏈 |
| `snapshot_store` | 保存來源快照與版本 |
| `document_curator` | 整理單一文件並產生本地摘要 |
| `local_retriever` | 優先查詢本地快照與摘要 |
| `source_evaluator` | 評估來源品質與證據層級 |
| `claim_extractor` | 建立原子化主張 |
| `evidence_mapper` | 連結主張、支持證據與反對證據 |
| `report_writer` | 產生 Markdown 與 JSON 報告 |
| `quality_gate` | 檢查發布門檻與計算品質分數 |

## 4. 滾動式更新策略

- 每份報告保留 `report_id`、`version`、`generated_at` 與 `data_cutoff`。
- 更新時保留既有 `claim_id` 與 `source_id`，新增或標記失效，不任意重編。
- 對需要時效性的來源設定重新檢查日期。
- 新證據若改變核心結論，需在 changelog 說明原因。
