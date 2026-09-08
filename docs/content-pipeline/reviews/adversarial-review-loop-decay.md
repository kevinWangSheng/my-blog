# Review: 让 agent 反复自审，质量是往下走的

## Metadata

- status: published
- source paths / source records:
  - `~/dev/AI/adversarial-loop-eval/` — 本次实验的完整产物目录（规划、审查意见、评分 JSON、统计脚本）
  - `~/dev/AI/adversarial-loop-eval/results/REPORT.md` — 实验报告
  - `~/dev/AI/adversarial-loop-eval/results/blogdata.json` — 文中所有数字的来源
  - `~/dev/AI/adversarial-loop-eval/citations_verified.md` — 17 篇 arXiv 引用的逐条核对记录
  - `~/dev/AI/adversarial-loop-eval/literature.md` — 前期文献综述
  - 已发布的 HTML 版本（同一作者、同一实验，非外部来源）
- refreshed/primary sources:
  - 17 篇 arXiv 论文页面，2026-09-08 逐条核对编号/标题/作者/年份/会议
- proposed collection: essays
- proposed slug: adversarial-review-loop-decay
- source type: public-original（作者自建实验，非 KB 派生）
- target reader: 用 coding agent 做规划/评审循环的工程师；正在搭 LLM-as-judge 门禁的人
- planned publishable markdown path: docs/content-pipeline/manifests/adversarial-review-loop-decay/adversarial-review-loop-decay.md
- planned manifest dir: docs/content-pipeline/manifests/adversarial-review-loop-decay/

## Public thesis

- memorable sentence: 无外部验证信号的对抗审查循环不收敛也不改善；退化最大的两条通道是范围失守与开始编造需求外的事实。
- reader decision helped: 该跑几轮自审、用什么当停止条件、能不能用成对比较做验收门禁、什么样的循环才值得跑。
- strongest counterpoint / edge case: 三个维度在初版即满分，存在天花板效应，本实验无法证明「循环救不回一份差的初版」。另有一篇预印本（Bohnet 等 2025）声称无验证器自评在 Blocksworld 上有效，与本文结论冲突——文中已正面处理并给出适用范围差异。

## Complete-story check

- [x] what the source actually said is covered — 前置研究在「为什么值得自己测一遍」与「相关工作」两节展开，含具体机制与数字
- [x] source deep-dive completeness — 本文非单一来源解析，前置研究按作用分五组给出，每条附具体结论而非仅标题
- [x] video/talk source embedded — N/A：无视频/演讲来源
- [x] source key visuals — N/A：来源为论文，无需引用其图；文中三张图均为本实验自有数据
- [x] what I actually practiced is concrete — 实验设计一节给出任务数、臂设置、盲评方式、停止条件；机制一节给出采纳率与批评条数
- [x] real results/data/outputs are included — 主曲线、逐格表、六维分解、成对比较表、脱敏对照表、篇幅数据
- [x] verified vs. untested claims are separated — 「这个结论管到哪里为止」明确标出哪条是文献推论而非实测；局限一节列出天花板效应与未跑完部分
- [x] my own judgment is present and separated — 「四条可操作的规则」与各节判断句均为作者判断，与数据陈述分开
- absent stages and why: 无缺失阶段。本文为 public-original，来源即作者自建实验。

## Draft direction

把一次受控实验写成对工程决策有用的结论：不是「自审有害」这种口号，而是给出退化的位置、机制、以及边界在哪。

## Rewrite plan

### Keep

- 主曲线、六维分解、机制图三张自有数据图（转为站内 inline SVG figure，沿用 `afe--*` 自包含模式；除 `prefers-color-scheme` 外另加 `[data-theme]` 选择器以匹配本站手动暗色切换）
- 脱敏翻车这一节：它是方法学教训，对读者有直接可操作价值
- 符号检验、逐格表：小样本下的稳健性证据

### Remove / anonymize

- 所有本地路径（实验目录、脚本名、结果文件名）不进公开正文，仅保留在本评审文件
- 具体模型额度/账号相关表述改为「模型额度耗尽」，不涉及账户细节
- 内部运行日志、子代理编排细节不进正文

### Add / refresh

- 为公开读者补上「为什么值得自己测」——已有研究的覆盖范围与空白
- 补上首轮审查意见的四个具体例子，让「批评有价值但产物没变好」这个区分落地
- 相关工作按作用分组，标注预印本与同行评审的分量差异
- 明确标出哪些是文献推论而非本实验实测

## Links collection maintenance

