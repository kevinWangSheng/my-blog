# CONVENTIONS.md

开发与协作规范(稳定层)。`AGENTS.md` 引用本文件;对应流程的 ⑤实现 / ⑧发布。技术栈 = Astro 静态站(见 `DECISIONS.md`)。命令里凡涉及具体脚本的,待 Astro 脚手架建好后回填确切形式。

## Git 工作流

### 分支模型(重建期)
- `main` = **当前部署源**(现仍是旧站,继续服役直到 cutover)。
- 旧站冻结:打 tag `old-site-frozen` 钉住旧站最后状态;旧站不再收 commit。
- 新站在 **`rebuild`** 分支上推进;经 ⑦验收 后在 ⑧ 把部署源切到新站(合并 `rebuild` → `main`)。
- 日常:在当前工作分支上**小步提交**,一个任务 = 一个(或少数)聚焦提交。

### 提交
- ✅ 只在 ⑥自验证(build / 类型 / 链接 / 截图)通过后才 commit;失败尝试用 `git stash` / `git restore`,不留成正式提交。
- 格式:Conventional Commits —— `feat|fix|docs|refactor|chore|style(scope): subject`。
- 颗粒度:`tasks.md` 里勾掉的一条 ≈ 一次提交。
- 署名:关闭 AI Co-Authored-By(Claude Code 设 `attribution: false`);提交信息保持任务本身可读,不额外写 AI 归属。

### push / 发布(对应人工门)
- 🚫 agent 不 push、不部署。
- push → ⑦人工结果验收 通过之后。
- 部署(GitHub Pages)→ ⑧发布,由 CI(`withastro/action`)在云端构建 `dist` 并部署。
- PR:solo 不强制;如想"合并前再过一道 diff",可用 PR 作自我 review gate。

### .gitignore(Astro)
- 必含:`dist/` `.astro/` `node_modules/` `.env*` `*.log` `.DS_Store` `.claude/worktrees/`。
- 🚫 构建产物不进 git(`dist` 由 CI 生成)。注:Astro 里**源** `public/`(图标、robots.txt 等)本应跟踪;旧站那条"`public/` 误跟踪"是把**产物**塞进了版本控制,cutover 时用 `git rm -r --cached` 处理。

### 回退纪律
- 未提交、要丢弃 → `git restore`;想暂存试别的 → `git stash`(**保留失败信息**,别直接丢)。
- 已 push / 已是历史 → `git revert`(不改写已发布历史)。
- 本地未推送、想重排 → `git reset`;⚠️ `reset --hard` / force-push 属破坏性,先确认。

## 多 agent worktree

并行跑多个 agent 时用 git worktree 隔离,避免互相覆盖未提交改动、避免上下文串味。

### 布局与命名
- 原则:**1 任务 = 1 分支 = 1 worktree = 1 agent**;并行任务之间**不写同一批文件**(分派前先做"文件互斥"检查)。
- Claude Code 原生(首选,最轻):`claude --worktree <task-slug>` → worktree 落在 `.claude/worktrees/`,分支 `worktree-<task-slug>`(该路径已在 `.gitignore`)。
- Codex 等其它 agent:`git worktree add ../site-<task> -b <task>`,再在该目录里启动。

### 环境与依赖(Astro / Node)
- 新 worktree 不带 gitignored 文件:用 `.worktreeinclude`(`.gitignore` 语法)列出 `.env` `.env.local`,Claude Code 会自动拷入。
- 包管理器固定为 **pnpm**。每个 worktree 各自装依赖;推荐 `enableGlobalVirtualStore: true`(各 worktree 软链同一 store,近零额外磁盘、装得快)。
- dev server 端口冲突:每个 worktree 用不同端口(`astro dev --port 43xx`),Astro 默认 4321。

### 合并与清理
- 合并前:rebase 到最新基线 → **逐文件看 diff**(agent 易过度重构 / 越界)→ 在 worktree 内跑 build 通过 → 再合并;多分支按依赖顺序合并。**human 是合并门**。
- 清理:`git worktree remove <path>`;`git worktree list` + `git worktree prune` 查悬挂;🚫 不要 `rm -rf` worktree 目录(留下脏管理文件)。
- 可选:`WORKTREES.md` 记录 活动分支 / agent / 任务 / 状态,防止重复分派。

