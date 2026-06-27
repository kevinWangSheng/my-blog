# 文章工艺细节(作者须知)

T19 给文章详情页加了四个「不炫技、但显贵」的工艺细节。三个是自动的(作者无需做任何事),一个需要作者显式开启。视觉参照 `design-previews/premium-touches.html`,落地代码在 `site/src/components/DetailPage.astro` 与 `site/src/styles/global.css`。

## 自动生效(作者无需操作)

- **① 首字下沉 Drop cap** —— 仅 **essays** 详情页正文首段会自动放大首字。判定在 `DetailPage.astro` 的 `essayLeadsWithLetter()`:首段以字母 / 中文起头才下沉;以引号、括号、标点起头则跳过(避免 `::first-letter` 带上前导标点放大后突兀)。notes / logs / projects / links **不下沉**。
  - 想让某篇 essay 下沉,就让正文第一段以正常文字开头,别用引用块 / 列表 / 标点 / `> ` 起头。
- **③ 脚注 hover/focus 预览 Footnote popover** —— 用标准 Markdown 脚注语法即可,弹出预览自动生成:
  ```markdown
  正文里的某句话[^a]。

  [^a]: 这是脚注内容,鼠标悬停或键盘聚焦脚注号即可就地预览。
  ```
  无 JS 时脚注号仍是跳到页尾的普通链接(渐进增强)。
- **④ 标题悬停锚点 Heading anchor** —— 正文 `##` / `###` 标题悬停 / 聚焦时,左侧浮现 `#` 锚链接,可复制章节深链。静止时隐藏,不打扰。触屏隐藏(标题 `id` 仍可深链)。

## 需要作者显式开启

- **② 放大引用 Pull quote** —— 把正文金句拎出来放大呈现。在 Markdown 里用一个带 `pull-quote` 类的 `blockquote`(Astro 默认允许行内 HTML):
  ```html
  <blockquote class="pull-quote">
    克制得当=高级,过度=廉价;真正的精致来自工艺。
  </blockquote>
  ```
  语义上仍是 `<blockquote>`(不是纯样式 div)。样式:展示字体、斜体、强调色、左侧琥珀色竖线。普通 `> ` 引用块不受影响,仍是原来的带底色样式。

## 边界

这四项只在文章详情页生效,全部主题感知(浅 / 暗双色正确)、键盘可达、`prefers-reduced-motion` 友好。不引入任何粒子 / 流动 / 3D / 额外入场动画。详见 `design-previews/spec/premium-touches-plan.md`。
