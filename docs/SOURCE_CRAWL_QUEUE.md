# 候選來源爬取佇列

## 1. 目的

Step 3 使用一份可追溯、只追加的候選來源佇列。它規定 agent 的爬取順序，也保留後續研究步驟發現新資料需求時的擴充紀錄。

佇列同時保存：

- `crawl-queue.json`：供 agent 執行與程式檢查。
- `crawl-queue.md`：供人員閱讀與審查。

## 2. 核心規則

1. agent 依 `queue_id` 由小到大處理。
2. 既有項目不可刪除、重編或插隊。
3. 後續步驟發現資料缺口時，將新項目追加至尾端。
4. 追加項目必須記錄 `added_by_step`、`reason` 與 `related_question_ids`。
5. 項目完成、失敗或略過時更新 `status`，但保留原始項目。
6. 搜尋結果中值得保存的具體 URL 也追加至尾端，不直接繞過佇列擷取。
7. 只有人工明確標記 `priority_override` 時，agent 才能優先處理較後面的項目；原始順序仍保留。

## 3. 建議的初始順序

對技術研究，初始清單通常依下列順序建立：

| 順序 | 目標 | 原因 |
| ---: | --- | --- |
| 1 | 定義與原始提案 | 先確定術語，避免工具比較失焦 |
| 2 | 官方文件 | 取得可直接驗證的能力與限制 |
| 3 | 官方 GitHub repository | 保存 README、程式碼、release 與 tag |
| 4 | 開源工具探索 | 尋找其他候選工具 |
| 5 | issue、discussion、PR | 補充限制、爭議與尚未完成的功能 |
| 6 | 案例與評估資料 | 驗證實際效果與風險 |

## 4. 欄位說明

| 欄位 | 用途 |
| --- | --- |
| `queue_id` | 穩定且遞增的項目編號，例如 `Q-001` |
| `sequence` | 建立時的順序，後續不可修改 |
| `target_type` | `search_query`、`url`、`domain_seed` 或 `local_gap` |
| `target` | 搜尋字串、URL、domain 或待補資料描述 |
| `reason` | 為何需要爬取 |
| `related_question_ids` | 對應的研究問題 |
| `added_by_step` | 初始規劃或哪一個後續步驟新增 |
| `status` | `pending`、`in_progress`、`completed`、`failed` 或 `skipped` |
| `discovered_from` | 若由另一個佇列項目發現，記錄其 `queue_id` |
| `result_source_ids` | 完成後產生的本地來源 |
| `notes` | 失敗原因、略過理由或其他備註 |

## 5. 追加範例

假設整理工具 README 時，發現文件引用一份 architecture specification：

1. 保留目前項目的完成狀態。
2. 在佇列尾端新增一筆 `url` 項目。
3. 設定 `added_by_step` 為 `step_5_document_curation`。
4. 將 `discovered_from` 指向目前處理中的項目。
5. agent 完成前方尚未處理的項目後，再處理新增項目。