| cited source (url) | core source? | decision | links slug |
|---|---|---|---|
| https://arxiv.org/abs/2407.04549 | 是，最贴近的前置工作 | promote | pan-spontaneous-reward-hacking |
| https://arxiv.org/abs/2406.01297 | 是，该问题的最佳入口综述 | promote | kamoi-when-can-llms-self-correct |
| https://arxiv.org/abs/2305.14325 | — | already-exists（本文未改变其重要性理由，不更新） | （已有条目） |
| https://arxiv.org/abs/2604.22891 | — | already-exists（同上） | （已有条目） |
| https://arxiv.org/abs/2310.01798 | 否，支撑性引用 | inline-only | — |
| https://arxiv.org/abs/2402.11436 | 否，支撑性引用 | inline-only | — |
| https://arxiv.org/abs/2601.11578 | 否，预印本旁证 | inline-only | — |
| https://arxiv.org/abs/2303.11366 | 否，机制说明引用 | inline-only | — |
| https://arxiv.org/abs/2305.11738 | 否，机制说明引用 | inline-only | — |
| https://arxiv.org/abs/2303.17651 | 否，支撑性引用 | inline-only | — |
| https://arxiv.org/abs/2604.22273 | 否，预印本旁证 | inline-only | — |
| https://arxiv.org/abs/2306.09896 | 否，支撑性引用 | inline-only | — |
| https://arxiv.org/abs/2306.05685 | 否，方法学引用 | inline-only | — |
| https://arxiv.org/abs/2305.17926 | 否，方法学引用 | inline-only | — |
| https://arxiv.org/abs/2404.13076 | 否，方法学引用 | inline-only | — |
| https://arxiv.org/abs/2512.24103 | 否，反例引用 | inline-only | — |
| https://arxiv.org/abs/2607.22653 | 否，支撑性引用 | inline-only | — |

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| 深层分 4.80 → 4.13 / 4.30（脱敏） | results/blogdata.json | 2026-09-08 | 是 | — |
| 12 格全部 P5 ≤ P0；按任务合并为 6 个独立单元后 6/6 下降，符号检验双侧 p≈0.031 | results/summary_judge_redacted.json 逐格计算 | 2026-09-08 | 是 | 原稿按 12 格算得 p≈0.001，因两臂共用初版不独立，已下调口径 |
| 维度分解：范围忠实 −1.50（约占深层分降幅 51%）、无虚构 −0.92（31%）、风险对策 −0.42（14%）、可读性 −2.08（不计入深层分） | results/blogdata.json dims_all | 2026-09-08 | 是 | 原稿称「坏掉的只有范围」，已按分解改写 |
| 成对比较 69 胜 0 负 2 平 / 71 次判定（未脱敏一遍）；脱敏一遍已完成的 51 次中 50 胜 0 负 | results/summary_judge.json 与 summary_judge_redacted.json pair | 2026-09-08 | 是 | 已在正文标明数据来源，不再笼统称「以脱敏为准」 |
| 60 份修订版中 54 份明写「全部采纳」（字符串共出现 86 次） | 对 60 份修订版正文逐份检查 | 2026-09-08 | 是 | 原稿写「78 次」不可复现，已改为按份数口径 |
| 60 轮 0 次 NO_ISSUES | 全部 C*.md 文件检查 | 2026-09-08 | 是 | — |
| 篇幅 9.5K → 59K 字符 | results/auto_stats.json | 2026-09-08 | 是 | — |
| 脱敏前后降幅 −0.30 vs −0.58 | 两套 judge 输出对比 | 2026-09-08 | 是 | — |
| 17 篇论文的编号/标题/作者/年份/会议 | citations_verified.md（逐条访问 arXiv 页面） | 2026-09-08 | 是 | 4 处转述过头已改写；会议仅在原页面标注时才写 |

## Required publishable frontmatter plan

- title: 让 agent 反复自审，质量是往下走的
- description: 6 个规划任务 × 2 条臂 × 5 轮的受控实验：无外部验证信号的对抗审查循环不收敛，从第二轮起持续退化，范围失守是最大的一条通道。
- date: 2026-09-08
- tags: agents, evals, coding-agents, llm-as-judge
- visibility: public
- essays: series = Agent Workflows

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked — 正文不含厂商/模型版本性能断言；实验所用模型仅在评审文件记录，公开正文不做跨模型性能比较
- [x] Benchmark/metric claims refreshed — 所有数字来自本实验产物，可回溯
- [x] Security claims — N/A
- [x] Hypothetical examples labeled — 无假设性例子；首轮批评的四个例子来自真实审查意见
- [x] Public links verified — 交由 eval 子代理机械核验（见下）

## Safety checklist

