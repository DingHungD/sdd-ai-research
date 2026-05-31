# 根據 SDD 使用 AI 全自動開發：技術架構、工具生態與可行邊界

## 報告資訊

- 報告 ID：`sdd-ai-autonomous-development-20260531-v2`
- 版本：`2.0.0`
- 產生時間：`2026-05-31T12:10:00Z`
- 資料截止時間：`2026-05-31T11:39:14Z`
- 整體可信度：`medium`
- 品質分數：`100/100`

## 摘要

本報告以 25 個獨立主要來源研究 SDD 與 AI 自動開發。結論是：可行系統不是單一 coding agent，而是由規格 artifact、traceability、task graph、repository context、scheduler、隔離 workspace、verifier、policy gate、retry 與 observability 組成的長時間執行系統。GitHub Spec Kit、OpenSpec、Spec Kitty、SpecDD、Kiro Specs、Akka SDD、codex-spec、SpecPulse、Specs CLI、Spec Workflow MCP 與 Specflow 提供不同形式的規格層；Kata、Taskmaster、OpenAI Symphony、Rover、BMAD 與 GSD 補上 context、任務圖與執行編排。現有證據支持 bounded autonomy：明確範圍內可高度自動化，但不足以支持任意專案的零人工可靠交付。

## 方法

依追加式 crawl queue 蒐集 25 個獨立主要來源，不將各來源內部引用的 supporting reference 計入數量。來源包含官方文件、官方 repository、公開 service specification 與 arXiv 預印本。每份來源保存本地 snapshot 並整理技術摘要。關鍵發現採跨來源統整，不以逐項工具介紹取代分析。工具 README 可證明公開設計與功能介面，但不當作獨立成效 benchmark。

## 關鍵發現

### `C-001`

- 主張：SDD 的共同核心不是固定檔名或單一工具，而是將 specification 提升為版本化、可演進、可驗證的主要 artifact，讓 code、task 與驗證結果能回指需求。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：GitHub Spec Kit、Akka、SpecDD、OpenSpec、Specs CLI 與 SDD 預印本在核心方向上一致。
- 支持來源：S-001, S-004, S-006, S-008, S-010, S-013

### `C-002`

- 主張：成熟的 SDD 流程通常採多階段 artifact pipeline：clarify 或 requirements -> design 或 plan -> tasks -> implementation -> verification，而不是一次性 prompt-to-code。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：多個獨立工具以不同名稱實作相同的階段化模式。
- 支持來源：S-001, S-003, S-007, S-009, S-010, S-011, S-014, S-015, S-023

### `C-003`

- 主張：規格層至少需要四種能力：可版本控制的 artifact、需求到 task 的 traceability、持續 refinement、可供不同 agent 呼叫的穩定介面。Markdown、`.sdd` 檔案、change folder 與 MCP server 都是可行形式。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：跨工具比較顯示 artifact 格式不同，但可追溯、可更新與可操作是共同需求。
- 支持來源：S-004, S-008, S-013, S-014, S-015

### `C-004`

- 主張：規格本身不足以支援 brownfield 自動開發；agent 還需要 repository-aware context。Kata 的 Tree-sitter 與 SQLite 索引、GSD 的 context engineering 與 fresh subagent 策略代表兩種互補方法。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：相鄰工具直接處理 codebase context；本次尚未進行大型 repository benchmark。
- 支持來源：S-017, S-018, S-024

### `C-005`

- 主張：從規格到長時間自動執行需要 task graph 與 scheduler。Taskmaster 提供 PRD-to-task dependency 層；Kiro、Akka 與 Spec Kit workflow 支援任務分解、平行化或可恢復執行。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：官方文件與 repository README 直接描述 task dependency、parallel execution 或 resume 能力。
- 支持來源：S-002, S-003, S-010, S-019

### `C-006`

- 主張：可靠的全自動執行層需要隔離 workspace、平行工作控制、retry、reconciliation 與 observability。OpenAI Symphony SPEC.md 將這些能力明確拆成服務元件；Rover 與 Spec Kitty 補充 workspace 或 worktree 隔離模式。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：OpenAI Symphony 公開 service specification、Rover 與 Spec Kitty repository 直接支持。
- 支持來源：S-005, S-020, S-021, S-022

### `C-007`

- 主張：驗證層不能只檢查是否產生 code。最低要求應包含 acceptance criteria、測試、spec-code traceability、偏差檢測與安全政策；必要時以 policy gate 阻擋自動放行。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：Akka 描述偏差與 human-in-the-loop；Agent Skills SDD 強調 verification；Constitutional SDD 預印本補充安全約束方向。
- 支持來源：S-010, S-013, S-023, S-025

### `C-008`

