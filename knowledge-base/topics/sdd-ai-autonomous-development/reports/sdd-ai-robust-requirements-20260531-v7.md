# SDD AI 全自動開發：最穩健且可精準對照需求書的 Assurance Architecture

## 報告資訊

- 報告 ID：`sdd-ai-robust-requirements-20260531-v7`
- 版本：`7.0.0`
- 產生時間：`2026-05-31T14:22:35Z`
- 資料截止時間：`2026-05-31T14:00:00Z`
- 整體可信度：`medium`
- 品質分數：`100/100`

## 摘要

本報告以 97 份主要來源重構 SDD AI 全自動開發的比較方式。面對工具定位衝突時，不應把所有工具壓成單一排名，而應分成兩個軸：第一軸是從輕量 Markdown specification、結構化 artifact、living spec 與雙向 traceability，到 executable architecture、compile-time traceability 與 policy-as-code gate 的成熟度；第二軸是效率迴圈、brownfield context、security policy、drift 維護、runtime orchestration 與 benchmark assurance 等特化能力。如果新增需求是「最穩健，且可以精準對照需求書」，推薦採用 bounded autonomy assurance architecture：受控需求基線、雙向 traceability graph、repository context graph、task graph、隔離執行環境、驗證矩陣、policy-as-code gate、evidence store 與人工升級機制。核心不是讓 agent 自由產碼，而是讓每一項需求都能沿著 Requirement -> Design -> Task -> Code -> Test -> Evidence 正反向查核。

## 方法

研究流程依 append-only crawl queue 保存 97 份主要來源；每一份來源均保存 raw snapshot、metadata、summary.md 與 catalog 項目。本輪新增 NASA SWE-052、SWE-059、SWE-067 與 requirements management，NIST SSDF 與 NCCoE DevSecOps，OWASP ASVS、AISVS、SCVS、DevGuard，OPA、OPA pull request checks、Conftest，CISA Secure by Design 與 Product Security Bad Practices，以及 SWE-Bench Pro、R2Code、ReqToCode。判讀時優先採官方規範與官方文件；arXiv 預印本只作為新方向線索，不視為已建立的產業事實。比較框架拆成成熟度軸與特化軸，避免不同問題的工具被混成單一排名。

## 關鍵發現

### `C-001`

- 主張：若目標是穩健與精準對照需求書，需求書必須成為受控 baseline。每一項需求應有唯一 ID、版本、來源、owner、優先級、驗收條件、變更紀錄與核准狀態；只有 prose 文件不足以支撐自動查核。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA requirements management、NASA traceability 規範與多個 SDD 工具均要求受控需求與結構化 artifact。
- 支持來源：S-001, S-003, S-004, S-008, S-010, S-013, S-032, S-079, S-080, S-081, S-082

### `C-002`

- 主張：穩健架構的核心是雙向 traceability：Requirement -> Design -> Task -> Code -> Verification/Test -> Evidence，並能反向找出 orphan design、額外程式碼、未覆蓋需求、缺少驗證與 non-conformance。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA SWE-052、SWE-059、SWE-067 對雙向追溯、需求落實與驗證提供直接規範。
- 支持來源：S-013, S-079, S-080, S-081, S-082

### `C-003`

- 主張：成熟度基準應分層：L1 輕量 Markdown spec；L2 結構化 requirements/design/tasks artifacts；L3 living spec、repository context 與 drift detection；L4 executable architecture、compile-time traceability 與 policy-as-code enforcement。這是能力階梯，不是所有專案一開始都必須採 L4。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：現有工具從 Spec Kit、OpenSpec、SpecDD 到 OpenLore、Akka 與新興 ReqToCode 呈現明確的能力遞進。
- 支持來源：S-001, S-004, S-008, S-010, S-013, S-029, S-068, S-095

### `C-004`

- 主張：特化能力應獨立比較：效率型強調 autonomous loop 與吞吐量；brownfield 型強調 repository context 與漸進導入；security 型強調安全控制與 policy gate；drift 維護型強調 living spec、staleness 與 impact analysis；runtime 型強調隔離、排程、重試與可觀測性。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Taskmaster、Flow Next、Ralph variants、OpenLore、Kata、Threatspec、Symphony、Rover 等來源各自優化不同指標。
- 支持來源：S-018, S-019, S-021, S-022, S-029, S-034, S-035, S-037, S-038, S-039, S-055, S-066, S-067, S-077

### `C-005`

- 主張：brownfield 專案若要求穩健，應加入 repository context graph、語意檢索、程式結構索引、living spec 與 drift/preflight gate，避免 agent 只憑單次 prompt 或單一長文件工作。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Kata、OpenLore、GSD 與 context engineering 來源均指出 repository-aware context 與 drift 管理的重要性。
- 支持來源：S-017, S-018, S-029, S-069, S-071, S-074, S-077, S-078

