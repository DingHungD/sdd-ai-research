# 本地研究資料庫

## 1. 目的

對同一領域反覆研究時，不需要每次重新搜尋與閱讀相同資料。來源第一次被發現後，應保存本地快照，交由文件整理 agent 建立摘要與 metadata。後續研究先查本地資料庫，只有在資料不足、需要最新資訊或來源已過期時才再次上網。

本地資料庫不是單純的書籤集合。它必須同時保存：

1. 原始來源的本地快照。
2. 可追溯的來源 metadata。
3. 由 agent 整理的結構化摘要。
4. 來源的新鮮度與重新檢查條件。

## 2. 目錄格式

每個研究領域使用一個穩定的 `topic_id`：

```text
knowledge-base/
  topics/
    <topic_id>/
      topic.json
      index.json
      crawl-queue.json
      crawl-queue.md
      sources/
        <source_id>/
          source.json
          raw/
            <downloaded files>
          summary.json
          summary.md
      reports/
        <generated reports>
```

以「根據 SDD 使用 AI 全自動開發」為例：

```text
knowledge-base/topics/sdd-ai-autonomous-development/
```

## 3. 檔案職責

| 檔案 | 用途 |
| --- | --- |
| `topic.json` | 定義領域、研究問題、關鍵字與更新策略 |
| `index.json` | 列出可搜尋來源、摘要路徑、分類、關鍵字與重新檢查日期 |
| `crawl-queue.json` | 規定 agent 依序處理的追加式候選來源佇列 |
| `crawl-queue.md` | 供人員閱讀與審查的佇列表格 |
| `source.json` | 保存來源 URL、版本、永久連結、快照路徑與品質資訊 |
| `raw/` | 保存 HTML、Markdown、PDF、程式碼或其他原始文件快照 |
| `summary.json` | 保存 agent 整理後的結構化內容 |
| `summary.md` | 供人員快速閱讀的摘要 |
| `reports/` | 保存使用這批來源產生的報告 |

## 4. 本地優先策略

研究 agent 執行新任務時：

1. 先比對 `topic_id`、關鍵字與既有摘要。
2. 使用本地 `summary.json` 篩選可能相關的來源。
3. 對重要主張回讀本地 `raw/` 快照，而不是只依賴摘要。
4. 檢查來源是否仍在有效期限內。
5. 只有在本地資料不足、來源過期或題目要求最新資訊時才上網。
6. 新來源與更新後的來源要重新進入整理流程。

初期使用 `index.json` 即可。當資料量增加到不適合逐筆掃描時，可在不改變來源目錄的情況下加入 SQLite FTS、向量索引或混合檢索；`raw/`、`source.json` 與 `summary.json` 仍作為可追溯的基礎資料。

需要上網時，依 `docs/SOURCE_CRAWL_QUEUE.md` 操作 `crawl-queue.json`。所有後續發現的 URL、查詢與資料缺口都追加至佇列尾端。

## 5. 新鮮度與更新

每個來源設定 `freshness`：

| 模式 | 使用時機 |
| --- | --- |
| `stable` | 定義文檔、固定版本規格、論文、已發布 PDF |
| `periodic` | 官方文件、README、工具清單、專案狀態 |
| `volatile` | 最新版本、issue 狀態、價格、排行榜、活躍度指標 |

`periodic` 與 `volatile` 來源需要設定 `recheck_after`。即使本地已有摘要，只要研究問題涉及「目前」、「最新」或近期變化，仍應重新確認。

更新時：

- 新快照不可覆蓋舊快照。
- `raw/` snapshot 預設只保存在本機，不直接提交至 GitHub；`source.json` 保留 URL、固定版本連結、SHA-256 hash 與本地路徑。
- 若團隊需要跨機器共享 snapshot，使用具權限控管的 artifact storage，並在散布前確認授權與保存政策。
- 同一來源的新版本沿用 `source_id`，另存新的 snapshot。
- 摘要需記錄依據的 snapshot。
- 新增或更新摘要後，同步更新 `index.json`。
- 若更新改變既有結論，報告 changelog 必須說明。

## 6. 文件整理 Agent 的責任

文件整理 agent 只處理單一來源，不直接寫跨來源結論。它需要：

- 判斷文件用途與來源類型。
- 摘要文件主要內容。
- 擷取可驗證的原子化重點。
- 保留重要章節、行號、頁碼或 anchor。
- 提供適合後續搜尋的關鍵字與實體。
- 揭露文件限制、版本與可能過期的部分。
- 產生符合 `schemas/document-summary.schema.json` 的 `summary.json`。

## 7. SDD 題目的建議分類

對「根據 SDD 使用 AI 全自動開發」，本地資料可先分成：

| 分類 | 內容 |
| --- | --- |
| `definition` | SDD 的定義、術語、方法論與原始提案 |
| `tooling` | 已有開源工具、官方文件、README、release note |
| `workflow` | 從 specification 到實作、測試、驗證的流程 |
| `evaluation` | 成功條件、限制、風險與可量測指標 |
| `case_study` | 實際案例、demo、技術文章與實驗結果 |
| `related_concepts` | agentic coding、spec-driven workflow、requirements engineering |

SDD 可能有多種定義。研究報告必須先列出採用的定義與來源，再比較工具是否真的符合該定義，避免只因工具宣稱支援 spec 就歸入同一類。
