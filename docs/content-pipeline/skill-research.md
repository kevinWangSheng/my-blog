# C02 — `kb-to-blog` / `blog-publisher` skill 调研与能力方案

> 状态: C02 已完成设计。本文记录 skill 市场查询、候选评估、不适配原因,以及本项目后续应实现的可复用发布能力。  
> 日期: 2026-06-14。  
> 输入: `docs/content-pipeline/candidates.md`, `site/scripts/content-check.mjs`, `site/scripts/content-sync.mjs`, `tasks.md` C02。

## 目标边界

目标不是“把 KB 自动发布到 blog”,而是建立一个可复用能力,把 KB 候选材料转成 **review-ready 草稿 + manifest + 验证证据**。真正进入 `site/src/content` 之前仍保留 human review gate。

能力必须覆盖:

1. 从候选池选择素材,保留 source path 和主题簇。
2. 生成 review 文件,明确公开化目标、质量 rubric、事实核验点和风险。
3. 只有 human 审核通过后,才生成 manifest 并调用 `content:check` / `content:sync`。
4. 发布后运行 build / RSS / route / UI 基础验证。
5. 让独立 subagent 对质量、隐私、伪造成果、链接和阅读路径做对抗审查。

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
| `playwright` / `screenshot` | 不安装 | 项目已有 `ui-verify` skill + 脚本;无需重复。 |

结论: curated 列表里没有一个 skill 同时覆盖 **KB 候选策展、公开风险审查、human review gate、blog manifest、content:check/sync、发布后验证**。不安装新 curated skill。

### 官方 experimental skills

查询命令:

```bash
python3 /Users/shenghuikevin/.codex/skills/.system/skill-installer/scripts/list-skills.py --path skills/.experimental --format json
```

结果: 官方路径返回 `Skills path not found: https://github.com/openai/skills/tree/main/skills/.experimental`。因此本轮没有可查询的 experimental 候选。

### 本机已安装 / 项目已有能力

| skill / tool | 结论 | 可复用点 | 边界 |
|---|---|---|---|
| `kb` skill | 部分复用 | 适合读 / 维护 llm-kb vault,可辅助 source discovery、vault lint/audit | skill 自身边界明确“不做长期治理或 publishing judge”;不能作为 blog publisher。 |
| `ui-verify` project skill | 复用 | 发布后本地 UI/a11y/Lighthouse 验证 | 不判断文章质量和公开风险。 |
| `site/scripts/content-check.mjs` | 复用为硬 gate | 检查 frontmatter、slug、发布意图、secrets/private markers、正文空值等 | 只检查结构与基础风险,不保证公开表达质量。 |
| `site/scripts/content-sync.mjs` | 复用为写入入口 | 通过 check 后将 Markdown 规范化写入内容目录 | 必须在 human approve 后才能调用。 |
| `docs/content-pipeline/candidates.md` | 复用 | C01 候选池,提供初始 priority 和风险标签 | 不是批准列表。 |

## 决策

不安装现有市场 skill。下一步应自建设计一个项目级 wrapper / skill,暂名 **`kb-to-blog`**。它不是“一键发布器”,而是“候选 → 审稿件 → human gate → manifest → sync → 验证”的可复用 SOP。

如果未来要做成真正 Codex skill,建议放在项目级 `.agents/skills/kb-to-blog/`,并同步给 Claude Code 的 `.claude/skills/kb-to-blog/` 或保留一个 wrapper import。C02 本轮先固定设计与模板,不急着创建 executable skill,避免在流程稳定前把一次性判断固化。

## `kb-to-blog` 能力契约

### 触发条件

使用于以下请求:

- “从 KB 里找几篇能发 blog 的内容”。
- “把这个 KB/output/wiki 文件整理成 blog 草稿”。
- “生成 blog 发布 review / manifest”。
- “把 approved 的 review 同步到 `site/src/content`”。

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
4. Published content: `site/src/content/<collection>/<slug>.md`。
5. Verification evidence: 命令输出摘要、RSS/route 检查、必要时 `out/summary.json`。

## 阶段流程

### Stage 1 — Select

1. 读取 `docs/content-pipeline/candidates.md`。
2. 选择 `candidate` 或 `needs-rewrite` 条目;`source-only` 只能作为辅助来源。
3. 明确目标 collection: `essays` / `notes` / `logs` / `links` / `projects`。
4. 检查是否需要 source refresh;fast-moving / security / benchmark / vendor claims 默认需要刷新官方或 primary sources。

### Stage 2 — Draft review file

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

### Stage 3 — Human gate

除非 review 文件明确标记 `approved` 且有 human 批准记录,不得生成可执行 manifest 或调用 `content:sync`。

推荐 human approval 最小格式:

```yaml
approval:
  status: approved
  reviewer: human
  date: YYYY-MM-DD
  notes: "..."
```

### Stage 4 — Generate manifest

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

### Stage 5 — Check / sync

1. 运行 content check。
2. 仅 check 通过后运行 sync。
3. 运行 `pnpm --dir site build`。
4. 如果影响 UI / 详情页阅读,运行 `pnpm ui-verify -- --serve site/dist --path /` 以及至少一个长文详情路径。

### Stage 6 — Adversarial review

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
- 已评估本机 `kb` skill、项目 `ui-verify`、`content-check`、`content-sync` 的复用边界。
- 未安装新 skill,因为没有现成能力完整覆盖本项目发布管线。
- 已按 skill-creator 原则设计 `kb-to-blog` 能力:触发条件、边界、输入/输出契约、阶段流程、质量 rubric、安全检查、human review gate、manifest/content:check/sync 接入、subagent 对抗审查模板。
