---
title: "Agent Learning Cockpit"
description: "一个把研究、阅读、复盘和产出连成闭环的个人学习控制台。"
date: 2026-06-10
tags: ["agent", "learning", "workflow"]
visibility: public
status: active
role: "产品设计 / 系统架构 / 实现"
period: "2026 — now"
source:
  label: "sample / project brief"
---

这个项目把学习从“收藏链接”推进到“形成可复用判断”的阶段。它不是知识库皮肤,而是一个帮助 agent 和人分工的工作台:agent 负责收集、抽取、比对和初筛,人保留真正的判断、取舍和验收。当前 repo / demo 尚未作为公开入口确认,所以本页只展示项目说明与过程证据,不伪造外部链接。

## Problem

AI 时代的学习材料太多,但真正困难的部分并没有消失。一个人可能让 agent 总结十篇文章,却仍然不知道哪一篇可靠、哪些结论互相冲突、哪些内容应该进入长期知识库,以及哪些只是短期上下文。传统收藏夹和普通笔记软件经常把这些状态混在一起,最后留下大量“以后再看”。

### Solution shape

Agent Learning Cockpit 的方向是把学习拆成可检查的节点:研究问题、来源队列、阅读摘录、判断校准、复盘输出和公开发布。每个节点都应该有清楚的输入和输出,并且能回答一个简单问题:下一步需要人判断,还是 agent 可以继续执行?

- 来源进入系统前先记录来源类型、时间和可信度线索;
- 阅读材料先被整理成可复查摘录,再进入人的判断界面;
- 结论必须区分事实、推断和建议;
- 可以公开的内容再经过发布前检查,同步到 blog 的 Markdown 内容目录;
- 每次阶段推进都留下 log,避免项目只剩最终包装。

> 项目的核心不是“让 AI 替我学习”,而是让学习过程里的证据、判断和行动更短路、更可复查。

## Process evidence

当前博客重建本身就是这个项目方向的一段过程证据:站点提供 content collections、`content:check`、`content:sync`、RSS 和 UI 自验证脚本,让 agent 整理出的内容可以通过明确格式进入公开页面。T13/T14 的验收材料也证明了这个项目的工作方式:先写计划,再实现,再由主 agent 自验证,最后让独立对抗 agent 挑刺。

### Current result and next step

当前结果不是一个对外宣称完成的 SaaS,而是一个正在被拆解和验证的个人学习系统方向。下一步不是急着做一个庞大的 dashboard,而是先把最小闭环跑稳定:本地 output → manifest / markdown → check → sync → build → route/UI verification → human acceptance。

这也是为什么项目详情页必须比普通卡片更厚。对于陌生访客来说,它应该说明我在解决什么问题、我承担了什么角色、目前做到哪一步、哪些证据可以被打开,以及还有什么没有完成。只有这样,Projects 才能成为能力入口,而不是一个漂亮但空泛的列表。
