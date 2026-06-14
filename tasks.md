# tasks.md — 个人博客重建任务拆分

> 阶段:⑤实现 ⇄ ⑥自验证
> 状态:首轮工程闭环已完成,但 ⑦ human 验收未通过;当前进入体验返工任务。
> 依据:`AGENTS.md`、`CONVENTIONS.md`、`DECISIONS.md`、`plan.md`。
> 原则:每完成一条任务,先自验证,再做一个小而可回退的提交。agent 不 push、不部署。

## 执行规则

- 新站只在 `site/` 内实现;cutover 前不改旧 Hugo 部署链路。
- 实现分支为 `rebuild`;`main` 保持旧站部署源直到 ⑦验收通过。
- 包管理器固定 `pnpm`。
- 允许依赖范围:Astro 核心、Astro 官方 RSS 所需包、已决策的本地 UI 验证依赖。不得引入第三方 UI 组件库、Three.js、GSAP、Framer Motion 等重 UI/动画库。
- UI 方向已按 human 反馈修正为:清爽、宁静、留白充足、阅读优先的现代知识花园 / 安静实验室;保留少量 agent/lab 结构感,不再以强 AI Lab Manual / 高对比实验舱作为第一版主方向。
- 固定自验证回路为 `pnpm ui-verify` / `scripts/ui-verify.mjs`;Playwright MCP 只作临时探索辅助。
- 任一自验证失败,回到上一个干净点重做,不在错误实现上层层打补丁。
- 每个返工任务按 TDD 风格执行:先写清楚局部验收与整体不偏离验收 → 实现 → agent 自验证 → **独立 subagent 对抗性验收**。agent 自验证和 subagent 对抗验收都通过,才允许勾选任务。
- 对抗性验收必须明确要求 subagent 挑刺,检查“局部是否真的满足本任务”和“整体是否偏离站点目标/审美方向/流程边界”;不得只复述主 agent 结论。

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
- [ ] 添加用于验证 UI 的少量手写样本:1 个项目、2–3 条 notes、1 条 log、1 篇 essay、3–5 个 links。

验收标准:
- Astro build 能校验所有示例内容 schema。
- 示例内容覆盖首页、列表页、详情页和 RSS 的真实密度。
- 无真实 secrets、私人信息或旧站 Notion 同步内容误迁移。
返工备注:
- 首轮样本满足 schema/build,但 human 验收认为“没有足够文章可以阅读”。后续 T14 需要补足真实阅读密度后,本项才重新视为完成。


### T03 — 实现站点基础壳与设计 token

> 历史首轮任务。当前审美 token 返工由 T15 执行;本节旧“深色/荧光/原型提取”口径不再作为当前执行基线。

- [ ] 按 T15 新审美方向重做 `tokens.css`:清爽、宁静、留白充足、阅读优先,不再从旧强 AI Lab Manual 原型提取深色荧光基线。
- [x] 实现全局样式、基础布局、导航、Footer、内容容器、Markdown 排版。
- [x] 实现 `prefers-reduced-motion: reduce` 降级策略。
- [x] 不写死散落颜色/间距;页面和组件优先使用 token。

验收标准:
- 首页和内容页共享同一套视觉系统。
- 当前清爽宁静审美成立,且正文对比度、行宽、行距适合长时间阅读。
- reduced-motion 模式下无核心信息丢失。

### T04 — 实现首页信息架构

- [x] 按默认顺序实现首页区块:Hero / Learning Now / Featured Projects / Recent Notes & Logs / Essays / Links / Footer。
- [x] Hero 在 5 秒内说明 Shawn 是谁、当前关注什么、站点价值与主要入口。
- [x] Projects 作为能力/作品入口拥有更强展示权重。
- [x] Notes/Logs 呈现“正在生成”的状态,但不退化成传统博客时间线。
- [ ] 加入克制的 CSS/SVG/Canvas/IntersectionObserver 视觉与 scroll reveal,不引重动画库。

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

