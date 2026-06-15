# Publishable Markdown contract

Use this after the review file reaches `draft-review-passed`. The generated Markdown and manifest remain draft staging artifacts until the quality gate marks the item `agent-cleared`.

## Required frontmatter by collection

Shared fields for every collection:

```yaml
title: "..."
description: "..."
date: "YYYY-MM-DD"
tags: ["..."]
visibility: "public"
```

Collection-specific required fields:

- `essays`: shared fields only. Optional: `canonical`, `series`.
- `notes`: `topic`.
- `logs`: `period`, `summary`.
- `links`: `url`, `category`, `note`.
- `projects`: `status`, `role`, `period`. Optional: `repo`, `demo`; do not invent public links.

Optional relation fields may be used when schema supports them, such as `related`.

## Staging layout

Use one directory per item:

```text
docs/content-pipeline/manifests/<slug>/
  manifest.json
  <slug>.md
```

The manifest file must be named exactly `manifest.json`. Item `file` paths are relative to that manifest directory and must not use `..`.

Example:

```json
{
  "items": [
    {
      "type": "essays",
      "file": "example-essay.md",
      "slug": "example-essay",
      "publish": true,
      "visibility": "public"
    }
  ]
}
```

## Commands

Manifest mode after `agent-cleared`:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site build
pnpm preview:prepare
```

Single-file mode:

```bash
pnpm --dir site content:check -- --file ../docs/content-pipeline/manifests/<slug>/<slug>.md --type essays --slug <slug>
```

Do not use single-file `content:sync` for public publishing unless a review file exists, the item is `agent-cleared`, and manifest mode is impossible for a documented reason.

Notes:

- Do not pass a bare positional path; scripts parse `--key value` arguments.
- Manifest mode always looks for `<input>/manifest.json`.
- Manifest item `file` is resolved inside the input directory; paths using `docs/...` or `../...` fail as unsafe.
- Add `--overwrite` only when replacing an existing target is explicitly intended and allowed.

## Limits

`content:check` catches metadata, empty body, unsafe slug, duplicate target, non-public visibility, some secrets, and explicit private/forbidden markers. It does not prove editorial quality. The review loop and editorial standard decide whether the piece deserves publication.
