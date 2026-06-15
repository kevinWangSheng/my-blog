---
title: "先有证据,再说完成"
description: "agent 协作里最重要的礼貌之一,是不要把推断说成已验证事实。"
date: 2026-06-12
tags: ["verification", "agents", "writing"]
visibility: public
topic: "Agent reliability"
related: []
source:
  label: "sample / project note"
---

Agent 很容易说出流畅的完成总结,但流畅不等于可靠。一个页面“应该能打开”、一个链接“看起来没问题”、一个脚本“理论上会通过”,都不是验收证据。协作里真正让人安心的是具体输出:命令、状态码、文件路径、截图、summary、失败项和未确认项。

## 三种句子要分开

我希望 agent 在复杂任务里区分三类句子。第一类是 checked facts,例如 `pnpm --dir site build` 通过、某个 URL 返回 200、某个 JSON 里 `ok: true`。第二类是 inference,例如“这说明列表到详情的基本链路成立”。第三类是 recommendation,例如“下一步可以进入内容密度补足”。

这三类句子混在一起时,人会很难判断哪里真的被检查过。尤其在 UI 和内容任务里,“我觉得可读”不应该替代三断点截图、console 检查和真实页面阅读路径。

> 证据不是为了显得严谨,而是为了让下一次协作能从真实状态继续。

在个人站里,这种习惯也会影响读者体验。如果项目页声称某个成果已经完成,它就应该有相应证据;如果只是方向或样例,就应该明确标注。公开表达最怕的不是不够完整,而是把未确认的东西写得像已发生事实。
