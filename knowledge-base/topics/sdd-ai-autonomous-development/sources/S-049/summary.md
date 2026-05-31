# S-049

- 來源：[OpenSpec Supported Tools Documentation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T121231Z`

## Introduction

OpenSpec supported tools。profiles、skills 與 tool-specific commands 的安裝方式。關鍵技術包括：skills delivery, command delivery, profiles, 30+ integrations。

## Ecosystem Role

OpenSpec supported tools

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- profiles、skills 與 tool-specific commands 的安裝方式
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- skills delivery
- command delivery
- profiles
- 30+ integrations

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OpenSpec supported tools 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- profiles、skills 與 tool-specific commands 的安裝方式 (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
