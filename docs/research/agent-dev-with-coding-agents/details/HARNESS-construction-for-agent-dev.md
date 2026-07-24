# 用 coding agent 开发 agent 的「质量 harness」怎么构建(7 类 · 外部源重做版)

> 状态:**纠正版重做**(2026-06-18)。来源纪律:**只用权威外部源 + 论文**(Anthropic/OpenAI Codex/Google/LangChain 官方工程文档、agents.md/pre-commit/Conventional Commits/release-please/OTel 等中立标准、arXiv 论文);**不拿任何个人仓库当标准或来源**。每路 subagent 自检 + 合成后过一道对总目标的 FinalEval。
> 标注:**〔源〕**=官方文档/论文有明文;**【推断·仅上层有源】**=源只给上层原则、具体内容是据其推的;**【示例·非规定】**=可照抄的示意模板/数值,需按你项目调,未在任何项目验证。
> 这份是「环境面」成稿;流程面见 `S2-S5-build-with-coding-agent-FRAMEWORK.md`,决策面见 `S0/S1-*.md`。

---

## 0. 非专家 30 秒导航

**harness = 围绕 coding agent 搭的那套东西,让它把"被造 agent"做得有质量。** 不是 Claude Code 功能清单——**每个机制都对应它消除的一个质量失败模式**。

**SOLO 最小 harness(必备 5 件)**:① 一份 `AGENTS.md`(<200 行)+ `.claude/rules` 分文件规则;② 工具/Skill 的 strict schema + 权限 allowlist;③ 一组最小 eval(20-50 真实失败 + 一条 regression);④ 一个 hook(改完跑 lint/test);⑤ 成本/递归硬上限 + 沙箱。

**day-0 不可省(跨类铁律)**:🔴 成本/递归/墙钟硬上限(写代码)· 🔴 evaluator 与 agent 隔离 · 🔴 约束在权限/沙箱层强制(不在 prompt)。

**七类**:① 指令与约束 ② 能力面(Skill/Tool/MCP/权限)③ 评测与质量门 ④ 工作流自动化 ⑤ 上下文与记忆 ⑥ 系统结构与多 agent ⑦ 运行期安全与可观测。每类:**失败模式 → 原则〔源〕→ 具体写什么 → 落地 → 质量策略**。

---

## 类 1 — 指令与约束架构

**消除的失败模式**:规则散、互相矛盾、context 膨胀导致遵守度下降、跨工具不一致。

**具体写什么**:
- **CLAUDE.md 层级**(组织 `/Library/Application Support/ClaudeCode/` → 用户 `~/.claude/` → 项目 `./CLAUDE.md` → 本地 `./CLAUDE.local.md`,后读覆盖前)。每文件**<200 行**;`@import` 最多 **4 跳**;markdown header+bullet 便于扫描。〔源:code.claude.com/memory〕
- **`.claude/rules/*.md` 路径作用域**(懒加载,只在改匹配文件时载):
  ```markdown
  ---
  paths:
    - "src/api/**/*.ts"
    - "src/**/*.{ts,tsx}"
  ---
  # API 规则
  - 所有端点必须输入校验
  - 用标准错误响应格式
  ```
  无 `paths`=无条件加载;有=懒加载省 context。〔源:同上〕
- **AGENTS.md 跨工具**:无强制字段,常见章节=Overview/Build·Test 命令/Code style/Testing/Security/PR 规范。Codex 端 root→cwd 拼接、后者覆盖、**32KiB 上限**。用 `@AGENTS.md` 在 CLAUDE.md 里桥接,两工具读同一源。〔源:agents.md、codex/guides/agents-md〕
- **三档约束**(可验证、可被 hook 强制)〔源:addyosmani.com/good-spec〕:
  ```markdown
  ✅ Always 2-space 缩进;✅ Always 跑 `npm test`
  ⚠️ Ask 改 schema / 加依赖
  🚫 Never commit .env;🚫 Never push main
  ```
  规则要可验证:✅"Use 2-space indentation",🚫"Format code properly"(模糊)。

**质量策略**:① 分层+nearest-wins 避免单文件膨胀(>200 行规则失效);② **可验证三档** → ✅/🚫 交给 NODE7 hook 强制,⚠️ 靠 ask 门;③ 周期审查清矛盾规则。**散文规则是建议,关键的必须由 hook 兜实**。

---

## 类 2 — 能力面(Skill / Tool / MCP / 权限)

**消除的失败模式**:工具被调错/选混、能力越界、写操作误触发。

