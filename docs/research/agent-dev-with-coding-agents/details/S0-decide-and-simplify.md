# S0 — 判断要不要 agent / 从简(执行层 · 正式版)

> 状态:**已过对抗 eval**(2026-06-17;无编造引语,一手直引逐字核过;两处日期 + 一处引语 + Gartner 主因 + 一条过时 caveat 已按 eval 修正)。
> 锚:`../flow.md` S0 行。一手源见 `../sources.md` A / I 段。证据标 **独立 vs 厂商**,拿不准标 **unverified / 未确认**。
> 适用对象:个人开发者用 coding agent 开发一个 AI agent 应用。**S0 无 d1–d6 草稿,本文从一手源直接提炼。**

## 做什么(一句话)

动手前先过一道门:**能用确定性方案 / 单次 LLM 调用 / workflow 解决的,就别上 agent;真要上,从最简形态起。** 这一步是 GATE,不是形式——它防的正是「项目被砍」那类错误(见坑 2)。

---

## 具体怎么做(照着走的决策程序)

### 步 1 — 先证伪 agent(默认不上)
这事能不能用以下任一解决?能 → **不要 agent**。
- (a) 一段确定性代码 / 规则;
- (b) 单次 LLM 调用 + 检索 / few-shot;
- (c) 预定义路径的 **workflow**(LLM 与工具按写死的代码路径编排)。

> OpenAI《A Practical Guide to Building Agents》(一手厂商,2025-04-17 发布;日期为发布日,非 PDF 内印):
> "Before committing to building an agent, validate that your use case can meet these criteria clearly. Otherwise, a deterministic solution may suffice."

> Anthropic《Building Effective Agents》(一手厂商,2024-12-19):
> "we recommend finding the simplest solution possible, and only increasing complexity when needed."
> "For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough."

workflow 与 agent 的官方分界(Anthropic 逐字):
- **Workflow** = "systems where LLMs and tools are orchestrated through predefined code paths."(可预测、可控,适合定义良好的任务)
- **Agent** = "systems where LLMs dynamically direct their own processes and tool usage."(灵活、模型自主决策,适合规模化的开放问题)

### 步 2 — 过 OpenAI 三条准入门(至少清楚命中一条)
OpenAI 建议优先挑「过去自动化反复碰壁」的场景,三类信号(标签 + 例子均逐字):
1. **复杂决策(Complex decision-making)**:需细腻判断、例外、上下文敏感的决定。例:客服里的 "refund approval"。
2. **难维护的规则(Difficult-to-maintain rules)**:规则集庞杂、改一处易出错。例:"performing vendor security reviews"。
3. **重度非结构化数据(Heavy reliance on unstructured data)**:解读自然语言 / 抽取文档 / 对话式交互。例:"processing a home insurance claim"(理赔)。

> ⚠️ 这三条是 OpenAI 从客户部署里**事后归纳的推荐**,非中立事实——但作为「准入筛子」可直接用。

### 步 3 — 过 Anthropic 适用性测试
命中以下全部 → 才真正适合 agent:
- 开放式问题,**步数无法预测**("difficult or impossible to predict the required number of steps");
- 路径**无法硬编码**("you can't hardcode a fixed path");
- 你愿意在**规模上信任模型的自主决策**。

### 步 4 — 复杂度阶梯(从低往高,只在不够用时升级)
```
单次 LLM 调用 + 检索/few-shot
  → workflow(预定义路径)
    → 单 agent + tools          ← agent 的默认起点
      → 多 agent(仅严格触发,留到 S1)
```
> 代价是实打实的:Anthropic「Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.」

---

## 跨厂商佐证(证明 S0 是公共交集,非一家之言 —— 四家)

- **OpenAI**(一手):"Our general recommendation is to maximize a single agent's capabilities first."(先把单 agent 喂饱,别过早编排多 agent。)
- **Anthropic**(一手):simplest-first + 单次 LLM 调用常已够(见上)。
- **Google ADK**(一手):start single-agent,grow to multi-agent only when needed;**无硬性要求**从单 agent 升到多 agent(第 4 家独立佐证)。
- **Microsoft Foundry**(一手,development-lifecycle 文档,`ms.date 2026-02-02`,更新 2026-06-05):生命周期「at a glance」**第 1 步**逐字为 "Choose an agent type: Start with a prompt-based agent, a workflow, or a Hosted agent."
  - 🟡 边界:这是 MS 的**建造 checklist 第 1 步**,可作为「建造前定范围/选类型」的第一步用;但 MS 并未把它框成「到底要不要 agent」那道门——「先选类型即定范围」是本研究的合理解读,非 MS 原话。
- **Hamel Husain**(**独立专家**,evals-FAQ,2026-01-15):"benevolent dictator"——单一领域专家拍板、单 agent 优先;先做 error analysis 而非先搭基础设施。(同站《Should I practice eval-driven development?》URL 现为 200 live,非 404。)

---

## 坑(S0 最容易栽的地方)

1. **过度工程**:把本该是 workflow / 单次调用的需求直接上 agent → 白付延迟与成本(Anthropic 的 latency/cost tradeoff)。这是 S0 的头号反模式。
2. **S0 做错代价大**:**Gartner 预测 >40% agentic AI 项目 2027 年前被砍**(独立研究机构,2025-06-25;number 已从 Gartner newsroom 原文确认,先前「被 Cloudflare 挡 / unverified」caveat 已失效删除)。Gartner 列的主因是 **成本攀升、业务价值不清/不足、风险控制不足**,叠加炒作与 "agent-washing"。
   - 〔本研究推断,非 Gartner 原话〕这类「成本/价值/复杂度不匹配」的失败,本可在 S0 的用例 + 复杂度决策阶段提前避免——这正是不省 S0 的理由。
3. **agent ≠ 一定更快**:METR 独立 RCT(2025-07-10),熟手在熟悉大仓用 early-2025 AI **反而慢 19%**,事前自估快 24%、事后仍以为快 20%。**强边界**:作者明确拒绝外推成「AI 普遍拖慢开发」。教训——别默认「上 agent/AI = 提速」,尤其成熟代码库 + 熟手场景。

---

## 边界(solo vs 生产)

- 纯 **solo / 小改 / ad-hoc**:完整 agent 机器(多 agent 编排、正式 eval 套件)是 overkill(与 Husain「benevolent dictator + error-analysis-first」、Anthropic simplest-first 一致;另有 TDS《From Vibe Coding to SDD》自承「小改/单人/ad-hoc 写完整 spec 是 overkill」——**未确认**,二手未独立核)。
- **但这道决策门本身极便宜,solo 也必须过**:它不要求你搭任何基础设施,只要求你诚实回答「确定性方案/workflow 够不够」。省掉它 = 直接奔向坑 2 那类被砍项目。
- 与 `flow.md` 三条诚实边界一致:全套工程回报随「多人 + 生产 + 长期维护」上升;但 **day-0 硬护栏 + evaluator 隔离对 solo 同样不可省**(那是 S2 的事,S0 这里只立「从简」基调)。

---

## 一句话出口(进入 S1 的判据)
> 走完步 1–4 后:**没命中三条准入门 / 适用性测试 → 停在 workflow 或单次调用,S0 即终点;命中 → 默认「单 agent + tools」进入 S1,把「要不要多 agent / 框架 vs 手写 / 部署载体」留给 S1 决。**
