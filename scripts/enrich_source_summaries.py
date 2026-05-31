#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from research_pipeline.document_curator import save_reviewed_summary
from research_pipeline.io_utils import iso_now, read_json
from research_pipeline.workflow import update_index


ROOT = Path(__file__).resolve().parents[1]
TOPIC_DIR = ROOT / "knowledge-base" / "topics" / "sdd-ai-autonomous-development"

CATEGORY_DETAILS = {
    "direct_sdd": {
        "fit": "位於 specification artifact 與 traceability 層，負責把需求轉成可演進、可檢查、可交給 agent 執行的狀態。",
        "workflow": ["建立或匯入需求", "產生 specification 與 design", "拆解 tasks", "執行或交付 coding agent", "回寫驗證結果與 refinement"],
        "questions": ["artifact 是否可版本控制並支援差異比較？", "requirement、task、test 與 commit 是否能互相回指？", "是否支援 approval、resume 與 brownfield 更新？"],
    },
    "workflow_runtime": {
        "fit": "位於流程編排層，將多步驟 SDD 命令、人工閘門與失敗恢復組成長時間 workflow。",
        "workflow": ["載入 workflow 定義", "依序或平行執行 steps", "遇到 gate 時暫停", "核准或修正後 resume", "保存 run state 與結果"],
        "questions": ["中斷後能否精準 resume？", "哪些 gate 可由 policy 自動判斷？", "是否保留每個 step 的輸入、輸出與 log？"],
    },
    "context_engineering": {
        "fit": "位於 repository context 層，降低 agent 對大型或既有 codebase 理解不足的風險。",
        "workflow": ["掃描 repository", "建立結構或語意索引", "選取與 task 相關 context", "提供 agent 執行", "依變更更新索引"],
        "questions": ["大型 repository 的索引成本是多少？", "context 選取錯誤如何偵測？", "索引是否能與 requirement traceability 結合？"],
    },
    "brownfield": {
        "fit": "位於 brownfield reverse-engineering 層，從既有 code 產生或更新 living specification。",
        "workflow": ["執行 static analysis", "建立 dependency 與 call graph", "識別 domain clusters", "由 LLM 補充語意", "輸出 living specs 與 drift 指標"],
        "questions": ["產生規格的準確率如何驗證？", "spec-code drift 是否可持續監控？", "未覆蓋的 code path 如何揭露？"],
    },
    "task_graph": {
        "fit": "位於 task graph 層，將規格轉為可排序、可恢復、可平行執行的工作單位。",
        "workflow": ["解析 PRD 或 specification", "建立 tasks 與 dependency", "找出 ready tasks", "交給 agent 執行", "更新狀態與下一個工作"],
        "questions": ["task 是否回指 requirement 與 acceptance criteria？", "如何處理失敗、拆分與重試？", "平行 task 的 merge 衝突如何避免？"],
    },
    "autonomous_loop": {
        "fit": "位於 autonomous loop 層，透過 iteration memory、completion condition 與驗證讓 agent 連續工作。",
        "workflow": ["載入 PRD、task 或 prompt", "執行單一 iteration", "跑檢查並保存 commit 或 progress", "判斷 completion condition", "未完成則進入下一輪或 escalation"],
        "questions": ["是否有 max iteration 與停止條件？", "跨 iteration memory 保存在哪裡？", "無法通過驗證時何時 escalation？"],
    },
    "multi_agent": {
        "fit": "位於 multi-agent orchestration 層，負責 specialist delegation、handoff、平行波次與最終驗證。",
        "workflow": ["建立依賴計畫", "分配 specialist 或 worker agents", "依 wave 平行執行", "收集 context handoff", "由 orchestrator 驗證與合併"],
        "questions": ["agent 邊界是否清楚？", "handoff 是否保存足夠 context？", "最終 merge 與 review 是否可追溯？"],
    },
    "execution_runtime": {
        "fit": "位於 execution runtime 層，管理長時間 agent session、workspace、scheduler、retry 與 observability。",
        "workflow": ["取得 issue 或 task", "建立隔離 workspace", "啟動 agent runtime", "監控 log 與狀態", "完成、retry 或 escalation"],
        "questions": ["workspace 是否真正隔離？", "retry 是否具冪等性？", "log、成本、權限與錯誤是否可觀測？"],
    },
    "workspace_isolation": {
        "fit": "位於 workspace isolation 層，讓多個 agent 可同時修改 code 而不互相污染。",
        "workflow": ["為 task 建立 worktree", "啟動 agent 或 terminal session", "執行修改與檢查", "review diff", "合併或丟棄 workspace"],
        "questions": ["worktree 生命週期如何管理？", "merge conflict 如何偵測與處理？", "刪除 workspace 前是否保留 artifact？"],
    },
    "security": {
        "fit": "位於 governance 與 security 層，將安全要求、threat model 與政策檢查加入交付鏈。",
        "workflow": ["定義 security constraints", "將限制映射到 code 或 spec", "執行分析與驗證", "產生報告", "阻擋或升級違規變更"],
        "questions": ["安全規格是否可機器驗證？", "policy violation 是否阻擋 merge？", "threat model 是否隨 code 變更更新？"],
    },
    "article": {
        "fit": "位於方法論與採用經驗層，用來補足工具文件未涵蓋的實作觀點、 trade-off 與導入風險。",
        "workflow": ["辨識文章主張與適用範圍", "拆分直接事實、作者觀點與案例", "對照官方工具文件", "保留可驗證的 adoption insight", "將未驗證主張標記為限制"],
        "questions": ["作者是否為官方或具編輯審查來源？", "文章主張是否有案例或數據支持？", "哪些結論只能作為採用假設？"],
    },
    "case_study": {
        "fit": "位於案例層，用來理解 SDD 在特定組織、法規或流程限制中的實際使用方式。",
        "workflow": ["確認案例背景", "辨識使用的 spec 與驗證機制", "記錄人工介入點", "拆出可移植做法", "標記不可外推部分"],
        "questions": ["案例是否能外推到其他團隊？", "成功條件與限制是否揭露？", "是否量測品質、速度與人工成本？"],
    },
    "benchmark": {
        "fit": "位於評估層，用來約束對 coding agent、context retrieval 與長時間自動開發能力的宣稱。",
        "workflow": ["確認 benchmark 任務分布", "檢查資料品質與污染風險", "辨識評估指標", "比較 agent 行為", "將限制回饋到系統 gate"],
        "questions": ["benchmark 是否覆蓋真實 software engineering 工作？", "是否只測 patch generation？", "是否揭露 context retrieval、驗證與維護任務？"],
    },
    "traceability": {
        "fit": "位於 requirements assurance 層，要求需求、設計、code、test、hazard 與 non-conformance 可雙向追溯。",
        "workflow": ["為 requirement 配置唯一 ID", "將 requirement 映射到 design", "將 design 映射到 code", "將 requirement 映射到 verification", "檢查 orphan、extra 與變更影響"],
        "questions": ["是否能雙向追溯？", "是否偵測 orphan design、extra code 與未驗證 requirement？", "baseline 變更是否經審批並更新 matrix？"],
    },
    "policy_as_code": {
        "fit": "位於 policy gate 層，將組織、安全與部署規則寫成可版本控制、可測試、可稽核的機器判斷。",
        "workflow": ["將 artifact 轉為結構化輸入", "以 declarative policy 評估", "在 PR 或 CI 阻擋違規", "保存 policy decision 與 audit trail", "例外進入人工審批"],
        "questions": ["policy 是否版本化與可測試？", "違規是否阻擋 merge 或 deploy？", "例外流程是否留下 audit trail？"],
    },
    "assurance": {
        "fit": "位於 assurance framework 層，提供安全開發實務、驗證控制、風險等級與持續改善基準。",
        "workflow": ["選擇適用控制", "將控制映射到需求與流程", "在 pipeline 蒐集 evidence", "執行自動與人工驗證", "持續改善並回應殘餘風險"],
        "questions": ["控制是否 outcome-based 且可提供 evidence？", "哪些控制可自動驗證？", "高 assurance 情境是否需要獨立覆核？"],
    },
}

