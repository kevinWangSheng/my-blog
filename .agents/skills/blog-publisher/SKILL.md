---
name: blog-publisher
description: Unified publishing workflow for this Astro blog. Use when Codex needs to turn KB material, research notes, drafts, links, logs, essays, notes, or project records into publishable blog content; run source tracing, editorial quality gates, privacy/freshness checks, multi-review adversarial critique, content manifest generation, content:check/content:sync/build/local preview, and stop at human review unless the user explicitly asks to publish/deploy.
---

# Blog Publisher

Turn candidate material into public blog content for this repository. This skill replaces the previous KB-only workflow: KB is one source, not the whole publishing system.

## Load these references

- Always read `references/editorial-standard.md` before drafting or approving content.
- Always read `references/review-template.md` before creating a review file.
- Always read `references/publishable-markdown.md` before creating manifest input.
- Always read `references/quality-gate.md` before marking an item agent-cleared, preview-ready, or publish-ready.

## Core contract

- Public content lives in `site/src/content/*` only after review, quality gate, and mechanical sync.
- Staging artifacts live under:
  - `docs/content-pipeline/reviews/<slug>.md`
  - `docs/content-pipeline/manifests/<slug>/manifest.json`
  - `docs/content-pipeline/manifests/<slug>/<slug>.md`
- Never copy KB/private notes directly into `site/src/content`.
- Keep source paths inside review metadata; do not expose local paths in public prose.
- Do not push/deploy unless the user explicitly asks for publishing after review.
- Follow repo `AGENTS.md` and `CONVENTIONS.md`; do not change old deployment/cutover boundaries unless the request explicitly includes that.

## Source routing

Use the narrowest source path available:

- KB/vault: `/Users/shenghuikevin/kb-vault`, `docs/content-pipeline/candidates.md`, or explicit user-named KB files.
- Draft files: user-provided Markdown, local output, research reports, or article notes.
- External sources: prefer official/primary sources for fast-moving claims; cite them in review metadata and public prose only when useful to readers.
- Project content: require real public evidence. Never invent repo/demo/results, users, endorsements, or shipped outcomes.

## Workflow

### 1. Select and scope

Pick a narrow public thesis before drafting. A good item should answer: who should read this, what decision it helps, and what one sentence the reader should remember.

Classify target type:

- `essay`: durable argument, synthesis, or map.
- `note`: compact judgment, concept boundary, or architecture pattern.
- `log`: time-bounded learning/process update.
- `link`: curated source plus why it matters.
- `project`: public project/portfolio evidence only.

### 2. Draft for public readers

Rewrite, do not transcribe. Add context, examples, tradeoffs, edge cases, and concrete reader payoff. Separate checked facts, inference, and personal judgment. Remove mentor scaffolding, raw run logs, private markers, internal paths, and unsupported claims.

### 3. Create review file and run source review

Create `docs/content-pipeline/reviews/<slug>.md` from `references/review-template.md` with status `draft`.

Before generating publishable Markdown, complete source/freshness/safety review and set status to `draft-review-passed` only if there are no source/safety blockers.

### 4. Create draft publishable Markdown and manifest

After `draft-review-passed`, create:

```text
docs/content-pipeline/manifests/<slug>/
  manifest.json
  <slug>.md
```

Follow `references/publishable-markdown.md`. These files are still draft staging files; do not sync yet.

### 5. Quality gate and review loop

Use `references/quality-gate.md`.

Run three review passes for every public content item except typo-only metadata fixes:

1. editor review: reader payoff, structure, title, voice, examples;
2. factual/source review: traceability, freshness, claim strength;
3. adversarial review: privacy leaks, fabricated authority, blandness, weak thesis, publish risk.

Use independent subagents when available. If subagents are not available, simulate the three roles in separate passes and record that limitation in the review file.

Iterate on the draft markdown until every blocker is fixed. Mark `agent-cleared` only after the final public markdown, manifest, and review file pass the gate. If blockers remain, mark `needs-rework` and do not sync.

### 6. Mechanical checks and local preview

Only after `agent-cleared`, run:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site build
pnpm preview:prepare
```

For changed UI/layout or a representative long-form page, also run `pnpm ui-verify -- --serve out/ui-serve --path /my-blog/<route>/`.

Run a concrete leak check on the staged public markdown, synced source, and generated HTML. At minimum search for:

```bash
grep -R "/Users/\|kb-vault\|docs/content-pipeline\|private draft\|confidential\|机密\|不发布\|禁止发布" <public-files>
```

### 7. Human review and rejection cleanup

Report local preview URLs, changed files, quality-gate result, reviewer blockers/resolutions, and command evidence.

If the human rejects the preview or asks for rework:

- set the review status to `needs-rework`;
- remove or revert the generated `site/src/content/*/<slug>.md` files from the tree;
- keep review/manifest drafts only if useful for rework;
- do not leave rejected content as live public-source content.

### 8. Publish boundary

Stop at human review unless the user explicitly says to publish/deploy. When the user says publish, run a final build, commit scoped changes, push the publishing branch, wait for CI/deploy, and verify the public URL.
