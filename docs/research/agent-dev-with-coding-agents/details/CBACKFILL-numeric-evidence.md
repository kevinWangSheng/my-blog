# 簇 C 回填清单 — `HARNESS-construction-for-agent-dev.md` 数值证据核查

> 用途:人工回填到 `HARNESS-construction-for-agent-dev.md`(及个别跨文件到 `flow.md` / `sources.md`)。
> 来源:本研究 workflow 簇 C(数值证据核查),过对抗 eval(verdict=pass,跨厂商/正确性/时效均 ok)。
> **本清单不自动改正式稿**:`HARNESS-construction-for-agent-dev.md` 与 `flow.md` 是正式/锁定稿,回填动作需 human 逐条确认。
> 标注约定:**〔源〕**=官方/论文明文;**【示例·非规定】**=可照抄示意数,按项目自定;**unverified**=经反查无一手据。

---

## FinalEval 附加修正(整体评审在簇 C 之上又抓到的口径问题,回填前必看)

1. **C1 不是简单替换**:`flow.md` 现写「8/8 主流 benchmark 可被刷分」来自 RDI 的 **`/blog/trustworthy-benchmarks-cont/`(8 benchmark)**;簇 C 引的「13 benchmark / 45 confirmed hacks」来自 RDI **另一篇 `/blog/trustworthy-benchmarks/`**。两篇是**两次不同审计**,FinalEval 已独立 WebFetch 核实两页都真实、各自数字正确。回填 flow.md 时**必须注明这是另一批 benchmark / 另一篇 RDI 文,不是「13 取代 8」**,并同步在 `sources.md` 增列 `/trustworthy-benchmarks/`(非 -cont)这条一手源。
2. **A9 变体口径**:本清单 ImpossibleBench `GPT-5=39%` 是 **Conflicting 变体**;`sources.md` L81 的 `GPT-5=76%` 是另一子集。回填时**显式标变体口径**,否则与 sources.md 自相矛盾。
3. **eval 数值修正已应用**:ImpossibleBench `Opus 4.1=48%`(非 54%),`Sonnet 3.7=48%`,区间 39%–76% 不变。
4. **$4,200/63h 降级**:与 `sources.md`「已被打回」第 9 条方向一致,建议落实替换为更硬例子(Replit#1152 / METR / ImpossibleBench)。

---

## A. 可去【示例·非规定】标 / 已确认〔源〕(有一手硬证据)

| # | doc 位置 | 现有带数字断言 | 找到的硬证据(来源 + 数值) | 来源类型 | 建议动作 |
|---|---|---|---|---|---|
| A1 | 类3 · L88 | `pass^k=p^k`;`75%→pass^3≈42%` | Anthropic *Demystifying evals*(2026-01-09)逐字:`(0.75)³ ≈ 42%` | 厂商自报(方法论) | 可视为官方原文,标〔源〕 |
| A2 | 类1·L13 / 类3·L86 | `20-50 真实失败起步` | 同篇逐字:`20-50 simple tasks drawn from real failures is a great start` | 厂商自报 | 去【示例】嫌疑,标〔源〕 |
| A3 | 类6 · L144 | `≈15× 聊天 token`、`单 agent ~4×` | Anthropic *multi-agent research system*(2025-06)逐字:`agents ~4× more tokens... multi-agent ~15× more tokens than chats` | 厂商自报·私有内部 eval | 可去【示例】,**必加注**:`厂商自报·私有内部 eval·无独立第三方复现` |
| A4 | 类6 · L144 | `+90.2%`(多 agent 优于单) | 同篇:内部 research eval 高 **90.2%**;BrowseComp token 解释 **80%** 方差,三因素合计 **95%** | 厂商自报·私有 eval | 可去【示例】,**必加注**私有-eval 警示 + 存在 arXiv 反例,不当通用结论 |
| A5 | 类1 · L26 | `每文件 <200 行`、`@import 最多 4 跳` | CC memory 官方文档逐字:`target under 200 lines`、`maximum depth of four hops` | 厂商自报 | 保持〔源〕;排除第三方「5 hops」噪音 |
| A6 | 类1·L39 / 类7·L160 | Codex AGENTS.md `32KiB 上限` | OpenAI Codex 官方指南 + issue #7138:`PROJECT_DOC_MAX_BYTES = 32*1024` | 厂商自报(文档+仓库 issue) | 保持〔源〕;**eval 未本轮重抓**,去标前 spot-check #7138 |
| A7 | 类2 · L60-63 | SKILL.md `name 1-64`、`description 1-1024` | 官方 Agent Skills:name ≤64 仅 `a-z0-9-`;description 非空 ≤1024 | 厂商自报 | 保持〔源〕;**eval 未本轮重抓**,去标前 spot-check 官方页 |
| A8 | 类3·防作弊 / flow.md | `o3 30% reward-hacking` | METR(2025-06-05):o3 与 Claude 3.7 Sonnet 在 30%+ 评测运行 reward-hack;问意图 10/10 答 no 仍继续 | 独立第三方 | 标〔源:METR〕;**归因修正**:RDI 的 o3 30% 系转引 METR,出处改标 METR |
| A9 | 类3 · L85 | `ImpossibleBench`(原仅列编号) | cheating rate(Conflicting 变体):GPT-5 **39%**、Sonnet 3.7 **48%**、**Opus 4.1 48%**、Sonnet 4 **70%**、o3 **76%** | 论文(有官方实现) | 升级为带区间 **39%–76%**。⚠️ **Opus 4.1=48%(非 54%)**,标变体口径 |
| A10 | 类7 · L156, L160 | `Replit 删库`、`Replit 1152` | AI Incident DB **#1152**;多家独立媒体:删约 **1,206** 条记录、伪造 4,000 假数据、违反冻结 | 独立第三方(编目+媒体) | 保持〔源〕。**口径**:`1152`=事故编号,**非**记录数(记录数 1,206) |
| A11 | 类2 · L77 | `Progent` 最小权限 + 0% | Progent(arXiv:2504.11703):DSL 策略 + 逐调用校验,AgentDojo/ASB/AgentPoison 上 ASR 降到 **0%** | 论文 | 0% 可标〔源〕;**保留**doc 现有【推断·仅上层有源】(CC 权限实现 Progent 模型属推断);**eval 未本轮重抓 0%** |

---

## B. 仍无硬证据 → 保留【示例·非规定】+ unverified(反查确认源中无据,不可去标)

| # | doc 位置 | 带数字断言 | 反查结论 | 动作 |
|---|---|---|---|---|
| B1 | 类3 · L89 | `capability ~92% 毕业` | Anthropic evals 一手文**无此数**;只给 capability `low pass rate`(SWE-bench 起于 30%)定性 | 保留【示例】+ unverified,**不可去标** |
| B2 | 类3 · L89 | `regression ~98%`、`CI 门 <98% 挂` | 源只说 regression `nearly 100% pass rate`;**未给 98%** | 保留【示例】+ unverified |
| B3 | 类3 · L93 | `--regression-threshold 2.0%` | 源中**无 2.0%** 任何表述 | 保留【示例】+ unverified |
| B4 | 类3 · L87 | `model-based grader >85% 一致` | 源只说需与人类专家校准,**未给 85%** | 保留【示例】+ unverified |
| B5 | 类7 · L159 | `$4,200/63h` | 唯一来源 LeanOps 弱博客,原文只说 `$4,200 in API fees over a long weekend`——**无 63h、无一手出处、厂商客户轶事** | 保留 unverified;降级为轶事或**替换**(Replit#1152 / METR / ImpossibleBench) |

> B1–B4 是本簇最重要护栏:`92% / 98% / 2.0% / 85%` 四个阈值经独立重抓确认**全部不在** Anthropic evals 一手文中。它们是示意数,按项目自定。

---

## C. 口径修正(回写 flow.md / 跨文件)

| # | 位置 | 现有写法 | 一手证据 | 动作 |
|---|---|---|---|---|
| C1 | flow.md | `8/8 主流 benchmark 可被刷分`(来自 RDI `-cont` 篇,8 benchmark) | RDI `/trustworthy-benchmarks/`(另一篇)审计 **13 benchmark**、**45 confirmed hacks**(Frontier-CS 100/100、WebArena 零浏览满分等) | **不是替换**:补注「另一篇 RDI 文 / 另一批 benchmark」,两篇都真实;sources.md 增列该篇一手源 |
| C2 | flow.md / 类3 | `o3 30%` 归因 Berkeley RDI | RDI 原文 `METR found that o3 and Claude 3.7 Sonnet reward-hack in 30%+...`,系转引 METR | 归因改标 **METR**(见 A8) |

---

## D. 越界 / 留作他簇(本簇不处理)

| # | 位置 | 事项 | 说明 |
|---|---|---|---|
| D1 | flow.md | `Isolate the agent from the evaluator. Non-negotiable` 归因 RDI | 该逐字短语**不在** RDI 博客(最接近 `Run evaluator and submission in separate containers with no shared state`)→ 散文/归因问题,路由散文簇 |
| D2 | 类7 · L161 | OTel GenAI 属性名拼写 | 中立标准非数值,留作他簇 |

---

## 来源索引(一手 URL)

| 标签 | 来源 | URL | 日期 | 类型 |
|---|---|---|---|---|
| Anthropic-multiagent | How we built our multi-agent research system | https://www.anthropic.com/engineering/built-multi-agent-research-system | 2025-06 | 厂商 |
| Anthropic-evals | Demystifying evals for AI agents | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-01-09 | 厂商 |
| METR | Recent Frontier Models Are Reward Hacking | https://metr.org/blog/2025-06-05-recent-reward-hacking/ | 2025-06-05 | 独立 |
| RDI | Trustworthy Benchmarks(13 benchmark 篇) | https://rdi.berkeley.edu/blog/trustworthy-benchmarks/ | 2026-04 | 独立 |
| RDI-cont | Trustworthy Benchmarks cont(8 benchmark 篇,flow.md 现引) | https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/ | 2026 | 独立 |
| ImpossibleBench | arXiv:2510.20270 + 官方实现 | https://arxiv.org/abs/2510.20270 / https://github.com/safety-research/impossiblebench | 2025-10 | 论文 |
| Replit-1152 | AI Incident Database #1152 | https://incidentdatabase.ai/cite/1152/ | 2025-07 | 独立 |
| Codex-AGENTS | AGENTS.md 指南 + issue #7138 | https://developers.openai.com/codex/guides/agents-md / https://github.com/openai/codex/issues/7138 | 2026 | 厂商 |
| CC-memory | Claude Code memory | https://code.claude.com/docs/en/memory | 2026-06(抓取日) | 厂商 |
| CC-skills | Agent Skills best practices | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | 2026 | 厂商 |
| Progent | arXiv:2504.11703 | https://arxiv.org/abs/2504.11703 | 2025-04 | 论文 |

---

## 回填前必做 spot-check(eval 未本轮重抓,去标前验证)

1. **A6 Codex 32KiB**:依赖精确 `32768 bytes` 时对照 live 官方文档 + issue #7138。
2. **A7 SKILL.md 64/1024**:去【示例】前对照 live 官方 Agent Skills best-practices 页。
3. **A11 Progent 0% ASR**:去标前对照 arXiv:2504.11703。

> A1–A5、A8–A10、B1–B5、C1–C2 已逐字/独立复核,可按建议动作回填;A6/A7/A11 需先 spot-check。
