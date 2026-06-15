# KB 候选池盘点

> 状态: C01 已完成初筛。
> 扫描时间: 2026-06-14。
> 范围: `/Users/shenghuikevin/kb-vault/output`, `/Users/shenghuikevin/kb-vault/wiki`, `/Users/shenghuikevin/kb-vault/learning/agent-field`。
> 方法: 3 个只读 subagent 分区扫描 + 主 agent 汇总去重。本文是候选池,不是发布批准;所有内容进入公开 blog 前仍需 review-ready 草稿、human 审核、`content:check` / `content:sync`。

## 结论

第一批最稳的公开化主线不是“把 KB 原文搬到 blog”,而是围绕 **RAG / Context Engineering → Agent Memory → Agent Systems / Harness → Agent Safety & Eval** 做策展改写。

优先级最高的 5 个起点:

1. `output/2026-06-04-rag-is-not-dead-context-engineering.md` — 最接近可发布的中文 essay。
2. `wiki/overview-rag-systems.md` — 可与上条合并校准,形成 RAG 主题主文。
3. `wiki/agent-memory/overview-agent-memory-2026.md` — 第二条主线,适合写成 Agent Memory 解释文。
4. `learning/agent-field/misconceptions.md` — 适合改成“我对 AI Agent 的 8 个误解”系列主矿脉。
5. `learning/agent-field/takes/agent-loop-vs-code-loop.md` + `wiki/agent-field/workflow-vs-agent.md` — 可合并成一篇 agent 架构判断框架。

当前没有任何候选应被视为 `approved` 或 `published`。大多数候选的主要风险是:外部事实需要刷新、内部学习语境需要去私有化、AI draft / deepresearch 草稿需要重写成公开成品、weekly digest 只能作为素材矿脉。

## 候选表

