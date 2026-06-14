# tasks.md — 个人博客重建任务拆分

> 阶段:④任务拆分
> 状态:待执行。完成本文件后进入 ⑤实现 ⇄ ⑥自验证。
> 依据:`AGENTS.md`、`CONVENTIONS.md`、`DECISIONS.md`、`plan.md`。
> 原则:每完成一条任务,先自验证,再做一个小而可回退的提交。agent 不 push、不部署。

## 执行规则

- 新站只在 `site/` 内实现;cutover 前不改旧 Hugo 部署链路。
- 实现分支为 `rebuild`;`main` 保持旧站部署源直到 ⑦验收通过。
- 包管理器固定 `pnpm`。
- 允许依赖范围:Astro 核心、Astro 官方 RSS 所需包、已决策的本地 UI 验证依赖。不得引入第三方 UI 组件库、Three.js、GSAP、Framer Motion 等重 UI/动画库。
- UI 方向以 `prototypes/ai-lab-manual-home.html` 为视觉基线:AI Lab Manual / AI 实验手册,审美优先但阅读不可牺牲。
- 固定自验证回路为 `pnpm ui-verify` / `scripts/ui-verify.mjs`;Playwright MCP 只作临时探索辅助。
- 任一自验证失败,回到上一个干净点重做,不在错误实现上层层打补丁。

## 任务列表

### T00 — 建立实现分支与旧站保护点

- [x] 从当前规划基线创建/切换到 `rebuild` 分支。
- [x] 确认旧站当前状态可恢复:已有 git 历史即可;如本地无 `old-site-frozen` tag,创建本地 tag 指向切换前旧站基线。
- [x] 不 push tag、不 push 分支。

验收标准:
- `git branch --show-current` 输出 `rebuild`。
- `git status --short` 无非预期改动。
- 旧站文件未被删除或覆盖。

### T01 — 创建 Astro 新站骨架

- [x] 在 `site/` 创建最小 Astro 静态站骨架。
- [x] 配置 `pnpm` 可在仓库根或 `site/` 内稳定安装/构建;避免生成物进入 git。
- [x] 建立基础目录:`src/pages`、`src/layouts`、`src/components`、`src/styles`、`src/lib`、`src/content`、`scripts`、`public`。
- [x] 保留旧站根目录文件不作为实现目标。

验收标准:
- `site/` 存在且包含 Astro 项目入口。
- `pnpm install` 与 `pnpm --dir site build` 可运行通过。
- `dist/`、`.astro/`、`node_modules/` 未进入 git。

### T02 — 建立内容模型与示例内容

- [x] 建立 Astro content collections schema: `projects`、`notes`、`logs`、`essays`、`links`。
- [x] 实现共享最小字段:`title`、`description`、`date`、`updated?`、`tags`、`source?`、`visibility`。
- [x] 为各集合添加少量已规划字段:projects/status/role/repo/demo/period; notes/topic/related; logs/period/summary; essays/canonical/series; links/url/category/feed/note。
- [x] 添加用于验证 UI 的少量手写样本:1 个项目、2–3 条 notes、1 条 log、1 篇 essay、3–5 个 links。

验收标准:
- Astro build 能校验所有示例内容 schema。
- 示例内容覆盖首页、列表页、详情页和 RSS 的真实密度。
- 无真实 secrets、私人信息或旧站 Notion 同步内容误迁移。

### T03 — 实现站点基础壳与设计 token

- [x] 从原型提取第一版 `tokens.css`:深色基底、1 个主荧光色、1 个低频强调色、字体、间距、圆角、边框、阴影。
- [x] 实现全局样式、基础布局、导航、Footer、内容容器、Markdown 排版。
- [x] 实现 `prefers-reduced-motion: reduce` 降级策略。
- [x] 不写死散落颜色/间距;页面和组件优先使用 token。

验收标准:
- 首页和内容页共享同一套视觉系统。
- 深色技术感成立,但正文对比度、行宽、行距适合长时间阅读。
- reduced-motion 模式下无核心信息丢失。

### T04 — 实现首页信息架构

- [x] 按默认顺序实现首页区块:Hero / Learning Now / Featured Projects / Recent Notes & Logs / Essays / Links / Footer。
- [x] Hero 在 5 秒内说明 Shawn 是谁、当前关注什么、站点价值与主要入口。
- [x] Projects 作为能力/作品入口拥有更强展示权重。
- [x] Notes/Logs 呈现“正在生成”的状态,但不退化成传统博客时间线。
- [x] 加入克制的 CSS/SVG/Canvas/IntersectionObserver 视觉与 scroll reveal,不引重动画库。

验收标准:
- 首页同时表达“学习自留地”和“作品/能力入口”。
- 第一屏不是默认博客模板、普通简历页或通用 AI landing page。
- 移动端布局仍有设计感,不是粗暴纵向堆叠。

### T05 — 实现一级页面与内容详情页

- [x] 实现 About 页面:方向、能力、正在关注、联系方式、代表项目入口。
- [x] 实现 Projects、Notes、Logs、Essays、Links 列表页。
- [x] 实现 Projects/Notes/Logs/Essays 详情页。
- [x] 为各内容类型写清楚差异化文案,避免访客分不清 Notes/Logs/Essays。
- [x] 处理 404 和空集合状态。

验收标准:
- 所有导航入口可点击到有效页面。
- Markdown 长文、短 note、项目说明都能自然成立。
- build 无路由生成错误,无明显 broken internal link。

### T06 — 实现 RSS 与基础站点元信息

