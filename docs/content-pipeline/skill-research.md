# C02 — `kb-to-blog` / `blog-publisher` skill 调研与能力方案

> 状态: C02 已完成设计。本文记录 skill 市场查询、候选评估、不适配原因,以及本项目后续应实现的可复用发布能力。  
> 日期: 2026-06-14。  
> 输入: `docs/content-pipeline/candidates.md`, `site/scripts/content-check.mjs`, `site/scripts/content-sync.mjs`, `tasks.md` C02。

## 目标边界

目标不是“把 KB 自动同步到 blog”,而是建立一个可复用的**内容处理 skill**:把 KB 候选材料转成面向陌生读者的 blog 草稿、review-ready 审稿件和公开风险清单。`content:check` / `content:sync` 是 agent 自检通过后的下游机械闸门,不是这个 skill 的核心。human review 放在最后看实际 blog 效果。

能力必须覆盖:

1. 从候选池选择素材,保留 source path 和主题簇。
2. 生成 review 文件,明确公开化目标、质量 rubric、事实核验点和风险。
3. 按 essay / note / log / link / project 的不同形态改写内容,避免 KB 原文搬运。
4. agent 自检和对抗审查无阻塞后,进入 manifest、`content:check`、`content:sync`;human 最后看实际 blog 效果。
5. 让独立 subagent 对内容质量、隐私、伪造成果、事实刷新和 blog fit 做对抗审查。

## 市场 / 已有 skill 查询记录

### 官方 curated skills

查询命令:

```bash
python3 /Users/shenghuikevin/.codex/skills/.system/skill-installer/scripts/list-skills.py --format json
```

结果: 成功返回 39 个 curated skills。相关候选:

| skill | 结论 | 不适配原因 / 可复用点 |
|---|---|---|
| `notion-knowledge-capture` | 不安装 | 偏 Notion 捕获,不是本地 KB → blog 发布管线;无法覆盖 review-ready / manifest / content:check。 |
| `notion-research-documentation` | 不安装 | 偏 Notion research/documentation 工作流;可借鉴“研究材料结构化”思路,但目标存储与审核边界不同。 |
| `notion-spec-to-implementation` | 不安装 | 从 Notion spec 到实现,不处理 KB 内容策展与公开风险。 |
| `security-best-practices` | 不安装 | 可作为未来安全审查参考,但不能替代内容发布 skill;本任务只需隐私/secrets/伪造成果检查。 |
| `security-threat-model` | 不安装 | 适合系统威胁建模,过重;不直接解决内容发布流程。 |
| `openai-docs` | 不安装 | 与 OpenAI 官方 API 文档相关,仅在需要刷新 OpenAI 事实时临时使用。 |
| `transcribe` | 不安装 | 视频/音频转写能力,可供某些 source refresh 使用,但不是发布管线。 |
| `playwright` / `screenshot` | 非核心,不安装 | 只与发布后页面验证有关;不是 KB→blog 内容处理 skill。项目已有 `ui-verify` 覆盖这类验证。 |

结论: curated 列表里没有一个 skill 直接覆盖本任务真正需要的核心: **从本地 KB 取材,按个人 blog 定位做公开化改写,保留 source tracing,检查隐私/伪造成果/事实 freshness,生成 review-ready 草稿并通过 agent self-review 后进入 blog 成品阶段**。Notion 类 skill 是外部工作区采集/文档化,Playwright 类 skill 是页面验证,security 类 skill 是安全专项;它们都不是 KB→blog 内容处理 skill。

### 官方 experimental skills

查询命令:

```bash
python3 /Users/shenghuikevin/.codex/skills/.system/skill-installer/scripts/list-skills.py --path skills/.experimental --format json
```

结果: 官方路径返回 `Skills path not found: https://github.com/openai/skills/tree/main/skills/.experimental`。因此本轮没有可查询的 experimental 候选。

### 本机已安装 / 项目已有能力

