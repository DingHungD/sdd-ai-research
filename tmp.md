agent-template/
├─ AGENTS.md                       # Agent 的長期行為規範與工作流程說明
├─ package.json                    # Node.js 專案依賴與執行腳本設定
├─ tsconfig.json                   # TypeScript 編譯設定
├─ Dockerfile                      # 建立 Agent Container 映像檔
├─ docker-compose.yml              # 本地開發與多服務啟動配置
├─ .env.example                    # 環境變數範本
├─ README.md                       # 專案說明與使用文件
│
├─ skills/                         # Agent 可載入的任務技能與專項 SOP
│  ├─ XXX/
│  │  ├─ SKILL.md                  # XXX標準流程
│  │  └─ policy.json               # XXX權限與工具限制
│
├─ src/
│  ├─ main.ts                      # Agent 系統啟動入口
│  │
│  ├─ config/
│  │  ├─ env.ts                    # 載入與驗證環境變數
│  │  ├─ agent.config.ts           # Agent 身份與能力設定
│  │  └─ remote-agents.config.ts   # 遠端 Agent 清單與連線設定
│  │
│  ├─ a2a/
│  │  ├─ server.ts                 # A2A Server 啟動與管理
│  │  ├─ client.ts                 # A2A Client 呼叫其他 Agent
│  │  ├─ card.ts                   # 建立與發布 Agent Card
│  │  ├─ routes.ts                 # A2A API 路由定義
│  │  ├─ task-adapter.ts           # A2A Task 與 Runtime 之間的轉換器
│  │  ├─ task-store.ts             # A2A 協定層 Task 狀態儲存
│  │  └─ types.ts                  # A2A 相關型別定義
│  │
│  ├─ mcp/
│  │  ├─ client.ts                 # MCP Server 連線管理
│  │  ├─ registry.ts               # MCP Server 與 Tool 註冊中心
│  │  ├─ tool-loader.ts            # 載入 MCP Tools 並轉換為 Agent Tools
│  │  └─ types.ts                  # MCP 相關型別定義
│  │
│  ├─ agent/
│  │  ├─ runtime.ts                # OpenAI Agent Runtime 執行核心
│  │  ├─ instructions.ts           # 載入與組合 Agent Instructions
│  │  ├─ tools.ts                  # Agent 可使用的工具定義
│  │  ├─ session.ts                # Agent Session 與短期記憶管理
│  │  ├─ guardrails.ts             # Agent 安全規則與限制條件
│  │  └─ handoffs.ts               # Agent 任務轉交與協作策略
│  │
│  ├─ skills/
│  │  ├─ loader.ts                 # 從 skills/ 目錄載入 Skill 文件
│  │  ├─ registry.ts               # 建立 Skill 清單與 metadata
│  │  ├─ matcher.ts                # 根據任務語意匹配 Skill
│  │  └─ types.ts                  # Skill 相關型別定義
│  │
│  ├─ workflow/
│  │  ├─ taskdb.client.ts          # TaskDB API 存取封裝
│  │  ├─ state-machine.ts          # 任務生命週期與狀態轉換管理
│  │  ├─ artifact.service.ts       # 任務產出物管理服務
│  │  └─ types.ts                  # Workflow 相關型別定義
│  │
│  ├─ infra/
│  │  ├─ http.ts                   # HTTP Server 與 Middleware 初始化
│  │  ├─ logger.ts                 # 系統日誌與追蹤管理
│  │  ├─ auth.ts                   # 驗證與授權機制
│  │  ├─ health.ts                 # Health Check 與存活監控
│  │  └─ errors.ts                 # 統一錯誤處理與例外管理
│  │
│  └─ shared/
│     ├─ ids.ts                    # ID 生成與格式工具
│     ├─ result.ts                 # 統一回傳結果格式
│     └─ json.ts                   # JSON 處理與序列化工具
│
├─ tests/
│  ├─ a2a/                         # A2A 模組測試
│  ├─ mcp/                         # MCP 模組測試
│  └─ agent/                       # Agent Runtime 測試
│
└─ scripts/
   ├─ dev.ts                       # 本地開發輔助腳本
   └─ smoke-test.ts                # 系統啟動後的快速驗證測試
