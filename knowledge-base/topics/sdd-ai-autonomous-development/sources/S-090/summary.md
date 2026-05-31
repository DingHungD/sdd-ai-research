# S-090

- 來源：[OPA Pull Request Check Policies](https://www.openpolicyagent.org/docs/cicd/pr-checks)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T135911Z`

## Introduction

OPA PR Check Policies。依 changed files 決定 PR 必跑 checks，policy 可 version、review、test 並形成 audit trail。關鍵技術包括：Rego, pull request checks, audit trail, GitHub Actions。

## Ecosystem Role

OPA PR Check Policies

## Architecture Fit

位於 policy gate 層，將組織、安全與部署規則寫成可版本控制、可測試、可稽核的機器判斷。

## Typical Workflow

1. 將 artifact 轉為結構化輸入
2. 以 declarative policy 評估
3. 在 PR 或 CI 阻擋違規
4. 保存 policy decision 與 audit trail
5. 例外進入人工審批

## Key Features

- 依 changed files 決定 PR 必跑 checks，policy 可 version、review、test 並形成 audit trail
- 架構層級：policy_as_code
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- Rego
- pull request checks
- audit trail
- GitHub Actions

## Best For

- policy_as_code
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OPA PR Check Policies 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- policy 是否版本化與可測試？
- 違規是否阻擋 merge 或 deploy？
- 例外流程是否留下 audit trail？

## Key Points

- 依 changed files 決定 PR 必跑 checks，policy 可 version、review、test 並形成 audit trail (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
