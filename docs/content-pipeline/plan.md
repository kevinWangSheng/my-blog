# 内容系统与 KB 发布管线规划

## 目标

把 `/Users/shenghuikevin/kb-vault` 里的 output / wiki / learning 材料,经过策展、改写、质量评估和 human 审核后,发布为 blog 中真正可公开的成品内容。Blog 不直接展示 KB 原始材料,也不展示 demo / toy 内容。

## 核心原则

- Blog 中公开的内容必须是成品或足够成熟的公开稿,不是 KB 原始摘录、调研中间态或 agent 草稿。
- KB 是素材库和证据库;blog 是公开表达层。二者之间必须有中间发布状态。
- 本地项目如果没有足够公开证据,可以不展示;Projects 允许暂时留空或只保留明确标注的非公开占位,不能伪造成熟成果。
- 内容优先质量和体系,不追求数量。每个主题簇应形成主 essay + notes + logs + links 的阅读路径。
- 后续可以接入 coding agent 定时任务,但自动发布必须经过内容质量门、安全检查和可回滚流程。

## 建议主题簇

第一批优先从已有 KB 中整理 3 个主题簇:

1. RAG / Context Engineering
   - 候选: `kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md`
   - 形态:主 essay + 若干 notes + links
2. Context Engineering / Agent Memory
   - 候选: `kb-vault/output/2026-05-23-context-engineering-in-2026-three-source-synthesis.md`, `wiki/agent-memory/*`
   - 形态:主 essay + 概念 notes + 学习 log
3. Agent Systems / Agent Field
   - 候选: `kb-vault/learning/agent-field/*`, `wiki/agent-field/*`
   - 形态:体系 notes + 阶段 logs + 少量成熟 essay

## 中间发布状态

建议新增 repo 内中间目录,不直接等同最终内容目录:

```text
docs/content-pipeline/
  plan.md                     # 本文件:长期规划
  candidates.md               # KB 候选池盘点
  reviews/                    # 每轮候选评估与 human review 记录
  manifests/                  # 通过审核后的 content:sync manifest
```

候选状态建议:

- `discovered`: 从 KB 扫到,未评估。
- `candidate`: 值得进入发布评估。
- `needs-rewrite`: 有价值但需要重写结构/口吻/来源。
- `review-ready`: 已整理成可审稿件,等待 human 审核。
- `approved`: human 通过,可进入 `content:check` / `content:sync`。
- `published`: 已进入 `site/src/content` 并通过 build / RSS / link / UI 验证。
- `rejected`: 不适合公开或质量不足。

## 工具 / skill 方向

先查 skill 市场和已有能力,再决定是否自建。顺序是:

1. 使用 `skill-installer` 查询官方 curated / 可用市场 skill。
2. 评估候选是否能覆盖内容策展、发布前审核、subagent 分工、质量检查、安全检查、blog manifest 生成。
3. 如果存在合适 skill,优先安装/复用,本项目只补 wrapper / SOP。
4. 如果没有合适 skill,再按 `skill-creator` 规范设计一个真正可用的 `kb-to-blog` 或 `blog-publisher` skill,而不是临时脚本。

无论复用还是自建,最终能力的职责都是:

1. 用多个 subagent 对 KB 进行分区搜索和候选评估。
2. 汇总候选池,按主题簇、成熟度、来源质量和公开风险排序。
3. 为每个候选推荐 blog 类型: essay / note / log / link / project。
4. 生成中间 review 文件,明确为什么值得发布、需要改写什么、有哪些来源和风险。
5. human 审核通过后,生成 `content:sync` manifest 和 Markdown 草稿。
6. 调用现有 `site/scripts/content-check.mjs` / `content-sync.mjs`。
7. 发布后跑 build / RSS / route / UI 基础验证。
8. 最后由独立 subagent 做对抗性审查:质量、体系、重复、隐私、伪造成果、链接和阅读路径。

Skill 不能只是 toy。若新建 skill,必须先遵守 `skill-creator` 的设计规范,并包含:

- 清楚触发条件和边界。
- 输入/输出契约。
- subagent 分工模板。
- 质量 rubric。
- 安全/隐私检查。
- 验证命令。
- 示例候选和示例 review 输出。

## 文章详情推荐

内容体系建立前,站点应先支持轻量推荐:

- 同 `series` 的上一篇 / 下一篇。
- 同 tags 的 related essays / notes。
- Project 详情推荐相关 logs / notes。
- Essay 详情推荐相关 notes / links。

第一版不需要复杂推荐算法,但要让读者从一篇文章进入同一主题簇。

## 自动发布边界

未来 coding agent 定时任务可以做:

1. 扫描 KB 新 output / wiki 更新。
2. 生成候选 review。
3. 对成熟候选生成草稿和 manifest。
4. 跑 content check。
5. 生成 PR 或本地提交。

但不建议直接无审核发布到线上。默认策略应是:自动生成候选与草稿,hard gate 留给 human 或明确批准规则。
