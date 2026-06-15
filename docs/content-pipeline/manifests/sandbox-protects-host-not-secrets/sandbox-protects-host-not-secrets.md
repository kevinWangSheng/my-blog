---
title: "Sandbox 保护 host，不保护你放进去的 secrets"
description: "隔离边界能限制失控进程,但不能替你决定哪些凭据、文件和网络权限不该进入 sandbox。"
date: "2026-06-15"
tags: ["sandbox", "security", "agents"]
visibility: "public"
topic: "Agent sandbox"
related: ["sandbox-is-execution-boundary"]
---

Sandbox 最常见的误解是:只要 agent 在 sandbox 里跑,就安全了。

更准确的说法是:sandbox 主要保护 host、其他租户和主系统,不自动保护已经放进 sandbox 的东西。

如果你把长期 token、SSH key、内部文档、客户数据或过宽的网络权限挂进去,agent 就已经被授权看见它们。之后就算进程被困在 microVM 里,它仍然可能读取这些材料,或者在允许的网络范围内把它们送出去。

所以 sandbox 的安全性不只取决于隔离技术,还取决于你放了什么进去。

最小化输入、短期低权限凭据、网络 allowlist、文件挂载白名单、命令 trace 和人工中断点,这些才是真正让 sandbox 成为执行边界的设计。
