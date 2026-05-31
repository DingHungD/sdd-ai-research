# S-086

- 來源：[OWASP AISVS](https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/)
- 類型：`official_documentation`
- Snapshot：`SNAP-20260531T135907Z`

## Introduction

OWASP AISVS。提供 AI-enabled system 可測試、可實作的安全 requirements catalogue。關鍵技術包括：AISVS, AI security requirements, CI/CD, assessment。

## Ecosystem Role

OWASP AISVS

## Architecture Fit

位於 assurance framework 層，提供安全開發實務、驗證控制、風險等級與持續改善基準。

## Typical Workflow

1. 選擇適用控制
2. 將控制映射到需求與流程
3. 在 pipeline 蒐集 evidence
4. 執行自動與人工驗證
5. 持續改善並回應殘餘風險

## Key Features

- 提供 AI-enabled system 可測試、可實作的安全 requirements catalogue
- 架構層級：assurance
- 輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。

## Key Technologies

- AISVS
- AI security requirements
- CI/CD
- assessment

## Best For

- assurance
- 快速判斷此工具在整體 SDD 架構中的責任
- 作為試點工具選型與後續深挖入口

## Research Value

此來源用於理解 OWASP AISVS 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。

## Verification Questions

- 控制是否 outcome-based 且可提供 evidence？
- 哪些控制可自動驗證？
- 高 assurance 情境是否需要獨立覆核？

## Key Points

- 提供 AI-enabled system 可測試、可實作的安全 requirements catalogue (`README or official documentation overview`)

## Limitations

- Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。
