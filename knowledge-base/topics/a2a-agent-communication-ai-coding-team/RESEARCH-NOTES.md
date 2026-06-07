# A2A Agent 溝通（AI Coding 團隊）研究筆記

## 目前階段

狀態：研究啟動與來源建庫階段。

已建立：

- `topic.json`：8 個研究問題，聚焦 AI coding team 的 agent-to-agent 溝通。
- `research-request.json`：正式研究請求與輸出設定。
- `crawl-queue.json` / `crawl-queue.md`：41 個候選來源與後續 gap 項。
- `sources/`：已收集 `S-001` 到 `S-018`。

## 第一輪判讀假設

- A2A 不應被視為 MCP 的替代品。A2A 偏「agent-to-agent/task/artifact/agent card」層；MCP 偏「agent-to-tool/context/resource/prompt」層。
- AI coding team 需要至少三種通訊面：跨 runtime 的 agent protocol、同一 runtime 內的 handoff/orchestration、以及不可變 artifact/evidence contract。
- 只用 framework handoff 可以快速落地，但難以跨 vendor、跨 repo 或跨 runtime；只用 A2A 則仍需要本地 orchestration、state store、trace 與 policy gate。
- 可靠 coding-team 架構需要把「聊天內容」轉成可稽核產物：task state、requirement reference、code diff、test evidence、review evidence、trace ID、capability boundary。

## 初始分類

| 層級 | 研究重點 | 已有來源 |
| --- | --- | --- |
| Agent-to-agent protocol | discovery、agent card、task lifecycle、message、artifact、streaming、auth | `S-001`, `S-002`, `S-006`, `S-018` |
| Agent-to-tool protocol | host/client/server、tools、resources、prompts、consent、安全 | `S-003`, `S-004`, `S-007` |
| Framework handoff | same-runtime specialist handoff、supervisor、team chat、trace | `S-008`, `S-009`, `S-010`, `S-011`, `S-012`, `S-013` |
| Adjacent protocols | ACP、ANP、AG-UI 與 A2A/MCP 的邊界 | `S-014`, `S-015`, `S-016`, `S-017` |

## 後續工作

1. 將 `S-001` 到 `S-018` 的初始摘要改成 reviewed summaries。
2. 補抓 redirect canonical pages：LangGraph current docs、AutoGen current docs、A2A docs final page。
3. 處理 `Q-022` 到 `Q-038` 搜尋項，補足 CrewAI、Pydantic AI、AGNTCY、Anthropic、security、benchmark 與 coding-team paper。
4. 建立 claim-evidence matrix，先回答「A2A/MCP/framework handoff 各解哪一層」。
5. 產出第一版架構建議：AI coding team communication contract 與最小 PoC。
