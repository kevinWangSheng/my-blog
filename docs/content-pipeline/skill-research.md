# C02 — `kb-to-blog` / `blog-publisher` skill 调研与能力方案

> 状态: C02 已完成设计。本文记录 skill 市场查询、候选评估、不适配原因,以及本项目后续应实现的可复用发布能力。  
> 日期: 2026-06-14。  
> 输入: `docs/content-pipeline/candidates.md`, `site/scripts/content-check.mjs`, `site/scripts/content-sync.mjs`, `tasks.md` C02。

## 目标边界

目标不是“把 KB 自动同步到 blog”,而是建立一个可复用的**内容处理 skill**:把 KB 候选材料转成面向陌生读者的 blog 草稿、review-ready 审稿件和公开风险清单。`content:check` / `content:sync` 是 human 批准后的下游机械闸门,不是这个 skill 的核心。

能力必须覆盖:

1. 从候选池选择素材,保留 source path 和主题簇。
2. 生成 review 文件,明确公开化目标、质量 rubric、事实核验点和风险。
3. 按 essay / note / log / link / project 的不同形态改写内容,避免 KB 原文搬运。
4. 只有 human 审核通过后,才进入 manifest、`content:check`、`content:sync`。
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

结论: curated 列表里没有一个 skill 直接覆盖本任务真正需要的核心: **从本地 KB 取材,按个人 blog 定位做公开化改写,保留 source tracing,检查隐私/伪造成果/事实 freshness,生成 review-ready 草稿并等待 human gate**。Notion 类 skill 是外部工作区采集/文档化,Playwright 类 skill 是页面验证,security 类 skill 是安全专项;它们都不是 KB→blog 内容处理 skill。

### 官方 experimental skills

查询命令:

```bash
python3 /Users/shenghuikevin/.codex/skills/.system/skill-installer/scripts/list-skills.py --path skills/.experimental --format json
```

结果: 官方路径返回 `Skills path not found: https://github.com/openai/skills/tree/main/skills/.experimental`。因此本轮没有可查询的 experimental 候选。

### 本机已安装 / 项目已有能力

| skill / tool | 结论 | 可复用点 | 边界 |
|---|---|---|---|
| `kb` skill | 必须结合,但不单独承担发布 | 负责读/查/维护 llm-kb vault,辅助 source discovery、source tracing、vault lint/audit | 它不做公开写作判断和 blog 成品改写;应作为 `kb-to-blog` 的上游材料能力。 |
| `ui-verify` project skill | 下游复用 | 内容进入站点后验证页面/a11y/Lighthouse | 不参与 KB 内容改写;不是 C02 研究重点。 |
| `site/scripts/content-check.mjs` | 下游硬 gate | 检查 frontmatter、slug、发布意图、secrets/private markers、正文空值等 | 只能验证结构和基础风险;不能替代内容 skill 的编辑判断。 |
| `site/scripts/content-sync.mjs` | 下游写入入口 | approved + check 通过后把 Markdown 写入内容目录 | 不是内容处理能力;必须在 human approve 后才能调用。 |
| `docs/content-pipeline/candidates.md` | 复用 | C01 候选池,提供初始 priority 和风险标签 | 不是批准列表。 |

## 决策

不安装现有市场 skill。自建项目级 **`kb-to-blog`** skill,并把它定义为内容处理能力: **source discovery / source tracing 结合 `kb` skill,公开化改写由 `kb-to-blog` 负责,写入与验证由 `content-check` / `content-sync` / `ui-verify` 在下游负责**。

已创建 Codex 项目级 skill: `.agents/skills/kb-to-blog/`。后续如需 Claude Code 同步,可在 C03/C04 追加 `.claude/skills/kb-to-blog/` wrapper 或 import,但本轮先把 Codex 执行入口打通。

## `kb-to-blog` 能力契约

### 触发条件

使用于以下请求:

