# S-031

- 來源：[Gentle-AI Repository README](https://github.com/Gentleman-Programming/gentle-ai)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121209Z`

## Introduction

Gentle-AI。為 coding agent 配置 memory、SDD workflow、skills、MCP、permission 與 per-phase model routing。關鍵技術包括：persistent memory, MCP, model routing, permissions。

## Ecosystem Role

Gentle-AI

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- 為 coding agent 配置 memory、SDD workflow、skills、MCP、permission 與 per-phase model routing
- 架構層級：harness_engineering
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- persistent memory
- MCP
- model routing
- permissions

## Best For

- harness_engineering
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Gentle-AI 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- 為 coding agent 配置 memory、SDD workflow、skills、MCP、permission 與 per-phase model routing (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
