# S-039

- 來源：[snarktank Ralph Repository README](https://github.com/snarktank/ralph)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121218Z`

## Introduction

snarktank Ralph。PRD Markdown 轉 prd.json，逐 story 執行 checks、commit 與 progress log。關鍵技術包括：prd.json, story loop, typecheck, tests, commits。

## Ecosystem Role

snarktank Ralph

## Architecture Fit

位於 autonomous loop 層，透過 iteration memory、completion condition 與驗證讓 agent 連續工作。

## Typical Workflow

1. 載入 PRD、task 或 prompt
2. 執行單一 iteration
3. 跑檢查並保存 commit 或 progress
4. 判斷 completion condition
5. 未完成則進入下一輪或 escalation

## Key Features

- PRD Markdown 轉 prd.json，逐 story 執行 checks、commit 與 progress log
- 架構層級：autonomous_loop
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- prd.json
- story loop
- typecheck
- tests
- commits

## Best For

- autonomous_loop
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 snarktank Ralph 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 是否有 max iteration 與停止條件？
- 跨 iteration memory 保存在哪裡？
- 無法通過驗證時何時 escalation？

## Key Points

- PRD Markdown 轉 prd.json，逐 story 執行 checks、commit 與 progress log (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
