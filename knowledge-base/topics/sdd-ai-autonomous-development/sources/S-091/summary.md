# S-091

- 來源：[Conftest Documentation](https://www.conftest.dev/)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T135912Z`

## Introduction

Conftest。使用 Rego 對 Kubernetes、Terraform、pipeline 與其他 structured configuration 執行測試。關鍵技術包括：Conftest, Rego, Kubernetes, Terraform, configuration testing。

## Ecosystem Role

Conftest

## Architecture Fit

位於 policy gate 層，將組織、安全與部署規則寫成可版本控制、可測試、可稽核的機器判斷。

## Typical Workflow

1. 將 artifact 轉為結構化輸入
2. 以 declarative policy 評估
3. 在 PR 或 CI 阻擋違規
4. 保存 policy decision 與 audit trail
5. 例外進入人工審批

## Key Features

- 使用 Rego 對 Kubernetes、Terraform、pipeline 與其他 structured configuration 執行測試
- 架構層級：policy_as_code
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Conftest
- Rego
- Kubernetes
- Terraform
- configuration testing

## Best For

- policy_as_code
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 Conftest 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- policy 是否版本化與可測試？
- 違規是否阻擋 merge 或 deploy？
- 例外流程是否留下 audit trail？

## Key Points

- 使用 Rego 對 Kubernetes、Terraform、pipeline 與其他 structured configuration 執行測試 (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
