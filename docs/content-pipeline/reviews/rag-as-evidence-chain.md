# Review: RAG 不是向量库，而是证据链工程

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md
  - /Users/shenghuikevin/kb-vault/wiki/overview-rag-systems.md
  - /Users/shenghuikevin/kb-vault/wiki/concept-context-engineering.md
- proposed collection: essays
- proposed slug: rag-as-evidence-chain
- source type: existing-material-summary
- target reader: 了解过 basic RAG,但仍把 RAG 等同于 embedding + vector DB + top-k chunk 的 AI builder / knowledge worker
- planned publishable markdown path: docs/content-pipeline/manifests/rag-as-evidence-chain/rag-as-evidence-chain.md
- planned manifest dir: docs/content-pipeline/manifests/rag-as-evidence-chain/

## Public framing

这篇应作为 RAG / Context Engineering 主题簇的主入口之一。陌生读者读完后应该能说清楚:现代 RAG 的核心不是向量数据库,而是把外部证据选择、排序、压缩、引用并装配进当前上下文的工程链条。它不是教程,而是一篇判断框架:什么时候 naive RAG 够用,什么时候需要 hybrid retrieval / rerank / graph / agentic retrieval / multimodal retrieval,以及为什么 long context 不能自动替代证据选择。

## Draft direction

将 KB 中已经较完整的中文长文改写成更公开、更紧凑的 essay。保留“lazy vector-RAG 已过时,但 RAG 作为证据供应链没有死”的主论点;删除内部学习入口语气和本地路径;用少量当前官方/primary 来源刷新关键例子,但避免写成产品功能清单或 vendor comparison。

## Rewrite plan

### Keep

- RAG 的稳定定义:外部证据进入当前上下文的选择与装配机制。
- naive RAG 的局限:固定 chunk、单向量、top-k、prompt stuffing、无 trace/eval。
- 分层链条:ingestion/index, query processing, retrieval/ranking, context assembly, grounded answer, trace/eval。
- 边界辨析:RAG vs memory vs long context vs tools/API。
- 安全段落:权限、间接 prompt injection、cache/summary/log/citation 旁路。

### Remove / anonymize

- 内部 KB 路径、学习计划、候选池语境不进入公开正文。
- 不声称 Shawn 已在生产环境证明某方案;本文只是基于已有材料与官方来源整理的判断框架。
- 不保留过多术语堆叠,避免读者被 GraphRAG / Agentic RAG / Multimodal RAG 名词墙淹没。

### Add / refresh

- 当前刷新来源:
  - Anthropic Contextual Retrieval: https://www.anthropic.com/engineering/contextual-retrieval
  - OpenAI File Search docs: https://developers.openai.com/api/docs/assistants/tools/file-search
  - Google Cloud Gemini Enterprise Agent Platform RAG Engine overview: https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview
  - Microsoft GraphRAG project/docs: https://github.com/microsoft/graphrag and https://microsoft.github.io/graphrag/
- 将“2026 当前判断”表述为截至 2026-06-15 的判断,避免伪装为长期不变事实。
- 在正文中用显式短句区分 checked facts、inference、recommendation。

## Required publishable frontmatter plan

Shared:

- title: RAG 不是向量库，而是证据链工程
- description: 把 RAG 从 embedding + top-k 的旧印象中拿出来,重新理解为外部证据进入模型上下文的选择、装配、引用和评估链条。
- date: 2026-06-15
- tags: [rag, context-engineering, retrieval, ai-systems]
- visibility: public

Collection-specific:

- essays: series: Knowledge systems

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or marked as dated 2026-06-15.
- [x] Benchmark/metric claims refreshed or removed. The public article avoids precise benchmark numbers except linked source descriptions.
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
| Public value | 2 | Reader gets a concrete mental model for modern RAG as evidence-chain engineering. |
| Source grounding | 2 | Primary KB sources are listed; current vendor examples refreshed against official/primary pages. |
| Rewrite maturity | 2 | Article is restructured for public readers, not copied as a raw KB page. |
| Safety/privacy | 2 | No secrets, internal paths, private data, fabricated results, or public project claims in the article. |
| Freshness | 2 | Fast-moving claims are scoped to 2026-06-15 and avoid brittle product details. |
| Blog fit | 2 | Directly fits AI learning, context engineering, RAG systems, and knowledge workflow themes. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers found after source tracing, freshness scoping, safety review, and public rewrite. Safe to generate publishable Markdown and manifest for final blog/result review."
```

## Final human blog review

Human review happens after the content is visible in the blog preview or published site. If the human finds problems, open a follow-up返工 session rather than blocking manifest/sync here.

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Agent verification notes

- content:check passed for `docs/content-pipeline/manifests/rag-as-evidence-chain/`.
- content:sync wrote `site/src/content/essays/rag-as-evidence-chain.md`.
- `pnpm --dir site build` generated `/essays/rag-as-evidence-chain/`, `/rss.xml`, and `/sitemap.xml`.
- RSS contains `RAG 不是向量库，而是证据链工程`.
- Public synced markdown/html were checked for absence of `/Users/shenghuikevin/kb-vault` and `docs/content-pipeline` internal paths.
- Selected from C01 priority item 1 and calibrated with C01 priority item 2.
- Public article avoids internal paths and writes as an explanatory essay, not as a KB export.
- The article includes public external links only; source paths remain in this review artifact.

## Adversarial review notes

- blockers: none.
- non-blocking risks: RAG vendor tooling changes quickly; article intentionally avoids implementation-specific feature claims and scopes the framing to 2026-06-15.
- recommended edits: after C05 related-content work, connect this essay to shorter notes on retrieval eval, context assembly, and memory boundaries.
- should sync for final blog review: yes.
