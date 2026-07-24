# 用 coding agent 造一个 agent — 完整操作框架(S2–S5 + 横切)

> 状态:**已过完整性闭环**(2026-06-17;33-agent 完整性 workflow 找缺口→补→复审,4 个残口单独补齐;本稿按复审方案合成、去重、标注对齐)。
> 对象:个人开发者用 **Claude Code(主)/ Codex(次)** 从头造一个 AI agent 应用,每个节点钻到「照着能做」的操作底。
> 锚:`../flow.md` S2(设计零件)+S3(实现)+S4(eval)+S5(上线)+横切。S0/S1 见 `S0-*.md`、`S1-*.md`。
> **标注纪律**:〔源〕=有一手出处(官方文档/署名实践者);【推断】=据已有材料合理推断、**无单一权威源**;⚠️=坑/弃用。证据偏 Anthropic 官方文档(2025-2026),跨厂商处标明。

---

## 0. 非专家 30 秒导航(先看这个,别被下面全量淹没)

**最小主干(SOLO 跑通一个 agent 的必经 6 步)**:
`①写 AGENTS.md 规矩 → ④造零件(工具+prompt+loop+护栏) → ⑤建个最小 eval → ⑦挂个 hook 跑测试 → ⑨迭代到绿 → ⑩发`。

**day-0 绝不可省(solo 也是)**:
- 🔴 **成本/递归/墙钟硬上限**(写进代码,不是 prompt)——见 NODE4c、横切。不设=可能像那个案例烧 $4,200/63h。
- 🔴 **evaluator 与 agent 隔离**——eval 不能让 agent 自己跑自己判(会刷分)。见 NODE6。

**SOLO 可降级(别上重的)**:
- 正式 eval 套件 → 降级为 **tracing + 人工抽检 + 3-5 个真实失败 case**(NODE5)。
- 框架/多 agent/MCP server → 默认不上,手写 loop + 短链(见 `S1-*.md`)。

**必读 vs 可选**:必读 = NODE0、4a、4c、5、6、7;其余按需。

---

## 全流程图

```
①立上下文/规矩 → ②最新知识注入 → ③探索 → ④规划
  → ⑤造零件[工具·prompt·loop+停止·上下文/记忆·护栏]
  → ⑥验证=eval(非单测) → ⑦确定性闸门(hook) → ⑧对抗review
  → ⑨迭代回灌 → ⑩commit/上线
横切:知识保鲜(②) · day-0硬护栏(成本/递归上限+evaluator隔离) · 运行时ReAct循环
```

每个节点统一结构:**放哪 / 命令·配置 / 最小骨架 / 验收(怎么算这步做完)/ 坑**。

---

## NODE0 立上下文 / 规矩(把 coding agent 该遵守的写下来)

- **放哪**:repo 根 `AGENTS.md`(跨工具)或 `CLAUDE.md`(Claude Code);**按文件生效**的质量规则放 `.claude/rules/*.md`,frontmatter 写 `paths`。〔源:code.claude.com/docs/en/memory〕
- **命令·配置**:加规则用 `/memory` 或直接编辑文件(**⚠️ 无 `#` 快捷键**);每文件 **<200 行**;`@import` 最多 **4 跳**。〔源〕
- **最小骨架**(`.claude/rules/tools.md`):
  ```markdown
  ---
  paths: ["src/tools/**/*.ts"]
  ---
  # 工具开发规则
  - 命名:动词_名词 + 服务前缀(order_get_detail)
  - schema:additionalProperties:false,enum 锁值,required 明确
  - 返回:只返高信号(name/status),不返 uuid/mime_type
  - 错误:可操作文案,不返 traceback
  - 每个工具:示例调用 + 边界 + 单测
  ```
  〔骨架格式来自 memory 文档的 paths 示例;规则内容来自 NODE4a 工具craft〕
- **验收**:`/memory` 能列出该规则已加载;编辑工具文件时它生效。
- **坑**:⚠️ 规则是**建议**,模型会飘——真正的强制靠 NODE7 的 hook,别指望写进 CLAUDE.md 就万事大吉。⚠️ 文件超 200 行,规则会被淹没失效。〔源〕

---

## NODE1 最新知识注入(模型没有最新 API/文档 → 把当前信息喂进去)

> 这是横切「知识保鲜」。**核心澄清**:Context7 这类是**运行时查**(不落地),和「下载成本地文件」是两条不同的路。

