# SDD AI 全自動開發：最穩健且可精準對照需求書的 Assurance Architecture

## 報告資訊

- 報告 ID：`sdd-ai-robust-requirements-20260531-v9`
- 版本：`9.0.0`
- 產生時間：`2026-05-31T14:53:09Z`
- 資料截止時間：`2026-05-31T14:00:00Z`
- 整體可信度：`medium`
- 品質分數：`93/100`
- 結構完整度：`100/100`

## 摘要

本報告以 97 份來源重構 SDD AI 全自動開發的比較方式，其中 79 份為官方文件、repository 或研究來源，另有 18 份專業文章作為補充脈絡。面對工具定位衝突時，不應把所有工具壓成單一排名，而應分成兩個軸：第一軸是從輕量 Markdown specification、結構化 artifact、living spec 與雙向 traceability，到 executable architecture、compile-time traceability 與 policy-as-code gate 的成熟度；第二軸是效率迴圈、brownfield context、security policy、drift 維護、runtime orchestration 與 benchmark assurance 等特化能力。如果新增需求是「最穩健，且可以精準對照需求書」，推薦採用 bounded autonomy assurance architecture：受控需求基線、雙向 traceability graph、repository context graph、task graph、隔離執行環境、驗證矩陣、policy-as-code gate、evidence store 與人工升級機制。核心不是讓 agent 自由產碼，而是讓每一項需求都能沿著 Requirement -> Design -> Task -> Code -> Test -> Evidence 正反向查核。

## 品質指標

- 關鍵主張覆蓋率：`30/30`
- 高品質證據分數：`22/25`
- 雙向可追溯性分數：`20/20`
- 衝突與未知處理分數：`11/15`
- 新鮮度與可重現性分數：`10/10`
- 說明：97 筆來源；79 筆主要來源；79 筆 A/B 層級來源；3 個 open resolution items。

## 研究問題

- SDD AI 全自動開發的衝突應如何按成熟度與特化能力分層比較？
- 最穩健且可精準對照需求書的系統，最低限度需要哪些架構元件與證據？
- 哪些未知項目必須透過 benchmark 或安全政策驗證，而不能只依賴產品宣稱？
- 如何讓需求、設計、程式碼、測試與安全控制形成可查核的雙向鏈結？

## 研究範圍

- 目標受眾：需要規劃 SDD AI 自動開發平台、治理流程與 PoC 的技術決策者
- 地區：global
- 語言：zh-TW, en
- 時間範圍：截至 2026-05-31T14:00:00Z 的本地 snapshot

### 包含範圍

- SDD 定義與 workflow
- 開源工具與官方文件
- requirements traceability
- brownfield context 與 drift
- security policy-as-code
- runtime orchestration
- benchmark 與研究原型

### 排除範圍

- 未保存原始 snapshot 的搜尋摘要
- 未經獨立重現的效能排行
- 把單一工具描述成完整 assurance architecture 的宣稱

## 方法

研究流程依 append-only crawl queue 保存 97 份來源；每一份來源均保存 raw snapshot、metadata、summary.md 與 catalog 項目。其中 79 份為官方文件、repository 或研究來源，18 份專業文章只用於補充脈絡。本輪新增 NASA SWE-052、SWE-059、SWE-067 與 requirements management，NIST SSDF 與 NCCoE DevSecOps，OWASP ASVS、AISVS、SCVS、DevGuard，OPA、OPA pull request checks、Conftest，CISA Secure by Design 與 Product Security Bad Practices，以及 SWE-Bench Pro、R2Code、ReqToCode。判讀時優先採官方規範與官方文件；arXiv 預印本只作為新方向線索，不視為已建立的產業事實。比較框架拆成成熟度軸與特化軸，避免不同問題的工具被混成單一排名。

## 關鍵發現

### `C-001`

- 主張：若目標是穩健與精準對照需求書，需求書必須成為受控 baseline。每一項需求應有唯一 ID、版本、來源、owner、優先級、驗收條件、變更紀錄與核准狀態；只有 prose 文件不足以支撐自動查核。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA requirements management、NASA traceability 規範與多個 SDD 工具均要求受控需求與結構化 artifact。
- 支持來源：S-001, S-003, S-004, S-008, S-010, S-013, S-032, S-079, S-080, S-081, S-082
- 反對或限制來源：無
- 備註：無

### `C-002`

- 主張：穩健架構的核心是雙向 traceability：Requirement -> Design -> Task -> Code -> Verification/Test -> Evidence，並能反向找出 orphan design、額外程式碼、未覆蓋需求、缺少驗證與 non-conformance。
- 類型：`fact`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA SWE-052、SWE-059、SWE-067 對雙向追溯、需求落實與驗證提供直接規範。
- 支持來源：S-013, S-079, S-080, S-081, S-082
- 反對或限制來源：無
- 備註：無

### `C-003`

- 主張：成熟度基準應分層：L1 輕量 Markdown spec；L2 結構化 requirements/design/tasks artifacts；L3 living spec、repository context 與 drift detection；L4 executable architecture、compile-time traceability 與 policy-as-code enforcement。這是能力階梯，不是所有專案一開始都必須採 L4。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：現有工具從 Spec Kit、OpenSpec、SpecDD 到 OpenLore、Akka 與新興 ReqToCode 呈現明確的能力遞進。
- 支持來源：S-001, S-004, S-008, S-010, S-013, S-029, S-068, S-095
- 反對或限制來源：無
- 備註：ReqToCode 為預印本，L4 的 compile-time 方向仍需實證。

### `C-004`

- 主張：特化能力應獨立比較：效率型強調 autonomous loop 與吞吐量；brownfield 型強調 repository context 與漸進導入；security 型強調安全控制與 policy gate；drift 維護型強調 living spec、staleness 與 impact analysis；runtime 型強調隔離、排程、重試與可觀測性。
- 類型：`inference`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Taskmaster、Flow Next、Ralph variants、OpenLore、Kata、Threatspec、Symphony、Rover 等來源各自優化不同指標。
- 支持來源：S-018, S-019, S-021, S-022, S-029, S-034, S-035, S-037, S-038, S-039, S-055, S-066, S-067, S-077
- 反對或限制來源：無
- 備註：無

### `C-005`

- 主張：brownfield 專案若要求穩健，應加入 repository context graph、語意檢索、程式結構索引、living spec 與 drift/preflight gate，避免 agent 只憑單次 prompt 或單一長文件工作。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：Kata、OpenLore、GSD 與 context engineering 來源均指出 repository-aware context 與 drift 管理的重要性。
- 支持來源：S-017, S-018, S-029, S-069, S-071, S-074, S-077, S-078
- 反對或限制來源：無
- 備註：無

### `C-006`

- 主張：安全政策不可只放在說明文字中。應把 NIST SSDF、OWASP ASVS、AISVS、SCVS 與組織內規映射成版本化 requirements，並透過 OPA/Rego、Conftest 或等價機制在 pull request、CI 與部署前執行可稽核 gate。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NIST、OWASP、OPA 與 Conftest 官方資料共同支持 outcome-based secure SDLC、可測試控制與 policy-as-code enforcement。
- 支持來源：S-083, S-084, S-085, S-086, S-087, S-088, S-089, S-090, S-091, S-096, S-097
- 反對或限制來源：無
- 備註：無

### `C-007`

- 主張：需求對照資料模型至少需要 Requirement ID、source、version、owner、priority、acceptance criteria、security control refs、design refs、task refs、code refs、test refs、evidence refs、status 與 change history。每次修改都應重新計算覆蓋率與 orphan artifacts。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：NASA traceability、requirements management 與 OWASP 版本化控制的組合推導出可稽核資料模型。
- 支持來源：S-079, S-080, S-081, S-082, S-085, S-086, S-087
- 反對或限制來源：無
- 備註：無

### `C-008`

- 主張：最穩健的執行模式是 bounded autonomy：agent 可以自動產生設計、tasks、patch、tests 與 evidence，但 baseline 變更、安全例外、未解驗證失敗與部署決策必須升級至人工或明確核准 gate。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：SDD workflow、Symphony runtime、AWS GovTech、Anthropic agent workflow 與 CISA Secure by Design 均支持受控邊界、核准與責任歸屬。
- 支持來源：S-002, S-010, S-021, S-023, S-027, S-033, S-063, S-067, S-070, S-096, S-097
- 反對或限制來源：無
- 備註：無

### `C-009`

- 主張：未知能力必須用 benchmark 驗證。不能只看 patch success；還要測 requirement coverage、traceability completeness、orphan artifacts、spec-code drift、first-pass verification、human interventions、security exceptions、長任務完成率與 brownfield context retrieval。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`medium`
- 理由：ContextBench、OmniCode、SWE Atlas 與 SWE-Bench Pro 支持擴充 benchmark 維度的方向，但組織專用 metric schema、fixtures 與門檻仍需透過 PoC 建立。
- 支持來源：S-072, S-074, S-075, S-078, S-092, S-093
- 反對或限制來源：無
- 備註：無

### `C-010`

