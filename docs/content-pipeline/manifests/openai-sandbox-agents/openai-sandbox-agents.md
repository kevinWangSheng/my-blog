---
title: "OpenAI Sandbox Agents"
description: "官方文档入口:什么时候该让 agent 在 isolated workspace 里执行代码,以及 orchestration 与 execution 如何分开。"
date: "2026-06-15"
tags: ["agents", "sandbox", "code-execution"]
visibility: "public"
url: "https://developers.openai.com/api/docs/guides/agents/sandboxes"
category: "reference"
note: "sandbox 在 Agents SDK 工作流中的边界说明。"
---

这条 source 适合和 sandbox 主题一起读。它的价值不是某个 API 细节,而是边界:当 agent 的答案依赖 isolated workspace 里的文件、代码执行、依赖安装或工具结果时,才需要 sandbox。

这能防止两个极端:一边是让 agent 在主系统里随便跑,另一边是把所有文本任务都过度工程化成 sandbox 工作流。