| skill / tool | 结论 | 可复用点 | 边界 |
|---|---|---|---|
| `kb` skill | 可选辅助,不是主上游 | 适合 llm-kb CLI 相关读/查/维护 | 当前候选来自 `/Users/shenghuikevin/kb-vault`,不是 llm-kb canonical repo;不要让后续 agent 误以为必须通过 `kb` skill 才能读候选。 |
| `ui-verify` project skill | 下游复用 | 内容进入站点后验证页面/a11y/Lighthouse | 不参与 KB 内容改写;不是 C02 研究重点。 |
| `site/scripts/content-check.mjs` | 下游硬 gate | 检查 frontmatter、slug、发布意图、secrets/private markers、正文空值等 | 只能验证结构和基础风险;不能替代内容 skill 的编辑判断。 |
| `site/scripts/content-sync.mjs` | 下游写入入口 | agent-cleared + check 通过后把 Markdown 写入内容目录 | 不是内容处理能力;不再要求 sync 前 human review,但必须先有 agent self-review。 |
| `docs/content-pipeline/candidates.md` | 复用 | C01 候选池,提供初始 priority 和风险标签 | 不是批准列表。 |


## 内容处理视角复查结论

用户复核后明确:本能力应主要服务 **KB 内容 → blog 内容** 的转换,而不是同步、部署或页面验证。重新按这个角度检查后,结论如下:

1. **现有 `kb` skill 只能可选辅助,不能当作唯一上游**。`kb-to-blog` 的实际取材根是 `/Users/shenghuikevin/kb-vault`;现有 `kb` skill 的 canonical source 是 `/Users/shenghuikevin/dev/AI/llm-kb`,两者不是同一个库。后续 agent 应优先按候选表和文件系统读取 `kb-vault`;只有任务明确涉及 llm-kb CLI 维护/查询时才调用 `kb` skill。
2. **需要自写 `kb-to-blog` 内容转化 skill**。它负责判断材料是否适合公开、决定 essay/note/log/link/project 形态、把 KB 笔记改写成面向陌生读者的 blog 草稿、做 source tracing/freshness/privacy/no-fabrication 检查,并生成 review-ready 文件。agent 自检通过后还必须生成单独的 publishable Markdown,不能把 review 文件当作 sync 输入。human 最后看 blog 成品。
3. **`content-check` / `content-sync` 是下游机械入口**。它们在 agent 自检通过后执行,负责结构校验和写入,不能替代内容判断。真实命令只接受 `--file ... --type ...` 或 `--input <dir>`,manifest 模式固定读取 `<dir>/manifest.json`。
4. **Notion curated skills 不适配**。`notion-knowledge-capture` 是把对话/笔记写入 Notion wiki;`notion-research-documentation` 是从 Notion sources 生成 briefs/reports;`notion-spec-to-implementation` 是 spec 到任务计划。它们的思想可借鉴,但依赖 Notion MCP 和 Notion database schema,不适合本项目的本地 KB + Astro blog 内容流。
5. **Playwright / screenshot / ui-verify 不属于此 skill 核心**。它们只在内容进入站点后验证页面可读性/a11y/路由,不是 KB 内容处理能力。

因此最终方案是 **组合式但以自写为主**: 项目级 `kb-to-blog` skill 负责内容转化;候选表和 `kb-vault` 文件系统是主要上游;现有 `kb` skill 只在需要 llm-kb CLI 能力时辅助;下游 `content-check/sync` 负责机械校验和写入。这比安装一个现成 Notion 或研究文档 skill 更贴合当前仓库和内容边界。

## 决策

不安装现有市场 skill。自建项目级 **`kb-to-blog`** skill,并把它定义为内容处理能力: **source discovery / source tracing 主要基于 `docs/content-pipeline/candidates.md` 和 `/Users/shenghuikevin/kb-vault`;现有 `kb` skill 仅作可选辅助;公开化改写由 `kb-to-blog` 负责;agent 自检通过后生成 publishable Markdown + manifest;写入与验证由 `content-check` / `content-sync` / `ui-verify` 在下游负责**。

已创建 Codex 项目级 skill: `.agents/skills/kb-to-blog/`。后续如需 Claude Code 同步,可在 C03/C04 追加 `.claude/skills/kb-to-blog/` wrapper 或 import,但本轮先把 Codex 执行入口打通。

## `kb-to-blog` 能力契约

### 触发条件

使用于以下请求:

- “从 KB 里找几篇能发 blog 的内容”。
- “把这个 KB/output/wiki 文件整理成 blog 草稿”。
- “生成 blog 内容 review-ready 草稿”。
- “把 agent-cleared 的 review 准备成 publishable Markdown / manifest / sync 输入”。

不使用于:

- 未经审核直接发布内容。
- 推送、部署、cutover。
- 把本地/private 项目伪装成公开成果。
- 安全攻防细节的未经审查公开。

### 输入

