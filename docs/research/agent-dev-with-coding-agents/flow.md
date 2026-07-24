# 开发一个 agent 的流程(正本 · 2026 · eval 通过版)

> 状态:**已确认**。经多轮 subagent 搜索 + 4 路对抗式 eval 修订通过(2026-06-16;eval 裁决要点/记录锚点见 `sources.md` 末「eval 轮关键修正」+「已被打回」两段)。
> 证据全表见 `sources.md`。本文件是「流程正本」,后续逐步深钻以此为锚。
> 适用对象:个人开发者用 coding agent(Claude Code / Codex / Cursor)开发一个 AI agent 应用。

## 重要前提
没有任何单一厂商发布过「唯一正确流程」。本流程 = OpenAI / Google / Anthropic / Microsoft / LangChain **重叠的公共交集** + 把关键护栏前置。文末有各家命名对照。

## 流程图

```
S0 判断要不要 agent → S1 选型/编排 → S2 设计零件(含 day-0 硬护栏)
   → S3 实现 → S4 观测+eval(贯穿) → S5 上线+运营
   ┌─ 横切(day-0,solo 也不可省):成本/递归硬上限 · evaluator 隔离 · 人审按风险触发 · 知识保鲜
   └─ 运行时循环(你做的 agent 跑起来的样子):ReAct / Think-Act-Observe(感知→行动→观察→自检)
```

## 各步定义 + 证据 + eval 判定

| 步 | 做什么 | 证据(尽量跨厂商) | eval 判定 |
|---|---|---|---|
| **S0 判断+从简** | 先判断该用 workflow 还是 agent;满足准入再上 agent;最简方案优先 | OpenAI《Practical Guide》;Anthropic building-effective-agents;Microsoft Foundry;Husain | ✅ 多厂商共识 |
| **S1 选型/编排** | **默认单 agent + tools**;多 agent 仅当指令跟不上/工具重叠/高价值并行;框架 vs 手写;部署载体(API/SDK/MCP server) | OpenAI「maximize a single agent first」;Anthropic「多 agent ~15× token」;LangChain | ✅ 共识(单 agent 默认) |
| **S2 设计零件** | 工具/ACI、上下文工程、指令、记忆/数据、护栏+停止条件、(可选)Skills 模块 | OpenAI=Model/Tools/Instructions;context engineering 已通用(Karpathy/Lütke);guardrails 早于 Anthropic(NVIDIA NeMo 2023) | 🟡 共识但各家分法不同 |
| ⛔ **day-0 硬护栏(在 S2 就定)** | 成本/递归深度/墙钟时间**硬上限**;**evaluator 与被测 agent 隔离** | $4,200/63h 复盘(2026-04);Berkeley RDI「Isolate the agent from the evaluator. Non-negotiable」(2026-04) | ✅ 前置(原候选放最后=错) |
| **S3 实现** | coding agent 辅助写码(explore→plan→implement→commit);接工具/指令/记忆 | Claude Code best-practices;OpenAI Codex | ✅ 共识 |
| ↻ **运行时循环(横切)** | agent 跑起来 = 感知→行动→观察→自检 | Google「Think, Act, Observe」;ReAct(arXiv);Anthropic「gather→act→verify」是同一回事的一家命名 | ✅ 共识(措辞各异) |
| **S4 观测+eval(贯穿)** | **先 tracing 看发生什么**,再用 trace 建 eval;eval-driven=early & continuous;capability vs regression | LangChain「traces become eval dataset」;Anthropic「20-50 真实失败任务起步」;Google trajectory eval | ⚠️ 见下边界 |
| **S5 上线+运营** | 部署形态、监控、**失败 trace→eval case→CI 门**、版本/回滚、**prompt-injection 防护**、成本监控 | Microsoft Foundry 9 步;Braintrust 2026;OTel GenAI 语义约定(中立) | ✅ 共识 |

## 三条诚实边界(必读,不加=把规范当现状)

