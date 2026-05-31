# S-019

- 來源：[Taskmaster Repository README](https://github.com/eyaltoledano/claude-task-master)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113907Z`

## Introduction

Taskmaster。PRD 轉 tasks、依賴與狀態管理，找出下一個可執行工作。關鍵技術包括：PRD parser, task graph, dependency tracking。

## Ecosystem Role

Taskmaster

## Architecture Fit

位於 task graph 層，將規格轉為可排序、可恢復、可平行執行的工作單位。

## Typical Workflow

1. 解析 PRD 或 specification
2. 建立 tasks 與 dependency
3. 找出 ready tasks
4. 交給 agent 執行
5. 更新狀態與下一個工作

## Key Features

- PRD 轉 tasks、依賴與狀態管理，找出下一個可執行工作
- 架構層級：task_graph
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- PRD parser
- task graph
- dependency tracking

## Best For

- task_graph
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Taskmaster 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- task 是否回指 requirement 與 acceptance criteria？
- 如何處理失敗、拆分與重試？
- 平行 task 的 merge 衝突如何避免？

## Key Points

- Taskmaster 將 PRD 拆為 task 並維護 dependency。 (`README overview`)
- agent 可依依賴關係取得下一個工作。 (`README workflow`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- Task graph 不等於 specification correctness。
