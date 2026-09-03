---
title: "Codex：实验性上下文管理配置"
description: "Codex 官方配置参考里关于 notes 与 searchable history 的开关、默认状态和账号条件。"
date: "2026-09-03T15:30:00-07:00"
tags: ["codex", "context-engineering", "agents", "configuration"]
visibility: "public"
url: "https://learn.chatgpt.com/docs/config-file/config-reference"
category: "reference"
note: "搜索 features.context_management.experimental_mode：文档明确区分它与 Memories，当前默认关闭，用 notes 加可搜索历史替代反复压成一份摘要。"
---

这是一张很长的 Codex 配置表，相关键只有一项：`features.context_management.experimental_mode`。它写清了三个发布页容易略过的边界：功能仍是 experimental、当前 off by default、需要以 Plus、Pro 或 Pro Lite 的 ChatGPT 账号登录。

《[GPT-6 让 Codex 能搜索被挤出窗口的历史](/my-blog/essays/gpt-6-astra-searchable-context/)》用这条配置把模型窗口、单任务 context management 与跨会话 Memories 分开，避免把它宣传成无限上下文。