- 主張：R2Code 與 ReqToCode 代表值得追蹤的新方向：前者聚焦 requirements-to-code traceability link accuracy，後者探索 language-native metadata 與 compile-time verification。兩者可作為實驗候選，但尚不能取代成熟的 traceability matrix 與 CI gate。
- 類型：`inference`
- 重要程度：`medium`
- 可信度：`medium`
- 理由：兩項來源為近期預印本，方向具體但仍需要獨立重現與工程驗證。
- 支持來源：S-094, S-095
- 反對或限制來源：無
- 備註：避免把研究原型當成已驗證產品能力。

### `C-011`

- 主張：建議的穩健 assurance architecture 由九個元件組成：Requirements Registry、Traceability Graph、Repository Context Graph、Plan/Task Graph、Isolated Runtime、Verifier Matrix、Policy Gates、Evidence Store、Escalation Workflow。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：這是把 SDD artifacts、NASA traceability、brownfield context、runtime isolation 與安全政策來源整合後的架構推論。
- 支持來源：S-001, S-004, S-021, S-022, S-029, S-055, S-068, S-079, S-080, S-081, S-088, S-089, S-090, S-091
- 反對或限制來源：無
- 備註：無

### `C-012`

- 主張：採用順序應由證據需求驅動：先建立 requirement IDs、baseline 與 traceability matrix；再接入 code/test evidence 與 drift detection；之後加入安全 policy gates；最後才擴大 autonomous loop、平行 agents 與 compile-time 實驗。
- 類型：`recommendation`
- 重要程度：`critical`
- 可信度：`high`
- 理由：此順序優先建立可查核性，再擴大自動化風險邊界。
- 支持來源：S-010, S-021, S-029, S-063, S-067, S-079, S-080, S-081, S-083, S-088
- 反對或限制來源：無
- 備註：無

## 限制

- 97 份來源涵蓋官方規範、官方文件、開源專案、工程文章與預印本；證據強度並不相同，因此報告對研究原型保持中等信心。
- 本報告建立的是選型與 assurance architecture，不是對所有候選工具完成同一環境下的實測排名。
- 部分來源抓取失敗項目仍保留於 append-only queue，包括 Red Hat HTTP 403 與 OpenAI 網頁 SSL 憑證驗證失敗，未被靜默移除。
- compile-time traceability 與 requirement-to-code AI linking 仍屬新興方向，不能取代 baseline、矩陣、測試與政策 gate。
- 47 份 GitHub 來源已解析 commit permalink；其餘持續更新頁面若無永久版本，依本地 snapshot hash 與 recheck_after 保存可重現邊界，後續引用最新狀態前仍需重新確認。

## 衝突與未知

- 已解決衝突：`3`
- 未關閉未知：`4`
- `RU-001` `open`：不同工具組合的實際穩健性比較
- `RU-002` `partially_resolved`：安全政策哪些可自動化、哪些需要人工核准
- `RU-003` `open`：Brownfield context graph 與 drift detection 的準確率及維護成本
- `RU-004` `open`：R2Code 與 ReqToCode 是否適用大型實務 repository

### 解決矩陣

三個衝突已可透過分類與決策規則收斂。四個未知不能只靠文件搜尋全部關閉：安全控制 baseline 可立即建立，但仍需組織核准；benchmark、brownfield 準確率與新興研究重現必須透過實作或實驗取得證據。

#### 衝突解決矩陣

##### `RC-001` 輕量 SDD 與 executable architecture 的比較方式

- 狀態：`resolved`
- 判斷：不再把輕量 Markdown spec 與 executable architecture 當成互斥答案或單一排名，而是視為 L1 到 L4 的成熟度階梯。專案依風險選擇最低足夠層級；「最穩健、可精準對照需求書」至少需要 L2 結構化 artifacts 與雙向 traceability，brownfield 或高風險專案再加入 L3 drift gate 與 L4 policy enforcement。
- 解決方式：以共同控制目標重新分類：artifact 結構化、traceability、drift、enforcement。將工具放入成熟度層級，而不是互相取代。
- 依據來源：S-001, S-004, S-008, S-010, S-013, S-029, S-068, S-079, S-080, S-081, S-095
- 下一步：在採用前為目標專案填寫風險表，決定最低成熟度層級；本報告的第一推薦採 L3，並以 policy gate 補足部分 L4 能力。
- 關閉條件：已定義 L1-L4 能力與選擇規則；每個候選工具能映射至層級；選型不再依賴含糊的單一排行。

##### `RC-002` 效率、brownfield、security、drift 與 runtime 工具無法直接比較

- 狀態：`resolved`
- 判斷：將工具視為不同架構層的 specialization，而非彼此互斥的競品。需求基線、repository context、runtime、verifier 與 policy gate 應各自選型；只使用單一工具時必須揭露缺口，多工具方案則明確定義角色分工。
- 解決方式：建立 specialization 軸與責任邊界，並以 v7 開源工具推薦矩陣列出單工具缺口及多工具整合方式。
- 依據來源：S-004, S-018, S-021, S-027, S-028, S-029, S-055, S-089, S-091
- 下一步：以第一推薦組合 OpenSpec + OpenLore + cc-sdd + OPA/Rego + Conftest 建立 PoC；若需要常駐 issue runner，再切換 Symphony 組合。
- 關閉條件：每一個工具具有唯一主要責任；整合流程列出 artifact 交換方式；沒有工具被描述成能單獨覆蓋完整 assurance architecture。

##### `RC-003` 新興研究原型與成熟 assurance 控制的證據強度

- 狀態：`resolved`
- 判斷：R2Code 與 ReqToCode 保留為 future direction，不進入目前 production baseline。現階段 production assurance 由 NASA 雙向 traceability、requirements management、NIST SSDF、OWASP controls 與 CI policy gates 承擔。
- 解決方式：依證據層級分流：官方規範與可執行 policy 作為 baseline；預印本僅進入實驗 backlog，必須獨立重現後才能升級。
- 依據來源：S-079, S-080, S-081, S-082, S-083, S-085, S-086, S-087, S-088, S-089, S-090, S-091, S-094, S-095
- 下一步：維持現有 matrix 與 CI gate；另開 R2Code、ReqToCode reproduction experiment，不阻擋第一版實作。
- 關閉條件：production baseline 與 experimental backlog 已分離；預印本能力不再被當成現有穩健性保證。

#### 未知事項解決矩陣

##### `RU-001` 不同工具組合的實際穩健性比較

- 狀態：`open`
- 判斷：文件搜尋只能建立候選架構，不能證明哪一組在組織環境中表現最佳。此未知必須用相同 repository、requirements、模型與權限設定進行 benchmark。
- 解決方式：建立組織專用 benchmark harness，比較 v7 的前三種多工具組合；量測 requirement coverage、traceability completeness、orphan artifacts、drift、first-pass verification、human interventions、security exceptions、完成時間與維護成本。
- 依據來源：S-072, S-074, S-075, S-078, S-092, S-093
- 下一步：先選一個 greenfield 與一個 brownfield repository，建立固定 requirements baseline、task fixtures、metric schema 與 runner。
- 關閉條件：前三種組合均在相同 fixtures 上至少重複執行三次；輸出可重現結果與選型決策；記錄模型、工具版本、權限與人工介入。

##### `RU-002` 安全政策哪些可自動化、哪些需要人工核准

- 狀態：`partially_resolved`
- 判斷：已有足夠官方資料建立第一版 baseline：NIST SSDF 作為 secure SDLC 骨架，OWASP ASVS、AISVS、SCVS 作為可測試控制來源，CISA Secure by Design 補充產品安全原則，OPA/Rego 與 Conftest 執行可自動化規則。尚未解決的是組織風險偏好、例外核准人與 deploy gate 門檻。
- 解決方式：建立版本化 security-controls.yaml；每一項控制標示 requirement ref、source version、owner、automation level、Rego policy、evidence、exception approver 與 expiry。
- 依據來源：S-083, S-084, S-085, S-086, S-087, S-088, S-089, S-090, S-091, S-096, S-097
- 下一步：產出第一版 security control catalog 與 Rego policy pack；邀請組織安全 owner 核准 automation level、例外流程與部署阻擋規則。
- 關閉條件：所有 in-scope 控制都有版本、owner 與 automation 分類；自動規則具有測試；人工控制具有 approver 與 SLA；例外具有 expiry；deploy gate 經安全 owner 核准。

##### `RU-003` Brownfield context graph 與 drift detection 的準確率及維護成本

- 狀態：`open`
- 判斷：OpenLore、Kata 與相關來源足以證明技術路徑存在，但不能證明對目標 repository 的準確率、誤報率與更新成本。需要在真實 brownfield 專案執行 PoC。
- 解決方式：選定代表性 repository，建立人工標註樣本；比較 symbol/call graph、impact analysis、spec extraction、drift detection 與 context retrieval；記錄 precision、recall、staleness、index update time 與 human correction time。
- 依據來源：S-018, S-029, S-069, S-071, S-074, S-077, S-078
- 下一步：先以 OpenLore 做兩週 PoC，建立靜態分析 baseline；對動態 dispatch、metaprogramming 與 eval 類 pattern 另外列人工覆核範圍。
- 關閉條件：在至少一個真實 brownfield repository 完成人工標註驗證；報告 precision、recall、誤報率、索引更新時間、人工修正時間與已知無法捕捉的語言模式。

##### `RU-004` R2Code 與 ReqToCode 是否適用大型實務 repository