### `C-006`

- 主張：安全政策不可只放在說明文字中。應把 NIST SSDF、OWASP ASVS、AISVS、SCVS 與組織內規映射成版本化 requirements，並透過 OPA/Rego、Conftest 或等價機制在 pull request、CI 與部署前執行可稽核 gate。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NIST、OWASP、OPA 與 Conftest 官方資料共同支持 outcome-based secure SDLC、可測試控制與 policy-as-code enforcement。
- 支持來源：S-083, S-084, S-085, S-086, S-087, S-088, S-089, S-090, S-091, S-096, S-097

### `C-007`

- 主張：需求對照資料模型至少需要 Requirement ID、source、version、owner、priority、acceptance criteria、security control refs、design refs、task refs、code refs、test refs、evidence refs、status 與 change history。每次修改都應重新計算覆蓋率與 orphan artifacts。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA traceability、requirements management 與 OWASP 版本化控制的組合推導出可稽核資料模型。
- 支持來源：S-079, S-080, S-081, S-082, S-085, S-086, S-087

### `C-008`

- 主張：最穩健的執行模式是 bounded autonomy：agent 可以自動產生設計、tasks、patch、tests 與 evidence，但 baseline 變更、安全例外、未解驗證失敗與部署決策必須升級至人工或明確核准 gate。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：SDD workflow、Symphony runtime、AWS GovTech、Anthropic agent workflow 與 CISA Secure by Design 均支持受控邊界、核准與責任歸屬。
- 支持來源：S-002, S-010, S-021, S-023, S-027, S-033, S-063, S-067, S-070, S-096, S-097

### `C-009`

- 主張：未知能力必須用 benchmark 驗證。不能只看 patch success；還要測 requirement coverage、traceability completeness、orphan artifacts、spec-code drift、first-pass verification、human interventions、security exceptions、長任務完成率與 brownfield context retrieval。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：ContextBench、OmniCode、SWE Atlas 與 SWE-Bench Pro 顯示單一 bug patch 指標不足以代表專業開發任務。
- 支持來源：S-072, S-074, S-075, S-078, S-092, S-093

### `C-010`

- 主張：R2Code 與 ReqToCode 代表值得追蹤的新方向：前者聚焦 requirements-to-code traceability link accuracy，後者探索 language-native metadata 與 compile-time verification。兩者可作為實驗候選，但尚不能取代成熟的 traceability matrix 與 CI gate。
- 類型：`inference`
- 重要程度：`medium`
- 可信度：`medium`
- 理由：兩項來源為近期預印本，方向具體但仍需要獨立重現與工程驗證。
- 支持來源：S-094, S-095

### `C-011`

- 主張：建議的穩健 assurance architecture 由九個元件組成：Requirements Registry、Traceability Graph、Repository Context Graph、Plan/Task Graph、Isolated Runtime、Verifier Matrix、Policy Gates、Evidence Store、Escalation Workflow。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：這是把 SDD artifacts、NASA traceability、brownfield context、runtime isolation 與安全政策來源整合後的架構推論。
- 支持來源：S-001, S-004, S-021, S-022, S-029, S-055, S-068, S-079, S-080, S-081, S-088, S-089, S-090, S-091

### `C-012`

- 主張：採用順序應由證據需求驅動：先建立 requirement IDs、baseline 與 traceability matrix；再接入 code/test evidence 與 drift detection；之後加入安全 policy gates；最後才擴大 autonomous loop、平行 agents 與 compile-time 實驗。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：此順序優先建立可查核性，再擴大自動化風險邊界。
- 支持來源：S-010, S-021, S-029, S-063, S-067, S-079, S-080, S-081, S-083, S-088

## 限制

- 97 份來源涵蓋官方規範、官方文件、開源專案、工程文章與預印本；證據強度並不相同，因此報告對研究原型保持中等信心。
- 本報告建立的是選型與 assurance architecture，不是對所有候選工具完成同一環境下的實測排名。
- 部分來源抓取失敗項目仍保留於 append-only queue，包括 Red Hat HTTP 403 與 OpenAI 網頁 SSL 憑證驗證失敗，未被靜默移除。
- compile-time traceability 與 requirement-to-code AI linking 仍屬新興方向，不能取代 baseline、矩陣、測試與政策 gate。

## 衝突與未知

