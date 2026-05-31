# 根據 SDD 使用 AI 全自動開發：78 來源技術地圖、文章脈絡與落地架構

## 報告資訊

- 報告 ID：`sdd-ai-autonomous-development-20260531-v4`
- 版本：`4.0.0`
- 產生時間：`2026-05-31T14:00:00Z`
- 資料截止時間：`2026-05-31T13:45:00Z`
- 整體可信度：`medium`
- 品質分數：`100/100`

## 摘要

本報告以 78 個獨立主要來源研究 SDD 與 AI 自動開發，包括工具 repository、官方文件、service specification、工程文章、企業採用文章、案例與 benchmark。跨來源結論維持一致：可靠自動開發不是單一 coding agent，而是由 specification artifact、traceability、repository context、task graph、scheduler、isolated workspace、verifier、security policy、observability、retry 與 escalation 組成。新增文章支線補強三點：第一，enterprise 採用的主要缺口是 brownfield、現有 workflow 整合與 spec 維護；第二，context engineering 是規格之外的必要能力；第三，benchmark 必須涵蓋 investigation、validation、maintenance、test generation 與 context retrieval，而不是只看 patch generation。現階段合理目標仍是 bounded autonomy。

## 方法

使用追加式 crawl queue 保存 78 個獨立主要來源，不把文件內 supporting reference 算入數量。來源分為工具與官方文件、文章與案例、研究與 benchmark。每份來源有 raw snapshot、metadata、深度 summary.md 與 catalog 項目。文章用於補足採用經驗與風險，不凌駕於官方技術文件或原始研究。

## 關鍵發現

### `C-001`

- 主張：SDD 的共通核心是 specification 作為版本化、可演進、可驗證的主要 artifact；code、task、test 與變更紀錄需能回指需求。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：官方工具、文章與研究方向一致。
- 支持來源：S-001, S-004, S-006, S-008, S-010, S-013, S-027, S-028, S-032, S-033, S-053, S-056, S-058, S-059

### `C-002`

- 主張：穩定 SDD workflow 通常為 clarify 或 requirements -> design 或 plan -> tasks -> implementation -> verification；不同工具差異在 artifact schema、approval、context 與 execution automation。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：多個工具、官方文件與實務文章呈現相同骨架。
- 支持來源：S-001, S-003, S-007, S-010, S-014, S-023, S-027, S-032, S-033, S-052, S-053, S-057, S-063, S-073

### `C-003`

- 主張：enterprise 採用的主要問題不是能否生成 code，而是 brownfield 導入、現有 workflow 整合、spec 維護、context engineering、review-centric 工作方式與安全治理。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Thoughtworks、InfoQ、Tessl、Bito、AWS 案例與多個工具限制互相補證。
- 支持來源：S-058, S-063, S-065, S-067, S-068, S-077, S-078

### `C-004`

- 主張：context engineering 是 SDD 的必要配套。大型 repository 需要 code graph、semantic retrieval、memory、compression 與 context selection；僅靠 monolithic spec 不足以穩定支援長時間 agent。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：OpenLore、Kata、GSD、Anthropic、Martin Fowler site 文章與 ContextBench 提供互補證據。
- 支持來源：S-017, S-018, S-029, S-069, S-071, S-074, S-077, S-078

### `C-005`

- 主張：長時間執行需要持久 task graph、iteration memory、workspace isolation、scheduler、retry、reconciliation 與 observability；Ralph loop 只是一部分。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Taskmaster、Flow Next、Ralph variants、Symphony、Rover、Worktrunk、workmux、Codexia 與 Tessl Symphony 解讀共同支持。
- 支持來源：S-019, S-021, S-022, S-034, S-035, S-037, S-038, S-039, S-043, S-044, S-045, S-066

### `C-006`

- 主張：驗證層必須超過 test pass：需要 acceptance criteria、traceability、static analysis、security policy、drift detection、review 與 escalation。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Constitutional SDD、Threatspec、OpenLore、MoAI-ADK、cc-sdd、AWS GovTech 案例與 executable architecture 文章共同支持。
- 支持來源：S-025, S-027, S-028, S-029, S-055, S-063, S-068

### `C-007`

- 主張：評估 coding agent 時不能只看 bug patch benchmark。應加入 context retrieval、investigation、validation、maintenance、test generation、多語言與人工介入成本。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：ContextBench、OmniCode、SWE Atlas 與 Loadsys 指標文章提供互補評估面。
- 支持來源：S-072, S-074, S-075, S-078

### `C-008`

- 主張：多 agent 架構應先區分 deterministic workflow 與 autonomous agent。可預測步驟使用 workflow；模糊探索才使用具自主性的 agent，並以 evaluator、review 或 policy gate 收斂。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Anthropic 官方 agent 指南與多 agent 工具架構一致。
- 支持來源：S-040, S-041, S-042, S-047, S-070

### `C-009`

