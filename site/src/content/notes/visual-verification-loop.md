---
title: "UI agent 必须看见自己做了什么"
description: "截图、axe 和 Lighthouse 是最低地板,审美仍然需要人的最终验收。"
date: 2026-06-14
tags: ["ui", "verification", "agents"]
visibility: public
topic: "UI verification"
related: ["agent-learning-cockpit"]
source:
  label: "sample / project note"
---

对 UI 来说,只跑 build 太薄了。构建通过只能说明页面存在,不能说明它能读、能用、在移动端不崩,也不能说明动效没有挡住内容。一个 agent 如果没有看见自己做出来的页面,它很容易把“组件已经写完”误判成“体验已经成立”。

## 固定回路先拦截客观问题

本项目把固定验证回路设计成 `build → serve dist → screenshots → axe → Lighthouse → summary`。它不试图评价审美,只负责拦截那些不应该交给 human 的低级问题:页面打不开、console error、明显横向溢出、严重可访问性问题、移动端首屏断裂、RSS 或页面链接缺失。

### 为什么截图不是装饰

截图的价值不是让 agent 每次都长篇描述画面,而是留下可复查证据。尤其在 375px、768px、1440px 这种断点上,很多布局问题只有渲染后才会出现。比如一个很长的英文 slug、一段没有换行的 inline code、或者 sticky header 与正文间距的冲突,都可能在源码里看起来无害,到页面上才露出真正的形状。

- `axe` 负责可访问性地板;
- Lighthouse 负责性能、SEO 和 best practices 的粗粒度信号;
- Playwright 截图负责让人验收时不必重新跑完整环境;
- 额外的 route/link check 负责证明列表和详情真的能连起来。

> 自动验证不是审美裁判。它只是确保交到人面前的版本已经过了最基本的工程地板。

## 审美仍然需要人的判断

清爽、宁静、留白、阅读节奏,这些东西不能只靠一个分数判断。脚本可以告诉我们 `document.scrollWidth` 没有超过 `clientWidth`,但它不能告诉我们这个页面有没有呼吸感。它可以证明 Markdown 的 `blockquote` 被渲染出来,但不能证明引用在文章节奏里是否自然。

所以最终流程应该是:agent 先把可客观检查的问题消掉,留下 summary、截图、URL 清单和已知限制;human 只做最终体验验收。这样人的注意力不会被“这个链接是不是 404”消耗,而是用在真正重要的判断上:这个站点像不像一个可以长期生长的个人知识空间。
