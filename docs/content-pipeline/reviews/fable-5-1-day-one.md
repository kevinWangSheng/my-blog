# Review: Fable 5.1 首日观察：修了什么、封了什么、该不该切

## Metadata

- status: published
- source paths / source records:
  - /Users/shenghuikevin/dev/AI/report/fable-5-1/fable-5-1-report.md（研究主报告）
  - /Users/shenghuikevin/dev/AI/report/fable-5-1/notes/sources.md（渠道覆盖、官方规格、第三方数字、系统卡关键句）
  - /Users/shenghuikevin/dev/AI/report/fable-5-1/notes/hn-thread.md（HN 917 条评论主题计数与前 40 条一级评论）
  - /Users/shenghuikevin/dev/AI/report/fable-5-1/notes/x-posts.md（21 个 X 账号时间线）
  - /Users/shenghuikevin/dev/AI/report/fable-5-1/visual/fable-5-1.html（Artifact 视觉版，本文图表数据同源）
- refreshed/primary sources:
  - https://www.anthropic.com/claude-fable-and-mythos-5-1
  - https://www.anthropic.com/claude/fable
  - https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1
  - https://platform.claude.com/docs/en/models/fable-5-1/overview
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
  - https://platform.claude.com/docs/en/build-with-claude/thinking
  - https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20&%20Claude%20Mythos%205.1%20System%20Card.pdf（本地 pdftotext 核对）
  - https://support.claude.com/en/articles/15363606
  - https://support.claude.com/en/articles/16761192
  - https://news.ycombinator.com/item?id=49525378（Algolia API 全量抓取，917 条）
  - https://every.to/vibe-check/fable-5-1-vibe-check
  - https://ampcode.com/news/fable-5.1
  - https://www.coderabbit.ai/blog/fable-5-1-model-review
  - https://snorkel.ai/blog/fable-5-1-vs-opus-5-coding-benchmark/
  - https://simonwillison.net/2026/Sep/1/claude-fable-5-1/
  - https://artificialanalysis.ai/models/claude-fable-5-1
  - https://arcprize.org/results/anthropic-claude-fable-5-1
  - https://www.vals.ai/blogs/fable-solves-cyphral-distich
  - https://www.163.com/dy/article/L5Q76G030511CSAO.html
  - https://github.com/anthropics/claude-code/issues/91289
- proposed collection: essays
- proposed slug: fable-5-1-day-one
- source type: research-derived
- target reader: 在用 Claude Code / 自建 agent harness 的工程师，知道 effort、prompt cache、tool_choice、thinking block 这些概念，正在决定要不要把负载从 Opus 5 或 Fable 5 切到 Fable 5.1。
- planned publishable markdown path: docs/content-pipeline/manifests/fable-5-1-day-one/fable-5-1-day-one.md
- planned manifest dir: docs/content-pipeline/manifests/fable-5-1-day-one/

## Public thesis

- memorable sentence: Fable 5.1 不是更聪明的 Fable 5，是更便宜、更能用、也更封闭的 Fable 5；评价它要看修了什么和封了什么，而不是 benchmark 涨了几个点。
- reader decision helped: 要不要把 agent 负载切到 5.1（按负载形状给了切 / 不切的条件），以及切之前必须改的八件事（API 迁移清单）。
- strongest counterpoint / edge case: 「更省」只对缓存占比高、effort 在 high 及以下的负载成立；Artificial Analysis 在 max effort 下测出每任务成本反而高 20%，HN 和 GitHub 首日报告额度 20–60 分钟烧完。文章第 7 节正面处理这个矛盾。

## Complete-story check (required for learning/practice-derived items)

- [x] what the source actually said is covered（官方公告、What's new、Prompting 指南、系统卡关键句均逐条覆盖）
- [x] source deep-dive completeness（三个修复、七项 benchmark、三个破坏性变更、五个新增、七条行为差异、六条系统卡结论）
- [ ] video/talk source embedded — N/A：非视频来源
- [x] source key visuals — 两张图表由官方 benchmark 数据与 HN 计数自绘（SVG），非截图；官方 benchmark 表未直接嵌图，改为自绘图并标来源
- [ ] what I actually practiced — N/A：本文是发布日调研，作者未跑自己的 eval；文中第一段与「方法与未确认」节明确声明「这篇不是评测，我没有跑自己的 eval」
- [ ] real results/data — N/A：同上，无实践阶段；第三方数字均标注引自原文未复现
- [x] verified vs. untested claims are separated（厂商自报 / 第三方引用 / 未确认三类在文中分开标注）
- [x] my own judgment is present and clearly separated（「我的判断」独立成节；文中「我的读法是」「我觉得」显式标记）
- absent stages and why: 无作者实践材料，按 pure source deep-dive + 作者判断写；未强行补「我试了」。

