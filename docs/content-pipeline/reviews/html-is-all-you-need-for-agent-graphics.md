# Review: HTML 是 agent 做视觉内容的中间表示

## Metadata

- status: preview-ready
- source paths / source records:
  - https://www.youtube.com/watch?v=JRTAtZ5iBkU
  - YouTube metadata and auto captions fetched locally with `yt-dlp` on 2026-07-03
  - Video frames extracted from the same YouTube video on 2026-07-03
- refreshed/primary sources:
  - https://www.youtube.com/watch?v=JRTAtZ5iBkU
- proposed collection: essays
- proposed slug: html-is-all-you-need-for-agent-graphics
- source type: link-derived
- target reader: 做博客、slides、解释型视频或 agent 内容工具的人
- planned publishable markdown path: docs/content-pipeline/manifests/html-is-all-you-need-for-agent-graphics/html-is-all-you-need-for-agent-graphics.md
- planned manifest dir: docs/content-pipeline/manifests/html-is-all-you-need-for-agent-graphics/

## Public thesis

- memorable sentence: 对 agent 来说,HTML/CSS 不是网页格式,而是一种可验证、可渲染、可迭代的视觉中间表示。
- reader decision helped: 如果想让 AI 生成 slides/docs/videos,先选 HTML/React/Remotion 这类结构化媒介,不要从 Figma/PowerPoint 自动操作或手写 SVG 坐标开始。
- strongest counterpoint / edge case: HTML 解决的是视觉结构和渲染接口,不是脚本、叙事、配音、节奏、审美和最终验收;复杂动画仍需要时间轴和视觉回归。

## Complete-story check (required for learning/practice-derived items)

