# A2A Agent Communication Sources Catalog

Updated: 2026-06-07T09:30:00+08:00

This catalog maps `S-001` to `S-045` to their role in the A2A Agent communication / AI Coding team research. Raw snapshots stay under each source folder and are ignored by Git when archived separately.

## Overview

| Source | Category | Evidence tier | Title | Role in research |
| --- | --- | --- | --- | --- |
| `S-001` | A2A core | A | [A2A Official GitHub Repository](https://github.com/a2aproject/A2A) | A2A official repository. It anchors AgentCard, task, message, artifact, streaming, sample implementation, and protocol governance details. |
| `S-002` | A2A core | A | [A2A A New Era of Agent Interoperability](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) | Google launch explanation for A2A. Useful for the motivation: agents need to collaborate across vendors, apps, and long-running enterprise workflows. |
| `S-003` | MCP comparison | A | [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | Official MCP introduction. It defines MCP as a model-to-context/tool/resource protocol, which is complementary rather than equivalent to A2A. |
| `S-004` | MCP comparison | A | [Model Context Protocol Latest Specification](https://modelcontextprotocol.io/specification/2025-11-25) | MCP 2025-11-25 specification. It grounds transport, tool/resource/prompt capability exposure, and host/client/server security boundaries. |
| `S-005` | A2A core | A | [A2A Protocol Official Documentation](https://a2a-protocol.org/) | A2A landing page capture. Lower value than the latest specification but retained for provenance and redirects. |
| `S-006` | A2A core | A | [A2A Protocol Specification v1.0](https://a2a-protocol.org/latest/specification/) | A2A protocol specification v1.0. Main evidence for task lifecycle, AgentCard discovery, message parts, artifacts, events, and auth-related extension points. |
| `S-007` | MCP comparison | A | [MCP Official Specification Repository](https://github.com/modelcontextprotocol/modelcontextprotocol) | MCP official specification repository. Useful for provenance, versioning, and implementation traceability. |
| `S-008` | Framework orchestration | A | [OpenAI Agents SDK Agents](https://openai.github.io/openai-agents-python/agents/) | OpenAI Agents SDK agent model. It supports tools, instructions, guardrails, sessions, and orchestration primitives for same-runtime agent teams. |
| `S-009` | Framework orchestration | A | [OpenAI Agents SDK Handoffs](https://openai.github.io/openai-agents-python/handoffs/) | OpenAI Agents SDK handoffs. Directly relevant to specialist transfer in an AI coding team, especially explicit delegation and input filtering. |
| `S-010` | Observability | A | [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/) | OpenAI Agents SDK tracing. Provides evidence capture, debugging, and handoff observability needed for auditable coding-team execution. |
| `S-011` | Framework orchestration | A | [LangGraph Multi-Agent Concepts](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) | Earlier LangGraph multi-agent page capture. Superseded by current LangChain/LangGraph docs but still useful as historical context. |
| `S-012` | Framework orchestration | A | [AutoGen Multi-agent Conversation Framework](https://microsoft.github.io/autogen/docs/Use-Cases/agent_chat/) | AutoGen agent chat page capture. It represents conversation-based multi-agent collaboration patterns, though the captured page should be refreshed before implementation. |
| `S-013` | Framework orchestration | A | [Semantic Kernel Agent Framework](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/) | Semantic Kernel Agent Framework documentation. Useful for enterprise .NET/Python orchestration, agent threads, and group collaboration patterns. |
| `S-014` | Adjacent protocols | A | [IBM Agent Communication Protocol](https://research.ibm.com/projects/agent-communication-protocol) | IBM ACP project page. It positions ACP as an agent communication protocol and notes convergence with A2A under the Linux Foundation ecosystem. |
| `S-015` | Adjacent protocols | A | [ACP BeeAI Reference Repository](https://github.com/i-am-bee/acp) | BeeAI ACP repository. Provides practical protocol and reference implementation material for agent-to-agent communication comparison. |
| `S-016` | Adjacent protocols | A | [Agent Network Protocol Repository](https://github.com/agent-network-protocol/AgentNetworkProtocol) | Agent Network Protocol repository. Useful for identity, discovery, and decentralized agent-network comparison. |
| `S-017` | Adjacent protocols | A | [AG-UI Protocol Repository](https://github.com/ag-ui-protocol/ag-ui) | AG-UI protocol repository. Separates agent-to-user UI event streams from agent-to-agent task communication. |
| `S-018` | A2A core | A | [A2A Protocol Latest Documentation](https://a2a-protocol.org/latest/) | A2A latest docs page. Canonical replacement for older pages and useful for current navigation. |
| `S-019` | Framework orchestration | A | [OpenAI Agents SDK Platform Guide](https://developers.openai.com/api/docs/guides/agents) | OpenAI platform Agents SDK guide. Production-oriented framing for agents, tools, handoffs, tracing, and hosted runtime choices. |
| `S-020` | Framework orchestration | A | [OpenAI Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | OpenAI practical guide to building agents. Useful for deciding when workflows, routing, evaluator-optimizer, and orchestrator-worker patterns are enough. |
| `S-021` | Framework orchestration | A | [LangGraph Supervisor Repository](https://github.com/langchain-ai/langgraph-supervisor-py) | LangGraph supervisor repository. Gives a concrete supervisor/team implementation pattern for routing work among specialist agents. |
| `S-022` | Protocol synthesis | A | [IBM What Are AI Agent Protocols](https://www.ibm.com/think/topics/ai-agent-protocols) | IBM overview of AI agent protocols. Secondary synthesis comparing A2A, MCP, ACP, ANP, and AG-UI. |
| `S-023` | Protocol synthesis | A | [Survey of Agent Interoperability Protocols](https://arxiv.org/abs/2505.02279) | Survey of agent interoperability protocols. Academic comparison source for MCP, ACP, A2A, ANP, and protocol design dimensions. |
| `S-024` | Benchmarks | A | [SWE-bench Official Site](https://www.swebench.com/) | SWE-bench official site. Baseline for evaluating coding agents against real GitHub issues, but not sufficient by itself for multi-agent handoff quality. |
| `S-025` | Benchmarks | A | [SWE-bench Repository](https://github.com/SWE-bench/SWE-bench) | SWE-bench repository. Provides task format, harness, and reproducibility material for coding-agent benchmark design. |
| `S-026` | Framework orchestration | A | [LangChain Multi-agent Patterns](https://docs.langchain.com/oss/python/langchain/multi-agent/index) | LangChain current multi-agent patterns. Distinguishes tool-calling supervisors from handoffs and emphasizes context engineering. |
| `S-027` | Framework orchestration | A | [LangChain Multi-agent Handoffs](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs) | LangChain handoffs documentation. Useful for active-agent switching and user-facing specialist transitions. |
| `S-028` | Framework orchestration | A | [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) | LangGraph overview. Strong evidence for durable execution, persistence, streaming, human-in-the-loop, and stateful agent graphs. |
| `S-029` | Framework orchestration | A | [Pydantic AI Multi-Agent Patterns](https://pydantic.dev/docs/ai/guides/multi-agent-applications/) | Pydantic AI multi-agent guide. Lightweight Python option with delegation, programmatic control, and typed outputs. |
| `S-030` | Framework orchestration | A | [CrewAI Introduction](https://docs.crewai.com/en/introduction) | CrewAI introduction. Production multi-agent framework focused on crews, flows, role/task modeling, and operational deployment. |
| `S-031` | Framework orchestration | A | [CrewAI Crews](https://docs.crewai.com/en/concepts/crews) | CrewAI crews concept page. Direct evidence for collaborative role-based agents, tasks, processes, and hierarchical execution. |
| `S-032` | Adjacent protocols | A | [AGNTCY ACP OpenAPI Specification](https://spec.acp.agntcy.org/) | AGNTCY ACP OpenAPI specification. Useful as a machine-readable comparison point for protocol surface and runtime calls. |
| `S-033` | Framework orchestration | A | [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | Anthropic building effective agents article. Important counterweight: prefer simple workflows first, then add agentic systems when flexibility is worth the cost. |
| `S-034` | Framework orchestration | A | [Anthropic Building Effective AI Agents Resource](https://resources.anthropic.com/building-effective-ai-agents) | Anthropic guidance on effective agents. Important counterweight: prefer simpler workflows until agentic flexibility is truly needed. |
| `S-035` | Coding-team research | A | [ChatDev Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) | ChatDev paper. Demonstrates a virtual software company using role-play and structured communication for software development. |
| `S-036` | Coding-team implementation | A | [ChatDev Repository](https://github.com/OpenBMB/ChatDev) | ChatDev repository. Practical implementation reference for multi-role AI software company style coding teams. |
| `S-037` | Coding-team research | A | [MetaGPT Multi-Agent Collaborative Framework Paper](https://arxiv.org/abs/2308.00352) | MetaGPT paper. Shows SOP-oriented multi-agent collaboration that translates requirements into structured software artifacts. |
| `S-038` | Coding-team implementation | A | [MetaGPT Repository](https://github.com/FoundationAgents/MetaGPT) | MetaGPT repository. Implementation reference for product manager, architect, engineer, and QA-style software company roles. |
| `S-039` | Coding-team research | A | [AgentCoder Multi-Agent Code Generation Paper](https://arxiv.org/abs/2312.13010) | AgentCoder paper. Provides a programmer, test designer, and test executor loop for code generation and validation. |
| `S-040` | Security | A | [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) | OWASP MCP Top 10. Key source for tool poisoning, excessive permissions, rug-pull risks, and MCP-specific controls. |
| `S-041` | Security | A | [OWASP Agentic Skills Top 10](https://owasp.org/www-project-agentic-skills-top-10/) | OWASP Agentic Skills Top 10. Directly relevant to the user's question about agent skills as a separate attack surface. |
| `S-042` | Security | A | [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | OWASP Top 10 for LLM Applications. Baseline for prompt injection, sensitive information disclosure, excessive agency, and supply-chain risk. |
| `S-043` | Governance | A | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | NIST AI Risk Management Framework. Governance baseline for trustworthy, risk-managed deployment of AI agent systems. |
| `S-044` | Security | A | [Prompt Injection Attacks on Agentic Coding Assistants](https://arxiv.org/abs/2601.17548) | Prompt injection attacks on agentic coding assistants. Research evidence that coding agents are exposed through skills, tools, docs, and protocol channels. |
| `S-045` | Security | A | [AIShellJack Prompt Injection Attacks on Coding Editors](https://arxiv.org/abs/2509.22040) | AIShellJack paper. Research evidence on prompt-injection attacks against agentic coding editors and shell/tool execution paths. |

## Category Index

- **A2A core**: `S-001`, `S-002`, `S-005`, `S-006`, `S-018`
- **Adjacent protocols**: `S-014`, `S-015`, `S-016`, `S-017`, `S-032`
- **Benchmarks**: `S-024`, `S-025`
- **Coding-team implementation**: `S-036`, `S-038`
- **Coding-team research**: `S-035`, `S-037`, `S-039`
- **Framework orchestration**: `S-008`, `S-009`, `S-011`, `S-012`, `S-013`, `S-019`, `S-020`, `S-021`, `S-026`, `S-027`, `S-028`, `S-029`, `S-030`, `S-031`, `S-033`, `S-034`
- **Governance**: `S-043`
- **MCP comparison**: `S-003`, `S-004`, `S-007`
- **Observability**: `S-010`
- **Protocol synthesis**: `S-022`, `S-023`
- **Security**: `S-040`, `S-041`, `S-042`, `S-044`, `S-045`