- 狀態：`open`
- 判斷：兩項預印本可作為未來方向，但尚不足以納入 production baseline。其價值必須透過獨立重現與大型 repository 測試確認。
- 解決方式：建立 reproduction experiment：使用已核准 requirement-code links 作為驗證集，量測 R2Code 類型 link recovery 的 precision、recall、F1 與成本；對 ReqToCode 類型 metadata 驗證標註成本、編譯期 coverage 與語言限制。
- 依據來源：S-094, S-095
- 下一步：排入實驗 backlog，優先級低於 registry、traceability matrix、brownfield PoC 與 security baseline。
- 關閉條件：完成至少一個大型 repository 的獨立重現；揭露資料集、語言、標註成本、precision、recall、F1、效能與失敗模式；再決定是否升級為可選能力。


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

### `S-001` [GitHub Spec Kit Documentation](https://github.github.com/spec-kit/index.html)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060534Z
- Snapshot hash：`sha256:ca8a5391751b7de3d59c2581cb046b0494bd011a537541e63574363ed6933c4e`
- 擷取日期：`2026-05-31T06:05:34+00:00`
- 重新檢查日期：`2026-06-30T06:05:34+00:00`
- 支持主張：C-001, C-003, C-011

### `S-002` [Spec Kit Workflows Documentation](https://github.github.com/spec-kit/reference/workflows.html)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060535Z
- Snapshot hash：`sha256:82935728f113f5ee0621e328ac2aa85de8e25ce24cc798a8dc01b6fb0765003f`
- 擷取日期：`2026-05-31T06:05:35+00:00`
- 重新檢查日期：`2026-06-30T06:05:35+00:00`
- 支持主張：C-008

### `S-003` [Kiro Specs Documentation](https://kiro.dev/docs/specs/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060535Z
- Snapshot hash：`sha256:51cba98eff562e0c897adff6c2f3ca048d3404cb6509cdc5f304e466a2b1b9d0`
- 擷取日期：`2026-05-31T06:05:35+00:00`
- 重新檢查日期：`2026-06-30T06:05:35+00:00`
- 支持主張：C-001

### `S-004` [OpenSpec Repository README](https://github.com/Fission-AI/OpenSpec)

- 證據層級：`B`
- 固定版本：https://github.com/Fission-AI/OpenSpec/tree/0c5f0c6c48dce8cdcb85c1c50089c2d1c7921209
- Commit SHA：`0c5f0c6c48dce8cdcb85c1c50089c2d1c7921209`
- 頁面定位：repository tree
- Snapshot hash：`sha256:62452c1aa7d7ee68667290759eba9f907710a1bfbc3947f67f82305a036c22a1`
- 擷取日期：`2026-05-31T06:05:37+00:00`
- 重新檢查日期：`2026-06-30T06:05:37+00:00`
- 支持主張：C-001, C-003, C-011

### `S-005` [Spec Kitty Repository README](https://github.com/Priivacy-ai/spec-kitty)

- 證據層級：`B`
- 固定版本：https://github.com/Priivacy-ai/spec-kitty/tree/8a295a510e92a68a9d5da0ed7bf60cfaa040e351
- Commit SHA：`8a295a510e92a68a9d5da0ed7bf60cfaa040e351`
- 頁面定位：repository tree
- Snapshot hash：`sha256:21c0586928863d858b0d57ef12ed7c3c98716a1e8d2a6830ba0703318468956b`
- 擷取日期：`2026-05-31T06:05:38+00:00`
- 重新檢查日期：`2026-06-30T06:05:38+00:00`
- 支持主張：無

