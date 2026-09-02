---
title: "What's new in Claude Fable 5.1"
description: "Anthropic 官方的 Fable 5.1 变更清单：三个破坏性 API 变更、五个新增功能、行为差异、定价与迁移步骤。"
date: "2026-09-02T00:30:00+08:00"
tags: ["agents", "claude-code", "fable-5-1", "api"]
visibility: "public"
url: "https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1"
category: "reference"
note: "自己拼 messages 数组的人必读：禁止强制 tool_choice、thinking 块绑定模型、修改历史即失效前两条会直接 400、第三条会静默丢块，页面把替代方案和迁移清单一起给了。"
---
Anthropic 给 Fable 5.1 写的开发者变更页。它比发布公告有用的地方在于把 API 契约说清楚了：哪两条会返回 400、哪一条会静默丢掉 thinking 块，三个 beta 功能各自需要什么 header，缓存读是输入价的 0.025 倍，以及从 Fable 5 迁移时该按什么顺序检查。

我在《Fable 5.1 首日观察：修了什么、封了什么、该不该切》里把这三条破坏性变更和官方说了一半的反蒸馏动机串起来讲了一遍。如果你只想知道自己的 harness 会不会坏，直接看这页的 Breaking changes 和 Migrate 两节就够。