- 衝突：成熟度基準比較：輕量 Markdown specification -> 結構化 artifacts -> living spec 與雙向 traceability -> executable architecture、compile-time traceability 與 policy-as-code enforcement。這是成熟度階梯，不宜混成單一產品排行。
- 衝突：特化能力比較：效率與 autonomous loop、brownfield context、security policy、drift 與維護成本、runtime orchestration、benchmark assurance 各自強調不同指標。選型應根據需求風險配置，而不是找一個工具包辦全部問題。
- 衝突：研究原型與成熟控制的證據強度不同。R2Code、ReqToCode 可追蹤，但現階段應由 NASA traceability、NIST SSDF、OWASP 與 CI policy gates 承擔主要 assurance。
- 未知：需要在相同 repository、相同需求書、相同模型與工具限制下，比較各方案的 requirement coverage、traceability completeness、orphan artifacts、spec-code drift、first-pass verification、human interventions 與長任務完成率。
- 未知：需要把組織安全政策、NIST SSDF、OWASP ASVS、AISVS、SCVS 與 CISA Secure by Design 轉成版本化控制清單，確認哪些控制能自動化、哪些需要人工核准。
- 未知：需要驗證 brownfield 專案中 context graph、語意檢索、spec extraction 與 drift detection 的準確率、更新成本與誤報率。
- 未知：需要獨立重現 R2Code 與 ReqToCode 的結果，確認其對實務語言、既有程式庫與大型 repository 的適用範圍。

## 結論

若需求新增為「最穩健的系統、可以精準對照需求書」，答案不是選擇最會自動產碼的單一 agent，而是建立 bounded autonomy assurance architecture。先把需求書轉為受控 baseline 與唯一 Requirement IDs，再建立 Requirement -> Design -> Task -> Code -> Test -> Evidence 的雙向 traceability graph；brownfield 專案加上 repository context graph 與 drift gate；安全要求映射 NIST、OWASP 與組織政策並由 policy-as-code 執行；agent 只能在隔離 runtime 中自動工作，baseline 變更、安全例外、驗證失敗與部署必須經核准或升級。這樣系統才具備可重現、可稽核、可維護的穩健性。

## 建議

### 1. 可實作性

現有技術已足以做出可用的第一版穩健系統，但應分階段組裝。先建立可稽核的 requirements registry 與 traceability graph，再接入 brownfield context、隔離執行、安全 policy gate 與 benchmark harness。以下每一項都可獨立交付，也附上可交給 agent 的後續研究提示詞。

#### 受控需求基線與雙向 Traceability Graph

- 目的：把需求書從 prose 文件轉成可查核的 baseline，使每個需求都能正反向對照設計、任務、程式碼、測試與 evidence。
- 技術組合：JSON Schema 或 YAML schema, Requirements Registry, Traceability Matrix, SQLite 或 graph database, OpenSpec 或 Spec Kit 類型 artifacts, CI coverage check
- 實作流程：解析需求書 -> 配發 Requirement ID -> 記錄版本、owner、驗收條件與安全控制 -> 建立 Design、Task、Code、Test、Evidence refs -> 每次 PR 更新 traceability graph -> CI 檢查未覆蓋需求與 orphan artifacts。
- 最小交付物：requirements.yaml、traceability.json、產生矩陣的 CLI、PR coverage report、baseline change approval 紀錄。
- 驗收標準：所有 in-scope requirements 具有唯一 ID；每一項至少連到設計與驗證證據；可反向找出未對應需求的 code 或 design；baseline 變更具有 audit trail。
- 依據來源：S-001, S-004, S-013, S-079, S-080, S-081, S-082
- 後續研究提示詞：`研究可落地的 requirements registry 與雙向 traceability graph。比較 JSON Schema、YAML、SQLite、graph database 與現有開源 SDD artifacts；設計 Requirement -> Design -> Task -> Code -> Test -> Evidence schema、CLI、PR report 與 baseline change workflow。列出可直接採用的 library、資料模型、遷移步驟與驗收測試。`

#### Brownfield Repository Context 與 Drift Gate

- 目的：讓 agent 在既有程式庫中使用可更新的 repository knowledge，而不是依賴一次性長 prompt；同步偵測 spec-code drift 與變更影響。
- 技術組合：Tree-sitter, SQLite, SCIP 或 code graph, semantic retrieval, OpenLore/spec-gen 類型 living spec, preflight CI gate
- 實作流程：索引 repository -> 建立 symbol、call graph 與模組摘要 -> 關聯 requirements 與 code refs -> 修改前提供限定 context -> PR 後重算受影響節點 -> drift gate 阻擋過期 spec 或缺少 impact analysis 的變更。
- 最小交付物：repository index、context retrieval API、requirement-code link、drift report、CI preflight command。
- 驗收標準：對選定 brownfield repository 可重建索引；需求變更能列出影響模組；程式碼修改若缺少 spec 更新會被檢出；量測索引更新時間、誤報率與人工修正成本。
- 依據來源：S-017, S-018, S-029, S-069, S-071, S-074, S-077, S-078
- 後續研究提示詞：`針對 brownfield SDD 系統研究 repository context graph 與 drift detection。比較 Tree-sitter、SCIP、SQLite、向量檢索、OpenLore/spec-gen 類型工具；提出 incremental indexing、impact analysis、spec staleness gate 與 context retrieval benchmark。輸出技術選型表、PoC 流程與維護成本量測方式。`

