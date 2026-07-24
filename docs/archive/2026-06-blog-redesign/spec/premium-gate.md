# 高级感门禁清单 + 各页面元素规格 — 方向 B「Warm Garden」

> 这是**规格 / 验收标准**,不是已上线代码。负责实现的 session 照此落地;human 在 ②决策 / ⑦验收 用此勾选。
> 视觉事实源:`design-previews/direction-b-garden.html`(首页/列表/卡片)、`design-previews/direction-b-article.html`(文章页/排版/动效)。
> Token 事实源:`design-previews/spec/tokens.css`。
> 硬约束:动效必须有 `prefers-reduced-motion` 兜底;不得让 UI 验证套件进 ⑧ 部署 CI;最终过 ui-verify(axe 0 violations、Lighthouse a11y·perf ≥90)。

---

## A. 高级感由什么组成(核心认知)

高级感**不是一个大动作,是几十个微观决策累加**。给 agent 一个「做得高级」的模糊目标会收敛到平庸(系统字体、纯白底、Bootstrap 味),因为「高级」对它没有定义。**这张清单就是定义**——照着勾,而不是凭灵感。

---

## B. 门禁清单(逐条可勾选)

### B1. 已在样稿验证 —— 落地时必须保留,不许退化
- [ ] 纸白非纯白(`--c-bg:#f7f3e8`)、墨黑非纯黑(`--c-ink:#27332e`)
- [ ] 单一强调色 sage,克制使用;amber 仅点睛(下划线肌理 / 二级标记)
- [ ] 标题用 Fraunces 光学尺寸;大标题收紧字距(`--ls-display`)、全大写标签放宽(`--ls-caps`)
- [ ] 正文 Literata 衬线,阅读宽度 ~72ch(`--measure:720px`),行高 1.75
- [ ] 代码块 = 深色卡片(文件名栏 + 语法配色);浅底直接塞代码 = 廉价,禁止
- [ ] 表格:发丝线、表头浅色块、hover 行高亮;媒体(代码/表/图)可比正文略宽(840px)
- [ ] 圆角 / 阴影走统一刻度(`--r-*` / `--shadow-*`),不要每处自定义
- [ ] 阅读进度条 + 滚动渐显 + 目录跟随高亮,**全部在 reduced-motion 下关闭、内容直接可见**,JS 失效有兜底不白屏

### B2. 样稿尚未加 · ROI 高 —— 落地时补齐(这些最能再上一档)
- [ ] `::selection` 选中色(`--c-selection`)
- [ ] `:focus-visible` 描边(`--c-focus-ring`)—— 兼顾 a11y 与质感
- [ ] 自定义细滚动条(暖中性,不刺眼)
- [ ] `text-wrap: balance`(标题不孤字)+ `text-wrap: pretty`(段落不留寡行)
- [ ] **页面间 View Transitions**(Astro 原生 `<ViewTransitions />`)—— 点开文章丝滑切场,高级感最明显的一招;同样要 reduced-motion 兜底
- [ ] 数字按场景:表格/代码用 tabular,正文可用 oldstyle(`font-variant-numeric`)
- [ ] 链接 `text-underline-offset` + 下划线变色 hover(样稿正文已有,需推广到全站)

### B3. 暗色模式 [待确认,需 ②决策]
- [ ] 设计一套暖调深色(非反色、非纯黑),见 `tokens.css` 的 `[data-theme="dark"]` 提案
- [ ] 加切换控件,记忆用户选择;跟随系统作默认
- [ ] 暗色下代码块、强调色对比度过 axe

### B4. 收尾完整度(看不见,但决定「专业 vs 业余」)
- [ ] 像样的 404 页(承接 B 气质,别用默认)
- [ ] 列表/搜索的空状态文案
- [ ] favicon + OG 分享图(社交预览)
- [ ] `@media print` 文章可打印样式
- [ ] 标题层级语义正确(h1 唯一、不跳级)——既是 a11y 也是排版纪律

---

## C. 各页面元素规格(高级感最怕不一致,每页都要有自己的「构图时刻」)

> 共享件:`BaseLayout.astro`(导航+页脚+字体+base)、`EntryCard` / `ListPage` / `PageHero` / `DetailPage`。
> 原则:**设计系统做一次,页面继承**;但下面标「需单独构图」的不是白拿,要专门设计。

| 页面 | 状态 | 要点 |
|---|---|---|
| **文章正文页** DetailPage | ✅ 样稿已定 | 按 `direction-b-article.html` 落地,含全部排版元素 + 动效三件套 |
| **首页** index | ⚠️ 需单独构图 | hero 构图最影响第一印象;参考 `direction-b-garden.html`(hero + nowcard + notes/essays 双区) |
| **列表页 ×5**(essays/notes/logs/projects/links) | ⚠️ 系统 + 微调 | 统一卡片(EntryCard),按内容类型微调元信息;links 可能是无详情的纯列表 |
| **About** | ⚠️ 需单独构图 | 个人页最能体现品味,值得单独设计,别套通用列表 |
| **404** | ⬜ 待做 | 承接 B 气质的小页面,加分项 |
| **RSS / sitemap** | n/a | 非视觉,保持现有 |

落地顺序建议:`tokens.css` → `BaseLayout`(外壳)→ DetailPage(已有样稿,最稳)→ 首页 → 四组件/列表页 → About / 404 → B2 细节 → B3 暗色。

---

## D. 验收(⑦ 之前 agent 自验,⑦ human 看)
- [ ] `pnpm --dir site build` 通过
- [ ] `pnpm preview:prepare && pnpm ui-verify` → `out/summary.json`:axe 0、Lighthouse a11y·perf ≥90
- [ ] 关键页面(首页 / 文章页 / 一个列表页 / About / 404)逐页对照本清单 B 段勾选
- [ ] reduced-motion 下复查:动效关闭、无内容被藏、无白屏
