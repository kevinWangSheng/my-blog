# Content pipeline manifests

Each subdirectory here is a staging package for content that has already passed the review layer.

Required layout:

```text
docs/content-pipeline/manifests/<slug>/
  manifest.json
  <slug>.md
```

Run from the repository root:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site build
```

`manifest.json` item `file` paths must stay relative to the staging directory and must not contain `..`.
