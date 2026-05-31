# S-020

- 來源：[OpenAI Symphony Repository README](https://github.com/openai/symphony)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113908Z`

## Introduction

OpenAI Symphony repository。issue tracker 驅動的隔離 coding-agent 執行原型。關鍵技術包括：issue tracker, isolated workspace, parallel runs。

## Ecosystem Role

OpenAI Symphony repository

## Architecture Fit

位於 execution runtime 層，管理長時間 agent session、workspace、scheduler、retry 與 observability。

## Typical Workflow

1. 取得 issue 或 task
2. 建立隔離 workspace
3. 啟動 agent runtime
4. 監控 log 與狀態
5. 完成、retry 或 escalation

## Key Features

- issue tracker 驅動的隔離 coding-agent 執行原型
- 架構層級：execution_runtime
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- issue tracker
- isolated workspace
- parallel runs

## Best For

- execution_runtime
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OpenAI Symphony repository 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- workspace 是否真正隔離？
- retry 是否具冪等性？
- log、成本、權限與錯誤是否可觀測？

## Key Points

- Symphony 將 issue tracker 工作交給 coding agent 執行。 (`README overview`)
- 每個工作使用隔離 workspace，並支援並行執行。 (`README overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- Symphony repository 明確定位為 engineering prototype；不是安全強化平台。
