# Review: Agent sandbox 是执行边界，不是安全按钮

## Metadata

- status: synced
- source paths:
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/sandbox-isolation.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/code-execution.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/microvm-sandbox.md
  - /Users/shenghuikevin/kb-vault/wiki/agent-field/sandbox-e2b.md
- proposed collection: essays
- proposed slug: sandbox-is-execution-boundary
- source type: existing-material-summary
- target reader: 想让 agent 执行代码/命令,但还没有把 sandbox 当成产品架构边界的人
- planned publishable markdown path: docs/content-pipeline/manifests/sandbox-is-execution-boundary/sandbox-is-execution-boundary.md
- planned manifest dir: docs/content-pipeline/manifests/sandbox-is-execution-boundary/

## Public framing

这篇是 sandbox 窄主题主文。不是做厂商横评,而是给读者一个判断框架:agent sandbox 不是“开了就安全”的按钮,而是执行边界。它要和权限、网络、凭据、文件挂载、trace、approval 一起设计。

## Draft direction

从 KB sandbox isolation / code execution / microVM / E2B 页面提炼成公开 essay。删除不稳定数字和未经核验 vendor claim,保留稳定机制和 fit condition。外部刷新使用 E2B docs、Firecracker docs、OpenAI Sandbox Agents、LangSmith Sandboxes 等 primary/official-ish sources。

## Rewrite plan

### Keep

- Sandbox 的核心作用是隔离 agent 执行面和主系统。
- 至少有 compute / filesystem / network / resource / credential 边界。
- Sandbox 保护 host,但不自动保护 sandbox 内部已经授权给 agent 的数据。
- MicroVM 适合 untrusted code / multi-tenant / proprietary code; container 更适合 trusted/dev/lightweight 场景。

### Remove / anonymize

- 未核验 CVE/百分比/厂商 benchmark 数字。
- 内部 KB 路径不进入公开正文。
- 不写成安全攻防教程,只做防守型架构判断。

### Add / refresh

- E2B docs: sandboxes for isolated agent code/tool execution.
- Firecracker: microVMs combine hardware virtualization isolation with container-like speed/flexibility.
- OpenAI Sandbox Agents docs: sandbox 用于答案依赖 workspace 工作结果时。
- LangSmith Sandboxes: secure environments for agent code execution, isolated environments.

## Required publishable frontmatter plan

Shared:

- title: Agent sandbox 是执行边界，不是安全按钮
- description: 让 agent 跑代码之前,先分清 sandbox 能隔离什么、不能替你决定什么,以及为什么凭据和网络边界仍然是产品设计问题。
- date: 2026-06-15
- tags: [agents, sandbox, security, harness]
- visibility: public

Collection-specific:

- essays: series: Agent systems

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or marked as scoped.
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
| Public value | 2 | Gives a narrow, actionable sandbox judgment framework. |
| Source grounding | 2 | Grounded in KB pages and refreshed official/primary sources. |
| Rewrite maturity | 2 | Public essay, not KB copy. |
| Safety/privacy | 2 | Defensive framing, no operational attack detail. |
| Freshness | 2 | Current sources refreshed and brittle numbers removed. |
| Blog fit | 2 | Strong fit with agent workflow/harness theme. |

Total: 12/12

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: Dex
  date: 2026-06-15
  notes: "No blockers. Good narrow follow-up theme after agent memory/workflow/harness."
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

- To be verified with content:check, sync, build, route/RSS and local preview checks.

## Adversarial review notes

- blockers: none.
- non-blocking risks: security topic should stay defensive; avoid expanding into detailed exploit mechanics.
- should sync for final blog review: yes.
