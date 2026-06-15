---
name: kb-to-blog
description: Turn local KB materials from /Users/shenghuikevin/kb-vault into blog-ready Markdown for this Astro blog. Use when Codex needs to select, evaluate, rewrite, or prepare KB-derived blog essays, notes, logs, links, or projects; generate docs/content-pipeline review files; create article Markdown and manifest inputs compatible with site/scripts/content-check.mjs and content-sync.mjs; enforce source tracing, freshness checks, privacy/no-fabrication checks, agent self-review, and final human review after the content is visible in the blog.
---

# KB to Blog

Convert KB material into public blog content. This is a **content transformation and editorial gating** skill. Sync scripts are downstream mechanical gates after agent self-review.

## Core stance

- Blog is the public expression layer; `/Users/shenghuikevin/kb-vault` is the source workspace.
- Use candidates and the `/Users/shenghuikevin/kb-vault` filesystem as the main source path. Use the existing `kb` skill only for explicit llm-kb CLI tasks; do not assume llm-kb and kb-vault are the same store.
- Do not copy KB pages directly into `site/src/content`.
- First produce `docs/content-pipeline/reviews/<slug>.md` with source paths, rewrite plan, safety checks, and agent review status.
- A review file is not publishable Markdown. Create a separate article `.md` with valid frontmatter and body before sync.
- Do not pause before manifest/sync just to request human approval; human review happens at the final blog/result stage. If the human finds problems, they can open a follow-up返工 session.
- Do not push or deploy unless the user explicitly asks for that phase.

## Workflow

### 1. Select source material

Start from `docs/content-pipeline/candidates.md`, an explicit `/Users/shenghuikevin/kb-vault/...` path, or a user-named theme. Classify sources as `candidate`, `needs-rewrite`, `source-only`, or `not-public`.

### 2. Decide blog shape

Map the material to exactly one primary target:

- `essay`: mature argument, map, synthesis, or durable explanation.
- `note`: compact judgment, glossary item, architecture pattern, or single idea.
- `log`: learning/process update or open question with time context.
- `link`: curated external source with short note.
- `project`: only when there is real public evidence; never invent repo/demo/results.

### 3. Transform content editorially

Rewrite for an unfamiliar public reader:

- Add missing context: why this matters, who should read it, what decision it helps.
- Preserve source-grounded claims; remove private learning scaffolding, mentor language, raw run logs, and internal-only paths from public prose.
- Separate checked facts, inference, and personal judgment.
- Label hypothetical cases as hypothetical.
- For fast-moving claims about models, vendors, protocols, benchmarks, security, or APIs, refresh against official/primary sources or mark as needing refresh.
- Avoid “I built / shipped / proved” language unless the source supports it and the project is public.

### 4. Create a review file

Write `docs/content-pipeline/reviews/<slug>.md` using `references/review-template.md`. For scoring and adversarial review, load `references/evaluation.md`.

Set status to `draft`; set status to `agent-cleared` only after agent self-review finds no blockers.

### 5. Agent self-review before publishable files

Do not generate a syncable manifest or run `content:sync` until the review file is complete and the draft passes `references/evaluation.md` gates. This is an agent quality gate, not a human approval gate.

For non-trivial drafts, use an adversarial subagent before sync when practical. If blockers remain, fix them before syncing.

### 6. Create publishable files and sync

Create a separate publishable Markdown article and manifest using `references/publishable-markdown.md`.

Required layout:

```text
docs/content-pipeline/manifests/<slug>/
  manifest.json
  <slug>.md
```

Real command shape:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site build
```

Do not pass bare positional paths; the scripts only parse `--key value` arguments.

### 7. Final human blog review

After sync/build/verification, report the local/online blog paths and evidence. The human review point is the actual blog result. Do not ask the user to approve intermediate review files unless they explicitly request that workflow.

## Evaluation

Use `references/evaluation.md` for pass/fail gates, the 12-point rubric, and the adversarial review prompt. Use `references/publishable-markdown.md` before preparing any article or manifest.
