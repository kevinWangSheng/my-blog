---
title: "Context engineering 不是把上下文塞满"
description: "上下文真正的难点是选择、压缩、隔离和恢复,而不是窗口长度。"
date: 2026-06-12
tags: ["context-engineering", "agents"]
visibility: public
topic: "Agent memory"
related: ["agent-learning-cockpit"]
source:
  label: "sample / existing-material-summary"
---

长上下文会降低一部分摩擦,但不会自动形成好系统。真正有价值的是知道哪些状态必须被保留,哪些证据只需要短期存在,哪些结论需要回写到稳定记忆里。

一个可运行的 agent 系统应该有明确的生命周期:写入、选择、压缩、隔离、恢复。否则窗口越大,噪声也只是被保存得更久。
