# 研究:用 coding agent 开发 agent 应用

个人学习型研究。目标:搞懂「个人开发者用 coding agent(Claude Code/Codex/Cursor)开发一个 AI agent 应用」的**完整流程**,并逐步钻到**执行层(具体怎么做)** 全部搞懂。

## 当前状态
- **Phase 1 宏观流程**:✅ 已确认,经 4 路对抗 eval 修订通过 → 见 `flow.md`。
- **Phase 2 逐步深钻(到执行层)**:🔜 进行中。已采集的执行层素材**已落盘 `details/d1`–`d6`(草稿,未套 eval 修正)**;深钻各步时套修正 + 重核时效 + 对抗 eval 后,提炼为正式 `details/SX-*.md`。
  - ✅ **S0 已完成**:`details/S0-decide-and-simplify.md`(2026-06-17,过对抗 eval;四家跨厂商佐证 + 决策程序 + 坑 + solo 边界)。
  - ✅ **S1 已完成**:`details/S1-selection-and-orchestration.md`(2026-06-17,过对抗 eval;三子决策=单vs多agent/框架vs手写/部署载体,含 2026 框架格局 + 弃用日期)。
  - ✅ **S2–S5 + 横切 已合成**:`details/S2-S5-build-with-coding-agent-FRAMEWORK.md`(2026-06-17;33-agent 完整性 workflow 找缺口→补→复审,4 残口补齐;按节点到操作底,〔源〕/【推断】标注,含 MCP-server 与 SKILL.md 端到端范例 + Claude Code↔Codex 映射 + 30 秒非专家导航)。
  - ✅ **harness 构建指南(外部源重做版)**:`details/HARNESS-construction-for-agent-dev.md`(2026-06-18;主控派发 7 路定向抓取**只用外部权威源+论文、不碰个人仓库**→我合成→FinalEval 对总目标自检)。**7 类 harness 构件**=指令架构/能力面(Skill·Tool·MCP·权限)/评测门/工作流自动化/上下文记忆/系统结构与多agent/运行期安全可观测;每类「失败模式→原则〔源〕→具体写什么(字段表/模板/配置)→落地→质量策略」,数值标【示例·非规定】。**注**:前一版因 subagent 误读本地仓库当标准被 FinalEval 判不达标,已弃,本版为纠正重做。

## 文件
- `flow.md` — 流程正本(eval 通过版),后续深钻的锚;末尾有「别再引入的说法」。
- `sources.md` — 全部引用来源(分 9 类 A–I,标源类型/日期/边界;末段「已被打回」清单)。
- `details/` — Phase 2 执行层素材:`_README.md` + `d1`–`d6`(草稿,未套 eval 修正);深钻后提炼为正式 `SX-*.md`。
- `details/HARNESS-construction-for-agent-dev.md` — 7 类 harness 框架(外部源重做版,过 eval)。
- `details/CASES-agent-dev-fieldnotes.md` — **工程实录 + 反例**(2026-06-20,4 簇 workflow 产出,每簇过对抗 eval + 整体 FinalEval pass)。补 HARNESS 框架缺的「真实案例」层;每案标 harness 类号 + 独立/厂商 + 覆盖诚实声明。
- `details/HARNESS-freshness-fast-moving.md` — **快变下 harness 怎么保持有效**(同上 workflow);核心是稳定层 vs 易变层划分 + 每个易变点的 pin/保鲜实践 + solo 最小保鲜回路。
- `details/CBACKFILL-numeric-evidence.md` — **簇 C 数值证据核查回填清单**(供人工回填 `HARNESS-construction-*.md` / `flow.md`,**未自动改正式稿**)。确认 `92%/98%/2.0%/85%` 四阈值确无一手据(保留 unverified);A 段可去标、C 段跨文件口径修正待 human 批。

## 方法约束(贯穿)
1. 证据实时优先 2026;标 独立 vs 厂商自报;拿不准标 unverified。
2. 流程:先从一手源筛证据 → subagent 对抗 eval(时效/正确性/跨厂商/实践边界)→ 通过才采纳。
3. eval 边界三铁律:eval-driven 是应然非现状;eval 须 evaluator 隔离;solo 与生产适用规模不同(见 flow.md)。

## 深钻计划(逐步)
按 `flow.md` 的 S0→S5 一步一会话深入(也可按需挑步)。每步产出:做什么 → 具体怎么做(命令/模板/配置)→ 坑 → 边界,落 `details/SX-*.md`,每条带证据。
**每步该取哪几份 `d1`–`d6` 草稿,见 flow.md「步 → 底料草稿 正向索引」**(注意:d1–d6 不对应 S1–S6;**S0 暂无草稿**,从 flow.md S0 行 + sources A/I 段起)。

## 新会话续接(可直接粘贴)
> 我在继续「用 coding agent 开发 agent 应用」的研究。**先读 `docs/research/agent-dev-with-coding-agents/flow.md` 全文 + `sources.md` 末「已被打回」段 + `details/` 对应草稿**,再动手。现在深钻 **S<n>**(合法步号 S0–S5,步名见 flow.md 流程图),钻到「照着能做」(命令/模板/配置/坑)。方法照旧:先从一手源筛证据,再用 subagent 对抗 eval(查时效/正确性/跨厂商/实践边界),通过才给我;证据要实时(2026)、标独立 vs 厂商、标 unverified;产出落 `details/S<n>-*.md`(目录已存在,内有 d1–d6 草稿可作底料)。

## 待办 / 开放项
- [x] **S0 判断/从简**——已落 `details/S0-decide-and-simplify.md`(过对抗 eval)。
- [x] **S1 选型/编排**——已落 `details/S1-selection-and-orchestration.md`(过对抗 eval)。
- [ ] 逐步深钻 S2–S5 到执行层(`details/d1`–`d6` 草稿为底料,套 eval 修正 + 重核时效 → 提炼 `SX-*.md`)。
- [ ] 仍 unverified:「用 coding agent 写 agent vs 手写」的比例(2026 无硬数据)。
- [ ] 可选:2026 术语小词典(context engineering / ReAct / eval-driven / Skills / harness)。
