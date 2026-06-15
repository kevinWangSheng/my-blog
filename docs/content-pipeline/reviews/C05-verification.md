# C05 verification — related content recommendations

Date: 2026-06-15

## Scope

Implemented lightweight related-content recommendations for detail pages:

- `site/src/lib/content.ts`: recommendation scoring and target collection logic.
- `site/src/components/DetailPage.astro`: renders a quiet "Next reading path" section when related entries exist.
- `site/src/pages/{essays,notes,logs,projects}/[slug].astro`: passes recommendations into detail pages.
- `site/src/styles/global.css`: responsive related-card styling.

## Recommendation basis

Priority and fallback logic:

1. Same `series` when present.
2. Explicit `related` frontmatter in either direction when present.
3. Shared tags.
4. Same collection recent entries.
5. Collection-specific target pools:
   - essays: essays, notes, links
   - notes: notes, essays, links
   - logs: logs, notes, essays
   - projects: projects, notes, logs

Links are allowed as external recommendations; other collections use internal routes.

## Commands run

```bash
pnpm --dir site build
pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/rag-as-evidence-chain/
```

`out/ui-serve/my-blog` is a temporary symlink to `site/dist` used only so local verification matches the deployed GitHub Pages base path `/my-blog/`.

## Verification results

- `pnpm --dir site build`: passed; generated 22 pages.
- Recommendation HTML checks:
  - `site/dist/essays/rag-as-evidence-chain/index.html`: 4 `related-card` entries.
  - `site/dist/notes/retrieval-eval-before-answer-eval/index.html`: 4 `related-card` entries.
  - `site/dist/logs/2026-week-24/index.html`: 4 `related-card` entries.
  - `site/dist/projects/agent-learning-cockpit/index.html`: 4 `related-card` entries.
- UI verify target: `http://127.0.0.1:<port>/my-blog/essays/rag-as-evidence-chain/`.
- UI verify summary from `out/summary.json`:
  - 375 / 768 / 1440 screenshots written to `out/screen-*.png`.
  - axe violations: 0 total, 0 critical, 0 serious at all breakpoints.
  - console errors/warnings: 0 at all breakpoints.
  - horizontal overflow: no at all breakpoints.
  - Lighthouse: performance 100, accessibility 100, best-practices 100, SEO 100.

## Conclusion

C05 acceptance is satisfied: detail pages expose 2-4 meaningful next-step entries, build passes, and local UI verification passes without accessibility, console, overflow, or Lighthouse blockers.
