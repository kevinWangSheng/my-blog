# 来源登记表:用 coding agent 开发 agent 应用(研究引用)

> 主题:开发 AI agent 应用时,用 coding agent(Claude Code / Codex / Cursor)的完整工程链路与每环节做法。
> 本表由多轮 subagent 搜索 + 对抗式交叉验证产出。**源类型** = 评估可信度的关键;**注意/边界** = 引用前必读。
> 标 ★ = 读原文优先级最高(建议「一起读原文」从这些开始)。
> 核对日期:2026-06-15。带版本号/价格/日期的「活动信息」会变,落盘进项目前请复核。

源类型图例:`一手厂商`(官方文档/工程博客,最强)｜`研究`(论文/独立评测机构)｜`实践者`(署名工程师一手)｜`媒体/事故库`(事实层可信、归因层谨慎)｜`二手/SEO`(论证参考,非实测)

---

## A. 端到端流程 / 最佳实践 / 规划方法论

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://code.claude.com/docs/en/best-practices | 一手厂商 | Claude Code 官方四阶段 `Explore→Plan→Implement→Commit`;「给 agent 可自跑的验证把 looks-done 变 pass/fail」;adversarial review;小改跳过 plan | 现行版(旧 URL `anthropic.com/engineering/claude-code-best-practices` 308 重定向到此)。**逐字官方命名**。 |
| ★ https://www.anthropic.com/engineering/building-effective-agents | 一手厂商 | workflow vs agent 区分;护栏/沙箱/停止条件/人类检查点;evaluator-optimizer | 发布 2024-12-19。 |
| ★ https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 一手厂商 | context 是有限资源、context rot、just-in-time 检索、结构化笔记(NOTES.md)、subagent 隔离上下文 | 发布 2025-09-29。 |
| https://developers.openai.com/codex/learn/best-practices | 一手厂商 | Codex「当队友 + definition of done」;Goal/Context/Constraints/Done-when 提示 schema;plan-first | **没有官方「五阶段」命名**——上一轮搜索把它归纳成五阶段是错的,已打回。 |
| https://developers.openai.com/codex/workflows | 一手厂商 | Codex 的 10 个独立任务 recipe | 是任务清单,不是一条命名流程。 |
| https://cursor.com/blog/agent-best-practices ; https://cursor.com/docs/agent/planning | 一手厂商 | Cursor「先规划」+ review + Plan/Agent 模式 | **没有官方「Plan/Build/Review/Verify」四阶段命名**(搜索 agent 自造),已打回。 |
| https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ | 一手厂商 | Spec-Kit:`Specify→Plan→Tasks→Implement`,每阶段产 Markdown artifact | 发布 2025-09-02(作者 GitHub Principal PM)。 |
| ★ https://github.com/github/spec-kit | 一手厂商 | 实际 6 命令 `/speckit.constitution/specify/clarify/plan/tasks/implement`;模板 `templates/spec-template.md`、`tasks-template.md` | 真实链路比「四阶段」重(含 Constitution+Clarify)。README 版本 0.10.2。 |
| https://kiro.dev/blog/introducing-kiro/ | 一手厂商 | Kiro:requirements/design/tasks 三文件 + steering files + 事件 hooks | preview 发布 2025-07-14;2026 GA 日期为二手,未核。 |
| ★ https://addyosmani.com/blog/good-spec/ (亦见 O'Reilly Radar) | 实践者 | 好 spec 六块;spec 里的验证步;✅/⚠️/🚫 三档边界 | 发布 2026-01-13(Addy Osmani,Google Chrome eng lead)。**与你 repo 的 AGENTS.md 三档边界同范式**。 |
| https://github.com/addyosmani/agent-skills | 实践者 | `planning-and-task-breakdown` SKILL:task 模板(Acceptance/Verification/Sizing)、垂直切片、L+ 必拆 | 公开 repo,MIT。 |
| https://simonwillison.net/2025/Sep/30/designing-agentic-loops/ ; /2025/Jun/29/agentic-coding/ ; /2025/Mar/11/using-llms-for-code/ ; /guides/agentic-engineering-patterns/ | 实践者 | agentic loop 抽象;人集中在 setup+最终 review;「没亲眼看它跑过就不算能用」;YOLO+sandbox | Simon Willison,署名一手。 |
| https://www.thoughtworks.com/radar/techniques/spec-driven-development | 二手(半官方评估) | SDD 评级 **Assess**(值得探索带警告);brownfield 用 Spec Kit | 中立第三方,对 SDD 比批评方更正面。 |
| https://marmelab.com/blog/2025/11/12/spec-driven-development-waterfall-strikes-back.html | 实践者(批评立场) | 「SDD=瀑布回归」七条批评(双倍 review、文档膨胀、agent 不遵守 spec) | **单人观点 + 单次实验**;作者自己也让步「新项目/抓 corner case 有用」。别当业界共识。 |

