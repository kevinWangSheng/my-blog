---
name: kb-to-blog
description: Turn local KB materials from /Users/shenghuikevin/kb-vault into review-ready and, after human approval, publishable Markdown for this Astro blog. Use when Codex needs to select, evaluate, rewrite, or prepare KB-derived blog essays, notes, logs, links, or projects; generate docs/content-pipeline review files; create approved article Markdown and manifest inputs compatible with site/scripts/content-check.mjs and content-sync.mjs; enforce source tracing, freshness checks, privacy/no-fabrication checks, and the human approval gate before any sync or publication.
---

# KB to Blog

Convert KB material into public blog content. This is a **content transformation and editorial gating** skill. Sync scripts are downstream mechanical gates after human approval.

## Core stance

- Blog is the public expression layer; `/Users/shenghuikevin/kb-vault` is the source workspace.
- Use candidates and the `/Users/shenghuikevin/kb-vault` filesystem as the main source path. Use the existing `kb` skill only for explicit llm-kb CLI tasks; do not assume llm-kb and kb-vault are the same store.
- Do not copy KB pages directly into `site/src/content`.
- First produce `docs/content-pipeline/reviews/<slug>.md` with source paths, rewrite plan, safety checks, and human approval status.
- A review file is not publishable Markdown. After approval, create a separate article `.md` with valid frontmatter and body.
- Do not run `content:sync`, publish, push, or deploy unless an approved review/manifest exists and the user request explicitly covers that phase.

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

Set status to `needs-human-review` unless the user explicitly approves.

### 5. Human gate before publishable files

Do not generate a syncable manifest or run `content:sync` unless the review file contains human approval, for example:

```yaml
approval:
  status: approved
  reviewer: human
  date: YYYY-MM-DD
  notes: "..."
```

This is a process gate, not a script-enforced gate. The agent must enforce it.

### 6. After approval only

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

### 7. Adversarial review

For non-trivial drafts, use an independent subagent after the main draft/review pass. Ask it to find blockers in public value, source grounding, freshness, privacy, fabricated claims, and blog fit.

## Evaluation

Use `references/evaluation.md` for pass/fail gates, the 12-point rubric, and the adversarial review prompt. Use `references/publishable-markdown.md` before preparing any approved article or manifest.
