---
title: "The Agentic AI Engineer(Mutagent @ AI Engineer)"
description: "用 agent 循环来构建 agent:离线 spec、构建、评估,在线监控、诊断、优化;eval 是终止条件,评估集是发现的产物。"
date: "2026-07-02"
tags: ["agents", "eval", "talks"]
visibility: "public"
url: "https://www.youtube.com/watch?v=pSto5YaNGUo"
category: "reference"
note: "两个循环框架和「eval 是终止条件」的来源,和《Agent 工程的两个循环》对照读。"
---

Mutagent 的 CEO Benedikt Sanftl 和 CTO Burak 在 AI Engineer 大会上合讲的 talk,35 分钟。把「构建 agent」拆成离线循环(spec、构建、评估、上线)和在线循环(监控、诊断、优化、再评估),主张这整个循环都交给 agent 跑,人负责设计循环和守门。

我收它是因为三个可以反复引用的判断。二元判据好过打分,挂了就是行动项;评估集是发现的产物,来自用户反馈和生产失败的持续沉淀,不是开工前能写全的;诊断要靠失败模式沉淀出代码可检的指标,否则读全量 traces 比执行还贵。我在《Agent 工程的两个循环》里拿自己的发布管线对照过这三条,前两条在我的小样本上应验了。