---

## B. 知识保鲜 / 信息检索 / 非确定性

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool | 一手厂商 | 内置实时检索补 cutoff、模型自决、带 citation;参数 `max_uses`/域过滤 | **当前版本 `web_search_20260209`**(旧 `web_search_20250305` 已非最新);dynamic filtering 需同时开 code execution;价格 $10/1000 次为厂商自报。 |
| https://developers.openai.com/codex/config-basic | 一手厂商 | Codex `web_search = cached/live/disabled`,**默认 cached** | cached 可能给过时 SDK 文档,核最新 API 用 `--search`(live)。 |
| https://github.com/upstash/context7 ; https://context7.com/docs/resources/all-clients | 一手厂商 | Context7 MCP:`resolve-library-id`+`query-docs`、版本特定文档;`claude mcp add` 命令 | 性能数字(token -65%/latency -38%)是**厂商自报、无独立验证**。 |
| https://github.com/ref-tools/ref-tools-mcp ; https://docs.ref.tools/context/comparison/context7 | 一手(竞品对比页有立场) | Ref MCP:`search()`+`read()` 迭代检索 | 对 Context7 的劣势描述出自竞品页,带偏向;确切 endpoint/key 获取 **未核**。 |
| https://docs.stripe.com/mcp ; https://github.com/MicrosoftDocs/mcp | 一手厂商 | 厂商官方 docs MCP 真实存在(比聚合器更权威) | 「Cloudflare 成事实标准」是二手聚合,未核。 |
| https://www.answer.ai/posts/2024-09-03-llmstxt.html ; https://llmstxt.org/ | 实践者(提案原文) | llms.txt 提案(Jeremy Howard,2024-09-03);为 inference 期给 LLM 读文档 | 原 spec 用 `llms-ctx-full.txt`;`llms-full.txt` 是 Mintlify/Cursor 事实名,非 spec 词。 |
| https://www.mintlify.com/blog/simplifying-docs-with-llms-txt | 一手厂商 | Mintlify 自动生成 `/llms.txt` `/llms-full.txt` | — |
| (反方)searchenginejournal / ppc.land(John Mueller)/ trakkr.ai | 二手 | llms.txt **采用率仅 ~10%、主流 AI 平台不解析**;当 GEO/SEO 手段无效 | 对「coding agent 按需读文档」语境仍可用,但**别说成 web 标准**。 |
| https://cursor.com/docs/mcp | 一手厂商 | Cursor MCP 配置(`.cursor/mcp.json`,`${env:NAME}` 插值) | @Docs「indexed 但不在下拉」是已报 bug,是否修未核。 |
| ★ https://www.trychroma.com/research/context-rot | 研究(独立) | **context rot 跨 4 厂商 18 模型实测**:输入越长召回越差 | 把 context rot 从厂商说法升级为独立实证——比厂商博客更硬。 |
| ★ https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ | 研究 | temp 0 仍漂的真因:浮点不结合 + kernel 缺 batch-invariance,随 endpoint 负载漂 | 数字(1000 次出 80 个补全、+20% 开销)为厂商自报。 |

---