- “从 KB 里找几篇能发 blog 的内容”。
- “把这个 KB/output/wiki 文件整理成 blog 草稿”。
- “生成 blog 内容 review-ready 草稿”。
- “把 approved 的 review 准备成 manifest / sync 输入”。

不使用于:

- 未经审核直接发布内容。
- 推送、部署、cutover。
- 把本地/private 项目伪装成公开成果。
- 安全攻防细节的未经审查公开。

### 输入

至少一种:

- 候选表条目: `docs/content-pipeline/candidates.md` 中的 source path。
- 明确 KB source path。
- 已 human-approved 的 review 文件。
- 已批准的 manifest。

### 输出

按阶段输出不同文件:

1. Discovery / selection: 更新候选表或生成候选摘要。
2. Review-ready: `docs/content-pipeline/reviews/<slug>.md`。
3. Approved manifest: `docs/content-pipeline/manifests/<slug>.json`。
4. Approved manifest: `docs/content-pipeline/manifests/<slug>.json`。
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
- Human review checklist。
- Approval status: `draft` / `needs-human-review` / `approved` / `rejected`。

### Stage 4 — Human gate

除非 review 文件明确标记 `approved` 且有 human 批准记录,不得生成可执行 manifest 或调用 `content:sync`。

推荐 human approval 最小格式:

```yaml
approval:
  status: approved
  reviewer: human
  date: YYYY-MM-DD
  notes: "..."
```

### Stage 5 — Generate manifest

只对 approved review 生成 `docs/content-pipeline/manifests/<slug>.json`。manifest 必须显式表达发布意图,例如:

```json
{
  "items": [
    {
      "type": "essays",
      "file": "docs/content-pipeline/reviews/<slug>.md",
      "slug": "<slug>",
      "publish": true,
      "sourceType": "existing-material-summary"
    }
  ]
}
```

实际字段必须以 `site/scripts/content-check.mjs` 支持为准。

### Stage 6 — Check / sync

1. 运行 content check。
2. 仅 check 通过后运行 sync。
3. 运行 `pnpm --dir site build`。
4. 如果影响 UI / 详情页阅读,运行 `pnpm ui-verify -- --serve site/dist --path /` 以及至少一个长文详情路径。

### Stage 7 — Adversarial review

主 agent 验证通过后,spawn 独立 subagent 做对抗检查。它必须检查:

- 内容是否像公开成品,不是 KB 原文搬运。
- 是否有隐私、secret、forbidden/private marker。
- 是否伪造经历、项目成果、外部背书或公开链接。
- 事实是否需要但尚未刷新。
- 站内 route / RSS / links 是否成立。

## 质量 rubric

每项 0-2 分,低于 8/12 不应进入 human approval:

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

## Human review

```yaml
approval:
  status: needs-human-review
  reviewer:
  date:
  notes:
```

## Agent verification notes
```

## Subagent prompt template

```text
你是独立对抗性审查 agent。请只审查以下 review 草稿和对应 KB source 摘要,不要发布、不要 sync、不要修改旧站部署链路。

目标:判断这篇内容是否可以进入 human review / approved manifest 前一步。

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
- 是否建议进入 human review: yes/no
```

## C02 验收结论

- 已查询官方 curated skills,记录相关候选与不适配原因。
- 官方 experimental 路径不可用,已记录错误。
- 已评估本机 `kb` skill、项目 `ui-verify`、`content-check`、`content-sync` 的复用边界: `kb` 做上游材料能力,`kb-to-blog` 做内容处理,同步和 UI 验证是下游。
- 未安装市场 skill,因为没有现成能力覆盖“本地 KB → 公开 blog 成品改写 → review-ready → human gate”。
- 已按 skill-creator 原则创建项目级 `.agents/skills/kb-to-blog/`,并定义触发条件、边界、输入/输出契约、阶段流程、质量 rubric、安全检查、human review gate、manifest/content:check/sync 接入、subagent 对抗审查模板。
