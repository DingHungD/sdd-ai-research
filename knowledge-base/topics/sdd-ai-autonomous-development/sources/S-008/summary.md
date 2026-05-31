# S-008

- 來源：[SpecDD Official Documentation](https://specdd.ai/)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T060635Z`

## Introduction

SpecDD framework。以 `.sdd` 檔案保存 intent、architecture、behavior、boundary、task。關鍵技術包括：.sdd files, colocated specs, incremental adoption。

## Ecosystem Role

SpecDD framework

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- 以 `.sdd` 檔案保存 intent、architecture、behavior、boundary、task
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- .sdd files
- colocated specs
- incremental adoption

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 SpecDD framework 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- SpecDD 使用本地且人可讀的 `.sdd` 檔案作為 humans 與 AI agents 的 shared source of truth。 (`#specdd`)
- SpecDD 文件表示可用於 greenfield，也可在既有專案逐步導入。 (`#specdd`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 官方文件是專案自述；需另行檢查 CLI、repository 與實際採用案例。
