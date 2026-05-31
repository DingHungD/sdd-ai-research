# S-001

- 來源：[GitHub Spec Kit Documentation](https://github.github.com/spec-kit/index.html)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T060534Z`

## Introduction

GitHub Spec Kit 官方文件。Spec -> Plan -> Tasks -> Implement；模板、checklist、跨 artifact 分析。關鍵技術包括：Markdown artifacts, CLI scaffolding, multi-agent integrations。

## Ecosystem Role

GitHub Spec Kit 官方文件

## Architecture Fit

位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。

## Typical Workflow

1. 建立或匯入需求
2. 產生 specification 與 design
3. 拆解 tasks
4. 執行或交付 coding agent
5. 回寫驗證結果與 refinement

## Key Features

- Spec -> Plan -> Tasks -> Implement
- 模板、checklist、跨 artifact 分析
- 架構層級：direct_sdd
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Markdown artifacts
- CLI scaffolding
- multi-agent integrations

## Best For

- direct_sdd
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 GitHub Spec Kit 官方文件 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- artifact 是否可版本控制並支援差異比較？
- requirement、task、test 與 commit 是否能互相回指？
- 是否支援 approval、resume 與 brownfield 更新？

## Key Points

- Spec Kit 將 SDD 描述為把 specification 放在 AI 輔助軟體開發中心的方法。 (`raw HTML lines 78-78`)
- 首頁列出的核心流程是 Spec -> Plan -> Tasks -> Implement。 (`raw HTML lines 86-86`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
- 首頁是持續更新頁面，數量型資訊需要在引用前重新檢查。