## Draft direction

Content brief:

- 一句话主张：Fable 5.1 真正改的是三个部署问题（缓存价格、数据留存、分类器误报），能力增量集中在长任务与科研，API 三个破坏性变更全是反蒸馏，第一天最大的争议是「更省还是更贵」，答案取决于负载形状与 effort。
- 读者带走：切 / 不切的条件清单；迁移前八步；「更省还是更贵」的拆解表；官方承认的行为差异与修法。
- 核心判断 → 支撑材料：
  - 修的是部署问题：Ramp 6% 份额（AppSo 引）、Opus 5 半价追平、缓存读 $1→$0.25、EFS、cyber −60% / bio −85%。
  - 通用增量小：官方表 + GodelNumbering 减法 + Simon Willison 评语；科研翻倍：TB-Science 24.7→52.6 及其标准误脚注。
  - 反蒸馏：What's new 三条 + 支持中心「公开记录的工业级蒸馏技术」+ HN mlaux 的串联。
  - 更省还是更贵：六方口径表 + Simon 的五档成本扫描。
- 缺口：作者无实测；Reddit 未抓到；X 覆盖有偏。均在文中声明。
- 非目标：不复述全部 benchmark；不展开科研案例细节；不写安全攻防操作细节（系统卡 exploit 数字只引结论，不写方法）。
- 可视化判断：两张自绘 SVG（官方 benchmark 分组条形图、HN 主题计数条形图），静态、显式颜色、白底，路径 `site/public/images/fable-5-1-day-one/`。

## Rewrite plan

### Keep

- 研究报告的事实层（规格、benchmark、API 变更、行为差异、系统卡结论）与争议拆解表。
- 引用的社区原话保留原作者 HN 用户名 / X 显示名（均为公开发言）。

### Remove / anonymize

- 研究报告里的渠道操作细节（twitter-cli 端点、镜像站、Exa 查询）只留一句方法说明。
- 本地路径、Artifact 链接、scratchpad 引用全部不进正文。
- 系统卡里的攻击细节只引数字与结论。

### Add / refresh

- 为博客读者加了 Fable 5 三个月处境的背景段。
- 加了「迁移前八步」清单与「我会 / 不会切」的条件。
- 把第三方评测统一成一张表并注明各自测的是什么。

## Links collection maintenance

| cited source (url) | core source? | decision | links slug |
|---|---|---|---|
| https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 | yes | promote | fable-5-1-whats-new |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | yes | promote | prompting-claude-fable-5-1 |
| https://www.anthropic.com/claude-fable-and-mythos-5-1 | no（公告本身不适合作为长期参考） | inline-only | |
| 系统卡 PDF | no | inline-only | |
| https://support.claude.com/en/articles/16761192 | no | inline-only | |
| https://news.ycombinator.com/item?id=49525378 | no | inline-only | |
| https://every.to/vibe-check/fable-5-1-vibe-check | no（时效性强） | inline-only | |
| Amp / CodeRabbit / Snorkel / Simon Willison / AA / ARC / Vals / AppSo | no | inline-only | |

去重：`site/src/content/links/` 中无 platform.claude.com 的 Fable 5.1 条目；现有 anthropic.com 条目为 engineering / research 文章，无冲突。

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| 无项目 / 个人成果类声明 | — | — | N/A | N/A |

## Required publishable frontmatter plan

- title: Fable 5.1 首日观察：修了什么、封了什么、该不该切
- description: 见 markdown
- date: 2026-09-02T00:30:00+08:00
- tags: agents, claude-code, fable-5-1, model-release
- visibility: public
- essays: canonical 无；series 无

## Fact refresh checklist

- [x] Fast-moving vendor/model claims checked against official/primary source（发布当日官方文档 + 系统卡本地核对）。
- [x] Benchmark/metric claims refreshed（均为 2026-09-01 数据，标注厂商自报 / 第三方引用）。
- [x] Security claims phrased defensively（只引系统卡的结论与红队结果，无操作细节）。
- [x] Hypothetical examples labeled（无假设性例子）。
- [x] Public links/repo/demo/result claims verified（无项目声明；引用链接待 eval 子代理逐条核验）。

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data（引用均为公开发言与公开评测）。
- [x] No fabricated result / feedback / endorsement / experience（作者明确声明未实测）。
- [x] Internal KB/local paths kept in review metadata only.

