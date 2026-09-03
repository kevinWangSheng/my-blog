---
title: "GPT-6 让 Codex 能搜索被挤出窗口的历史"
description: "Astra 在 Codex 里的关键变化包括跨窗口 notes 和早期历史搜索。本文拆解这个机制的适用边界，并设计一次多窗口 A/B，验证它能否在摘要漏掉细节后减少返工。"
date: "2026-09-03T15:30:00-07:00"
tags: ["agents", "codex", "gpt-6", "context-engineering", "model-release"]
visibility: "public"
series: "Agent systems"
---

GPT-6 Astra 发布后，最显眼的是 benchmark 和 1.05M context window。我最后停在 Coding 章节的两小段。OpenAI 在那里讲了一件更接近真实工作的问题：一个 Codex 任务把窗口用完以后，前面发生的事情怎么办？

过去主要靠 compaction。历史越长，模型越要把前面的工作压成一份摘要，再带着摘要继续走。摘要漏掉一个失败原因、一个早期约束或者一段测试输出，后面通常找不回来了。

Astra 在 Codex 里引入的实验方案，把这件事拆成了两条路：跨窗口留下 notes，同时让更早的窗口保持可搜索。当前窗口里没有答案时，模型可以回去找原始消息和工具输出。

对长任务，我更关心被挤出窗口的信息还能不能找回来。

