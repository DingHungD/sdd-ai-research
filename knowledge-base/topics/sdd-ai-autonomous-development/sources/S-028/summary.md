# S-028

- 來源：[MoAI-ADK Repository README](https://github.com/modu-ai/moai-adk)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121205Z`

## Introduction

MoAI-ADK。SPEC-first harness；TDD/DDD、自我驗證 loop、code maps、progress persistence、agent teams。關鍵技術包括：Go CLI, TDD, DDD, LSP, AST-grep, worktrees, metrics。

## Ecosystem Role

MoAI-ADK

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- SPEC-first harness
- TDD/DDD、自我驗證 loop、code maps、progress persistence、agent teams
- 架構層級：harness_engineering
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Go CLI
- TDD
- DDD
- LSP
- AST-grep
- worktrees
- metrics

## Best For

- harness_engineering
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 MoAI-ADK 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- SPEC-first harness；TDD/DDD、自我驗證 loop、code maps、progress persistence、agent teams (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
