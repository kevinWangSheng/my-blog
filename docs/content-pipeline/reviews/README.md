# Content pipeline reviews

This directory stores the editorial/audit layer between `/Users/shenghuikevin/kb-vault` and the public Astro content directory. Review files are not publishable Markdown; they preserve source tracing, rewrite intent, safety checks, freshness checks, and agent review status.

## Status model

- `discovered`: found in KB or candidate scan, not yet evaluated.
- `candidate`: likely worth turning into blog content, but not rewritten or reviewed.
- `needs-rewrite`: useful material, but requires public framing, restructuring, safety cleanup, or freshness work.
- `review-ready`: review file is complete enough for agent review, but blockers may remain.
- `agent-cleared`: agent self-review and adversarial review found no blockers; may generate publishable Markdown and manifest for `content:check` / `content:sync`.
- `synced`: publishable Markdown has passed `content:check` and has been written into `site/src/content`.
- `published`: synced content is visible on the final online blog after build/deploy.
- `needs-rework`: final blog review, verification, or later audit found problems.
- `rejected`: not suitable for public blog use.

## Gate rule

No KB-derived content should enter `site/src/content` without a matching review file and a matching manifest directory under `docs/content-pipeline/manifests/`.