至少一种:

- 候选表条目: `docs/content-pipeline/candidates.md` 中的 source path。
- 明确 KB source path。
- 已 agent-cleared 的 review 文件。
- 已 agent-cleared 的 manifest。

### 输出

按阶段输出不同文件:

1. Discovery / selection: 更新候选表或生成候选摘要。
2. Review-ready: `docs/content-pipeline/reviews/<slug>.md`。
3. Agent-cleared publishable Markdown: `docs/content-pipeline/manifests/<slug>/<slug>.md`。
4. Agent-cleared manifest directory: `docs/content-pipeline/manifests/<slug>/manifest.json`。
5. 下游验证证据: `content:check` / `content:sync` / build / route / UI verify 输出摘要。

## 阶段流程

### Stage 1 — Select

1. 读取 `docs/content-pipeline/candidates.md`。
2. 选择 `candidate` 或 `needs-rewrite` 条目;`source-only` 只能作为辅助来源。
3. 明确目标 collection: `essays` / `notes` / `logs` / `links` / `projects`。
4. 检查是否需要 source refresh;fast-moving / security / benchmark / vendor claims 默认需要刷新官方或 primary sources。

### Stage 2 — Transform the KB material into blog-shaped content

这是本 skill 的核心,不是同步。处理要求:

- 为陌生读者补上下文:为什么值得读、读完能做什么判断。
- 把 KB/学习材料改写成公开语气,移除 mentor/课程化/内部 run log 痕迹。
- 按目标类型改写:essay 要有论点和结构;note 要有单点判断;log 要标明时间与未定性;link 要突出外部来源价值;project 只展示真实可公开证据。
- 保留 source path 在 review metadata,不要把本地路径写进公开正文。
- 对模型/厂商/协议/benchmark/security 等快变事实标记需要刷新,必要时查 official/primary source。

### Stage 3 — Draft review file

生成 `docs/content-pipeline/reviews/<slug>.md`,必须包含:

- Source paths。
- Proposed collection / slug / title。
- Source type: `sample` / `existing-material-summary` / `public-original` / `source-only-derived`。
- Public framing: 这篇对陌生读者是什么。
- Rewrite plan: 保留什么、删除什么、补什么。
- Fact-refresh checklist。
- Privacy / secret / forbidden marker checklist。
- No-fabrication checklist: 不伪造经历、成果、外部背书、公开 repo/demo。
- Quality rubric score。
- Agent review checklist。
- Status: `draft` / `agent-cleared` / `synced` / `published` / `needs-rework` / `rejected`。

### Stage 4 — Agent self-review gate

除非 review 文件已完成 agent 自检并标记 `agent-cleared`,不得生成 publishable Markdown、可执行 manifest 或调用 `content:sync`。human review 不再卡在这里,而是在最终 blog/result 阶段进行。

推荐 agent review 最小格式:

```yaml
agent_review:
  status: agent-cleared
  reviewer: agent
  date: YYYY-MM-DD
  notes: "..."
```

### Stage 5 — Generate publishable Markdown and manifest

只对 agent-cleared review 生成独立 staging 目录:

```text
docs/content-pipeline/manifests/<slug>/
  manifest.json
  <slug>.md
```

`<slug>.md` 是真正可发布文章,必须包含目标 collection 的合法 frontmatter 和正文;review 文件不能作为 sync 输入。manifest 必须命名为 `manifest.json`,且 `file` 只能写相对 staging 目录内的文件名,不能写 `../` 或 `docs/...` 路径,例如:

```json
{
  "items": [
    {
      "type": "essays",
      "file": "<slug>.md",
      "slug": "<slug>",
      "publish": true,
      "visibility": "public"
    }
  ]
}
```

实际必填 frontmatter 以 `site/scripts/content-shared.mjs` 的 `REQUIRED` 与 `site/src/content.config.ts` 为准。

### Stage 6 — Check / sync

1. 运行 `pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>`。
2. 仅 check 通过后运行 `pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>`。
3. 运行 `pnpm --dir site build`。
4. 如果影响 UI / 详情页阅读,运行 `pnpm ui-verify -- --serve site/dist --path /` 以及至少一个长文详情路径。

脚本只解析 `--key value` 参数;不要传裸位置参数。

### Stage 7 — Adversarial review

主 agent 验证通过后,spawn 独立 subagent 做对抗检查。它必须检查:

