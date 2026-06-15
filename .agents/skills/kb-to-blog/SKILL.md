---
name: kb-to-blog
description: Turn local KB materials into review-ready blog drafts for this Astro blog. Use when Codex needs to select, evaluate, rewrite, or prepare content from /Users/shenghuikevin/kb-vault for blog essays, notes, logs, links, or projects; generate docs/content-pipeline review files; enforce source tracing, freshness checks, privacy/no-fabrication checks, and the human approval gate before any content:sync or publication.
---

# KB to Blog

Convert KB material into public blog content. This skill is primarily a **content transformation and editorial gating** workflow, not a deploy/sync automation. The sync scripts are downstream mechanical gates after human approval.

## Core stance

- Blog is the public expression layer; KB is the private/source workspace.
- Do not copy KB pages directly into `site/src/content`.
- Produce `review-ready` drafts first, with source paths, rewrite plan, safety checks, and human approval status.
- Do not call `content:sync`, publish, push, or deploy unless an approved review/manifest exists and the user request explicitly covers that phase.
- Preserve the human at the judgment gate: approve/reject public framing, not routine file handling.

## Workflow

### 1. Select source material

Start from one of:

- `docs/content-pipeline/candidates.md`
- an explicit `/Users/shenghuikevin/kb-vault/...` path
- a user-named theme such as RAG, Context Engineering, Agent Memory, or Agent Systems

Classify each source as:

- `candidate`: can become a draft after editorial rewriting.
- `needs-rewrite`: valuable but requires structure/freshness/public-framing work.
- `source-only`: background/source pack only; do not publish directly.
- `not-public`: private, unsafe, too local, or not suitable.

### 2. Decide blog shape

Map the material to exactly one primary target:

- `essay`: mature argument, map, synthesis, or durable explanation.
- `note`: compact judgment, glossary item, architecture pattern, or single idea.
- `log`: learning/process update or open question with time context.
- `link`: curated external source with short note.
- `project`: only when there is real public evidence; never invent repo/demo/results.

Prefer first batches from:

1. RAG / Context Engineering
2. Agent Memory
3. Agent Systems / Harness

### 3. Transform content editorially

For review-ready drafts, rewrite for an unfamiliar public reader:

- Add the missing context: why this matters, who should read it, what decision it helps.
- Preserve source-grounded claims; remove private learning scaffolding, mentor language, raw run logs, and internal-only paths.
- Separate checked facts, inference, and personal judgment.
- Label hypothetical cases as hypothetical.
- For fast-moving claims about models, vendors, protocols, benchmarks, security, or APIs, refresh against official/primary sources or mark as needing refresh.
- Avoid “I built / shipped / proved” language unless the source clearly supports it and the project is public.

### 4. Create a review file

Write `docs/content-pipeline/reviews/<slug>.md` using `references/review-template.md`. For scoring and adversarial review, load `references/evaluation.md`.

A review file must contain:

- source paths and proposed collection/slug/title
- target reader and public framing
- rewrite plan: keep / remove-anonymize / add-refresh
- fact refresh checklist
- safety and no-fabrication checklist
- quality rubric score
- human review block

Set status to `needs-human-review` unless the user explicitly approves.

### 5. Human gate before sync

Do not generate an executable manifest or run `content:sync` unless the review file contains human approval, for example:

```yaml
approval:
  status: approved
  reviewer: human
  date: YYYY-MM-DD
  notes: "..."
```

### 6. After approval only

After approval, generate `docs/content-pipeline/manifests/<slug>.json`, then run project tooling:

```bash
pnpm --dir site content:check -- <input-or-manifest>
pnpm --dir site content:sync -- <input-or-manifest>
pnpm --dir site build
```

If a UI/content route changes materially, also run the local UI verification loop from the project `ui-verify` skill.

### 7. Adversarial review

For non-trivial drafts, use an independent subagent after the main draft/review pass. Ask it to find blockers in:

- public value and readability
- source grounding and freshness
- secrets/private markers/forbidden publish markers
- fabricated achievements, external backing, repo/demo links, or project results
- mismatch with the blog's positioning: AI learning, agent systems, project practice, knowledge workflows

## Evaluation

Use `references/evaluation.md` for pass/fail gates, the 12-point rubric, and the adversarial review prompt.
