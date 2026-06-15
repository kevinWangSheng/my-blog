# Quality gate and review loop

Use this before syncing and before publishing.

## Gate states

- `draft`: content direction exists; source/safety review is not complete.
- `draft-review-passed`: source grounding, safety checklist, and target shape are clear enough to create draft publishable Markdown and manifest.
- `agent-cleared`: final staged Markdown, manifest, review file, quality score, leak check, and three-pass critique have no blockers; content may be synced for local preview.
- `synced`: content is in `site/src/content` and build passes locally.
- `preview-ready`: local preview and required checks pass; human can review rendered result before publish/deploy.
- `publish-ready`: human has approved rendered preview or explicitly asked to publish; final build passes.
- `published`: CI/deploy has succeeded and public URL was verified.
- `needs-rework`: blockers remain or human rejected preview; do not publish. If already synced for preview, remove/revert generated `site/src/content/*/<slug>.md`.

## Review passes

Run three review passes for every public content item except typo-only metadata fixes. Use independent subagents when available. If not available, run three separate role passes yourself and disclose that limitation.

### Editor reviewer

Prompt goal: make the article worth reading.

Check:

- Is the thesis memorable?
- Does the title promise the actual article?
- Where does the reader get bored?
- Are examples, contrast, and edge cases concrete enough?
- Is the voice public and human rather than KB/admin tone?

Output:

- blockers
- major edits
- minor edits
- score impact
- pass: yes/no

### Source/factual reviewer

Prompt goal: prevent unsupported claims.

Check:

- Are all non-obvious claims traceable to source paths or refreshed sources?
- Are fast-moving vendor/model/API/security claims current enough?
- Are inferences labeled as judgment rather than fact?
- Are public links/claims real?
- For project content: does every repo/demo/result/status claim have public evidence or local source evidence recorded in review metadata?

Output:

- blockers
- claims needing citation/refresh/removal
- safe claims
- pass: yes/no

### Adversarial reviewer

Prompt goal: try to stop publication.

Check:

- Any secret, internal path, private data, or forbidden marker in public prose?
- Any fabricated achievement or inflated authority?
- Any content-farm blandness or weak reason to publish?
- Any reputational/security risk?
- Would a sharp external reader learn anything?

Output:

- blockers
- non-blocking risks
- required revisions
- pass: yes/no

## Passing rule

To mark `draft-review-passed`:

- source paths/records are identified;
- target collection and public thesis are clear;
- no obvious privacy, forbidden-publish, or fabrication blocker remains;
- fast-moving claims have a refresh plan or are removed.

To mark `agent-cleared`:

- final staged Markdown and manifest exist;
- editorial score >= 14/18;
- all three review passes say pass or have only non-blocking risks;
- every blocker has a recorded resolution;
- staged public markdown contains no local source paths or forbidden markers;
- source/freshness/privacy checklists are complete.

To mark `preview-ready`:

- `content:check`, `content:sync`, and `pnpm --dir site build` pass;
- local preview route exists;
- leak check passes on staged public markdown, synced source, and generated HTML;
- `ui-verify` is run for UI/layout changes or representative long-form page changes.

To mark `publish-ready`:

- human has approved rendered preview or explicitly requested publish;
- final build passes;
- deployment boundary is understood: push/deploy only on explicit request.
