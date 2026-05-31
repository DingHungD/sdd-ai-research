# S-004

- 來源：[OpenSpec Repository README](https://github.com/Fission-AI/OpenSpec)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T060537Z`

## Introduction

OpenSpec 核心工具。change folder 內保存 proposal、specs、design、tasks；brownfield-first。關鍵技術包括：change folders, living specs, local CLI, profiles。

## Ecosystem Role

OpenSpec 核心工具

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- change folder 內保存 proposal、specs、design、tasks
- brownfield-first
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- change folders
- living specs
- local CLI
- profiles

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OpenSpec 核心工具 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- OpenSpec 在 code 前加入 spec layer，讓 human 與 AI 對齊。 (`#why-openspec`)
- OpenSpec 將 change 分資料夾保存 proposal、specs、design 與 tasks。 (`#why-openspec`)

## Limitations

- README 是專案自述；需要另行測試其可靠性與維護品質。
- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
