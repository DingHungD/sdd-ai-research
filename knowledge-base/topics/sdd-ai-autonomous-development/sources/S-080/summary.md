# S-080

- 來源：[NASA SWE-052 Bidirectional Traceability](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052+-+Bidirectional+Traceability)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T135859Z`

## Introduction

NASA SWE-052。要求 higher-level requirements、software requirements、hazards、design、code、verification 與 non-conformance 雙向追溯。關鍵技術包括：end-to-end traceability, hazards, verification, non-conformance。

## Ecosystem Role

NASA SWE-052

## Architecture Fit

位於 requirements assurance 層，要求需求、設計、code、test、hazard 與 non-conformance 可雙向追溯。

## Typical Workflow

1. 為 requirement 配置唯一 ID
2. 將 requirement 映射到 design
3. 將 design 映射到 code
4. 將 requirement 映射到 verification
5. 檢查 orphan、extra 與變更影響

## Key Features

- 要求 higher-level requirements、software requirements、hazards、design、code、verification 與 non-conformance 雙向追溯
- 架構層級：traceability
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- end-to-end traceability
- hazards
- verification
- non-conformance

## Best For

- traceability
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 NASA SWE-052 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 是否能雙向追溯？
- 是否偵測 orphan design、extra code 與未驗證 requirement？
- baseline 變更是否經審批並更新 matrix？

## Key Points

- 要求 higher-level requirements、software requirements、hazards、design、code、verification 與 non-conformance 雙向追溯 (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
