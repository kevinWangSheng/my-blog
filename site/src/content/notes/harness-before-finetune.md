---
title: "先投 harness，再谈 fine-tune"
description: "如果问题能通过工具、权限、上下文、评估和流程解决, fine-tune 不应该是第一反应。"
date: "2026-06-15"
tags: ["agents", "harness", "product"]
visibility: "public"
topic: "Agent product strategy"
related: ["function-calling-is-not-agent-loop", "agent-memory-is-write-policy"]
---
当一个 AI 产品表现不够好时,很多人的第一反应是:是不是该换更强模型,或者 fine-tune 一个专用模型?

我现在会先问另一个问题:你真的已经把 harness 做到位了吗?

Harness 包括工具设计、权限边界、上下文选择、记忆策略、评估集、失败回放、人工验收点和产品流程。它不是 fine-tune 的替代品,而是任何路径都绕不过的系统层。

如果 base model 升级,好的 harness 仍然有价值。工具 schema、任务路由、上下文压缩、review gate、trace/eval 都会继续服务新模型。相反,一个 fine-tune 如果只是补工具缺口、补上下文缺口、补流程缺口,下一次模型升级或需求变化时很容易失效。

这不表示 fine-tune 没价值。它适合在问题已经被明确归因之后使用:prompt 解决不了,context 解决不了,harness 解决不了,而且任务分布稳定、数据质量足够、收益能覆盖维护成本。

> Fine-tune 应该是证据驱动的后手,不是焦虑驱动的第一步。
