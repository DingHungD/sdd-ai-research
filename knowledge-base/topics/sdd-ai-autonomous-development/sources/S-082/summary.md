# S-082

- 來源：[NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T135904Z`

## Introduction

NASA Requirements Management。管理 requirement baseline、change board、stakeholder expectation、design、test 與 V&V results。關鍵技術包括：baseline management, change control board, requirement database, V&V mapping。

## Ecosystem Role

NASA Requirements Management

## Architecture Fit

位於 requirements assurance 層，要求需求、設計、code、test、hazard 與 non-conformance 可雙向追溯。

## Typical Workflow

1. 為 requirement 配置唯一 ID
2. 將 requirement 映射到 design
3. 將 design 映射到 code
4. 將 requirement 映射到 verification
5. 檢查 orphan、extra 與變更影響

## Key Features

- 管理 requirement baseline、change board、stakeholder expectation、design、test 與 V&V results
- 架構層級：traceability
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- baseline management
- change control board
- requirement database
- V&V mapping

## Best For

- traceability
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 NASA Requirements Management 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 是否能雙向追溯？
- 是否偵測 orphan design、extra code 與未驗證 requirement？
- baseline 變更是否經審批並更新 matrix？

## Key Points

- 管理 requirement baseline、change board、stakeholder expectation、design、test 與 V&V results (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
