# 根據 SDD 使用 AI 全自動開發：55 來源技術地圖與落地架構

## 報告資訊

- 報告 ID：`sdd-ai-autonomous-development-20260531-v3`
- 版本：`3.0.0`
- 產生時間：`2026-05-31T13:00:00Z`
- 資料截止時間：`2026-05-31T12:45:00Z`
- 整體可信度：`medium`
- 品質分數：`100/100`

## 摘要

本報告以 55 個獨立主要來源建立 SDD 與 AI 自動開發技術地圖。結論是：全自動開發不是單一 coding agent，而是由規格 artifact、traceability、repository context、task graph、scheduler、隔離 workspace、驗證、安全政策、observability、retry 與 escalation 組成的長時間執行系統。來源顯示規格層已相當多元：GitHub Spec Kit、OpenSpec、Spec Kitty、SpecDD、Kiro、Akka、cc-sdd、MoAI-ADK、Specs CLI、各類 MCP workflow 與 OpenSpec 生態。執行層則由 Ralph loops、Swarms、Metaswarm、Maestro、Symphony、Rover、Codexia、worktree 工具補上。現階段可實作高自動化 bounded autonomy；若要可靠零人工交付，仍缺少跨工具 benchmark、安全政策驗證與大型 brownfield 證據。

## 方法

依追加式 crawl queue 蒐集 55 個獨立主要來源，不把文件內 supporting reference 算入數量。所有來源保存本地 snapshot、來源 metadata、深度 summary.md 與索引。`sources/CATALOG.md` 提供 S-001 到 S-055 的導航。關鍵發現採跨來源架構統整；官方文件與 repository README 可證明公開設計，但不視為獨立 benchmark。

## 關鍵發現

### `C-001`

- 主張：SDD 的共通核心是 specification 作為版本化、可演進、可驗證的主要 artifact；code、task、test 與變更紀錄需能回指需求。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：多個官方工具、文件與研究來源在核心方向一致。
- 支持來源：S-001, S-004, S-006, S-008, S-010, S-013, S-027, S-028, S-032, S-033, S-053

### `C-002`

- 主張：SDD 流程的穩定骨架是 clarify 或 requirements -> design 或 plan -> tasks -> implementation -> verification；不同工具主要差在 artifact schema、審批點與執行自動化程度。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：至少十個獨立工具實作相近階段。
- 支持來源：S-001, S-003, S-007, S-009, S-010, S-011, S-014, S-015, S-023, S-027, S-032, S-033, S-052, S-053

### `C-003`

- 主張：規格層至少需要 artifact versioning、traceability、refinement、agent-accessible interface 與 approval state。OpenSpec change folder、SpecDD `.sdd`、Specs CLI traceability、MCP workflow 與 JSON spec 都是可用形態。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：跨來源比較顯示共同需求，但格式沒有單一標準。
- 支持來源：S-004, S-008, S-013, S-014, S-015, S-032, S-033, S-049, S-053

### `C-004`

- 主張：brownfield 自動開發需要 codebase context 層。OpenLore 以 static analysis、knowledge graph、living specs、drift detection 與 graph-native MCP 建立持久架構記憶；Kata 以 Tree-sitter 與 SQLite 建立 repository-aware context。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：工具 README 直接描述設計；仍需大型 repository benchmark。
- 支持來源：S-018, S-029

### `C-005`

- 主張：長時間自動執行需要可持久化 task graph 與 iteration memory。Taskmaster、Flow Next、Swarms、Ralph 類工具分別使用 dependency graph、wave execution、PRD JSON、progress log 或 git commit 保存狀態。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：多個 repository 直接描述狀態與執行方式。
- 支持來源：S-019, S-035, S-037, S-038, S-039, S-040

### `C-006`

- 主張：可靠執行層需要隔離 workspace、平行控制、retry、reconciliation 與 observability。Symphony SPEC.md 提供服務級拆分；Rover、Worktrunk、workmux、Codexia 與 Spec Kitty 補上 workspace 或 worktree 實作模式。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：官方 SPEC 與多個 repository 直接支持。
- 支持來源：S-005, S-020, S-021, S-022, S-043, S-044, S-045