### `S-006` [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180v1)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060539Z
- Snapshot hash：`sha256:9808b854c7b1bd02af7e3b5a54d81fe9be9f5f4973300810dd4449788be866b9`
- 擷取日期：`2026-05-31T06:05:39+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：無

### `S-007` [GitHub Spec Kit Repository README](https://github.com/github/spec-kit)

- 證據層級：`B`
- 固定版本：https://github.com/github/spec-kit/tree/3617cd9c0219092d778f81118110daf127918baf
- Commit SHA：`3617cd9c0219092d778f81118110daf127918baf`
- 頁面定位：repository tree
- Snapshot hash：`sha256:6862c731b4abb38f5f85f302e9267d2457aef2f306d7c4629ed8ead2c3b38c4b`
- 擷取日期：`2026-05-31T06:06:34+00:00`
- 重新檢查日期：`2026-06-30T06:06:34+00:00`
- 支持主張：無

### `S-008` [SpecDD Official Documentation](https://specdd.ai/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060635Z
- Snapshot hash：`sha256:e6d59fa3b16044a001b1c72fb6907d886263821f75b9e404cc0f2afb338b0638`
- 擷取日期：`2026-05-31T06:06:35+00:00`
- 重新檢查日期：`2026-06-30T06:06:35+00:00`
- 支持主張：C-001, C-003

### `S-009` [OpenSpecification Repository README](https://github.com/spenceriam/OpenSpecification)

- 證據層級：`B`
- 固定版本：https://github.com/spenceriam/OpenSpecification/tree/fd0dc03b92492476187849be8116939ab265b54d
- Commit SHA：`fd0dc03b92492476187849be8116939ab265b54d`
- 頁面定位：repository tree
- Snapshot hash：`sha256:7e5ac1404cd7a6905c77d283a9dc5fc3d1def28289633253c8a1f2ad14a4241a`
- 擷取日期：`2026-05-31T06:06:36+00:00`
- 重新檢查日期：`2026-06-30T06:06:36+00:00`
- 支持主張：無

### `S-010` [Akka Spec-Driven Development Documentation](https://doc.akka.io/sdk/spec-driven-development.html)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T060637Z
- Snapshot hash：`sha256:e3cd09466a599bedc2976d44b5e63962bfe5d29cc03792f82a78bf3345fb24e1`
- 擷取日期：`2026-05-31T06:06:37+00:00`
- 重新檢查日期：`2026-06-30T06:06:37+00:00`
- 支持主張：C-001, C-003, C-008, C-012

### `S-011` [codex-spec Repository README](https://github.com/shenli/codex-spec)

- 證據層級：`B`
- 固定版本：https://github.com/shenli/codex-spec/tree/7b585f0dbf75fb3523244586a1f77a183520fb43
- Commit SHA：`7b585f0dbf75fb3523244586a1f77a183520fb43`
- 頁面定位：repository tree
- Snapshot hash：`sha256:06007ba8ac402033dbaa22c123ac43aaf136e039d5b9165d37cc08e567a689d1`
- 擷取日期：`2026-05-31T11:38:56+00:00`
- 重新檢查日期：`2026-06-30T11:38:56+00:00`
- 支持主張：無

### `S-012` [SpecPulse Repository README](https://github.com/specpulse/specpulse)

- 證據層級：`B`
- 固定版本：https://github.com/specpulse/specpulse/tree/01801da4ae31da7eca569b1d1ab0e4ea2cc0dc7d
- Commit SHA：`01801da4ae31da7eca569b1d1ab0e4ea2cc0dc7d`
- 頁面定位：repository tree
- Snapshot hash：`sha256:efc546ef023d2cb5b6174f923ee2cc0a8cdf962b22da09f36f509870f33df8a4`
- 擷取日期：`2026-05-31T11:38:58+00:00`
- 重新檢查日期：`2026-06-30T11:38:58+00:00`
- 支持主張：無

### `S-013` [Specs CLI Repository README](https://github.com/specs-cli/specs-cli)

- 證據層級：`B`
- 固定版本：https://github.com/specs-cli/specs-cli/tree/c36ee1afdd72061ded2f0ab88b4a3ab8e7353fe4
- Commit SHA：`c36ee1afdd72061ded2f0ab88b4a3ab8e7353fe4`
- 頁面定位：repository tree
- Snapshot hash：`sha256:efc26a610ee64f4ec615d8ebb1ee54aa74673198a2b682336f57ad3f6b92ffc6`
- 擷取日期：`2026-05-31T11:38:59+00:00`
- 重新檢查日期：`2026-06-30T11:38:59+00:00`
- 支持主張：C-001, C-002, C-003

### `S-014` [Spec Workflow MCP Repository README](https://github.com/mamajiaa/specs-workflow-mcp)

- 證據層級：`B`
- 固定版本：https://github.com/mamajiaa/specs-workflow-mcp/tree/5d08dac63d80a8e585e26b2513b5ede440787fac
- Commit SHA：`5d08dac63d80a8e585e26b2513b5ede440787fac`
- 頁面定位：repository tree
- Snapshot hash：`sha256:7a5efb8e9148c7391023c31f9f1c25e2763822e2b55000e2f0fbedb84e84b333`
- 擷取日期：`2026-05-31T11:39:00+00:00`
- 重新檢查日期：`2026-06-30T11:39:00+00:00`
- 支持主張：無

### `S-015` [Specflow Repository README](https://github.com/specstoryai/specflow)

- 證據層級：`B`
- 固定版本：https://github.com/specstoryai/specflow/tree/8e4a6c4bdaa84f1381e647116cd8ae47b7c7d444
- Commit SHA：`8e4a6c4bdaa84f1381e647116cd8ae47b7c7d444`
- 頁面定位：repository tree
- Snapshot hash：`sha256:389c61b13ac44affddfcb69c8792585b7b6b52aaeacd70e63f59774f439cb4d1`
- 擷取日期：`2026-05-31T11:39:01+00:00`
- 重新檢查日期：`2026-06-30T11:39:01+00:00`
- 支持主張：無

### `S-016` [BMAD Method Repository README](https://github.com/bmad-code-org/BMAD-METHOD)

- 證據層級：`B`
- 固定版本：https://github.com/bmad-code-org/BMAD-METHOD/tree/fae70152266659061bf57e8b08b2a50a7981fc9c
- Commit SHA：`fae70152266659061bf57e8b08b2a50a7981fc9c`
- 頁面定位：repository tree
- Snapshot hash：`sha256:923306df66eaa0978babf5b2471177284c9b81dd6a0f41a0b367c7f4651671b1`
- 擷取日期：`2026-05-31T11:39:03+00:00`
- 重新檢查日期：`2026-06-30T11:39:03+00:00`
- 支持主張：無

### `S-017` [Get Shit Done Repository README](https://github.com/gsd-build/get-shit-done)

- 證據層級：`B`
- 固定版本：https://github.com/gsd-build/get-shit-done/tree/837114c1d0a4bec91983bb198a2b0d9f42a9446f
- Commit SHA：`837114c1d0a4bec91983bb198a2b0d9f42a9446f`
- 頁面定位：repository tree
- Snapshot hash：`sha256:5b1cb5424647b89cce06e727f19fae59762cdcb6accc5bb1c44f5708dabbe2dc`
- 擷取日期：`2026-05-31T11:39:04+00:00`
- 重新檢查日期：`2026-06-30T11:39:04+00:00`
- 支持主張：C-005

### `S-018` [Kata Repository README](https://github.com/gannonh/kata)

- 證據層級：`B`
- 固定版本：https://github.com/gannonh/kata/tree/4a592c90c7518375e7f64c9e8b74558ec775168f
- Commit SHA：`4a592c90c7518375e7f64c9e8b74558ec775168f`
- 頁面定位：repository tree
- Snapshot hash：`sha256:482d4c88371bd4c469bbc8ef875d3eaa4d61725e821ffe7217ca0ccb8d2fed84`
- 擷取日期：`2026-05-31T11:39:06+00:00`
- 重新檢查日期：`2026-06-30T11:39:06+00:00`
- 支持主張：C-004, C-005

### `S-019` [Taskmaster Repository README](https://github.com/eyaltoledano/claude-task-master)

- 證據層級：`B`
- 固定版本：https://github.com/eyaltoledano/claude-task-master/tree/c0c98d367c55296bfe69e65680625b6db437af02
- Commit SHA：`c0c98d367c55296bfe69e65680625b6db437af02`
- 頁面定位：repository tree
- Snapshot hash：`sha256:c5735012fd81bb680bce26a3448f79db736cbfc03d221836889938af98ab11e5`
- 擷取日期：`2026-05-31T11:39:07+00:00`
- 重新檢查日期：`2026-06-30T11:39:07+00:00`
- 支持主張：C-004

### `S-020` [OpenAI Symphony Repository README](https://github.com/openai/symphony)

- 證據層級：`B`
- 固定版本：https://github.com/openai/symphony/tree/c5261d12101b02e0045ca84701eed0c4be367387
- Commit SHA：`c5261d12101b02e0045ca84701eed0c4be367387`
- 頁面定位：repository tree
- Snapshot hash：`sha256:1c823c7e34d67caa68a943c2281261e03963c10f219afaecadfdbf69c8c65884`
- 擷取日期：`2026-05-31T11:39:08+00:00`
- 重新檢查日期：`2026-06-30T11:39:08+00:00`
- 支持主張：無

### `S-021` [OpenAI Symphony Service Specification](https://github.com/openai/symphony/blob/main/SPEC.md)

- 證據層級：`A`
- 固定版本：https://github.com/openai/symphony/blob/c5261d12101b02e0045ca84701eed0c4be367387/SPEC.md
- Commit SHA：`c5261d12101b02e0045ca84701eed0c4be367387`
- 頁面定位：SPEC.md
- Snapshot hash：`sha256:000d714aa69d4c6a98edcc08349c75066d0ee1289644b6d942fb4ede2dab1e2d`
- 擷取日期：`2026-05-31T11:39:10+00:00`
- 重新檢查日期：`2026-06-30T11:39:10+00:00`
- 支持主張：C-004, C-008, C-011, C-012

### `S-022` [Rover Repository README](https://github.com/endorhq/rover)

- 證據層級：`B`
- 固定版本：https://github.com/endorhq/rover/tree/165b689f84a1f74f60c4d8c0706bdfd00f132899
- Commit SHA：`165b689f84a1f74f60c4d8c0706bdfd00f132899`
- 頁面定位：repository tree
- Snapshot hash：`sha256:a31128399e82bd6290af302ff914a546bb89ff8ae6c254d590b93c1a59fc43cd`
- 擷取日期：`2026-05-31T11:39:12+00:00`
- 重新檢查日期：`2026-06-30T11:39:12+00:00`
- 支持主張：C-004, C-011

### `S-023` [Agent Skills Spec-Driven Development Skill](https://github.com/addyosmani/agent-skills/blob/main/skills/spec-driven-development/SKILL.md)

- 證據層級：`B`
- 固定版本：https://github.com/addyosmani/agent-skills/blob/6ce029897d2b794940325fc7148774a6ec51111c/skills/spec-driven-development/SKILL.md
- Commit SHA：`6ce029897d2b794940325fc7148774a6ec51111c`
- 頁面定位：skills/spec-driven-development/SKILL.md
- Snapshot hash：`sha256:68f5a614182efcb83e3271ce3911af819998d72553326812b5fd3127725247bd`
- 擷取日期：`2026-05-31T11:39:13+00:00`
- 重新檢查日期：`2026-06-30T11:39:13+00:00`
- 支持主張：C-008

### `S-024` [Spec Kit Agents: Context-Grounded Agentic Workflows](https://arxiv.org/abs/2604.05278v1)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T113913Z
- Snapshot hash：`sha256:527ec5203cecfeed5d0af795e0e83876692f25daa002af8a3e11c92b4854f447`
- 擷取日期：`2026-05-31T11:39:13+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：無