截至 2026 年 9 月 3 日，我还没有调用 Astra，也没有开启这个实验功能。本文依据[模型文档](https://developers.openai.com/api/docs/models/gpt-6-astra)、[Codex 配置](https://learn.chatgpt.com/docs/config-file/config-reference)和[System Card](https://deploymentsafety.openai.com/gpt-6-astra)分析公开机制，效果要留给实验回答。

## 一份摘要为什么会越压越薄

Compaction 面对的是一个有损压缩任务。

假设一次大型重构已经跑了几个小时。第一个窗口里，数据库测试的原始日志暴露了一条不能破坏的 schema 约束；第二个窗口里，agent 找到一条看似更干净的迁移路径；第三个窗口才真正开始修改。每次窗口填满时，系统都要判断哪些信息值得留进摘要。

「测试失败」很容易被留下，「为什么失败」可能只剩半句。再压一次，半句又可能变成「注意兼容性」。等到真正改 schema 时，原始日志已经不在眼前，摘要也不足以解释那条限制从哪来。

递归摘要会让一次省略延续到后面的窗口。对短问答影响不大，对长调试、跨模块改造和多阶段研究，它可能改变后面的决策。

![传统 compaction 把历史反复压成单一摘要；Astra 的 Codex 实验模式同时维护 notes，并允许搜索早期窗口，让遗漏信息有机会从原始消息和工具输出中找回](/my-blog/images/gpt-6-astra-searchable-context/context-memory.svg)
*依据 OpenAI 模型文档和 Codex 配置文档绘制。图里只包含官方已经公开的机制；索引结构、召回策略和保存期限仍未知。*

## Notes 记状态，搜索找遗漏

Notes 适合保存已经识别出的稳定状态：目标、已完成步骤、失败方案、当前假设和待处理风险。搜索补回 notes 没保存的细节。当后面的任务突然需要一条当时没被判断为重要的信息，旧窗口仍然是可回查的证据源。

OpenAI 的[配置参考](https://learn.chatgpt.com/docs/config-file/config-reference)给出的开关是：

```toml
[features]
context_management.experimental_mode = true
```

文档写明它目前默认关闭，需要使用 ChatGPT Plus、Pro 或 Pro Lite 登录。

这里有三个容易混掉的层级：

| 层级 | 它解决什么 | 目前能确认的边界 |
|---|---|---|
| 模型原生 context | 一次请求眼前能放多少内容 | Astra 是 1,050,000 tokens，最大输出 128K |
| Codex context management | 一个长任务跨过多个窗口后怎样保留和找回工作历史 | notes 加 searchable earlier windows，仍在实验中 |
| Memories | 从过往 chats 带入未来任务的长期记忆 | 有独立配置；这次发布没有说两者等价 |

Astra 仍然有固定窗口。实验功能改变的是窗口外历史的可恢复性，公开材料还没有证明恢复效果。

## 真正的问题是它何时有用

搜索让遗漏有机会恢复，也引入了检索系统常见的失败方式。旧窗口保存多久？Notes 由模型还是规则生成？同一事实前后冲突时谁覆盖谁？什么时候触发搜索？查询词不对、召回结果太多或者旧状态已经过期时，模型怎样判断？

发布日没有这些实现细节，也没有一组把实验开关打开和关闭、在同一个长任务上重复多次的独立 A/B。

许多任务也许根本用不完 1.05M tokens。一次工作从未跨过窗口边界时，可搜索历史没有信息恢复的机会，却仍可能增加 notes 维护、检索和判断成本。这项功能首先要在真正的长任务里证明自己。

外部状态也没有因此失去价值。在刚才的 schema 例子里，搜索可以把早期失败日志找回来，但版本化 spec 应该明确写下禁改约束，测试应该把它锁成可重复检查的 invariant。搜索历史是恢复证据的渠道，不该成为团队事实的唯一权威。

## 和 Fable 5.1 放在一起看

Astra 与 Fable 5.1 的表面规格接近：前者 1.05M context，后者 1M；最大输出都是 128K；标准 API 输入和输出都是每百万 token 10 美元与 50 美元。

Anthropic 的[Fable 5.1 提示指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)以 server-side 或 client-side compaction 为主。它明确要求摘要保留失败原因、废弃方案、约束、精确名称、数字和链接，高质量 compaction 可以减轻有损压缩。Anthropic 也提供 [client-side memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)，它读写应用自己维护的 memory files，解决的是另一层问题。公开文档里暂时没有与 Codex「搜索已压缩前窗口」相同的说明。

价格给出了另一个取舍。[Fable 5.1 模型页](https://platform.claude.com/docs/en/models/fable-5-1/overview)列出的 cache read 是每百万 token 0.25 美元，Astra 是 1 美元；Astra 总输入超过 272K 后，整个请求还会进入更高费率。

这给长任务划出了一条具体分岔：经常跨窗口并丢失早期证据的工作，值得测试 Astra 的搜索恢复；缓存命中率高、现有 compaction 已经够用的工作，Fable 的运行成本可能更低。我的《[Fable 5.1 首日观察](/my-blog/essays/fable-5-1-day-one/)》记录了它的其余变化，这里只比较与上下文续航直接相关的部分。

## 一次能说明问题的 A/B

普通问答碰不到这个机制。我会固定同一个仓库、commit、权限和验收标准，在任务前半段埋入 10 到 20 条后期才会用到的约束。一部分足够明显，应该进入 notes；另一部分放在工具输出和失败日志里，专门测试遗漏后的搜索恢复。

任务至少经历两次上下文窗口耗尽。实验组开启 context management，对照组沿用旧 compaction。每个条件重复 5 到 10 次并交换运行顺序，然后看六项指标：远距约束召回率、未进 notes 的事实找回率、最终验收通过率、重复调查与人工纠正次数、每任务总成本，以及分开统计的越权与误停。

[System Card](https://deploymentsafety.openai.com/gpt-6-astra)解释了最后两项为什么要单列。OpenAI 在 54,000 多个内部 Codex 模拟任务里观察到，Astra 的高严重性标记约为 Sol 的一半；同一份材料也记录了 written reasoning monitorability 的回归，以及合法任务被安全检查减速、暂停或停止的可能。这些模型级结果不能预测 context management 开关会让安全指标怎样变化，它们只是同一模型进入长任务时需要带进实验的 guardrail。

恢复率最能区分两组。实验组需要在 notes 遗漏后回到早期原始输出，并让最终验收少一次返工。否则，searchable context 只是换了一种整理历史的方式。
