# research.md — UI 工作流(agent 做前端)

> ①研究产出。主题:用 AI agent 做 UI 的业界流程 + 该定义哪些内容。
> 方法:2 个研究 subagent(业界流程 / 可视化验证闭环)+ 1 个评估 subagent(针对本仓库约束把关)。
> 结论已落地:决策见 `DECISIONS.md` 的 `D-20260614-UI验证工具链`;回路规范见 `CONVENTIONS.md`。
> 完成后归档到 `docs/archive/<日期>-ui-workflow/`。
> 注:业界部分为公开二手测评 / 厂商博客综述,非独立复现;仓库相关判断由评估 agent 实读 `DECISIONS.md`/`CONVENTIONS.md` 得出。

## 1. 核心结论

agent 做 UI 的质量瓶颈**不在「会不会写 CSS」,而在「能不能看到自己渲染的结果再迭代」**(三类来源一致)。把渲染截图 + 可访问性树喂回多模态模型,可把 UI 调试从 10+ 轮盲改压到 2–3 轮。因此「截图回喂 + a11y 扫描」这条自验证回路比任何 token 体系更值得先建。

## 2. 通用流程(业界)→ 落到本项目自闭环 ⑤⇄⑥

```
设计基调(human 一次性给参考站 + 气质词)
  └─ design tokens(色/字/间距/圆角)         ← agent 在 plan 定值
       └─ 组件→页面(原子→页面,逐组件实现)   ← ⑤ 实现,每组件一次小提交
            └─ 自验证回路 ⑥:
                 build 通过 → 截图(375+1280)回喂自检 → axe a11y → 一次 Lighthouse
                 └─ 任一失败 → git restore/revert 回退,不打补丁
  └─ human 只在 ⑦ 看预览 + 关键截图验收
```

## 3. 该「定」哪些内容(按落地顺序 + 归属)

> 前提:第一版不引第三方 UI 组件库(纯 Astro + CSS),绕开「组件库选型」决策点。

**P0 脚手架阶段**
1. `[human·必要]` 视觉基调:2–3 个参考站 + 几个气质词。轻量,一行写进 `plan.md`,不开正式 D- 条。
2. `[human·必要]` 验证工具链拍板 → 已定 = Playwright + axe-core(见 D-20260614-UI验证工具链)。
3. `[agent·必要]` Astro 脚手架 + `.gitignore`(见 CONVENTIONS.md)。
4. `[agent·必要]` content collections frontmatter schema(`src/content/config.ts`)——「agent 能开始排版页面」的真正前置,比 token 还靠前(两份研究都漏了,评估补上)。

**P1 设计落地**
5. `[agent·必要]` `tokens.css` —— 单层 CSS 自定义属性(色/字阶/间距阶/圆角)。不做三层间接。
6. `[agent·必要]` 基础布局 + 各一级内容类型页面模板(原子→页面)。
7. `[agent·可选]` 模板稳定后在 CONVENTIONS.md 补 UI 约定。

**P2 自验证回路(⑥)**
8. `[agent·必要]` 视觉自检:build → 截图 375+1280 → 多模态自检(Playwright MCP)。
9. `[agent·必要]` a11y 自检:对构建产物跑 axe(Astro 默认零 JS,多数页面静态 HTML 即可查)。
10. `[agent·可选]` 一次性 `npx lighthouse` 跑首页,记 perf/SEO 基线,不固化、不进 CI。
11. `[agent·必要]` ⑦验收清单写进 `tasks.md`:human 只看预览 + 关键截图。

## 4. 明确砍掉的(别建)

- ❌ tokens 三层间接 + token-audit 漂移脚本(solo 首版无漂移规模)。
- ❌ 逐组件 `specs/` 文档 + 结构化 `design.md` 体系(与截图自检功能重叠)。
- ❌ Storybook / Chromatic / Percy 托管 VRT —— overkill,且与「GitHub Pages 无 preview 链路」决策(D-20260614-部署目标)直接冲突。
- ❌ 全站逐像素 VRT(静态站字体渲染差异易假报警)。
- ❌ Figma→代码 / design-to-code(无 Figma 源,与 Astro 手写取向不符)。
- ❌ moodboard 作为正式产物(降级为 human 口头给参考站)。
- ❌ 把验证套件塞进 ⑧ 部署 CI(全留本地 ⑥,保护冻结期发布链路)。

## 5. 评估 agent 的关键把关点(为什么这么砍)

- **Astro 特性盲区**:两份研究全程没提 Astro。默认零 JS / 岛屿架构让 a11y 可对 `dist/` 静态 HTML 直接跑,不必非走全浏览器驱动;真正卡脖子的前置是 content collections schema,而非 moodboard/token。
- **依赖纪律**:Playwright(重,带 Chromium 二进制 + CI 影响)、axe-core(轻但字面命中)合并为**一个** ②决策项一次拍板,不逐个临时 `npm i`;Playwright MCP(配置非依赖)、Lighthouse(`npx` 不固化)、token-audit(自写脚本)归 agent 自做。
- **与已定决策冲突**:托管 VRT 服务价值在 per-PR preview/baseline,与已定「不设 preview 链路」正面冲突,不是模糊的「以后再说」。
- **solo 偏重**:token 三层间接 + spec 文档体系是给多人/多主题规模造的解药,本项目首版没有那个规模问题。

## 6. 主要来源

业界流程 / 设计系统:
- https://bradfrost.com/blog/post/agentic-design-systems-in-2026/
- https://hvpandya.com/llm-design-systems
- https://wavespeed.ai/blog/posts/design-md-vs-design-tokens-ai-workflows/
- https://www.builder.io/blog/best-llms-for-coding

可视化验证闭环 / 工具:
- https://azukiazusa.dev/en/blog/playwright-cli-ai-agent-visual-feedback/
- https://egghead.io/ai-driven-design-workflow-playwright-mcp-screenshots-visual-diffs-and-cursor-rules~aulxx
- https://testdino.com/blog/playwright-ai-ecosystem
- https://luca-becker.me/blog/level-up-agentic-coding-mcp-2-playwright/
- https://www.deque.com/axe/axe-core/ · https://inclly.com/resources/axe-vs-lighthouse
- https://developer.chrome.com/docs/devtools/agents/use-cases/lighthouse-audit
- https://bug0.com/knowledge-base/visual-regression-testing-tools

前端模型对比(选型背景):
- https://benchlm.ai/best/frontend-app-dev