### `S-025` [Constitutional Spec-Driven Development](https://arxiv.org/abs/2602.02584v1)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T113914Z
- Snapshot hash：`sha256:ee7bd875a6755d496dc4c60ef892d8fe2a4497ab20f18da3113cb63a6991d4c4`
- 擷取日期：`2026-05-31T11:39:14+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：無

### `S-026` [Kiro Repository README](https://github.com/kirodotdev/Kiro)

- 證據層級：`B`
- 固定版本：https://github.com/kirodotdev/Kiro/tree/2f1d7a72e28203332ad11894886b1903e7dbbebe
- Commit SHA：`2f1d7a72e28203332ad11894886b1903e7dbbebe`
- 頁面定位：repository tree
- Snapshot hash：`sha256:365a8dbd687ec92c8dd8d26fa926d0d5cc56ce74c14f0707b2a1b26f8707be3f`
- 擷取日期：`2026-05-31T12:12:02+00:00`
- 重新檢查日期：`2026-06-30T12:12:02+00:00`
- 支持主張：無

### `S-027` [cc-sdd Repository README](https://github.com/gotalab/cc-sdd)

- 證據層級：`B`
- 固定版本：https://github.com/gotalab/cc-sdd/tree/29aee950f4addc36f9aeecb9881c46540e71ecc9
- Commit SHA：`29aee950f4addc36f9aeecb9881c46540e71ecc9`
- 頁面定位：repository tree
- Snapshot hash：`sha256:2392ac0fa675ceb78d772f437fe6dd86213186a3370557284fed4daff70cb800`
- 擷取日期：`2026-05-31T12:12:03+00:00`
- 重新檢查日期：`2026-06-30T12:12:03+00:00`
- 支持主張：C-008

### `S-028` [MoAI-ADK Repository README](https://github.com/modu-ai/moai-adk)

- 證據層級：`B`
- 固定版本：https://github.com/modu-ai/moai-adk/tree/4e8074e019aa047f0c6e154829d619be20cf8620
- Commit SHA：`4e8074e019aa047f0c6e154829d619be20cf8620`
- 頁面定位：repository tree
- Snapshot hash：`sha256:7514b556a692904949accfc8b234005b9642f964cefb7d918106b8c9fc9803fc`
- 擷取日期：`2026-05-31T12:12:05+00:00`
- 重新檢查日期：`2026-06-30T12:12:05+00:00`
- 支持主張：無

### `S-029` [OpenLore Repository README](https://github.com/clay-good/OpenLore)

- 證據層級：`B`
- 固定版本：https://github.com/clay-good/OpenLore/tree/57b639cf5cf010bc702369987ab35b78916cb8bc
- Commit SHA：`57b639cf5cf010bc702369987ab35b78916cb8bc`
- 頁面定位：repository tree
- Snapshot hash：`sha256:b67521987397a17d3fceee7761c87eda2ed802d64270f337d9257b301e9f8801`
- 擷取日期：`2026-05-31T12:12:06+00:00`
- 重新檢查日期：`2026-06-30T12:12:06+00:00`
- 支持主張：C-003, C-004, C-005, C-011, C-012

### `S-030` [Specboot ai-specs Repository README](https://github.com/LIDR-academy/lidr-specboot)

- 證據層級：`B`
- 固定版本：https://github.com/LIDR-academy/lidr-specboot/tree/d19d286e9895bdf9be54b3e97070b9fe081c93af
- Commit SHA：`d19d286e9895bdf9be54b3e97070b9fe081c93af`
- 頁面定位：repository tree
- Snapshot hash：`sha256:75b83b242817d178bece891168cc2c1d134f9d4543c6c7f3a7e346b292c5ec47`
- 擷取日期：`2026-05-31T12:12:08+00:00`
- 重新檢查日期：`2026-06-30T12:12:08+00:00`
- 支持主張：無

### `S-031` [Gentle-AI Repository README](https://github.com/Gentleman-Programming/gentle-ai)

- 證據層級：`B`
- 固定版本：https://github.com/Gentleman-Programming/gentle-ai/tree/21634526c5a1096fd7c278841e62766f2b090b1d
- Commit SHA：`21634526c5a1096fd7c278841e62766f2b090b1d`
- 頁面定位：repository tree
- Snapshot hash：`sha256:a8372025c98fd6d4720e5c936d4ad24690f08ab88ac4a233b66a6f544247265b`
- 擷取日期：`2026-05-31T12:12:09+00:00`
- 重新檢查日期：`2026-06-30T12:12:09+00:00`
- 支持主張：無

### `S-032` [spec-coding-mcp Repository README](https://github.com/kevinlin/spec-coding-mcp)

- 證據層級：`B`
- 固定版本：https://github.com/kevinlin/spec-coding-mcp/tree/403fb8eebd2de186d7e348fd37cc263b628ad20a
- Commit SHA：`403fb8eebd2de186d7e348fd37cc263b628ad20a`
- 頁面定位：repository tree
- Snapshot hash：`sha256:4eda42552290cc30ed85635da01ed563649c2e0621ba088606d527c33db9287d`
- 擷取日期：`2026-05-31T12:12:10+00:00`
- 重新檢查日期：`2026-06-30T12:12:10+00:00`
- 支持主張：C-001

### `S-033` [Pimzino Spec Workflow MCP README](https://github.com/Pimzino/spec-workflow-mcp)

- 證據層級：`B`
- 固定版本：https://github.com/Pimzino/spec-workflow-mcp/tree/b63e6cd8d6ed53bbc48fe93d634f7b548285762f
- Commit SHA：`b63e6cd8d6ed53bbc48fe93d634f7b548285762f`
- 頁面定位：repository tree
- Snapshot hash：`sha256:b72d92ca8b8c6dc8d2e6e85a29fd06cca1019b0e89d49b28878dc702c1bd4ed2`
- 擷取日期：`2026-05-31T12:12:12+00:00`
- 重新檢查日期：`2026-06-30T12:12:12+00:00`
- 支持主張：C-008

### `S-034` [Smart Ralph Repository README](https://github.com/tzachbon/smart-ralph)

- 證據層級：`B`
- 固定版本：https://github.com/tzachbon/smart-ralph/tree/1b332022227af46006793e7774dcf55eab1706f0
- Commit SHA：`1b332022227af46006793e7774dcf55eab1706f0`
- 頁面定位：repository tree
- Snapshot hash：`sha256:0c6bcb05c32e84df3a503ea4120d9bfe73ad1106ada933462da44d49e0f4dc34`
- 擷取日期：`2026-05-31T12:12:13+00:00`
- 重新檢查日期：`2026-06-30T12:12:13+00:00`
- 支持主張：C-004

### `S-035` [Flow Next Repository README](https://github.com/gmickel/flow-next)

- 證據層級：`B`
- 固定版本：https://github.com/gmickel/flow-next/tree/fccd2ba8a17a65f6ba31247ce170b63b0998f7be
- Commit SHA：`fccd2ba8a17a65f6ba31247ce170b63b0998f7be`
- 頁面定位：repository tree
- Snapshot hash：`sha256:5de22301f84f658a86d1c09c8eca8ea599570d27dadfa59d0a9b530c951bcd5d`
- 擷取日期：`2026-05-31T12:12:14+00:00`
- 重新檢查日期：`2026-06-30T12:12:14+00:00`
- 支持主張：C-004

### `S-036` [GAAI Framework Repository README](https://github.com/Fr-e-d/GAAI-framework)

- 證據層級：`B`
- 固定版本：https://github.com/Fr-e-d/GAAI-framework/tree/c12e1de36847e65a98d768b83bf6fa7951637d89
- Commit SHA：`c12e1de36847e65a98d768b83bf6fa7951637d89`
- 頁面定位：repository tree
- Snapshot hash：`sha256:c9810ebe9532c33c4955679aabb5b31e568801ff82f6467200bf3128cd53b886`
- 擷取日期：`2026-05-31T12:12:15+00:00`
- 重新檢查日期：`2026-06-30T12:12:15+00:00`
- 支持主張：無

### `S-037` [iannuttall Ralph Repository README](https://github.com/iannuttall/ralph)

- 證據層級：`B`
- 固定版本：https://github.com/iannuttall/ralph/tree/5bc402540c45192bd1e9cacb84611ee2e5ba13a8
- Commit SHA：`5bc402540c45192bd1e9cacb84611ee2e5ba13a8`
- 頁面定位：repository tree
- Snapshot hash：`sha256:758b21f0ab6329a276a535a57d8536ef106465850e6c5970ead502d102ba4433`
- 擷取日期：`2026-05-31T12:12:16+00:00`
- 重新檢查日期：`2026-06-30T12:12:16+00:00`
- 支持主張：C-004

### `S-038` [Anthropic Ralph Wiggum Plugin README](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md)

- 證據層級：`A`
- 固定版本：https://github.com/anthropics/claude-code/blob/295dee881d0e1c1d0cd22fe171e4c1d07118fb04/plugins/ralph-wiggum/README.md
- Commit SHA：`295dee881d0e1c1d0cd22fe171e4c1d07118fb04`
- 頁面定位：plugins/ralph-wiggum/README.md
- Snapshot hash：`sha256:87542e4c83c60f7330b241d6b50e87d3cbe05968088f3fe58517aba9ff7df0e4`
- 擷取日期：`2026-05-31T12:12:17+00:00`
- 重新檢查日期：`2026-06-30T12:12:17+00:00`
- 支持主張：C-004

### `S-039` [snarktank Ralph Repository README](https://github.com/snarktank/ralph)

- 證據層級：`B`
- 固定版本：https://github.com/snarktank/ralph/tree/6c53cb0b831ebe8739c6a003e22af14902d8b0b5
- Commit SHA：`6c53cb0b831ebe8739c6a003e22af14902d8b0b5`
- 頁面定位：repository tree
- Snapshot hash：`sha256:6337ca9d1a85ebc96e496c5213337a3fa24c5ca80e09509abc0c58bc5fcd1598`
- 擷取日期：`2026-05-31T12:12:18+00:00`
- 重新檢查日期：`2026-06-30T12:12:18+00:00`
- 支持主張：C-004

### `S-040` [Swarms Repository README](https://github.com/am-will/swarms)

- 證據層級：`B`
- 固定版本：https://github.com/am-will/swarms/tree/110268148a1fdf149a19e4dab848a1c0fca9835d
- Commit SHA：`110268148a1fdf149a19e4dab848a1c0fca9835d`
- 頁面定位：repository tree
- Snapshot hash：`sha256:5d7f98f4dcaf675dc8cf0935a63ba0e878f321f5b3bdd87c1dace5cc6e8e25ec`
- 擷取日期：`2026-05-31T12:12:20+00:00`
- 重新檢查日期：`2026-06-30T12:12:20+00:00`
- 支持主張：無

### `S-041` [Metaswarm Repository README](https://github.com/dsifry/metaswarm)

- 證據層級：`B`
- 固定版本：https://github.com/dsifry/metaswarm/tree/398be78231bc1c57b147869c5c80696003e95f31
- Commit SHA：`398be78231bc1c57b147869c5c80696003e95f31`
- 頁面定位：repository tree
- Snapshot hash：`sha256:ba36c8c3f954efdbdf47f185c3fdf135846f46c2fab45e7d6284100cbe621a2f`
- 擷取日期：`2026-05-31T12:12:21+00:00`
- 重新檢查日期：`2026-06-30T12:12:21+00:00`
- 支持主張：無

### `S-042` [Maestro Orchestrate Repository README](https://github.com/josstei/maestro-orchestrate)

- 證據層級：`B`
- 固定版本：https://github.com/josstei/maestro-orchestrate/tree/4f5d434dded8a5e58808ad60f56c6e410f57cf7e
- Commit SHA：`4f5d434dded8a5e58808ad60f56c6e410f57cf7e`
- 頁面定位：repository tree
- Snapshot hash：`sha256:5f7a62fbc09ea10bbc782b60bed2c59521a3db229a4e6f8dec4fa5c788b0e0b3`
- 擷取日期：`2026-05-31T12:12:22+00:00`
- 重新檢查日期：`2026-06-30T12:12:22+00:00`
- 支持主張：無

### `S-043` [Worktrunk Repository README](https://github.com/max-sixty/worktrunk)

- 證據層級：`B`
- 固定版本：https://github.com/max-sixty/worktrunk/tree/33bab089bff623ac66b78719c5d761388e09b91e
- Commit SHA：`33bab089bff623ac66b78719c5d761388e09b91e`
- 頁面定位：repository tree
- Snapshot hash：`sha256:da3d2c7b524bf0308735798f0213ffa4d0ffed1b7c30c94121f2642e5f82d7fd`
- 擷取日期：`2026-05-31T12:12:23+00:00`
- 重新檢查日期：`2026-06-30T12:12:23+00:00`
- 支持主張：無

### `S-044` [workmux Repository README](https://github.com/raine/workmux)

- 證據層級：`B`
- 固定版本：https://github.com/raine/workmux/tree/d3f7930bfa9026aecdca12509bee2c93553badf6
- Commit SHA：`d3f7930bfa9026aecdca12509bee2c93553badf6`
- 頁面定位：repository tree
- Snapshot hash：`sha256:e8f41c9428930ac8511ff58ccc20b9d3a3a2ce2c567f61d1bc749ee8ed73efbb`
- 擷取日期：`2026-05-31T12:12:25+00:00`
- 重新檢查日期：`2026-06-30T12:12:25+00:00`
- 支持主張：無

### `S-045` [Codexia Repository README](https://github.com/milisp/codexia)

- 證據層級：`B`
- 固定版本：https://github.com/milisp/codexia/tree/f2eb514021e9a4c91c5dc3877952ade4175fd536
- Commit SHA：`f2eb514021e9a4c91c5dc3877952ade4175fd536`
- 頁面定位：repository tree
- Snapshot hash：`sha256:cb59b39bde0eea0055c7d0d1af196622f1041428c8d4e1091dbc77e2c40f7a6b`
- 擷取日期：`2026-05-31T12:12:26+00:00`
- 重新檢查日期：`2026-06-30T12:12:26+00:00`
- 支持主張：無

### `S-046` [Claw Orchestrator Repository README](https://github.com/Enderfga/claw-orchestrator)

- 證據層級：`B`
- 固定版本：https://github.com/Enderfga/claw-orchestrator/tree/2002effdf1490f7ccf53682b3363e690a373f766
- Commit SHA：`2002effdf1490f7ccf53682b3363e690a373f766`
- 頁面定位：repository tree
- Snapshot hash：`sha256:ae7c7e7248098c992243ddbc6efb53a2638d6ded797f00bda719b2d1fdc4a846`
- 擷取日期：`2026-05-31T12:12:27+00:00`
- 重新檢查日期：`2026-06-30T12:12:27+00:00`
- 支持主張：無

### `S-047` [Local-first Maestro Repository README](https://github.com/ReinaMacCredy/maestro)

- 證據層級：`B`
- 固定版本：https://github.com/ReinaMacCredy/maestro/tree/87f8e446b5997763e0ec0ac088494be15175bce4
- Commit SHA：`87f8e446b5997763e0ec0ac088494be15175bce4`
- 頁面定位：repository tree
- Snapshot hash：`sha256:06dd9928103cad0dfd87f62df133c49dd3e17c25b95438e79c9998af43a3d819`
- 擷取日期：`2026-05-31T12:12:29+00:00`
- 重新檢查日期：`2026-06-30T12:12:29+00:00`
- 支持主張：無

### `S-048` [Awesome OpenSpec Repository README](https://github.com/wearetechnative/awesome-openspec)

- 證據層級：`B`
- 固定版本：https://github.com/wearetechnative/awesome-openspec/tree/1f29432fbf9aa2b7559241a1a1ace34f031d32f4
- Commit SHA：`1f29432fbf9aa2b7559241a1a1ace34f031d32f4`
- 頁面定位：repository tree
- Snapshot hash：`sha256:c2440e55b18d38427756bdfc05237b60552d2dcddaf0ef9f1cabd1b207beacd4`
- 擷取日期：`2026-05-31T12:12:30+00:00`
- 重新檢查日期：`2026-06-30T12:12:30+00:00`
- 支持主張：無

### `S-049` [OpenSpec Supported Tools Documentation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)

- 證據層級：`A`
- 固定版本：https://github.com/Fission-AI/OpenSpec/blob/9aded17af760ad2015ed3e91ce3b93bec9f3adfc/docs/supported-tools.md
- Commit SHA：`9aded17af760ad2015ed3e91ce3b93bec9f3adfc`
- 頁面定位：docs/supported-tools.md
- Snapshot hash：`sha256:058c5688abd248471a5e13adcdabdc1d2c8b971bd24f1d80929e4e810f60ac3e`
- 擷取日期：`2026-05-31T12:12:31+00:00`
- 重新檢查日期：`2026-06-30T12:12:31+00:00`
- 支持主張：無

### `S-050` [OpenSpec for Copilot Repository README](https://github.com/atman-33/openspec-for-copilot)

- 證據層級：`B`
- 固定版本：https://github.com/atman-33/openspec-for-copilot/tree/e2c933e567199de8b42feea7314a530af8f98a9a
- Commit SHA：`e2c933e567199de8b42feea7314a530af8f98a9a`
- 頁面定位：repository tree
- Snapshot hash：`sha256:049de663ae39d397166e530fb2413f1e54954982ccd2b07e4fcb22a8b6aef8c0`
- 擷取日期：`2026-05-31T12:12:32+00:00`
- 重新檢查日期：`2026-06-30T12:12:32+00:00`
- 支持主張：無

### `S-051` [ClawSpec Repository README](https://github.com/bytegh/clawspec)

- 證據層級：`B`
- 固定版本：https://github.com/bytegh/clawspec/tree/980e32ddab1ba3dfe8abfcd70f400340fc95588d
- Commit SHA：`980e32ddab1ba3dfe8abfcd70f400340fc95588d`
- 頁面定位：repository tree
- Snapshot hash：`sha256:d66119d1b0597daa6870c832d070f45cfb15c0b2fdeb7de6876be4ef38fb573e`
- 擷取日期：`2026-05-31T12:12:33+00:00`
- 重新檢查日期：`2026-06-30T12:12:33+00:00`
- 支持主張：無

### `S-052` [AI Coding Workflow Repository README](https://github.com/nicksp/ai-coding-worflow)

- 證據層級：`B`
- 固定版本：https://github.com/nicksp/ai-coding-worflow/tree/b1c98d4266118421de53248ab0fded348b84660f
- Commit SHA：`b1c98d4266118421de53248ab0fded348b84660f`
- 頁面定位：repository tree
- Snapshot hash：`sha256:e8e021949c42a298acefd9304b9219b7f60635144e489fc3b3ee6325917af2f6`
- 擷取日期：`2026-05-31T12:12:34+00:00`
- 重新檢查日期：`2026-06-30T12:12:34+00:00`
- 支持主張：無

### `S-053` [Claude SDD Toolkit Repository README](https://github.com/tylerburleigh/claude-sdd-toolkit)

- 證據層級：`B`
- 固定版本：https://github.com/tylerburleigh/claude-sdd-toolkit/tree/1916846fbe3155405fcb193283332a250db18efb
- Commit SHA：`1916846fbe3155405fcb193283332a250db18efb`
- 頁面定位：repository tree
- Snapshot hash：`sha256:1df5ecb4e9987046a1b2c6ac5e45b10b972de5e3462b9e96e692e90e5396f693`
- 擷取日期：`2026-05-31T12:12:36+00:00`
- 重新檢查日期：`2026-06-30T12:12:36+00:00`
- 支持主張：無

### `S-054` [AI Governor Framework Repository README](https://github.com/Fr-e-d/AI-Governor-Framework)

- 證據層級：`B`
- 固定版本：https://github.com/Fr-e-d/AI-Governor-Framework/tree/73631da4f6df50faaac882198ca77db589f19d54
- Commit SHA：`73631da4f6df50faaac882198ca77db589f19d54`
- 頁面定位：repository tree
- Snapshot hash：`sha256:12a504e22c5eee08c1eac2f089f6c1179b81f744683f4fb573f025c56e743d12`
- 擷取日期：`2026-05-31T12:12:37+00:00`
- 重新檢查日期：`2026-06-30T12:12:37+00:00`
- 支持主張：無

### `S-055` [Threatspec Repository README](https://github.com/threatspec/threatspec)

- 證據層級：`B`
- 固定版本：https://github.com/threatspec/threatspec/tree/0c03d6076eabc226cbe9f126e299871cbcda5a0f
- Commit SHA：`0c03d6076eabc226cbe9f126e299871cbcda5a0f`
- 頁面定位：repository tree
- Snapshot hash：`sha256:61089f7620b7c7f9a746f24f24913763aad82289e5c25fc4d0520147bd54d687`
- 擷取日期：`2026-05-31T12:12:38+00:00`
- 重新檢查日期：`2026-06-30T12:12:38+00:00`
- 支持主張：C-004, C-011

### `S-056` [GitHub Blog: Spec-driven development with AI toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133939Z
- Snapshot hash：`sha256:23276602b73755afeabf14a7d34b651afece38b738e84676b4708ab0e5957422`
- 擷取日期：`2026-05-31T13:39:39+00:00`
- 重新檢查日期：`2026-06-30T13:39:39+00:00`
- 支持主張：無

### `S-057` [GitHub Blog: Markdown as a programming language](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133940Z
- Snapshot hash：`sha256:6cc90fc5ef8b8801dbad39e99fef5c1cb51fdf118acabd17cb7c44daa0d1d26d`
- 擷取日期：`2026-05-31T13:39:40+00:00`
- 重新檢查日期：`2026-06-30T13:39:40+00:00`
- 支持主張：無

### `S-058` [Thoughtworks Technology Radar: Spec-driven development](https://www.thoughtworks.com/en-gb/radar/techniques/spec-driven-development)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133941Z
- Snapshot hash：`sha256:f89732f1e4b4092df6fbbca80c6a729557e810dfc6846e3d276ce8b84a30ca9e`
- 擷取日期：`2026-05-31T13:39:41+00:00`
- 重新檢查日期：`2026-06-30T13:39:41+00:00`
- 支持主張：無

### `S-059` [Thoughtworks: Unpacking spec-driven development](https://www.thoughtworks.com/en-gb/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133941Z
- Snapshot hash：`sha256:08099cef9471b211aa987e812d3663713e7d656beeef7beeb182f9cd27a327e1`
- 擷取日期：`2026-05-31T13:39:41+00:00`
- 重新檢查日期：`2026-06-30T13:39:41+00:00`
- 支持主張：無

### `S-060` [Thoughtworks Podcast: What is spec-driven development?](https://www.thoughtworks.com/en-us/insights/podcasts/technology-podcasts/what-is-spec-driven-development)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133942Z
- Snapshot hash：`sha256:75e935d1de6a055ff26302347565ab5fb0ce933dc2482472ef9a437a99f434e2`
- 擷取日期：`2026-05-31T13:39:42+00:00`
- 重新檢查日期：`2026-06-30T13:39:42+00:00`
- 支持主張：無

### `S-061` [Kiro Blog: Introducing Kiro](https://kiro.dev/blog/introducing-kiro/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133943Z
- Snapshot hash：`sha256:4cad4d64c516bea0b01716fcda2fa4fc03d7e49a7f313f92fa13d205032e001e`
- 擷取日期：`2026-05-31T13:39:43+00:00`
- 重新檢查日期：`2026-06-30T13:39:43+00:00`
- 支持主張：無

### `S-062` [AWS Documentation Overview: Kiro](https://aws.amazon.com/documentation-overview/kiro/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133943Z
- Snapshot hash：`sha256:62ce3c9c42195898f6bddd92a38e34fd4191fe47d1827603ce9c32e8f151d438`
- 擷取日期：`2026-05-31T13:39:43+00:00`
- 重新檢查日期：`2026-06-30T13:39:43+00:00`
- 支持主張：無

### `S-063` [AWS Public Sector Blog: Accelerating GovTech development with Kiro](https://aws.amazon.com/blogs/publicsector/accelerating-govtech-development-with-kiro/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133944Z
- Snapshot hash：`sha256:8714c4a42bc3d38b51a5ec048d5dd1d6019946053cc03f67fb3f8dbe6bbb1da7`
- 擷取日期：`2026-05-31T13:39:44+00:00`
- 重新檢查日期：`2026-06-30T13:39:44+00:00`
- 支持主張：C-008, C-012

### `S-064` [Tessl: How products pioneer SDD](https://tessl.io/blog/how-tessls-products-pioneer-spec-driven-development/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133946Z
- Snapshot hash：`sha256:dd140a711c3e99a2a9e3de6928a0d4918146a2489b6e1d624bbffa46496dbe8f`
- 擷取日期：`2026-05-31T13:39:46+00:00`
- 重新檢查日期：`2026-06-30T13:39:46+00:00`
- 支持主張：無

### `S-065` [Tessl: 10 things about specs](https://tessl.io/blog/spec-driven-development-10-things-you-need-to-know-about-specs/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133947Z
- Snapshot hash：`sha256:d8342abd009ad8fa44b470082c3ea00a1b8139fd536d94261dc194b8aea00cf9`
- 擷取日期：`2026-05-31T13:39:47+00:00`
- 重新檢查日期：`2026-06-30T13:39:47+00:00`
- 支持主張：無

### `S-066` [Tessl: OpenAI Symphony orchestration spec](https://tessl.io/blog/openai-open-sources-symphony-a-spec-for-orchestrating-codex-agents/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133948Z
- Snapshot hash：`sha256:79e831f372f59db144c4fca4dc7519f569cd3a140cd02d44c3f9c374c9385914`
- 擷取日期：`2026-05-31T13:39:48+00:00`
- 重新檢查日期：`2026-06-30T13:39:48+00:00`
- 支持主張：C-004

### `S-067` [InfoQ: Enterprise SDD adoption](https://www.infoq.com/articles/enterprise-spec-driven-development/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133950Z
- Snapshot hash：`sha256:bc30b67101db3d32de48af7fa170582ea417f9f6e36ee5df03414b9e58a6c7b8`
- 擷取日期：`2026-05-31T13:39:50+00:00`
- 重新檢查日期：`2026-06-30T13:39:50+00:00`
- 支持主張：C-004, C-008, C-012

### `S-068` [InfoQ: When architecture becomes executable](https://www.infoq.com/articles/spec-driven-development/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133952Z
- Snapshot hash：`sha256:d1cfb55acac20de5d04226c051459080620d65eeb6b21db07e31009890ebfdaa`
- 擷取日期：`2026-05-31T13:39:52+00:00`
- 重新檢查日期：`2026-06-30T13:39:52+00:00`
- 支持主張：C-003, C-011

### `S-069` [Martin Fowler: Context Engineering for Coding Agents](https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133953Z
- Snapshot hash：`sha256:55cb072698e11a7d65079def045780ef764ef5d36729b08355803b252966076b`
- 擷取日期：`2026-05-31T13:39:53+00:00`
- 重新檢查日期：`2026-06-30T13:39:53+00:00`
- 支持主張：C-005

### `S-070` [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T133955Z
- Snapshot hash：`sha256:7db7fb408d3fe3a08d3e41b99c43d601026d276b2c453e7d6efca7cbed341d7d`
- 擷取日期：`2026-05-31T13:39:55+00:00`
- 重新檢查日期：`2026-06-30T13:39:55+00:00`
- 支持主張：C-008

### `S-071` [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134003Z
- Snapshot hash：`sha256:2b7f6bd759d51a7305b9f352e12dbb323dfa5b60788bc5b5e488dc0c479cc7d3`
- 擷取日期：`2026-05-31T13:40:03+00:00`
- 重新檢查日期：`2026-06-30T13:40:03+00:00`
- 支持主張：C-005

### `S-072` [Scale AI: SWE Atlas is Complete](https://scale.com/blog/swe-atlas-complete)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134005Z
- Snapshot hash：`sha256:d00cb9a3ae54865d06ebed3b5e92fd8a4e256626144cb07d8843d45e8db8896a`
- 擷取日期：`2026-05-31T13:40:05+00:00`
- 重新檢查日期：`2026-06-30T13:40:05+00:00`
- 支持主張：C-009

### `S-073` [Xcapit: SDD with AI Agents Practical Guide](https://www.xcapit.com/en/blog/spec-driven-development-ai-agents)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134126Z
- Snapshot hash：`sha256:1dfb894ca80b84d27099f9c1602fea06a7b229f5ef81fe2a4e049f0852cee216`
- 擷取日期：`2026-05-31T13:41:26+00:00`
- 重新檢查日期：`2026-06-30T13:41:26+00:00`
- 支持主張：無

### `S-074` [ContextBench Paper Page](https://huggingface.co/papers/2602.05892)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134127Z
- Snapshot hash：`sha256:ea77bc7545f85ed41f724070dd5d027e4d26158a136ce80eea3c829995102422`
- 擷取日期：`2026-05-31T13:41:27+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：C-005, C-009