- [x] 确认根目录 `pnpm ui-verify` 可对 `site/dist` 执行。
- [x] 如需要,补齐脚本与 site build 的路径约定,但不把 UI 验证塞进部署 CI。
- [x] 对首页、一个长文页至少跑一次 build + ui-verify。
- [x] 保存并汇报 `out/summary.json` 中的 lighthouse、axe、console、截图路径。

验收标准:
- `pnpm --dir site build` 通过。
- `pnpm ui-verify -- --serve site/dist --path /` 通过或给出需回退修正的客观失败。
- axe 无 critical/serious;console 无错误;Lighthouse 分数若低于 80,需收敛实现后重跑。

### T10 — 首轮视觉/交互自检与收敛

> 历史首轮任务。当前视觉/交互自检由 T13–T17 重新执行;不再按旧“技术审美 / AI Lab Manual”口径验收。

- [ ] 用浏览器或 Playwright MCP 临时探索首页、移动端、内容页和滚动动效。
- [ ] 对照 `tasks.md` T13–T17 检查:blog 基本功能、清爽宁静审美、5 秒理解、学习/作品平衡、Markdown 阅读、短 note、Projects 展示强度、移动端美感和 scroll reveal。
- [ ] 对不达标处回退或重做,不堆补丁。
- [ ] 形成 ⑦验收材料:本地预览地址、关键截图路径、自验证摘要、已知限制。

验收标准:
- 首页首屏具备清爽、宁静、阅读优先的知识空间气质,且不普通模板化。
- 长文阅读舒适;短内容不显空;Projects 足够像作品入口。
- reduced-motion 与移动端已实际看过。

### T11 — 准备 human ⑦结果验收

- [ ] 确认本轮任务全部已提交且工作区干净。
- [ ] 汇总验收入口:本地预览命令、首页/各一级页面/RSS/示例详情页路径、截图目录、自验证摘要。
- [ ] 明确未做事项:未 push、未部署、未 cutover、未迁移旧内容。

验收标准:
- human 只需要看预览和关键截图,不需要自己跑验证。
- 若 ⑦通过,下一阶段才进入 ⑧发布/cutover;若不通过,按反馈回到具体任务重做。

### T13 — Blog 基本功能保障与阅读链路验收

> 返工来源:human 反馈“最基础的 blog 功能、阅读、页面、文字渲染、文章跳转、使用、页面布局都必须先保证”。本任务优先级高于审美和高级动效;它是后续所有体验任务的地基。

- [ ] 明确站点基本路径清单:首页、About、Projects 列表/详情、Notes 列表/详情、Logs 列表/详情、Essays 列表/详情、Links、404、RSS、sitemap;并把最终 URL 清单写入验收摘要,确保可复跑。
- [ ] 每个导航入口都能打开真实页面;每个列表页至少能进入一个对应详情页;所有详情页有可阅读正文而不是空壳。
- [ ] Markdown 常见元素渲染正常:段落、二级/三级标题、列表、链接、行内 code、blockquote、长段落、中文/英文混排。
- [ ] 文字基础可读:桌面和移动端没有横向溢出、正文不贴边、行宽不过长、行距舒适、颜色对比足够。
- [ ] 站内链接、RSS 链接、sitemap、favicon、404 都可访问,浏览器 console 无 error/warning。
- [ ] reduced-motion 模式下内容默认可见,不依赖动效才能阅读。

局部验收标准:
- `pnpm --dir site build` 通过,且生成上述页面与详情路由。
- 用脚本或 Playwright 检查站内链接:所有站内页面/RSS href 无 404;列表到详情的跳转可用。
- 用浏览器实际打开首页、Essays 列表、至少 2 篇文章详情、Notes 列表、Projects 详情、404、RSS。
- 375/768/1440 三个断点截图无横向滚动条、标题溢出、正文被遮挡或导航不可用。

整体不偏离验收:
- 基本功能修正不能破坏 agent 内容检查/同步工具、RSS、项目分支/部署边界。
- 不能为了修布局删除内容类型、隐藏入口或降低 Projects/Notes/Logs/Essays 的区分度。