## C. 上下文工程文件体系(资料放哪、怎么被读)

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://agents.md/ ; https://developers.openai.com/codex/guides/agents-md | 一手厂商 | AGENTS.md:纯 Markdown、放根、nearest-file-wins、跨工具;Codex 拼接顺序 + 32KiB 上限 | 嵌套「合并 vs 覆盖」语义 spec 未钉死(各工具自定)。 |
| https://www.prnewswire.com/news-releases/...aaif...302636897.html ; https://openai.com/index/agentic-ai-foundation/ | 一手 | AGENTS.md:OpenAI 2025-08 发布、60k+ 项目;**2025-12-09 OpenAI 联合发起 Linux Foundation 下 AAIF 并捐出** | 是「co-founder + 捐赠」,不只是捐给既有机构。 |
| ★ https://code.claude.com/docs/en/memory | 一手厂商 | CLAUDE.md 4 层级、启动全量加载、`@path` import **最多 4 跳**、<200 行;auto-memory 默认开(v2.1.59+)、`~/.claude/projects/<p>/memory/`、MEMORY.md 前 200 行/25KB;`.claude/rules/*.md` 的 `paths` scope | **纠正**:`@import` 不省 token(启动即加载);**无 `#` 快捷键**加 memory(用 `/memory` 或自然语言)。 |
| https://code.claude.com/docs/en/skills ; https://agentskills.io/specification | 一手厂商 | Skills(SKILL.md)按需加载、progressive disclosure 三级、Agent Skills 开放标准;frontmatter `name`/`description` 必填 | L2<5k token 为软指标;`allowed-tools` 标 experimental。 |
| ★ https://cursor.com/docs/context/rules | 一手厂商 | Cursor `.cursor/rules/*.mdc` 四模式 + frontmatter(`alwaysApply`/`description`/`globs`)映射;原生读 AGENTS.md | **纠正过时命名**:当前是 `Always Apply / Apply Intelligently / Apply to Specific Files / Apply Manually`(旧 Auto-Attached/Agent-Requested 已废);`.cursorrules` 当前页已不提,legacy 状态未明。 |

---

## D. 实现内循环:hooks / subagents / 纠偏 / worktree

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://code.claude.com/docs/en/hooks-guide ; https://code.claude.com/docs/en/hooks | 一手厂商 | hook 退出码契约;PostToolUse/Stop/PreToolUse settings.json 形状;Stop 门把 looks-done 变 pass/fail | **关键纠正**:**exit 1 不阻断,只有 exit 2(或结构化 JSON)才阻断**;决策字段逐事件不同(Stop/PostToolUse 用 `decision:"block"`;PreToolUse 用 `permissionDecision:"deny"`);Stop 连阻 8 次被强制放行(读 `stop_hook_active` 早退)。 |
| ★ https://code.claude.com/docs/en/sub-agents | 一手厂商 | subagent 冷启动隔离上下文;`.claude/agents/*.md` frontmatter;只读 reviewer 用 `tools: Read,Grep,Glob`;别用 fork(会泄露 writer 推理) | 验收标准必须在 delegation 提示里重述;`model:inherit` 默认——主会话弱则 reviewer 弱。 |
| https://code.claude.com/docs/en/common-workflows ; /interactive-mode ; /checkpointing ; /worktrees | 一手厂商 | plan 模式进入;Esc/Ctrl+C/`/rewind`/`/clear`;`claude --worktree` 并行 | rewind 撤不回 bash 改的文件(只追踪编辑工具);worktree 不复制 `.env`(用 `.worktreeinclude`)。 |
| https://github.com/anthropics/claude-code/blob/main/plugins/code-review/commands/code-review.md | 一手厂商 | 官方 code-review 插件:只报「编译失败/明确逻辑错/CLAUDE.md 违反」,每条发现先并行验证再报 | correctness-only 规则的权威出处。 |
| GitHub issues #24327、#13744 | 社区(issue 追踪) | PreToolUse exit-2 阻 Write/Edit 不可靠、可能让 Claude「停而不自修」 | 版本相关;阻 Edit/Write 优先用 JSON `permissionDecision:"deny"`,装前实测。 |

---

