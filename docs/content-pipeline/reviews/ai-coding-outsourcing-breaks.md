# Review: AI coding 全部外包,现在一定会崩

## Metadata

- status: preview-ready
- source paths / source records:
  - user-provided reflective draft (conversation, 2026-07-02)
  - seed pointer: /Users/shenghuikevin/kb-vault/inbox/2026-07-02.md
- refreshed/primary sources:
  - https://www.youtube.com/watch?v=2n41YjR5QfU (Google I/O talk — cited per user framing; not independently verified by agent)
- proposed collection: essays
- proposed slug: ai-coding-outsourcing-breaks
- source type: public-original
- target reader: 每天用 coding agent、正在把越来越多决策外包出去、隐约感到失控的工程师
- planned publishable markdown path: docs/content-pipeline/manifests/ai-coding-outsourcing-breaks/ai-coding-outsourcing-breaks.md
- planned manifest dir: docs/content-pipeline/manifests/ai-coding-outsourcing-breaks/

## Public thesis

- memorable sentence: 自动化不消灭工作量,它只是把工作量推到你还没自动化、也最不想亲手做的那一环——现在那一环是 review。
- reader decision helped: 与其追求全自动,不如守一道小到自己真会看的 review 门(只守不可逆/决策动作)+ 把 agent 运行环境当一等公民维护。
- strongest counterpoint / edge case: 也许这只是当前模型代际的临时缺陷,下一代模型 + 更好的 agentic 检索会让"全自动"重新可行,届时"守门"的论点会显得保守。文中以"中间状态,不是终局"承认了这一点。

## Draft direction

保留作者原始随笔的全部核心论点与"我"的个人语气,把松散的情绪流收敛成有论证弧的公开文章:诱惑→滑坡→garbage 指数级→ADR 只能复盘→缺的是环境不是 reason→瓶颈守恒(Google I/O)→守一道守得住的门。加入"瓶颈守恒"作为可记忆的心智模型和读者收益。

### Keep

- 个人第一人称、略带愤怒的诚实语气("复盘时大概率是愤怒的"、"考古")。
- 全部原始论点:dangerous 模式滑坡、plan 的 context 不够、GIGO 指数级、workspace/检索污染、ADR 只能止损、缺的不是 reason、Google I/O 瓶颈传导。

### Remove / anonymize

- 无内部路径 / secrets / 私密项目数据需要脱敏(原文本身是抽象反思,无泄漏物)。
- 去掉原文口语重复("总之就是人太懒了"这类)并转成有收益的结尾判断。

### Add / refresh

- 加入"瓶颈守恒"模型作为记忆点与标题呼应。
- 结尾从情绪收束改为两条可执行判断(小门 + 干净环境)。
- Google I/O 观点用脚注标注为"一场讨论"并附链接,显式标注未独立核实。

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| Google I/O 讨论:下游加速→瓶颈移向 review→CI/CD | https://www.youtube.com/watch?v=2n41YjR5QfU | 2026-07-02 | 按用户转述,agent 未独立核实;已在脚注中限定为"一场讨论"并标注不确定 | n/a — 保留但已 scope |

无对个人已发布成果 / demo / 用户 / 外部背书的声明。

## Required publishable frontmatter plan

Shared:

- title: AI coding 全部外包,现在一定会崩
- description: 生成越快,越多的判断被推给 review;而 review 恰恰是人最想外包、也最难守住的一环。全部外包给 AI,崩只是时间问题。
- date: 2026-07-02
- tags: agents, coding-agents, workflow, review
- visibility: public

Collection-specific:

- essays: series = "Agent Workflows"; canonical 无

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain. — 仅 Google I/O 一处外部声明,已 scope 为不确定并附链接。
- [x] Benchmark/metric claims refreshed or removed. — 无 benchmark/指标声明。
- [x] Security claims phrased defensively and without operational attack detail. — 无攻击性安全内容。
- [x] Hypothetical examples labeled as hypothetical. — 例子均为通用工作流场景,非虚构具体成果。
- [x] Public links/repo/demo/result claims verified. — 仅 YouTube 链接一处,格式有效;内容按用户转述。

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [x] Internal KB/local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | 断言式标题 + 瓶颈守恒,中心主张锋利可记 |
| Reader payoff | 2 | 两条可执行判断:小门 + 干净环境 |
| Specificity | 2 | dangerous 模式滑坡、plan、ADR 考古、schema/删数据/部署/依赖 |
| Structure | 2 | 诱惑→滑坡→GIGO→ADR→环境→守恒→出路,弧线清晰 |
| Source grounding | 1 | 个人原创观点为主;唯一外部声明(Google I/O)未独立核实,已 scope |
| Judgment density | 2 | 通篇是判断与取舍,非罗列 |
| Voice | 2 | 保留个人第一人称与真实情绪 |
| Safety/privacy | 2 | 无泄漏 / 无虚构成果 |
| Freshness | 1 | Google I/O 声明未核实,已用脚注限定不确定性 |

Total: 16/18

## Review loop

三个角色由单一 agent 分三轮模拟(无独立 subagent);此为已知限制,记录在此。

### Editor review

- reviewer: agent
- pass: yes
- blockers: 无
- major edits: 将原随笔的情绪结尾改为两条可执行判断;加入瓶颈守恒模型作记忆点。
- minor edits: 段落顺序收敛为论证弧;去口语重复。

### Source/factual review

- reviewer: agent
- pass: yes
- blockers: 无(Google I/O 一处已 scope 为不确定并附链接;非 benchmark/vendor 硬声明)
- claims needing refresh/removal: 若日后核实 Google I/O 原视频内容与转述不符,应回来修正脚注。
- notes: 其余均为作者个人观点,无需外部核实。

### Adversarial review

- reviewer: agent
- pass: yes
- non-blocking risks:
  - 观点性强、断言标题("一定会崩")——属作者立场,已用"中间状态,不是终局"和最强反论(下一代模型可能让全自动重新可行)平衡,不构成 publish 风险。
  - 提到 AGENTS.md / DECISIONS.md 属作者本站已公开的通用概念,非私密。
- required revisions: 无

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Google I/O 转述未核实 | 脚注限定为"一场讨论"+附链接+review 元数据标注未独立核实 | yes(已 scope) |

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: agent
  date: 2026-07-02
  notes: 16/18,无 blocker,达到 sync(≥14)与 publish(≥16)门槛。三角色由单 agent 分轮模拟(已知限制)。
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

- content:check: ok (1 checked, 0 errors, 0 warnings)
- content:sync: ok → site/src/content/essays/ai-coding-outsourcing-breaks.md
- build: ok (25 pages, 1.05s); essay page built at site/dist/essays/ai-coding-outsourcing-breaks/index.html
- preview URL: http://127.0.0.1:4327/my-blog/essays/ai-coding-outsourcing-breaks/ (200)
- ui-verify if run: 未跑(内容页,无 UI/layout 改动;craft 特性已在构建产物中确认:drop-cap 首段以中文起头合格、pull-quote class×1、footnote popover×1、YouTube 链接×1)
- leak check: NO LEAKS FOUND(grep /Users/、kb-vault、docs/content-pipeline、private/机密/不发布 等,命中 0)
- rejection cleanup if needed: 若验收未过,revert site/src/content/essays/ai-coding-outsourcing-breaks.md 并将 review 置 needs-rework
