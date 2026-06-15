# Review: Anthropic Contextual Retrieval

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/overview-rag-systems.md
  - /Users/shenghuikevin/kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md
- proposed collection: links
- proposed slug: anthropic-contextual-retrieval
- source type: source-only-derived
- target reader: 需要一个现代 RAG retrieval 改进入口源的读者
- planned publishable markdown path: docs/content-pipeline/manifests/anthropic-contextual-retrieval/anthropic-contextual-retrieval.md
- planned manifest dir: docs/content-pipeline/manifests/anthropic-contextual-retrieval/

## Public framing

这条 link 给 RAG 主题簇补一个官方工程来源。它不是替 Anthropic 背书,而是说明一个重要工程模式:chunk 被切出来后会丢文档级语境,可以在 embedding/BM25 前补充 chunk-specific context,并与 reranking 组合。

## Draft direction

写成 link entry,突出为什么值得读、和本站 RAG essay 的关系、读者应注意的边界。

## Rewrite plan

### Keep

- Contextual Retrieval 的核心问题:traditional RAG chunking removes context.
- 技术点:contextual embeddings, contextual BM25, reranking.
- 作为 RAG evidence-chain 的 ingestion/index/retrieval 案例。

### Remove / anonymize

- 不复制长段官方原文。
- 不把厂商实验数字写成普遍保证。

### Add / refresh

- 已打开官方 Anthropic 页面,发布时间 2024-09-19;当前仍可访问。

## Required publishable frontmatter plan

Shared:

- title: Anthropic Contextual Retrieval
- description: 一个说明现代 RAG 不只靠向量相似度的官方工程来源:给 chunk 补上下文,再结合 BM25 和 reranking。
- date: 2026-06-15
- tags: [rag, retrieval, context-engineering]
- visibility: public

Collection-specific:

- links: url: https://www.anthropic.com/engineering/contextual-retrieval; category: essay; note: 官方工程文章,适合作为 RAG evidence-chain 的 retrieval/indexing 案例。

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
| Public value | 2 | Gives readers a concrete source to revisit. |
| Source grounding | 2 | Official Anthropic source checked. |
| Rewrite maturity | 2 | Public link note, not copied article. |
| Safety/privacy | 2 | No private data. |
| Freshness | 2 | Current source checked on 2026-06-15. |
| Blog fit | 2 | Fits RAG/context engineering source shelf. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; link entry is safe and useful as companion source."
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
- non-blocking risks: vendor docs can drift; entry includes date and does not overgeneralize benchmark results.
- should sync for final blog review: yes.
