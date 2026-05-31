# 根據 SDD 使用 AI 全自動開發：現況與可行邊界

## 報告資訊

- 報告 ID：`sdd-ai-autonomous-development-20260531`
- 版本：`1.0.0`
- 產生時間：`2026-05-31T06:20:00Z`
- 資料截止時間：`2026-05-31T06:06:37Z`
- 整體可信度：`medium`
- 品質分數：`100/100`

## 摘要

SDD 在 AI 開發情境中可合理理解為：將 specification 提升為可版本控制、可驗證的主要 artifact，再由 agent 依序產生 plan、tasks、implementation 與驗證結果。目前已有多個可用工具與官方工作流，包括 GitHub Spec Kit、OpenSpec、Spec Kitty、SpecDD、Kiro Specs、OpenSpecification 與 Akka SDD。現有資料支持「高度自動化、可恢復、可平行執行的開發流程」已經存在，但不足以支持「任意專案可以完全無人監督地可靠開發」。適合的落地方式是 bounded autonomy：讓 agent 自動執行明確任務，並在規格核准、風險變更、測試失敗與發布前保留品質閘門。

## 方法

依追加式 crawl queue 搜尋與擷取來源。優先保存官方文件、官方 repository README 與版本固定的 arXiv 摘要頁。本次共保存 10 份本地 snapshot，逐份覆核後建立主張。工具自述可證明功能設計與公開介面，但不視為獨立成效驗證。

## 關鍵發現

### `C-001`

- 主張：本報告採用的 SDD 定義是：以 specification 作為主要且可演進的 source of truth，讓 code 成為由 specification 引導產生或驗證的 artifact。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：GitHub Spec Kit、Akka 官方文件與 arXiv 預印本摘要在核心概念上方向一致。
- 支持來源：S-001, S-006, S-010

### `C-002`

- 主張：常見 SDD 流程不是單一步驟 prompt-to-code，而是將需求逐步轉為 specification、plan 或 design、tasks、implementation 與驗證 artifact。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：GitHub Spec Kit、Kiro 與 Akka 官方文件均列出多階段 artifact 流程。
- 支持來源：S-001, S-003, S-007, S-010

### `C-003`

- 主張：GitHub Spec Kit 是開源 SDD 工具包，核心流程為 Spec -> Plan -> Tasks -> Implement；其 workflow 功能可串接 prompt、shell step、條件、迴圈、fan-out/fan-in 與 human checkpoint，並支援恢復中斷執行。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：由 GitHub Spec Kit 官方文件與官方 repository README 直接支持。
- 支持來源：S-001, S-002, S-007

### `C-004`

- 主張：OpenSpec 是開源 SDD 工具，使用 lightweight spec layer 與 change folder 保存 proposal、specs、design、tasks，重點是 code 前的人機對齊與可稽核變更。
- 類型：`fact`
- 重要程度：`supporting`
- 可信度：`medium`
- 理由：由 OpenSpec 官方 repository README 支持；本次未進行實際安裝測試。
- 支持來源：S-004

### `C-005`

- 主張：Spec Kitty 是開源 CLI，將流程擴展為 spec -> plan -> tasks -> next -> review -> accept -> merge，並使用 repository-native artifact、work package 與 git worktree 支援 agent 工作。
- 類型：`fact`
- 重要程度：`supporting`
- 可信度：`medium`
- 理由：由 Spec Kitty 官方 repository README 支持；本次未進行實際安裝測試。
- 支持來源：S-005

### `C-006`

- 主張：SpecDD 是開源 framework，使用放在專案內容旁的本地 `.sdd` 檔案保存 intent、architecture、behavior、boundary 與 task，並宣稱可逐步導入既有專案。
- 類型：`fact`
- 重要程度：`supporting`
- 可信度：`medium`
- 理由：由 SpecDD 官方文件支持；本次未深入驗證 CLI repository。
- 支持來源：S-008

### `C-007`