### `C-007`

- 主張：多 agent 系統需要明確的 orchestration contract：specialist delegation、handoff、wave 或 staged execution、持久 session state、verification 與 merge boundary。BMAD、Swarms、Metaswarm、Maestro 與 Local-first Maestro 提供不同解法。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：工具邊界清楚，但目前缺跨工具獨立比較。
- 支持來源：S-016, S-040, S-041, S-042, S-047

### `C-008`

- 主張：全自動系統的驗證不能只看 test pass。最低要求應涵蓋 acceptance criteria、spec-code traceability、靜態分析、安全規格、政策閘門、review 與 escalation。Threatspec、Constitutional SDD、AI Governor、MoAI-ADK 與 cc-sdd 補充此層。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：多個來源支持品質與安全約束方向，但尚缺統一標準。
- 支持來源：S-025, S-027, S-028, S-041, S-054, S-055

### `C-009`

- 主張：Ralph loop 能提高連續執行能力，但必須配合 task 邊界、completion condition、max iteration、git memory、驗證與人工 escalation；否則只是把單次失敗延長。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Smart Ralph、Flow Next、Anthropic Ralph Wiggum、iannuttall Ralph 與 snarktank Ralph 呈現互補機制。
- 支持來源：S-034, S-035, S-037, S-038, S-039

### `C-010`

- 主張：現階段適合落地的是 bounded autonomy：agent 可自動處理明確且可驗證的工作；模糊需求、架構變更、安全風險、無法自動驗證的結果與發布決策應進入人工或政策 escalation。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：human gate、approval、review、policy boundary 與 escalation 在多種工具中重複出現。
- 支持來源：S-002, S-005, S-007, S-010, S-021, S-023, S-027, S-033, S-034, S-036

### `C-011`

- 主張：可行首版架構可選：OpenSpec 或 Spec Kit 作規格層，OpenLore 或 Kata 補 repository context，Taskmaster 或 Flow Next 管 task graph，Symphony、Rover 或 worktree 工具做隔離執行，MoAI-ADK、CI 與 Threatspec 補驗證與安全。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：此為跨來源系統整合建議，需用試點驗證相容性。
- 支持來源：S-001, S-004, S-018, S-019, S-021, S-022, S-028, S-029, S-035, S-055

## 限制

- 55 個來源以官方文件與 repository README 為主，適合建立技術地圖，不等於獨立成效驗證。
- 部分來源為較小型專案，需要另外檢查維護活躍度、測試覆蓋與 production readiness。
- S-024 與 S-025 是 arXiv 預印本，尚不能視為同行評審共識。
- GitHub snapshot 保存於 2026-05-31；尚未全部轉成固定 commit permalink。
- 本次未端到端安裝執行全部 55 個來源。

## 衝突與未知

- 衝突：SDD 沒有單一 artifact 標準：Markdown、JSON、`.sdd`、OpenSpec change folder、MCP state 都存在。
- 衝突：部分工具追求 auto-run，另一些工具刻意保留 approval gate；兩者代表不同風險偏好。
- 衝突：Ralph loop、multi-agent orchestrator 與 worktree manager 是執行層，不應被誤認為規格品質本身。
- 衝突：README 可證明工具公開設計，但不能取代端到端 benchmark。
- 未知：缺少同一 repository、同一模型、同一需求下的跨工具 benchmark。
- 未知：大型 brownfield 專案的 spec extraction 準確率、drift 偵測與 context index 成本仍需量測。
- 未知：多 agent concurrent spec update 的衝突解決與權限模型尚未形成共識。
- 未知：完全無人發布在安全、法規與事故責任上仍有重大缺口。

## 結論