## Editorial quality rubric

| item | score | note |
|---:|---:|---|
| Thesis | 2 | 「更便宜、更能用、也更封闭」一句可记 |
| Reader payoff | 2 | 切 / 不切条件 + 迁移八步 + 争议拆解表 |
| Specificity | 2 | 每条判断带数字与出处，含失败模式（Snorkel、Every 不守限制） |
| Structure | 2 | 论点前移；修了什么 → 能力 → API → 系统卡 → 行为 → 反馈 → 争议 → 判断 → 方法；长段落改列表 |
| Source grounding | 2 | 一手文档 + 本地核对系统卡 + 全量 HN |
| Judgment density | 2 | 独立「我的判断」节 + 行内标记 |
| Voice | 2 | 报告腔段落已改为「我」的叙述；行为变化一节加作者取舍；结尾回扣 |
| Safety/privacy | 2 | 无本地路径、无私密数据 |
| Freshness | 2 | 发布当日；未确认项显式列出 |

Total: 18/18（三轮 review 修订后复核；editor 原评 16/18，做完 M1/M4/M5 后 Structure 与 Voice 各回到 2）

## Review loop

### Editor review

- reviewer: subagent（独立 general-purpose 子代理，2026-09-02）
- pass: yes（16/18，无 blocker）
- blockers: 无
- major edits: M1 论点前移到首段；M2 「更省还是更贵」补订阅额度维度并把 Every 那句提为组织句；M3 水印主题图文脱节（补 HN 争议段）；M4 两个「四件事」段落与切/不切条件改列表；M5 行为变化一节瘦身为 4 行 + 作者取舍，系统卡一节前移到 API 之后；M6 第三方评测表瘦身为「一句结论 + 一个关键数」，Snorkel/CodeRabbit 用散文展开；M7 「五个新增全是 append-only 工具」改为「前三项」；M8 去重（缓存降价、xhigh 草稿、X 覆盖偏差、Reddit）。全部采纳。
- minor edits: description 改承载论点；「七家」→「八家第三方」；EFS/ZDR/HLE/Sol/Astra 首次出现补全称；「一毛钱」改美元；「泄露账号」→「爆料账号」；「四方」→「六方」；表头「数字来自」→「为什么省 / 为什么贵」；fallbacks 补解释；medium 档补「与 Fable 5 持平」；结尾加回扣句；60.9% 重复已回公告核为巧合并在文中说明。全部采纳。

### Source/factual review

- reviewer: subagent（独立子代理，逐段对照 notes/ 与原始抓取，部分用 WebFetch 复核）
- pass: no → 13 条 blocker 全部修复后复核通过（见 Blocker resolution log）
- blockers: 图 1 alt 比较对象混淆；「差距全部来自分类器干预」为推断非官方原话；HN 计数 79/62/38 与笔记 78/60/37 不符；felixrieseberg 引文「最大」应为「很大」；三派归属错（认同派引文来自 Every、指令衰减证言在 tarr11 树下）；「一碰 Linux 就被踢回 Opus」是两条评论拼接；「HN 上有人说单向收窄」实为作者判断；bcherny 引文缺抓取记录；ARC 32% 口径写错；bio 85% 是 Fable 5/5.1 共用的既有分类器更新；date 早于发布且「六小时」实为十小时（本机 PDT）；「21 个账号」笔记只存了 12 个；synthwavedd 引文缺记录。
- claims needing refresh/removal: Cognition 引言出处改产品页；Pro 可用性加 HN 反例；Fable 5 暂停原因弱化；「多数基准追平」→「多项基准接近或追平」；ZDR 400 → 无法调用；Batches 未在官方页提及 → 删；8 月 31 日「起」；「唯一条件」→ 两个条件之一；「十条」→ What's new 七条 + Prompting 指南十几条；「1.4–2.5×」→「最高 2.5×」；外部验证仅结合剂一项；Vals 年份 1652 → 1653；CodeRabbit 版本差异注；争议表末行 high/xhigh 推断改为 issue 实际档位 medium；系统卡条目点名 Mythos 5.1、Firefox 147 是版本号、Trajectory「仅用 Fable 5.1」；Mythos 「目前限美国机构」。全部采纳。
- notes: 已核对无误清单见评审原文（定价、七项 benchmark、三个破坏性变更细节、五个新增、系统卡引文、HN/X/Every/Amp/CodeRabbit/Snorkel/Simon/Vals 数字）。时效性：正文已限定为「发布后十小时」；EFS「今秋」、旧账号「目前不强制」、Pro 可用性、HN 计数为快照，均已在文中限定或列入未确认。

