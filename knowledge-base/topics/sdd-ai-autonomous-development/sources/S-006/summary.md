# S-006

- 來源：[Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180v1)
- 類型：`research_paper`
- Snapshot：`SNAP-20260531T060539Z`

## Introduction

SDD 概念預印本。specification 為 source of truth；spec-first、spec-anchored、spec-as-source。關鍵技術包括：conceptual taxonomy, decision framework。

## Ecosystem Role

SDD 概念預印本

## Architecture Fit

位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。

## Typical Workflow

1. 確認輸入 artifact
2. 執行工具核心能力
3. 保存輸出與狀態
4. 交給下一層或人工覆核

## Key Features

- specification 為 source of truth
- spec-first、spec-anchored、spec-as-source
- 架構層級：research
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- conceptual taxonomy
- decision framework

## Best For

- research
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 SDD 概念預印本 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 此工具解決哪一層問題？
- 輸出是否可追溯與版本化？
- 失敗時是否有明確 escalation？

## Key Points

- 論文摘要將 SDD 定義為 specification 為 source of truth，code 為 generated or verified secondary artifact。 (`Abstract`)
- 論文摘要提出 spec-first、spec-anchored、spec-as-source 三種嚴謹程度。 (`Abstract`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 這是 2026-01-30 提交的 arXiv 預印本，不能當成已完成同行評審的共識。