### `S-075` [OmniCode Benchmark Paper](https://arxiv.org/abs/2602.02262)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134127Z
- Snapshot hash：`sha256:cb6b9e64054cdb29e82c07f7afb2db1681dfadf374332eeb80eee8da0cb99b79`
- 擷取日期：`2026-05-31T13:41:27+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：C-009

### `S-076` [SDD Practitioner Guide OpenReview PDF](https://openreview.net/pdf?id=bw5mNj75h9)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134129Z
- Snapshot hash：`sha256:f3ee6d7927e2802b12c547e9b5fa2d8dd0f8b16a4d1683d779d1b0d7dd449f6e`
- 擷取日期：`2026-05-31T13:41:29+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：無

### `S-077` [Bito: SDD Explained for AI Coding Teams](https://bito.ai/blog/spec-driven-development-explained-for-ai-coding-teams/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134132Z
- Snapshot hash：`sha256:f5451a092bb3dac8fe4ce01c706fb28acb55e74f4ee528fd179cd6853c298ce5`
- 擷取日期：`2026-05-31T13:41:32+00:00`
- 重新檢查日期：`2026-06-30T13:41:32+00:00`
- 支持主張：C-004, C-005

### `S-078` [Loadsys: Context Engineering AI Practice for SDD Teams](https://www.loadsys.com/blog/context-engineering-ai-spec-driven-development-practice/)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T134133Z
- Snapshot hash：`sha256:242fc7ecbbbcbcf90b05a2ffd7f8ce7d509ab1e1d78f164e5de9c70fe1801219`
- 擷取日期：`2026-05-31T13:41:33+00:00`
- 重新檢查日期：`2026-06-30T13:41:33+00:00`
- 支持主張：C-005, C-009