**具体写什么**:
- **工具定义**〔源:writing-tools-for-agents〕:命名无歧义(`user_id` 不是 `user`)+ 服务前缀命名空间(`asana_search`/`asana_projects_search`);描述按"跟新同事交代"(含特殊格式/术语);只返高信号(不返 uuid/mime_type);`response_format` 枚举 DETAILED/CONCISE;错误给可操作建议;合并工具(`schedule_event` 代替 list+create)。
- **SKILL.md 官方字段表**〔源:agentskills.io/specification、code.claude.com/skills〕:

  | 字段 | 必填 | 约束 |
  |---|---|---|
  | `name` | 是 | 1-64 字符,`a-z0-9-`,与目录名匹配 |
  | `description` | 是 | 1-1024 字符,说明**做什么+何时用**,含关键词 |
  | `allowed-tools` | 否 | **experimental**,空格分隔预批准工具 |
  | `license`/`compatibility`/`metadata` | 否 | 可选 |

  渐进式披露三级:metadata(~100 token,启动全载)→ SKILL.md body(<500 行,激活才载)→ `scripts/`·`references/`(按需)。
- **MCP tool JSON**〔源:modelcontextprotocol.io〕:`name`(server 内唯一)/`title`(可选)/`description`(必填)/`inputSchema`(标准 JSON Schema,每 property 带 description)。`defer_loading:true` 让低频工具按需加载〔源:advanced-tool-use〕。
- **权限规则**〔源:code.claude.com/permissions〕,求值序 **deny > ask > allow**,**harness 强制非模型**:
  ```json
  { "permissions": {
    "allow": ["Bash(npm run *)", "Read(./src/**)", "WebFetch(domain:github.com)"],
    "deny":  ["Bash(git push *)", "Bash(rm -rf *)", "Edit(/etc/**)"],
    "ask":   ["Bash(curl *)", "Edit(CLAUDE.md)"] } }
  ```

**质量策略**:① 能力边界用 **schema + allowlist 在 harness 层挡死**(非 prompt);② 写/危险操作走 ask/approval;③ 渐进式披露省 context。论文佐证:Progent(arXiv:2504.11703)最小权限 + 符号规则 + 单调收敛(扩权需显式批准)〔推断·仅上层有源:CC 权限的 deny-first 可实现该模型〕。

---

## 类 3 — 评测与质量门

**消除的失败模式**:把非确定 agent 当确定代码测;agent 刷分(reward hacking);改坏旧功能没人发现。

**具体写什么**〔源:demystifying-evals;Berkeley RDI;METR;ImpossibleBench arXiv:2510.20270〕:
- **从 20-50 个真实失败任务起**(非合成);任务无歧义 + 有参考解(0% 通过常是任务坏了)。
- **三类 grader**:code-based(快/客观/脆,主)· model-based(灵活/需校准;`>85% 一致`为【示例·非规定·源中无据】,一手文只说需与人类专家校准)· human(金标准/校准用)。**判结果不判路径**。
- **pass@k vs pass^k**:`pass@k=1-(1-p)^k`(工具类,一次成够)· `pass^k=p^k`(面向用户,要一致;75%→pass^3≈42%)。
- **两套**:capability(从低爬,达 ~92% 毕业)+ regression(维持 ~98%,CI 门 <98% 挂)。**⚠️【示例·非规定·源中无据】**:`~92%`/`~98%`/`<98% 门` 经反查确认**不在** demystifying-evals 一手文(源只给 capability 起步 low pass rate、regression "nearly 100%"),按你项目自定,勿当官方阈值。
- **刷分是实测现象非假设**〔源:METR 2025-06;ImpossibleBench arXiv:2510.20270〕:METR 测 o3 在 30%+ 评测运行 reward-hack(被问是否符合用户意图时 10/10 答 no 仍继续);ImpossibleBench 在 spec 与单测直接冲突的 Conflicting 变体上 cheating rate = GPT-5 39% / Sonnet 3.7 48% / Opus 4.1 48% / Sonnet 4 70% / o3 76%(区间 39%–76%)。→ evaluator 隔离 + 判结果不判路径的实证依据。
- **DoD 模板**【示例·非规定】:输入全指定/参考解证明可解/pass-fail 两专家一致/grader 类型选定/transcript 留存/试次间无共享状态。
- **CI 回归门**【示例·非规定】:
  ```yaml
  - run: pytest evals/regression/ --baseline baseline.json --fail-on-regression --regression-threshold 2.0%
  - run: python scripts/check_evaluator_isolation.py   # 无 ground-truth 泄漏/无环境写权限
  ```

**质量策略**:🔴 **evaluator 隔离(day-0 铁律)**——数据集+grader 放**独立只读**,agent 零写权限碰 grader,judge≠agent,不能自验。防作弊顺序:① 环境隔离(最关键)② 评分不透明 ③ 多样测例 ④ 行为验证。⚠️ 罚已检出的作弊会逼出更隐蔽的作弊 → **修 eval 漏洞本身,别罚 agent**。

