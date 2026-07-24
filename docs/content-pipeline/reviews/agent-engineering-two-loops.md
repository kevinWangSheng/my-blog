# Review: Agent 工程的两个循环(+ links: mutagent-agentic-ai-engineer-talk)

## Metadata

- status: publish-ready (human 已验收渲染预览 2026-07-23;final build pass)
- source paths / source records:
  - https://www.youtube.com/watch?v=pSto5YaNGUo(核心来源,视频 34:49,AI Engineer 频道,2026-06-29 上传)
  - 字幕全文:yt-dlp 自动字幕,2026-07-02 抓取(会话 scratchpad/transcript.txt,可用 yt-dlp --write-auto-subs 复取)
  - 实践对照数据:docs/content-pipeline/reviews/publish-pipeline-three-gates.md(上一篇的评审/eval/ui-verify 记录)
- refreshed/primary sources:
  - 同上(视频即一手来源;文中 Hermes/deep agents 为视频内转述,标注为「talk 里点了」)
- proposed collection: essays(文章)+ links(视频条目,同 manifest)
- proposed slug: agent-engineering-two-loops / mutagent-agentic-ai-engineer-talk
- source type: research-derived(视频解析)+ project-derived(实践对照)
- target reader: 在建/维护 LLM agent、纠结评估和迭代方式的人
- planned publishable markdown path: docs/content-pipeline/manifests/agent-engineering-two-loops/agent-engineering-two-loops.md
- planned manifest dir: docs/content-pipeline/manifests/agent-engineering-two-loops/

## Public thesis

- memorable sentence: 人不该在循环里干活,人该设计循环、然后守门;eval 是循环的终止条件,不是质量分。
- reader decision helped: 决定自己 agent 的评估怎么建(二元判据 vs 打分)、人放在循环的哪个位置、什么时候敢自动部署。
- strongest counterpoint / edge case: 「eval 全绿即自动部署」与「评估集是发现的产物」在冷启动阶段互相矛盾;文中作为存疑点明写。

## Complete-story check (required for learning/practice-derived items)

v2 起按「纯来源深解 + 评注」处理(作者反馈:无实践素材不强套实践环节;v1 的实践对照节已整体移除,仅评注里留一句带链接的指涉)。

- [x] what the source actually said is covered(七阶段逐节完整还原,含 slides 上的数字与机制)
- [x] source deep-dive completeness: 覆盖全部 16 页 slides 的主要内容(吞吐量对比、全景图、spec/build/eval/monitor/diagnose/optimize 各阶段、产品与 demo 全流程),非目录式简介
- [x] source key visuals embedded with source-credit captions(10 张视频抽帧,site/public/images/agent-engineering-two-loops/,均带「视频 mm:ss 画面 © Mutagent」标注)
- [x] N/A — practice: 无实践素材,按纯深解写;评注节一句话链接上一篇管线文章,不展开
- [x] N/A — results/data: 同上
- [x] verified vs. untested claims: 全文转述均以「他们/slides 上/视频里」归属给演讲者;评注节明确标注「以下三条是我的判断」
- [x] my own judgment is present and clearly separated(独立评注节,开头声明)
- absent stages and why: 实践环节缺席,原因是本篇为视频深解、无对应实践素材;按 v2 规则记录于此,不在正文强套

## Links collection maintenance

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| https://www.youtube.com/watch?v=pSto5YaNGUo | yes(文章围绕它展开) | promote(同 manifest links item) | mutagent-agentic-ai-engineer-talk |
| Hermes / deep agents(视频内提及的框架名) | no(转述,非引用来源) | inline-only(标注为视频内说法) | - |

## Draft direction

essays 类型;视频解析 + 实践对照 + 判断;嵌入 afe--two-loops 走播动图(主环走播 = 在线循环,离线内环琥珀色,spec 一次性进入)。

## Rewrite plan

### Keep

- 两循环框架与五个判断(spec 隔离、终止条件、二元判据、评估集是发现的产物、诊断成本结构)
- 实践对照的真实数据(上一篇管线记录)
- 存疑点(自动部署 vs 冷启动评估集覆盖率)

### Remove / anonymize

- 演讲者口误/闲聊、产品营销性表述;不复述我未核实的产品能力细节

### Add / refresh