### `S-079` [NASA SWE-059 Requirements to Design Traceability](https://swehb.nasa.gov/pages/viewpage.action?pageId=16453101)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135855Z
- Snapshot hash：`sha256:e0f15703e7b6350f65316595e05d6bdc888be090621ce9b12d1390b2b79fd562`
- 擷取日期：`2026-05-31T13:58:55+00:00`
- 重新檢查日期：`2026-06-30T13:58:55+00:00`
- 支持主張：C-001, C-002, C-007, C-011, C-012

### `S-080` [NASA SWE-052 Bidirectional Traceability](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052+-+Bidirectional+Traceability)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135859Z
- Snapshot hash：`sha256:a63c777e66e90419df3931bda9a987d7615ffcc8e4d8e56bfaaaefb66c5314d0`
- 擷取日期：`2026-05-31T13:58:59+00:00`
- 重新檢查日期：`2026-06-30T13:58:59+00:00`
- 支持主張：C-001, C-002, C-007, C-011, C-012

### `S-081` [NASA SWE-067 Verify Implementation](https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604539/SWE-067%2B-%2BVerify%2BImplementation)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135901Z
- Snapshot hash：`sha256:f2d888e915b23a2ffaa0ca65c1213c5a52e65955b26f817ea1bc7778784cf132`
- 擷取日期：`2026-05-31T13:59:01+00:00`
- 重新檢查日期：`2026-06-30T13:59:01+00:00`
- 支持主張：C-001, C-002, C-007, C-011, C-012