#### 隔離執行、驗證矩陣與人工升級

- 目的：讓 agent 可以自動工作，但每次執行都有隔離環境、可觀測狀態、驗證證據與明確 escalation 邊界。
- 技術組合：git worktree 或 ephemeral workspace, Symphony-style scheduler, retry 與 reconciliation, CI test runner, static analysis, evidence store, approval gate
- 實作流程：由 approved task 啟動隔離 workspace -> agent 產生 patch 與 tests -> 執行 verifier matrix -> 保存 logs、測試與差異 evidence -> 通過者進入 review -> baseline 變更、安全例外、反覆失敗或 deploy 一律升級。
- 最小交付物：task runner、workspace manager、verifier matrix、evidence bundle、retry policy、escalation rules。
- 驗收標準：平行任務不互相污染；每個 patch 可追溯 task 與 requirement；重試次數受控；失敗 evidence 可重現；規定的高風險事件不會自動越過人工 gate。
- 依據來源：S-020, S-021, S-022, S-027, S-043, S-044, S-063, S-067, S-070
- 後續研究提示詞：`研究 bounded autonomy coding-agent runtime。比較 git worktree、container、ephemeral workspace、scheduler、retry、reconciliation、observability 與 evidence bundle 的開源實作；設計 verifier matrix 與 escalation policy。輸出最小架構、事件狀態機、失敗模式與整合測試。`

#### 安全需求映射與 Policy-as-Code Gate

- 目的：將安全要求變成版本化、可測試、可阻擋部署的控制，而不是只存在於文件或 prompt。
- 技術組合：NIST SSDF, OWASP ASVS, OWASP AISVS, OWASP SCVS, OPA/Rego, Conftest, OWASP DevGuard, SBOM 與 provenance
- 實作流程：選定安全控制 baseline -> 映射至 Requirement IDs -> 將可自動化控制寫成 Rego 或等價規則 -> 在 PR、CI、artifact 與 deploy 階段執行 -> 保存 policy version、decision 與 exception approval。
- 最小交付物：security-controls.yaml、control-to-requirement mapping、Rego policy pack、Conftest/CI job、exception workflow、audit report。
- 驗收標準：每一項安全控制具有版本與 owner；可自動化規則在 PR 或 deploy 前執行；例外必須記錄理由與核准者；policy decision 可重現。
- 依據來源：S-083, S-084, S-085, S-086, S-087, S-088, S-089, S-090, S-091, S-096, S-097
- 後續研究提示詞：`研究如何將 NIST SSDF、OWASP ASVS、AISVS、SCVS 與組織政策映射成 SDD requirements，再以 OPA/Rego、Conftest、DevGuard 或等價工具建立 PR、CI、artifact、deploy gates。輸出控制矩陣、policy pack 結構、例外流程與驗收案例。`

#### 組織專用 Benchmark Harness

- 目的：驗證候選架構是否真的穩健，避免只用 patch success 或產品宣稱判定成效。
- 技術組合：requirements baseline fixture, SWE-Bench Pro 類型長任務, ContextBench 類型 retrieval 測試, OmniCode 與 SWE Atlas 類型多工作負載, metrics dashboard
- 實作流程：固定 repository、requirements、模型與工具權限 -> 執行相同任務 -> 收集 requirement coverage、traceability completeness、orphan artifacts、drift、first-pass verification、human interventions、security exceptions、完成時間與維護成本 -> 分成熟度與特化軸比較。
- 最小交付物：benchmark fixtures、runner、metric schema、結果 dashboard、候選方案比較表。
- 驗收標準：同一任務可重複執行；指標定義明確；結果能區分成熟度與特化能力；報告不再只依賴單一 patch benchmark。
- 依據來源：S-072, S-074, S-075, S-078, S-092, S-093
- 後續研究提示詞：`設計一套組織專用 SDD AI benchmark harness。參考 SWE-Bench Pro、ContextBench、OmniCode、SWE Atlas，建立固定 requirements baseline 與 brownfield repository fixtures；定義 traceability、drift、驗證、安全、人工介入、長任務與維護成本指標。輸出 runner 架構、資料格式與最小實驗計畫。`

### 2. 開源工具選型

以下排名以「最穩健、可以精準對照需求書」為主目標，而不是以 star 數量或功能數量排序。沒有任何單一開源工具能完整覆蓋 Requirements Registry、雙向 Traceability Graph、brownfield context、隔離 runtime、驗證矩陣與安全 policy gate。單一工具推薦適合先建立主幹能力；正式導入若風險較高，應採多工具組合並以自有 schema 與 CI contract 串接。

