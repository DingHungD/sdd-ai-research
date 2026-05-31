# S-011

- 來源：[codex-spec Repository README](https://github.com/shenli/codex-spec)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T113856Z`

## Introduction

codex-spec。context、spec、requirements、design、development plan、implementation、validation。關鍵技術包括：Codex commands, dependency-aware tasks, context refresh。

## Ecosystem Role

codex-spec

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- context、spec、requirements、design、development plan、implementation、validation
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Codex commands
- dependency-aware tasks
- context refresh

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 codex-spec 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- codex-spec 將需求、設計、開發計畫與實作拆成顯式階段。 (`README overview`)
- 工作流以版本化 artifact 提供 agent 上下文。 (`README workflow`)

## Limitations

- Repository README 可證明設計，不足以證明實際交付品質。
- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