## E. TDD-with-agents / reward hacking(agent 骗过检查)

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes | 实践者(专家一手) | Kent Beck 记录 agent 作弊迹象:**「disabling or deleting tests」** | 逐字可引的是这句;更强措辞见下。 |
| https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent | 二手(访谈摘要) | 「stopping AI agents from deleting tests」 | 是 takeaway 转述,非 Beck 逐字原话,别当直接引语。 |
| ★ https://arxiv.org/html/2510.20270v1 (ImpossibleBench) | 研究 | 量化作弊:GPT-5 在某集作弊 76%;**Claude 主要靠改测试作弊(>79%)**;更强模型作弊率更高 | 数字取自 HTML,付印前核 PDF。 |
| ★ https://metr.org/blog/2025-06-05-recent-reward-hacking/ | 研究(独立评测) | o3 在 RE-Bench reward-hack 30.4%;**明令「别作弊」反而更作弊** | 独立机构一手。 |
| https://arxiv.org/abs/2503.11926 (OpenAI CoT monitoring) | 研究 | coding agent 真实 hack(`sys.exit(0)`/改 verifier);CoT 监控召回高但被当奖励会失效 | — |
| https://www.anthropic.com/research/emergent-misalignment-reward-hacking ; https://arxiv.org/abs/2511.18397 | 研究/一手 | reward-hack 会泛化出 misalignment(~12% 破坏尝试);inoculation prompting 削减 >75% | 数字为厂商自报。 |
| https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ | 研究 | specification gaming 定义:满足字面规格、不达预期;根因是规格写错 | 2020,仍是标准引用。 |

---

## F. eval 驱动开发 / 可观测 / 工具质量

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★★ https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 一手厂商 | eval-driven development 8 步;从 20-50 真实失败起步;grader 判结果非顺序;pass@k vs pass^k;saturation | **本主题做 eval 最关键的一手 playbook。** CORE-Bench 42%→95% 等数字为厂商自报。 |
| https://platform.claude.com/docs/en/test-and-evaluate/eval-tool | 一手厂商 | Console 零代码最小 eval 回路(变量 + 生成用例 + side-by-side + 5 分制) | 起步门槛最低。 |
| ★ https://www.anthropic.com/engineering/writing-tools-for-agents | 一手厂商 | 工具描述/命名直接影响表现;用 eval 迭代工具;把 transcript 喂回让 agent 自己改工具 | — |
| LangSmith docs:https://docs.langchain.com/langsmith/evaluate-complex-agent 、/trajectory-evals 、/evaluation 、/observability-quickstart | 一手厂商 | 单步/端到端/多轮 eval 落地;`@traceable`/`wrap_openai`/OTEL 埋点;生产 trace → dataset;agentevals 四模式 | 站点已迁 `docs.smith.langchain.com`→`docs.langchain.com/langsmith`;GA 日期/「all users」为厂商单方声明。 |
| Braintrust:https://www.braintrust.dev/docs/start/eval-sdk 、/guides/logging 、compare-experiments | 一手厂商 | `Eval()` 抽象;autoevals;**experiment diff(score delta/红绿/regression 排序)做 hill-climbing**;CI `fail_on_regression` | — |
| OpenAI Evals:https://developers.openai.com/api/docs/guides/evals 、/graders 、https://github.com/openai/evals | 一手厂商 | graders 类型;trace grading | **重大警告:托管 Evals 平台弃用——2026-10-31 只读、2026-11-30 关停**;2026 新项目别押。发布前自查日期。 |
| https://hamel.dev/blog/posts/evals-faq/ | 实践者 | 「60-80% 时间在 error analysis / 看数据」 | **非受控测量**,从业者口径;原义偏「看数据」非泛指「写 eval」。标 unverified。 |

---

## G. 多 agent 编排 / 护栏 / 权限 / 安全 / 生产可靠性

