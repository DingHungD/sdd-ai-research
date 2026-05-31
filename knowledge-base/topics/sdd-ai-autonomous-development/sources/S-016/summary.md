# S-016

- 來源：[BMAD Method Repository README](https://github.com/bmad-code-org/BMAD-METHOD)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113903Z`

## Introduction

BMAD Method。依複雜度調整 planning depth；analysis、architecture、implementation 與專業 agent。關鍵技術包括：specialized agents, adaptive planning, modules。

## Ecosystem Role

BMAD Method

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- 依複雜度調整 planning depth
- analysis、architecture、implementation 與專業 agent
- 架構層級：lifecycle_workflow
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- specialized agents
- adaptive planning
- modules

## Best For

- lifecycle_workflow
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 BMAD Method 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- BMAD 依專案複雜度調整 planning depth。 (`README: Why the BMad Method?`)
- BMAD 提供 analysis、planning、architecture、implementation 的 structured workflow 與 specialized agents。 (`README: Why the BMad Method?`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 這是相鄰工具，不應直接歸類為純 SDD 實作。
