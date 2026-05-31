# S-055

- 來源：[Threatspec Repository README](https://github.com/threatspec/threatspec)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121238Z`

## Introduction

Threatspec。在 source code annotations 中保存 threat model，產生報告與 data-flow diagrams。關鍵技術包括：security annotations, threat model, DFD, CI/CD integration。

## Ecosystem Role

Threatspec

## Architecture Fit

位於 governance 與 security 層，將安全要求、threat model 與政策檢查加入交付鏈。

## Typical Workflow

1. 定義 security constraints
2. 將限制映射到 code 或 spec
3. 執行分析與驗證
4. 產生報告
5. 阻擋或升級違規變更

## Key Features

- 在 source code annotations 中保存 threat model，產生報告與 data-flow diagrams
- 架構層級：security
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- security annotations
- threat model
- DFD
- CI/CD integration

## Best For

- security
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Threatspec 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 安全規格是否可機器驗證？
- policy violation 是否阻擋 merge？
- threat model 是否隨 code 變更更新？

## Key Points

- 在 source code annotations 中保存 threat model，產生報告與 data-flow diagrams (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
