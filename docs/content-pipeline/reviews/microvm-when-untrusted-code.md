# Review: 什么时候需要 microVM sandbox

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/microvm-sandbox.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/sandbox-e2b.md
  - /Users/shenghuikevin/kb-vault/wiki/source-summary-2026-05-18-e2b-breakdown.md
- proposed collection: notes
- proposed slug: microvm-when-untrusted-code
- source type: existing-material-summary
- target reader: 不确定 Docker/container 和 microVM 该怎么选的 builder
- planned publishable markdown path: docs/content-pipeline/manifests/microvm-when-untrusted-code/microvm-when-untrusted-code.md
- planned manifest dir: docs/content-pipeline/manifests/microvm-when-untrusted-code/

## Public framing

短 note,给 microVM 的 fit condition,避免把 microVM 当万能答案。

## Draft direction

从 KB 和 Firecracker/E2B 官方来源提炼。不写具体性能数字,只写边界。

## Rewrite plan

### Keep

- Shared-kernel container vs dedicated-kernel microVM 的核心差异。
- untrusted code / multi-tenant / proprietary code 更适合 microVM。
- trusted/dev/lightweight workload 可以先用更轻方式。

### Remove / anonymize

- 未核验 boot-time/vendor 数字。

### Add / refresh

- Firecracker official definition and E2B docs as source anchors.

## Required publishable frontmatter plan

Shared:

- title: 什么时候需要 microVM sandbox
- description: microVM 的理由不是炫技,而是 threat model:不可信代码、多租户、强隔离和可控执行面。
- date: 2026-06-15
- tags: [sandbox, microvm, agents]
- visibility: public

Collection-specific:

- notes: topic: Agent sandbox

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
| Public value | 2 | Clear fit condition. |
| Source grounding | 2 | KB + Firecracker/E2B sources. |
| Rewrite maturity | 2 | Public note. |
| Safety/privacy | 2 | Defensive. |
| Freshness | 2 | No brittle metrics. |
| Blog fit | 2 | Fits sandbox theme. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers."
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

- To be verified by content:check, sync, build.

## Adversarial review notes

- blockers: none.
- should sync for final blog review: yes.