## UI 自验证回路(⑥)

对应流程 ⑥自验证。每次 UI 改动落地后,agent 自己跑完这套回路才能宣称完成;失败 → 按上面「回退纪律」回到干净点重做,**不层层打补丁**。工具链见 `DECISIONS.md` 的 `D-20260614-UI验证工具链`;**驱动方式 = Skill `/ui-verify` + 项目脚本 `scripts/ui-verify.mjs`**(见 `D-20260614-UI验证驱动方式`;Claude `.claude/skills/ui-verify/`、Codex `.agents/skills/ui-verify/` 共用同一脚本;Playwright MCP 仅作临时探索,不进固定回路)。**全程仅本地,不进 ⑧ 部署 CI。**

### 核心回路:改 → 渲染 → 跑脚本 → 判定
1. **build / 起服务**:`astro build` 通过(无类型 / 构建错误),产出静态 `dist/`。
2. **跑客观验证脚本(一把做)**:`pnpm ui-verify -- --serve <dist> --path /`(或 Skill `/ui-verify`)。脚本在 **3 断点**(375 / 768 / 1440)截图(reduced-motion + 冻结动画,落盘 `out/`)、跑 **axe**(wcag2a/aa)、检查 console error/warning、检查 `document.scrollWidth > document.clientWidth` 横向溢出、跑 **lighthouse**(移动端,perf/a11y/seo/best-practices),汇总写 `out/summary.json`。**agent 只读 `out/summary.json` 判定,不逐张回喂截图**;截图路径留 ⑦ human 看。
3. **主观/交互自检(脚本判不了的部分)**:动效 reveal 是否正确、不闪、不挡读、下滑显示/上滑消失是否可感知;克制度(对照 `DECISIONS.md` 的 `D-20260614-UI审美方向修正`:清爽、宁静、留白充足、阅读优先);Markdown 长文可读性。agent 应先用本地浏览器/Playwright MCP 手动探查并留下证据;human 只做 ⑦最终结果验收。若要让 reveal 变成可自动断言,实现需提供稳定状态探针(如 `data-reveal-state` 或明确 class 状态),否则不得声称固定 `ui-verify` 已证明 reveal 成立。
4. **reduced-motion 降级**:必须实现 `prefers-reduced-motion: reduce` 版本;脚本即在 reduce 模式下截图,核验其渲染成立(a11y 硬要求)。
5. **判定**:`summary.ok=false`,或出现 axe critical/serious、lighthouse 任一项 < 目标门槛、console error/warning、横向溢出 → 回退重做,不打补丁。

### UI 实现约定
- 只用 `tokens.css` 的 token,不写死颜色 / 间距值。
- **审美第一,但阅读不可牺牲**:当前审美方向为清爽、宁静、留白充足、阅读优先;Markdown 长文的正文对比度 / 行宽 / 可读性单独核验(强于 axe 的最低线)。
- **动效技术栈**:第一版动效用 CSS / SVG / Canvas / IntersectionObserver 实现;**不引 Three.js / 重动画库**(GSAP、Framer Motion 等)——要引即命中「新增依赖先问」,走 D- 条。
- **样张不再作为当前主基线**:`prototypes/ai-lab-manual-home.html` 仅保留为历史探索参考;当前首版页面以 `DECISIONS.md` 的 `D-20260614-UI审美方向修正` 和 `tasks.md` T13–T17 为准。
- 第一版**不引第三方 UI 组件库 / 框架**(纯 Astro + CSS);若要引,命中「新增依赖先问」。
- 具体 token 取值、断点、页面模板清单属执行层 → 见 `plan.md` / `tasks.md`,不写进本文件。
- 验证命令已就绪:`pnpm ui-verify -- --serve <dir> --path <route>`(对任意静态目录 / Astro `dist/` 复用)。lighthouse 门槛阈值与返工验收属执行层,见 `tasks.md`。
