# AGENTS.md

AI 编码 agent 的稳定入口,每次进项目先读。只放长期稳定的事实/约定/边界;当前任务的易变计划在执行层文件(见 Pointers),决策全文在 `DECISIONS.md`。CLAUDE.md 仅通过 import 引用本文件,所有指令以本文件为唯一事实源。

## 仓库现状(开工前必读)

- 这是一个 solo 个人博客。当前实现是 **Astro 自建静态站**,源码根为 `site/`,部署目标为 GitHub Pages,线上产物来自 `site/dist` 发布到 `gh-pages` 分支。
- 旧 Notion → Hugo 同步链路已废弃并从当前项目中移除。不要恢复 `.gitmodules`、`scripts/notion-sync.py`、根目录 `assets/`、`content/`、`themes/`、`resources/`、`public/` 这类旧站实现;旧内容如需参考,从 Git 历史恢复或人工挑选后走新的内容管线。
- 内容源长期方向是 agent 从 KB / draft / research / links / project notes 整理为显式 Markdown / manifest,再进入 `site/src/content`。统一入口见 `docs/content-pipeline/agent-publish.md` 和 `.agents/skills/blog-publisher/`。

## 开发流程(暂定)

```
①研究 → ②决策 → ③规划 → ④任务拆分 → ⑤实现 ⇄ ⑥自验证 → ⑦结果验收 → ⑧发布
```

| 阶段 | 负责 | 产出 |
|---|---|---|
| ①研究 | agent | `research.md` |
| ②决策 | **human** | `DECISIONS.md` 追加 `D-` 条 |
| ③规划 | agent 起草 / human 标注 | `plan.md` |
| ④任务拆分 | agent | `tasks.md`(每条带验收标准) |
| ⑤实现 | agent | 代码;每完成一条在 `tasks.md` 勾选 |
| ⑥自验证 | agent | build / 类型 / 链接 / 截图 自检 |
| ⑦结果验收 | **human** | 看预览 |
| ⑧发布 | agent | 仅 ⑦ 通过后切换上线 |

- **human 只在 ②决策、⑦验收 两处**;其余 agent 自闭环,不要为进度中途停下来问。**验证是 agent 的职责**,human 不做验证,只做 ⑦ 最终结果验收。
- ⑤⇄⑥ 是实现与自验证的内循环。自验证失败 → 回退到上一个干净点重做(未提交用 `git restore`,已提交用 `git revert`),**不在错误实现上层层打补丁**。
- 文件路径:`research.md` / `plan.md` / `tasks.md` 放仓库根;完成后归档到 `docs/archive/<日期>-<主题>/`。执行层内容不要写进本文件。

## 边界

- ✅ 总是:实现前检查真实文件和当前状态;实现后自己跑验证再宣称完成;内容发布类任务走 `blog-publisher` / review / manifest / `content:check` / `content:sync`。
- ⚠️ 先问(命中即停,**优先级高于「不中途问」**;属安全确认,不算流程门):任何 ②决策类选择(技术栈 / 内容源 / 部署);新增依赖;删除文件。
- 🚫 禁止:
  - 把 secrets 写入仓库或提交 → 改用环境变量 / 本地未跟踪文件。(此规则后续应由 pre-commit hook 强制,散文仅作兜底。)
  - 恢复旧 Notion/Hugo 自动同步或旧站部署链路。
  - 未经明确请求就发布 / 推送生产变更。日常内容和 UI 改动可本地验证;push/deploy 需要用户明确要求或当前任务已包含发布。
  - 把执行层 todo / 当前任务计划塞进本文件 → 放 `tasks.md` / `plan.md`。
  - UI 验证套件(Playwright 截图 / axe / Lighthouse)塞进 ⑧ 部署 CI → 只在本地 ⑥自验证 跑,保护冻结期发布链路(详见 `CONVENTIONS.md` 的「UI 自验证回路」、`DECISIONS.md` 的 `D-20260614-UI验证工具链`)。

## Pointers

- `plan.md` / `tasks.md`:当前重建任务的执行层文件(可能尚未创建;到 ③④ 阶段由 agent 建)。
- `DECISIONS.md`:决策日志全文 + `D-` 格式定义。本文件不复制其内容。
- `CONVENTIONS.md`:开发与协作规范(git 工作流、多 agent worktree、UI 自验证回路)。对应流程 ⑤实现 / ⑥自验证 / ⑧发布。
- `research.md`:UI 工作流的 ①研究产出(业界方案 + 评估,完成后归档 `docs/archive/`)。
- `docs/content-pipeline/agent-publish.md` / `.agents/skills/blog-publisher/`:统一 agent 内容发布入口;所有 KB/draft/research/link/project 内容先过质量门检和 review loop,再 sync/build/preview。
- `docs/deployment.md`:当前 CI/CD、部署边界和旧 Notion/Hugo 废弃说明。
- 构建:`pnpm --dir site build`;机械检查:`pnpm ci:sanity`;本地 UI 自验证:`pnpm ui-verify -- --serve out/ui-serve --path /my-blog/`;部署由 `.github/workflows/deploy.yml` 发布 `site/dist` 到 `gh-pages`。
