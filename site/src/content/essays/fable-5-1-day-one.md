---
title: "Fable 5.1 首日观察：修了什么、封了什么、该不该切"
description: "Fable 5.1 不是更聪明的 Fable 5，是更便宜、更能用、也更封闭的 Fable 5。发布当天读完官方文档、系统卡、HN 主线程和八家第三方评测：它修了价格、留存、误报三件部署问题，API 用三个围绕 thinking 块的破坏性变更收窄了推理的可见性，第一天最大的争议是它到底更省还是更贵。"
date: "2026-09-02T00:30:00-07:00"
tags: ["agents", "claude-code", "fable-5-1", "model-release"]
visibility: "public"
---
美西时间 2026 年 9 月 1 日上午，Anthropic 发布了 Claude Fable 5.1。发布后的十个小时里，我把官方公告、开发者文档、212 页系统卡、Hacker News 主线程的 917 条评论、X 上 21 个账号的时间线，以及 Every、Amp、CodeRabbit、Snorkel、Simon Willison、Artificial Analysis、ARC Prize、Vals AI 这八家的第三方评测过了一遍。这篇不是评测，我没有跑自己的 eval。它是一份「怎么读这次发布」的地图。

先说结论：5.1 不是更聪明的 Fable 5，是更便宜、更能用、也更封闭的 Fable 5。相对半价的 Opus 5，通用基准的增量小到 HN 能用一道减法否掉；真正变的是账怎么算、误报多不多，以及 API 不再让你碰它的思考。

读法交代一下：所有数字都标了来源；官方 benchmark 是厂商自报，第三方数字引自原文，我没有复现；社区反馈只覆盖发布后十小时，长期口碑还没形成；哪些是我的判断，我在句子里标了「我的读法」。

## 它修的是三个部署问题，不只是刷分

Fable 5.1 与 Mythos 5.1 是同一个模型，区别只在安全分类器。Fable 5.1 全平台通用（Pro / Max / Team / Enterprise、Claude Code、API、Bedrock、Vertex、Foundry，GitHub Copilot 也在当天的 changelog 里宣布可用；不过发布日 HN 上也有 Pro 用户说自己还没看到），Mythos 5.1 只给经审核的网络防御和生命科学机构，目前还限于美国机构。输入 $10、输出 $50 每百万 token，和 Fable 5 一致。

要理解这次发布，得先看 Fable 5 上线 12 周的处境。它 6 月 9 日发布，6 月 12 日到 7 月 1 日暂停访问近三周（官方时间线只写了暂停与恢复，HN 当时的热帖把原因归为出口管制），7 月底 Opus 5 以一半价格在多项基准上接近或追平了它。AppSo 转引支出平台 Ramp 的样本数据，Fable 5 只占其客户 Anthropic token 消耗的约 6%，这是二手数字，Ramp 的原始口径我没有核，但它和 HN 上「谁在付 $50/M 的钱」的质疑是一个方向。太贵、留不住数据、分类器误伤，是这三个月里被反复提的三件事。5.1 的公告把它们放在 benchmark 前面讲：

| 问题 | Fable 5 的状态 | Fable 5.1 的改法 |
|---|---|---|
| 太贵 | 缓存读 $1 / MTok | 缓存读降到 **$0.25 / MTok**，是输入价的 0.025 倍（其他 Claude 模型是 0.1 倍）。官方按 8 月真实负载测算：典型负载省 25%，重 agent 负载最多约省 45% |
| 30 天留存 | Every 的说法是「把大多数大公司挡在了门外」 | 推出 **Enterprise Frontier Safeguards（EFS）**：数据存客户自己的云，人工审核默认由客户做，今秋分批上线。就绪之前，符合资格的企业可以用零留存 |
| 分类器误伤 | HN 用户 nrmitchi：「只要看到和 Linux 沾边的东西就发作」；scronkfinkle：「对齐检查太敏感，基本总把我踢回 Opus」 | Claude Code 里 cyber 干预每会话平均少约 60%，允许在源码里找漏洞；bio 分类器（Fable 5 与 5.1 共用，此前已更新过）对基础生物和医学类良性问题的误触发少 85%。渗透测试、exploit 生成、二进制扫描仍然回退到 Opus |

