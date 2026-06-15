---
title: "Anthropic Building Effective Agents"
description: "官方 agent 架构地基:先区分 workflow 和 agent,从简单可组合模式开始,不要默认追求全自动 loop。"
date: "2026-06-15"
tags: ["agents", "workflow", "architecture"]
visibility: "public"
url: "https://www.anthropic.com/research/building-effective-agents"
category: "essay"
note: "workflow vs agent 的官方架构来源。"
---
这篇是理解 agent 系统时很好的地基来源。它把 workflow 和 agent 按控制权区分开:workflow 是预定义代码路径编排 LLM 和工具;agent 是模型动态决定自己的流程和工具使用。

我把它放在 source shelf 里,是因为很多系统问题都来自默认追求 autonomous loop。更稳的起点通常是先用简单、可组合、可观测的 workflow,只在路径无法预画的地方给 agent loop。