### `S-082` [NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135904Z
- Snapshot hash：`sha256:1c54a23d56cde50162d92dbbaa74f192807eb0027c11c5519a3f3207710b9a91`
- 擷取日期：`2026-05-31T13:59:04+00:00`
- 重新檢查日期：`2026-06-30T13:59:04+00:00`
- 支持主張：C-001, C-002, C-007

### `S-083` [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135905Z
- Snapshot hash：`sha256:5366532c9afb64b193399186452b4711d116036103d4c288da30ffcffc8d2be7`
- 擷取日期：`2026-05-31T13:59:05+00:00`
- 重新檢查日期：`2026-06-30T13:59:05+00:00`
- 支持主張：C-006, C-012

### `S-084` [NIST NCCoE DevSecOps Practices](https://pages.nist.gov/nccoe-devsecops/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135906Z
- Snapshot hash：`sha256:db8e2c1b895a30773a764a6a492d82b1e15e690927e4d5723589637d8b858187`
- 擷取日期：`2026-05-31T13:59:06+00:00`
- 重新檢查日期：`2026-06-30T13:59:06+00:00`
- 支持主張：C-006

### `S-085` [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135907Z
- Snapshot hash：`sha256:e7d072d99cbd8b67fe4cc81c7d06031db06fa45696158f7fc17fecc5b107582a`
- 擷取日期：`2026-05-31T13:59:07+00:00`
- 重新檢查日期：`2026-06-30T13:59:07+00:00`
- 支持主張：C-006, C-007

### `S-086` [OWASP AISVS](https://owasp.org/www-project-artificial-intelligence-security-verification-standard-aisvs-docs/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135907Z
- Snapshot hash：`sha256:b6a4e263392d2cc0749b355cdb54bd4a85521fe88253e200dc5f9f39b0b9f7b7`
- 擷取日期：`2026-05-31T13:59:07+00:00`
- 重新檢查日期：`2026-06-30T13:59:07+00:00`
- 支持主張：C-006, C-007

### `S-087` [OWASP SCVS Usage and Levels](https://scvs.owasp.org/scvs/using-scvs/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135908Z
- Snapshot hash：`sha256:1b44f2b94a640d7edb76b1ec9b74f1f05c95017b19f78cde831bae0b28e053f8`
- 擷取日期：`2026-05-31T13:59:08+00:00`
- 重新檢查日期：`2026-06-30T13:59:08+00:00`
- 支持主張：C-006, C-007

### `S-088` [OWASP DevGuard](https://owasp.org/www-project-devguard/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135908Z
- Snapshot hash：`sha256:e5869342ac21b5738090cce94e30be62a9068f7e182106a5d0dd7568a4e8dc20`
- 擷取日期：`2026-05-31T13:59:08+00:00`
- 重新檢查日期：`2026-06-30T13:59:08+00:00`
- 支持主張：C-006, C-011, C-012

### `S-089` [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135910Z
- Snapshot hash：`sha256:e0c3ef9a9d054b536b29439350f474613fdab5908184deca2fa707dd611815ac`
- 擷取日期：`2026-05-31T13:59:10+00:00`
- 重新檢查日期：`2026-06-30T13:59:10+00:00`
- 支持主張：C-006, C-011

### `S-090` [OPA Pull Request Check Policies](https://www.openpolicyagent.org/docs/cicd/pr-checks)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135911Z
- Snapshot hash：`sha256:d7a9207a45ada880eff8ccc475ab65b00801b2d5f703eb417a1ad81f950f13e2`
- 擷取日期：`2026-05-31T13:59:11+00:00`
- 重新檢查日期：`2026-06-30T13:59:11+00:00`
- 支持主張：C-006, C-011

### `S-091` [Conftest Documentation](https://www.conftest.dev/)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135912Z
- Snapshot hash：`sha256:73716e6bfdd19f6359a67d4b1aad8dd7ab6e4132e7b8e58f7add039333d57d86`
- 擷取日期：`2026-05-31T13:59:12+00:00`
- 重新檢查日期：`2026-06-30T13:59:12+00:00`
- 支持主張：C-006, C-011

### `S-092` [Scale AI SWE-Bench Pro Article](https://scale.com/blog/swe-bench-pro)

- 證據層級：`C`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135914Z
- Snapshot hash：`sha256:ceeac953cb31e2d1406fbfe7ecbf580f821080c5a3ae9ad8f5dd1399354e8f4c`
- 擷取日期：`2026-05-31T13:59:14+00:00`
- 重新檢查日期：`2026-06-30T13:59:14+00:00`
- 支持主張：C-009

### `S-093` [Scale Labs SWE-Bench Pro Paper Page](https://labs.scale.com/papers/swe_bench_pro)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135915Z
- Snapshot hash：`sha256:2cb95018f28c6fca35a030913aa234ae6108de4ab73b108668fa5ca97db6cccc`
- 擷取日期：`2026-05-31T13:59:15+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：C-009

### `S-094` [R2Code Requirements-to-Code Traceability](https://arxiv.org/abs/2604.22432)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135915Z
- Snapshot hash：`sha256:9ace88c7c266c9345be4822edb25ad97c8fb20f2283ef1a195eb356a388354f5`
- 擷取日期：`2026-05-31T13:59:15+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：C-010

### `S-095` [ReqToCode Compile-Time Traceability](https://arxiv.org/abs/2603.13999)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135916Z
- Snapshot hash：`sha256:42be71ec5e69b1711784c0ea1d899e48ebecd07400362e3d0591085cbb6cd7aa`
- 擷取日期：`2026-05-31T13:59:16+00:00`
- 重新檢查日期：`stable/on-demand`
- 支持主張：C-003, C-010

### `S-096` [CISA Secure by Design](https://www.cisa.gov/resources-tools/resources/secure-by-design)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135916Z
- Snapshot hash：`sha256:8b42f4c9b370e4dd0113f8f7b79da017230012a120b625e73d4d6632ffab169a`
- 擷取日期：`2026-05-31T13:59:16+00:00`
- 重新檢查日期：`2026-06-30T13:59:16+00:00`
- 支持主張：C-006, C-008

### `S-097` [CISA Product Security Bad Practices](https://www.cisa.gov/resources-tools/resources/product-security-bad-practices)

- 證據層級：`A`
- 固定版本：未取得；使用本地 snapshot 保存擷取內容
- Commit SHA：`未取得`
- 頁面定位：local snapshot SNAP-20260531T135917Z
- Snapshot hash：`sha256:db60da09c9d430ab7a6d1238a8285028bea137ab3329764b5ee0892a3365cad6`
- 擷取日期：`2026-05-31T13:59:17+00:00`
- 重新檢查日期：`2026-06-30T13:59:17+00:00`
- 支持主張：C-006, C-008

## 變更紀錄

- 9.0.0: 對齊可信報告 schema；加入 scope、evidence-aware quality score、structural score、雙向 backlinks、source snapshot hash、freshness、47 筆 GitHub commit permalink 與可重現性限制；將 benchmark 建議 C-009 調整為 medium confidence。
- 8.0.0: 將衝突與未知升級為 resolution matrix；三個衝突標記為 resolved，安全政策 baseline 標記為 partially_resolved，其餘 benchmark、brownfield PoC 與研究重現保留 open 並新增 closure criteria。
- 7.0.0: 在可落地建議新增開源工具選型維度；提供只使用一個開源工具與多個開源工具配合的前三種推薦，並列出理由、缺口、整合流程、驗收標準與研究提示詞。
- 6.0.0: 將建議拆分為可實作性與未來性；新增可落地技術組合、流程、最小交付物、驗收標準，以及可交給 agent 的後續研究提示詞。
- 5.0.0: 擴充至 97 份主要來源；新增 requirements assurance、policy-as-code、secure SDLC 與 benchmark 來源；重構成熟度軸與特化軸；新增最穩健需求對照 assurance architecture。
