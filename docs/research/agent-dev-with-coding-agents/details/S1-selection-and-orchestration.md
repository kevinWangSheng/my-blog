# S1 — 选型/编排(执行层 · 正式版)

> 状态:**已过对抗 eval**(2026-06-17;3 路一手源重抓 + 1 路对抗核验。修正:删假逐字引语、删无依据「2 周」、多 agent 数已坐实去 unverified、补 Evals 双日期、MCP 98.7% 改回单例)。
> 锚:`../flow.md` S1 行。底料 d2(规划侧)+ d6(单 vs 多/部署)。一手源见 `../sources.md` A / G / H 段。证据标 **独立 vs 厂商**,拿不准标 **未确认**。
> 前置:S0 已判「该上 agent」。本步定三件事 → 进 S2。

## 做什么(一句话)

S0 判定要 agent 后,S1 定**三个子决策**:① 单 vs 多 agent ② 框架 vs 手写 ③ 部署载体。默认姿态:**单 agent + tools + 短链;框架按规模取;载体从最简 API loop 起。**

---

## 子决策 A — 单 agent vs 多 agent(默认强单 agent)

**独立证据**:Stack Overflow《Agents on a leash》(独立调查,2026-05-27,n≈1,100):**69% 用单 agent** / 17% 多专才 / 16% 多协调;68% 偏好单 agent 而非复杂多 agent 配置。

**严格触发(基本全命中才上多 agent)**:
1. 子任务**真正独立、可并行**(breadth-first),无共享 state;
2. **专才化收益 >> 协调成本**;
3. **价值 >> token 成本**。

**多 agent 成本(Anthropic 自报,built-multi-agent-research-system,已重抓核实)**:
- 多 agent 系统 "use about **15× more tokens** than chats"(单 agent 基线约 4× chat;即多 agent ≈ 单 agent 的 ~4 倍量级);
- "token usage by itself explains **80% of the variance**" in performance;
- "multi-agent system ... outperformed single-agent Claude Opus 4 by **90.2%**"(厂商内部 eval)。

**别用(官方)**:强依赖 / 共享 context / 实时协调;**大多数编码任务**。失败模式逐字(C 编译器):"Every agent would hit the same bug, fix that bug, and then overwrite each other's changes."

**旗舰边界(别拿它当日常)**:Anthropic 用 16 个并行 agent 写 Rust 版 C 编译器,~2,000 个 Claude Code 会话,API 成本 just under **$20,000**,Opus 4.6 烧 **2 billion input tokens**。作者逐字定性:"This project was designed as a capability benchmark. I am interested in stress-testing the limits of what LLMs can just barely achieve today." —— 即能力压测,非日常工作流。

---

## 子决策 B — 框架 vs 手写(默认从手写 loop 起)

**Anthropic《Building Effective Agents》(一手,2024-12-19,`/engineering/building-effective-agents`)**:
- "We suggest that developers start by using LLM APIs directly; many patterns can be implemented in a few lines of code."
- 框架 "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug."
- "don't hesitate to reduce abstraction layers and build with basic components as you move to production."

**LangChain《On Agent Frameworks and Agent Observability》(厂商,2026-02-12)**:
- 框架价值:把最佳实践编进框架、减样板、提升可读性、上生产更顺;
- 但 "if it's a simple LLM request, adding a framework may be too heavy handed";
- 关键转向:"Agents are non-deterministic systems ... your app logic is documented in **traces, not code**" —— 选不选框架,不如 debug/test/monitor 重要(锚到 S4)。

**何时上框架**:多 agent 编排 / 需 checkpoint / 持久执行 / 会话状态 / 长任务。

**2026 框架格局**(指示性,名 + 存活状态;**具体采用率/星数/客户名一律 未确认**,本研究不引营销数):
| 框架 | 厂商 | 2026 状态 |
|---|---|---|
| LangGraph | LangChain | 在世 / 生产 |
| CrewAI | CrewAI | 在世 / 生产 |
| OpenAI Agents SDK | OpenAI | 在世 / 生产(官方推荐的迁移目标) |
| Microsoft Agent Framework 1.0 | Microsoft | 在世(2026-04-03 GA,合并 AutoGen + Semantic Kernel) |
| Google ADK | Google | 在世 |
| Claude Agent SDK | Anthropic | 在世 / 生产 |
| ⛔ OpenAI Agent Builder | OpenAI | **已弃,2026-11-30 关停** → 迁 Agents SDK |
| ⛔ OpenAI hosted Evals | OpenAI | **2026-10-31 转只读、2026-11-30 关停** → 迁 Promptfoo |
| ⛔ AutoGen | Microsoft | 维护模式,被 Agent Framework 取代 |

**坑**:别押已弃产品(Agent Builder / hosted Evals);AutoGen 仅维护、新项目别起。

---

## 子决策 C — 部署载体(怎么把 agent 跑起来 / 交出去)

三种主要形态,**从简往复杂**:

- **原生 API loop(最简)**:直接 Messages / Responses API + 自管编排;单次 / 短链够用。
- **Agent SDK(loop 托管)**:Claude Agent SDK / OpenAI Agents SDK——库,把循环 + 工具 + 会话/状态管起来;要自定工具逻辑 / 本地原型 / CI 时选。Claude Agent SDK 核心循环逐字(出自《Building agents with the Claude Agent SDK》博客,2025-09-29,非 API docs 页):**"gather context → take action → verify work → repeat"**。
- **MCP server(互操作)**:把能力做成 MCP 服务,任何 MCP 客户端(Claude / ChatGPT / Cursor / VS Code)可调;跨客户端复用 / 团队共享 / 对外暴露时选。Anthropic《Code execution with MCP》(2025-11-04):把 MCP 当 code API 让 agent 写代码调用——一个工作示例从 150,000 token 降到 2,000(**98.7%**,**单例非通用率**,厂商自报)。

**OpenAI 载体辨析**:
- **Responses API**(单次模型调用 + 内置工具,你管编排)vs **Agents SDK**(框架管编排/状态/handoff/guardrails)。
- **Assistants API 已弃,sunset 2026-08-26**(2025-08-26 公告,一年通知期);**Chat Completions 仍在**(向后兼容),但新项目官方推 Responses API。

**solo 选择**:单 agent 应用最快上手 = Responses API 或 Claude Agent SDK;要别的客户端调你的工具 → 做成 MCP server。

---

## 边界(solo)

- **单 agent 强默认对 solo 尤其成立**(SO 69%;价值/token 比例几乎总不利多 agent)。
- 框架对 **solo 单 agent 常是 overkill**;手写 loop + 好工具 + 短链通常够。
- 载体别过早复杂:**无跨客户端复用需求前,别为「架构感」先上 MCP server**。

---

## 出口(进 S2)
> 选定 **[单/多 agent] × [框架/手写] × [载体]** 后进 S2 设计零件(工具/ACI、上下文、指令、记忆、护栏)。**S2 的 day-0 硬护栏(成本/递归硬上限 + evaluator 隔离)必须在那一步定死**——本步只立「单 agent + 从简」基调。