- 主張：Kiro Specs 與 OpenSpecification 顯示另一種常見結構：Requirements -> Design -> Tasks；Kiro 文件另描述依賴分析與平行 task execution。
- 類型：`fact`
- 重要程度：`supporting`
- 可信度：`high`
- 理由：Kiro 官方文件直接支持其 Specs 流程；OpenSpecification repository README 支持其 Kiro-inspired 開源實作。
- 支持來源：S-003, S-009

### `C-008`

- 主張：目前證據支持 SDD 可達到高度自動化，但不支持將它描述為對任意專案皆可靠的完全無人開發。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：Spec Kit workflow 明確保留 human checkpoints；Spec Kit README 要求 clarification；Akka 文件描述 human-in-the-loop；本次未找到足以證明任意專案可無人完成的獨立 benchmark。
- 支持來源：S-002, S-007, S-010

### `C-009`

- 主張：較可行的落地策略是 bounded autonomy：agent 自動執行規格明確且可驗證的工作，人工負責 domain decision、規格核准、例外處理與發布前風險確認。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：此建議符合官方文件中的 clarification、human checkpoint、build failure 與 human-in-the-loop 設計。
- 支持來源：S-002, S-003, S-007, S-010

## 限制

- 多數工具能力來自官方文件或 repository README，適合證明設計與公開功能，不等於獨立成效驗證。
- GitHub 與官方文件會持續更新；本報告保存了 2026-05-31 的本地 snapshot，但尚未將 GitHub README 轉為固定 commit permalink。
- arXiv 來源是預印本，不能當成已完成同行評審的共識。
- 本報告著重工具與流程盤點，沒有執行實際 SDD 專案 benchmark。

## 衝突與未知

- 衝突：SDD 目前不是單一標準：GitHub Spec Kit、OpenSpec、SpecDD、Kiro 與 Akka 對 artifact、phase gate 與更新方式的設計不同。
- 衝突：部分工具主張 AI 可生成全部 code，但同一批官方資料仍保留 clarification、human checkpoint 或 human-in-the-loop，因此「全自動」需要明確限定範圍。
- 未知：本次未收集足以比較各工具 defect rate、維護成本或交付速度的獨立 benchmark。
- 未知：本次未對每個開源工具執行安裝、端到端測試與安全審查。
- 未知：大型 brownfield repository 中，spec 與 code 長期同步的實際成本仍需試點驗證。

## 結論

SDD 已經形成可操作的 AI 開發工作流家族，而不是單一工具。若目標是提高自動化程度，應將 specification、task graph、測試、品質閘門與可恢復執行納入同一流程。若目標是完全移除人工，現有證據不足；更務實的方向是逐步擴大 bounded autonomy，並用可量測的試點決定哪些 checkpoint 可以自動放行。

## 建議

- 先選一個邊界清楚、可用自動測試驗證的中小型功能作為試點。
- 將需求、acceptance criteria、架構限制、安全限制與完成條件保存為版本化 artifact。
- 設定至少四個人工或政策閘門：規格核准、架構或安全風險變更、測試無法自動判定、發布前確認。
- 評估工具時分開量測規格品質、任務完成率、測試通過率、人工介入次數、返工率與 spec-code drift。
- 下一輪對 GitHub Spec Kit、OpenSpec 與 Spec Kitty 各做一個相同需求的端到端試驗，再比較維護成本與可恢復性。

## 來源

- `S-001` [GitHub Spec Kit Documentation](https://github.github.com/spec-kit/index.html)
- `S-002` [Spec Kit Workflows Documentation](https://github.github.com/spec-kit/reference/workflows.html)
- `S-003` [Kiro Specs Documentation](https://kiro.dev/docs/specs/)
- `S-004` [OpenSpec Repository README](https://github.com/Fission-AI/OpenSpec)
- `S-005` [Spec Kitty Repository README](https://github.com/Priivacy-ai/spec-kitty)
- `S-006` [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180v1)
- `S-007` [GitHub Spec Kit Repository README](https://github.com/github/spec-kit)
- `S-008` [SpecDD Official Documentation](https://specdd.ai/)
- `S-009` [OpenSpecification Repository README](https://github.com/spenceriam/OpenSpecification)
- `S-010` [Akka Spec-Driven Development Documentation](https://doc.akka.io/sdk/spec-driven-development.html)
