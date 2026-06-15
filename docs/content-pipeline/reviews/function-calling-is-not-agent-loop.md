# Review: Function calling 是能力，agent loop 是授权

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/learning/agent-field/takes/agent-loop-vs-code-loop.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/workflow-vs-agent.md
- proposed collection: notes
- proposed slug: function-calling-is-not-agent-loop
- source type: existing-material-summary
- target reader: 容易把 tools/function calling/code loop 都叫 agent 的 AI builder
- planned publishable markdown path: docs/content-pipeline/manifests/function-calling-is-not-agent-loop/function-calling-is-not-agent-loop.md
- planned manifest dir: docs/content-pipeline/manifests/function-calling-is-not-agent-loop/

## Public framing

把 KB 里最清楚的一条架构判断公开化:Function calling 只是给模型一个能力;agent loop 是把下一步控制权交给模型。二者不分清,系统会被过度 agent 化。

## Draft direction

短 note,去掉 mentor/学习轨迹,保留判断和适用条件。用 Anthropic Building Effective Agents 作为官方校准来源。

## Rewrite plan

### Keep

- 外层 workflow + 内层 bounded loop。
- 步骤空间可预画就 workflow,不可预画才考虑 agent loop。
- Function calling 是能力,loop 是授权。

### Remove / anonymize

- 学习分数、mentor 轨迹、内部场景编号。
- 未核验生产数字。

### Add / refresh

- Anthropic 官方 workflow vs agent 定义作为 freshness anchor。

## Required publishable frontmatter plan

Shared:

- title: Function calling 是能力，agent loop 是授权
- description: 给模型工具不等于让模型控制流程;多数生产系统应该先 workflow,只在必要处给 bounded loop。
- date: 2026-06-15
- tags: [agents, workflow, architecture]
- visibility: public

Collection-specific:

- notes: topic: Agent architecture

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or marked as needing refresh.
- [x] Benchmark/metric claims refreshed or removed.
- [x] Security claims phrased defensively and without operational attack detail.
- [x] Hypothetical examples labeled as hypothetical.

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, or external endorsement.
- [x] Internal KB paths are kept in review metadata, not exposed as public article prose.

## Quality rubric

| item | score | note |
|---|---:|---|
| Public value | 2 | Crisp architecture distinction. |
| Source grounding | 2 | Grounded in KB take and Anthropic official framing. |
| Rewrite maturity | 2 | Clean public note, not course log. |
| Safety/privacy | 2 | No private/internal content. |
| Freshness | 2 | Official source checked. |
| Blog fit | 2 | Strong agent systems fit. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; this is one of the strongest compact viewpoints in the KB."
```

## Final human blog review

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Agent verification notes

- To be verified by content:check, sync, build, route/RSS checks.

## Adversarial review notes

- blockers: none.
- should sync for final blog review: yes.