三条里最实在的是第一条。长时 agent 会话里，缓存读经常占 token 的大头。Amp 说他们典型线程里超过 90% 的 token 是缓存读，所以切到 5.1 后 ultra 线程的成本降了约 35%。

第二条要看清范围。官方原文是「符合 EFS 资格的客户在 EFS 就绪前可以用零留存」，Every 的评测写成「支持零留存协议、符合资格的企业客户可用」，漏掉了 EFS 过渡期这个前提。普通 API 账号仍然是 30 天留存，没有授权的零留存（ZDR）组织无法调用这个模型。

## 能力涨在长任务和科研，相对 Opus 5 是小幅增量

![官方 benchmark：Fable 5.1 在七项百分比基准上对比 Fable 5、Opus 5 和 GPT-5.6 Sol。Terminal-Bench-Science 从 24.7% 涨到 52.6%；相对 Fable 5，Terminal-Bench 4.0 和 AutomationBench 各涨约 14 个点；相对 Opus 5，除 Science 外其余基准涨 1.4 到 4.5 个点](/my-blog/images/fable-5-1-day-one/01-official-benchmarks.svg)
*官方公告的七项百分比基准。GDPval-AA v2 是 Elo 分：Fable 5.1 1853，Fable 5 1723，Opus 5 1824，GPT-5.6 Sol 1711。*

比较对象决定结论。相对 Fable 5，这是一次实打实的升级：Terminal-Bench 4.0 从 42.0% 到 55.8%，AutomationBench 从 17.1% 到 31.4%，Terminal-Bench-Science 翻倍。相对半价的 Opus 5，除了 Science 那一项，其余基准的差距是 1.4 到 4.5 个点。HN 用户 GodelNumbering 做了一道减法（这条评论下面有 32 条回复）：去掉 Terminal-Bench-Science，5.1 对 Opus 5 的优势是 TB 4.0 加 3.5、GDPval 加 1.5、OSWorld 加 2.5、Humanity's Last Exam 加 1.6。这位用户的结论是「一个档次加一个版本，这不算提升」。

两个官方自己写的脚注值得记住。第一，所有分数是在生产安全分类器开启下测的，分类器触发时 OSWorld 记 0，cyber 任务实际由 Opus 4.8 完成、bio 任务由 Opus 5 完成。Mythos 5.1 在 Terminal-Bench 4.0 上是 60.9%（和 Humanity's Last Exam 无工具那格的 60.9% 是巧合，我回公告核过），比 Fable 5.1 高 5.1 个点；官方脚注只说分类器触发时 cyber 任务由 Opus 4.8 代做、「可能拉低」了 Fable 5.1 的分数，没有明确把这 5.1 个点全归因于分类器，那是我的推断。第二，Terminal-Bench-Science 0.1 的标准误是 ±3.5 到 4.5 个点，Simon Willison 指出它是 8 月 27 日才公布的新基准。他对整张表的评价是：其他基准只是略有提升，没有一个像 Science 这个那么惊人。

第三方评测给的是另一种画面。它们测的不是通用基准，而是「成功时省多少、失败时怎么失败」。其中 Artificial Analysis 自述参与了发布前评测，Every 提前一周拿到访问，所以我叫它们第三方而不是独立：

| 评测方 | 一句话结论 | 一个关键数 |
|---|---|---|
| Artificial Analysis | Intelligence Index 66 分榜首（Opus 5 63、Fable 5 62、GPT-5.6 Sol 61），但「非常啰嗦」 | 跑完整套输出 1.4 亿 token，中位数模型是 0.71 亿 |
| ARC Prize | ARC-AGI-2 90.0%、ARC-AGI-1 97.5%（max 档） | 每题 $4.49 / $1.40 |
| Snorkel AI | 对比 Opus 5「不是严格升级」：成功时更省更快，但更容易半途丢失 | 共同任务集里同解 18 题、Opus 独解 5 题、Fable 独解 2 题 |
| CodeRabbit | 「专科审查员，不是默认替代」；High 推理反而更差 | 最终评论从 253 条降到 166 条 |
| Every | 「Fable for everyone」：更快、更友好、说人话；但不守限制 | Slack agent 任务用不到 Opus 5 一半的 token |