- [x] No secrets/tokens/keys
- [x] No private marker / forbidden publish marker
- [x] No private person/company data
- [x] No fabricated result — 所有数字有产物支撑；未声称任何生产环境部署或外部背书
- [x] Internal paths kept in review metadata only

## Editorial quality rubric

| item | score | note |
|---|---:|---|
首轮自评为 18/18，三位评审一致认为不可支撑（编辑评审实评 14/18）。以下为按评审意见修订后的重评。

| item | score | note |
|---|---:|---|
| Thesis | 2 | 修订后主张与数据一致：不是「只有范围坏了」，而是范围与无虚构两条通道占八成降幅 |
| Reader payoff | 2 | 跑几轮、用什么停止条件、能否用成对比较做门禁，四条规则可直接执行 |
| Specificity | 2 | 逐任务表、首轮四个具体缺陷、违反并行处理禁止项的实例、脱敏翻车过程 |
| Structure | 2 | 反例与编辑量数据已从参考文献提入正文；结尾补判断句 |
| Source grounding | 2 | 全部数字可回溯产物并经独立子代理复算；引用按核对记录改正四处转述 |
| Judgment density | 2 | 天花板效应、统计口径下调、反例适用范围均正面处理并标为判断 |
| Voice | 2 | 已清理面向审稿人的元注释与实验室日志腔 |
| Safety/privacy | 2 | 三处泄露检查零命中；正文无厂商与模型名 |
| Freshness | 2 | 实验与引用核对均为 2026-09-08 |

Total: 17/18（Specificity 与 Structure 按编辑评审的修订后预估；仍高于发布门槛 16）

## Review loop

### Editor review

- reviewer: subagent（独立，opus）
- pass: no（首轮）→ 阻断项已全部修复
- blockers（首轮给出，均已修）:
  1. 「坏掉的只有范围」与自家图表矛盾（无虚构 −0.92、风险对策 −0.42 并非不动）→ 改为「退化主要发生在范围上」，正文给出 51%/31%/14% 分解
  2. 「深层分」全文未定义 → 在方法节定义为五维均值，并说明排除可读性的理由（它掉得最多，排除更保守）
  3. 范围蔓延零实例 → 补入日志合并任务第五轮把被点名禁止的并行处理排进阶段计划的具体例子
- major edits 已采纳: 前言文献段压缩约六成；Bohnet 反例从参考文献提到「边界」正文并给出我的判断；编辑量数据提到机制节并与规则二对齐；无虚构单独成段；「中途翻车」教训前置并压缩；结尾补判断句；相关工作精简并去掉面向审稿人的元注释
- minor edits 已采纳: 删除空转句、去掉预告式句式、修正 5 轮 vs 初版行合计、去除三位小数假精度、首次出现处定义「格」

### Source/factual review

- reviewer: subagent（独立，opus）
- pass: no（首轮）→ 五项阻断已全部修复
- blockers（首轮给出，均已修）:
  1. 「只有范围」框架 → 同编辑评审第 1 条
  2. 「可读性十二格十一格下降」实为未脱敏数据 → 已标注：脱敏 7 降 5 平，未脱敏 11 降
  3. 「78 次」不可复现（产物为 86 次出现 / 54 份文件）→ 改为「60 份修订版里 54 份明写全部采纳」
  4. 「编辑量始终在两成以上」为假（60 个格轮中 5 个低于 0.20，最低 0.087）→ 改为「各轮十二格平均」并给出 0.47/0.33/0.30/0.25/0.23 与最低格 8.7%
  5. Huang 转述过强 → 按 citations_verified 软化为「往往不能改善，有时反而变差」
- 其他已处理: 假阳性率未测（改为只声称不终止）；Reflexion 反馈来源收口径并标明因果联系是我的读法；Wu 的编辑量停止条件标为我的推论；Du 论文补全完整标题；脱敏效应由 0.3 改为 0.23（两臂 0.37/0.20）；critic 条数标注纯对抗臂；篇幅增长标注按臂均值；输出上限观察标注为无日志的运行时观察；自报标记两种口径都写明；「收益被抵消」标为推论并说明无对照臂
- 已核验无误（抽样）: 4.80/4.13/4.30、−0.58、12 格全部 delta、维度分解、成对比较 69-0-2、60 轮 0 次 NO_ISSUES、9.5K→59K、脱敏对照表、2.5% 删除比例、唯一一次禁止项违反、首轮四个缺陷均在原始审查意见中逐字可查
- 会议标注: 仅 Huang(ICLR 2024)/Kamoi(TACL)/CRITIC(ICLR 2024)/Olausson(ICLR 2024)/Zheng(NeurIPS 2023 D&B) 五处，均为 arXiv 页面明确标注；其余七篇未印会议

