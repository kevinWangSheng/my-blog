# Review: Sandbox 保护 host，不保护你放进去的 secrets

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/sandbox-isolation.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/code-execution.md
- proposed collection: notes
- proposed slug: sandbox-protects-host-not-secrets
- source type: existing-material-summary
- target reader: 正在把敏感材料挂进 agent workspace 的 builder
- planned publishable markdown path: docs/content-pipeline/manifests/sandbox-protects-host-not-secrets/sandbox-protects-host-not-secrets.md
- planned manifest dir: docs/content-pipeline/manifests/sandbox-protects-host-not-secrets/

## Public framing

短 note,强调 sandbox 的边界误解。它保护 host 和其他租户,但不自动保护已经放进 sandbox 的数据。

## Draft direction

防守型短判断,不涉及攻击步骤。

## Rewrite plan

### Keep

- Sandbox protects host, not itself.
- 凭据、文件、网络授权是产品设计问题。

### Remove / anonymize

- 攻防细节和未核验安全事件数字。

### Add / refresh

- 和主文互相链接。

## Required publishable frontmatter plan

Shared:

- title: Sandbox 保护 host，不保护你放进去的 secrets
- description: 隔离边界能限制失控进程,但不能替你决定哪些凭据、文件和网络权限不该进入 sandbox。
- date: 2026-06-15
- tags: [sandbox, security, agents]
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
| Public value | 2 | Sharp safety boundary. |
| Source grounding | 2 | Grounded in sandbox KB. |
| Rewrite maturity | 2 | Clean note. |
| Safety/privacy | 2 | Defensive, no exploit detail. |
| Freshness | 2 | No brittle claims. |
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