| status | source path | proposed type | theme | quality signal | public risks | next action |
|---|---|---|---|---|---|---|
| candidate | `/Users/shenghuikevin/kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md` | essay | RAG / context engineering / evidence chain | 中文长文结构完整,有明确论点、分层解释、边界辨析和安全段落 | 外部技术判断需按当前来源刷新;需要补 blog frontmatter 和来源链接 | 作为第一批主 essay 候选;与 `wiki/overview-rag-systems.md` 交叉校准后进入 review-ready 草稿 |
| candidate | `/Users/shenghuikevin/kb-vault/wiki/overview-rag-systems.md` | essay | RAG / context engineering | `status: active`;中文主线清楚,有 source calibration 和学习路线 | 2026 来源需刷新;不要暴露 raw/private 路径或内部索引 | 与 RAG output 合并为公开长文,保留“RAG 没死,死的是 lazy vector-RAG”主论点 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/output/2026-05-23-context-engineering-in-2026-three-source-synthesis.md` | essay | context engineering / agents / long-horizon work | 三源综合,结构清晰,有时间线、taxonomy、生产案例 | 第三方公司和产品架构描述需核对原始来源和时间点;英文/双语口吻需统一 | 改成中文或双语长文,保留“2025-2026 收敛”主线 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/concept-context-engineering.md` | essay | context engineering / RAG / memory | 材料密度高,有大量 headings 和 links | 标记偏 `needs-review`;聚合来源多,容易过时或混杂 | 做事实核查后拆成概念长文或作为上条的 source-only 支撑 |
| candidate | `/Users/shenghuikevin/kb-vault/wiki/agent-memory/overview-agent-memory-2026.md` | essay | agent memory / context lifecycle | `status: active`;边界定义强,贴合个人知识空间定位 | 过于笔记化;外部框架和术语需刷新 | 扩写成“Agent memory 不是 vector DB”类解释文 |
| candidate | `/Users/shenghuikevin/kb-vault/wiki/agent-memory/learning-plan-agent-memory-2026.md` | log | learning log / study map | 阶段看板完整,中文学习路径明确 | 可公开为个人学习路径,但不能包装成通用课程或权威教程 | 改成“我如何系统学习 Agent Memory”的学习 log |
| source-only | `/Users/shenghuikevin/kb-vault/wiki/agent-memory/source-summary-agent-memory-frontier-sources-2026.md` | source-only | agent memory / source pack | 可作为 frontier sources 索引,支撑主文事实校准 | 不是成品文章;需检查每个来源时效和授权引用边界 | 作为 Agent Memory essay 的来源清单,不直接发布 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/learning/agent-field/misconceptions.md` | essay | agent systems / harness / production judgment | “Old model → New model → why wrong”结构强,适合系列化 | 含个人学习过程和 mentor/内部语境;部分外部数字需重新核验 | 改成《我对 AI Agent 的 8 个误解》系列,删除私人学习记录,补 primary sources |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/takes/harness-as-moat.md` | essay | harness / model commodity / strategy | thesis 清楚,短而有判断,和 blog 定位匹配 | 当前是 draft; benchmark 数字和判断需核验 | 扩成 900-1200 字文章,补“什么时候 fine-tune 才值得做”的边界 |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/takes/agent-loop-vs-code-loop.md` | essay | workflow vs agent / architecture judgment | 核心判据清楚:“function calling 是能力,loop 是授权” | 含个人验证轨迹;不能包装成已完成生产项目 | 与 `wiki/agent-field/workflow-vs-agent.md` 合并成架构解释文 |
| candidate | `/Users/shenghuikevin/kb-vault/wiki/agent-field/workflow-vs-agent.md` | essay | agent architecture | 有 My take / Fact-check / sources_pending false,适合作为判断框架 | AI draft 需重写;术语判断避免绝对化 | 写成“什么时候用 workflow,什么时候给 agent loop 授权” |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/scenarios/theme-2-customer-service-refactor.md` | note | agent architecture / customer service / tool surface | 有问题、指标、错误方案、最终架构,案例感强 | 场景必须标明 hypothetical;引用厂商实践需重找来源 | 改成“架构判断题 + 标准解”,不要称为真实项目 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/learning/agent-field/scenarios/theme-3-research-platform.md` | essay | MCP / A2A / context engineering / knowledge systems | 综合性强,能展示系统判断力 | 公司内部平台设定易被误读为真实内部设计;MCP/A2A 状态时效性强 | 改成“400 人公司 research assistant 架构题”,标明假设案例并刷新协议事实 |
| source-only | `/Users/shenghuikevin/kb-vault/learning/agent-field/curriculum.md` | source-only | learning map / agent field | 五大主题结构完整,适合生成系列目录 | 内部教学脚本和 mentor 准备较多,不宜原文公开 | 抽成公开版 landing essay:《2026 年理解 Agent 工程的 5 个问题》 |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/glossary.md` | note | glossary / field map | 条目密度高,很多定义已压缩成一句话 | 部分“2026 当前状态”需刷新;术语可能依赖未公开 wiki | 挑 12-15 个术语做公开 glossary / notes |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/scenarios/theme-2-pdf-summarization.md` | note | workflow patterns / document AI | 结论实用: parallelization + prompt chaining,而非 agent loop | teach-only 材料;不能声称生产实践 | 改成短文《不是所有长任务都需要 Agent》 |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/scenarios/theme-1-choosing-the-moat.md` | note | strategy / harness / fine-tuning | 商业判断题形式好,tradeoff 清楚 | fine-tune/harness 行业状态变化快,不应绝对化 | 补 fit conditions:何时 harness-first 成立,什么证据会改变选择 |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/questions.md` | log | agent infra / CI/CD / continuous compute | 问题意识强,适合 research agenda | 多数是未验证问题,不能写成结论 | 发布为 open questions log,明确“观察清单,不是判断” |
| candidate | `/Users/shenghuikevin/kb-vault/learning/agent-field/scenarios/theme-2-pattern-placement-round2.md` | log | workflow patterns / learning from mistakes | 失败案例有价值,能展示判断边界 | 个人学习痕迹重;不适合权威教程口吻 | 改成“判断误区复盘”,弱化个人分数,强化判据 |
| source-only | `/Users/shenghuikevin/kb-vault/learning/agent-field/progress.md` | source-only | learning log / process evidence | 可作为事实索引,记录稳定概念和 gap | 高度私人化,含过程性缺陷和导师评价 | 只作为素材索引,不直接发布 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/output/2026-05-16-agents-report.md` | note | agent architecture / workflows / reflection / code agents | 短而聚焦,有 executive summary、findings、evidence、implications | 部分例子涉及产品/协议现象,需避免未经验证的普遍结论 | 改成“我现在怎么看 agent 系统的可控性”短文 |
| source-only | `/Users/shenghuikevin/kb-vault/output/2026-06-10-week-2026-W24-digest.md` | source-only | AI adoption / memory / agent eval / cross-surface execution | 素材密度高:大量 raw/wiki/update 汇总 | 混有医疗/生物安全、第三方产品、未解决冲突、局部内部痕迹 | 不迁全文;拆出“AI adoption as behavior change”“cross-surface execution”等专题 |
| source-only | `/Users/shenghuikevin/kb-vault/output/2026-06-03-week-2026-W23-digest.md` | source-only | RAG systems / AI governance / decision traces / observability | 含 RAG overview 相关材料,覆盖面广 | 治理/第三方事实需复核,有未解决冲突 | 作为 RAG 后续系列和 agent observability 选题池 |
| source-only | `/Users/shenghuikevin/kb-vault/output/2026-05-27-week-2026-W22-digest.md` | source-only | agent-native cloud / composable computers / multi-agent systems | 覆盖面广,可挖“agent-native cloud”主题 | 太杂,含本地/内部痕迹、医学/安全类敏感主题 | 只抽主题,优先抽“composable computers / end of localhost” |
| source-only | `/Users/shenghuikevin/kb-vault/output/2026-05-19-week-2026-W21-digest.md` | source-only | continuous compute / E2B / agent runtime | 候选主题集中,围绕 continuous compute | 视频/演讲内容需回看来源,避免标题式总结 | 整理成 note:“为什么 agent 需要 continuous compute,而不是传统 CI/CD” |
| source-only | `/Users/shenghuikevin/kb-vault/output/2026-05-10-week-2026-W19-digest.md` | source-only | agent foundations / Reflexion / smolagents / guardrails | 可给 Agents Report 补背景材料 | 有本地路径/私有语境类型,只能抽公开概念 | 作为 agent 系列背景材料,不直接发布 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/agent-field/mcp.md` | note | MCP / tools / protocol | hub/cc 标记,结构完整,有 when-to-use | MCP 变化快,可能有重复 draft | 做成“工程师视角的 MCP 使用边界”,发布前查官方/primary docs |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/agent-field/code-execution.md` | essay | sandbox / code interpreter / agent safety | 材料完整,source 状态较好 | 安全主题高风险;CVE/标准/厂商能力需刷新;避免攻击细节 | 做官方来源刷新后写防守型 code execution/sandbox 文章 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/agent-field/prompt-injection-defense.md` | essay | agent security | 有 Fact-check,材料密度高 | 攻防内容需克制,不要给可操作攻击细节 | 改成威胁模型 + 防线分层的防守型文章 |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/agent-field/permission-system.md` | essay | agent safety / governance | 权限系统主题适合和 prompt injection 组成安全系列 | 安全/治理主张需审慎,可能含厂商概念 | 与 prompt injection 合并或组成安全系列第二篇 |
| candidate | `/Users/shenghuikevin/kb-vault/wiki/agent-field/continuous-compute.md` | essay | agent infra / dev loop | 主题有个人 blog 差异化,来自 session synthesis | 前瞻性强,需标注判断/趋势而非事实 | 写成“agent 时代为什么 CI 不够了” |
| source-only | `/Users/shenghuikevin/kb-vault/wiki/agent-field/tau-bench.md` | source-only | agent eval / benchmark | benchmark 结构清楚 | benchmark 分数/状态易过时,不宜直接当观点文 | 作为 eval 系列素材,先刷新论文/leaderboard |
| needs-rewrite | `/Users/shenghuikevin/kb-vault/wiki/agent-field/tool-use-eval.md` | note | agent eval / tools | 有 My take / Fact-check | 榜单和工具生态需刷新,部分断言可能过强 | 与 regression set / tau-bench 合并成“agent eval 地图” |

