# S-072

- 來源：[Scale AI: SWE Atlas is Complete](https://scale.com/blog/swe-atlas-complete)
- 類型：`professional_article`
- Snapshot：`SNAP-20260531T134005Z`

## Introduction

Scale AI：SWE Atlas。擴充 software engineering benchmark 到 bug investigation、validation 與 codebase maintenance。關鍵技術包括：SWE Atlas, benchmark, validation, maintenance, investigation。

## Ecosystem Role

Scale AI：SWE Atlas

## Architecture Fit

位於評估層，用來約束對 coding agent、context retrieval 與長時間自動開發能力的宣稱。

## Typical Workflow

1. 確認 benchmark 任務分布
2. 檢查資料品質與污染風險
3. 辨識評估指標
4. 比較 agent 行為
5. 將限制回饋到系統 gate

## Key Features

- 擴充 software engineering benchmark 到 bug investigation、validation 與 codebase maintenance
- 架構層級：benchmark
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- SWE Atlas
- benchmark
- validation
- maintenance
- investigation

## Best For

- benchmark
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Scale AI：SWE Atlas 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- benchmark 是否覆蓋真實 software engineering 工作？
- 是否只測 patch generation？
- 是否揭露 context retrieval、驗證與維護任務？

## Key Points

- 擴充 software engineering benchmark 到 bug investigation、validation 與 codebase maintenance (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