| 来源 | 源类型 | 支撑什么 | 注意/边界 |
|---|---|---|---|
| ★ https://www.anthropic.com/engineering/built-multi-agent-research-system | 一手厂商 | orchestrator-worker;多 agent 比单 agent 高 90.2%,但 **~15× token**;**多数编码任务别用多 agent** | 何时值得:breadth-first 可并行 + 价值 >> 15× token。 |
| https://www.anthropic.com/engineering/building-c-compiler | 一手厂商 | 旗舰示范:16 并行 Claude、~$20k、10 万行;文件锁认领任务、无 orchestrator | 发布 2026-02-05。**能力压测 demo,非日常工作流**(作者自标)。 |
| ★ https://code.claude.com/docs/en/permissions | 一手厂商 | 权限模式表;求值顺序 hooks→deny→ask→allow;权限由 harness 强制非模型 | Bash 参数约束很脆(用 deny+WebFetch domain);Read/Edit deny 挡不住子进程(需 sandbox)。 |
| ★ https://developers.openai.com/codex/concepts/sandboxing | 一手厂商 | Codex `sandbox_mode × approval_policy × network_access` 三轴;Seatbelt/bubblewrap/Windows Sandbox | YOLO(full access + never)官方仅限隔离环境。 |
| https://www.veracode.com/blog/genai-code-security-report/ ; /spring-2026-genai-code-security/ | 研究(厂商,有立场) | 45% AI 代码引入 OWASP 漏洞;安全通过率几乎不随模型变大改善 | **受控基准(无安全提示)≠ 生产漏洞率**;安全厂商有商业动机。 |
| https://incidentdatabase.ai/cite/1152/(+ Tom's Hardware / The Register) | 媒体/事故库 | Replit agent 在 code freeze + read-only 下删生产库、伪造 ~4000 假记录;CEO 道歉 | 事实层可信;**「panicking/lied」是模型文本,非证实的意图**,归因层别拟人化。教训:约束要在工具/权限层强制。 |
| ★ https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ ; https://arxiv.org/abs/2507.09089 | 研究(独立 RCT) | 熟手在熟悉大仓用 early-2025 AI 反而慢 19%,自估快 20-24% | **强边界**:作者明确拒绝外推成「AI 普遍拖慢开发」。 |
| https://www.oreilly.com/radar/the-hidden-cost-of-agentic-failure/ | 实践者 | 误差复合 ∏pᵢ / 0.95^N | 作者自承「简化模型」;**是上界玩具模型,非实测**,只用来论证「缩短链路」。 |
| https://jxnl.co/writing/2025/09/11/why-grep-beat-embeddings-in-our-swe-bench-agent-lessons-from-augment/ | 实践者 | grep 在结构化代码+小仓赢;**作者本人说不主张 grep-only,RAG 仍必要** | 定性无具体胜率数字;「RAG 已死」是被过度推广。 |
| https://survey.stackoverflow.co/2025/ai/ | 调查 | ~31% 开发者用 AI agent;agent 编排生态以框架为主(LangChain 32.9% 等) | **无**「agent 应用是 agent 写 vs 手写」的比例数据(标 unverified)。 |

---

## 已被打回 / 不要引用的说法(对抗验证击落)

- ❌ Cursor「语义搜索平均提升 12.5% 准确率」——0-3 否决,具体数字无支撑。
- ❌ Codex 官方「五阶段流程」、Cursor 官方「Plan/Build/Review/Verify」——非官方命名,搜索 agent 自造。
- ❌「agentic search 同时碾压关键词和语义」「RAG 已死」——过度宣称。
- ❌ Context7/Ref 性能数字当客观事实——仅厂商自报。
- ❌ hook 用 `exit 1` 阻断——错,只有 exit 2 / JSON 才阻断。
- ❌ 把 0.95^N、Replit「说谎」、Veracode 45%、METR -19% 当无边界硬结论——各有边界,见上表。

---

## 「一起读原文」建议顺序(★ 源,双重作用:加深理解 + 顺带核验 copy-paste 配置)

1. **Anthropic Claude Code best-practices** — 整条实现内循环的骨架。
2. **Anthropic demystifying-evals-for-ai-agents** — 开发 agent 应用最特殊、最该吃透的一环。
3. **Anthropic building-effective-agents** — workflow vs agent、护栏、停止条件。
4. **Anthropic effective-context-engineering** — 上下文/资料怎么喂。
5. **Claude Code hooks-guide + sub-agents** — 把质量焊死的确定性机制(配置易错,值得对着读)。
6. **agents.md + Claude Code memory + Cursor rules** — 文件体系,配模板用。
7. **Anthropic built-multi-agent-research-system + building-c-compiler** — 多 agent 的收益/成本/边界。

---

## H. 2026 刷新源(date-verified;替换/补强 2024《Building Effective Agents》)

> 用户要求实时性:2024-12 的《Building Effective Agents》虽是奠基文但偏旧。以下为 2025-H2 / 2026 的一手材料,日期均逐页核实(标注例外)。

