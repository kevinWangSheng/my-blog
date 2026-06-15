---
title: "Review gate 不是拖慢 agent,而是产品设计"
description: "真正需要人的地方应该被设计成清晰验收点,而不是让人承担重复检查。"
date: 2026-06-13
tags: ["agents", "workflow", "review"]
visibility: public
topic: "Agent workflow"
related: ["agent-learning-cockpit"]
source:
  label: "sample / existing-material-summary"
---

很多 agent 工作流的问题,不是自动化不够,而是 review gate 放错了位置。人不应该被要求反复运行 build、数链接、检查截图路径,这些是 agent 和脚本能承担的地板工作。人真正应该判断的是方向是否正确、公开边界是否安全、体验是否符合目标。

## 好的 gate 长什么样

一个好的 review gate 应该让人看到少量高价值证据:入口 URL、关键截图、验证 summary、已知限制和下一步真实选择。它不应该要求人从日志海里自己捞结论,也不应该让 agent 用一句“已验证”代替证据。

- 低风险、本地、可回退的执行由 agent 自己完成;
- 可客观判断的问题用命令和脚本先筛掉;
- 需要审美、方向、安全边界的部分交给 human;
- 每次 gate 之后,决策要写回稳定文件,避免下一个 agent 重开讨论。

> Review gate 的目标不是制造等待,而是保护人的判断力不被低价值检查消耗。

这个博客重建里的 ②决策和 ⑦验收就是两个不同 gate。前者决定方向,后者判断结果;中间的实现、验证、修复都应该由 agent 自闭环。这样人仍然掌握方向,但不需要成为工具链操作员。