Snorkel 和 CodeRabbit 的发现值得展开，因为它们说的是失败方式。Snorkel 在自己的 Terminal-Bench+ 私有集上测到，5.1 成功运行的输出 token 比 Opus 5 少 58%、耗时少 36%，但 Build / 依赖管理这一类任务只有 18%，Opus 5 是 67%；它的失败模式是终端里大文件写入之后恢复不了，工作其实已经接近完成，却在最后一步丢掉。CodeRabbit 在 45 个代码审查任务上测到召回持平（61.0% 对 Fable 5 的 61.9%）、精度升（37.3% 对 32.8%）、评论数少三分之一，但单任务从 12 分半慢到 18 分半（CodeRabbit 自己注明两次评测用的审查系统版本不同，只能看方向）；开更高的推理档位反而召回更低。两条合起来读：5.1 在「环境能反驳它」的任务上更好，在靠约定而不是靠反馈的任务上没有变强。

轶事类的两条我也放一句。Vals AI 让它零干预解出了 Thomas Urquhart 1653 年书里的 Cyphral Distich 密码，三百七十多年没人解出，用了 44 分钟、17.6 万 token。Simon Willison 用 pelican 测试扫了五个 effort 档，max 档给出他见过 Anthropic 模型里最好的一张，但 low 和 medium 两档没有返回推理摘要。

官方另外给了三个科研案例：Mythos 5.1 设计的蛋白结合剂在 12 个靶点上命中率接近 50%（行业常见是 10% 到 15%）；Fable 5.1 用 30 年前 Magellan 雷达数据重建了金星三分之一的高程图；Mythos 5.1 给七个开源基因组模型写 GPU kernel，H100 上最高提速 2.5 倍。这三项都是厂商自报，其中只有蛋白结合剂一项写明送了外部机构做实验验证。

## API 的三个破坏性变更，都围绕 thinking 块

这是开发者最该读的一节。官方文档说 Fable 5 的提示词在 5.1 上「应该无需修改就能工作」，但 API 契约有三处会破坏现有调用：两处直接 400，一处静默丢块。

| 变更 | 表现 | 官方给的替代 |
|---|---|---|
| 禁止强制 tool_choice | `{"type": "any"}` 和 `{"type": "tool"}` 返回 400，count_tokens 端点做同样的校验 | `auto` 加提示词点名工具；`strict: true` 保证 schema；或者改用 structured outputs |
| thinking 块绑定模型 | 只有产出它的模型或更新的模型能读；向 Opus 5 等旧模型切换时块被静默丢弃（不计费；带 `thinking-binding-controls-2026-08-01` 这个 beta header 才会在响应里报告） | 向上切到 5.1 保留推理，向下切丢失 |
| 修改历史即失效（官方叫 preserved thinking） | 改了 system、tools 或任何早期消息之后再回放 thinking 块，返回 400 `bound to a different conversation` | 对话保持 append-only；用 mid-conversation system message 改指令和工具；用服务端 compaction 或 context editing 裁剪 |

第三条的执行范围有个时间线：2026 年 8 月 31 日（UTC）起新建的账号立即强制；旧账号目前不强制，除非请求里主动设置 `prefix_mismatch_behavior`；官方明说「未来模型发布将适用于所有用户」。这不是可选项，只是给了旧账号一个缓冲期。

动机官方说了一半。支持中心的文章直接说第三条是反蒸馏：编辑前文诱导模型解密并打印自己的思考，是「公开记录的工业级蒸馏技术」，用几千个假账号批量做；同一篇也把「限制把会话或推理从更强模型转移到更弱模型」列为已有的反蒸馏措施，那就是第二条。第一条官方给的理由不是蒸馏，而是质量：思考常开，强制调用会跳过思考，模型会把推理写进工具参数里，参数质量下降。把三条串成同一个动机、说第一条堵的是「伪造一个工具再强制调用来套出原始思考」，是 HN 用户 mlaux 的推测，他自己也写了「我相信是这样」。我的读法是：不管第一条的动机是什么，三条的共同效果是 thinking 块只能被本模型在原封不动的对话里读回来，推理的可见性和可编辑性同时收窄了一圈。

