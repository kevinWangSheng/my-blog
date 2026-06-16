# Deployment and CI/CD

## Current model

The only active site implementation is the Astro project under `site/`.

- Source: `site/`
- Build output: `site/dist`
- Production branch: `gh-pages`
- Live URL: `https://kevinwangsheng.github.io/my-blog/`
- Package manager: `pnpm`
- Node version in CI: `22`

The old Notion to Hugo pipeline is retired. Do not restore `.gitmodules`, root-level `assets/`, `content/`, `themes/`, `resources/`, `public/`, `.hugo_build.lock`, `config.yaml`, or `scripts/notion-sync.py` as active project files.

## Workflows

### CI

`.github/workflows/ci.yml` runs on pull requests, pushes to `main`, and manual dispatch.

It runs:

```bash
pnpm install --frozen-lockfile
pnpm --dir site build
pnpm ci:sanity
```

CI proves that the submitted Astro site builds and that the generated public output passes mechanical checks. It does not publish the site.

### Deploy

`.github/workflows/deploy.yml` runs after the `CI` workflow succeeds on `main`, and can also be started manually.

It rebuilds and sanity-checks the same commit, uploads `site/dist` as an artifact, then a separate publish job with write permission publishes that artifact to `gh-pages`.

Deploy intentionally does not run local UI verification. The heavier UI loop remains local-only:

```bash
pnpm --dir site build
pnpm preview:prepare
pnpm ui-verify -- --serve out/ui-serve --path /my-blog/
```

## Content boundary

CI/CD does not pull from Notion, KB, research folders, or any external content source.

Content enters the public site through the project publishing flow:

1. Source tracing and rewrite with `blog-publisher`.
2. Review file under `docs/content-pipeline/reviews/`.
3. Publishable Markdown plus `manifest.json`.
4. `pnpm --dir site content:check -- --input <manifest-dir>`.
5. `pnpm --dir site content:sync -- --input <manifest-dir>`.
6. Build, route checks, and local preview or UI verification as needed.

Human review happens on the rendered blog/result. If the published page is wrong, open a follow-up rework task rather than bypassing the content pipeline.

## Sanity checks

`pnpm ci:sanity` checks the generated `site/dist` plus repository structure for:

- retired Hugo/Notion paths;
- workflow references to the retired pipeline;
- missing RSS or sitemap;
- draft/private content generated publicly;
- private local paths such as `/Users/`, `kb-vault`, or `docs/content-pipeline`;
- old build-test log routes and tool-source filler entries;
- presence of the empty `/logs/` section route.

These checks are mechanical gates. They do not replace editorial review, source freshness checks, or local UI verification.