## 第一批建议组合

### 组合 A: RAG / Context Engineering

- 主 essay: `output/2026-06-04-rag-is-not-dead-context-engineering.md`
- 校准素材: `wiki/overview-rag-systems.md`, `wiki/concept-context-engineering.md`
- 补充素材: `output/2026-05-23-context-engineering-in-2026-three-source-synthesis.md`
- 推荐 blog 形态: 1 篇长文 + 2-3 条 notes + links。
- 进入 C04 前置条件: source refresh、frontmatter、公开口吻重写、`content:check`。

### 组合 B: Agent Memory

- 主 essay: `wiki/agent-memory/overview-agent-memory-2026.md`
- log: `wiki/agent-memory/learning-plan-agent-memory-2026.md`
- source pack: `wiki/agent-memory/source-summary-agent-memory-frontier-sources-2026.md`
- 推荐 blog 形态: “Agent memory 不是 vector DB”长文 + 学习 log。
- 进入 C04 前置条件: 框架/术语刷新,删除内部学习计划痕迹。

### 组合 C: Agent Systems / Harness

- 主矿脉: `learning/agent-field/misconceptions.md`
- essay seeds: `learning/agent-field/takes/harness-as-moat.md`, `learning/agent-field/takes/agent-loop-vs-code-loop.md`, `wiki/agent-field/workflow-vs-agent.md`
- case notes: `learning/agent-field/scenarios/theme-2-customer-service-refactor.md`, `theme-2-pdf-summarization.md`, `theme-1-choosing-the-moat.md`
- 推荐 blog 形态: 一篇“误解纠偏”长文 + 3 条架构判断 notes。
- 进入 C04 前置条件: 去 mentor/课程化口吻,标明 hypothetical cases,补 fit conditions。