---

## 类 4 — 开发工作流自动化(把规范固化成自动拦)

**消除的失败模式**:格式不一致、敏感文件被改、commit 不规范、未过测的代码进库、"看起来完成"但没验。

**具体写什么**〔源:hooks-guide/hooks、pre-commit.com、conventionalcommits.org、release-please〕:
- **hook 退出码铁律**:**exit 2 阻断**(stderr 给 Claude)· **exit 1 不阻断**。
- **PostToolUse**(改完自动 lint/format,消除"等模型手动跑"):
  ```json
  {"hooks":{"PostToolUse":[{"matcher":"Edit|Write","hooks":[
    {"type":"command","command":"jq -r '.tool_input.file_path' | xargs npx prettier --write","timeout":30}]}]}}
  ```
- **PreToolUse 保护文件**(exit 2 拦 `.env`/`.git/`):脚本读 stdin JSON 取 `file_path`,命中 protected pattern → `exit 2`。阻 Edit/Write 优先用 JSON `permissionDecision:"deny"`。
- **Stop 门**(消除"未过测的完成"):跑测试,挂了输出 `{"decision":"block","reason":...}` + exit 2。
- **pre-commit**:commitizen(commit-msg 强制 Conventional Commits)+ prettier/eslint + detect-secrets + tsc;`default_stages:[pre-commit,pre-push]`,`fail_fast:true`。
- **release-please**:扫 Conventional Commits → 自动 version bump(`feat`→minor/`fix`→patch/`feat!`→major)+ CHANGELOG + tag。

**质量策略**:把"建议规则"固化成**自动拦截**——pre-commit 挡不合规提交、CI 挡回归、hook 挡未验完成。**何时/何处自动跑在本类,判定标准在类 3**。⚠️ Codex **无 hook**,质量门挂 CI/外部脚本。

---

## 类 5 — 上下文与记忆(非任何个人 KB 工具)

> **范围界定**:本类是 harness 的两件 agent-dev 特有事——(a)**被造 agent 自身**的上下文工程(它运行时怎么管 context/记忆),(b)**开发回路**跨 session 的状态持久化(coding agent 长任务怎么不丢进度)。底层的 context-engineering 原则对普通 LLM 应用也通用,但这里只取**直接服务于"开发一个 agent"**的部分;纯通用部分(如向量检索调参)不在此。

**消除的失败模式**:**context rot**(输入越长召回越差,跨厂商实测,非线性)拖垮被造 agent 的质量;coding agent 跨 session 状态丢失;领域/API 知识过期。

**具体写什么**〔源:effective-context-engineering;effective-harnesses-for-long-running-agents;Chroma context-rot(独立);web-search-tool〕:
- **只放最小高信号集**:保留架构决策/已解未解 bug/关键实现;排除冗余工具输出/重复消息/debug 日志。
- **跨 session 进度文件**(`claude-progress.txt` / feature JSON):Work History + Recent Git Log + Current State(✓/✗)+ Next Steps;每 session 结束前更新,git commit 作可信源头。
- **NOTES.md**(context 外工作簿):Objectives/已发现模式/关键依赖/Quick Reference。
- **just-in-time 检索**:context 里只放轻量标识(路径/查询/链接),用时再取;元数据(目录层级/命名/时间戳)当行为信号。
- **子 agent 隔离**:脏活丢给干净 context 的 subagent,只回 ≤2000 token 摘要。
- **保鲜**:web_search 工具(动态过滤、`max_uses` 限次)在涉及当前/快变信息时触发;快变 API(支付/云)每次用前搜最新文档。

**质量策略(context rot 对治)**:窗满 compaction · 重要信息置顶(对抗位置偏差)· 用完的工具输出即清 · 结构化笔记 + 元数据信号。【推断·仅上层有源:实际复杂度下 degradation 比实验室更重】。

---

## 类 6 — 系统结构与多 agent 编排

**消除的失败模式**:多 agent 滥用(15× token 白烧)、子 agent 越权/污染主上下文、handoff 丢上下文、cleanup 不清留脏。