- [x] 生成全站综合 RSS feed。
- [x] feed 初始包含 `essays`、`logs` 和公开 `notes`;projects 是否进入 feed 按内容密度暂不强制。
- [x] 添加基础 metadata、OpenGraph、sitemap/robots 的最小可用版本。
- [x] 导航和 Footer 暴露 RSS 入口。

验收标准:
- `/rss.xml` 可构建生成且包含示例内容。
- 首页、列表页、详情页有合理 title/description。
- RSS 链接可从站内发现。

### T07 — 实现 agent 内容检查工具

- [x] 在 `site/scripts/` 实现 `content:check` 命令。
- [x] 支持单篇 Markdown 与目录 + `manifest.json` 两种输入。
- [x] 检查 manifest 发布意图、type 映射、front matter 最小字段、slug/path 安全、冲突、标题/摘要/正文非空。
- [x] 检查疑似 secrets/token/key、私密标记、禁止发布标记。
- [x] 输出机器可读或结构稳定的检查报告,供 agent 决定修正。

验收标准:
- 合法样本通过 check。
- 缺字段、未知 type、路径逃逸、slug 冲突、疑似 secret、禁止发布标记均失败并给出明确原因。
- check 不写入站点内容目录。

### T08 — 实现 agent 内容同步工具

- [x] 在 `site/scripts/` 实现 `content:sync` 命令。
- [x] sync 必须先复用 `content:check`;失败不写入。
- [x] 将输入 Markdown 规范化写入 `site/src/content/<collection>/...`。
- [x] 规范化 slug/文件名,补齐缺省字段,避免覆盖已有内容;覆盖需要显式参数或失败。
- [x] 输出同步报告:写入路径、跳过项、失败原因。

验收标准:
- 单篇 Markdown 可同步到正确 collection。
- manifest 批量输入可同步多篇内容。
- 冲突、失败、跳过场景行为明确且可复现。
- 同步后 Astro build 通过。

### T09 — 接入本地自验证回路

- [ ] 确认根目录 `pnpm ui-verify` 可对 `site/dist` 执行。
- [ ] 如需要,补齐脚本与 site build 的路径约定,但不把 UI 验证塞进部署 CI。
- [ ] 对首页、一个长文页至少跑一次 build + ui-verify。
- [ ] 保存并汇报 `out/summary.json` 中的 lighthouse、axe、console、截图路径。

验收标准:
- `pnpm --dir site build` 通过。
- `pnpm ui-verify -- --serve site/dist --path /` 通过或给出需回退修正的客观失败。
- axe 无 critical/serious;console 无错误;Lighthouse 分数若低于 80,需收敛实现后重跑。

### T10 — 首轮视觉/交互自检与收敛

- [ ] 用浏览器或 Playwright MCP 临时探索首页、移动端、内容页和滚动动效。
- [ ] 对照 `plan.md` 12.9 检查:技术审美、5 秒理解、学习/作品平衡、Markdown 阅读、短 note、Projects 展示强度、移动端美感。
- [ ] 对不达标处回退或重做,不堆补丁。
- [ ] 形成 ⑦验收材料:本地预览地址、关键截图路径、自验证摘要、已知限制。

验收标准:
- 首页首屏具备 AI Lab Manual 气质且不廉价。
- 长文阅读舒适;短内容不显空;Projects 足够像作品入口。
- reduced-motion 与移动端已实际看过。

### T11 — 准备 human ⑦结果验收

- [ ] 确认本轮任务全部已提交且工作区干净。
- [ ] 汇总验收入口:本地预览命令、首页/各一级页面/RSS/示例详情页路径、截图目录、自验证摘要。
- [ ] 明确未做事项:未 push、未部署、未 cutover、未迁移旧内容。

验收标准:
- human 只需要看预览和关键截图,不需要自己跑验证。
- 若 ⑦通过,下一阶段才进入 ⑧发布/cutover;若不通过,按反馈回到具体任务重做。

### T12 — ⑧发布 / CI-CD cutover（仅 ⑦通过后执行）

> 当前阶段不执行。本任务是发布阶段占位,防止后续 agent 提前或遗漏 CI/CD 切换。

- [ ] 在 ⑦结果验收通过后,把旧 Hugo workflows 迁移/替换为 Astro GitHub Pages workflow。
- [ ] 新 workflow 以 `site/` 为构建根,使用 `pnpm` 安装依赖,构建 `site/dist`。
- [ ] 优先使用 GitHub Pages 官方链路 / `withastro/action` 等 Astro Pages 方案;不要把 Playwright、axe、Lighthouse UI 自验证塞进部署 CI。
- [ ] 处理旧站遗留发布源:确认是否停止 Notion→Hugo workflow、是否停止旧 `gh-pages` 发布方式、是否需要清理旧产物跟踪。
- [ ] 只在 human 明确通过 ⑦后 push / 发布 / cutover。

验收标准:
- `.github/workflows/` 中不再有会误触发旧 Hugo/Notion 部署的线上链路。
- GitHub Pages 云端构建 Astro 新站成功,发布产物来自 `site/dist`。
- 本地 UI 自验证仍只在 ⑥执行,不成为部署 CI gate。
- 发布后线上站点可访问;RSS、首页、一级页面和示例详情页可打开。

## 当前下一步

T00 已完成。下一步从 T01 开始创建 `site/` Astro 新站骨架;之后每条任务遵循:实现 → 自验证 → 小提交 → 更新本文件勾选状态。T12 只有在 ⑦结果验收通过后才允许执行。