- 主張：現有工具生態可分為三層：純規格與 traceability 工具、完整生命週期 workflow 工具、執行與隔離編排工具。將所有工具混為 SDD 會掩蓋其不同責任。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：25 個來源的功能邊界清楚顯示分層。
- 支持來源：S-001, S-004, S-005, S-008, S-011, S-013, S-016, S-017, S-019, S-020, S-022

### `C-009`

- 主張：現有證據支持 bounded autonomy，不支持把 SDD 宣稱為任意專案的零人工可靠開發。clarification、human checkpoint、review、accept、policy boundary 與 human-in-the-loop 仍反覆出現在工具設計中。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：多個獨立來源明確保留人工或政策介入點；本次未發現足以證明通用零人工交付的獨立 benchmark。
- 支持來源：S-002, S-005, S-007, S-010, S-021, S-023

### `C-010`

- 主張：可落地的首版系統應採分層整合：Spec Kit 或 OpenSpec 類規格層、Taskmaster 類 task graph、Kata 類 code context、Symphony 或 Rover 類隔離執行層，再接 CI verifier 與人工 escalation。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：此建議由跨來源架構比較推得，仍需以試點驗證工具相容性。
- 支持來源：S-001, S-004, S-018, S-019, S-021, S-022

## 限制

- 25 個主要來源多為官方文件與 repository README，可證明公開設計，但不等於獨立成效驗證。
- S-024 與 S-025 是 arXiv 預印本，尚不能視為同行評審共識。
- 本次保存 2026-05-31 snapshot；部分 GitHub 頁面尚未轉為固定 commit permalink。
- 本次未安裝並端到端執行所有工具。

## 衝突與未知

- 衝突：SDD 尚無單一標準：artifact 可為 Markdown、change folder、`.sdd`、MCP 狀態或工具自有資料結構。
- 衝突：部分來源使用「全自動」語言，但同時保留 clarification、review、accept、human checkpoint 或 policy boundary。
- 衝突：純 SDD 工具與執行編排工具責任不同；後者不能取代規格品質。
- 未知：尚缺少針對同一需求、同一 repository、同一模型的跨工具獨立 benchmark。
- 未知：大型 brownfield repository 中，spec-code drift、context index 準確率與長時間 retry 成本仍需量測。
- 未知：多 agent 同時修改 specification 與 code 時，衝突解決與安全 escalation 的最佳策略仍未確立。

## 結論

要根據 SDD 使用 AI 全自動開發，應將問題視為系統工程，而不是選一個 coding agent。建議架構分為八層：1. specification artifact；2. requirement-task-test traceability；3. repository context；4. task graph；5. scheduler；6. isolated workspace；7. verifier 與 policy gate；8. observability、retry 與 escalation。短期目標應是 bounded autonomy：自動完成可驗證工作，將高風險決策與模糊需求升級給人。當試點資料證明特定 gate 可可靠自動化，再逐步縮小人工介入範圍。

## 建議

- 以一個可測試的中小型服務做試點，不直接從大型核心系統開始。
- 先選一個規格層：GitHub Spec Kit 或 OpenSpec；將 requirement、acceptance criteria、design constraint 與 task 版本化。
- 加入 task graph 與 repository context，避免只用長 prompt 驅動 agent。
- 執行層採隔離 workspace，保存 run state、log、retry 次數與 escalation 原因。
- CI 至少檢查 test、lint、security scan、requirement coverage 與 spec-code drift。
- 用相同需求比較 2 至 3 組工具組合，量測人工介入次數、成功率、返工率、成本與恢復能力。

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
- `S-011` [codex-spec Repository README](https://github.com/shenli/codex-spec)
- `S-012` [SpecPulse Repository README](https://github.com/specpulse/specpulse)
- `S-013` [Specs CLI Repository README](https://github.com/specs-cli/specs-cli)
- `S-014` [Spec Workflow MCP Repository README](https://github.com/mamajiaa/specs-workflow-mcp)
- `S-015` [Specflow Repository README](https://github.com/specstoryai/specflow)
- `S-016` [BMAD Method Repository README](https://github.com/bmad-code-org/BMAD-METHOD)
- `S-017` [Get Shit Done Repository README](https://github.com/gsd-build/get-shit-done)
- `S-018` [Kata Repository README](https://github.com/gannonh/kata)
- `S-019` [Taskmaster Repository README](https://github.com/eyaltoledano/claude-task-master)
- `S-020` [OpenAI Symphony Repository README](https://github.com/openai/symphony)
- `S-021` [OpenAI Symphony Service Specification](https://github.com/openai/symphony/blob/main/SPEC.md)
- `S-022` [Rover Repository README](https://github.com/endorhq/rover)
- `S-023` [Agent Skills Spec-Driven Development Skill](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md)
- `S-024` [Spec Kit Agents: Context-Grounded Agentic Workflows](https://arxiv.org/abs/2604.05278v1)
- `S-025` [Constitutional Spec-Driven Development](https://arxiv.org/abs/2602.02584v1)