对抗性验收:
- [ ] 主 agent 自验证通过后,spawn 独立 subagent 做对抗性测试:它必须按普通访客路径随机点击导航和列表,尝试找 404、空详情、不可读文字、移动端溢出、console error、RSS/sitemap 问题。
- [ ] subagent 必须输出“阻塞项 / 非阻塞风险 / 已验证证据”;若有阻塞项,本任务不得勾选。

### T14 — 内容阅读密度补足

> 返工来源:human 反馈“没有文章什么的可以阅读”。首轮样本只够测试 schema,不够验收真实阅读体验。

- [ ] 至少补足 3 篇可阅读 essays,每篇有明确主题、起承转合和不少于 700 中文字或等效密度;每篇 frontmatter 或正文开头标明内容性质:样例、来自已有材料整理、或真实可公开文章。
- [ ] 至少补足 6 条 notes,其中至少 3 条能从列表进入详情并有实质正文,不是一句话占位;不得伪造 Shawn 的经历、项目成果、外部评价或未经确认的个人判断。
- [ ] 至少补足 2 条 logs,能体现阶段变化和当前工作进展。
- [ ] 首页、Essays、Notes、Logs 列表能看出内容层次和真实密度;不能只显示一两张卡片。
- [ ] RSS 包含新增公开 essays/logs/notes,并能从站内发现。

局部验收标准:
- `pnpm --dir site build` 能校验全部内容 schema。
- Essays 列表至少 3 篇;Notes 列表至少 6 条;Logs 列表至少 2 条;详情页均可打开。
- 内容不得包含真实 secrets、私人信息、旧站 Notion 未审核迁移内容、“禁止发布”标记,也不得伪造个人经历、项目成果、客户/用户反馈或外部背书。

整体不偏离验收:
- 示例内容要服务站点定位:AI 学习、agent 系统、项目实践、知识工作流;不要为了凑数写泛泛而谈的博客水文。
- 内容密度提升后,首页仍保持清爽宁静,不能变成信息噪声墙。

对抗性验收:
- [ ] 主 agent 自验证通过后,spawn 独立 subagent 审查:它必须随机打开列表和详情页,判断是否“真的有文章可读”、是否内容空泛、是否 RSS/导航/详情链路完整。
- [ ] subagent 需尝试找私密/secret/禁止发布风险;若发现风险,本任务不得勾选。

### T15 — 审美方向重构:清爽宁静的知识空间

> 返工来源:⑦ human 验收反馈。当前版本偏强技术实验舱,不符合“清爽、宁静、更好一点的审美”。必须在 T13 基本功能和 T14 内容密度不倒退的前提下执行。

- [ ] 重做视觉 token:从强荧光深色,调整为宁静底色、低饱和强调色、柔和边界、舒展留白、稳定正文色。
- [ ] 首页首屏从巨大冲击标题改为更安静的个人知识空间入口,5 秒内仍说明 Shawn 是谁、当前关注什么、站点价值与主要入口。
- [ ] 内容卡片改成更像可阅读文章/笔记入口,而不是仪表盘模块;卡片层级要清楚但不过度炫技。
- [ ] 保留少量 agent/lab 结构感,但去掉廉价赛博朋克、强荧光扫描、压迫性大标题和过重背景纹理。
- [ ] 移动端优先检查:首屏不拥挤,导航不压迫,标题不溢出,正文第一段能在自然视线内开始。

局部验收标准:
- 首页、列表页、详情页在 375/768/1440 三个断点均无横向溢出。
- 长文页正文行宽、行距、字号适合连续阅读;标题有气质但不压迫正文。
- `prefers-reduced-motion: reduce` 下页面仍完整可用且不丢信息。

整体不偏离验收:
- 仍然是“学习自留地 + 项目/能力入口”,不能退化成普通博客模板或纯简历页。
- 仍保持 agent 内容流、RSS、Projects 权重、Notes/Logs/Essays 差异。
- 不新增 UI 组件库、重动画库或部署链路改动。

