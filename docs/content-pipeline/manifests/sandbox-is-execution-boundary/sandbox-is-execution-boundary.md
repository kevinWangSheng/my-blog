---
title: "Agent sandbox 是执行边界，不是安全按钮"
description: "让 agent 跑代码之前,先分清 sandbox 能隔离什么、不能替你决定什么,以及为什么凭据和网络边界仍然是产品设计问题。"
date: "2026-06-15"
tags: ["agents", "sandbox", "security", "harness"]
visibility: "public"
series: "Agent systems"
---

当 agent 开始写文件、装依赖、跑命令、访问网页或调用外部 API,它就不再只是“生成文本”。它已经进入执行面。

这时 sandbox 的价值不是让系统“绝对安全”,而是给执行面画边界:agent 能在哪里读写,能访问哪些网络,能消耗多少资源,能拿到哪些凭据,出错时 blast radius 到哪里为止。

所以我现在更愿意把 sandbox 理解成 harness 的一部分,而不是一个可选安全插件。

## Sandbox 隔离的是执行面

一个可用的 agent sandbox 至少要回答五个问题。

第一,compute boundary。agent 跑出来的进程和主系统是不是隔离? 是共享宿主 kernel 的容器,还是有独立 kernel 的 microVM? 多租户和不可信代码场景里,这个差异很大。

第二,filesystem boundary。agent 能不能读到仓库外的文件? 能不能写系统目录? 上传进 sandbox 的材料有没有最小化? 只要你把 SSH key、cookie、生产配置放进 sandbox,它们就已经在 agent 的执行范围内。

第三,network boundary。agent 能不能访问任意外网? 能不能打到内网服务? 能不能把数据传到不该去的域名? 对 code execution agent 来说,网络不是默认能力,而应该是显式授权。

第四,resource boundary。agent 死循环、装巨型依赖、生成大量文件、跑高成本任务时,谁负责限时、限内存、限磁盘、限并发?

第五,trace boundary。执行过什么命令、读写了哪些文件、访问了哪些网络、用了哪些凭据,是否能被回放和审计? 没有 trace 的 sandbox 只是一个黑盒。

## 它保护 host,不保护你放进去的东西

Sandbox 最容易被误解的一点是:它主要保护外部系统免受 sandbox 内部失控影响,不自动保护 sandbox 内部已经授权给 agent 的数据。

如果一个 agent 被 prompt injection 诱导,而 sandbox 里正好有可读的 token、客户数据、内部文档或生产配置,隔离边界不会神奇地阻止它读取这些材料。因为从 sandbox 的角度看,这些东西已经被你放进来了。

这就是为什么 sandbox 必须和权限设计一起看。最小化挂载、短期凭据、网络 allowlist、敏感操作审批、日志审计,这些不是 sandbox 的附属项,而是 sandbox 是否真的可用的条件。

> Sandbox 能限制 blast radius,但不能替你判断哪些东西不该进 blast radius。

## MicroVM 不是炫技,是 threat model

不是所有 agent 都需要最强隔离。

如果只是本地可信脚本、一次性数据转换、低权限开发任务,容器或本地 OS 级限制可能足够。它们启动快、开发体验好、成本低。

但如果 agent 要运行用户上传代码、第三方仓库、自动安装包、访问企业资料,或者作为多租户产品的一部分,shared-kernel container 的边界就会变薄。Firecracker 这类 microVM 的价值,是用硬件虚拟化给每个 sandbox 更强的隔离边界,同时保留接近容器的启动和资源效率。

E2B、LangSmith Sandboxes、OpenAI Sandbox Agents 这些方向的共同信号是:agent runtime 正在把“隔离 workspace”变成一等公民。不是因为每个应用都要做安全平台,而是因为很多有用 agent 都需要真实 workspace:文件、依赖、命令、状态、工具、错误输出。

## 什么时候不该上重 sandbox

Sandbox 也不是越重越好。

如果 agent 的回答只依赖 prompt context,不需要写文件、跑代码、安装依赖或观察命令结果,那 sandbox 可能只是增加复杂度。OpenAI 的 Sandbox Agents 文档也把使用场景说得很清楚:当答案依赖 sandbox workspace 里的工作结果时,才需要 sandbox。

如果你只是做静态文本改写、分类、摘要、轻量 routing,先把 workflow、guardrails、eval、review gate 做好,比急着接 microVM 更重要。

更好的顺序是:先问任务是否真的需要执行;如果需要,再问执行需要哪些文件、工具、网络和权限;最后才选容器、gVisor、microVM、managed sandbox 或本地限制。

## 我会这样设计默认边界

对一个能跑代码的 agent,我会把默认边界设得很保守。

输入材料最小化,不要把整台电脑或整个内部知识库挂进去。网络默认关,只为明确任务打开必要域名。凭据默认不进 sandbox,必须进时使用短期、低权限、可撤销 token。所有命令、文件变更和网络访问留下 trace。长任务必须有 timeout 和人工可中断点。输出回到主系统前,先做结构检查和安全检查。

这听起来不像“让 agent 自由工作”,但它恰恰是让 agent 真正可用的条件。没有边界,agent 的能力越强,系统越不敢给它真实任务。

Sandbox 的目标不是束缚 agent,而是让我们敢把更真实的工作交给它。
