---
name: ui-verify
description: Run the project's fixed UI self-verification loop after any front-end/UI change to an Astro page, layout, component, or style. Captures multi-breakpoint screenshots (with prefers-reduced-motion + frozen animations), runs axe-core accessibility scan, and a Lighthouse performance/SEO/a11y audit, then writes out/summary.json. Use when changing UI/styles/layout, building the site, or asked to verify/check the UI. Local-only; never part of deploy CI.
---

# UI 自验证(⑥)

固定、可重复、低 token 的 UI 验证回路。脚本做客观判定(截图/axe/lighthouse),**截图留给 ⑦ human 看,审美主观判断不在这里做**。与 Claude Code 的 `.claude/skills/ui-verify` 共用同一个脚本 `scripts/ui-verify.mjs`;规范见 `CONVENTIONS.md`「UI 自验证回路」、`DECISIONS.md` 的 `D-20260614-UI验证工具链`。

## 怎么跑

从仓库根运行(首次需 `pnpm install` 装好 devDependencies):

1. **Astro 新站已脚手架时**:先构建静态产物,再对 `dist/` 跑:
   ```
   npx astro build           # 在 site/ 内,产出 dist/
   pnpm ui-verify -- --serve <dist 路径> --path /
   ```
2. **临时对任意静态目录 / 已起服务**:
   ```
   pnpm ui-verify -- --serve <静态目录> --path /some.html
   pnpm ui-verify -- --url http://localhost:4321 --path /
   ```
   可选 `--breakpoints 375,768,1440`(默认即此)。

## 跑完后

1. 读 `out/summary.json`。
2. 汇报:lighthouse 各项分数、各断点 axe violations 计数(critical/serious 优先)与前几条规则、console 错误数、截图路径。
3. **不要把截图逐张读进上下文**;只汇报客观信号,截图路径列出留给 human 在 ⑦ 验收时看。
4. 判定:`summary.ok=false` 或出现 axe critical/serious、lighthouse 某项 <80、console error → 按 `AGENTS.md` 回退到上一个干净点重做,不在错误实现上打补丁。

## 边界

- 仅本地;**不进 ⑧ 部署 CI**(`withastro/action`),保护冻结期发布链路。
- 动效「克制度 / 审美是否够好」这类主观判断脚本判不了 → 交给 ⑦ human,或临时用 Playwright MCP 手动探查(仅作探索辅助,不进固定回路)。