#### 2.1 只使用一個開源工具：前三種推薦

如果限制只能選一個工具，優先選擇能保存需求基線與變更歷史的工具；若核心風險改成長時間自動執行或 brownfield drift，再改選第二或第三名。

##### 第 1 名：OpenSpec

- 推薦理由：最適合作為單一工具起點。它把目前有效規格與 proposed changes 分離，使用 proposal、spec delta、design、tasks、validate 與 archive 保存可 review、可追溯的變更歷史；brownfield-first，且可接入多種 coding assistants。對「精準對照需求書」而言，先穩定需求基線比先放大 autonomous loop 更重要。
- 適用情境：想用最低導入成本建立 requirements baseline、spec delta、tasks 與人工 review gate；需要跨多種 coding assistants；既有專案要漸進採用 SDD。
- 主要能力：brownfield-first, source-of-truth specs, change folders, proposal/spec delta/design/tasks, validate 與 archive, 多 coding assistant 整合, MIT license
- 必須接受的缺口：OpenSpec 本身不是完整雙向 traceability graph，也不內建 code/test evidence、static-analysis drift graph、隔離 runtime 或安全 policy-as-code。正式 assurance 仍需額外補上 Requirement IDs、CI mapping 與安全 gate。
- 最小導入方式：執行 openspec init；在 openspec/specs 維護目前有效規格，在 openspec/changes 保存 proposal、spec delta、design 與 tasks；為每項 requirement 加唯一 ID；PR 必跑 openspec validate，完成後 archive。
- 依據來源：S-004, S-048, S-049
- 後續研究提示詞：`以 OpenSpec 作為唯一開源工具，設計最小可行的 requirements assurance workflow。研究如何在 openspec/specs 與 openspec/changes 中加入 Requirement IDs、acceptance criteria、design refs、task refs、PR validate 與 archive audit trail；列出 OpenSpec 原生能力、需要自製的 CI glue、導入步驟與驗收案例。`

##### 第 2 名：cc-sdd

- 推薦理由：如果單一工具的重點是從 approved specs 走到長時間自動實作，cc-sdd 比純規格工具完整。它提供 discovery、requirements、design、tasks 與 autonomous implementation；每個 task 使用 fresh implementer、TDD、獨立 reviewer、auto-debug，並以 boundary 與 dependency annotations 控制工作範圍。
- 適用情境：需求已相對明確，希望單一 harness 同時處理規格拆解與長時間實作；想保留 task 邊界、TDD、review 與中斷後 resume；需要支援 Codex、Claude Code 等多種 agent。
- 主要能力：approved specs to autonomous implementation, fresh implementer per task, TDD, independent reviewer, auto-debug, boundary-first tasks, resume, multi-agent skills
- 必須接受的缺口：cc-sdd 偏向 implementation harness；它不等於完整 requirements registry，也不提供 OpenLore 類型 static-analysis knowledge graph、完整 spec-code drift gate、組織安全 policy pack 或 Symphony 類型 daemon runtime。
- 最小導入方式：先以 discovery 建立 brief 或 roadmap，再產生 requirements、design、tasks；人工核准 specs 後才啟動 long-running implementation；把 Requirement IDs、Boundary、Depends 與驗證 evidence 寫入模板。
- 依據來源：S-027
- 後續研究提示詞：`以 cc-sdd 作為唯一開源工具，設計 approved specs 到 autonomous implementation 的穩健流程。研究 discovery、requirements、design、tasks、boundary、dependency、TDD、independent reviewer、auto-debug、resume 與 evidence 保存；補出 Requirement IDs 與安全例外 gate 的模板。`

##### 第 3 名：OpenLore

- 推薦理由：如果最大風險是 brownfield codebase、context decay 與 spec-code drift，OpenLore 是最有價值的單工具。它以 static analysis 建立 SQLite call graph 與 clusters，提供 living specs、drift detection、pre-commit decision gate 與 graph-native MCP tools，可將 repository knowledge 持續交給 agent。
- 適用情境：大型或既有 repository；需求書不完整；需要 reverse engineering、影響分析、living specs、drift detection 與跨 session architectural memory。
- 主要能力：static analysis, SQLite call graph, clusters, living OpenSpec specs, drift detection, pre-commit decision gate, graph-native MCP, incremental indexing
- 必須接受的缺口：OpenLore 不是完整 SDD task runner 或隔離 orchestration runtime。動態 dispatch、metaprogramming 與 eval 類模式無法由 static analysis 完整捕捉；LLM 產生的 specs 也必須人工覆核。
- 最小導入方式：先執行 offline analyze 產生 repository graph 與 CODEBASE digest；啟用 MCP context；對關鍵模組產生並人工核准 living specs；在 PR 前加入 drift 或 decision gate。
- 依據來源：S-029
- 後續研究提示詞：`以 OpenLore 作為唯一開源工具，針對 brownfield repository 設計最小導入。研究 static analysis、SQLite graph、orient、living specs、drift detection、pre-commit gate 與 incremental indexing；列出動態語言限制、人工覆核流程、誤報量測與 Requirement IDs 補強方式。`

