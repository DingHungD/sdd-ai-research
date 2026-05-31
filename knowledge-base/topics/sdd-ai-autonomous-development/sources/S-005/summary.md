# S-005

- 來源：[Spec Kitty Repository README](https://github.com/Priivacy-ai/spec-kitty)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T060538Z`

## Introduction

Spec Kitty CLI。spec、plan、tasks、review、accept、merge；work package 與 git worktree。關鍵技術包括：repository-native artifacts, work packages, git worktrees, auto-merge。

## Ecosystem Role

Spec Kitty CLI

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- spec、plan、tasks、review、accept、merge
- work package 與 git worktree
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- repository-native artifacts
- work packages
- git worktrees
- auto-merge

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Spec Kitty CLI 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- Spec Kitty 的核心流程包含 review、accept 與 merge，而不只生成 code。 (`README overview`)
- Spec Kitty 使用 repository-native artifacts、work packages 與 git worktrees。 (`#what-it-provides`)

## Limitations

- README 是專案自述；需要另行評估成熟度、測試覆蓋與維護狀態。
- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