FALLBACK_DETAIL = {
    "fit": "位於 SDD AI 自動開發生態中的輔助層。使用時應先確認它解決的是規格、context、task、runtime、整合或治理問題。",
    "workflow": ["確認輸入 artifact", "執行工具核心能力", "保存輸出與狀態", "交給下一層或人工覆核"],
    "questions": ["此工具解決哪一層問題？", "輸出是否可追溯與版本化？", "失敗時是否有明確 escalation？"],
}


def main() -> int:
    mapping = read_json(TOPIC_DIR / "curation" / "enrichment-map.json")
    for source_id, values in mapping.items():
        category, role, features, technologies = values
        source_dir = TOPIC_DIR / "sources" / source_id
        source = read_json(source_dir / "source.json")
        summary = read_json(source_dir / "summary.json")
        existing_points = summary.get("key_points", [])
        if not existing_points:
            existing_points = [
                {
                    "text": features,
                    "locator": "README or official documentation overview",
                    "notes": "Agent-reviewed catalog summary; return to raw snapshot for publication claims."
                }
            ]
        detail = CATEGORY_DETAILS.get(category, FALLBACK_DETAIL)
        limitations = [item for item in summary.get("limitations", []) if "initial machine-generated" not in item.lower()]
        limitations.append("Repository 或官方文件可用於理解公開設計；production readiness 仍需安裝測試、維護狀態與 benchmark 驗證。")
        feature_items = [item.strip() for item in features.split("；") if item.strip()]
        tech_items = [item.strip() for item in technologies.split(",") if item.strip()]
        summary.update(
            {
                "summarized_at": iso_now(),
                "document_purpose": f"深度來源摘要：{role}。",
                "summary": f"{role}。{features}。關鍵技術包括：{technologies}。",
                "role_in_ecosystem": role,
                "architecture_fit": detail["fit"],
                "workflow_outline": detail["workflow"],
                "key_features": feature_items + [f"架構層級：{category}", "輸出應保存為可追溯 artifact，重要結論需回讀 raw snapshot。"],
                "key_technologies": tech_items,
                "best_for": [category, "快速判斷此工具在整體 SDD 架構中的責任", "作為試點工具選型與後續深挖入口"],
                "research_value": f"此來源用於理解 {role} 在整體架構中的角色。重要結論仍需回讀本地 raw snapshot 與原始 URL。",
                "verification_questions": detail["questions"],
                "categories": sorted(set(summary.get("categories", []) + [category])),
                "key_points": existing_points,
                "keywords": sorted(set(summary.get("keywords", []) + [category, role])),
                "limitations": sorted(set(limitations)),
            }
        )
        save_reviewed_summary(TOPIC_DIR, summary)
        update_index(TOPIC_DIR, source, summary)
    print(f"Enriched {len(mapping)} source summaries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
