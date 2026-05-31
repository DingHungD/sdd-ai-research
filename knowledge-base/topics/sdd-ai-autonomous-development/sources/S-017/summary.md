# S-017

- 來源：[Get Shit Done Repository README](https://github.com/gsd-build/get-shit-done)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113904Z`

## Introduction

Get Shit Done。分階段 planning artifact、fresh subagent 與驗證，降低 context rot。關鍵技術包括：phase plans, fresh agents, verification。

## Ecosystem Role

Get Shit Done

## Architecture Fit

位於 repository context 層，降低 agent 對大型或既有 codebase 理解不足的風險。

## Typical Workflow

1. 掃描 repository
2. 建立結構或語意索引
3. 選取與 task 相關 context
4. 提供 agent 執行
5. 依變更更新索引

## Key Features

- 分階段 planning artifact、fresh subagent 與驗證，降低 context rot
- 架構層級：context_engineering
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- phase plans
- fresh agents
- verification

## Best For

- context_engineering
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Get Shit Done 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 大型 repository 的索引成本是多少？
- context 選取錯誤如何偵測？
- 索引是否能與 requirement traceability 結合？

## Key Points

- GSD 以分階段 artifact 與 fresh subagent 控制 context 品質。 (`README overview`)
- 執行與驗證被拆為可重複步驟。 (`README workflow`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 這是相鄰工具，不是 specification schema 標準。
