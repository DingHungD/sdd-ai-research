# S-023

- 來源：[Agent Skills Spec-Driven Development Skill](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113913Z`

## Introduction

Agent Skills SDD skill。clarify、plan、tasks、implementation、verification 與 human gate。關鍵技術包括：agent skill, verification, human approval。

## Ecosystem Role

Agent Skills SDD skill

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- clarify、plan、tasks、implementation、verification 與 human gate
- 架構層級：workflow_contract
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- agent skill
- verification
- human approval

## Best For

- workflow_contract
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Agent Skills SDD skill 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- skill 使用明確階段與人工 gate 管理 agent 行為。 (`SKILL.md workflow`)
- verification 是 implementation 後的必要步驟。 (`SKILL.md verification`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 這是操作指南，不是成效 benchmark。