### 组合 D: Agent Safety / Eval

- security seeds: `wiki/agent-field/prompt-injection-defense.md`, `code-execution.md`, `permission-system.md`
- eval seeds: `wiki/agent-field/tau-bench.md`, `tool-use-eval.md`
- 推荐 blog 形态: 暂不作为第一篇发布;先做 source-only refresh。
- 进入 C04 前置条件: 官方/primary source refresh,避免攻击细节,避免过期 benchmark。

## 不适合直接公开的类型

- Weekly digest 原文: 适合作为 source-only 主题矿脉,不适合直接发布。
- `learning/agent-field/progress.md`, `curriculum.md`: 可做素材索引,不宜原文公开。
- deepresearch/wiki AI drafts: 需要重写成公开成品,不能直接搬运。
- local/private 项目痕迹: 只能抽象成公开概念或 hypothetical case,不能伪装成真实项目成果。
- 医疗、生物安全、攻防安全类内容: 必须经过更强来源刷新和风险删减。

## 对 C02/C03 的输入

C02 设计 `blog-publisher` 能力时,至少应支持:

1. 从本候选表筛选 `candidate` / `needs-rewrite`。
2. 生成 `docs/content-pipeline/reviews/<slug>.md`,包含来源、改写目标、公开风险、需要核验的事实、human review checklist。
3. 只有 human 审核通过后,才生成 `docs/content-pipeline/manifests/<slug>.json`。
4. 调用 `site/scripts/content-check.mjs` 和 `content-sync.mjs`。
5. 发布后再跑 build / RSS / route / UI 基础验证。

## C01 验收记录

- 已覆盖目录: `/Users/shenghuikevin/kb-vault/output`, `/Users/shenghuikevin/kb-vault/wiki`, `/Users/shenghuikevin/kb-vault/learning/agent-field`。
- 候选数量: 33 条,满足至少 20 条要求。
- 每条候选已包含 proposed type、主题簇、质量信号、公开风险、下一步。
- 已明确 source-only、needs-rewrite、candidate 的区别。
- 已明确 demo/toy/local/private 不得伪装成公开项目或真实成果。
