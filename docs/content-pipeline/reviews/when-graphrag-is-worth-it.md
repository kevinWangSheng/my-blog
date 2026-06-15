# Review: 什么时候 GraphRAG 值得上

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md
  - /Users/shenghuikevin/kb-vault/wiki/overview-rag-systems.md
- proposed collection: notes
- proposed slug: when-graphrag-is-worth-it
- source type: existing-material-summary
- target reader: 听过 GraphRAG,但不确定什么时候该引入图结构的 AI builder
- planned publishable markdown path: docs/content-pipeline/manifests/when-graphrag-is-worth-it/when-graphrag-is-worth-it.md
- planned manifest dir: docs/content-pipeline/manifests/when-graphrag-is-worth-it/

## Public framing

这条 note 把 GraphRAG 从 buzzword 拉回 fit condition:不是文档多就上图,而是答案必须依赖实体关系、跨文档结构、全局主题或多跳推理时才值得增加复杂度。

## Draft direction

基于 KB RAG 文章和 Microsoft GraphRAG docs 的官方刷新,写成短判断,避免夸大 GraphRAG 普适性。

## Rewrite plan

### Keep

- GraphRAG 适合关系密集、多跳、跨文档 sensemaking。
- 简单事实问答、单文档 QA、低延迟场景不该默认上 GraphRAG。

### Remove / anonymize

- 不进入具体 benchmark 数字或 vendor 胜负判断。
- 不声称实际项目成果。

### Add / refresh

- Microsoft GraphRAG docs 当前描述:structured hierarchical approach, extracts knowledge graph, builds community hierarchy, generates summaries, uses structures for RAG tasks.

## Required publishable frontmatter plan

Shared:

- title: 什么时候 GraphRAG 值得上
- description: GraphRAG 的判断标准不是文档多,而是答案是否必须依赖关系结构和跨文档综合。
- date: 2026-06-15
- tags: [rag, graphrag, architecture]
- visibility: public

Collection-specific:

- notes: topic: RAG architecture

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
| Public value | 2 | Gives a clear adoption condition. |
| Source grounding | 2 | Grounded in KB RAG work and Microsoft GraphRAG docs. |
| Rewrite maturity | 2 | Public note with fit conditions. |
| Safety/privacy | 2 | No private data or fabricated claims. |
| Freshness | 2 | Current official docs checked. |
| Blog fit | 2 | Fits RAG architecture theme. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; official GraphRAG framing refreshed and scoped."
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

- content:check/content:sync/build evidence recorded in C04 task completion.

## Adversarial review notes

- blockers: none.
- non-blocking risks: should eventually link to the RAG essay once C05 recommendations exist.
- should sync for final blog review: yes.