- 主張：現階段應採 bounded autonomy：讓 agent 自動完成明確且可驗證的工作；模糊需求、架構變更、安全風險、無法驗證結果與發布決策進入人工或政策 escalation。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：工具設計、案例與文章均反覆出現 approval、human oversight、review 與 escalation。
- 支持來源：S-002, S-005, S-010, S-021, S-023, S-027, S-033, S-034, S-063, S-067, S-070, S-073

## 限制

- 78 個來源中包含工具自述、官方文章、編輯文章、案例與 benchmark；不同來源證據權重不同。
- Red Hat 兩篇文章因 HTTP 403 未保存，OpenAI SWE-bench Verified 頁面因本機 SSL 憑證錯誤未保存；失敗紀錄保留於 queue。
- 文章適合補充採用脈絡，不應取代官方技術文件與端到端測試。
- 本次未安裝執行全部工具。

## 衝突與未知

- 衝突：SDD 沒有單一標準，從輕量 Markdown 到 executable architecture 都存在。
- 衝突：文章對 SDD 採用前景的態度不同：部分強調效率，部分強調 brownfield、security、drift 與維護成本。
- 衝突：benchmark 仍不足以完整代表企業軟體交付。
- 未知：缺少同一 repository、模型與需求下的跨工具獨立 benchmark。
- 未知：大型 brownfield 的 spec extraction、context retrieval 與 drift detection 成本仍需試點量測。
- 未知：安全政策與人工 escalation 最佳邊界仍依領域而異。

## 結論

SDD AI 全自動開發應以分層系統實作：specification artifact、traceability、repository context、task graph、workflow 與 agent orchestration、isolated runtime、verifier、security policy、observability 與 escalation。文章與 benchmark 擴充後，最重要的修正是：不要把自動化程度誤認為可靠性。可行路線是 bounded autonomy，透過量測逐步擴張自動放行範圍。

## 建議

- 將 `sources/CATALOG.md` 作為研究入口，依技術層與來源類型選擇深挖材料。
- 試點至少量測 first-pass verification rate、人工介入次數、iteration cycles、context provision time、retry、返工率與安全事件。
- 工具組合建議從 OpenSpec 或 Spec Kit、OpenLore 或 Kata、Taskmaster 或 Flow Next、Symphony 或 Rover、CI verifier 與 Threatspec 開始。
- 對 workflow 與 agent 分別設計：可預測步驟固定化，模糊探索步驟保留 agent，但必須配置 evaluator 與 escalation。

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
- `S-056` [GitHub Blog: Spec-driven development with AI toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- `S-057` [GitHub Blog: Markdown as a programming language](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)
- `S-058` [Thoughtworks Technology Radar: Spec-driven development](https://www.thoughtworks.com/en-gb/radar/techniques/spec-driven-development)
- `S-059` [Thoughtworks: Unpacking spec-driven development](https://www.thoughtworks.com/en-gb/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- `S-060` [Thoughtworks Podcast: What is spec-driven development?](https://www.thoughtworks.com/en-us/insights/podcasts/technology-podcasts/what-is-spec-driven-development)
- `S-061` [Kiro Blog: Introducing Kiro](https://kiro.dev/blog/introducing-kiro/)
- `S-062` [AWS Documentation Overview: Kiro](https://aws.amazon.com/documentation-overview/kiro/)
- `S-063` [AWS Public Sector Blog: Accelerating GovTech development with Kiro](https://aws.amazon.com/blogs/publicsector/accelerating-govtech-development-with-kiro/)
- `S-064` [Tessl: How products pioneer SDD](https://tessl.io/blog/how-tessls-products-pioneer-spec-driven-development/)
- `S-065` [Tessl: 10 things about specs](https://tessl.io/blog/spec-driven-development-10-things-you-need-to-know-about-specs/)
- `S-066` [Tessl: OpenAI Symphony orchestration spec](https://tessl.io/blog/openai-open-sources-symphony-a-spec-for-orchestrating-codex-agents/)
- `S-067` [InfoQ: Enterprise SDD adoption](https://www.infoq.com/articles/enterprise-spec-driven-development/)
- `S-068` [InfoQ: When architecture becomes executable](https://www.infoq.com/articles/spec-driven-development/)
- `S-069` [Martin Fowler: Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)
- `S-070` [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- `S-071` [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- `S-072` [Scale AI: SWE Atlas is Complete](https://scale.com/blog/swe-atlas-complete)
- `S-073` [Xcapit: SDD with AI Agents Practical Guide](https://www.xcapit.com/en/blog/spec-driven-development-ai-agents)
- `S-074` [ContextBench Paper Page](https://huggingface.co/papers/2602.05892)
- `S-075` [OmniCode Benchmark Paper](https://arxiv.org/abs/2602.02262)
- `S-076` [SDD Practitioner Guide OpenReview PDF](https://openreview.net/pdf?id=bw5mNj75h9)
- `S-077` [Bito: SDD Explained for AI Coding Teams](https://bito.ai/blog/spec-driven-development-explained-for-ai-coding-teams/)
- `S-078` [Loadsys: Context Engineering AI Practice for SDD Teams](https://www.loadsys.com/blog/context-engineering-ai-spec-driven-development-practice/)
