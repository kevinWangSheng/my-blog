# Review: Anthropic Building Effective Agents

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/agent-memory/source-summary-agent-memory-frontier-sources-2026.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/workflow-vs-agent.md
- proposed collection: links
- proposed slug: anthropic-building-effective-agents
- source type: source-only-derived
- target reader: 需要 workflow vs agent 官方架构地基的读者
- planned publishable markdown path: docs/content-pipeline/manifests/anthropic-building-effective-agents/anthropic-building-effective-agents.md
- planned manifest dir: docs/content-pipeline/manifests/anthropic-building-effective-agents/

## Public framing

这条 link 替代 RAG source shelf,作为 agent architecture 主线的官方来源。它支撑“workflow first, agents only where needed”的判断。

## Draft direction

简短 link entry。避免大段引用,只说明为什么这个来源值得读。

## Rewrite plan

### Keep

- Workflow vs agent 的 locus-of-control 区分。
- Start simple / composable patterns 的实践价值。

### Remove / anonymize

- 不复制官方长文。
- 不写成唯一权威或不变结论。

### Add / refresh

- 2026-06-15 当前仍可访问的 Anthropic 官方/primary source。

## Required publishable frontmatter plan

Shared:

- title: Anthropic Building Effective Agents
- description: 官方 agent 架构地基:先区分 workflow 和 agent,从简单可组合模式开始,不要默认追求全自动 loop。
- date: 2026-06-15
- tags: [agents, workflow, architecture]
- visibility: public

Collection-specific:

- links: url: https://www.anthropic.com/research/building-effective-agents; category: essay; note: workflow vs agent 的官方架构来源。

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
| Public value | 2 | Gives reader an official architecture source. |
| Source grounding | 2 | Official Anthropic page checked. |
| Rewrite maturity | 2 | Public source note. |
| Safety/privacy | 2 | No private data. |
| Freshness | 2 | Checked on 2026-06-15. |
| Blog fit | 2 | Strong agent architecture fit. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; replaces RAG-heavy source shelf with stronger agent architecture source."
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

- To be verified by content:check, sync, build, route checks.

## Adversarial review notes

- blockers: none.
- should sync for final blog review: yes.
