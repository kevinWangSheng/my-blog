# C07 verification — sandbox content batch

Date: 2026-06-15
Status: agent-verified-local-preview

## Scope

Added a narrow public content batch around the theme: agent sandbox as execution boundary, not a magic safety switch.

Synced items:

- essay: `sandbox-is-execution-boundary`
- note: `sandbox-protects-host-not-secrets`
- note: `microvm-when-untrusted-code`
- link: `openai-sandbox-agents`

## Commands run

```bash
for slug in sandbox-is-execution-boundary sandbox-protects-host-not-secrets microvm-when-untrusted-code openai-sandbox-agents; do
  pnpm --dir site content:check -- --input "../docs/content-pipeline/manifests/$slug"
  pnpm --dir site content:sync -- --input "../docs/content-pipeline/manifests/$slug"
done
pnpm --dir site build
pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/sandbox-is-execution-boundary/
```

## Evidence

- `content:check`: all 4 manifest directories returned `ok: true` with no warnings.
- `content:sync`: wrote all 4 target files under `site/src/content/` with no warnings.
- `pnpm --dir site build`: passed; Astro generated 23 pages, including:
  - `/essays/sandbox-is-execution-boundary/index.html`
  - `/notes/sandbox-protects-host-not-secrets/index.html`
  - `/notes/microvm-when-untrusted-code/index.html`
  - `/links/index.html`
  - `/rss.xml`
- Route content check:
  - essay html contains `Agent sandbox 是执行边界`
  - note html contains `Sandbox 保护 host`
  - note html contains `什么时候需要 microVM`
  - links page contains `OpenAI Sandbox Agents`
  - RSS contains `sandbox-is-execution-boundary`
- Local path leak check:
  - no matches for `/Users/shenghuikevin/kb-vault` or `docs/content-pipeline` in the new public source/html files checked.
- UI verification for `/my-blog/essays/sandbox-is-execution-boundary/`:
  - 375px: axe 0, critical 0, serious 0, console errors 0, overflow no
  - 768px: axe 0, critical 0, serious 0, console errors 0, overflow no
  - 1440px: axe 0, critical 0, serious 0, console errors 0, overflow no
  - Lighthouse: performance 100, accessibility 100, best-practices 100, SEO 100
  - summary: `out/summary.json`
  - screenshots: `out/screen-375.png`, `out/screen-768.png`, `out/screen-1440.png`

## Human review entry

Local preview is served at:

- `http://127.0.0.1:4327/my-blog/`
- `http://127.0.0.1:4327/my-blog/essays/sandbox-is-execution-boundary/`
- `http://127.0.0.1:4327/my-blog/notes/sandbox-protects-host-not-secrets/`
- `http://127.0.0.1:4327/my-blog/notes/microvm-when-untrusted-code/`
- `http://127.0.0.1:4327/my-blog/links/`

## Boundary

Not pushed, not deployed, not cut over to production.