### Adversarial review

- reviewer: subagent（独立，opus）
- pass: no（首轮）→ 四项阻断已全部修复
- blockers（首轮给出，均已修）:
  1. 结论与自家图表矛盾，且无虚构 −0.92 全文无一字提及 → 已改框架并为无虚构单独成段
  2. p≈0.001 依赖两个错误前提：零假设被天花板效应污染；十二格不独立（两臂共用初版）→ 改为按任务合并的六个独立单元 p≈0.031，并加入天花板效应说明
  3. 「所有主要数字以脱敏为准」与成对比较来自未脱敏一遍矛盾 → 已标明来源，并补入脱敏已完成的 51 项中 50 胜 0 负、方向一致
  4. 模型信息公开正文与评审文件均无记录 → 已记入本文件，正文补「单一模型家族，结论未必跨家族转移」
- 已处理的非阻断项: 柱状图改为严格零基线等比；「全部采纳 78 次」与「只驳回 1–2 条」的自相矛盾已消除；「推迟了下滑」改为「两臂差异在 n=6 下不可分辨」；六轮改为六组对比；成对比较总数 71 并说明一次调用未完成；Al Azher 年份按 arXiv 编号与当前版本记为 2026
- 已确认无风险: 泄露检查零命中；正文未出现任何厂商或模型名；无捏造成果或外部背书
- 未处理（记录在案）: 站点用 data-theme + localStorage 做手动暗色切换，站内三篇既有文章的内联图仅响应系统偏好，手动切换会主题错位。本文三张图已补 [data-theme] 选择器；既有文章属既存问题，不在本次任务范围

### 模型与运行环境记录（公开正文不含）

- 规划者 / 审查者: Opus 5
- 评审（judge）: Fable 5.1，与生成方不同模型、同一家族
- 运行日期: 2026-09-07 至 2026-09-08
- 规模: 126 次生成调用，约 470 次评审调用（含脱敏重跑）
- 未完成部分: 脱敏一遍的成对比较 109/144、退化核查 19/60，因模型额度耗尽中止

### Eval review (links/images, after build)

- reviewer: subagent（独立，sonnet；与撰稿代理分离）
- pass: yes
- link results: 共 41 个唯一 URL，其中 18 个 arXiv

| url | status | pass? |
|---|---|---|
| 18 个 arXiv 链接（2303.11366 / 2303.17651 / 2305.11738 / 2305.14325 / 2305.17926 / 2306.05685 / 2306.09896 / 2310.01798 / 2402.11436 / 2404.13076 / 2406.01297 / 2407.04549 / 2511.07784 / 2512.24103 / 2601.11578 / 2604.22273 / 2604.22891 / 2607.22653） | 全部 200 | pass |
| 站内其余外链（code.claude.com ×2、developers.openai.com ×5、github.com、openreview.net、anthropic.com ×2、promptfoo.dev、youtube.com ×5） | 全部 200 | pass |
| fonts.googleapis.com / fonts.gstatic.com 裸域 | 404 | 非内容链接，仅 preconnect 提示；实际字体子路径均 200 |
| 本文 canonical / og:url | 404 | 预期，尚未部署到 GitHub Pages |

- arXiv 标题抽查（5 篇）: 2305.14325、2512.24103 完全一致；2601.11578 标题一致（v1 提交 2025-12-30，当前 v2 为 2026-03-16，编号 2601）；2604.22273、2607.22653 为省略副标题的简写，非错误
- image results: 正文 img 数为 0，三张图均为内联 SVG

| src | resolved location / status | pass? |
|---|---|---|
| figure afe--loopdecay | inline SVG，viewBox 0 0 900 340，渲染宽 666px | pass |
| figure afe--loopdims | inline SVG，viewBox 0 0 900 340，渲染宽 700px | pass |
| figure afe--loopmech | inline SVG，viewBox 0 0 900 306，渲染宽 700px | pass |