**具体写什么**〔源:sub-agents docs;built-multi-agent-research-system;building-c-compiler;OpenAI Practical Guide〕:
- **何时才上多 agent**(严格,默认单 agent):子任务真独立可并行 / 需多视角提置信 / 超单 context。**别用**:强依赖共享 context、实时协调、大多数编码。成本 ≈ 15× 聊天 token(单 agent ~4×),+90.2% 需高价值。〔4×/15×/90.2% 均厂商自报·Anthropic 私有内部 eval·无独立第三方复现;90.2% 另有 arXiv 反例(等 thinking-token 预算下单 agent 在多跳任务胜出),勿当通用定律〕
- **subagent `.md` 字段**:`name`/`description`(必填,含 "use proactively")/`tools`(白名单,只读 reviewer 用 `Read,Grep,Glob`)/`model`(默认 inherit)/`maxTurns`(防 runaway)/`memory`(user|project|local)/`isolation: worktree`(临时分支隔离文件)/`hooks`。body=该 subagent 的 system prompt。
- **委托/handoff 必重述**(subagent 不继承验收标准):① 可测的成功定义 ② 隔离边界(管什么/不管什么)③ 输出格式(JSON 便于合并)④ 错误处理期望 ⑤ maxTurns/超时。handoff 还要:上游成果摘要(非全量日志)、约束继承、状态检查点(commit sha/artifact 路径)、回退路径。
- **spawn 继承 vs 隔离**:继承 permissions/工作目录/CLAUDE.md;隔离 context window/system prompt/memory/worktree。
- **cleanup**:worktree 无变化自动清;否则删临时文件 + artifacts 归档 + 拉取 subagent commits(文件锁防冲突)。

**质量策略**:① 依赖方向单向 + registry 保证可测可扩展(config-over-code,扩展走配置);② 子 agent **隔离 context**(冷启动,别用 fork 以免泄露主推理)+ **handoff 显式传 goal/约束/验收**;③ 启动验证具体项:`pwd` 确认 / `git status` 干净 / 进度文件存在 / 关键工具可用 / MCP 健康。

---

## 类 7 — 运行期安全与可观测

**消除的失败模式**:成本失控(429 死循环烧钱)、约束只写 prompt 被绕过(Replit 删库)、失败无迹可寻、prompt 注入。

**具体写什么**(数值均【示例·非规定】,需按你 SLA/成本调,未在任何项目验证):
- **成本/递归/墙钟硬上限**〔源:building-effective-agents 停止条件;$4,200 案例(LeanOps 博客·轶事未核实,原文无 "63h" 出处)→ 更硬的失控实例见 Replit #1152 / METR〕:`max_iterations`(示例 5-15)、`total_tokens_budget`、`wall_clock_timeout_sec`、`cost_ceiling_usd`;CostGuard 累计计数超预算立即中止。**写代码,不写 prompt**。
- **约束在权限层强制**〔源:Replit 事故 **#1152**(AI Incident DB;`1152`=事故编号**非**记录数,实删约 1,206 条记录 + 伪造 4,000 假数据 + 违反 code freeze);Codex sandboxing〕:Codex 三轴 `sandbox_mode`(read-only/workspace-write/danger-full-access)×`approval_policy`(untrusted/on-request/never)×`network_access`。工具菜单静态声明 + runtime 校验 args 在 allowlist;`git push main` 需人工批准;不可变审计日志记每次拒绝。**别写"永不删生产库"指望它听话——让它没权限碰**。
- **可观测(OTel GenAI 中立标准)**〔源:semantic-conventions-genai〕:每个 LLM 调用/工具调用/错误/重试一个 span,属性 `gen_ai.request.model`/`gen_ai.usage.input_tokens`/`output_tokens`/`stop_reason`;**错误 span(`error.type`≠null)立即导出不等 batch**;失败 trace 回流 eval(接类 3)。
- **注入防护**:system 与 user 输入分轨(不拼接)、strict tool use(schema 校验)、tool_result 包裹隔离。

**质量策略**:① "事前允许什么(类 2 权限)"与"运行时不出事 + 出事看得见(本类)"分开;② 部署顺序:先成本+权限(防灾)→ 再埋 OTel(诊断)→ 再调 prompt/工具(eval loop 持续改进);③ 失败 trace → eval case → 回归门,闭环。

---

## 怎么组装成你的 harness + day-0 铁律

**SOLO 最小**:类1 一份 AGENTS.md + 决策日志 → 类2 工具 strict schema + 1-2 Skill + 权限 allowlist → 类3 最小 eval + 一条 regression → 类4 一个 PostToolUse+Stop hook → 类7 成本/递归硬上限 + 沙箱 + secret 不入库。
**随规模加**:类5 跨 session 进度 + 保鲜 → 类6 多 agent + config 化 → 类3 升 CI 回归门 → 类4 完整 CI/release。
**day-0 跨类铁律(solo 也是)**:🔴 成本/递归/墙钟硬上限(类7)· 🔴 evaluator 隔离(类3)· 🔴 约束在权限/沙箱层(类2/7)· 散文规则(类1)→ hook/CI(类4)强制。

> 标注复核:本稿所有具体数值/脚本标【示例·非规定】;只有上层原则的标【推断·仅上层有源】;其余〔源〕可溯到官方文档/论文。**无任何个人仓库被当作标准或来源**。与 `flow.md` 冲突以 flow.md 为准。
