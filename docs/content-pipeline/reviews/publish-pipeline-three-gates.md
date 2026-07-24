# Review: 发布管线的三道门,和一张会动的流程图

## Metadata

- status: publish-ready (human 已验收渲染预览 2026-07-23;final build pass)
- source paths / source records:
  - .agents/skills/blog-publisher/SKILL.md(本次四处改动:强制 subagent 评审、eval subagent、links 维护、完整叙事)
  - .agents/skills/blog-publisher/references/quality-gate.md(eval reviewer pass)
  - .agents/skills/blog-publisher/references/editorial-standard.md(完整叙事 hard blocker)
  - ~/.agents/skills/animated-flow-explainer/(本次新建 skill:SKILL.md、references/techniques.md、templates/agent-loop.html)
  - design-previews/animated-flow-demo.html(走播版流程图 demo,浏览器四项验证)
  - 本次工作会话(2026-07-02)的真实改动与验证记录
- refreshed/primary sources:
  - https://github.com/konraddzbik/architecture-diagram-skill(2026-07-02 检查,subagent 深读 README/SKILL.md)
- proposed collection: logs
- proposed slug: publish-pipeline-three-gates
- source type: project-derived
- target reader: 用 coding agent 维护个人博客/内容管线的人
- planned publishable markdown path: docs/content-pipeline/manifests/publish-pipeline-three-gates/publish-pipeline-three-gates.md
- planned manifest dir: docs/content-pipeline/manifests/publish-pipeline-three-gates/

## Public thesis

- memorable sentence: 判断类检查交给独立评审,机械类检查交给 eval,两类混在一起时哪个都不可信。
- reader decision helped: 给自己的 agent 内容管线设门时,该把哪些检查拆成独立 subagent、哪些做成机械 eval。
- strongest counterpoint / edge case: solo 博客加四道门可能过重;文中以「门的成本远低于返工成本」回应,并承认这是当前判断。

## Complete-story check (required for learning/practice-derived items)

- [x] what the source (video/course/paper/tool) actually said is covered(来源是自己的管线痛点,文中开头交代,非外部视频,已声明)
- [x] what I actually practiced is concrete(三处规则改动 + 新建 skill + 走播动画实现方式)
- [x] real results/data/outputs are included(节点数、时间轴参数、四项验证结果、选型对比结论)
- [x] verified vs. untested claims are separated(专门一节:RSS 表现未测、反爬外链误报未遇到)
- [x] my own post-practice judgment is present(判断/机械检查分离、动画编码真实流向)
- missing stages explicitly declared (if any): 无外部视频/课程来源,开头已说明这是自己管线的返工记录

## Links collection maintenance

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| https://github.com/konraddzbik/architecture-diagram-skill | no(对比参照,文章不围绕它展开) | inline-only | - |

## Draft direction

log 类型:时间锚定在 2026-07 初,记录这次管线返工 + 动图 skill 的实践全程,嵌入走播版流程图作为成果展示。

## Rewrite plan

### Keep

- 三处规则改动的动机与具体内容
- animated-flow-explainer 的选型过程与技术决定(零依赖内嵌片段)
- 走播动画的实现要点(单一 14s 主时间轴 + per-element delay)
- 四项验证结果与两个未验证项

### Remove / anonymize

- 本地绝对路径、会话内部细节、subagent 编排细节中与读者无关的部分

### Add / refresh

- 嵌入式动图本体(文章即 demo)

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| 社区最接近的现成 skill 是 architecture-diagram-skill,输出为独立交互页 | https://github.com/konraddzbik/architecture-diagram-skill | 2026-07-02 | yes(subagent 深读) | n/a |
| demo 图通过桌面/移动/暗色/reduced-motion 四项检查 | design-previews/verify/pipeline-{desktop,mobile,dark,reduced-motion}.png(脉冲版)+ walk-frame{1,2}.png(走播版两帧,证明包移动与节点点亮同步)| 2026-07-02 | yes | 最终文章路由的四项复验在 preview 阶段由 ui-verify + 定向截图完成,见 Mechanical verification notes |

## Required publishable frontmatter plan

Shared:

- title: 发布管线的三道门,和一张会动的流程图
- description: 给博客发布管线加上强制 subagent 评审、机械 eval 和 links 维护规则,顺手做了一个生成内嵌动态流程图的 skill。
- date: 2026-07-02
- tags: ["agents", "publishing-pipeline", "eval", "svg-animation"]
- visibility: public

Collection-specific:

- logs: period: "2026-07 第一周", summary: 管线返工 + 动图 skill 实践记录

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.(仅涉及一个 GitHub 仓库,当日核查)
- [x] Benchmark/metric claims refreshed or removed.(无)
- [x] Security claims phrased defensively and without operational attack detail.(无安全内容)
- [x] Hypothetical examples labeled as hypothetical.(无)
- [x] Public links/repo/demo/result claims verified.(见 evidence table)

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [x] Internal KB/local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | editor:清晰可复述(判断类 vs 机械类检查分离) |
| Reader payoff | 2 | editor:可复制的设计与失效机理 |
| Specificity | 2 | editor:判据、数字、未验证边界俱全 |
| Structure | 2 | editor 初评 1(三道门框架未兑现),按其方案重构小节后复核为 2 |
| Source grounding | 2 | source 初评 1("三个月/几十个"无据、证据未落盘),已改为实数并落盘截图后复核为 2 |
| Judgment density | 2 | 取舍明确(管线变重是否值得、门 vs 返工成本) |
| Voice | 2 | 对抗评审:仅 1 处破折号命中,已修;无其他 AI 腔 |
| Safety/privacy | 2 | 对抗评审 grep 泄漏检查全零命中 |
| Freshness | 2 | 唯一外链当日核查;时间锚定准确 |

