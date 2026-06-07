# A2A Agent 溝通（AI Coding 團隊）：來源目錄

本目錄保存 `a2a-agent-communication-ai-coding-team` 的已收集來源。正式報告撰寫前，必須先將每份 `summary.md` 由初始 HTML 摘要改寫成 reviewed summary。

## 目前來源狀態

| Source ID | 分類 | 來源 | 用途 |
| --- | --- | --- | --- |
| `S-001` | A2A 協定 | [A2A Official GitHub Repository](https://github.com/a2aproject/A2A) | 規格、SDK、範例與 Linux Foundation/a2aproject governance |
| `S-002` | A2A 背景 | [A2A A New Era of Agent Interoperability](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) | Google 對 A2A 動機、企業 interoperability 與生態夥伴的說明 |
| `S-003` | MCP 協定 | [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | 比較 MCP 的 agent-to-tool/context 定位 |
| `S-004` | MCP 規格 | [Model Context Protocol Latest Specification](https://modelcontextprotocol.io/specification/2025-11-25) | JSON-RPC、host/client/server、tools/resources/prompts、安全原則 |
| `S-005` | Redirect snapshot | [A2A Protocol Official Documentation](https://a2a-protocol.org/) | 僅保存 redirect 頁；正式分析時優先使用 `S-018` |
| `S-006` | A2A 規格 | [A2A Protocol Specification v1.0](https://a2a-protocol.org/latest/specification/) | AgentCard、Task、Message、Part、Artifact、streaming、auth 與 task operations |
| `S-007` | MCP repo | [MCP Official Specification Repository](https://github.com/modelcontextprotocol/modelcontextprotocol) | MCP spec repo、schema、docs history |
| `S-008` | Framework | [OpenAI Agents SDK Agents](https://openai.github.io/openai-agents-python/agents/) | agent、tools、guardrails、sessions、orchestration model |
| `S-009` | Framework | [OpenAI Agents SDK Handoffs](https://openai.github.io/openai-agents-python/handoffs/) | specialist handoff、input filter、handoff prompt 與 human-in-the-loop |
| `S-010` | Observability | [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/) | handoff trace、workflow observability、evidence |
| `S-011` | Framework | [LangGraph Multi-Agent Concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) | 舊 URL redirect；後續應補抓目前 docs.langchain.com canonical page |
| `S-012` | Framework | [AutoGen Multi-agent Conversation Framework](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/) | multi-agent conversation、role delegation、coding/team chat |
| `S-013` | Framework | [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/) | enterprise agent framework 與 multi-agent orchestration |
| `S-014` | ACP | [IBM Agent Communication Protocol](https://research.ibm.com/projects/agent-communication-protocol) | ACP 與 A2A/MCP 的比較；IBM 註明 ACP 已納入 A2A under Linux Foundation |
| `S-015` | ACP repo | [ACP BeeAI Reference Repository](https://github.com/i-am-bee/acp) | ACP reference implementation 與 BeeAI ecosystem |
| `S-016` | ANP | [Agent Network Protocol Repository](https://github.com/agent-network-protocol/AgentNetworkProtocol) | identity、discovery、agent network 與 peer-to-peer 通訊 |
| `S-017` | AG-UI | [AG-UI Protocol Repository](https://github.com/ag-ui-protocol/ag-ui) | 區分 agent-to-user UI event protocol 與 agent-to-agent communication |
| `S-018` | A2A docs | [A2A Protocol Latest Documentation](https://a2a-protocol.org/latest/) | A2A latest documentation canonical landing page |

## 需要補強

- 將 `S-005` 視為 redirect-only，不用於主要主張。
- 將 `S-011` 與 `S-012` 補抓 canonical redirected pages，避免只保存 redirect stub。
- 優先處理 `Q-011` 到 `Q-021`，完成 OpenAI platform guide、LangGraph supervisor、IBM protocol overview 與其他 protocol comparison。
- 搜尋項目 `Q-022` 到 `Q-038` 用於補足 CrewAI、Pydantic AI、AGNTCY、Anthropic、security、benchmark 與 coding-team 實證研究。
