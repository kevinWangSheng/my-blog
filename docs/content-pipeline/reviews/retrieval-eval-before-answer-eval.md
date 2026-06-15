# Review: RAG 评估要先拆开 retrieval 和 answer

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/output/2026-06-04-rag-is-not-dead-context-engineering.md
  - /Users/shenghuikevin/kb-vault/wiki/overview-rag-systems.md
- proposed collection: notes
- proposed slug: retrieval-eval-before-answer-eval
- source type: existing-material-summary
- target reader: 正在做 RAG demo,但只用最终答案观感判断系统好坏的 builder
- planned publishable markdown path: docs/content-pipeline/manifests/retrieval-eval-before-answer-eval/retrieval-eval-before-answer-eval.md
- planned manifest dir: docs/content-pipeline/manifests/retrieval-eval-before-answer-eval/

## Public framing

这条 note 是 `rag-as-evidence-chain` 的配套短判断:如果 RAG 答错,不要只看最终答案,要先问正确证据有没有被召回。它帮助读者把 failure attribution 从“模型不好”拆成 retrieval failure、context assembly failure、generation faithfulness failure。

## Draft direction

改写成短 note,不复制 KB 长文。保留“retrieval eval 和 answer eval 要分开”的判断,不引入具体 benchmark 数字。

## Rewrite plan

### Keep

- 相关性不是正确性。
- RAG eval 要能回放 query、filter、candidate、rerank、context、answer。
- 先判断证据链哪一段失败,再决定修 embedding、chunking、rerank、prompt 或 answer policy。

### Remove / anonymize

- 内部 KB 路径不进入正文。
- 不声称有生产验证或 benchmark 结论。

### Add / refresh

- 作为截至 2026-06-15 的工程判断;不依赖快变产品功能。

## Required publishable frontmatter plan

Shared:

- title: RAG 评估要先拆开 retrieval 和 answer
- description: 最终答案错了,不等于模型或 RAG 整体错了;先看正确证据有没有进入上下文。
- date: 2026-06-15
- tags: [rag, evaluation, context-engineering]
- visibility: public

Collection-specific:

- notes: topic: RAG evaluation

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
| Public value | 2 | Gives a concrete debugging distinction. |
| Source grounding | 2 | Tied to RAG KB sources and companion essay. |
| Rewrite maturity | 2 | Short public note, not raw excerpt. |
| Safety/privacy | 2 | No private data or fabricated claims. |
| Freshness | 2 | No brittle fast-moving claims. |
| Blog fit | 2 | Fits RAG/context engineering theme. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; suitable as a companion note for the RAG essay."
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
- non-blocking risks: compact note may need future related-content links after C05.
- should sync for final blog review: yes.