- [x] what the source (video/course/paper/tool) actually said is covered
- [x] source deep-dive completeness: full section-by-section coverage (mechanisms/arguments/numbers/examples), not an outline or intro
- [x] source key visuals (slides/diagrams/demo screens) embedded with source-credit captions, or N/A (no informative visuals)
- [x] what I actually practiced is concrete (steps/code/prompts/configs) — or N/A: no practice material, piece written as pure deep-dive
- [x] real results/data/outputs are included — or N/A with the practice stage
- [x] verified vs. untested claims are separated (for pure deep-dives: source claims the author cannot check are marked as the speaker's claims)
- [x] my own judgment is present and clearly separated from the source's content
- absent stages and why (recorded here, not padded in the article): no implementation practice has happened yet; this is a pure source deep-dive plus project direction note. The follow-up implementation plan is captured separately in KB.

## Draft direction

Write as a source deep-dive first: what Amol Kapoor argues, why Figma/PowerPoint/SVG are bad native interfaces for agents, why HTML/CSS is better, and what is actually shown about the video's own production. End with the author's judgment and a concrete implementation path for a future prototype without claiming it exists.

## Rewrite plan

### Keep

- Section-by-section talk summary.
- Clear separation between speaker claims and author's judgment.
- Mention that the "this video is HTML/CSS" claim is not independently audited.

### Remove / anonymize

- Local filesystem paths and command logs.
- Any claim that we already built the follow-up video system.

### Add / refresh

- Five credited video frames.
- Links collection entry for the source video.
- Implementation-oriented judgment section.

## Links collection maintenance

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| https://www.youtube.com/watch?v=JRTAtZ5iBkU | yes | promote | html-is-all-you-need-for-agent-graphics-video |

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| Video title, channel, duration, description, upload date | YouTube metadata via `yt-dlp` | 2026-07-03 | yes | no |
| Speaker says the video itself is made from HTML/CSS | YouTube auto captions | 2026-07-03 | yes as speaker claim | no |
| We have built a similar system | none | 2026-07-03 | no | yes, framed as future project only |

## Required publishable frontmatter plan

Shared:

- title: "HTML 不是网页,是 agent 的视觉中间表示"
- description: "解析 AI Engineer talk:为什么 agent 做图不该从 Figma、PowerPoint 或手写 SVG 开始,而应该先把 slides、docs、videos 变成 HTML/CSS 可以渲染和验证的结构。"
- date: "2026-07-03"
- tags: ["agents", "video-notes", "html", "generative-ui"]
- visibility: public

Collection-specific:

- essays: canonical?, series?

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.
- [x] Benchmark/metric claims refreshed or removed.
- [x] Security claims phrased defensively and without operational attack detail.
- [x] Hypothetical examples labeled as hypothetical.
- [x] Public links/repo/demo/result claims verified.

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [x] Internal KB/local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | sharp central claim around intermediate representation |
| Reader payoff | 2 | helps choose production medium for AI visual content |
| Specificity | 2 | covers slides/docs/video, SVG, canvas tools, HTML/CSS |
| Structure | 2 | source first, judgment second, implementation direction last |
| Source grounding | 2 | primary video and captions, credited frames |
| Judgment density | 2 | includes limits and practical path |
| Voice | 2 | concise public essay voice |
| Safety/privacy | 2 | no local paths in public prose |
| Freshness | 2 | video checked on task date |

Total: 18/18

## Review loop

### Editor review

- reviewer: agent (degraded from subagent because current runtime policy only permits spawning subagents on explicit user request)
- pass: yes
- blockers: none
- major edits: tightened title around "intermediate representation"; made source and commentary sections distinct.
- minor edits: kept "HTML is all you need" as a useful slogan but softened literal interpretation.

### Source/factual review

- reviewer: agent (degraded from subagent because current runtime policy only permits spawning subagents on explicit user request)
- pass: yes
- blockers: none
- claims needing refresh/removal: no external model/vendor claims beyond the primary video; "video made from HTML/CSS" framed as speaker claim, not independently audited fact.
- notes: YouTube auto captions are sufficient for this source deep-dive; no long verbatim transcript is reproduced.

### Adversarial review

- reviewer: agent (degraded from subagent because current runtime policy only permits spawning subagents on explicit user request)
- pass: yes
- blockers: none
- non-blocking risks: the article may make HTML sound too sufficient; mitigated by explicitly naming missing pipeline pieces.
- required revisions: added "not all you need" boundary and future-project framing.

### Eval review (links/images, after build)

- reviewer: agent (degraded from subagent because current runtime policy only permits spawning subagents on explicit user request)
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://www.youtube.com/watch?v=JRTAtZ5iBkU | 200 | yes |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| /my-blog/images/html-is-all-you-need-for-agent-graphics/01-deck-fiddling.webp | non-empty in site/dist and out/ui-serve | yes |
| /my-blog/images/html-is-all-you-need-for-agent-graphics/02-human-canvas-tools.webp | non-empty in site/dist and out/ui-serve | yes |
| /my-blog/images/html-is-all-you-need-for-agent-graphics/03-pelican-svg-test.webp | non-empty in site/dist and out/ui-serve | yes |
| /my-blog/images/html-is-all-you-need-for-agent-graphics/04-html-structure.webp | non-empty in site/dist and out/ui-serve | yes |
| /my-blog/images/html-is-all-you-need-for-agent-graphics/05-html-css-video.webp | non-empty in site/dist and out/ui-serve | yes |

- rendered check run: yes (`pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/html-is-all-you-need-for-agent-graphics/`)
- broken items and fixes: none

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Runtime policy prevented independent subagent reviews | Ran separate role reviews locally and disclosed degradation | yes |
| Future implementation not yet built | Kept article as source deep-dive; captured future plan separately in KB | yes |

## Agent review

```yaml
agent_review:
  status: preview-ready
  reviewer: agent
  date: 2026-07-03
  notes: Source review, staged markdown, manifest, role reviews, content checks, build, UI verification, link/image eval, and leak check passed; ready for human preview.
```

## Final human blog review

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Mechanical verification notes

- content:check: pass (`pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/html-is-all-you-need-for-agent-graphics --overwrite`)
- content:sync: pass (`pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/html-is-all-you-need-for-agent-graphics --overwrite`)
- build: pass (`pnpm --dir site build`, 21 pages built)
- preview URL: http://127.0.0.1:4328/my-blog/essays/html-is-all-you-need-for-agent-graphics/ (4327 was occupied; 4328 returned HTTP 200)
- ui-verify if run: pass; axe 0 at 375/768/1440, console errors 0, console warnings 0, overflow no, Lighthouse 99/100/100/100; summary in `out/summary.json`
- leak check: pass; no matches for local paths, KB paths, pipeline paths, private/confidential markers, or forbidden-publish markers in staged markdown, synced source, and generated HTML
- rejection cleanup if needed: pending
