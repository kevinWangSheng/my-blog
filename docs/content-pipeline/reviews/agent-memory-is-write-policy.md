# Review: Agent memory 不是向量库，是写入策略

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/agent-memory/overview-agent-memory-2026.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-memory/source-summary-agent-memory-frontier-sources-2026.md
- proposed collection: essays
- proposed slug: agent-memory-is-write-policy
- source type: existing-material-summary
- target reader: 正在把 agent memory 简化成 vector DB / chat history 的 AI builder
- planned publishable markdown path: docs/content-pipeline/manifests/agent-memory-is-write-policy/agent-memory-is-write-policy.md
- planned manifest dir: docs/content-pipeline/manifests/agent-memory-is-write-policy/

## Public framing

这篇替代 RAG 主题成为更高质量的知识系统主文。核心判断是:agent memory 的关键不在“存得更多”,而在什么时候写、写什么、如何更新、如何遗忘、如何在下一轮上下文中选择。陌生读者应该读完后能区分 RAG、memory、checkpoint、chat history 和 vector search。

## Draft direction

从 KB 的 Agent Memory overview 和 source-summary 改写成公开 essay。保留系统边界与四类 memory 问题,删除内部学习路线和 raw source path。快速变化的产品/论文信号只作为“方向”,不写成不可变事实。

## Rewrite plan

### Keep

- Agent memory 不是 vector DB。
- Memory 包含当前任务状态、长期事实、经验转技能、上下文选择。
- Semantic / episodic / procedural memory 的工程意义。
- 质量问题:write policy、update policy、selection、eval、human governance。

### Remove / anonymize

- 本地 KB 路径不进入公开正文。
- 不包装成 Shawn 已构建完整 memory 产品。
- 不把论文/产品 benchmark 写成确定行业结论。

### Add / refresh

- 参考官方/primary 当前信号:OpenAI Dreaming, LangGraph memory docs, Anthropic managed agents docs。文章把它们作为方向例子,不做产品对比。

## Required publishable frontmatter plan

Shared:

- title: Agent memory 不是向量库，是写入策略
- description: 真正有用的 agent memory 不只是保存聊天历史,而是决定什么状态值得写入、更新、选择、遗忘和审计。
- date: 2026-06-15
- tags: [agent-memory, agents, context-engineering]
- visibility: public

Collection-specific:

- essays: series: Agent systems

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or explicitly scoped.
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
| Public value | 2 | Gives a durable memory architecture judgment. |
| Source grounding | 2 | Grounded in KB overview and 2026 source pack. |
| Rewrite maturity | 2 | Public essay structure, not KB copy. |
| Safety/privacy | 2 | No private paths or fake achievements. |
| Freshness | 2 | Current signals scoped to 2026-06-15. |
| Blog fit | 2 | Strong fit for agent systems and knowledge workflows. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; stronger blog-fit than the previous RAG-heavy batch."
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
- non-blocking risks: product memory features change quickly; article intentionally frames them as signals, not guarantees.
- should sync for final blog review: yes.