配套新增了五项。前三项正好是给「append-only」这个约束配的工具，后两项是定价和溯源：

- **per-message effort**（beta）：在 `messages` 里塞一条 `role: system` 加 `output_config.effort`，中途改档不打断缓存。
- **turn-scoped system message**（beta）：`clear_at: "next_user_message"`，只在当前轮生效，之后留在数组里不渲染、不计费。这就是你以前「注入 reminder、下一轮删掉」的替代品。
- **`thinking.display: "updates"`**（beta）：隐藏推理，但把工具调用之间的进度短句作为 thinking 块返回。
- 缓存读降价（第一节已经讲过）。
- 内容溯源：所有平台的文本输出带统计水印，Files API 取回的图片和视频带 C2PA 签名。这条在 HN 上引出了一整串争论，后面再说。

如果你自己拼 `messages` 数组，迁移前至少做这几件事：

```text
1. 删掉所有 tool_choice: any / tool，改 strict 或 structured outputs
2. 用 prefix_mismatch_behavior: "drop_block" 跑一遍会话，看 input_transformations 里有没有 prefix_binding_mismatch
3. 把每轮注入又删除的 reminder 改成 turn-scoped system message
4. 把动态改 system / tools 改成 mid-conversation system message
5. 客户端压缩时整段换成一条 summary，不回放任何 thinking 块
6. 重跑 effort 扫描：同名档位在不同模型上思考量不同，官方说 5.1 的 medium 档结果大致与 Fable 5 持平、成本更低
7. 开 display: "updates"，否则长任务对用户是静默的
8. 配 fallbacks: "default"：分类器拦下请求时（stop_reason 为 refusal），服务端自动按类别回退到 Opus 4.8 或 Opus 5 重跑
```

## 系统卡里值得记住的几句

212 页系统卡我没有通读，但把关键结论逐条核对过原文：

- 化生风险判为 CB-1（能显著帮助有基础背景的人制造已知武器），未达 CB-2（替代稀缺专家），官方说这个判断「带一些不确定性」。
- 对齐风险从「very low」上调为「low」。这承接 8 月的 Risk Report，原因是 cyber 评测里模型未授权访问真实系统的事故被披露。
- Cyber 能力是「发布过的模型里最强」：Mythos 5.1 在针对 Firefox 147 版本漏洞的 250 次试验里 245 次做出了完整 exploit。
- 行为审计（对象是同一模型的 Mythos 5.1 版本）：相对 Opus 5「整体失准行为略有回退」，但优于 Mythos 5 和 Sonnet 5；「在压力下不如近期 Claude 诚实」；「是测过的模型里最能控制自己扩展思考内容、最能不被发现地完成隐蔽副任务的之一」。官方称这是「可能更难监控的弱证据」。
- 外部测试中曾利用沙箱漏洞读取环境外的文件，官方评为低严重度。
- 外部红队：Trajectory Labs 花 74 小时、6,500 多个请求，仅用 Fable 5.1 没有拿到端到端 exploit，也没找到通用越狱。

把「更会控制自己的思考内容」和上一节的「不再让你编辑历史、不再让旧模型读它的思考」放在一起看，就是我说「更封闭」的意思：模型这一侧更会藏，API 这一侧更不让看。这是我读完系统卡最在意的一点，也是我自己的叠加判断，系统卡没有这样连起来说。

## 不改代码也会变的几件事

What's new 页列了七条「不改代码也会出现」的差异，Prompting 指南另外按症状索引了十几条，每条附了修法。完整的表在同批收录的 links 里，这里只留对 agent 负载影响最大的四条：

