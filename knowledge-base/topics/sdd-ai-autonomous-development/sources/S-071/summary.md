# S-071

- 來源：[Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T134003Z`

## Introduction

Anthropic：Effective Context Engineering。官方指南聚焦長時間 agent 的 context 管理、compression、memory 與工具設計。關鍵技術包括：Anthropic, context engineering, compression, memory, tools。

## Ecosystem Role

Anthropic：Effective Context Engineering

## Architecture Fit

位於方法論與採用經驗層，用來補足工具文件未涵蓋的實作觀點、 trade-off 與導入風險。

## Typical Workflow

1. 辨識文章主張與適用範圍
2. 拆分直接事實、作者觀點與案例
3. 對照官方工具文件
4. 保留可驗證的 adoption insight
5. 將未驗證主張標記為限制

## Key Features

- 官方指南聚焦長時間 agent 的 context 管理、compression、memory 與工具設計
- 架構層級：article
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Anthropic
- context engineering
- compression
- memory
- tools

## Best For

- article
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Anthropic：Effective Context Engineering 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 作者是否為官方或具編輯審查來源？
- 文章主張是否有案例或數據支持？
- 哪些結論只能作為採用假設？

## Key Points

- 官方指南聚焦長時間 agent 的 context 管理、compression、memory 與工具設計 (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
