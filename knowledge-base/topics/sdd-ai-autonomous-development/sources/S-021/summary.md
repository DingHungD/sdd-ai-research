# S-021

- 來源：[OpenAI Symphony Service Specification](https://github.com/openai/symphony/blob/main/SPEC.md)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T113910Z`

## Introduction

OpenAI Symphony service specification。scheduler、workspace manager、agent runner、retry、reconciliation、observability。關鍵技術包括：scheduler, retries, reconciliation, observability, policy boundaries。

## Ecosystem Role

OpenAI Symphony service specification

## Architecture Fit

位於 execution runtime 層，管理長時間 agent session、workspace、scheduler、retry 與 observability。

## Typical Workflow

1. 取得 issue 或 task
2. 建立隔離 workspace
3. 啟動 agent runtime
4. 監控 log 與狀態
5. 完成、retry 或 escalation

## Key Features

- scheduler、workspace manager、agent runner、retry、reconciliation、observability
- 架構層級：execution_runtime
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- scheduler
- retries
- reconciliation
- observability
- policy boundaries

## Best For

- execution_runtime
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OpenAI Symphony service specification 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- workspace 是否真正隔離？
- retry 是否具冪等性？
- log、成本、權限與錯誤是否可觀測？

## Key Points

- 服務規格包含 scheduler、workspace manager、agent runner 與 issue tracker client。 (`SPEC.md architecture`)
- 規格包含 retry、reconciliation 與 observability 行為。 (`SPEC.md lifecycle`)
- workspace isolation 與 policy boundary 是長時間執行的基礎。 (`SPEC.md workspace and policy sections`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- SPEC.md 描述理想服務行為；實際部署仍需安全控制。