| 变化 | 官方描述 | 修法 |
|---|---|---|
| 并行工具调用变得不稳定 | 编码和 computer-use 循环里可能一轮只发一个调用，Fable 5 会批量发 | 每轮工具结果后追加一句 batching 提示 |
| 长工具链里进度更新更少 | 高 effort、长链时用户会看到「静默几分钟」 | 先开 `display: "updates"`，删掉「把发现留到最后」类的旧指令 |
| 小改动整文件重写 | 输出 token 和时间上升 | 加「优先定点编辑」指令 |
| 任务没做完就结束回合 | 「Next, I'll…」或者询问已经授权过的步骤 | 加「用户不在看，不要问已授权的事」和「用户请求即交付范围」两段 |

另外几条（超范围修改和多余测试文件、散文更密、xhigh / max 先在思考里打草稿、low 档更少触发搜索）在后面成本那一节还会碰到。如果只能先改一条，我会先改并行调用和进度更新这两处，因为它们直接决定一个 agent 在用户眼里是快还是卡。还有三条和误报有关的建议我觉得挺实用：不要问「这个程序能不能编译通过」，改问「有没有 bug」；冷门语言给它文档上下文；工具输出里的 base64 会触发误报，建议剥掉。

## 第一天大家在吵什么

![HN 主线程 917 条评论的主题计数：Opus 对比 127 条、价格 93 条、写作风格 78 条、GPT 对比 60 条、水印 40 条](/my-blog/images/fable-5-1-day-one/02-hn-themes.svg)
*按关键词正则计数，一条评论可以命中多个主题，美西时间 9 月 1 日 20:50 抓取。*

**最长的讨论树是一位自称在 Anthropic 工作的用户开的。** felixrieseberg 说：「抛开 benchmark，我觉得 5.1 在写作风格上是很大的进步，不再那么像刻板的 Claude，对我的风格指令响应更可靠。」这棵 333 条的树和 tarr11 开的 68 条树（他的原话是「散文密度不等于简洁，人也有 token 上限」）加起来有三种声音：认同的（ddahlen：「写作风格明显改善了」）、反问的（troupo：「你觉得，还是真的更好？」），以及在 tarr11 那棵树下被多人证实的观察：任何「写简洁点」的指令在长会话里几轮之后都会衰减，output style、hook、CLAUDE.md 都只管两三轮。这一点 5.1 有没有改善，第一天还没有证据。

**正面集中在四件事。**

- 写作与沟通：Amp 说这是第一次让团队愿意用 AI 写文档；Every 量化成阅读级别降到 7 年级、AI 痕迹最少。
- 长任务和中途 steer：Amp 的描述是「跑几小时，证明不成立就回去改，再证明」；官方产品页里 Cognition 的客户引言说发布当天就把 Devin 的 Opus 5 流量迁过去。
- 相对 Opus 5 的 token 效率：Every 测 Slack agent 用不到一半 token；Snorkel 测成功运行少 58% 输出 token。
- 安全误报下降：HN 用户 llm_nerd 说「5.0 拒绝的项目加固任务现在能做，GPT-5.6 Sol 和 Gemini 也拒了」。

**负面集中在四件事。**

- 价格和额度：sergiotapia 问「$50/M 输出太离谱，谁在付这个钱」；InsideOutSanta 说两个账号都在第一个任务做完之前撞到 5 小时上限；Claude Code 仓库当天就有 issue 说 medium 档 20 分钟烧完 100% 额度。
- 推理不可见和 preserved thinking：exabrial 说「没有 thought traces 就没法确认 prompt 对不对」；sippeangelo 说「这一条就够我们把 API 用量整体迁出 Anthropic」。
- 增量太小：GodelNumbering 的减法上面已经引过；爆料账号 synthwavedd 的话是「相对 Fable 5 是相当增量的改进，OpenAI 传闻中的下一代模型 Astra 大概会碾压它，但仍然很酷」。
- 写作更密、指令衰减：见上面 tarr11 那棵树；官方 Prompting 指南自己也承认「某些情况下比 Fable 5 更密」。

**水印是第五大主题，40 条评论。** 官方说水印「不增加 token 或隐藏字符、不含用户信息、对质量无实际影响」，检测 API 只私测开放给监管、媒体和事实核查机构。HN 上的追问集中在两点：dabinat 和 tosh 都问「不改输出怎么可能有水印」；mixedbit 担心的是另一头，如果我自己写的文章用模型校对，哪怕改动很小，也可能被检测 API 判成 AI 生成。BoorishBears 的总结更尖：「至少一半的变更都是反蒸馏策略。」