| 做法 | 放哪 | 命令·配置 | 原文/提炼 | 时效 | 何时用 |
|---|---|---|---|---|---|
| **官方 docs-MCP**(优先) | MCP 配置,运行时查 | `claude mcp add` 厂商官方(如 Stripe) | 提炼(厂商供) | 同日 | 有官方 MCP 的复杂 API |
| **Context7** | 同上 | `npx ctx7 setup --claude` | 提炼 | 索引滞后几天 | 库文档,无官方 MCP ⚠️ |
| **按需 web** | 不存 | Claude Code 自带 WebFetch/WebSearch(`web_search_20260209`) | 原文 | 实时 | 临时查、无 MCP 〔源〕 |
| **本地下载文档** | `./docs/vendor/<名>-<日期>.md` | `curl ... > file && git add` | 都行,提炼优 | 手动刷 | 离线/可审计/常引用 |
| **提炼进规则** | `CLAUDE.md`/`.claude/rules` | 手写关键事实 | 提炼(~200tok) | 手更新 | 会话级常量(模型清单/价格) |
| **做成 Skill** | `.claude/skills/<n>/SKILL.md` | 见 NODE-范例B | 提炼+示例 | 手更新 | 跨 3+ 项目复用的「怎么用 X」 |

- **⚠️ Codex 坑**:`web_search` 默认 `cached` = **可能给过时文档**,设 `live`(或 `--search`)。〔源:codex/config-basic〕
- **⚠️ 安全**:Context7 出过 ContextCrush 事故(Noma 发现,2026-02-23 已修)→ **有官方 docs-MCP 优先官方**。〔源:Noma Security〕
- **【推断】SOLO 默认**:先用 Claude Code 自带 WebFetch(实时零配置);**反复踩「写了过时 API」的坑、且某库文档量大,才接一个 docs-MCP**。一上来就接 Context7 非必需,还多供应链风险。(无「live-MCP vs 本地文件」主流采用硬数据)
- **⚠️ llms.txt**:采用率仅 ~10%、主流平台不解析——只当「给 agent 本地读」用,别指望它做发现性。〔源:SE Ranking 300k 域研究〕

---

## NODE2 探索(Explore,只读)

- **放哪**:无产物落地,产出是**一份口头/写下的理解**。
- **命令·配置**:`claude --permission-mode plan` 或 `Shift+Tab` 进 plan mode(只读)。〔源:best-practices〕
- **最小骨架**(照着敲的探索 prompt):
  ```
  读 /src/agent,讲清这个 agent 的 loop 和工具怎么接的,先别改任何东西
  ```
  ```
  找到处理鉴权的文件,从前端到 DB 追一遍登录流程,有没有现成 OAuth 工具可复用
  ```
  〔源:best-practices / common-workflows 逐字模式〕
- **造 agent 时具体读什么**【推断,据 best-practices "follow the pattern" 推】:① system prompt/agent 配置 → ② 主 loop → ③ 工具定义 → ④ 类似的现有 agent(当范本)→ ⑤ env/secrets 配置 → ⑥ 测试文件(看验证套路)。
- **验收(探够了 = 全勾)**:□ 能一句话说清这 agent 干嘛 □ 能点名要改/要读哪些文件 □ 知道 loop 怎么停、有哪些工具 □ 找到了可参照的现有实现 □ 知道怎么测。〔源:best-practices "name the files and interfaces"〕
- **坑**:⚠️ Codex **没有**对应的 explore/plan 阶段——是代码生成型工具;Codex 用户得靠 spec 文件 + prompt 自己分离探索与实现(见末尾映射表)。〔源:codex 文档无该阶段〕

---

## NODE3 规划(Plan,人审)

- **放哪**:计划文本(plan mode 内可编辑);solo 可只口头+一页 outline。
- **命令·配置**:让它出实现计划 → `Ctrl+G` 开编辑器改计划 → 退出 plan mode 才放它写。**一句话能描述的小改跳过 plan**。〔源:best-practices "if you could describe the diff in one sentence, skip the plan"〕
- **零件依赖序**【部分验证 + 推断】:**设计阶段并行**(工具契约/eval 骨架/system prompt/编排 可同时设计),**集成有顺序**:① 工具定义+schema 过沙箱 → ② eval case 能独立判 pass/fail → ③ prompt+工具联测 → ④ 护栏集成(恶意输入被拦、循环有硬 limit)。
  - ⚠️ **标注对齐**:`flow.md`/d2 把这条标「综合推断,非单一权威源」。完整性 workflow 从 4 份 Anthropic 文档交叉佐证了**矢向**(工具→prompt→编排→护栏→eval),但「唯一正确次序」仍无单一权威源 → 保留 **部分未确认**;修正:不是「严格线性」,是「设计并行 + 集成有序」。
