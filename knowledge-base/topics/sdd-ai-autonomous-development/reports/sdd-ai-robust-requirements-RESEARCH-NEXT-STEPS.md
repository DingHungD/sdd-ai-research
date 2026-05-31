# SDD AI 穩健需求研究補強判斷

## 結論

目前不需要再無差別擴充網路文章。現有 `97` 筆來源已涵蓋 SDD 定義、開源工具、requirements traceability、brownfield context、drift、security policy-as-code、runtime orchestration、benchmark 與研究原型，足以建立第一版 assurance architecture 與 PoC backlog。

繼續增加一般介紹文章的邊際效益已低。下一階段應把研究資源放在可重現實驗、組織政策核准與目標 repository 的實測。

截至本次審查，既有 `periodic` 來源尚未到達重新檢查日期，append-only crawl queue 也沒有待處理項目。因此目前不新增一般網路搜尋。

## 必要補強

| 優先級 | 項目 | 類型 | 原因 | 完成條件 |
| ---: | --- | --- | --- | --- |
| 1 | 不同工具組合的穩健性比較 | Benchmark | 文件只能建立候選架構，不能證明哪一組最適合組織環境 | 在相同 fixtures 上重複測試前三種組合，保存版本、權限、人工介入與量測結果 |
| 2 | Brownfield context graph 與 drift gate | PoC | 現有資料證明路徑存在，但沒有目標 repository 的 precision、recall 與維護成本 | 在至少一個真實 repository 完成人工標註驗證與成本量測 |
| 3 | 安全政策自動化邊界 | Policy review | 官方標準足以建立 baseline，但組織風險偏好、例外核准人與 deploy gate 門檻仍未核准 | 產出版本化 control catalog、Rego policy pack、例外流程與安全 owner 核准紀錄 |
| 4 | R2Code 與 ReqToCode 實務適用性 | Reproduction experiment | 兩者仍是新興研究方向，不足以直接納入 production baseline | 在大型 repository 獨立重現並揭露 precision、recall、F1、成本與失敗模式 |

## 追加網路研究條件

僅在下列情況追加網路搜尋：

1. 既有 `periodic` 或 `volatile` 來源到達 `recheck_after`，且新報告仍依賴其目前狀態。
2. PoC 發現現有工具無法覆蓋必要能力，需要尋找替代工具或特定實作文件。
3. NIST、OWASP、CISA 或組織採用的安全標準發布新版本。
4. benchmark 或 reproduction experiment 出現無法由現有文件解釋的失敗模式。

## 導航

- [v11 主報告](sdd-ai-robust-requirements-20260531-v11.md)
- [來源總目錄](../sources/CATALOG.md)
- [候選來源佇列](../crawl-queue.md)
