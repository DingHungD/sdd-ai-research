#!/usr/bin/env python3
"""Generate the A2A agent communication research report.

This script intentionally keeps the synthesis in code so the report can be
regenerated after more sources are collected.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_pipeline.quality_gate import evaluate_report_details

TOPIC = "a2a-agent-communication-ai-coding-team"
TOPIC_DIR = ROOT / "knowledge-base" / "topics" / TOPIC
SOURCES_DIR = TOPIC_DIR / "sources"
REPORTS_DIR = TOPIC_DIR / "reports"
GENERATED_AT = "2026-06-07T09:30:00+08:00"
DATA_CUTOFF = "2026-06-07"


SOURCE_OVERVIEWS: dict[str, dict[str, str]] = {
    "S-001": {
        "category": "A2A core",
        "summary": "A2A official repository. It anchors AgentCard, task, message, artifact, streaming, sample implementation, and protocol governance details.",
    },
    "S-002": {
        "category": "A2A core",
        "summary": "Google launch explanation for A2A. Useful for the motivation: agents need to collaborate across vendors, apps, and long-running enterprise workflows.",
    },
    "S-003": {
        "category": "MCP comparison",
        "summary": "Official MCP introduction. It defines MCP as a model-to-context/tool/resource protocol, which is complementary rather than equivalent to A2A.",
    },
    "S-004": {
        "category": "MCP comparison",
        "summary": "MCP 2025-11-25 specification. It grounds transport, tool/resource/prompt capability exposure, and host/client/server security boundaries.",
    },
    "S-005": {
        "category": "A2A core",
        "summary": "A2A landing page capture. Lower value than the latest specification but retained for provenance and redirects.",
    },
    "S-006": {
        "category": "A2A core",
        "summary": "A2A protocol specification v1.0. Main evidence for task lifecycle, AgentCard discovery, message parts, artifacts, events, and auth-related extension points.",
    },
    "S-007": {
        "category": "MCP comparison",
        "summary": "MCP official specification repository. Useful for provenance, versioning, and implementation traceability.",
    },
    "S-008": {
        "category": "Framework orchestration",
        "summary": "OpenAI Agents SDK agent model. It supports tools, instructions, guardrails, sessions, and orchestration primitives for same-runtime agent teams.",
    },
    "S-009": {
        "category": "Framework orchestration",
        "summary": "OpenAI Agents SDK handoffs. Directly relevant to specialist transfer in an AI coding team, especially explicit delegation and input filtering.",
    },
    "S-010": {
        "category": "Observability",
        "summary": "OpenAI Agents SDK tracing. Provides evidence capture, debugging, and handoff observability needed for auditable coding-team execution.",
    },
    "S-011": {
        "category": "Framework orchestration",
        "summary": "Earlier LangGraph multi-agent page capture. Superseded by current LangChain/LangGraph docs but still useful as historical context.",
    },
    "S-012": {
        "category": "Framework orchestration",
        "summary": "AutoGen agent chat page capture. It represents conversation-based multi-agent collaboration patterns, though the captured page should be refreshed before implementation.",
    },
    "S-013": {
        "category": "Framework orchestration",
        "summary": "Semantic Kernel Agent Framework documentation. Useful for enterprise .NET/Python orchestration, agent threads, and group collaboration patterns.",
    },
    "S-014": {
        "category": "Adjacent protocols",
        "summary": "IBM ACP project page. It positions ACP as an agent communication protocol and notes convergence with A2A under the Linux Foundation ecosystem.",
    },
    "S-015": {
        "category": "Adjacent protocols",
        "summary": "BeeAI ACP repository. Provides practical protocol and reference implementation material for agent-to-agent communication comparison.",
    },
    "S-016": {
        "category": "Adjacent protocols",
        "summary": "Agent Network Protocol repository. Useful for identity, discovery, and decentralized agent-network comparison.",
    },
    "S-017": {
        "category": "Adjacent protocols",
        "summary": "AG-UI protocol repository. Separates agent-to-user UI event streams from agent-to-agent task communication.",
    },
    "S-018": {
        "category": "A2A core",
        "summary": "A2A latest docs page. Canonical replacement for older pages and useful for current navigation.",
    },
    "S-019": {
        "category": "Framework orchestration",
        "summary": "OpenAI platform Agents SDK guide. Production-oriented framing for agents, tools, handoffs, tracing, and hosted runtime choices.",
    },
    "S-020": {
        "category": "Framework orchestration",
        "summary": "OpenAI practical guide to building agents. Useful for deciding when workflows, routing, evaluator-optimizer, and orchestrator-worker patterns are enough.",
    },
    "S-021": {
        "category": "Framework orchestration",
        "summary": "LangGraph supervisor repository. Gives a concrete supervisor/team implementation pattern for routing work among specialist agents.",
    },
    "S-022": {
        "category": "Protocol synthesis",
        "summary": "IBM overview of AI agent protocols. Secondary synthesis comparing A2A, MCP, ACP, ANP, and AG-UI.",
    },
    "S-023": {
        "category": "Protocol synthesis",
        "summary": "Survey of agent interoperability protocols. Academic comparison source for MCP, ACP, A2A, ANP, and protocol design dimensions.",
    },
    "S-024": {
        "category": "Benchmarks",
        "summary": "SWE-bench official site. Baseline for evaluating coding agents against real GitHub issues, but not sufficient by itself for multi-agent handoff quality.",
    },
    "S-025": {
        "category": "Benchmarks",
        "summary": "SWE-bench repository. Provides task format, harness, and reproducibility material for coding-agent benchmark design.",
    },
    "S-026": {
        "category": "Framework orchestration",
        "summary": "LangChain current multi-agent patterns. Distinguishes tool-calling supervisors from handoffs and emphasizes context engineering.",
    },
    "S-027": {
        "category": "Framework orchestration",
        "summary": "LangChain handoffs documentation. Useful for active-agent switching and user-facing specialist transitions.",
    },
    "S-028": {
        "category": "Framework orchestration",
        "summary": "LangGraph overview. Strong evidence for durable execution, persistence, streaming, human-in-the-loop, and stateful agent graphs.",
    },
    "S-029": {
        "category": "Framework orchestration",
        "summary": "Pydantic AI multi-agent guide. Lightweight Python option with delegation, programmatic control, and typed outputs.",
    },
    "S-030": {
        "category": "Framework orchestration",
        "summary": "CrewAI introduction. Production multi-agent framework focused on crews, flows, role/task modeling, and operational deployment.",
    },
    "S-031": {
        "category": "Framework orchestration",
        "summary": "CrewAI crews concept page. Direct evidence for collaborative role-based agents, tasks, processes, and hierarchical execution.",
    },
    "S-032": {
        "category": "Adjacent protocols",
        "summary": "AGNTCY ACP OpenAPI specification. Useful as a machine-readable comparison point for protocol surface and runtime calls.",
    },
    "S-033": {
        "category": "Framework orchestration",
        "summary": "Anthropic building effective agents article. Important counterweight: prefer simple workflows first, then add agentic systems when flexibility is worth the cost.",
    },
    "S-034": {
        "category": "Framework orchestration",
        "summary": "Anthropic guidance on effective agents. Important counterweight: prefer simpler workflows until agentic flexibility is truly needed.",
    },
    "S-035": {
        "category": "Coding-team research",
        "summary": "ChatDev paper. Demonstrates a virtual software company using role-play and structured communication for software development.",
    },
    "S-036": {
        "category": "Coding-team implementation",
        "summary": "ChatDev repository. Practical implementation reference for multi-role AI software company style coding teams.",
    },
    "S-037": {
        "category": "Coding-team research",
        "summary": "MetaGPT paper. Shows SOP-oriented multi-agent collaboration that translates requirements into structured software artifacts.",
    },
    "S-038": {
        "category": "Coding-team implementation",
        "summary": "MetaGPT repository. Implementation reference for product manager, architect, engineer, and QA-style software company roles.",
    },
    "S-039": {
        "category": "Coding-team research",
        "summary": "AgentCoder paper. Provides a programmer, test designer, and test executor loop for code generation and validation.",
    },
    "S-040": {
        "category": "Security",
        "summary": "OWASP MCP Top 10. Key source for tool poisoning, excessive permissions, rug-pull risks, and MCP-specific controls.",
    },
    "S-041": {
        "category": "Security",
        "summary": "OWASP Agentic Skills Top 10. Directly relevant to the user's question about agent skills as a separate attack surface.",
    },
    "S-042": {
        "category": "Security",
        "summary": "OWASP Top 10 for LLM Applications. Baseline for prompt injection, sensitive information disclosure, excessive agency, and supply-chain risk.",
    },
    "S-043": {
        "category": "Governance",
        "summary": "NIST AI Risk Management Framework. Governance baseline for trustworthy, risk-managed deployment of AI agent systems.",
    },
    "S-044": {
        "category": "Security",
        "summary": "Prompt injection attacks on agentic coding assistants. Research evidence that coding agents are exposed through skills, tools, docs, and protocol channels.",
    },
    "S-045": {
        "category": "Security",
        "summary": "AIShellJack paper. Research evidence on prompt-injection attacks against agentic coding editors and shell/tool execution paths.",
    },
}


CLAIMS: list[dict[str, Any]] = [
    {
        "claim_id": "C-001",
        "statement": "A2A and MCP solve different communication layers: A2A is best treated as an external agent-to-agent task and artifact protocol, while MCP exposes tools, resources, prompts, and context to an agent runtime.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-001", "S-003", "S-004", "S-006", "S-018", "S-022", "S-023"],
        "opposing_source_ids": [],
        "reasoning": "The official specs expose different nouns and boundaries. A2A centers AgentCard, tasks, messages, parts, artifacts, and status updates; MCP centers host/client/server capability exposure.",
    },
    {
        "claim_id": "C-002",
        "statement": "For an AI coding team, same-runtime orchestration should usually use framework handoffs or graph control, not A2A, unless agents are separated by vendor, runtime, permission boundary, or long-running service ownership.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-008", "S-009", "S-010", "S-020", "S-026", "S-027", "S-028", "S-029", "S-033", "S-034"],
        "opposing_source_ids": ["S-001", "S-006"],
        "reasoning": "Frameworks provide lower-latency local state, typed handoff, tracing, and graph control. A2A becomes valuable when the communication boundary is broader than one framework runtime.",
    },
    {
        "claim_id": "C-003",
        "statement": "The minimum robust coding-team contract is not free-form chat; it needs task state, role, requirement references, input artifacts, output artifacts, test evidence, review evidence, trace IDs, and policy/capability boundaries.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-006", "S-009", "S-010", "S-024", "S-025", "S-028", "S-040", "S-041", "S-042", "S-043"],
        "opposing_source_ids": [],
        "reasoning": "Specs and benchmarks consistently show the need to preserve artifacts, state, traces, and reproducibility. Security sources add the need for permission and policy evidence.",
    },
    {
        "claim_id": "C-004",
        "statement": "Multi-agent coding is worthwhile only when role separation, independent verification, long-context partitioning, parallel exploration, or cross-domain/tool isolation outweigh orchestration overhead.",
        "importance": "critical",
        "confidence": "medium-high",
        "supporting_source_ids": ["S-020", "S-026", "S-029", "S-030", "S-031", "S-033", "S-034", "S-035", "S-037", "S-039"],
        "opposing_source_ids": [],
        "reasoning": "Anthropic and framework docs emphasize simpler workflows first, while coding-team papers show benefits when roles and verification loops are explicit.",
    },
    {
        "claim_id": "C-005",
        "statement": "A practical AI coding team should start with planner, implementer, tester, reviewer, and security/policy roles; product-manager and architect roles become useful when requirements are ambiguous or architecture-heavy.",
        "importance": "critical",
        "confidence": "medium-high",
        "supporting_source_ids": ["S-009", "S-020", "S-026", "S-031", "S-035", "S-036", "S-037", "S-038", "S-039"],
        "opposing_source_ids": [],
        "reasoning": "The role sets from ChatDev, MetaGPT, and AgentCoder converge on planning, implementation, and verification, while modern frameworks provide the handoff mechanisms.",
    },
    {
        "claim_id": "C-006",
        "statement": "Agent skills are a real architectural layer, but they widen the attack surface; they should be versioned, permission-scoped, tested, and policy-checked like tools.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-041", "S-042", "S-044", "S-045", "S-026"],
        "opposing_source_ids": [],
        "reasoning": "OWASP Agentic Skills Top 10 and recent coding-assistant attack papers identify skills, tool descriptions, and shell interactions as injection and capability-escalation vectors.",
    },
    {
        "claim_id": "C-007",
        "statement": "Current benchmarks such as SWE-bench are necessary but insufficient for A2A coding-team communication; the report should add handoff correctness, artifact completeness, defect catch rate, security catch rate, recovery, cost, latency, and human-intervention metrics.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-024", "S-025", "S-035", "S-037", "S-039", "S-044", "S-045"],
        "opposing_source_ids": [],
        "reasoning": "SWE-bench evaluates final coding task success, while multi-agent architecture needs extra measurements for communication quality and defense-in-depth.",
    },
    {
        "claim_id": "C-008",
        "statement": "Adjacent protocols should be classified by layer: A2A/ACP/ANP handle agent communication and discovery, MCP handles tool/context access, and AG-UI handles user-interface event streams.",
        "importance": "important",
        "confidence": "high",
        "supporting_source_ids": ["S-014", "S-015", "S-016", "S-017", "S-022", "S-023", "S-032"],
        "opposing_source_ids": [],
        "reasoning": "The protocol nouns, transport surfaces, and target participants differ enough that a single-protocol architecture would blur responsibilities.",
    },
    {
        "claim_id": "C-009",
        "statement": "The best first PoC is a hybrid: one internal orchestration framework for the coding team, MCP for tools and repository context, an A2A-compatible task/artifact envelope at team boundaries, and a policy gate for risky actions.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-001", "S-004", "S-006", "S-008", "S-009", "S-010", "S-028", "S-040", "S-041", "S-043"],
        "opposing_source_ids": [],
        "reasoning": "This combines the lowest-friction local orchestration with protocol-grade external boundaries and security controls.",
    },
    {
        "claim_id": "C-010",
        "statement": "Security policy must be enforced before tool execution and before accepting cross-agent artifacts, because prompt injection can travel through documentation, code comments, tool descriptions, skills, and protocol payloads.",
        "importance": "critical",
        "confidence": "high",
        "supporting_source_ids": ["S-040", "S-041", "S-042", "S-044", "S-045"],
        "opposing_source_ids": [],
        "reasoning": "OWASP and recent research sources converge on indirect prompt injection, tool poisoning, excessive agency, and shell-command abuse as high-priority risks.",
    },
]


def load_sources() -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for path in sorted(SOURCES_DIR.glob("S-*/source.json")):
        with path.open("r", encoding="utf-8") as handle:
            source = json.load(handle)
        overview = SOURCE_OVERVIEWS.get(source["source_id"], {})
        source.setdefault("quality", {})
        source["quality"]["review_summary"] = overview.get("summary", "")
        source["quality"]["category"] = overview.get("category", "Uncategorized")
        sources.append(source)
    return sources


def build_backlinks() -> dict[str, list[str]]:
    backlinks: dict[str, set[str]] = defaultdict(set)
    for claim in CLAIMS:
        for source_id in claim["supporting_source_ids"]:
            backlinks[source_id].add(claim["claim_id"])
    return {source_id: sorted(claim_ids) for source_id, claim_ids in backlinks.items()}


def update_source_files(backlinks: dict[str, list[str]]) -> None:
    for path in sorted(SOURCES_DIR.glob("S-*/source.json")):
        with path.open("r", encoding="utf-8") as handle:
            source = json.load(handle)
        source["supported_claim_ids"] = backlinks.get(source["source_id"], [])
        overview = SOURCE_OVERVIEWS.get(source["source_id"], {})
        source.setdefault("quality", {})
        source["quality"]["review_summary"] = overview.get("summary", "")
        source["quality"]["category"] = overview.get("category", "Uncategorized")
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(source, handle, ensure_ascii=False, indent=2)
            handle.write("\n")


def build_report(sources: list[dict[str, Any]]) -> dict[str, Any]:
    report: dict[str, Any] = {
        "report_id": "a2a-agent-communication-ai-coding-team-20260607-v1",
        "version": "1.0",
        "title": "A2A Agent 溝通：AI Coding 團隊的協作協議、框架與安全架構研究",
        "generated_at": GENERATED_AT,
        "data_cutoff": DATA_CUTOFF,
        "overall_confidence": "medium-high",
        "minimum_sources": 40,
        "minimum_primary_sources": 28,
        "minimum_high_quality_sources": 35,
        "quality_score": 0,
        "structural_score": 0,
        "quality_metrics": {},
        "executive_summary": [
            "A2A 適合放在跨 runtime、跨 vendor、跨服務邊界的 agent-to-agent 任務協議；MCP 適合放在 agent-to-tool/context/resource 的能力存取層。兩者不是互斥替代品。",
            "AI Coding 團隊若只在同一個程式內運作，優先採用 OpenAI Agents SDK、LangGraph、Pydantic AI、CrewAI 等框架的 handoff、supervisor 或 graph 控制會更落地；A2A 應當作外部任務與 artifact boundary。",
            "穩健系統的核心不是增加 agent 數量，而是建立可審計的 contract：需求引用、任務狀態、角色、輸入/輸出 artifact、測試證據、review 證據、trace ID、權限與 policy gate。",
            "安全風險不只在工具，也在 agent skill、文件、code comments、tool description、protocol payload 與 shell execution。技能架構可以使用，但必須版本化、權限化與政策檢查。",
        ],
        "questions": [
            {
                "question_id": "RQ-001",
                "question": "A2A Agent 溝通與 MCP、ACP、ANP、AG-UI 的分工是什麼？",
                "answer_summary": "A2A/ACP/ANP 偏 agent-to-agent/discovery；MCP 偏工具與上下文；AG-UI 偏 agent-to-user UI event stream。",
            },
            {
                "question_id": "RQ-002",
                "question": "AI Coding 團隊應如何設計 agent role 與 handoff？",
                "answer_summary": "先用 planner/implementer/tester/reviewer/security 的最小角色集，再依需求複雜度加入 architect/product roles。",
            },
            {
                "question_id": "RQ-003",
                "question": "什麼時候需要 A2A，而不是框架內建 handoff？",
                "answer_summary": "跨 runtime、跨 vendor、跨服務、跨權限邊界、長任務或需外部 artifact contract 時用 A2A；同 runtime 內優先用框架 handoff/graph。",
            },
            {
                "question_id": "RQ-004",
                "question": "單一或多工具落地方案應如何選？",
                "answer_summary": "單工具以 OpenAI Agents SDK、LangGraph、CrewAI/Pydantic AI 分不同情境；多工具以 orchestration + MCP + A2A envelope + policy gate 為主。",
            },
            {
                "question_id": "RQ-005",
                "question": "安全與 governance 需要哪些控制？",
                "answer_summary": "權限最小化、tool/skill allowlist、artifact validation、Conftest/OPA 類 policy gate、trace、human approval、prompt-injection 防護與 NIST RMF 治理。",
            },
            {
                "question_id": "RQ-006",
                "question": "最小可實作 PoC 的通訊 contract 是什麼？",
                "answer_summary": "TaskEnvelope + Artifact + Evidence + Trace + PolicyDecision；不要只傳自然語言 chat transcript。",
            },
        ],
        "scope": {
            "included": [
                "A2A/MCP/ACP/ANP/AG-UI protocol comparison",
                "AI coding team orchestration frameworks",
                "multi-agent coding research and implementations",
                "benchmark and evaluation dimensions",
                "security, skill-layer, and governance controls",
                "implementable architecture recommendations",
            ],
            "excluded": [
                "直接實作完整 A2A server/client runtime",
                "大量跑 benchmark 實驗",
                "封閉商業平台的未公開能力比較",
            ],
        },
        "methodology": {
            "workflow": [
                "Step 3 依 crawl queue 建立候選來源順序。",
                "Step 4 收集官方規格、框架文件、研究論文、repo、benchmark 與安全治理資料。",
                "Step 5 將來源整理為 catalog 與 source review summary。",
                "Step 6 建立 claim-evidence matrix，將結論連回 source IDs。",
                "Step 7 將衝突分成 protocol boundary、framework boundary、benchmark insufficiency、安全未知，並提供 resolution matrix。",
                "Step 8 產生 JSON 與 Markdown 報告，並用 validate_report.py 檢查一致性。",
            ],
            "source_selection": "優先官方規格、官方文件、官方 repository、研究論文、benchmark、OWASP/NIST 等治理來源；商業或二手文章只作輔助，不作核心依據。",
            "source_count": len(sources),
        },
        "claims": CLAIMS,
        "sources": sources,
        "conflicts": [
            {
                "conflict_id": "F-001",
                "summary": "A2A vs MCP 容易被視為替代品，但兩者其實是不同層。",
                "positions": [
                    "A2A documents emphasize agent-to-agent tasks and artifacts.",
                    "MCP documents emphasize model-to-tool/context/resource access.",
                ],
                "impact": "若混用，會把 tool permission、task ownership、artifact lifecycle 放在錯誤層。",
            },
            {
                "conflict_id": "F-002",
                "summary": "多 agent coding team 可以提升結構化協作，也可能只增加延遲、成本與錯誤傳播。",
                "positions": [
                    "ChatDev, MetaGPT, AgentCoder show role specialization and verification loops.",
                    "Anthropic and framework docs warn that simpler workflows are often sufficient.",
                ],
                "impact": "PoC 必須用 benchmark 與 evidence contract 衡量，而不是預設 agent 越多越好。",
            },
            {
                "conflict_id": "F-003",
                "summary": "Agent skills 可提升複用性，但也成為新的供應鏈與 prompt injection 攻擊面。",
                "positions": [
                    "Framework docs expose skills/tools/subagents as productivity abstractions.",
                    "OWASP and research papers identify skill/tool descriptions and shell execution as attack vectors.",
                ],
                "impact": "技能架構要納入 policy gate、版本、審查與測試，不應直接信任。",
            },
        ],
        "unknowns": [
            {
                "unknown_id": "U-001",
                "summary": "缺少公開標準 benchmark 直接衡量 A2A coding-team communication quality。",
                "why_it_matters": "SWE-bench 主要看最後 patch 是否解決問題，不能直接看 handoff 是否正確、artifact 是否完整。",
            },
            {
                "unknown_id": "U-002",
                "summary": "A2A、ACP、ANP 的實作生態仍在快速變動。",
                "why_it_matters": "正式採用前需要重新檢查 2026 下半年的 spec、SDK、interop status。",
            },
            {
                "unknown_id": "U-003",
                "summary": "不同框架的成本、延遲、可靠度與維運成本需要實測。",
                "why_it_matters": "OpenAI Agents SDK、LangGraph、CrewAI、Pydantic AI 的取捨高度依賴 repo 型態與團隊習慣。",
            },
        ],
        "resolution_matrix": {
            "summary": "本報告將 protocol、framework、benchmark、安全四類衝突拆開處理：跨邊界用 A2A 類 envelope，同 runtime 用框架 handoff，工具層用 MCP，安全用 policy gate 與 evidence validation。",
            "conflict_resolutions": [
                {
                    "resolution_id": "R-F-001",
                    "conflict_id": "F-001",
                    "status": "resolved",
                    "resolution": "採用 layered architecture：A2A for external agent task/artifact boundary, MCP for tool/context access, framework handoff for local orchestration.",
                    "supporting_source_ids": ["S-001", "S-003", "S-004", "S-006", "S-022", "S-023"],
                },
                {
                    "resolution_id": "R-F-002",
                    "conflict_id": "F-002",
                    "status": "partially_resolved",
                    "resolution": "用角色分離與獨立驗證作為採用條件，並以 SWE-bench plus handoff/artifact/security metrics 測量是否真的有效。",
                    "supporting_source_ids": ["S-020", "S-024", "S-025", "S-035", "S-037", "S-039"],
                },
                {
                    "resolution_id": "R-F-003",
                    "conflict_id": "F-003",
                    "status": "resolved",
                    "resolution": "技能與工具都納入同一個 allowlist、版本鎖定、權限 scope、policy decision、trace 和 human approval 流程。",
                    "supporting_source_ids": ["S-040", "S-041", "S-042", "S-044", "S-045"],
                },
            ],
            "unknown_resolutions": [
                {
                    "resolution_id": "R-U-001",
                    "unknown_id": "U-001",
                    "status": "partially_resolved",
                    "resolution": "採用 SWE-bench 作為 final patch baseline，另加 handoff correctness、artifact completeness、defect/security catch rate、latency/cost、recovery 與 human intervention。",
                    "supporting_source_ids": ["S-024", "S-025", "S-035", "S-037", "S-039"],
                },
                {
                    "resolution_id": "R-U-002",
                    "unknown_id": "U-002",
                    "status": "open",
                    "resolution": "正式開發前重新跑 protocol source refresh；目前以 A2A 最新 docs、ACP/ANP/AG-UI source snapshot 作為 2026-06-07 判斷。",
                    "supporting_source_ids": ["S-001", "S-006", "S-014", "S-016", "S-017", "S-032", "S-033"],
                },
                {
                    "resolution_id": "R-U-003",
                    "unknown_id": "U-003",
                    "status": "open",
                    "resolution": "下一階段需要同一個 coding task 在 OpenAI Agents SDK、LangGraph、CrewAI/Pydantic AI 上跑最小 benchmark。",
                    "supporting_source_ids": ["S-008", "S-009", "S-028", "S-029", "S-030", "S-031"],
                },
            ],
        },
        "limitations": [
            "目前是文獻與文件研究，尚未實際跑 A2A server/client、MCP server、框架 runtime 的端到端 benchmark。",
            "部分頁面是快速變動的官方文件或 repository default branch；正式採納前要重新 refresh。",
            "S-005、S-011、S-012 的價值較低或可能是過期/redirect 捕捉，已在 catalog 中標示，核心結論主要依賴較新的來源。",
        ],
        "conclusion": "最穩健的方向是 layered hybrid：同一個 AI Coding 團隊內用成熟 framework 做 handoff/graph/state/tracing，工具與 repo context 透過 MCP 或類 MCP tool boundary 管理，跨團隊或跨 runtime 用 A2A-compatible task/artifact envelope，所有 risky tool/skill/action 經過 policy gate 與 evidence validation。這比單純追求全 A2A 或全多-agent 更可實作，也更容易驗證。",
        "recommendation_sections": build_recommendations(),
        "changelog": [
            {
                "date": DATA_CUTOFF,
                "change": "Generated v1 report from 45 curated sources and synchronized source claim backlinks.",
            }
        ],
    }
    metrics, _ = evaluate_report_details(report)
    report["quality_score"] = metrics["quality_score"]
    report["structural_score"] = metrics["structural_score"]
    report["quality_metrics"] = metrics
    return report


def build_recommendations() -> dict[str, Any]:
    return {
        "implementability": {
            "summary": "先實作最小 hybrid PoC，再擴充成 A2A boundary。不要一開始就把所有 agent 都做成遠端服務。",
            "items": [
                {
                    "title": "最小可落地 PoC：Framework handoff + MCP tools + A2A-compatible envelope + policy gate",
                    "objective": "在一個 repo 任務中讓 planner、implementer、tester、reviewer/security 產生可追蹤 artifact 與證據。",
                    "technologies": ["OpenAI Agents SDK or LangGraph", "MCP/tool adapter", "A2A TaskEnvelope JSON", "Conftest/OPA-style policy gate", "trace log"],
                    "workflow": [
                        "Planner 將需求拆成 task envelope，附 requirement IDs。",
                        "Implementer 產出 patch artifact，不直接執行高風險命令。",
                        "Tester 產出 test command、result、log hash。",
                        "Reviewer/Security 檢查 diff、tool use、skill use、policy decision。",
                        "Coordinator 只接受包含 evidence 的 final artifact。",
                    ],
                    "minimum_deliverable": "一個 CLI demo：輸入需求文件與 repo，輸出 task envelope、patch、test evidence、review evidence、policy decision、trace。",
                    "acceptance_criteria": [
                        "每個 artifact 可追溯到 source requirement。",
                        "每個 tool/skill execution 有 trace ID 與 policy decision。",
                        "失敗時能指出是哪個 agent、artifact、policy 或 test 失敗。",
                    ],
                    "supporting_source_ids": ["S-006", "S-009", "S-010", "S-028", "S-040", "S-041", "S-043"],
                    "research_prompt": "研究如何把 A2A Task/Artifact schema 映射到現有 framework handoff 與 MCP tool calls，並加入 Conftest/OPA policy gate。",
                }
            ],
        },
        "open_source_options": {
            "single_tool_recommendations": {
                "summary": "單一工具代表只選一個主要 orchestrator；A2A/MCP/policy 先以 adapter 或薄封裝保留，不必全部引入。",
                "items": [
                    {
                        "rank": 1,
                        "tool": "LangGraph / LangChain multi-agent",
                        "recommendation_reason": "最適合需要 durable state、graph control、human-in-the-loop、supervisor/worker 與可觀測流程的 coding team。",
                        "suitable_for": "較複雜的 repo、自動修 bug、需要 rollback/retry/human approval 的團隊流程。",
                        "strengths": ["stateful graph", "supervisor and handoff patterns", "durable execution", "large ecosystem"],
                        "gaps": ["需要自己設計 A2A boundary", "安全 policy 與 artifact schema 需額外實作"],
                        "minimum_adoption": "用 LangGraph 建 planner->implementer->tester->reviewer graph，所有節點輸出 typed artifact。",
                        "supporting_source_ids": ["S-021", "S-026", "S-027", "S-028"],
                        "research_prompt": "用 LangGraph 實作 AI coding team graph，評估 artifact schema、checkpoint、retry 與 human approval。",
                    },
                    {
                        "rank": 2,
                        "tool": "OpenAI Agents SDK",
                        "recommendation_reason": "handoffs、guardrails、tracing 與 platform guide 對最小 PoC 很直接，適合快速驗證 role handoff 與 evidence tracing。",
                        "suitable_for": "想快速建立可追蹤 specialist agents，且可以接受 SDK 生態綁定的 PoC。",
                        "strengths": ["handoff primitive", "tracing", "guardrails", "clear agent abstraction"],
                        "gaps": ["跨 vendor/open-source runtime 邊界需要 adapter", "不是完整 A2A protocol implementation"],
                        "minimum_adoption": "用 agents + handoffs + tracing 建 planner/implementer/tester/reviewer 四角色。",
                        "supporting_source_ids": ["S-008", "S-009", "S-010", "S-019", "S-020"],
                        "research_prompt": "用 OpenAI Agents SDK 建 coding-team PoC，測量 handoff trace、guardrail 命中與 artifact completeness。",
                    },
                    {
                        "rank": 3,
                        "tool": "CrewAI or Pydantic AI",
                        "recommendation_reason": "CrewAI 適合 role/task crew 建模，Pydantic AI 適合輕量 typed Python agent；二者都適合快速驗證流程，但需補強 protocol/security layer。",
                        "suitable_for": "快速 demo、role-based crew、typed Python workflow、較小團隊或研究原型。",
                        "strengths": ["role/task modeling", "typed outputs with Pydantic AI", "low barrier to prototype"],
                        "gaps": ["durable execution與跨 runtime protocol需另補", "policy gate與benchmark harness需自建"],
                        "minimum_adoption": "建立 planner/engineer/tester/reviewer crew 或 typed handoff pipeline，輸出 standardized evidence JSON。",
                        "supporting_source_ids": ["S-029", "S-030", "S-031"],
                        "research_prompt": "比較 CrewAI 與 Pydantic AI 在 typed artifact、role delegation、test evidence 輸出上的工程成本。",
                    },
                ],
            },
            "multi_tool_recommendations": {
                "summary": "多工具組合的目標是分層，而不是堆工具：orchestrator 管流程，MCP 管工具，A2A 管外部邊界，policy 管風險。",
                "items": [
                    {
                        "rank": 1,
                        "title": "LangGraph + MCP tools + A2A-compatible TaskEnvelope + OPA/Conftest gate",
                        "tools": ["LangGraph", "MCP/tool adapters", "A2A JSON envelope", "OPA/Rego or Conftest", "SWE-bench-style harness"],
                        "objective": "建立最穩健、可審計、可重跑的 AI coding team。",
                        "roles": ["planner", "architect", "implementer", "tester", "reviewer", "security/policy"],
                        "workflow": "LangGraph 控制狀態與重試；工具透過 MCP adapter；跨團隊輸入輸出使用 A2A-like task/artifact；所有 risky action 先跑 policy。",
                        "recommendation_reason": "兼顧 durable orchestration、工具邊界、外部協議邊界與安全治理，是本報告首選。",
                        "tradeoffs": ["初始工程量較高", "需要定義內部 artifact schema"],
                        "minimum_deliverable": "一個 repo bugfix task 的端到端 run，包含 patch、test log、review、policy decision。",
                        "acceptance_criteria": ["trace complete", "policy decision complete", "artifact schema valid", "test reproducible"],
                        "supporting_source_ids": ["S-004", "S-006", "S-025", "S-028", "S-040", "S-041", "S-043"],
                        "research_prompt": "設計 LangGraph + MCP + A2A-compatible envelope 的端到端 PoC，加入 OPA/Rego policy 與 SWE-bench-style 評測。",
                    },
                    {
                        "rank": 2,
                        "title": "OpenAI Agents SDK + MCP + trace-first evidence store + security reviewer",
                        "tools": ["OpenAI Agents SDK", "MCP/tool adapters", "trace store", "security review agent", "policy checklist"],
                        "objective": "快速建立可觀測、可展示的 coding-team prototype。",
                        "roles": ["triage agent", "implementation agent", "test agent", "review agent", "security agent"],
                        "workflow": "Agents SDK handoff 負責角色轉移；trace 連接每次 tool use；MCP adapter 管 repo/query/test 工具；security reviewer 檢查 risky diffs。",
                        "recommendation_reason": "最容易快速落地，但長期跨 runtime interoperability 需補 A2A adapter。",
                        "tradeoffs": ["生態綁定較高", "A2A protocol coverage 需額外開發"],
                        "minimum_deliverable": "同一個 task 產生完整 trace 與 evidence bundle。",
                        "acceptance_criteria": ["handoff trace exists", "tool call trace exists", "test evidence exists", "review verdict exists"],
                        "supporting_source_ids": ["S-008", "S-009", "S-010", "S-019", "S-020", "S-040", "S-042"],
                        "research_prompt": "用 OpenAI Agents SDK 實作 trace-first coding team，將 evidence bundle 對映成 A2A artifact。",
                    },
                    {
                        "rank": 3,
                        "title": "A2A boundary + AGNTCY/ACP comparison + framework-internal crew",
                        "tools": ["A2A", "AGNTCY ACP", "CrewAI or Pydantic AI", "MCP", "policy gate"],
                        "objective": "探索跨 organization 或跨 runtime 的 agent marketplace/team communication。",
                        "roles": ["external requester", "coordinator", "specialist crew", "policy verifier", "result publisher"],
                        "workflow": "外部請求用 A2A/ACP-like protocol，內部 crew 完成工作，結果以 artifact + evidence 回傳。",
                        "recommendation_reason": "適合研究 protocol interoperability，但不建議作第一個工程落地版本。",
                        "tradeoffs": ["interop 不確定性最高", "需要更多 adapter", "benchmark 設計複雜"],
                        "minimum_deliverable": "一個 mock remote agent server/client 交換 task envelope 與 artifact evidence。",
                        "acceptance_criteria": ["agent card/descriptor exists", "task lifecycle modeled", "artifact returned", "policy decision attached"],
                        "supporting_source_ids": ["S-001", "S-006", "S-014", "S-015", "S-032"],
                        "research_prompt": "比較 A2A 與 AGNTCY ACP 在 remote coding-agent invocation、task lifecycle、artifact streaming 上的差異。",
                    },
                ],
            },
        },
        "future_directions": {
            "summary": "未來性重點在 benchmark、interop、security proof、artifact schema standardization，而不是單純增加 agent role。",
            "items": [
                {
                    "title": "A2A coding-team benchmark extension",
                    "current_limitation": "SWE-bench 不能直接衡量 handoff correctness 與 artifact completeness。",
                    "direction": "建立 SWE-bench plus communication metrics：handoff correctness、artifact completeness、defect/security catch rate、latency/cost、human intervention。",
                    "trigger": "當 PoC 可以穩定跑 10 個以上 repo tasks 後開始。",
                    "supporting_source_ids": ["S-024", "S-025", "S-035", "S-037", "S-039"],
                    "research_prompt": "設計 SWE-bench plus multi-agent communication benchmark，定義可自動評分的 handoff/artifact/security metrics。",
                },
                {
                    "title": "Skill supply-chain and permission model",
                    "current_limitation": "技能層缺少統一簽章、版本、權限與測試標準。",
                    "direction": "建立 skill manifest、permission scope、policy tests、hash pinning、review workflow。",
                    "trigger": "當團隊開始複用自訂 agent skills 或 marketplace skills。",
                    "supporting_source_ids": ["S-041", "S-042", "S-044", "S-045"],
                    "research_prompt": "研究 agent skill security manifest 與 OPA/Rego policy model，涵蓋 shell、network、file、credential 權限。",
                },
                {
                    "title": "Protocol interoperability adapter",
                    "current_limitation": "A2A、ACP、ANP、AG-UI 還沒有單一穩定主導方案。",
                    "direction": "把內部 artifact contract 與外部 protocol adapter 分離，避免被某一個 protocol 變動拖住。",
                    "trigger": "當需要跨 vendor/跨 team agent 溝通。",
                    "supporting_source_ids": ["S-001", "S-006", "S-014", "S-016", "S-017", "S-022", "S-023", "S-032"],
                    "research_prompt": "建立 A2A/ACP adapter abstraction，驗證同一個 TaskEnvelope 是否可映射到不同 protocol。",
                },
            ],
        },
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_catalog(sources: list[dict[str, Any]]) -> None:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in sources:
        category = source.get("quality", {}).get("category", "Uncategorized")
        grouped[category].append(source)

    lines = [
        "# A2A Agent Communication Sources Catalog",
        "",
        f"Updated: {GENERATED_AT}",
        "",
        "This catalog maps `S-001` to `S-045` to their role in the A2A Agent communication / AI Coding team research. Raw snapshots stay under each source folder and are ignored by Git when archived separately.",
        "",
        "## Overview",
        "",
        "| Source | Category | Evidence tier | Title | Role in research |",
        "| --- | --- | --- | --- | --- |",
    ]
    for source in sources:
        source_id = source["source_id"]
        overview = SOURCE_OVERVIEWS.get(source_id, {})
        lines.append(
            f"| `{source_id}` | {overview.get('category', 'Uncategorized')} | {source.get('evidence_tier', '')} | [{source.get('title', source_id)}]({source.get('canonical_url') or source.get('url')}) | {overview.get('summary', '')} |"
        )

    lines.extend(["", "## Category Index", ""])
    for category in sorted(grouped):
        ids = ", ".join(f"`{item['source_id']}`" for item in grouped[category])
        lines.append(f"- **{category}**: {ids}")

    lines.append("")
    (SOURCES_DIR / "CATALOG.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def markdown_report(report: dict[str, Any]) -> str:
    lines: list[str] = [
        f"# {report['title']}",
        "",
        f"- Report ID: `{report['report_id']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Data cutoff: `{report['data_cutoff']}`",
        f"- Sources: `{len(report['sources'])}`",
        f"- Quality score: `{report['quality_score']}` / Structural score: `{report['structural_score']}`",
        "",
        "## Executive Summary",
        "",
    ]
    for item in report["executive_summary"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Key Findings", ""])
    for claim in report["claims"]:
        refs = ", ".join(f"`{sid}`" for sid in claim["supporting_source_ids"])
        lines.append(f"### {claim['claim_id']}. {claim['statement']}")
        lines.append("")
        lines.append(f"- Confidence: `{claim['confidence']}`")
        lines.append(f"- Evidence: {refs}")
        lines.append(f"- Reasoning: {claim['reasoning']}")
        lines.append("")

    lines.extend(
        [
            "## Recommended Architecture",
            "",
            "```mermaid",
            "flowchart LR",
            '  R["Requirement / Issue"] --> P["Planner"]',
            '  P --> A["Architect (optional)"]',
            '  A --> I["Implementer"]',
            '  P --> I',
            '  I --> T["Tester"]',
            '  T --> RV["Reviewer"]',
            '  RV --> S["Security / Policy Gate"]',
            '  S --> O["Evidence Bundle + Patch Artifact"]',
            '  Tool["MCP / Tool Adapter"] <--> P',
            '  Tool <--> I',
            '  Tool <--> T',
            '  Ext["A2A-compatible Task / Artifact Boundary"] <--> P',
            '  Ext <--> O',
            "```",
            "",
            "The core rule: keep internal team orchestration inside a framework graph or handoff runtime; expose cross-runtime work as an A2A-compatible task and artifact contract; place MCP/tool access behind policy and trace boundaries.",
            "",
            "## Minimal Communication Contract",
            "",
            "```json",
            json.dumps(
                {
                    "task_id": "TASK-001",
                    "requirement_refs": ["REQ-001", "REQ-002"],
                    "role": "implementer",
                    "input_artifacts": [{"type": "requirements", "path": "docs/spec.md", "hash": "sha256:..."}],
                    "output_artifacts": [{"type": "patch", "path": "changes.diff", "hash": "sha256:..."}],
                    "evidence": [{"type": "test", "command": "pytest", "result": "pass", "log_hash": "sha256:..."}],
                    "trace_id": "TRACE-001",
                    "policy_decision": {"status": "allow", "rules": ["no-secret-write", "safe-shell"]},
                },
                ensure_ascii=False,
                indent=2,
            ),
            "```",
            "",
            "## Recommendations",
            "",
            "### Implementability",
            "",
        ]
    )
    impl = report["recommendation_sections"]["implementability"]["items"][0]
    lines.extend(
        [
            f"**{impl['title']}**",
            "",
            f"- Objective: {impl['objective']}",
            f"- Technologies: {', '.join(impl['technologies'])}",
            f"- Minimum deliverable: {impl['minimum_deliverable']}",
            f"- Evidence: {', '.join(f'`{sid}`' for sid in impl['supporting_source_ids'])}",
            "",
            "### If Only One Open-Source Tool Is Used",
            "",
            "| Rank | Tool | Why | Main gap |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in report["recommendation_sections"]["open_source_options"]["single_tool_recommendations"]["items"]:
        lines.append(f"| {item['rank']} | {item['tool']} | {item['recommendation_reason']} | {'; '.join(item['gaps'])} |")

    lines.extend(["", "### If Multiple Open-Source Tools Are Combined", "", "| Rank | Stack | Why | Tradeoffs |", "| --- | --- | --- | --- |"])
    for item in report["recommendation_sections"]["open_source_options"]["multi_tool_recommendations"]["items"]:
        lines.append(f"| {item['rank']} | {item['title']} | {item['recommendation_reason']} | {'; '.join(item['tradeoffs'])} |")

    lines.extend(["", "### Future Directions", ""])
    for item in report["recommendation_sections"]["future_directions"]["items"]:
        lines.append(f"- **{item['title']}**: {item['direction']} Trigger: {item['trigger']}")

    lines.extend(["", "## Conflicts And Unknowns", ""])
    for item in report["resolution_matrix"]["conflict_resolutions"]:
        lines.append(f"- `{item['resolution_id']}` ({item['status']}): {item['resolution']}")
    for item in report["resolution_matrix"]["unknown_resolutions"]:
        lines.append(f"- `{item['resolution_id']}` ({item['status']}): {item['resolution']}")

    lines.extend(["", "## Source Width", ""])
    lines.append("The report uses the following source groups:")
    categories: dict[str, int] = defaultdict(int)
    for source in report["sources"]:
        categories[source.get("quality", {}).get("category", "Uncategorized")] += 1
    for category, count in sorted(categories.items()):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "For the full source list and summaries, see `sources/CATALOG.md`.", "", "## Limitations", ""])
    for item in report["limitations"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Conclusion", "", report["conclusion"], ""])
    return "\n".join(lines)


def write_research_notes() -> None:
    notes = f"""# A2A Agent Communication / AI Coding Team Research Notes

