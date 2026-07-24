---
title: "HTML 不是网页,是 agent 的视觉中间表示"
description: "解析 AI Engineer talk:为什么 agent 做图不该从 Figma、PowerPoint 或手写 SVG 开始,而应该先把 slides、docs、videos 变成 HTML/CSS 可以渲染和验证的结构。"
date: "2026-07-03T12:00:00-07:00"
tags: ["agents", "video-notes", "html", "generative-ui"]
visibility: "public"
---
这篇是对 AI Engineer 频道 7 分钟 talk [HTML is All You Need(for Agents to Make Graphics)](https://www.youtube.com/watch?v=JRTAtZ5iBkU) 的完整解析。讲者是 Amol Kapoor,视频里自我介绍为 Nori 的 CEO。他的主张很直接:agent 做视觉内容差,不一定是因为模型没有空间能力,也可能是因为我们给它的工具接口错了。

下面先按视频顺序讲完它的内容。最后一节才是我的判断:这不是「HTML 真能解决一切」,而是一个更稳的工程方向,把 slides、docs、videos 先变成可渲染、可检查、可迭代的结构。

## 开场:agent 不只是写代码

视频开头先做产品语境:他们做的是一个能理解公司代码、文档、Slack 和其他数据的 AI employee。接着讲者把「coding agent」这个名字拆开看:如果 agent 能写代码,那它不只是在写代码,它是在操纵一种可执行、可组合的结构化媒介。只把它叫 coding agent,反而低估了它能做的事。

于是问题变成:如果让 agent 做大家以为它不擅长的东西,比如 slides、docs、video,应该给它什么媒介?

他先抛了一个数字:世界每天大约花 34,000 个 human years 做 slide decks。这个数字在视频里没有展开来源,所以我只把它当作讲者用来强调浪费规模的说法。真正重要的不是数字本身,而是后面的判断:做 deck 最耗时的部分往往不是思考,而是格式、品牌、对齐、搬动元素这些 fiddling。

![视频用 slide deck 的时间浪费作为开场:大部分时间不是思考,而是格式和移动元素](/my-blog/images/html-is-all-you-need-for-agent-graphics/01-deck-fiddling.webp)
*视频 01:01 画面,© Amol Kapoor / Nori / AI Engineer(YouTube)*

## 为什么 Figma/PowerPoint 不是 agent 的好接口

如果人要做一页 slide,会打开 PowerPoint、Google Slides、Figma、Canva,然后开始操纵画布。点、拖、放、缩放、吸附到网格,这些动作都是为人的手和眼设计的。底层当然有数据结构,但通常藏在应用自己的格式里。

讲者的批评是:我们把这些工具交给 agent,等于要求 agent 像人类一样操作一个视觉画布。结果常见得很:元素重叠,文字看不见,对齐混乱,整体像坏掉的自动排版。

![视频把 PowerPoint、Slides、Figma、Canva 归为给人类手眼设计的 canvas 工具](/my-blog/images/html-is-all-you-need-for-agent-graphics/02-human-canvas-tools.webp)
*视频 01:31 画面,© Amol Kapoor / Nori / AI Engineer(YouTube)*

这里他顺手回应了一个更大的反驳:AI skeptics 会说这不是工具问题,而是模型根本不懂空间。视频提到 ARC-AGI 这类 benchmark,也提到 Simon Willison 常用的 pelican riding a bicycle 测试:要求模型只用 SVG 画一只骑自行车的鹈鹕。

视频展示的 SVG 结果确实很糟。讲者的解释是:这不能完全证明模型不会做图,因为让人类手写一堆 SVG 坐标来画鹈鹕,大多数人也做不好。SVG 对这个任务来说像一堵数字墙,不是人类的直觉媒介,也未必是 agent 最舒服的视觉媒介。

![视频展示 pelican riding a bicycle 的 SVG 测试,作为「手写坐标不是好媒介」的例子](/my-blog/images/html-is-all-you-need-for-agent-graphics/03-pelican-svg-test.webp)
*视频 02:22 画面,© Amol Kapoor / Nori / AI Engineer(YouTube)*

## 关键转换:不要按人的工具想,按模型的媒介想

这支视频最有价值的一句不是标题,而是这个转换:stop thinking like a user, think like the model。

人类想图形,自然会想画布,所以我们发明了 Figma MCP、PowerPoint CLI、截图后替换的循环。但 agent 的强项不是鼠标动作,而是语言、token、结构。给它的接口也应该贴近这些强项。

于是讲者问:有没有一种语言,擅长描述 layout,模型见过大量训练样本,能表达结构,又能渲染成像素并到处运行?

答案就是 HTML/CSS。

HTML 让模型用结构来思考。heading、chart、grid、section、card 这类概念带着语义,浏览器负责把它们变成像素。模型不必手摆每个坐标,就能得到布局、字体、动效、图表和主题。

![视频的核心论点:HTML lets a model think in structure](/my-blog/images/html-is-all-you-need-for-agent-graphics/04-html-structure.webp)
*视频 04:00 画面,© Amol Kapoor / Nori / AI Engineer(YouTube)*

这也是他重新解释 deck 的地方。PowerPoint 只是做 deck 的一个工具,不是 deck 本身。听众最后看到的是 presentation mode,并不关心你用什么编辑格式到达那个结果。所以编辑格式可以换成 agent 更擅长的 HTML,之后再导出 PDF 或别的格式。

## 他们怎么用:slides、docs、video

讲者说他们用这个 HTML trick 做 slide decks、board decks、sales decks,也用来做 docs,让文档有颜色、活力和品牌一致性。这里视频没有给代码仓库或可审计的实现细节,所以我把它视为产品实践陈述,不是独立验证过的公开工程结果。

最有意思的是他对这支视频本身的说明:你正在看的东西就是 HTML 和 CSS,「divs all the way down」。也就是说,它看起来像一支剪辑好的科技解释视频,但画面本体更像一组会动的网页场景:浏览器窗口、字幕、卡片、代码块、绿色光效、过渡动画,再叠上配音和音乐。

![视频说明它自身也是 HTML/CSS 生成的画面,再被渲染成视频](/my-blog/images/html-is-all-you-need-for-agent-graphics/05-html-css-video.webp)
*视频 05:31 画面,© Amol Kapoor / Nori / AI Engineer(YouTube)*

最后他补了一个重要边界:漂亮 deck 本身不值钱。内容、数据、客户电话、邮件、故事线才是价值。agent 如果能访问这些数据,才可能端到端生成 deck;否则只是把空壳做漂亮。

所以视频的完整链路其实是两层:第一层,用 HTML/CSS 做视觉结构;第二层,让 agent 接入真实公司数据,自动填充内容。Nori Sessions 的产品广告落点也在这里。

## 我的判断:标题是口号,方向是对的

我不觉得「HTML is all you need」字面成立。视频生产至少还需要脚本、分镜、配音、字幕、时间轴、音频混合、渲染、验收。复杂动画还需要 Remotion、Motion Canvas、GSAP 或自写 timeline;数据图表还需要 chart layer;最终视频还要用 Playwright、Chromium 或 ffmpeg 录制/合成。

但它的核心判断非常对:对 agent 来说,HTML/CSS 是一个强大的视觉中间表示。它比「模拟人类拖拽 Figma」更可控,比「手写 SVG 坐标」更语义化,也比「直接生成最终视频」更容易检查。

我会把这个方向拆成一个实际项目:

1. 先写旁白稿,把 2-3 分钟内容拆成 8-12 个 scenes。
2. 每个 scene 用 HTML/React 表达,固定 16:9 画布,用 CSS grid/flex、typography、code block、browser mockup 和图表组件承载信息。
3. 用 Remotion 或 Playwright 控制时间轴,让每个 scene 可以按帧渲染。
4. 用 TTS 或真人录音生成音轨,再用字幕/时间戳驱动画面变化。
5. 用自动检查守门:截图非空、文本不溢出、图片能加载、关键帧可读、最终 mp4 可播放。

这个管线的目标不是替代审美判断,而是把视觉内容生产变成 agent 可以迭代的工程对象。换句话说,以后做一支解释型视频,我不想先打开剪辑软件,而是先写一份可以被浏览器渲染、被测试脚本检查、被 agent 修改的 motion deck。

这才是我从这支视频里拿走的东西:HTML 不是网页,是给 agent 用的视觉 IR。