#### 2.2 多個開源工具配合：前三種推薦

多工具組合的原則是分層：一個工具負責需求基線，一個工具負責 brownfield context 與 drift，一個工具負責執行或驗證，最後用 policy-as-code 把安全與組織規則放進 CI。以下三種組合依一般適用性排序；實際採用前仍需用組織專用 benchmark 驗證。

##### 第 1 名：平衡型穩健組合：OpenSpec + OpenLore + cc-sdd + OPA/Rego + Conftest

- 工具組合：OpenSpec, OpenLore, cc-sdd, OPA/Rego, Conftest
- 目標：在不先自建大型平台的情況下，同時具備受控需求基線、brownfield context、drift gate、TDD 實作、獨立 reviewer 與安全政策檢查。
- 角色分工：OpenSpec 保存 source-of-truth specs、proposal 與 spec delta；OpenLore 建立 repository graph、living specs 與 drift gate；cc-sdd 將核准 specs 拆成 boundary-aware tasks，執行 TDD、review 與 auto-debug；OPA/Rego 保存組織與安全規則；Conftest 在 PR、CI 與 deploy 前執行 policy tests。
- 實作流程：需求書 -> OpenSpec Requirement IDs 與 change proposal -> OpenLore 產生 repository context、impact analysis 與 drift 狀態 -> 人工核准 specs -> cc-sdd 逐 task 實作、測試、review、auto-debug -> 將 traceability、測試 evidence 與 artifacts 轉成 structured input -> Conftest/OPA gate -> merge 與 OpenSpec archive。
- 推薦理由：這是目前最實際的第一推薦：每一層工具責任清楚，能從需求基線一路走到 evidence 與政策 gate；不要求先自建常駐 daemon，也保留人工核准點。
- 取捨：OpenSpec 與 cc-sdd 使用不同 artifact 習慣，需要建立 mapping adapter；OpenLore 產生的 living specs 必須人工覆核；OPA/Rego policy pack 需要持續維護。
- 最小交付物：OpenSpec Requirement ID convention、OpenLore context/drift job、OpenSpec-to-cc-sdd mapping script、cc-sdd evidence bundle、security-controls.yaml、Rego policies、Conftest CI job。
- 驗收標準：每個已核准 requirement 能對照 proposal、task、code、test 與 evidence；brownfield 修改具 impact analysis；drift 與 orphan artifact 可被檢出；安全 policy 違規能在 merge 或 deploy 前阻擋；失敗可升級人工處理。
- 依據來源：S-004, S-027, S-029, S-083, S-085, S-088, S-089, S-090, S-091
- 後續研究提示詞：`研究並實作 OpenSpec + OpenLore + cc-sdd + OPA/Rego + Conftest 的整合 PoC。定義 Requirement IDs、OpenSpec-to-cc-sdd mapping、OpenLore drift report、evidence bundle、security-controls.yaml、Rego input schema、CI jobs 與人工 approval gates。列出 adapter 程式、資料格式、端到端驗收案例與維護成本。`

##### 第 2 名：營運型隔離執行組合：OpenSpec + OpenLore + Symphony + OPA/Rego + Conftest

- 工具組合：OpenSpec, OpenLore, OpenAI Symphony, OPA/Rego, Conftest
- 目標：針對持續 issue-to-implementation、平行 agent、隔離 workspace、retry、reconciliation 與可觀測性，建立可營運的 bounded autonomy runtime。
- 角色分工：OpenSpec 維護需求與變更基線；OpenLore 提供 repository context、living specs 與 drift；Symphony 依 issue 建立隔離 workspace，載入 repository-owned WORKFLOW.md，處理 dispatch、retry、reconciliation 與 structured logs；OPA/Rego 與 Conftest 執行安全與部署政策。
- 實作流程：OpenSpec approved change -> 建立或更新 issue -> Symphony poll issue 並建立 deterministic workspace -> WORKFLOW.md 要求先查 OpenLore context、實作、測試與保存 evidence -> Symphony reconciliation、retry 與 escalation -> Conftest/OPA gate -> Human Review -> archive specs。
- 推薦理由：當工作量已經需要常駐 runner 與多個平行 agent 時，這個組合比只用腳本穩健。Symphony 把 runtime contract、workspace、retry 與 observability 明文化，適合進一步平台化。
- 取捨：整合成本較高；Symphony 是 scheduler/runner，不替你決定 sandbox、安全 posture 或 ticket business logic；必須自行定義 WORKFLOW.md、issue adapter、approval gate 與 evidence storage。
- 最小交付物：OpenSpec-to-issue adapter、WORKFLOW.md、OpenLore MCP configuration、Symphony runtime、structured logs、evidence store、OPA/Rego policy pack、Conftest CI/deploy gate。
- 驗收標準：每個 issue 對照已核准 change；每次執行在獨立 workspace；中斷與 transient failure 可 retry；狀態變更可 reconciliation；logs 可依 requirement、issue 與 session 查詢；高風險事件停在 Human Review。
- 依據來源：S-004, S-020, S-021, S-029, S-089, S-090, S-091
- 後續研究提示詞：`研究並實作 OpenSpec + OpenLore + Symphony + OPA/Rego + Conftest 的 bounded autonomy runtime。定義 OpenSpec approved change 到 issue 的 adapter、WORKFLOW.md、OpenLore MCP context、workspace lifecycle、retry、reconciliation、structured logs、evidence store、Human Review 與 deploy policy gates。輸出事件狀態機與故障測試。`