Updated: {GENERATED_AT}

## Completed

- Created the topic workspace and crawl queue.
- Collected 45 sources (`S-001` to `S-045`) covering A2A, MCP, ACP, ANP, AG-UI, framework handoff, coding-team research, benchmarks, security, and governance.
- Captured both Anthropic variants available to the collector (`S-033`, `S-034`) and use them only for workflow/agent architecture claims.
- Generated `sources/CATALOG.md` so every source has a category and short role summary.
- Generated a structured JSON report and a readable Markdown report.
- Synchronized `supported_claim_ids` in every `source.json` from the claim-evidence matrix.

## Remaining Optional Follow-Up

- Run an actual PoC benchmark with one shared coding task across LangGraph, OpenAI Agents SDK, and CrewAI/Pydantic AI.
- Refresh rapidly changing protocol sources before implementation starts, especially A2A, AGNTCY ACP, and framework docs.
- Add an executable policy-gate experiment for tool/skill permission control.

## Report Files

- `reports/a2a-agent-communication-ai-coding-team-20260607-v1.json`
- `reports/a2a-agent-communication-ai-coding-team-20260607-v1.md`
- `sources/CATALOG.md`
"""
    (TOPIC_DIR / "RESEARCH-NOTES.md").write_text(notes, encoding="utf-8", newline="\n")


def update_crawl_queue() -> None:
    path = TOPIC_DIR / "crawl-queue.json"
    with path.open("r", encoding="utf-8") as handle:
        queue = json.load(handle)

    updates: dict[str, dict[str, Any]] = {
        "Q-022": {"status": "completed", "result_source_ids": ["S-030", "S-031"], "notes": "Resolved by direct CrewAI official docs."},
        "Q-023": {"status": "completed", "result_source_ids": ["S-029"], "notes": "Resolved by Pydantic AI official multi-agent guide."},
        "Q-024": {"status": "completed", "result_source_ids": ["S-032"], "notes": "Resolved by AGNTCY ACP OpenAPI specification."},
        "Q-025": {"status": "completed", "result_source_ids": ["S-033", "S-034"], "notes": "Resolved by Anthropic effective agents pages."},
        "Q-026": {"status": "completed", "result_source_ids": ["S-040", "S-042"], "notes": "Resolved by OWASP MCP Top 10 and OWASP LLM Top 10."},
        "Q-027": {"status": "completed", "result_source_ids": ["S-006", "S-018"], "notes": "Resolved by A2A specification and latest docs."},
        "Q-029": {"status": "completed", "result_source_ids": ["S-035", "S-036"], "notes": "Resolved by ChatDev paper and repository."},
        "Q-030": {"status": "completed", "result_source_ids": ["S-037", "S-038"], "notes": "Resolved by MetaGPT paper and repository."},
        "Q-031": {"status": "completed", "result_source_ids": ["S-039"], "notes": "Resolved by AgentCoder paper."},
        "Q-034": {"status": "completed", "result_source_ids": ["S-024", "S-025", "S-035", "S-037", "S-039"], "notes": "Resolved with SWE-bench baseline plus coding-team research papers."},
        "Q-035": {"status": "completed", "result_source_ids": ["S-021", "S-036", "S-038"], "notes": "Resolved with LangGraph supervisor, ChatDev, and MetaGPT implementations."},
        "Q-036": {"status": "completed", "result_source_ids": ["S-010", "S-028"], "notes": "Resolved with tracing and durable graph execution sources."},
        "Q-037": {"status": "completed", "result_source_ids": ["S-040", "S-041", "S-042", "S-044", "S-045"], "notes": "Resolved with OWASP and prompt-injection research."},
        "Q-038": {"status": "completed", "result_source_ids": ["S-043"], "notes": "Resolved with NIST AI RMF."},
        "Q-039": {"status": "completed", "result_source_ids": [], "notes": "Resolved in report Minimal Communication Contract section."},
        "Q-040": {"status": "completed", "result_source_ids": [], "notes": "Resolved in report Recommended Architecture and resolution matrix."},
        "Q-048": {"status": "skipped", "result_source_ids": [], "notes": "AGNTCY details were covered by Q-049 / S-032; this docs page remains optional for a future refresh."},
    }
    for item in queue["items"]:
        update = updates.get(item["queue_id"])
        if update:
            item.update(update)
    queue["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(path, queue)

    md_lines = [
        "# Crawl Queue",
        "",
        f"Updated: {GENERATED_AT}",
        "",
        "| Seq | Queue ID | Type | Target | Related questions | Step | Status | Result sources | Reason / notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in queue["items"]:
        questions = ", ".join(item.get("related_question_ids", []))
        results = ", ".join(f"`{sid}`" for sid in item.get("result_source_ids", []))
        reason = item.get("notes") or item.get("reason", "")
        target = str(item.get("target", "")).replace("|", "\\|")
        reason = reason.replace("|", "\\|")
        md_lines.append(
            f"| {item['sequence']} | `{item['queue_id']}` | `{item['target_type']}` | `{target}` | {questions} | `{item['added_by_step']}` | `{item['status']}` | {results} | {reason} |"
        )
    (TOPIC_DIR / "crawl-queue.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    update_crawl_queue()
    backlinks = build_backlinks()
    update_source_files(backlinks)
    sources = load_sources()
    report = build_report(sources)
    report_path = REPORTS_DIR / f"{report['report_id']}.json"
    md_path = REPORTS_DIR / f"{report['report_id']}.md"
    write_json(report_path, report)
    md_path.write_text(markdown_report(report), encoding="utf-8", newline="\n")
    write_catalog(sources)
    write_research_notes()
    print(f"Wrote {report_path}")
    print(f"Wrote {md_path}")
    print(f"Wrote {SOURCES_DIR / 'CATALOG.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
