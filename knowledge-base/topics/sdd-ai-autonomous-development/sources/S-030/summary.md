# S-030

- 來源：[Specboot ai-specs Repository README](https://github.com/LIDR-academy/lidr-specboot)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121208Z`

## Introduction

Specboot ai-specs。可攜式 coding standards、agent role、skills 與 OpenSpec augmentation。關鍵技術包括：AGENTS.md, CLAUDE.md, standards, skills, OpenAPI。

## Ecosystem Role

Specboot ai-specs

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- 可攜式 coding standards、agent role、skills 與 OpenSpec augmentation
- 架構層級：governance
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- AGENTS.md
- CLAUDE.md
- standards
- skills
- OpenAPI

## Best For

- governance
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Specboot ai-specs 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- 可攜式 coding standards、agent role、skills 與 OpenSpec augmentation (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
