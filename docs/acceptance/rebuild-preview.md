# Rebuild preview — ⑦ human acceptance packet

## Current status

返工队列 T13 → T14 → T18 → T15 → T16 → T17 已完成双层验收。已在 human ⑦验收通过后发布到 GitHub Pages。旧 Hugo/Notion 管线已从当前项目移除,当前 CI/CD 只构建 Astro `site/dist` 并发布到 `gh-pages`。

## Local preview

```bash
pnpm --dir site build
pnpm --dir site preview -- --host 127.0.0.1 --port 4321
```

Open: `http://127.0.0.1:4321/`

## Suggested review path

1. `/` — 首页:检查首屏是否清楚、清爽宁静、Projects/能力证据 与 Essays/学习判断两条路径是否明显。
2. `/projects` → `/projects/agent-learning-cockpit` — 检查作品/能力入口是否可信,是否说明 role/period/status/repo-demo 状态/问题/方案/过程证据/下一步。
3. `/about` — 检查 30 秒内是否知道 Shawn 当前方向、代表项目、阅读路径和 GitHub/RSS 入口。
4. `/essays` → `/essays/learning-in-the-agent-era` — 检查长文阅读舒适度、Markdown 渲染和文字节奏。
5. `/notes`、`/logs`、`/links`、`/rss.xml` — 检查内容密度、类型差异、RSS 和来源货架。

## Verification evidence

Ignored local evidence lives under `out/acceptance/`:

- T13 basic blog flow: `T13-main.md`, `T13-adversarial.md`, `T13-route-check.json`.
- T14 content density: `T14-main.md`, `T14-adversarial.md`, `T14-density.json`, `T14-rss-check.json`, `T14-content-safety.json`.
- T18 visitor/project proof path: `T18-main.md`, `T18-adversarial.md`, `T18-visitor-paths.json`.
- T15 visual direction: `T15-main.md`, `T15-adversarial.md`, `T15-style-check.json`.
- T16 scroll reveal: `T16-main.md`, `T16-adversarial.md`, `T16-reveal-check.json`.
- T17 final acceptance: `T17-main.md`, `T17-adversarial.md`, `T17-human-preview.md`.

Final UI summaries:

- `out/acceptance/T17-ui-home-summary.json`
- `out/acceptance/T17-ui-about-summary.json`
- `out/acceptance/T17-ui-project-summary.json`
- `out/acceptance/T17-ui-essay-summary.json`

All four final UI summaries report: Lighthouse performance/accessibility/best-practices/SEO = 100/100/100/100, axe critical/serious = 0, console warnings/errors = 0, horizontal overflow = no at 375/768/1440.

## Known limits before acceptance

- 内容仍是第一版 sample / draft / existing-material-summary,可在 ⑦ 前由 human 判断是否需要替换为更真实公开材料。
- GitHub 是当前唯一公开外部入口;更多联系方式需要 human 明确后再加入。
- UI 自验证只在本地 ⑥ 跑,不加入部署 CI。
- 当前部署链路见 `docs/deployment.md`。


## Live URL

- https://kevinwangsheng.github.io/my-blog/
- RSS: https://kevinwangsheng.github.io/my-blog/rss.xml
- Sitemap: https://kevinwangsheng.github.io/my-blog/sitemap.xml

## Deployment evidence

- GitHub Actions run `27522304477` completed successfully.
- Live checks returned HTTP 200 for home, Projects, project detail, About, essay detail, RSS, and sitemap.
