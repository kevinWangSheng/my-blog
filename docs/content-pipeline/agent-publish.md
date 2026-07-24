# Agent publishing entrypoint

Current publishing skill: `.agents/skills/blog-publisher/` (`$blog-publisher`).

Use it for any public blog content, whether the source is KB material, a draft, research output, a link, a log, or a project record.

## Required gate

No content should be synced into `site/src/content` unless it has:

1. `docs/content-pipeline/reviews/<slug>.md` with source tracing, public thesis, and editorial quality score;
2. status progression through `draft` -> `draft-review-passed` -> `agent-cleared`;
3. editor/source/adversarial review passes recorded, each run by an independent subagent (or an explicitly disclosed degraded self-review);
4. no unresolved blockers;
5. `docs/content-pipeline/manifests/<slug>/manifest.json` and publishable Markdown;
6. `content:check`, `content:sync`, and `pnpm --dir site build` evidence after agent clearance;
7. a link/image eval by a separate subagent after build (every external link 2xx/3xx, every internal link and image resolves in `site/dist`), with per-URL/per-image results in the review file — required before `preview-ready`.

If human preview rejects the content, mark it `needs-rework` and remove/revert generated `site/src/content/*/<slug>.md` files.

Publishing to GitHub Pages still requires an explicit human request after preview/review.