对抗性验收:
- [ ] 主 agent 自验证通过后,spawn 一个独立 subagent 审查:它必须从“审美是否真的清爽宁静、是否普通模板化、移动端是否压迫、阅读是否舒服、是否偏离站点目标”角度挑刺。
- [ ] subagent 输出阻塞项/非阻塞风险/证据路径;若有阻塞项,本任务不得勾选。

### T16 — Scroll reveal 与交互质感重做

> 返工来源:human 反馈没有看到“下滑显示、上滑消失”等高级动作。首轮 IntersectionObserver 存在,但视觉反馈不明显,不能算完成。

- [ ] 先写清楚 reveal 规则:元素进入视口时柔和显示/位移/层级展开;离开视口时回到待激活状态;上滑回看时可再次自然出现。
- [ ] 用 CSS + IntersectionObserver 实现,不引入 GSAP/Framer Motion/Three.js 等重动画库。
- [ ] 动效风格匹配“清爽宁静”:轻、慢、细腻,不做强烈扫描线或炫技闪烁。
- [ ] 卡片、章节标题、正文 metadata 至少三类元素有可感知但克制的 reveal。
- [ ] reduced-motion 下关闭位移/透明动画,内容默认可见。

局部验收标准:
- Playwright MCP 或等效浏览器检查证明并记录具体检查方式:初始首屏外的 reveal 元素处于待激活状态;下滑进入后变为可见;上滑离开/回到初始区域后状态按规则切换。
- 浏览器 console 无 error/warning;动效不导致布局跳动、链接不可点或阅读被遮挡。
- `pnpm ui-verify -- --serve site/dist --path /` 和至少一个长文页通过。

整体不偏离验收:
- 动效增强后不能破坏清爽宁静风格,不能让页面变回高对比实验舱。
- 动效服务信息层级,不是为了展示技术。

对抗性验收:
- [ ] 主 agent 自验证通过后,spawn 独立 subagent 审查:它必须实际滚动页面,报告 reveal 是否可感知、是否上滑消失/回看成立、是否 reduced-motion 友好、是否有性能/阅读干扰。
- [ ] subagent 若认为“代码有动效但用户感知不到”,本任务不得勾选。

### T17 — 局部 + 整体双层验收协议

- [ ] 为 T13/T14/T15/T16 每个任务保存验收摘要:改动范围、局部验收证据、整体不偏离证据、subagent 对抗结论。
- [ ] 每个大任务完成后都运行:build、首页和长文页 UI verify、浏览器人工路径检查;如涉及内容变更,还必须运行内容检查相关命令,否则在验收摘要中记录“未涉及内容变更”。
- [ ] 每个大任务完成后都检查整体:导航、首页定位、Projects 权重、Notes/Logs/Essays 差异、RSS、移动端、reduced-motion、旧站部署边界。
- [ ] 所有返工任务通过后再进入 T11 重新准备 ⑦验收材料。


对抗性验收输出模板:
- 执行命令:
- 访问路径 / URL 清单:
- 截图 / summary 路径:
- 阻塞项:
- 非阻塞风险:
- 结论:通过 / 不通过 / 有条件通过

验收标准:
- 每个返工任务都有主 agent 证据和 subagent 对抗验收结论。
- 若主 agent 与 subagent 结论冲突,默认按未通过处理,继续返工或把冲突点交给 human 判断。
- `tasks.md` 只勾选已经双层验收通过的任务。

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

⑦ human 验收未通过。当前下一步是按 T13 → T14 → T15 → T16 → T17 返工:先保证 blog 基本功能/阅读/跳转/渲染,再补内容阅读密度,再做清爽宁静审美重构,再重做 scroll reveal,最后执行主 agent + subagent 对抗性双层验收。T11 重新通过后才回到 ⑦验收;T12 仍只在 ⑦通过后执行。