SDD AI 全自動開發應被設計為多層控制系統。推薦技術地圖：1. specification artifact；2. traceability；3. repository context；4. task graph；5. scheduler 與 autonomous loop；6. isolated workspace；7. verifier 與 security policy；8. observability、retry 與 escalation。來源生態已足以組裝原型，但尚不足以保證任意專案零人工交付。最合理的路徑是 bounded autonomy：先讓系統在明確範圍內自動完成、驗證、重試與回報，再依量測結果逐步收縮人工閘門。

## 建議

- 閱讀 `sources/CATALOG.md` 選出試點工具，不直接以星數或宣傳用語決策。
- 首個試點選中小型服務，固定 requirement、acceptance criteria、安全限制與 CI verifier。
- 以 OpenSpec 或 Spec Kit 作規格層；以 OpenLore 或 Kata 驗證 brownfield context；以 Taskmaster 或 Flow Next 驗證 task graph。
- 執行層採 Symphony、Rover、Codexia 或 worktree 工具之一，保存每次 run 的狀態、log、retry 與 escalation 原因。
- 驗證層加入 test、lint、static analysis、security scan、requirement coverage、spec-code drift 與人工 review。
- 用同一需求執行至少三組工具組合，量測成功率、人工介入次數、返工率、執行成本、恢復能力與安全事件。

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
- `S-026` [Kiro Repository README](https://github.com/kirodotdev/Kiro)
- `S-027` [cc-sdd Repository README](https://github.com/gotalab/cc-sdd)
- `S-028` [MoAI-ADK Repository README](https://github.com/modu-ai/moai-adk)
- `S-029` [OpenLore Repository README](https://github.com/clay-good/OpenLore)
- `S-030` [Specboot ai-specs Repository README](https://github.com/LIDR-academy/lidr-specboot)
- `S-031` [Gentle-AI Repository README](https://github.com/Gentleman-Programming/gentle-ai)
- `S-032` [spec-coding-mcp Repository README](https://github.com/kevinlin/spec-coding-mcp)
- `S-033` [Pimzino Spec Workflow MCP README](https://github.com/Pimzino/spec-workflow-mcp)
- `S-034` [Smart Ralph Repository README](https://github.com/tzachbon/smart-ralph)
- `S-035` [Flow Next Repository README](https://github.com/gmickel/flow-next)
- `S-036` [GAAI Framework Repository README](https://github.com/Fr-e-d/GAAI-framework)
- `S-037` [iannuttall Ralph Repository README](https://github.com/iannuttall/ralph)
- `S-038` [Anthropic Ralph Wiggum Plugin README](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md)
- `S-039` [snarktank Ralph Repository README](https://github.com/snarktank/ralph)
- `S-040` [Swarms Repository README](https://github.com/am-will/swarms)
- `S-041` [Metaswarm Repository README](https://github.com/dsifry/metaswarm)
- `S-042` [Maestro Orchestrate Repository README](https://github.com/josstei/maestro-orchestrate)
- `S-043` [Worktrunk Repository README](https://github.com/max-sixty/worktrunk)
- `S-044` [workmux Repository README](https://github.com/raine/workmux)
- `S-045` [Codexia Repository README](https://github.com/milisp/codexia)
- `S-046` [Claw Orchestrator Repository README](https://github.com/Enderfga/claw-orchestrator)
- `S-047` [Local-first Maestro Repository README](https://github.com/ReinaMacCredy/maestro)
- `S-048` [Awesome OpenSpec Repository README](https://github.com/wearetechnative/awesome-openspec)
- `S-049` [OpenSpec Supported Tools Documentation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)
- `S-050` [OpenSpec for Copilot Repository README](https://github.com/atman-33/openspec-for-copilot)
- `S-051` [ClawSpec Repository README](https://github.com/bytegh/clawspec)
- `S-052` [AI Coding Workflow Repository README](https://github.com/nicksp/ai-coding-worflow)
- `S-053` [Claude SDD Toolkit Repository README](https://github.com/tylerburleigh/claude-sdd-toolkit)
- `S-054` [AI Governor Framework Repository README](https://github.com/Fr-e-d/AI-Governor-Framework)
- `S-055` [Threatspec Repository README](https://github.com/threatspec/threatspec)
