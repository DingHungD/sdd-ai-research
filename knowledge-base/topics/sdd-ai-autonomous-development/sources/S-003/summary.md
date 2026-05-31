# S-003

- 來源：[Kiro Specs Documentation](https://kiro.dev/docs/specs/)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T060535Z`

## Introduction

Kiro 官方 Specs。requirements.md、design.md、tasks.md；task dependency 與平行執行。關鍵技術包括：structured specs, dependency graph, agent hooks, steering, MCP。

## Ecosystem Role

Kiro 官方 Specs

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- requirements.md、design.md、tasks.md
- task dependency 與平行執行
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- structured specs
- dependency graph
- agent hooks
- steering
- MCP

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Kiro 官方 Specs 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- Kiro spec 由 requirements 或 bugfix、design、tasks 三類檔案構成。 (`#core-structure`)
- Kiro 可分析 tasks.md 的依賴並平行執行獨立任務。 (`#running-tasks-in-parallel`)

## Limitations

- Kiro 是產品官方文件，不是開源工具證據；功能效果仍需實際測試。
- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