##### 第 3 名：Claude Code 品質工程組合：OpenSpec + OpenLore + MoAI-ADK + OPA/Rego + Conftest

- 工具組合：OpenSpec, OpenLore, MoAI-ADK, OPA/Rego, Conftest
- 目標：若團隊已以 Claude Code 為核心，使用現成 SPEC-first harness、TDD/DDD、code maps、worktrees、agent teams 與 metrics，快速建立較完整的品質工程流程。
- 角色分工：OpenSpec 管理需求 baseline 與變更；OpenLore 補強 brownfield repository graph 與 drift；MoAI-ADK 依專案狀態選擇 TDD 或 DDD，執行 self-verify loop、code maps、progress persistence、worktrees、agent teams 與 task metrics；OPA/Rego 與 Conftest 負責安全政策。
- 實作流程：OpenSpec proposal 與 Requirement IDs -> OpenLore context 與 impact analysis -> MoAI plan/run/sync 執行 SPEC-first TDD 或 DDD -> 保存 task metrics、tests、PR 與 evidence -> Conftest/OPA gate -> review -> archive specs。
- 推薦理由：適合希望快速取得完整 harness engineering 能力的 Claude Code 團隊。相較自行組裝 task runner，它已有品質迴圈、brownfield DDD、worktree 與 metrics，可更快進入 benchmark。
- 取捨：對 Claude Code 綁定較強；MoAI-ADK 功能面廣，團隊需要先縮小啟用範圍；OpenSpec、OpenLore 與 MoAI artifacts 仍需 mapping；不能把內建品質框架視為組織安全政策的替代品。
- 最小交付物：OpenSpec-to-MoAI SPEC mapping、OpenLore MCP configuration、MoAI project config、TDD/DDD 驗證流程、task metrics export、OPA/Rego policy pack、Conftest CI job。
- 驗收標準：Requirement IDs 可連到 MoAI SPEC、task、PR 與 tests；brownfield 專案有 characterization tests 與 impact analysis；metrics 可用於 benchmark；安全政策違規可阻擋 merge 或 deploy。
- 依據來源：S-004, S-028, S-029, S-089, S-090, S-091
- 後續研究提示詞：`研究並實作 OpenSpec + OpenLore + MoAI-ADK + OPA/Rego + Conftest 的 Claude Code 品質工程 PoC。定義 OpenSpec-to-MoAI SPEC mapping、OpenLore context、TDD/DDD 選擇、worktrees、task metrics、evidence export 與 CI policy gates。列出 Windows/WSL 限制、最小啟用功能與 benchmark 計畫。`

### 3. 未來性

目前可實作的系統仍以 registry、矩陣、CI gate 與人工核准維持穩健性。未來方向不是取消這些控制，而是降低維護成本、提高自動連結準確率，並逐步把 assurance 提前到編譯期與組織級 benchmark。

#### Compile-time Traceability

- 當前缺點：現有 traceability matrix 多半在 CI 或 review 階段檢查，需求與程式碼連結仍可能延遲更新。
- 演進方向：研究 language-native metadata、Traceable<T> 類型或 annotation，使部分 requirement-code 關係與必要證據能在編譯期驗證。
- 啟動條件：當 registry 與 CI traceability 已穩定，且團隊能接受語言或 framework 層級的標註成本時啟動。
- 依據來源：S-095
- 後續研究提示詞：`評估 ReqToCode 類型 compile-time traceability 對實務語言與大型 repository 的適用性。研究 annotation、type metadata、compiler plugin、IDE support、遷移成本與無法靜態驗證的邊界；提出 PoC 與 benchmark。`

#### AI 輔助 Requirement-to-Code Link Recovery