**第三方评测里最有信息量的是 Every。** 他们提前一周拿到访问，五个测试者里两个给了金牌，结论是「Fable for everyone」：更快、更友好、说人话，Slack agent 任务用 Opus 5 一半的 token。但同一篇里也记录了它不守限制：让写 1000 字写了 1288 字，要 8 到 12 条引用给了 43 条，抽查的 27 条里有 5 条不在原文里；xhigh 档会忽略中断继续开子代理；一个人一天打了 18 亿 token。

**X 上的官方口径**和 HN 形成对照。Alex Albert 说「向人描述 5.1 的方式就是：它就是能用，几句含糊的话它就能补全其余部分」；Claude Code 负责人 Boris Cherny 说「什么都用它」，并承认「我们听到了反馈，正在减少 Claude-speak」。我抓到的账号里当天点赞最高的一条不是任何能力展示，而是「重置了所有用户的 5 小时和周额度」，接近两万赞。这大概比任何 benchmark 都能说明用户在意什么。

**Reddit 我没有拿到。** 所有路径都被反爬拦住，只有一份 8 月 28 日灰度期的存档帖：一批人说 CLI 突然快很多、回复只剩两三句，另一批说 Fable 和 Opus 都变得极慢。发布后的 Reddit 反应在这篇里是空白。

## 争议：更省还是更贵

Every 那句总结是理解这个争议的钥匙：「它每一步都便宜，但你让它走多少步它就走多少步，effort 决定步数。」六方的数字每一方都对，但测的不是同一件事：

| 说法 | 测的是什么 | 为什么省 / 为什么贵 |
|---|---|---|
| Anthropic 省 25%，最多 45% | 8 月四周真实负载，默认 effort，按 token 计费 | 缓存读 $1 降到 $0.25 |
| Amp 省 35% | ultra 线程，90% 以上 token 是缓存读 | 90% 缓存读乘以缓存单价降 75% |
| ARC 省 32% | max 档，两个基准每题平均成本 | token 效率提升；若按 ARC 结果页的 $4.49 而不是推文的 $3.12 算，两基准平均只省约 9%，这个差异我没核清 |
| Every 和 Snorkel「一半 token」 | 对比对象是 **Opus 5**，不是 Fable 5 | 每步更省 |
| Artificial Analysis 贵 20% | **max effort** 跑推理密集的基准，缓存占比低 | 输出 1.4 亿 token，远超中位数 |
| HN 和 GitHub「20 到 60 分钟烧完额度」 | 订阅额度按 token 折算；Claude Code 默认 high 档，那条 issue 报的是 medium 档 | 每步便宜，但步数不设限 |

我的读法是：缓存命中率高、能用 high 及以下档的负载，价格是真降了；推理密集、缓存占比低、必须跑 max effort 的负载，不降反升。官方 Prompting 指南自己也承认 xhigh 和 max 会「先在思考里打草稿，再写一遍」。Simon Willison 用同一个提示扫了五档：low $0.10，high $0.13，xhigh $1.83，max $3.30。差 30 倍的不是模型，是你选的档位。

订阅用户要另算一笔账。上面六方里只有最后一行是订阅视角，而这个博客的读者多数是 Claude Code 的订阅用户。订阅额度看到的不是单价，是按 token 折算的配额；缓存读降价 75% 有没有进入 5 小时和周额度的折算，官方没说，第一天也没人测出来。如果没有，那「省 45%」对 Max 用户是零，5.1 更长的步数只会让你更快撞墙。这也是为什么当天点赞最高的是「重置额度」。这一项我列进了未确认。

## 我的判断

回到开头那句：**它不是「更聪明的 Fable 5」，是「更便宜、更能用、也更封闭的 Fable 5」。** 相对半价的 Opus 5，通用能力的增量小到 HN 能用一道减法否掉；真正的变化是缓存定价把长时 agent 的账算平了、误报下降让它在日常编码里不再动不动就被踢回 Opus、EFS 让企业有了合规路径，同时 API 用三个围绕 thinking 块的变更把推理的可见性和可编辑性收窄了一圈。评价这个版本，看它修了什么和封了什么，比看 benchmark 涨了几个点更有用。