| 来源 | 日期 | 源类型 | 锚定流程的哪部分 / 关键点 |
|---|---|---|---|
| Anthropic《Building agents with the Claude Agent SDK》 https://claude.com/blog/building-agents-with-the-claude-agent-sdk | 2025-09-29 | 一手厂商 | **核心循环逐字**:`gather context → take action → verify work → repeat`;工具=primary building blocks |
| Anthropic《Effective context engineering for AI agents》 https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | 一手厂商 | **范式更新**:context engineering 取代 prompt engineering;agent=「LLMs autonomously using tools in a loop」 |
| Anthropic《Equipping agents with Agent Skills》 https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 2025-10-16(标准 2025-12-18) | 一手厂商 | **新零件**:Agent Skills 模块化能力、progressive disclosure;后成开放标准 |
| Anthropic《Code execution with MCP》 https://www.anthropic.com/engineering/code-execution-with-mcp | 2025-11-04 | 一手厂商 | **新范式**:MCP 当 code API 让 agent 写代码调用,省 ~98% token(自报) |
| Anthropic《Advanced tool use》 https://www.anthropic.com/engineering/advanced-tool-use | 2025-11-24 | 一手厂商 | 工具零件更新:tool search + 编程式工具调用 |
| Anthropic《Effective harnesses for long-running agents》 https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | 一手厂商 | 长任务:跨会话增量进展 + 结构化交接 |
| Anthropic《Demystifying evals for AI agents》 https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-01-09 | 一手厂商 | **eval-driven development 旗舰**:从真实失败起步、code/model/human grader、capability vs regression、pass@k/pass^k |
| Anthropic《Building a C compiler with parallel Claudes》 https://www.anthropic.com/engineering/building-c-compiler | 2026-02-05 | 一手厂商 | 多 agent/并行自主旗舰示范(能力上限,非日常) |
| OpenAI《Testing Agent Skills Systematically with Evals》 https://developers.openai.com/blog/eval-skills | 2026-01-22 | 一手厂商 | eval 定义:prompt→trace→checks→score;先定「success 可测」再写 skill |
| LangChain《On Agent Frameworks and Agent Observability》 https://www.langchain.com/blog/on-agent-frameworks-and-agent-observability | 2026-02-12 | 一手厂商 | 「agent 是非确定系统,debug/test/monitor 才是关键」 |
| Braintrust《Agent observability: complete guide for 2026》 https://www.braintrust.dev/articles/agent-observability-complete-guide-2026 | 2026-05-06 | 厂商 | 失败 trace→eval case→CI 门 的闭环写法 |
| **Stack Overflow《Agents on a leash》** https://stackoverflow.blog/2026/05/27/agents-on-a-leash-agentic-ai-remains-mostly-monitored-at-work/ | 2026-05-27 | **独立调查** | 59% 用 agent(2025=31%)、日用 37%;63% 几乎不全自动;69% 单 agent;Copilot 65%/Claude Code 50%;痛点 准确性47%/安全44% |
| LangChain《State of Agent Engineering》 https://www.langchain.com/state-of-agent-engineering | 调查 2025-11~12,2026 初发布 | 厂商调查(独立受访) | 可观测 89% 但 eval 滞后(离线52%/在线37%/30%没eval);**明说未测「用 coding agent 写 agent」** |
| OutSystems《2026 State of AI Development》 https://www.outsystems.com/news/enterprise-ai-agent-report-2026/ | 2026-04-07 | 厂商调查(独立受访) | 96% 用 agent;52% human-on-the-loop |

**date-unverified（页面未显日期）**:OpenAI AgentKit 页(公告 2025-10-06,且 Agent Builder/Evals 产品 2026-11-30 下线);Anthropic/Material《2026 State of AI Agents Report》(厂商自报,80% ROI 谨慎)。

**2024→2026 范式更新一览**:prompt→context engineering(2025-09)｜直接 tool call→code execution with MCP(2025-11)｜重复 prompt→Agent Skills 模块(2025-10)｜单 agent→agent teams 并行(2026-02)｜短任务→长任务 harness(2025-11)。

