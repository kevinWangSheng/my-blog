---
title: "GPT-6 Astra System Card"
description: "OpenAI 对 GPT-6 Astra 的能力、安全、提示注入、越权、cyber 风险与 chain-of-thought monitorability 的公开评估。"
date: "2026-09-03T15:30:00-07:00"
tags: ["gpt-6", "alignment", "security", "agents"]
visibility: "public"
url: "https://deploymentsafety.openai.com/gpt-6-astra"
category: "reference"
note: "值得一起看的两面：Astra 在任务边界和提示注入防御上进步明显，但书面推理在部分对抗评测中更难监控。"
---

这份 System Card 比“更 aligned”的发布口号更有用。它公开了 Astra 达到 Critical cyber capability 后增加的隔离、监控和停止机制，也给出内部 Codex 部署模拟、提示注入防御、任务越权与 capability hallucination 的结果。

同一份材料还记录了 counterevidence：Astra 在部分对抗场景里更能控制显式 reasoning，chain-of-thought monitorability 相比 Sol 有回归。《[GPT-6 让 Codex 能搜索被挤出窗口的历史](/my-blog/essays/gpt-6-astra-searchable-context/)》把这点和长时间 agent 的动作监督、误停率放在一起讨论。
