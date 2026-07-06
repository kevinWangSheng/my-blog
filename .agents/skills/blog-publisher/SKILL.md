---
name: blog-publisher
description: Unified publishing workflow for this Astro blog. Use when Codex needs to turn KB material, research notes, drafts, links, logs, essays, notes, or project records into publishable blog content; run source tracing, editorial quality gates, privacy/freshness checks, multi-review adversarial critique, content manifest generation, content:check/content:sync/build/local preview, and stop at human review unless the user explicitly asks to publish/deploy.
---

# Blog Publisher

Turn candidate material into public blog content for this repository. This skill replaces the previous KB-only workflow: KB is one source, not the whole publishing system.

## Working directory (read first)

This skill is symlinked into the global skills dir, so it can be invoked from **any** directory. But it operates only on the my-blog repo at `~/dev/AI/my-blog`. **Before doing anything else, make sure the working directory is that repo root** — if not already there, run `cd ~/dev/AI/my-blog`. Every path here (`site/src/content`, `docs/content-pipeline/...`) and every `pnpm --dir site ...` command is relative to that repo root. Never write blog content anywhere else, and never create a second copy of this repo's content elsewhere.

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

**Tell the whole story (owner preference, hard requirement).** When the piece is derived from learning + practice (a video, course, paper, or tool that the author then tried), the article must cover the full arc, not just the conclusion:

1. what the source actually said (the video/course/paper's core content, in enough detail that a reader who has not seen it can follow);
2. what I actually did in practice (concrete steps, setup, code, prompts, or configs — the specific content, not "I tried it");
3. what came out of it (real data, numbers, outputs, screenshots/artifacts when they exist — do not omit results just to keep the piece short);
4. what was verified vs. what remains untested (which claims from the source held up, which didn't, which I couldn't check);
5. my own thinking afterwards (judgment, boundaries, what I'd do differently).

Compress wording, not stages — **but never force a stage whose material doesn't exist.** The arc only binds stages that actually happened or were provided. If no practice material exists, write the piece as a pure source deep-dive plus the author's judgment; do not pad it with tangential "practice" pulled from elsewhere to fill the template. Record the absent stage in the review file (a one-line declaration in the article is optional, not required). Forced padding is a blocker, same as silent skipping.

**Source deep-dives must be complete, not introductory (owner preference, hard requirement).** When the piece's job is to explain a video/talk/course/paper, cover its full content section by section — every major stage, argument, mechanism, number, and example the source gives — so a reader gets the substance without opening the original. A piece that only names the topics or summarizes the outline is a blocker. Additionally:

- Show the source's key visuals (slides, diagrams, demo screens) as images where they carry information. For video: fetch it and extract frames (`yt-dlp` + `ffmpeg -ss <t> -frames:v 1`), pick sharp, information-dense, non-duplicate frames, convert to webp, store under `site/public/images/<slug>/`, embed with a caption that credits the source (e.g. 「视频 12:20 处画面,© <speaker/org>(YouTube)」).
- For video/talk deep-dives, embed the playable source video near the top of the article unless the platform forbids embedding or the source is unavailable. For YouTube, put the bare watch URL on its own line so the site's `rehype-video-embed` plugin renders a responsive, click-to-play embed; do not rely on a text link or static screenshots alone.
- Keep the author's own commentary clearly separated from the source's content (a dedicated 评注/思考 section, or explicit 「我的判断是」 markers inline).

When an upstream draft arrives with an author voice file (e.g. blog-writing-specialist's `voice.md`), treat its author-level signatures as constraints, not raw material to normalize: keep punctuation frequency, signature phrasings, and person ("我"/"我们") as specified; rewrite only to add reader context, payoff, and boundaries. Do not flatten these into a generic house style. If the upstream says the draft was written without that voice file, this constraint does not apply.

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

**Maintain the links collection for core sources.** When the article is built around an external source — the video being解析, the primary doc the argument rests on, a tool actually practiced with — that source also gets a `links` collection entry, staged as an additional item in the same `manifest.json`. Rules:

- Promote only core sources: the test is "would I recommend this source standalone, with a one-sentence why-it-matters note?" Batch examples, passing citations, and supporting evidence stay inline in the article and do not become links entries.
- Before creating an entry, dedupe by URL against `site/src/content/links/*.md` and staged links manifests; if an entry already exists, update it only when the new article changes why it matters.
- Each links entry follows the links frontmatter contract (`url`, `category`, `note`) and passes the same review/eval pipeline as the article; its body should mention the related article so readers can jump between them (schema-level `related` only exists on notes today — do not add schema fields for this without an explicit decision).
- Record the promote/inline decision for every cited source in the review file's links-maintenance table.

### 5. Quality gate and review loop

Use `references/quality-gate.md`.

Run three review passes for every public content item except typo-only metadata fixes:

1. editor review: reader payoff, structure, title, voice, examples;
2. factual/source review: traceability, freshness, claim strength;
3. adversarial review: privacy leaks, fabricated authority, blandness, weak thesis, publish risk.

Each pass must run as an independent subagent. Only if the runtime truly cannot spawn subagents, simulate the three roles in separate passes and record that degradation explicitly in the review file.

Iterate on the draft markdown until every blocker is fixed. Mark `agent-cleared` only after the final public markdown, manifest, and review file pass the gate. If blockers remain, mark `needs-rework` and do not sync.

### 6. Mechanical checks, eval subagent, and local preview

Only after `agent-cleared`, run:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site build
pnpm preview:prepare
```

Then dispatch a **separate eval subagent** (not the drafting agent) to verify links and images against the staged markdown and the built page, following the "Eval reviewer" section of `references/quality-gate.md`. Record its per-URL/per-image results in the review file. The item cannot become `preview-ready` with a failing eval.

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
