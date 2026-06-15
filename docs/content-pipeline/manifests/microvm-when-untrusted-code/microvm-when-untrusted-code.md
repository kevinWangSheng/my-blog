---
title: "什么时候需要 microVM sandbox"
description: "microVM 的理由不是炫技,而是 threat model:不可信代码、多租户、强隔离和可控执行面。"
date: "2026-06-15"
tags: ["sandbox", "microvm", "agents"]
visibility: "public"
topic: "Agent sandbox"
related: ["sandbox-is-execution-boundary"]
---

MicroVM sandbox 的理由不是“更高级”,而是 threat model 需要更强边界。

容器通常共享 host kernel。它很快、很熟悉,适合可信开发环境、低权限任务和轻量隔离。但当 agent 要运行用户上传代码、第三方仓库、自动安装依赖,或者作为多租户产品的一部分,shared-kernel 边界就会变薄。

Firecracker 这类 microVM 给每个 workload 一个更强的虚拟化边界。E2B、LangSmith Sandboxes 这类 agent runtime 都把 microVM 当成执行不可信 agent code 的重要底座。

我的判断是:

- 本地可信脚本:先用轻量隔离,别过度工程化。
- 受控内部任务:容器 + 文件/网络限制可能够用。
- 用户代码、第三方依赖、多租户、企业资料:优先考虑 microVM。
- 有凭据或网络动作:microVM 仍不够,还要做权限和审计。

MicroVM 解决的是隔离强度,不是完整安全策略。