Total: 18/18(其中 Structure/Source grounding 为修复后复核分,初评见各 reviewer 记录)

## Review loop

### Editor review

- reviewer: subagent(独立上下文)
- pass: yes
- blockers: none
- major edits: (1) 标题"三道门"框架未在正文兑现,小节"改了四处"计数漂移;(2) 首句合规声明对公共读者是噪音;(3) 落点把动画类比硬缝进检查分法。三条均已按建议修复:小节改为「三道门,两条配套规则」并开头点破结构;删首句声明;落点拆成两条独立记录。
- minor edits: "亮点包"改"流动的光点";review 文件加半句 gloss;visual-explainer 细节删减;frontmatter"顺手做了"改为与正文一致的"现成方案不合用,自建"。均已应用。

### Source/factual review

- reviewer: subagent(独立上下文,对照真实 diff/git 历史/外链实访)
- pass: no(初评);blocker 修复后达标
- blockers: 「收藏页三个月只躺着三条」不实(links 集合建于 2026-06-14,约两周半)。已改为「两周多只躺着三条」。
- claims needing refresh/removal: 「这周没发新内容」与当日两笔本地提交冲突,改为「这周先没急着发新文章」;「几十个来源」实测 25 个,改为「二十多个」;「图过了四项检查」证据未落盘,已将截图存 design-previews/verify/ 并在 evidence table 记路径,最终文章路由在 preview 阶段复验。
- notes: 其余关键断言(规则原文、eval 判据、links 口径、外链三点描述、走播时间轴数值)全部抽查通过;review 文件"三处规则改动"笔误已更正为四处。

### Adversarial review

- reviewer: subagent(独立上下文)
- pass: no(初评);blocker 修复后放行
- blockers: figcaption 一处破折号(作者硬性排除项)。已改逗号,正文与 demo 文件同步修正。
- non-blocking risks: 元文章题材不宜连发;"评审者会替作者补完意图"是断言非实测;走播首轮"发布"高亮出现在 15.2s(相位偏移,后续周期正常)。均记录,不改稿。
- required revisions: 仅破折号一处,已完成。泄漏 grep 全零命中;外链 200 + MIT 核实;可访问性(aria-label/reduced-motion)获正面评价。

### Eval review (links/images, after build)

- reviewer: subagent(独立于写稿 agent)
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://github.com/konraddzbik/architecture-diagram-skill(正文唯一外链) | 200 | pass |
| https://fonts.googleapis.com/css2?family=Fraunces...(模板样式表) | 200 | pass |
| https://kevinwangsheng.github.io/my-blog/og.png | 200 image/png | pass |
| preconnect 裸域 fonts.googleapis.com / fonts.gstatic.com | 404(根路径,正常,非文档链接) | pass(注释见 eval 输出) |
| 本文 self-canonical(线上) | 404(未发布,预期;同模式已上线文章 200) | pass(发布后自解) |
| 站内链接 14 条 | dist 内全部存在且非零字节 | pass |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| (无 img 元素,配图为内联 SVG) | n/a | n/a |

- rendered check run: yes(由 ui-verify 覆盖:375/768/1440 截图 + axe + Lighthouse + console)
- broken items and fixes: none。非阻塞建议:canonical/og:url 统一补尾斜杠避免一次 301(未改,记录在案)。

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| figcaption 破折号(对抗评审) | 改逗号;文章与 demo 同步修 | yes |
| 「三个月只躺着三条」不实(source 评审) | 改「两周多」,与 git 历史一致 | yes |
| 标题框架未兑现(editor,major) | 小节重构为「三道门,两条配套规则」并开头点破 | yes |

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: agent
  date: 2026-07-02
  notes: 三路独立 subagent 评审完成;3 个 blocker 与全部 major edits 已修复并复核;voice.md 为模板态,本篇按 §0 基调 + 通用真人味撰写,已向作者声明。
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

- content:check: pass(manifest 模式,无 warnings)
- content:sync: pass(logs/publish-pipeline-three-gates.md;tabindex 修复后 --overwrite 重同步)
- build: pass(19 pages,1.16s)
- preview URL: http://127.0.0.1:4327/my-blog/logs/publish-pipeline-three-gates/(200)
- ui-verify if run: 首轮 1440px 报 scrollable-region-focusable(serious);figure 加 tabindex="0" 后复跑全绿:axe 0/0/0,console 0,overflow no,Lighthouse 100/100/100/100(out/summary.json)
- 暗色/reduced-motion 定向复验: design-previews/verify/article-dark.png(走播正常、暗色配色正确)、article-reduced-motion.png(静态完整、无残留光点)
- leak check: grep 全零命中(staged md、synced source、dist HTML)
- rejection cleanup if needed: 未触发
- 已知边界(非阻塞):图的明暗跟随系统 prefers-color-scheme;若站点手动切换主题与系统相反,图与站点主题可能不一致,后续可改挂站点主题机制