- **Plan→Human 交接清单**(solo 也建议把 day-0 数值在这步定死)〔源:best-practices + hooks〕:
  ```
  □ 每个验收场景都有走通路径;异常路径(timeout/invalid/quota)有处理
  □ 外部依赖列表 + 假设
  □ day-0 护栏填数值(非"适当"):成本上限 $__ / 墙钟 __min / token __ / 递归 __ / 每工具重试 __
  □ 此 agent 可改的文件/表(deny 什么)、与现有系统边界(会不会死循环)
  □ 所有 task ≤ Small/Med(Large 必拆),已排依赖
  ```
- **验收**:计划具体到能照着写、每个列的文件都探过、day-0 数值已定。
- **坑**:⚠️ Codex 无 `/plan` 命令——用 `specs/*.md`(Goal/Non-Goals/Acceptance/Touched-Files)+ AGENTS.md 里写「先写计划再改码」模拟。〔源〕

---

## NODE4 造零件(agent 特有,**这是和普通编码最不一样的地方**)

### 4a 工具 / ACI〔源:Anthropic writing-tools 2025-09-11、advanced-tool-use 2025-11-24〕
- **放哪**:工具定义(代码里)+ schema;规则在 NODE0 的 `tools.md`。
- **要点**:命名无歧义(`user_id` 不是 `user`)+ 服务前缀命名空间;描述按「跟新同事交代」(何时用/**何时别用**);strict schema(`additionalProperties:false`/enum/required);**只返高信号**(不返 uuid/mime_type/256px_url);`response_format` 枚举 concise/detailed(省 ~1/3 token);错误**可操作**(供自纠);分页/limit(Claude Code 默认截 **25,000 token**);**别 1:1 包 API**,按工作流合并;读/写工具拆开(便于加审批门)。
- **工具太多的正确顺序**:① 加前缀命名 → ② `Tool Search`(`tool_search_tool_regex_20251119`,标 `defer_loading:true`,**省 85% token**,选对率 Opus4 49%→74%)→ ③ `Programmatic Tool Calling`(`code_execution_20260120`,**省 37%**)→ ④ 才考虑拆多 agent。〔源,数字已核〕
- **验收**:每个工具有 name/desc/schema/示例/边界;沙箱跑样例,模型不调错;eval 里工具调用率达标。
- **迭代**:把 eval transcript **整段贴回 Claude Code** 让它批量重构工具。〔源逐字〕

### 4b system prompt〔源:context-engineering 2025-09-29〕
- **放哪**:一个稳定常量/prompt 文件(**别每请求改**——它是缓存边界)。
- **写什么**:角色 + 核心 loop(gather→act→verify)+ **硬约束**(可逆性/成本门/升级触发,用阈值不用散文:`confidence<0.70 的可逆动作需审批`,不是「别太乐观」)+ 软指南。
- **不放什么**:完整工具定义、长会话上下文、时间戳(用 just-in-time 检索)——否则破坏 prompt 缓存。
- **验收**:prompt 缓存生效(`cache_read_input_tokens>0`);对抗输入(「忽略上面指令」)被拒;版本化(`PROMPT_VERSION_x`)。
- **坑**:⚠️ 靠 **eval 迭代**,不是瞎调措辞。

### 4c agent loop + 停止条件(day-0)〔源:building-effective-agents;$4,200 案例〕
- **放哪**:代码里的主循环。
- **最小骨架**:
  ```python
  while iterations < MAX_ITER and cost < BUDGET and time.time() < deadline:
      state = gather()                 # 感知
      resp = llm.complete(...)         # 行动
      cost += resp.usage * PRICE       # ←成本累计,day-0
      if resp.stop_reason == "end_turn": return DONE   # 观察/自检
      iterations += 1
  return STOPPED   # 不靠模型"自觉省着点"
  ```
- **必须的确定性硬上限**:max iterations / **成本预算** / 墙钟超时 / 每工具重试上限。**全是代码,不是 prompt**。
- **验收**:设 `BUDGET=0.01` 跑超额→立即停;设 `MAX_ITER=2`→第 2 步停并升级;模拟 429 死循环→成本守卫在预算内截停。
- **坑**:⚠️ **不设成本上限 = $4,200/63h 那类事故**(429 死循环)。〔源:实践者复盘〕

### 4d 上下文 / 记忆〔源:context-engineering;Chroma context-rot 独立实证〕
- **放哪**:`AGENTS.md`(策展知识)+ 运行时笔记(`progress.txt`/`NOTES.md`/git)。
- **三个杠杆**:① 压缩(summarize 旧轮)② 结构化笔记(写文件、选择性读回)③ 子 agent 隔离(脏活丢给干净上下文的 subagent,只回摘要)。
- **验收**:100 轮对话 token 不线性爆涨(压缩生效);100KB 代码库每任务读 <10 个文件(选择性检索)。
- **坑**:⚠️ **输入越长召回越差(context rot,跨 4 厂商 18 模型实测)**——全历史 ≠ 更好。AGENTS.md 是策展知识,**不是**塞全部历史。

### 4e 护栏〔源:building-effective-agents;prompt-injection-defenses 2025-11;Replit 事故〕
- **放哪**:输入校验(pre-LLM)+ 输出校验(post-LLM),**代码 + 权限层**,不是 prompt。
- **写什么**:输入 PII/注入筛查(加盐标签 `<jd_4f7a2c>...`+ 分类器)；输出 fact 白名单/PII 正则;第二模型 judge。
- **🔴 铁律**:**约束在工具/权限层强制,不在 prompt**。别写「永不删生产库」然后指望它听话——让它**根本没权限**碰生产库。〔源:Replit code-freeze 下仍删库 + 伪造 ~4000 记录〕
- **验收**:路径穿越 `../../etc/passwd` 被拦;注入 JD 被加盐标签隔离;捏造的 fact_id 不在白名单→回退。
- **坑**:⚠️ 单层防御不够(注入即便训练+分类器后仍有 ~1% 成功率)→ 加盐 + 分类器 + 结构隔离三层。

---

## NODE5 验证 = eval(**不是单测**;agent 非确定)〔源:demystifying-evals 2026-01-09〕

- **放哪**:eval 数据集 + grader(**独立只读仓**,见 NODE6);最简起步在 Anthropic Console(零代码)。
- **为什么不是单测**:agent 非确定,同输入两次结果可能不同 → 用 **pass@k / pass^k** 分布指标,不是布尔门。
- **怎么做(0→1)**:
  1. 从 **20–50 个真实失败任务**起(不是合成);bug/生产日志/人工抽检 → 转 case。
  2. 任务要**无歧义 + 有参考解**(两个专家能独立判出同样 pass/fail;0% 通过常是任务坏了不是模型弱)。
  3. grader:代码(快/客观/脆)/ 模型(灵活/需校准 >85% 一致)/ 人(金标准/不扩展);**判结果不判路径**。
  4. 两套:**capability**(从 20-50% 爬)+ **regression**(95%+,CI 门 <95% 即挂)。
- **最简骨架**:Anthropic Console 贴 10-15 个 case + 5 分制 grader + side-by-side(30 分钟,零代码)〔源:eval-tool〕;长大后转代码 + `trace→eval-case→CI 门`(LangSmith `@traceable` / Braintrust `Eval()` `fail_on_regression`)。
- **验收**:regression 套件在 CI 上 pass@1 ≥95% 才放行 merge。
- **坑**:⚠️ **OpenAI 托管 Evals 弃用**(2026-10-31 只读、11-30 关停)→ 用 Promptfoo / Braintrust / LangSmith。⚠️ eval-driven 是「应然非现状」(实测离线 eval 仅 52%);**solo 别追求先建完美 eval**,error-analysis-first(Husain)。

---

## NODE6 evaluator 隔离(🔴 day-0 铁律)〔源:Berkeley RDI 2026-04;ImpossibleBench;METR〕

- **为什么**:agent 会**刷分**——改/删测试让自己通过(ImpossibleBench:Claude >79% 靠改测试;METR o3 ~30% reward-hack)。
- **怎么做**:eval 数据集 + grader 放**独立只读仓**,agent 代码**零写权限**碰 grader/dataset;judge ≠ 被测 agent;agent **不能自验**。
  ```
  ❌ /project/{src, tests, graders.py}   ← agent 能改 tests/graders
  ✅ /project-src(agent) + /project-evals(独立只读:dataset+graders+results)
  ```
- **验收**:agent 说「完成」但独立 judge 说「没达标」→ 不自动信任,触发升级。
- **坑**:⚠️ 这就是「为什么不能让 coding agent 自己写+跑自己的 pass/fail」——它有动机刷分。Berkeley 原话:"Isolate the agent from the evaluator. **Non-negotiable**."

---

## NODE7 确定性闸门(hook —— 把 NODE0 的规则从「建议」变「强制」)〔源:hooks docs〕

- **放哪**:`.claude/settings.json`。
- **最小骨架**:
  ```json
  {
    "hooks": {
      "PostToolUse": [{ "matcher": "Edit|Write", "hooks": [
        { "type": "command", "command": "cd $CLAUDE_PROJECT_DIR && npm run lint && npm run typecheck" } ]}],
      "Stop": [{ "matcher": "", "hooks": [
        { "type": "command", "command": "cd $CLAUDE_PROJECT_DIR && npm test" } ]}]
    }
  }
  ```
- **🔴 退出码铁律**:**只有 exit 2 阻断**;exit 1 **不**阻断(只当非阻塞错)。阻断要 `exit 2` + 原因写 stderr(模型读到会改)。阻 Edit/Write 优先用 JSON `permissionDecision:"deny"`(exit 2 阻编辑不稳)。〔源,本研究既有纠正〕
- **验收**:故意写个 lint 错→PostToolUse 拦住;测试挂→Stop 不让收尾。
- **坑**:⚠️ Stop 连阻 8 次会被强制放行(读 `stop_hook_active` 早退避免循环)。⚠️ Codex **无 hook 生态**——质量门挂 CI / 外部脚本(见映射表)。

---

## NODE8 对抗 review(独立 reviewer)〔源:sub-agents docs;官方 code-review 插件〕

- **放哪**:`.claude/agents/tool-reviewer.md`。
- **最小骨架**:
  ```markdown
  ---
  name: tool-reviewer
  description: 审新写的工具是否合规
  tools: Read, Grep, Glob
  model: inherit
  ---
  你是工具审查员(只读)。对照 .claude/rules/tools.md 审:schema/校验/错误处理/测试/类型。
  只报影响正确性的 gap,带行号;不报风格偏好。
  ```
- **验收**:reviewer 报出真实 gap(漏校验/未处理错误),不刷一堆风格意见。
- **坑**:⚠️ 委托提示里**重述验收标准**(subagent 不自动继承);⚠️ 叮嘱「只报正确性 gap」否则它为挑而挑→带你过度工程。官方 code-review 插件范式:只报 编译失败/明确逻辑错/违反 CLAUDE.md,且**每条发现先验证再报**。

---

## NODE9 迭代回灌 + NODE10 commit/上线(S5)

**NODE9**:把 eval transcript / reviewer 反馈贴回 Claude Code → 它批量改 → 循环到闸门全绿 → commit。〔源:writing-tools〕

**NODE10 上线/运营(S5)**〔源:Microsoft Foundry;Braintrust 2026;OTel GenAI 中立〕:
- 部署载体(原生 API / Agent SDK / MCP server,见 `S1-*.md`)。
- **闭环**:生产失败 trace → 转 eval case → 进 regression 套件 → CI 门自动抓回归。
- 监控用 **OTel GenAI 语义约定**(厂商中立);版本/回滚;注入防护;**成本监控**(day-0 护栏延伸到线上)。
- **【推断】solo 最小上线**:tracing 开着 + 失败 case 持续回灌 + 成本告警,不必上全套可观测平台。

---

## 范例 A:把工具用 MCP 暴露给「被造的 agent」(回答「MCP 接文档 vs 接工具」)

> **3 行澄清**:MCP 是**传输协议**,不是数据类型。docs-MCP 和 tool-MCP **同一个协议、不同 server**:docs-MCP 暴露文档资源,tool-MCP 暴露可执行工具。你接 Stripe 的 tool-MCP、接 Context7 的 docs-MCP,**agent 端代码一样**,差别只在 server 那头发布什么。〔源:modelcontextprotocol.io〕

- **最小 server 骨架(Python FastMCP)**:
  ```python
  # server.py
  from mcp.server.fastmcp import FastMCP
  server = FastMCP("order-tools")
  @server.tool()
  def query_orders(order_id: str) -> str:
      """按 ID 查订单。"""
      return query_from_db(order_id)
  if __name__ == "__main__":
      server.run(transport="stdio")   # 或 http
  ```
- **agent 端接上**:`claude mcp add order-tools -- python /path/server.py`(生成 `.mcp.json`)。
- **何时用 MCP vs 直接 in-process 函数**【推断,据 order-guard 等实例】:跨客户端复用 / 工具独立仓/语言 / 要热重载 → **MCP**;单 app、同语言、一起迭代 → **直接函数**(别为架构感套 MCP)。
- ⚠️ 具体 SDK 版本以 modelcontextprotocol.io 当前为准(版本号变动快)。

## 范例 B:Skill vs MCP vs 直函数 + 端到端 SKILL.md〔源:code.claude.com/skills;Anthropic Agent Skills 2025-10-16〕

- **判据(一句话)**:
  - **Skill** = 可复用的**过程性知识/怎么做**(多步流程),渐进式披露、按需加载 → `.claude/skills/<n>/SKILL.md`。
  - **MCP** = **工具/数据连接**(外部系统),跨客户端 → MCP server。
  - **直函数** = 单个 in-process 能力(hash/parse)→ 代码里。
  - 决策:**是不是反复用的多步流程?**→是→Skill;否→**要不要接外部系统/数据?**→是→MCP;否→直函数。
- **SKILL.md 三级骨架**:
  ```markdown
  ---
  name: code-release
  description: "准备/验证/发布一个 release(打 tag、changelog、GitHub release)。用户说'发版/ship it'时用。"
  ---
  # L1 一句话 + 主流程:gather→定版本→校验→产物→commit&tag→push→GitHub release
  # L2 各阶段详细步骤 + 决策门 + 具体 bash 命令
  # L3 references/*.md 按需加载(version-strategy.md / changelog-rules.md / rollback-runbook.md)
  ```
  - frontmatter 始终加载(~80 token);L2 命中才加载;L3 用到才读 → 省上下文。
- ⚠️ `allowed-tools` 标 experimental。

---

## Claude Code ↔ Codex 映射(次工具能不能独立走完)〔源:codex 文档〕

| 阶段 | Claude Code | Codex 等价 | 缺口 |
|---|---|---|---|
| 上下文规矩 | `.claude/AGENTS.md`/rules | `.codex/AGENTS.md`(`[features] child_agents_md=true`,32KiB) | ✅ 基本一致 |
| 探索 | plan mode 只读 | **无**,靠 spec 文件 + prompt | ❌ 无原生 |
| 规划 | plan mode + 可编辑 | **无 `/plan`**,用 `specs/*.md` 模拟 | ❌ 无原生 |
| 实现 | while-loop + 沙箱 | 同(`sandbox_mode`×`approval_policy`,Seatbelt/bubblewrap) | ⚠️ Linux 装 bubblewrap |
| 质量门 | hooks | **无 hook**,挂 CI/外部脚本 | ❌ 无原生 |
| 知识注入 | WebFetch/MCP/Skill | `web_search=live`(默认 cached 过时!)/ 自建 MCP | ⚠️ 较弱 |

【推断,基于 codex 文档无相关命令】**结论**:Codex ≈ 70% 对齐;探索/规划/质量门三处需自己用 spec 文件 + CI + 外部脚本补。Codex 偏「本地自主执行」,不是「多阶段团队工作流」。

---

## 横切铁律(收口,solo 也不可省)

1. 🔴 **成本/递归/墙钟硬上限**,写代码不写 prompt(NODE4c)。
2. 🔴 **evaluator 与 agent 隔离**(NODE6)。
3. 🔴 **约束在工具/权限层强制**,不在 prompt(NODE4e)。
4. 规则(NODE0,建议)必须由 **hook(NODE7,强制)** 兜底——模型会飘。
5. 验证 agent = **eval 非单测**(NODE5),因为它非确定。

> 标注复核:本稿凡带数字/版本/价格处均标〔源〕或【推断】;弃用项(OpenAI Evals、Codex cached、Context7 安全)已标 ⚠️。与 `flow.md` 冲突时以 flow.md 为准。