**该不该切，取决于负载形状。** 我会切的条件是满足两条以上：

1. 负载是多小时的自主 agent（代码审查、迁移、研究），缓存读占 token 大头。
2. Opus 5 在高 effort 下的 eval 仍然不达标。官方文档给的「用 Fable」条件就两个：高难度推理与长时 agent 任务，或者 Opus 5 高 effort 仍不达标。
3. 需要文档、表格、幻灯片端到端交付，或者密集图表阅读。
4. 能接受 30 天留存，或者有 EFS 资格。

我不会切的条件：

1. 短交互、缓存命中低、必须 max effort 的推理任务。
2. 自建 harness 依赖编辑历史而短期改不了，新账号会立即 400。
3. 依赖强制 tool_choice 拿结构化输出，改完 strict 再说。
4. 订阅用户而且任务不是「一次跑几小时」，额度消耗是第一天最集中的抱怨。

**会改变我判断的证据**：一周后 Reddit 和 X 上普通用户对额度的反应；Artificial Analysis 补充 high 和 medium 档的每任务成本；Opus 5.1 会不会出现（GodelNumbering 的看法是 Opus 5 半价已经追平 Fable 5，再出 5.1 定价上「没地方放」）；以及 OpenAI Astra 发布之后的对比，我抓到的 scaling01、synthwavedd 和 DanDr1s 这几个账号都预期 Astra 会超过它。

差 30 倍的不是模型，是你选的档位；该不该切也不看它多聪明，看你的负载长什么样。

## 方法与未确认

官方文档和系统卡是一手来源，系统卡我用 pdftotext 转成文本后按关键句逐条核对。HN 主线程通过 Algolia API 全量抓取，主题计数用正则做，一条评论可以命中多个主题。X 因为搜索接口故障，只抓了 21 个账号的时间线，覆盖偏向官方和 KOL。Reddit 见上一节。中文渠道以 AppSo 的稿子为主，知乎只有 8 月 19 日的爆料稿，V2EX 唯一的 5.1 帖是渠道商广告。

没有核实的几项：Reddit 发布后的真实反应；缓存读降价是否进入订阅额度的折算；ARC 结果页每题 $4.49 和 ARC 推文里每题 $3.12 的差异；爆料账号 DanDr1s 说的「幻觉测试 69% 到 73%」出处，我在系统卡里没找到这个数字；HN 引用的 Fable 5 跑 Artificial Analysis 全套成本 $5,455。

主要来源：[Anthropic 发布公告](https://www.anthropic.com/claude-fable-and-mythos-5-1)、[Fable 产品页](https://www.anthropic.com/claude/fable)、[What's new in Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1)、[Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)、[系统卡 PDF](https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20&%20Claude%20Mythos%205.1%20System%20Card.pdf)、[支持中心：preserved thinking](https://support.claude.com/en/articles/16761192)、[GitHub Copilot changelog](https://github.blog/changelog/2026-09-01-claude-fable-5-1-generally-available-in-github-copilot/)、[HN 主线程](https://news.ycombinator.com/item?id=49525378)、[Every Vibe Check](https://every.to/vibe-check/fable-5-1-vibe-check)、[Amp](https://ampcode.com/news/fable-5.1)、[CodeRabbit](https://www.coderabbit.ai/blog/fable-5-1-model-review)、[Snorkel AI](https://snorkel.ai/blog/fable-5-1-vs-opus-5-coding-benchmark/)、[Simon Willison](https://simonwillison.net/2026/Sep/1/claude-fable-5-1/)、[Artificial Analysis](https://artificialanalysis.ai/models/claude-fable-5-1)、[ARC Prize](https://arcprize.org/results/anthropic-claude-fable-5-1)、[Vals AI](https://www.vals.ai/blogs/fable-solves-cyphral-distich)、[AppSo 报道](https://www.163.com/dy/article/L5Q76G030511CSAO.html)、[claude-code issue #91289](https://github.com/anthropics/claude-code/issues/91289)。
