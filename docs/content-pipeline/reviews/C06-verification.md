# C06 verification — content quality and topic rebalance

Date: 2026-06-15

## User request

- Remove the currently public project because quality is not high enough.
- Reduce RAG-heavy article direction.
- Select more recent, higher-quality viewpoints from the KB.

## Public content downlined

Set to draft, no file deletion:

- `site/src/content/projects/agent-learning-cockpit.md`
- `site/src/content/essays/rag-as-evidence-chain.md`
- `site/src/content/notes/rag-correctness.md`
- `site/src/content/notes/retrieval-eval-before-answer-eval.md`
- `site/src/content/notes/when-graphrag-is-worth-it.md`
- `site/src/content/links/anthropic-contextual-retrieval.md`

## New KB-derived public content

Published via review → manifest → content:check → content:sync:

- Essay: `site/src/content/essays/agent-memory-is-write-policy.md`
  - Source: `/Users/shenghuikevin/kb-vault/wiki/agent-memory/overview-agent-memory-2026.md`
  - Source: `/Users/shenghuikevin/kb-vault/wiki/agent-memory/source-summary-agent-memory-frontier-sources-2026.md`
- Note: `site/src/content/notes/function-calling-is-not-agent-loop.md`
  - Source: `/Users/shenghuikevin/kb-vault/learning/agent-field/takes/agent-loop-vs-code-loop.md`
  - Source: `/Users/shenghuikevin/kb-vault/wiki/agent-field/workflow-vs-agent.md`
- Note: `site/src/content/notes/harness-before-finetune.md`
  - Source: `/Users/shenghuikevin/kb-vault/learning/agent-field/takes/harness-as-moat.md`
  - Source: `/Users/shenghuikevin/kb-vault/learning/agent-field/misconceptions.md`
- Link: `site/src/content/links/anthropic-building-effective-agents.md`
  - Source: Anthropic official `Building Effective Agents`

## Page/content adjustments

- Homepage no longer leads with Projects as the primary path.
- Homepage current focus changed to `agent memory / workflow`.
- About page no longer names `Agent Learning Cockpit` as representative project.
- Default meta description no longer says `项目入口`.
- Projects collection description now says project entries are intentionally conservative and quality-gated.

## Commands run

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/agent-memory-is-write-policy
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/agent-memory-is-write-policy
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/function-calling-is-not-agent-loop
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/function-calling-is-not-agent-loop
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/harness-before-finetune
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/harness-before-finetune
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/anthropic-building-effective-agents
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/anthropic-building-effective-agents
pnpm --dir site build
pnpm ui-verify -- --serve out/ui-serve --path /my-blog/
```

## Verification results

- All four new staging packages passed `content:check` with `ok: true`, `errors: []`, `warnings: []`.
- `content:sync` wrote all four new public content files.
- `pnpm --dir site build` passed and generated 20 pages.
- New public routes generated:
  - `/essays/agent-memory-is-write-policy/`
  - `/notes/function-calling-is-not-agent-loop/`
  - `/notes/harness-before-finetune/`
- Downlined routes no longer generated:
  - `/projects/agent-learning-cockpit/`
  - `/essays/rag-as-evidence-chain/`
  - `/notes/rag-correctness/`
  - `/notes/retrieval-eval-before-answer-eval/`
  - `/notes/when-graphrag-is-worth-it/`
- RSS contains the new Agent Memory / workflow / harness entries and no longer contains the downlined RAG entries.
- Public leak check: no `/Users/shenghuikevin/kb-vault` or `docs/content-pipeline` internal paths in the new public content/html checked.
- UI verify homepage result from `out/summary.json`:
  - axe: 0 violations at 375 / 768 / 1440.
  - console: 0 errors / 0 warnings at all breakpoints.
  - horizontal overflow: no at all breakpoints.
  - Lighthouse: performance 100, accessibility 100, best-practices 100, SEO 100.

## External sources refreshed

- Anthropic Building Effective Agents: https://www.anthropic.com/research/building-effective-agents
- OpenAI Dreaming memory: https://openai.com/index/chatgpt-memory-dreaming/
- LangGraph memory docs: https://docs.langchain.com/oss/python/concepts/memory
- Claude Managed Agents docs: https://platform.claude.com/docs/en/managed-agents/overview

## Conclusion

The public site is now less RAG-heavy, the weak project is removed from public routing, and the newest high-quality viewpoint path is agent memory / workflow / harness.