- 當前缺點：brownfield 專案人工補齊 requirement-code links 的成本高，歷史系統常缺少完整需求資料。
- 演進方向：以 AI 提出候選 links，再透過 retrieval、consistency verification 與人工覆核逐步建立可信 traceability graph。
- 啟動條件：當人工建鏈成本成為導入瓶頸，且有可用的已核准 links 作為驗證集時啟動。
- 依據來源：S-094
- 後續研究提示詞：`研究 R2Code 類型 requirements-to-code traceability link recovery。針對 brownfield repository 建立人工標註驗證集，比較 retrieval、reranking、consistency verification、人工覆核與 confidence threshold；輸出 precision、recall、F1、token cost 與誤連結風險。`

#### Drift 與維護成本的量化

- 當前缺點：living spec、context graph 與 drift gate 會提高穩健性，但索引更新、誤報與人工維護成本尚缺少一致量測。
- 演進方向：建立長期觀測指標，量測 spec staleness、impact analysis 準確率、索引更新成本、誤報率與修復時間。
- 啟動條件：當 brownfield context PoC 進入持續使用階段時立即啟動。
- 依據來源：S-029, S-069, S-071, S-074, S-077, S-078
- 後續研究提示詞：`研究 SDD living spec 與 context graph 的維護成本。定義 drift detection precision、recall、staleness age、impact analysis accuracy、index update time、human correction time；設計至少三個月的觀測計畫與 dashboard。`

#### 安全控制的版本化演進

- 當前缺點：安全標準、AI 風險與供應鏈政策會持續更新；固定 policy pack 可能逐漸與最新要求脫節。
- 演進方向：建立 control catalog 版本管理、policy migration、exception expiry、SBOM/provenance evidence 與 deploy attestation。
- 啟動條件：當第一版 policy-as-code gate 上線後，依安全標準更新週期與內部風險審查持續執行。
- 依據來源：S-083, S-085, S-086, S-087, S-088, S-096, S-097
- 後續研究提示詞：`設計安全控制 catalog 與 policy pack 的版本化演進流程。研究 NIST SSDF、OWASP ASVS、AISVS、SCVS、SBOM、provenance、attestation、exception expiry 與 migration；輸出版本策略、變更影響分析與自動化檢查。`

#### 以風險調整 Autonomy Level

- 當前缺點：完全自動與完全人工審核都不是最佳解；不同 repository、需求與安全等級需要不同自治程度。
- 演進方向：依 traceability completeness、測試品質、安全風險、歷史失敗率與 benchmark 結果，動態限制 agent 可執行的動作與需要升級的事件。
- 啟動條件：當 benchmark harness 已累積足夠實測資料，能以證據設定門檻時啟動。
- 依據來源：S-021, S-063, S-067, S-070, S-092, S-093
- 後續研究提示詞：`研究 risk-adjusted autonomy policy。根據 requirement coverage、traceability completeness、test confidence、security severity、repository criticality、historical failure rate 與 benchmark 結果，定義自治等級、approval gates、escalation thresholds 與回退策略。`


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
- `S-079` [NASA SWE-059 Requirements to Design Traceability](https://swehb.nasa.gov/pages/viewpage.action?pageId=16453101)
- `S-080` [NASA SWE-052 Bidirectional Traceability](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052+-+Bidirectional+Traceability)
- `S-081` [NASA SWE-067 Verify Implementation](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604539/SWE-067%2B-%2BVerify%2BImplementation)
- `S-082` [NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)
- `S-083` [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)
- `S-084` [NIST NCCoE DevSecOps Practices](https://pages.nist.gov/nccoe-devsecops/)
- `S-085` [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- `S-086` [OWASP AISVS](https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/)
- `S-087` [OWASP SCVS Usage and Levels](https://scvs.owasp.org/scvs/using-scvs/)
- `S-088` [OWASP DevGuard](https://owasp.org/www-project-devguard/)
- `S-089` [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs)
- `S-090` [OPA Pull Request Check Policies](https://www.openpolicyagent.org/docs/cicd/pr-checks)
- `S-091` [Conftest Documentation](https://www.conftest.dev/)
- `S-092` [Scale AI SWE-Bench Pro Article](https://scale.com/blog/swe-bench-pro)
- `S-093` [Scale Labs SWE-Bench Pro Paper Page](https://labs.scale.com/papers/swe_bench_pro)
- `S-094` [R2Code Requirements-to-Code Traceability](https://arxiv.org/abs/2604.22432)
- `S-095` [ReqToCode Compile-Time Traceability](https://arxiv.org/abs/2603.13999)
- `S-096` [CISA Secure by Design](https://www.cisa.gov/resources-tools/resources/secure-by-design)
- `S-097` [CISA Product Security Bad Practices](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices)
