---
title: "UI agent 必须看见自己做了什么"
description: "截图、axe 和 Lighthouse 是最低地板,审美仍然需要人的最终验收。"
date: 2026-06-14
tags: ["ui", "verification", "agents"]
visibility: public
topic: "UI verification"
related: ["agent-learning-cockpit"]
---

对 UI 来说,只跑 build 太薄了。构建通过只能说明页面存在,不能说明它能读、能用、在移动端不崩,也不能说明动效没有挡住内容。

固定验证回路应该把客观问题先筛掉:多断点截图、可访问性扫描、性能和 SEO 基线。审美判断不应该伪装成脚本结论,但脚本可以保证人看到的是一个已经过地板线的版本。