- 内部链接: 16 个站内 href 全部解析到 site/dist 下真实文件，0 缺失
- rendered check run: yes（Playwright headless 加载预览页）——控制台 0 错误 0 警告，本页资源无 404，三张 SVG 渲染宽度均非零
- broken items and fixes: 无

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| 「坏掉的只有范围」与图表矛盾（编辑 B1 / 事实 1 / 对抗 B1） | 改标题与前言，给出 51%/31%/14% 分解，无虚构单独成段 | 是 |
| 「深层分」未定义（编辑 B2） | 方法节定义为五维均值并说明排除可读性的理由 | 是 |
| 范围蔓延零实例（编辑 B3） | 补入日志合并任务违反并行处理禁止项的具体例子 | 是 |
| p≈0.001 依赖错误独立性与被污染的零假设（对抗 B2） | 改为按任务合并的 p≈0.031，并说明天花板效应 | 是 |
| 成对比较来自未脱敏一遍却被称为脱敏结果（对抗 B3 / 事实 g） | 标明来源，补入脱敏 51 项中 50 胜 0 负的同向证据 | 是 |
| 模型信息无记录（对抗 B4） | 记入本评审文件，正文补单一模型家族局限 | 是 |
| 可读性 11/12 实为未脱敏（事实 2） | 标注脱敏 7 降 5 平、未脱敏 11 降 | 是 |
| 「78 次」不可复现（事实 3） | 改为 60 份中 54 份明写全部采纳 | 是 |
| 「编辑量始终两成以上」为假（事实 4） | 改为各轮十二格平均，并给出最低格 8.7% | 是 |
| Huang 转述过强（事实 5） | 按核对记录软化 | 是 |
| 假阳性率未测却断言很高（事实 a） | 改为只声称循环不终止 | 是 |
| ui-verify 报 1 处 serious 无障碍问题（可滚动区不可聚焦） | 三张图的 .wrap 加 tabindex=0 / role=img / aria-label 与 focus-visible 样式，沿用站内既有写法 | 是 |

## Agent review

```yaml
agent_review:
  status: preview-ready
  reviewer: agent
  date: 2026-09-08
  notes: |
    三轮独立子代理评审（编辑 / 事实 / 对抗）首轮均判 no，合计 12 项阻断，
    已逐条修复并记录在 Blocker resolution log。
    eval 子代理（独立）判 pass：18 个 arXiv 链接全部 200，内部链接零缺失，
    三张内联 SVG 渲染宽度非零，控制台零错误。
    ui-verify 三断点 axe 0/0，无横向溢出，lighthouse 96/100/100/100。
    泄露检查零命中。等待人工预览验收；未提交、未推送、未部署。
```

## Final human blog review

```yaml
human_blog_review:
  status: approved
  reviewer: human
  date: 2026-09-08
  notes: |
    人工在本地预览验收通过，明确要求发布。
    注意：验收时的预览构建自 kimi-k3/readability 分支（Monograph 改版模板）；
    部署源 main 上为改版前样式。已在 main 的 worktree 中重新构建并核验：
    content:check ok、build 27 页、ui-verify 三断点 axe 0/0、lighthouse 100/100/100/100。
    文章正文与三张内联 SVG 在两套模板下均正常，差异仅在站点外壳配色。
```

## Mechanical verification notes

- content:check: ok，3 项（essays ×1，links ×2），0 error 0 warning
- content:sync: ok，写入 site/src/content/essays/adversarial-review-loop-decay.md 与两条 links
- build: ok，25 页；notes 集合为空的告警为既存问题，与本次无关
- preview URL: pnpm preview:prepare 后 out/ui-serve，路由 /my-blog/essays/adversarial-review-loop-decay/
- ui-verify: 375/768/1440 三断点 axe critical 0 / serious 0，consoleErr 0，无横向溢出，lighthouse performance 96、a11y 100、best-practices 100、seo 100
- leak check: 对暂存 markdown、同步源、产出 HTML 三处执行，/Users/、kb-vault、docs/content-pipeline、机密、不发布等关键词零命中；另检查厂商与模型名，正文零命中
- 部署与线上核验（2026-09-08）:
  - commit bea904b 推送至 main；CI success，Deploy Astro site to GitHub Pages success
  - 线上返回码：文章页 / essays 列表 / links / 首页 / rss.xml 全部 200
  - 线上正文抽查命中：标题、p ≈ 0.031、范围忠实、无虚构、条件性多进程解析实例
  - 三张内联 SVG 均在线上 HTML 中（afe--loopdecay / loopdims / loopmech），正文 img 数为 0
  - 线上 HTML 泄露复检零命中
  - 公开地址：https://kevinwangsheng.github.io/my-blog/essays/adversarial-review-loop-decay/
- 备注：本次发布在 main 的临时 worktree 中完成，未触碰 kimi-k3/readability 分支及其未提交改动
- rejection cleanup if needed: 若人工驳回，删除 site/src/content/essays/adversarial-review-loop-decay.md 与 site/src/content/links/{pan-spontaneous-reward-hacking,kamoi-when-can-llms-self-correct}.md，并将本文件状态改为 needs-rework