- 内容是否像公开成品,不是 KB 原文搬运。
- 是否有隐私、secret、forbidden/private marker。
- 是否伪造经历、项目成果、外部背书或公开链接。
- 事实是否需要但尚未刷新。
- 站内 route / RSS / links 是否成立。

## 质量 rubric

每项 0-2 分,低于 8/12 不应同步给最终 blog review:

| item | 0 | 1 | 2 |
|---|---|---|---|
| Public value | 只有内部记录 | 有主题但读者收益模糊 | 陌生读者能明确获得判断/方法/地图 |
| Source grounding | 来源不清 | 有来源但未校准 | source path 清楚,关键事实可追溯 |
| Rewrite maturity | 原文搬运 | 局部改写 | 公开口吻、结构、标题、上下文完整 |
| Safety/privacy | 有明显风险 | 风险待查 | 无 secrets/private/forbidden/伪造成果 |
| Freshness | 过时或未标注 | 部分需刷新 | 快变事实已刷新或明确标注时间 |
| Blog fit | 与站点定位弱 | 勉强相关 | 明确服务 AI 学习/agent 系统/项目实践 |

## Review 模板

后续 C03 可把此模板落成独立文件;当前先固定内容契约。

```markdown
# Review: <title>

## Metadata

- status: draft
- source paths:
  - /Users/shenghuikevin/kb-vault/...
- proposed collection: essays|notes|logs|links|projects
- proposed slug:
- source type: existing-material-summary|public-original|source-only-derived|sample
- target reader:

## Public framing

## Rewrite plan

### Keep

### Remove / anonymize

### Add / refresh

## Fact refresh checklist

- [ ] Fast-moving vendor/model/protocol claims checked against official/primary source.
- [ ] Benchmark/metric claims refreshed or removed.
- [ ] Security claims phrased defensively and without operational attack detail.

## Safety checklist

- [ ] No secrets/tokens/keys.
- [ ] No private marker / forbidden publish marker.
- [ ] No private person/company data.
- [ ] No fabricated project result, customer/user feedback, repo/demo, or external endorsement.
- [ ] Hypothetical cases are labeled as hypothetical.

## Quality rubric

| item | score | note |
|---|---:|---|
| Public value |  |  |
| Source grounding |  |  |
| Rewrite maturity |  |  |
| Safety/privacy |  |  |
| Freshness |  |  |
| Blog fit |  |  |

Total: /12

## Agent review

```yaml
agent_review:
  status: draft
  reviewer: agent
  date:
  notes:
```

## Final human blog review

Human review happens after the content is visible in the blog preview or published site. If there are issues, open a follow-up返工 session rather than blocking manifest/sync here.

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Agent verification notes
```

## Subagent prompt template

```text
你是独立对抗性审查 agent。请只审查以下 review 草稿和对应 KB source 摘要,不要发布、不要 sync、不要修改旧站部署链路。

目标:判断这篇内容是否可以进入 publishable Markdown / manifest / sync 阶段。

必须检查:
1. 是否是公开成品方向,还是 KB 原文搬运。
2. 是否存在 secrets/private/forbidden publish/个人隐私/内部路径暴露风险。
3. 是否伪造经历、项目成果、外部背书或公开链接。
4. 是否有快变事实、benchmark、厂商能力、安全建议需要刷新。
5. 是否符合 blog 定位:AI 学习、agent 系统、项目实践、知识工作流。

输出:
- 阻塞项:
- 非阻塞风险:
- 建议改写:
- 是否建议进入 sync 后的最终 blog review: yes/no
```

## C02 验收结论

- 已查询官方 curated skills,记录相关候选与不适配原因。
- 官方 experimental 路径不可用,已记录错误。
- 已评估本机 `kb` skill、项目 `ui-verify`、`content-check`、`content-sync` 的复用边界: 候选表和 `kb-vault` 文件系统是主上游,`kb` 仅作可选辅助,`kb-to-blog` 做内容处理,同步和 UI 验证是下游。
- 未安装市场 skill,因为没有现成能力覆盖“本地 KB → 公开 blog 成品改写 → agent self-review → blog final review”。
- 已按 skill-creator 原则创建项目级 `.agents/skills/kb-to-blog/`,并定义触发条件、边界、输入/输出契约、阶段流程、质量 rubric、安全检查、agent self-review、final human blog review、publishable Markdown 与 manifest 真实脚本契约、content:check/sync 接入、subagent 对抗审查模板。
