---
title: "Fable 5 的用法：先找到未知"
description: "解析 Thariq Shihipar 的 Field Guide to Fable：模型能力的 overhang、系统提示词为什么变短、unknown 四象限怎么用，以及为什么“be unreasonable”仍然离不开验收。"
date: "2026-07-06T10:10:00-07:00"
tags: ["agents", "claude-code", "fable-5", "video-notes"]
visibility: "public"
---
这篇是对 AI Engineer 频道 talk [Field Guide to Fable](https://www.youtube.com/watch?v=9fubhllmsBU) 的完整解析。讲者 Thariq Shihipar 在视频里说自己在 Anthropic 做 Claude Code。这支视频的时间语境有点特别：Anthropic 在 2026-06-09 发布 [Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)，6-12 暂停访问，6-30 公布 [redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5)，7-1 恢复访问。AI Engineer 频道上传这支视频时已经是 2026-07-06。

https://www.youtube.com/watch?v=9fubhllmsBU

所以我会把视频里的 Fable 能力例子都当作讲者在现场给出的经验和主张，不写成我自己已经复现实测过的结论。我的判断放在最后一节。

先说主线：这支 talk 表面在讲 Fable 5，其实更像在讲下一代 coding agent 的使用方式。模型更强以后，问题开始落到三件事上：给模型工具、暴露未知、让自己还留在决策里。

![视频把这支 talk 分成四段：unhobbling Claude、finding your unknowns、dealing with the grief、being unreasonable](/my-blog/images/field-guide-to-fable/01-field-guide.webp)
*视频 02:23 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

## 第一段：先别把 Claude 绑住

Shihipar 开场先用了一个比喻：Fable 像 RPG 里地图突然打开。以前还在 tutorial，现在进入 open world。机会变多，困惑也变多，所以他要给一份 field guide。

这份 guide 的第一部分叫 unhobbling Claude。hobble 是把脚绊住的意思。讲者并不是在鼓励“给模型完全自由”。他的意思更具体：模型的能力不是按人设计图纸长出来的，它更像被训练、反馈和计算资源“养”出来的东西。我们对模型的理解会落后于模型本身，结果就是 harness、提示词和工具反过来限制它。

他用一个很小的例子说明 capability overhang。有人问普通 chat model：哪些 Pokemon 名字以 `aw` 结尾？它可能答不出来。这个问题看起来怪，因为模型大概率“知道”所有 Pokemon 名字。但如果问 Claude Code，它可以抓取 Pokemon 列表，写脚本筛选，得到 Croconaw 和 Drednaw。

![视频用 Pokemon 例子解释 capability overhang：模型未必直接记得答案，但给它执行工具后就能自己查和算](/my-blog/images/field-guide-to-fable/02-pokemon-overhang.webp)
*视频 04:18 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

Pokemon 只是入口。真正值得看的地方是：模型能力会以很不均匀的方式出现。它可能不会在纯聊天里给出正确答案，但一旦给它 bash、网络、文件系统、脚本执行，它就能把问题改写成一个可验证的小程序。

Shihipar 接着把这件事放到 Claude Code 的历史里看。早期大家可能以为 coding 的解法是把上下文窗口变得巨大，把整个代码库塞进去。Claude Code 的洞察相反：给模型“手臂”，让它能搜索、运行命令、读取文件，它就能自己构造上下文。换句话说，工具不是附属品，工具会改变模型能触到哪一块能力。

这个思路也解释了他后面几个例子。

第一个是系统提示词。视频里他说，Claude Code 最近删掉了 80% 的 system prompt。早期经验是：小 system prompt、少量工具、很多 examples。后来模型更会遵循指令，就可以给更大的 system prompt、更多 examples、更多工具。但到 Fable 这类模型，examples 反而可能约束它，因为模型比示例更有想象力。于是他们更想给 context，而不是堆 constraints，尤其少写“不要做这个”。

![视频提到 Claude Code 删掉 80% 的 system prompt：更强模型可能不再需要那么多例子和禁止项](/my-blog/images/field-guide-to-fable/03-system-prompt.webp)
*视频 06:03 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

这个判断很容易被误读成“提示词越短越好”。我不这么看。更准确的说法是：当模型能力、工具和验收方式都变了，旧的指令密度可能开始变成负担。少写规则不是偷懒，它要求你把空间留给模型探索，同时保留真正必要的边界。

第二个例子是 AskUserQuestion（视频 slide 上这么写）。Shihipar 说这是他刚到 Claude Code 时做过的工具。最早在 Opus 4 上，模型勉强能调用一个 multiple choice dialog；到 Opus 4.5，它可以围绕 spec 连续问很多问题，像在采访你；到 Opus 4.8 和 Fable，它可以生成一整份 HTML report，把问题嵌在里面。

![AskUserQuestion 的演化：从能调用，到能采访，再到能把采访做进 HTML 报告](/my-blog/images/field-guide-to-fable/04-ask-user-question.webp)
*视频 07:38 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

这又是一个 spiky progression。它已经不是“同一个功能更准了一点”的变化，交互形态直接换了。模型从问一个问题，变成组织一场访谈，最后能做一份带问题的结构化报告。

第三个例子是 Markdown 和 HTML。Markdown 最早只是模型的输出格式。后来在 plan mode 里，Markdown 让人知道模型准备做什么。再往后，HTML 变成一种更丰富的报告和交互界面。这个方向和我之前写的《HTML 不是网页，是 agent 的视觉中间表示》能对上：对 agent 来说，HTML 不只是前端文件，它是一个可渲染、可检查、可迭代的结构。

Shihipar 用一句话收住这一段：这更像 biology，不像 physics。我们还不知道所有规则，只能通过经验观察模型怎么长出来、什么时候需要什么样的 harness。他也提到 Anthropic 的 interpretability 工作，尤其是 [Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model) 以及里面链接到的 “On the biology of a large language model”。

## 第二段：真正要解的是你的未知

第一段是 unhobble Claude。第二段反过来：unhobble yourself。

这里 Shihipar 用的是“map is not the territory”。你脑子里的 plan、prompt、spec 是 map；真实代码库、约束、运行环境、用户需求才是 territory。Claude 一旦遇到 map 里没有的东西，就进入一个 unknown：这是一个你没有事先写明的决策点。

Fable 这类模型的问题是，它走得更远，所以会撞见更多 unknown。以前模型走不了多远，你的 spec 模糊一点，问题可能停在第一公里。现在它能一直推进，模糊处就会变成一串实际决策。

他把 unknown 拆成四类：

1. known knowns：你知道自己知道，通常会写进 prompt，比如“我要什么”。
2. known unknowns：你知道自己还没弄清楚，比如某个 API 怎么接。
3. unknown knowns：你其实知道，但太习惯了，所以没写出来；设计里常见的“看了就知道不对”就在这里。
4. unknown unknowns：你完全没想到的变量。如果提前知道，它会改变你怎么提示 Claude。

这段是整支视频最有用的部分。因为它把“提示词写不好”换成了一个更工程的问题：怎么把未知变成可讨论、可记录、可验证的东西。

Shihipar 给了几种做法。

第一种是 blind spot pass。比如你要在一个代码库里接一个新的 auth provider，但你不懂这里的 auth module。你可以直接让 Claude 做 blind spot pass：帮我找出相关的 unknown unknowns，帮我之后把 prompt 写得更好。它可能去读 auth module，找那些经常出问题的死角，也可能在 git diff 或 Slack 里找上下文。这个方法不只适用于代码。他提到自己做视频剪辑里的 color grading 时也这么用。

![blindspot pass 的例子：让模型先帮你找任务里的 unknown unknowns，再回头改 prompt](/my-blog/images/field-guide-to-fable/05-blindspot-pass.webp)
*视频 11:00 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

第二种是 brainstorms and prototypes。有些东西你说不清楚，但看见就知道。设计尤其如此。视频里的例子是：我要一个 dashboard，但我没有视觉品味，也不知道有什么可能。请做一个 HTML 页面，给我四个差异很大的设计方向，让我可以反应。prototype 的价值在这里：它先把 unknown knowns 拉出来，让我看到之后才意识到自己想要什么、讨厌什么。

第三种是 interviews。等你大概知道自己要做什么，仍然会有很多没指定的地方。让 Claude 采访你。这里他强调了一点：要给更多上下文，比如“优先问那些会改变架构的问题”。否则模型可能问一堆表面问题。好的采访应该把真正影响实现方向的问题提早翻出来。

第四种是 references。Shihipar 的说法是：给 Claude 地图的最好方式之一，是给它另一张地图。你不一定要把 spec 全写出来，可以给它一段另一个系统或另一个语言里的代码，让它读懂你要的行为，再迁移到当前任务。如果做 React component，也可以给一个 HTML mockup。reference 的关键是减少空想，把意图落到一个已有结构上。

第五种是 implementation notes。如果 Fable 在执行时遇到 unknown，让它把这个 unknown 记下来。这样你事后能看到偏离发生在哪里、它当时为什么这么处理。这个习惯很朴素，但对长任务很重要。没有 notes，你只看到最后结果；有 notes，你能复盘模型在哪些岔路口做了决定。

第六种是 quiz me。任务做完后，让 Fable 问你发生了什么，确认你真的理解这个 PR 或这次 merge。Shihipar 说这是确保自己还在 loop 里的好办法。这个点我很认同。agent 做得越多，人越容易只看 diff 和 summary，最后变成“不知道自己批准了什么”。

## 第三段：变强之后会有失落感

第三段叫 dealing with the grief。这个转折有点意外，但也很真实。

Shihipar 说，第一次用到 Fable 这类模型时，他同时感到巨大的 gain 和 loss。他回忆 LLM 之前写代码像另一个国家。他以前做 YC startup，30 人左右，团队不断被迫在速度、质量、试新功能之间取舍。一个功能可能要一个月或两个月，所以必须选择。

后来他回到旧代码库，发现很多过去要几周的事，现在几个小时能做。他的反应不是单纯兴奋。视频里他讲得很直接：怎么能不笑？但也怎么能不想哭？他喜欢手写代码，喜欢把代码库放在脑子里旋转的感觉；但他也记得熬夜 debug、连续几周没有进展、项目失败。大多数项目失败，startup 破产，编程本来就很难。

他的结论是：不能回去。唯一的路是穿过去。继续学这种 agentic coding，继续学 Fable，同时保持自己在 loop 里。

这段对技术文章来说有点情绪化，但它很重要。因为很多 coding agent 讨论只谈效率，默认“更快”一定让人更开心。实际不是。工具替你拿走一部分痛苦，也会拿走一部分你熟悉的身份感。这个失落不需要被包装成反 AI，也不需要被压成鸡血。承认它，然后继续调整工作方式就行。

## 第四段：不要太早替现实做取舍

最后一段叫 being unreasonable。

Shihipar 说，他在 Anthropic 很喜欢的一点是“tradeoffs are not real”。这句话当然不能按字面理解。现实里成本、时间、风险都存在。但他的意思是：以前你可能太早把自己变得“合理”。先列优先级，然后接受这个季度只能做其中几件。现在模型和 agent 改变了工程成本，很多过去默认的取舍应该重新被挑战。

他把经典的 good、fast、cheap 拿出来说：现在是 pick three。更精确地说，我觉得这里的重点不在“永远都能全都要”。重点是先别在脑子里提前放弃。先要求好、快、便宜都要，让现实告诉你真正的瓶颈在哪里。

![视频把 good / fast / cheap 改成 pick three：先要求全都要，再让现实证明哪里真有取舍](/my-blog/images/field-guide-to-fable/06-pick-three.webp)
*视频 17:25 画面，© Thariq Shihipar / Anthropic / AI Engineer(YouTube)*

他给了一个现场例子：这份 deck 是他前一晚用 Fable 大约 4 小时做出来的。他觉得自己喜欢这份 deck，也做得很快。接着他把这个要求扩到 AI Engineer 这群人身上：世界在看你们证明 AI 有用，不只是 fad，而是真的能让人更 productive，也能省时间。

不过他最后又补了一个边界：building is easier, generating value is still hard。构建变容易，不等于价值自动出现。你仍然要打很多次，试很多次，才知道哪些东西真的有价值。

我觉得这句比 pick three 更重要。否则“be unreasonable”很容易被误解成盲目加速。真正合理的版本是：在构建成本下降后，多试一点、更早把想法做成实物；但对价值、风险和验收，不要因为生成快了就降低标准。

## 我的判断：这不是提示词技巧，是工作流变化

看完这支视频，我最想带走的不是某一句 prompt。我更在意这个判断：Fable 5 这类模型把工程瓶颈往上推了一层。

以前卡在“模型能不能写出代码”。现在更多卡在：

1. 你有没有给它能触到能力的工具。
2. 你有没有把任务里的 unknown 提前翻出来。
3. 你有没有给参考，还是只给抽象要求。
4. 你有没有让它记录执行中的岔路。
5. 你有没有在最后确认自己仍然理解结果。

这和“写更好的提示词”有关系，但不止于提示词。它更像一套工作方式：

```text
先让 agent 做 blind spot pass
再用 prototypes 暴露你说不清的偏好
然后让它 interview 你，优先问会改变架构的问题
给 reference 作为另一张地图
执行时保留 implementation notes
结束后让它 quiz 你，确认你能解释这个结果
```

这套方法也有边界。

第一，视频里的能力例子不是我复现过的 benchmark。系统提示词删 80%、AskUserQuestion 的进化、4 小时做 deck，都是讲者给出的经验。它们足够有启发，但如果要变成团队规则，还是要用你自己的任务集测。

第二，“少写约束”不等于不写边界。对安全、权限、数据、发布、成本、用户承诺这些事，约束仍然要清楚。Fable 5 的官方发布材料正好是反例：Anthropic 说，被 classifiers 判定为涉及 cybersecurity、biology and chemistry、distillation 的请求会由 Opus 4.8 接手；发布页还提到，这套 safeguards 平均会影响不到 5% 的 sessions。6-30 的 redeploy 说明又补了一层：新 classifier 用来阻断报告里的 bypass，但代价是 routine coding 和 debugging 里会有更多 benign request 被误伤。能力越强，边界越不能靠感觉。

第三，“be unreasonable”适合用在探索和构建速度上，不适合用来跳过验收。你可以要求 agent 同时做得好、快、便宜，但合并、上线、给客户之前，还是要让事实说话。

如果只用一句话概括这支 talk：Fable 5 的用法从承认 map 不等于 territory 开始，然后想办法把未知翻出来。
