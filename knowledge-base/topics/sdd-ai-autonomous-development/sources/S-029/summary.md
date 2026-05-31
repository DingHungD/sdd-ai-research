# S-029

- 來源：[OpenLore Repository README](https://github.com/clay-good/OpenLore)
- 類型：`repository_file`
- Snapshot：`SNAP-20260531T121206Z`

## Introduction

OpenLore。以 static analysis 建立可查詢 knowledge graph，結合 living specs、drift detection、graph-native MCP tools 與 CI staleness gate。關鍵技術包括：knowledge graph, call graph, SQLite, graph-native MCP, semantic retrieval, drift detection, SCIP export, CI preflight。

## Ecosystem Role

OpenLore

## Architecture Fit

位於 brownfield reverse-engineering 層，從既有 code 產生或更新 living specification。

## Typical Workflow

1. 執行 static analysis
2. 建立 dependency 與 call graph
3. 識別 domain clusters
4. 由 LLM 補充語意
5. 輸出 living specs 與 drift 指標

## Key Features

- 以 static analysis 建立可查詢 knowledge graph，結合 living specs、drift detection、graph-native MCP tools 與 CI staleness gate
- 架構層級：brownfield
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- knowledge graph
- call graph
- SQLite
- graph-native MCP
- semantic retrieval
- drift detection
- SCIP export
- CI preflight

## Best For

- brownfield
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OpenLore 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 產生規格的準確率如何驗證？
- spec-code drift 是否可持續監控？
- 未覆蓋的 code path 如何揭露？

## Key Points

- 以 static analysis 與 LLM 反向產生 living OpenSpec，追蹤 spec test coverage 與 drift (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
