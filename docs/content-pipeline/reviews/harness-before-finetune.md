# Review: 先投 harness，再谈 fine-tune

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/learning/agent-field/takes/harness-as-moat.md
  - /Users/shenghuikevin/kb-vault/learning/agent-field/misconceptions.md
- proposed collection: notes
- proposed slug: harness-before-finetune
- source type: existing-material-summary
- target reader: 以为差异化主要来自 fine-tune 或换更强模型的 AI product builder
- planned publishable markdown path: docs/content-pipeline/manifests/harness-before-finetune/harness-before-finetune.md
- planned manifest dir: docs/content-pipeline/manifests/harness-before-finetune/

## Public framing

这条 note 是高质量观点:模型会变,但 harness 投资可累积。它不是说 fine-tune 没价值,而是把 fine-tune 放到 prompt/context/harness 之后。

## Draft direction

短判断,不保留学习轨迹和未经刷新 benchmark 数字。强调 fit condition 和反证条件。

## Rewrite plan

### Keep

- Harness 不是 fine-tune 替代品,是任何路径都必经。
- Harness 投资会随模型升级继续复用。
- Fine-tune 应该是后手,不是默认第一步。

### Remove / anonymize

- 未核验 benchmark 数字。
- 内部 scenario/mentor 语言。

### Add / refresh

- 用“截至 2026-06-15 的实践判断”措辞,避免绝对化。

## Required publishable frontmatter plan

Shared:

- title: 先投 harness，再谈 fine-tune
- description: 如果问题能通过工具、权限、上下文、评估和流程解决, fine-tune 不应该是第一反应。
- date: 2026-06-15
- tags: [agents, harness, product]
- visibility: public

Collection-specific:

- notes: topic: Agent product strategy

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
| Public value | 2 | Clear product strategy heuristic. |
| Source grounding | 2 | Grounded in KB take/misconception record. |
| Rewrite maturity | 2 | Public note, no internal learning trace. |
| Safety/privacy | 2 | No private or fabricated claims. |
| Freshness | 2 | Metrics removed; judgment scoped. |
| Blog fit | 2 | Strong fit for agent product/workflow direction. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers; concise high-signal viewpoint."
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
- non-blocking risks: add public examples later if user wants stronger evidence.
- should sync for final blog review: yes.
