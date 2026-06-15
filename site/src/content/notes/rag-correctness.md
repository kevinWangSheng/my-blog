---
title: "RAG 的相关性不等于正确性"
description: "检索能找到相似文本,但系统仍然需要证据约束、冲突处理和回答校准。"
date: 2026-06-11
tags: ["rag", "evaluation"]
visibility: draft
topic: "Retrieval systems"
related: []
source:
  label: "sample / existing-material-summary"
---

RAG 最容易被误解的地方是把“找到了相关段落”当成“回答已经可靠”。检索只是把模型拉回证据附近,并不自动解决来源冲突、时间漂移、引用粒度和用户意图偏差。

更稳的做法是让系统显式区分事实、推断和建议,并在证据不足时承认不确定。
