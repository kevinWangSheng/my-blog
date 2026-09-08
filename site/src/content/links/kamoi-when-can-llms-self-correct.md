---
title: "When Can LLMs Actually Correct Their Own Mistakes?"
description: "TACL 2024 综述:系统梳理自纠错在什么条件下成立,并指出以往正面结果的设计缺陷。"
date: "2026-09-08"
tags: ["paper", "evals", "self-correction", "agents"]
visibility: "public"
url: "https://arxiv.org/abs/2406.01297"
category: "paper"
note: "想搞清楚「要不要让 agent 自己审自己」时,先读这篇:它把有效前提和不公平实验设计都列清楚了。"
---
核心结论有两处限定不能省:除少数天然极适合自纠的任务外,没有工作证明仅靠 prompt 的模型反馈能成功自纠;而有效前提是可靠外部反馈**或**大规模微调,不是只有前者。文中还给了一份自纠错实验的设计 checklist,可直接用来检查自己的 eval 是否偷偷用了 oracle 停止条件。