1. **eval-driven 是「应然」非「现状」**:2026 实测 tracing 89%,但离线 eval 仅 52%、在线 37%、近 30% 完全不做(LangChain n=1340)。「先建 eval」是少数派最佳实践;LangChain 称「先建完美 eval 再上线 rarely realistic」;Hamel Husain 主张 error-analysis-first。
2. **eval 数字只有 evaluator 隔离时才可信**:Berkeley RDI 2026-04 证主流 benchmark 普遍可刷分(`/trustworthy-benchmarks-cont/` 篇 8/8;另一篇 `/trustworthy-benchmarks/` 审计 13 个 benchmark、确认 45 处 hack——**两次不同审计,非「13 取代 8」**);o3 30% reward-hacking(原始出处 **METR** 2025-06,RDI 系转引)。没隔离的 eval = 虚假安全感。
3. **适用规模**:全套回报随 多人+生产+长期维护 上升。纯 solo/原型,正式 eval 降级为 tracing+人工抽检;但 **day-0 硬护栏 + evaluator 隔离对 solo 同样不可省**。

## 各家流程命名对照(证明这是综合,非「唯一真理」)

| 来源 | 怎么分 |
|---|---|
| OpenAI | 无命名生命周期;Model/Tools/Instructions + Guardrails + run loop + 决策门 |
| Google ADK | Build → Evaluate → Deploy(+ Observability/Safety);循环 Think-Act-Observe |
| LangChain | Build → Test → Deploy → Monitor + 横切 Iterate/Govern |
| Microsoft Foundry | 9 步:选类型→建+测→加工具→版本→tracing→评估→优化→发布→监控迭代 |
| 本流程 | S0–S5(取公共交集 + 把 day-0 护栏/evaluator 隔离前置) |

## 深钻目标(每步要钻到「照着能做」)

后续按 S0→S5(或按需先挑)逐步深钻,目标颗粒度 = **具体命令 / 模板 / 配置 / 坑**,到执行层为止。
Phase 2 已采集的该层素材(知识保鲜接入、任务拆分模板、上下文文件体系、hook/subagent 配置、eval 8 步、权限/护栏配置)已**抢救性落盘到 `details/d1`–`d6`(草稿,未套本轮 eval 修正)**。深钻每一步时:以本 flow.md 为准 → 重核时效 → 用 subagent 对抗 eval → 通过后提炼为正式 `details/SX-*.md`。

### 步 → 底料草稿 正向索引(深钻时按此取料)
> ⚠️ 文件名 `d1`–`d6` **不**对应 `S1`–`S6`(d1=知识保鲜=横切,不是 S1)。**按下表取料,别按文件名直觉。**

| 流程步 | 取哪几份 details 草稿 | 备注 |
|---|---|---|
| **S0 判断/从简** | **⚠️ 暂无 details 草稿** | 从 flow.md S0 行 + `sources.md` A 段(OpenAI Practical Guide / building-effective-agents / Husain)+ I 段起 |
| **S1 选型/编排** | d2(规划侧)+ d6(单 vs 多 agent) | — |
| **S2 设计零件** | d1 + d2 + d3 + d6(day-0 护栏) | **最重的一步,底料最散,最易漏** |
| **S3 实现** | d3(上下文文件)+ d4(实现/hooks) | — |
| **S4 观测+eval** | d5 | — |
| **S5 上线+运营** | d6(护栏/权限/部署) | — |
| 横切(知识保鲜/护栏) | d1 / d6 | 贯穿多步 |

## 方法约束(每步深钻都要遵守)
- 证据必须**实时(优先 2026)**、标 **独立 vs 厂商自报**、拿不准标 **unverified**。
- 先从一手源筛证据 → 再用 **subagent 对抗 eval**(查时效/正确性/跨厂商/实践边界)→ **通过才采纳**。

## ⛔ 别再引入的说法(被对抗 eval 打回,完整清单见 `sources.md` 末「已被打回」段)
- 「eval 先行(写 prompt 前先建完整 eval)」→ 实为贯穿、early & continuous(被 LangChain/Husain 反对)。
- 「多 agent 是默认」→ 单 agent 强默认,多 agent 仅严格触发。
- 「gather→act→verify 是开发的一步」→ 它是运行时循环(ReAct/Think-Act-Observe)。
- 其它(Cursor 12.5%、Codex 五阶段、RAG 已死、hook exit 1 阻断…)见 sources.md。