### Adversarial review

- reviewer: subagent（独立子代理，另行拉取 HN 全线程 1,032 条与官方原文核对，跑了泄露 grep 与 URL 清单）
- pass: no → 6 条 blocker 全部修复后通过
- blockers: 伪造「原话」（Linux 拼接句）；「三处直接 400」错（第二条是静默丢块）；「全部指向反蒸馏」把 HN 推测当官方动机；date 早于模型发布、「六小时」实为十小时；中心论点比较对象未说清且图注错；「HN 有人说单向收窄」是作者综合。
- non-blocking risks: mlaux 的 think_deeply 细节仅一句、已被 400 封掉，保留但标为推测；felixrieseberg 标「自称在 Anthropic 工作」；「泄露账号」→「爆料账号」并补回 synthwavedd 原话末尾；Every ZDR 纠错措辞放软；Cognition 标官方客户引言；「21 个账号」需可追溯（已补齐 21 个账号 JSON 与 x-posts.md）；「X 上普遍预期」「HN 认为」缩小主语；最弱一节是行为变化（已瘦身）；图 2 计数与笔记统一（已改 78/60/37、992 分）；「七家独立」→「八家第三方」并注明 AA/Every 提前访问。
- required revisions: 「最多约省 45%」；ARC 行改口径并指向未确认；felixrieseberg 引文；Every 27 条抽查；Amp「ultra 线程」；Simon「没有返回推理摘要」；美元数字；Fable 5 暂停原因；Opus 5 追平弱化；Ramp 二手口径；ZDR 无法调用；medium 档原文；「我抓到的账号里」；GodelNumbering 减法子树 32 条、去性别代词；Astra/「没地方放」缩主语；TB-Science 日期标 Simon 出处；links whats-new note 与正文两处；Copilot 补来源。全部采纳。

### Eval review (links/images, after build)

- reviewer: subagent（独立子代理，2026-09-02，针对 staged markdown + site/dist HTML）
- pass: yes
- link results（正文与 links 条目共 18 条内容外链全部 2xx；HN 不接受 HEAD、163 拦截 HEAD，GET 均 200）:

| url | status | pass? |
|---|---|---|
| https://www.anthropic.com/claude-fable-and-mythos-5-1 | 200 | yes |
| https://www.anthropic.com/claude/fable | 200 | yes |
| https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 | 200 | yes |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | 200 | yes |
| 系统卡 PDF（www-cdn.anthropic.com/0339e6…System Card.pdf） | 200 application/pdf | yes |
| https://support.claude.com/en/articles/16761192 | 200（302 到带 slug 的 URL） | yes |
| https://github.blog/changelog/2026-09-01-claude-fable-5-1-generally-available-in-github-copilot/ | 200 | yes |
| https://github.com/anthropics/claude-code/issues/91289 | 200 | yes |
| https://news.ycombinator.com/item?id=49525378 | HEAD 405 / GET 200 | yes |
| https://every.to/vibe-check/fable-5-1-vibe-check | 200 | yes |
| https://ampcode.com/news/fable-5.1 | 200 | yes |
| https://www.coderabbit.ai/blog/fable-5-1-model-review | 200 | yes |
| https://snorkel.ai/blog/fable-5-1-vs-opus-5-coding-benchmark/ | 200 | yes |
| https://simonwillison.net/2026/Sep/1/claude-fable-5-1/ | 200 | yes |
| https://artificialanalysis.ai/models/claude-fable-5-1 | 200 | yes |
| https://arcprize.org/results/anthropic-claude-fable-5-1 | 200 | yes |
| https://www.vals.ai/blogs/fable-solves-cyphral-distich | 200 | yes |
| https://www.163.com/dy/article/L5Q76G030511CSAO.html | HEAD 403（bot 拦截）/ GET+UA 200 | yes |
| canonical https://kevinwangsheng.github.io/my-blog/essays/fable-5-1-day-one | 404（部署前预期） | n/a，部署后复核 |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| /my-blog/images/fable-5-1-day-one/01-official-benchmarks.svg | site/dist/images/fable-5-1-day-one/01-official-benchmarks.svg，8713 B，xmllint OK，本地 200 image/svg+xml | yes |
| /my-blog/images/fable-5-1-day-one/02-hn-themes.svg | site/dist/images/fable-5-1-day-one/02-hn-themes.svg，7157 B，xmllint OK，本地 200 image/svg+xml | yes |
| 站内链接（/my-blog/、essays/、links/、logs/、projects/、about/、rss.xml、_astro 资源、favicon）16 项 | 均存在于 site/dist 且非空 | yes |

