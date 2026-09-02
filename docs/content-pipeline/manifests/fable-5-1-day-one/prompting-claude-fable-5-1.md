---
title: "Prompting Claude Fable 5.1"
description: "Anthropic 官方的 Fable 5.1 提示词指南：按观察到的症状索引，每条行为差异都给了可直接粘贴的修法。"
date: "2026-09-02T00:30:00+08:00"
tags: ["agents", "claude-code", "fable-5-1", "prompting"]
visibility: "public"
url: "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1"
category: "reference"
note: "少见的按症状组织的官方指南：并行调用变少、进度更新变少、整文件重写、任务没做完就停、散文太密，每一条都对应一段系统提示词。"
---
这页的结构是「你观察到什么，就跳到哪一节」：一轮只发一个工具调用、长任务静默几分钟、小改动整文件重写、写到一半停下来问你、散文越来越密。每一节先解释 5.1 相对 Fable 5 为什么会这样，再给一段可以直接放进系统提示词的修法。

它值得单独收进 links，因为里面的判断可以反过来读：官方承认的这些行为差异，就是 5.1 在长时 agent 负载里最容易踩的坑。我在《Fable 5.1 首日观察：修了什么、封了什么、该不该切》里挑了对 agent 影响最大的七条做了表。
