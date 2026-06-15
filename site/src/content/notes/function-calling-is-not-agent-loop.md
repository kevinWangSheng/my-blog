---
title: "Function calling 是能力，agent loop 是授权"
description: "给模型工具不等于让模型控制流程;多数生产系统应该先 workflow,只在必要处给 bounded loop。"
date: "2026-06-15"
tags: ["agents", "workflow", "architecture"]
visibility: "public"
topic: "Agent architecture"
related: ["agent-memory-is-write-policy"]
---
很多系统被过度 agent 化,不是因为任务真的需要自主 loop,而是因为大家把三件事混在一起了:tool use、code loop、agent loop。

Function calling 只是能力。它表示模型可以请求调用某个工具。

Agent loop 是授权。它表示模型不只调用工具,还可以根据中间结果决定下一步、再下一步、什么时候停止。

这两个差别很大。一个 workflow 可以给模型工具,但仍然由代码决定执行路径:先分类,再查订单,再生成回复。模型在其中是节点,不是总控。

只有当步骤空间无法预画、需要根据中间观察动态改变计划时,才值得给 bounded agent loop。否则,你只是把可测试的控制流交给一个更贵、更难复现的运行时。

我现在更偏向的默认架构是:外层 workflow 做 routing、权限和任务分发;内层只有在开放式探索、多步诊断、复杂修复这类场景里,才给受限 agent loop。

> Function calling 是模型能不能拿工具。Agent loop 是模型能不能决定接下来发生什么。
