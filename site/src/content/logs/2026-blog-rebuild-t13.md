---
title: "Blog rebuild: T13 基础阅读链路通过"
description: "本阶段先不追求视觉重构,而是把页面、详情、Markdown、RSS 和验收证据跑通。"
date: 2026-06-15
tags: ["blog", "verification", "astro"]
visibility: public
period: "T13 acceptance"
summary: "完成基础 blog 使用链路验证,为后续内容密度和审美返工铺地基。"
source:
  label: "sample / project log"
---

这一阶段刻意把目标收窄到基础 blog 是否成立。之前的实现已经能 build,也有首页、列表页、详情页和 RSS,但这不足以证明日常使用可行。T13 的重点是确认普通访客路径真的能走通:从首页进入 note,再读 essay,再看 project,最后到 About 和 RSS。

## 做了什么

首先补厚了 1 篇 essay、1 条 note、1 条 log 和 1 个 project 详情,让真实页面覆盖二级标题、三级标题、段落、列表、链接、inline code、blockquote、长段落和中英文混排。然后修正本地 UI 验证脚本,让它不会清掉 `out/acceptance/` 证据,也能正确服务 Astro 的目录型路由。

### 验证结果

主验证包括三层:Astro build、固定 UI verify、路由/链接/Markdown 检查。build 生成 15 个页面;UI verify 在 375/768/1440 三个断点下没有横向溢出、console error 或 warning,axe 没有 critical/serious,Lighthouse 四项都是 100。route check 覆盖 15 个 URL 和 109 个站内链接,并统计了详情页 Markdown 元素。

- 首页和长文页都通过 `pnpm ui-verify`;
- RSS、sitemap、favicon 和 404 都能访问;
- reduced-motion 下 reveal 内容默认可见;
- 独立对抗验收没有发现 T13 阻塞项。

> 这不是最终站点完成,而是证明“可以正常读和正常跳转”的地基已经搭起来。

## 下一步

T14 会继续补内容密度。当前站点虽然有可读样本,但 Essays/Notes/Logs 的数量还不够支撑真实知识空间。后续还要做 Projects/About 的访客路径验收和清爽宁静审美返工,所以这一阶段的意义是把地基钉住,避免后面的设计工作建立在空壳页面上。
