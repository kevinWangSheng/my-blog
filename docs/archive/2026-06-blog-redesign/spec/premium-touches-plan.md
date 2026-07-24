# 实现规划 — 文章工艺细节(高级感细节,非炫技特效)

> 性质:这是给实现 session 的**规划/验收标准**,不是已上线代码。建议在 `tasks.md` 立为 **T19「文章工艺细节」**(按项目 T-编号与 out/acceptance 三件套流程)。
> 视觉参照:`design-previews/premium-touches.html`(四个细节的样稿)。
> 设计系统:沿用已落地的方向 B,变量见 `site/src/styles/tokens.css`。
> 边界:**只做下面四项**。不得新增粒子 / 流动 / 3D / 额外入场动画等炫技特效(会掉档,见 `premium-gate.md` 的"克制=高级")。不得回退已落地的 B 系统 / 噪点 / 暗色 / View Transitions。不动其他 session 未提交的文件。

---

## 共同约束(四项都适用)

- 纯 CSS 优先;需要 JS 的只有脚注预览,且必须**渐进增强**(JS 失效时脚注链接仍能跳转)。
- **可访问**:键盘可达、可聚焦、可关闭;`prefers-reduced-motion` 下去掉过渡。
- **暗色**:用主题感知 token(`--c-sage` 等),浅/暗两套都要看着对。
- 落点集中在 `site/src/components/DetailPage.astro` 与 `site/src/styles/global.css`;标题锚点可能涉及 `site/astro.config.mjs`(rehype 插件)。
- 验收门:`pnpm --dir site build` 通过 + `pnpm ui-verify`(axe 0、Lighthouse a11y 保持 100、perf ≥90)+ 一个 essay 页面肉眼对照样稿。

---

## ① 首字下沉 Drop cap

- **目标**:文章正文第一段首字放大、下沉,出版物质感。
- **落点**:**仅 essays 详情页**正文首段(notes/logs/projects 短内容不加,避免突兀)。
- **实现**:`.prose > p:first-of-type::first-letter`,`float:left`,`font-family:var(--font-display)`,约 `4.4rem`、`line-height:.82`、`color:var(--c-accent)`,右/下留白。
- **边界情况**:若首段以引号/标点开头则不应用(可用 `:not()` 或在内容层避免);中文首字可正常下沉。
- **可访问**:纯装饰,无 a11y 影响。

## ② 放大引用 Pull quote

- **目标**:把正文金句拎出来放大呈现,给长文节奏一个停顿。
- **落点**:**opt-in 能力**,不是每篇都有。需要一个**作者书写约定**(三选一,实现者定并写进内容指南):
  - a) MDX 用 `<PullQuote>` 组件;或
  - b) Markdown 里给特定 blockquote 加类(如 `> ` + 约定标记 → remark 转 `.pull-quote`);或
  - c) 先只提供 `.pull-quote` 样式 + 文档,作者手动用。
- **实现**:`font-family:var(--font-display)`,斜体,约 `1.7rem`、`line-height:1.3`、`color:var(--c-accent)`,左边 `3px solid var(--c-accent-2)`。
- **可访问**:语义上仍是 `<blockquote>` 或 `<aside>`,不要做成纯样式 div。

## ③ 脚注 hover 预览 Footnote popover

- **目标**:悬停脚注号就地弹出脚注内容,不必跳到页尾。
- **前提**:确认 essays 正文已启用脚注(remark-gfm / rehype footnotes);若未启用,先启用。
- **实现**:小段 JS——读取脚注引用 `href="#fn-x"` 指向的脚注文本,生成 popover;CSS 控制显隐。
- **可访问(关键)**:
  - 键盘可达:脚注号 `:focus` 也要弹出(不只是 `:hover`)。
  - 不抢焦点、可 Esc 关闭;popover 用 `role="tooltip"` + `aria-describedby` 关联。
  - **渐进增强**:无 JS 时脚注号仍是能跳到页尾的普通链接。
  - `prefers-reduced-motion` 下去掉淡入位移。

## ④ 标题悬停锚点 Heading anchor

- **目标**:悬停 h2/h3 时左侧浮现 `#` 锚链接,可复制章节链接,静止时不打扰。
- **实现**:用 `rehype-slug` + `rehype-autolink-headings`(`behavior:'prepend'`)给正文标题自动加 id 与锚 `<a>`;CSS 让锚链接默认 `opacity:0`,`h2:hover .anchor`/`:focus-within` 时显现。
- **可访问**:锚 `<a>` 要有 `aria-label`(如 "链接到本节:<标题>");键盘 focus 时也要可见(`:focus-visible`)。

---

## 落地顺序与验收

1. 先做零风险静态两项:**① 首字下沉 → ② 放大引用样式**(纯 CSS)。
2. 再做交互两项:**④ 标题锚点(rehype)→ ③ 脚注预览(JS 渐进增强)**。
3. 每做完一项:`build` + 在 essay 页肉眼对照样稿。
4. 全部完成:`pnpm ui-verify`,确认 **axe 0 / Lighthouse a11y 仍 100 / perf ≥90**;键盘走查脚注与锚点;浅/暗各看一遍。
5. 按项目流程写 `out/acceptance/T19-plan.md` / `T19-main.md` / `T19-adversarial.md`,通过后再勾选、提交。

## 给实现 session 的提示词(可直接粘)

```
任务:实现「文章工艺细节」(在 tasks.md 立为 T19)。开工前读 AGENTS.md / CONVENTIONS.md,先 git status 确认无他人未提交改动会被覆盖。
规格照 design-previews/spec/premium-touches-plan.md,视觉对照 design-previews/premium-touches.html,设计变量用 site/src/styles/tokens.css。
只做规格里的四项:首字下沉、放大引用、脚注 hover 预览、标题悬停锚点。不得新增粒子/流动/3D/额外入场动画,不得回退已落地的 B 系统/噪点/暗色/View Transitions。
落点:DetailPage.astro + global.css(+ astro.config.mjs 的 rehype 插件)。
全部键盘可访问 + reduced-motion 友好 + 浅暗双主题。
做完:pnpm --dir site build 通过、pnpm ui-verify 达 axe 0 / Lighthouse a11y 100 / perf ≥90;写 out/acceptance/T19-{plan,main,adversarial}.md;不要 push/deploy。
```