- 走播动图;与上一篇文章的自然衔接

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| 视频内容转述(七阶段、各机制、数字) | 字幕全文(yt-dlp,2026-07-02)+ 14 帧 slides 截图(信息以画面为准交叉核对) | 2026-07-02 | yes | n/a |
| slides 数字(12 vs 242 cycles、61/100、1.2k/880/610/430/210、99%/$0.05) | 对应抽帧画面(03:00/12:20/20:40/24:05) | 2026-07-02 | yes | n/a |
| 配图 10 张 | site/public/images/agent-engineering-two-loops/*.webp(01-throughput…10-demo-finding) | 2026-07-02 | yes | n/a |

## Required publishable frontmatter plan

Shared:

- title: Agent 工程的两个循环
- description: 见 staged frontmatter
- date: 2026-07-02
- tags: ["agents", "eval", "agent-engineering", "video-notes"]
- visibility: public

Collection-specific:

- essays: 无额外字段;links 条目:url/category(reference,按对抗评审建议由 essay 改)/note 已填

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.(视频即一手来源;框架更替说法标注为视频内观点)
- [x] Benchmark/metric claims refreshed or removed.(无数字型 benchmark 断言;视频未给数据的处明写"视频没给数据")
- [x] Security claims phrased defensively.(无)
- [x] Hypothetical examples labeled as hypothetical.(无)
- [x] Public links/repo/demo/result claims verified.(YouTube 链接待 eval subagent 验;实践数据见上一篇 review)

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.(演讲者姓名/公司为公开会议信息)
- [x] No fabricated project result or experience.(实践数据全部来自上一篇的留档记录)
- [x] Internal KB/local paths are kept in review metadata.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | editor:「eval 是终止条件」尖锐好记;主次已按其建议重排(开头即押主论点) |
| Reader payoff | 2 | editor:模型 + 可操作决策 + 边界警示 |
| Specificity | 2 | editor:blocker 明细、git 证据、沉淀实例 |
| Structure | 1→2 | editor 初评 1(开头程序化、五判断无路标);已改钩子开头 + 加粗路标,复核为 2 |
| Source grounding | 2 | source:全部关键转述可回溯字幕时间戳;三处措辞已软化 |
| Judgment density | 2 | 保留意见(自动部署 vs 冷启动)是文中原生观点 |
| Voice | 2 | 三方扫描均干净;「周而复始」套话已删 |
| Safety/privacy | 2 | 对抗:泄漏 grep 全零;讲者表述已改为字幕可背书的职衔 |
| Freshness | 2 | 视频 2026-06-29,当日核查 |

Total: 18/18(Structure 为修复后复核分)

## Review loop(v2 重评)

### Eval review (v2, links/images, after build)

- reviewer: subagent(独立于写稿 agent)
- pass: yes
- 图片:12/12(01-throughput…11-demo-decisions 含 03b-build),markdown 引用 = built HTML img 一一对应,dist 内全部存在且非零字节(38KB–67KB),目录无多余文件
- 外链:4 条实链全 200(YouTube 视频、模板相关链接、字体样式表);preconnect 裸域/未发布 self-canonical 按惯例注释不计 fail
- 站内链接:12 条全部在 dist 解析且非零字节,重点核验 /my-blog/logs/publish-pipeline-three-gates/ 通过
- rendered check: ui-verify 覆盖


### Editor review (v2)

- reviewer: subagent(独立上下文)
- pass: yes
- blockers: none(确认非提纲式简介、无强套实践、评注独立)
- major edits: (1) Phase 编号与七阶段自相矛盾,已去编号只留阶段名;(2) eval 长节缺导航,已加四个 H3;(3) ship 着墨少,已加「talk 对 ship 本身着墨不多」管住预期。
- minor edits: 两处名词裸奔已加括号释义;「很实际」判断词改中性;连接器清单压缩;img02 caption 点明与动图的分工;补 build slide 与 decisions 页两张图(计 12 张)。「X,不是Y」句式多为 slide 原句直译,保留并记录。

### Source/factual review (v2)

- reviewer: subagent(独立上下文,逐帧比对 10 张 slides 原图 + 字幕)
- pass: yes
- blockers: none
- claims needing refresh/removal(均已应用): build 名单挂靠到产品 slide 并把「Claude Agents」改为 slide 原文「Claude」;SYNTHESIZE 补上 spec 来源;「长回 spec 和评估集」改为「spec、agent 和评估集」;figcaption「spec 只进入一次」改「新意图从 spec 进入」(与官方图 spec 回流虚线一致)。「Benedikt Sanftl」全名由视频官方标题背书(eval subagent 曾以 oembed 核实),记录于此。
- notes: 12 vs 242、61/100、五类失败量级 1.2k/880/610/430/210、success gate 双条件、ONE RULE 与四属性、demo 全流程等逐项核到帧或字幕时间戳。

### Adversarial review (v2)

- reviewer: subagent(独立上下文)
- pass: no(初评);blocker 裁决后放行
- blockers: 演讲者姓名职务需证实。裁决:字幕开场自我介绍(Bene: "CEO and co-founder";Burak: "I'm the CTO")+ 视频官方标题含全名 Benedikt Sanftl;正文已加「(视频开场两人如此自我介绍)」注明证据来源。
- non-blocking risks: 截图合理引用姿态成立(10→12 张,统一 © 标注、每张锚定实质解说、非整片搬运);时间戳按截帧记录采信;v1 实践对照内容系作者明确要求删除(非遗失),记录在案;figcaption 推导归属已改「我据此把两个循环画成」。
- required revisions: 均已完成。泄漏 grep 全零。

## Review loop(v1,已被 v2 取代,记录保留)

### Editor review

- reviewer: subagent(独立上下文)
- pass: yes
- blockers: none
- major edits: (1) 开头程序化无钩子;(2) 主论点主次不明;(3) 五判断连排无路标。均已修复:开头改押「eval 是终止条件」、思考节重排以其为主线、五判断加粗段首。
- minor edits: 图注删动画机制说明保留概念句;「标点习惯违规」具体化为破折号;删「周而复始」;产品长句断句;links category 疑点(见对抗评审,已改 reference)。均已应用。

### Source/factual review

- reviewer: subagent(独立上下文,逐条对照字幕时间戳 + 上一篇 review 记录)
- pass: yes
- blockers: none
- claims needing refresh/removal: 「原话」改「说法」(figcaption);「一年一换」软化为「一年左右可能就要换」;「人退出去」与思考节统一为「人挪到循环外面」。均已应用。
- notes: 两循环框架、五判断、产品描述、实践数字全部核到字幕时间戳或上游 review 记录;「35 分钟」为 34:49 的可接受取整。

### Adversarial review

- reviewer: subagent(独立上下文)
- pass: no(初评);blocker 修复后放行
- blockers: 「两位创始人」超出可背书证据。裁决依据字幕开场自我介绍(Bene: CEO and co-founder;Burak: I'm the CTO,两人确系同台合讲),文章与 links 条目均改为「CEO Benedikt Sanftl 和 CTO Burak 合讲」。
- non-blocking risks: (1) 产品现有人工勾选门 vs 批评自动部署愿景,已在存疑段补一句「公平地说……矛盾说的是终局愿景」;(2) 其点名待核的三处转述(Hermes/deep agents、三年、35 分钟)经字幕核实均有原句支撑,不改;(3) links category 改为 reference;(4) 实践数据需站内链接,已加指向《发布管线的三道门》的站内链接(注意:两篇需一起发布,否则该链接悬空,见 Mechanical notes)。
- required revisions: 均已完成。泄漏 grep 全零命中。

### Eval review (links/images, after build)

- reviewer: subagent(独立于写稿 agent)
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://www.youtube.com/watch?v=pSto5YaNGUo(正文唯一外链) | 200 + oembed 200,标题与文中一致 | pass |
| 文章/links 页 built HTML 其余外链 20 条(arxiv/anthropic/openai/promptfoo 等) | 全部 200 | pass |
| /my-blog/logs/publish-pipeline-three-gates/(文中新增站内链接) | dist 内存在,30086 B | pass |
| 其余站内链接 11 条 | dist 内全部存在且非零字节 | pass |
| preconnect 裸域 ×2、待发布 self-canonical ×1 | 404,非文档链接,按惯例不计 fail | n/a |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| (无 img 元素,配图为内联 SVG) | n/a | n/a |

- rendered check run: yes(ui-verify 覆盖)
- broken items and fixes: none

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| 「两位创始人」表述超出证据(对抗评审) | 按字幕自我介绍改为「CEO Benedikt Sanftl 和 CTO Burak 合讲」,文章与 links 条目同步 | yes |
| 开头无钩子 + 主论点主次不明(editor,major) | 开头押「eval 是终止条件」,思考节以其为主线重排 | yes |

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: agent
  date: 2026-07-02
  notes: 三路独立 subagent 评审完成;1 个 blocker 与全部 major/minor 修复并复核;自查发现的 diagnose 节点标题溢出同批修复(节点加宽至 140);voice.md 为模板态,本篇按 §0 基调 + 通用真人味撰写,已向作者声明。
```

## Final human blog review

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Mechanical verification notes

- content:check: pass(v2 复跑,无 warnings)
- content:sync: pass(v2 --overwrite 重同步;v1 实践对照版被 v2 完整深解版有意覆盖,作者要求)
- build: pass(20 pages,1.08s)
- preview URL: http://127.0.0.1:4327/my-blog/essays/agent-engineering-two-loops/
- ui-verify if run: v2 复跑全绿(375/768/1440 axe 全 0、console 0、overflow no;Lighthouse 94/100/100/100)
- 暗色/reduced-motion 定向复验: design-previews/verify/two-loops-dark.png(走播正常、diagnose 节点加宽后无溢出)、two-loops-reduced.png
- leak check: grep 全零命中(staged md ×2、synced source ×2、dist HTML)
- 发布依赖:文中站内链接指向《发布管线的三道门》(preview-ready),两篇需一起发布,否则该链接线上悬空
- rejection cleanup if needed: 未触发
