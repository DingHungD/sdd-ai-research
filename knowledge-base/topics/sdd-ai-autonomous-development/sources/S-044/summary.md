# S-044

- 來源：[workmux Repository README](https://github.com/raine/workmux)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121225Z`

## Introduction

workmux。以 worktree 與 tmux window 管理 coordinator 與 worker agents。關鍵技術包括：git worktree, tmux, coordinator, merge skills。

## Ecosystem Role

workmux

## Architecture Fit

位於 workspace isolation 層，讓多個 agent 可同時修改 code 而不互相污染。

## Typical Workflow

1. 為 task 建立 worktree
2. 啟動 agent 或 terminal session
3. 執行修改與檢查
4. review diff
5. 合併或丟棄 workspace

## Key Features

- 以 worktree 與 tmux window 管理 coordinator 與 worker agents
- 架構層級：workspace_isolation
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- git worktree
- tmux
- coordinator
- merge skills

## Best For

- workspace_isolation
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 workmux 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- worktree 生命週期如何管理？
- merge conflict 如何偵測與處理？
- 刪除 workspace 前是否保留 artifact？

## Key Points

- 以 worktree 與 tmux window 管理 coordinator 與 worker agents (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