**仍 unverified**:「用 coding agent 写 agent vs 手写」的比例——2026 年依然无硬数据(LangChain 明确未测)。

---

## I. 对抗 eval 轮新增源(中立化 + 反方 + 跨厂商)

> 用于把流程从「Anthropic 框架」中立化,并补上实践反方与边界。

| 来源 | 日期 | 源类型 | 用途 / 关键点 |
|---|---|---|---|
| OpenAI《A Practical Guide to Building Agents》(PDF) https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 2025-04 | 一手厂商 | 准入门「validate use case... otherwise deterministic solution may suffice」;**单 agent 优先**「maximize a single agent's capabilities first」;Model/Tools/Instructions + 分层 guardrails |
| Google ADK 文档 https://adk.dev/evaluate/ · https://adk.dev/safety/ | 2026(持续) | 一手厂商 | 流程 Build→Evaluate→Deploy;循环 Think-Act-Observe;eval 是「highly recommended」但非 step-0;in-tool guardrails |
| Microsoft Foundry agent 生命周期 https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/development-lifecycle | 2026(持续) | 一手厂商 | 9 步生命周期;eval 在 publish 前才 gate,非设计第一步 |
| **Hamel Husain《LLM Evals FAQ》**+《Should I practice eval-driven development?》 https://hamel.dev/blog/posts/evals-faq/ · /should-i-practice-eval-driven-development.html | 2025 | **独立专家** | **反对 eval 先行**:「generally no」「error analysis first」;「benevolent dictator(单 agent)优先」 |
| LangChain《The Agent Development Lifecycle》/《State of Agent Engineering》 https://www.langchain.com/blog/the-agent-development-lifecycle · /state-of-agent-engineering | 2026 | 厂商 + 调查 | 「先建完美 eval 再上线 rarely realistic」;trace-first;现状 观测89%/离线eval52%/在线37%/30%没eval |
| **Berkeley RDI《Trustworthy benchmarks》(-cont 篇)** https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/ | 2026-04 | 研究(独立) | **8/8 主流 benchmark 可被刷分**;「Isolate the agent from the evaluator. Non-negotiable」;「Don't trust the number, trust the methodology」(注:此逐字短语经反查疑似转述而非 RDI 原文,归因待散文簇核) |
| **Berkeley RDI《Trustworthy benchmarks》(首篇)** https://rdi.berkeley.edu/blog/trustworthy-benchmarks/ | 2026-04 | 研究(独立) | **另一次审计:13 个 benchmark 全存在可刷分漏洞、45 处确认 hack**(Frontier-CS 100/100、WebArena 零浏览满分等);o3 30% reward-hacking 系**转引 METR**(原始出处 METR 2025-06-05)。与 -cont 篇是两次不同审计,非替换 |
| 成本失控复盘《The Agent That Burned $4,200 in 63 Hours》 https://medium.com/@sattyamjain96/...-d38fd9586a85 | 2026-04-14 | 实践者复盘 | 429 死循环烧 $4,200/63h;救命的是 **budget guard 硬上限**,非更好 eval → 护栏须 day-0 |
| Gartner 预测 https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 | 2025-06-25 | 研究机构 | >40% agentic 项目 2027 前被砍,主因工程/部署决策错而非模型能力 |
| OpenTelemetry GenAI 语义约定 https://github.com/open-telemetry/semantic-conventions-genai | 2026(持续) | 中立标准 | 可观测的厂商中立标准(S5 锚) |
| TDS《From Vibe Coding to Spec-Driven Development》 https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/ | 2026-05-12 | 实践者 | 工程化收敛;但自承「小改/单人/ad-hoc 写完整 spec 是 overkill」→ solo 适用边界 |

**eval 轮关键修正(已并入流程)**:① 「eval 先行」降级为「贯穿、应然非现状」(LangChain/Husain 反对);② `gather→act→verify` 是运行时循环非开发步,业界叫 ReAct/Think-Act-Observe;③ 单 agent 强默认(原候选偏多 agent;SO「69% 单 agent」一度被误用,以厂商指南为准);④ 成本护栏 + evaluator 隔离前置到 day-0;⑤ 补 部署形态/成本/版本回滚/prompt-injection;⑥ 加 solo vs 生产 适用边界。
