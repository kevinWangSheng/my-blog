# Publishable Markdown contract

Use this reference only after a review-ready draft exists and the user explicitly asks to prepare approved content for sync.

## Important boundary

The review file is not publishable input. It is an editorial/audit artifact. `content:check` and `content:sync` require a separate Markdown article file with valid frontmatter and non-empty public body.

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

## Recommended staging layout

Use one directory per approved item:

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
      "file": "rag-is-not-dead-context-engineering.md",
      "slug": "rag-is-not-dead-context-engineering",
      "publish": true,
      "visibility": "public"
    }
  ]
}
```

## Real commands

Single-file mode:

```bash
pnpm --dir site content:check -- --file ../docs/content-pipeline/manifests/<slug>/<slug>.md --type essays --slug <slug>
pnpm --dir site content:sync -- --file ../docs/content-pipeline/manifests/<slug>/<slug>.md --type essays --slug <slug>
```

Manifest mode:

```bash
pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/<slug>
pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/<slug>
```

Notes:

- Do not pass a bare positional path; the scripts only parse `--key value` arguments.
- Manifest mode always looks for `<input>/manifest.json`.
- Manifest item `file` is resolved inside the input directory; `docs/...` or `../...` paths will fail as unsafe.
- Add `--overwrite` only when replacing an existing target is explicitly intended and allowed by the current task.

## Mechanism limits

`content:check` catches required fields, empty body, unsafe slug, duplicate target, non-public visibility, some secrets, and explicit private/forbidden markers. It does not prove:

- public quality
- factual freshness
- absence of all private personal information
- absence of fabricated achievements or endorsement
- removal of mentor/internal learning tone

Those remain review/adversarial responsibilities of `$kb-to-blog`.