- rendered check run: yes（临时 http.server 4331，文章页 200，两张图 200 且 content-type 正确，故意错误路径 404）
- broken items and fixes: 无

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Linux 拼接引文 | 拆为 nrmitchi「只要看到和 Linux 沾边的东西就发作」+ scronkfinkle「对齐检查太敏感，基本总把我踢回 Opus」各自署名 | yes |
| 「三处直接 400」 | 改「两处直接 400，一处静默丢块」，links note 同步 | yes |
| 「全部指向反蒸馏」 | 标题改「都围绕 thinking 块」；正文区分官方对第二、三条明说反蒸馏、第一条官方理由是参数质量、串联是 mlaux 推测；description 同步 | yes |
| date 早于发布 / 六小时 | date 改 2026-09-02T00:30:00-07:00；全文「六小时」→「十个小时」；「昨天」→「美西时间 9 月 1 日上午」；研究笔记时区标签同步改 PDT | yes |
| 比较对象 / 图注 | alt 与小标题区分「相对 Fable 5」「相对 Opus 5」，正文补两组数字 | yes |
| 「HN 有人说单向收窄」 | 改为作者自己的叠加判断并声明系统卡未如此连接 | yes |
| 「差距全部来自分类器干预」 | 改为官方脚注「可能拉低」+ 归因是作者推断 | yes |
| HN 计数 79/62/38 | SVG、正文、研究报告、Artifact 统一为 78/60/37、992 分 | yes |
| felixrieseberg「最大」 | 改「很大的进步」「对我的风格指令响应更可靠」 | yes |
| 三派归属 | 认同派改 ddahlen，反问 troupo，指令衰减归 tarr11 树；去掉 Every 的「终于能读懂」 | yes |
| bcherny / synthwavedd 引文缺记录 | 重新抓取并保存 21 个账号 JSON，x-posts.md 重生成含 URL | yes |
| ARC 32% 口径 | 改「max 档，两个基准每题平均」，并注明与结果页 $4.49 不符、列入未确认 | yes |
| bio 85% 归属 | 改「Fable 5 与 5.1 共用、此前已更新过的分类器」 | yes |
| 「21 个账号」不可追溯 | 见上，notes 现含 21 个账号 | yes |

## Agent review

```yaml
agent_review:
  status: published
  reviewer: agent
  date: 2026-09-02
  notes: 三轮独立子代理评审（editor pass / source 13 blockers / adversarial 6 blockers）全部处理并复核；泄露 grep 无命中；links 维护表已填；等待 content:sync、build、eval 子代理。
```

## Final human blog review

```yaml
human_blog_review:
  status: explicit-publish-request-approved
  reviewer: human
  date: 2026-09-02
  notes: 用户在同一会话中明确要求「转成 blog 发布到我的 blog 上」，并授权内容与形式可修改。
```

## Mechanical verification notes

- content:check: ok（3 items, 0 errors, 0 warnings）
- content:sync: ok，写入 site/src/content/essays/fable-5-1-day-one.md、links/fable-5-1-whats-new.md、links/prompting-claude-fable-5-1.md（表头微调后以 --overwrite 重同步一次）
- build: `pnpm --dir site build` 25 pages OK；`pnpm ci:sanity` ok（仅既有 warning「Logs page does not contain the standard empty collection message」）
- preview URL: http://127.0.0.1:4327/my-blog/essays/fable-5-1-day-one/（`pnpm preview:local`）；本次自验证用临时端口 4332 截图核对
- ui-verify: `/my-blog/essays/fable-5-1-day-one/` ok=true；375/768/1440 axe 0（crit 0 / serious 0），console 0，横向溢出无；Lighthouse perf 94 / a11y 100 / best-practices 100 / seo 100（CLS 0，LCP 2.5 s）
- leak check: staged markdown、synced source、dist HTML 三处 grep（/Users/、kb-vault、docs/content-pipeline、scratchpad、private draft、confidential、机密、不发布、禁止发布）均无命中
- rejection cleanup if needed: 无（用户在同一会话明确要求发布，跳过本地 human preview 门，直接 publish-ready）
- publish: main 推送 f0a50a0 → CI → Deploy run 33602492741 success（build / publish 两个 job 均 success）；线上核验 2026-09-02 07:15Z：https://kevinwangsheng.github.io/my-blog/essays/fable-5-1-day-one 200 且含标题与两张 SVG（均 200 image/svg+xml），links 页含两条新条目，rss.xml 含本文；canonical 已通
