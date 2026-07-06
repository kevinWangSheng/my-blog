---
title: "Matt Pocock's skills (writing-great-skills)"
description: "把'好 skill'讲成一套可操作词汇:no-op、渐进披露、沉积、leading words——写 agent skill 的删减判据。"
date: "2026-07-06"
tags: ["skills", "agents", "prompt-engineering"]
visibility: "public"
url: "https://github.com/mattpocock/skills"
category: "reference"
note: "写 agent skill 的删减判据来源:no-op、渐进披露、沉积。"
---
写 agent skill 时最容易犯的错是往里加,而不是往外删。这个仓库里的 `writing-great-skills` 给了几把好用的尺:一行相对模型默认行为没有改变什么,就是 no-op;只有部分分支才用的细节应该渐进披露到单独文件;没有删减纪律的 skill 会沉积成谁也不敢动的手册。

我在《[我把 skill 从 371 行砍到 74 行,真正的发现是 eval 差点骗了我](/my-blog/essays/evaluating-an-agent-skill/)》里用这几把尺量了自己的一个 371 行 skill,并做了一次带异源判官的 eval。
