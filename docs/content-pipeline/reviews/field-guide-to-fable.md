# Review: Fable 5 的用法：先找到未知

## Metadata

- status: publish-ready
- source paths / source records:
  - https://www.youtube.com/watch?v=9fubhllmsBU
  - out/video-field-guide-to-fable/metadata.json
  - out/video-field-guide-to-fable/transcript-dedup.txt
  - site/public/images/field-guide-to-fable/*.webp
- refreshed/primary sources:
  - https://www.youtube.com/watch?v=9fubhllmsBU
  - https://www.anthropic.com/news/claude-fable-5-mythos-5
  - https://www.anthropic.com/news/redeploying-fable-5
  - https://www.anthropic.com/research/tracing-thoughts-language-model
- proposed collection: essays
- proposed slug: field-guide-to-fable
- source type: link-derived
- target reader: 已经在用 coding agent / Claude Code 的工程师，知道 prompt、工具调用、代码库上下文这些概念，但未必看过 Fable 5 的发布材料。
- planned publishable markdown path: docs/content-pipeline/manifests/field-guide-to-fable/field-guide-to-fable.md
- planned manifest dir: docs/content-pipeline/manifests/field-guide-to-fable/

## Public thesis

- memorable sentence: Fable 5 这类模型把难点从“让模型会做事”推到“人能不能把真实任务里的未知先翻出来”。
- reader decision helped: 读者可以判断自己该怎么改 agent 工作流：少写死一堆规则，多做 blind spot pass、prototype、interview、reference、implementation notes 和 quiz。
- strongest counterpoint / edge case: “减少系统提示词”和“good fast cheap pick three”不是通用规则；没有验收、权限边界和回滚手段时，模型越强越容易把错误推进更远。

## Complete-story check (required for learning/practice-derived items)

The arc binds only stages whose material actually exists. Mark N/A (with reason) for absent stages; forcing an absent stage with tangential material is a blocker.

- [x] what the source (video/course/paper/tool) actually said is covered
- [x] source deep-dive completeness: full section-by-section coverage (mechanisms/arguments/numbers/examples), not an outline or intro
- [x] video/talk source is embedded as a playable video near the top
- [x] source key visuals (slides/diagrams/demo screens) embedded with source-credit captions, or N/A (no informative visuals)
- [x] what I actually practiced is concrete (steps/code/prompts/configs) — or N/A: no practice material, piece written as pure deep-dive
- [x] real results/data/outputs are included — or N/A with the practice stage
- [x] verified vs. untested claims are separated (for pure deep-dives: source claims the author cannot check are marked as the speaker's claims)
- [x] my own judgment is present and clearly separated from the source's content
- absent stages and why (recorded here, not padded in the article): No hands-on Fable 5 practice material was provided; article is a pure source deep-dive plus author judgment.

## Draft direction

Content brief:

- 一句话主张: 这支 talk 最重要的不是 Fable 5 有多强，而是模型变强后，人的瓶颈变成找未知、给参考、留在 loop 里。
- 读者带走: 一个可复用的 Fable/agent 工作流清单，以及哪些说法只能当 speaker claim，不能当已验证事实。
- 核心判断 -> 支撑材料:
  - 模型能力会“spiky”地出现，工具/harness 决定能不能触到能力。支撑: Pokemon 以 aw 结尾例子、Claude Code fetch + script、系统提示词删 80%、AskUserQuestion 能力演化。
  - Fable 5 的使用重点是让未知显形。支撑: map vs territory、unknown 四象限、blind spot pass、prototype、interview、reference、implementation notes、quiz。
  - 情绪上会有 gain 和 loss，但回退不是办法。支撑: 讲者回到旧创业项目，weeks -> hours，喜欢手写代码但 cannot go back。
  - “be unreasonable”应该理解为先要求全都要，再让现实证明取舍，而不是跳过验收。支撑: good fast cheap pick three、4 小时做 deck、building easier but value still hard。
- 缺口 / 待用户补: 没有用户自己的 Fable 5 实践结果；文中不写“我试了”。
- 非目标 / 不展开: 不写 Fable 5 完整产品评测；不展开安全政策细节；不复述所有官方 benchmark。
- 可视化判断: 需要视频关键帧。文章是 source deep-dive，source 自带 slides 承载结构、案例和数字；抽取 6 张 webp 并配 source-credit captions。

## Rewrite plan

### Keep

- 视频四段结构和每段核心例子。
- Fable 5 官方发布/恢复访问的日期背景。
- 讲者 claim 与作者 judgment 的边界。

### Remove / anonymize

- 不保留本地下载路径到公共正文。
- 不把自动字幕里可能误识别的产品名当事实写死。

### Add / refresh

- Anthropic 官方 Fable 5 发布、redeploy 页面。
- Anthropic interpretability 文章，作为视频里 “biology of a large language model” 提到的延伸来源。
- 视频关键帧。

## Links collection maintenance

For every external source cited in the article: promote core sources (the piece is built around them) to a `links` entry in the same manifest; batch examples and passing citations stay inline only.

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| https://www.youtube.com/watch?v=9fubhllmsBU | yes | promote | field-guide-to-fable-video |
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | no | inline-only | |
| https://www.anthropic.com/news/redeploying-fable-5 | no | inline-only | |
| https://www.anthropic.com/research/tracing-thoughts-language-model | no | inline-only | |

## Project/public evidence table

Use for projects or any claim about public work, shipped results, demos, repos, users, or external validation.

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| AI Engineer video title, speaker, upload metadata, transcript | yt-dlp metadata and transcript, YouTube URL | 2026-07-06 | yes | n/a |
| Fable 5 launch/redeploy timing and safeguards | Anthropic official pages | 2026-07-06 | yes | n/a |
| Speaker-specific capability examples | YouTube transcript | 2026-07-06 | yes as speaker claims | n/a |

## Required publishable frontmatter plan

Shared:

- title: Fable 5 的用法：先找到未知
- description: 解析 Thariq Shihipar 的 Field Guide to Fable：模型能力的 overhang、系统提示词为什么变短、unknown 四象限怎么用，以及为什么“be unreasonable”仍然离不开验收。
- date: 2026-07-06T10:10:00-07:00
- tags: ["agents", "claude-code", "fable-5", "video-notes"]
- visibility: public

Collection-specific:

- essays: canonical?, series? n/a
- notes: topic n/a
- logs: period, summary n/a
- links: url, category, note for promoted video entry
- projects: status, role, period, repo?, demo? n/a

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
| Thesis | 2 | Clear thesis around unknowns, not generic prompt tips. |
| Reader payoff | 2 | Gives a concrete working checklist. |
| Specificity | 2 | Uses video's concrete examples, timestamps, and slides. |
| Structure | 2 | Follows video order, then separates author judgment. |
| Source grounding | 2 | Video transcript plus official Anthropic pages. |
| Judgment density | 2 | Explicit boundaries and caveats. |
| Voice | 1 | Generic human Chinese; voice.md has no real samples. |
| Safety/privacy | 2 | No leaks in public prose planned. |
| Freshness | 2 | Checked official Anthropic pages on 2026-07-06. |

Total: 17/18

## Review loop

### Editor review

- reviewer: independent `codex exec -s read-only` reviewer (subagent tool unavailable under current runtime policy unless user explicitly requests subagents)
- pass: yes
- blockers: none
- major edits: none required
- minor edits: Title is accurate but plain; first section is dense; final judgment could carry more author texture.

### Source/factual review

- reviewer: independent `codex exec -s read-only` reviewer (subagent tool unavailable under current runtime policy unless user explicitly requests subagents)
- pass: yes
- blockers: none
- claims needing refresh/removal: tightened classifier/fallback wording; clarified AskUserQuestion as slide text; changed "unknown matrix" to "unknown 四象限".
- notes: Video metadata/transcript support the talk claims; Anthropic official pages support Fable 5 launch/redeploy/fallback/safeguards timing; staged public prose leak check found no local paths/private markers.

### Adversarial review

- reviewer: independent `codex exec -s read-only` reviewer (subagent tool unavailable under current runtime policy unless user explicitly requests subagents)
- pass: yes
- blockers: none
- non-blocking risks: YouTube key-frame screenshots have a small platform/copyright risk even with captions; "完整解析" is a strong promise but mostly earned.
- required revisions: none before agent-cleared

### Eval review (links/images, after build)

- reviewer: degraded self-check. Attempted independent `codex exec -s read-only` eval reviewer, but Codex usage limit blocked the run; ran the same mechanical URL/image checks locally and recorded the degradation.
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://code.claude.com/docs/en/best-practices | 200 | yes |
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | 200 | yes |
| https://www.anthropic.com/news/redeploying-fable-5 | 200 | yes |
| https://www.anthropic.com/research/tracing-thoughts-language-model | 200 | yes |
| https://www.youtube.com/watch?v=9fubhllmsBU | 200 | yes |
| https://www.youtube-nocookie.com/embed/9fubhllmsBU?autoplay=1&rel=0 | 200 | yes |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| https://i.ytimg.com/vi/9fubhllmsBU/hqdefault.jpg | 200 image/jpeg | yes |
| /my-blog/images/field-guide-to-fable/01-field-guide.webp | site/dist/images/field-guide-to-fable/01-field-guide.webp (52782 bytes) | yes |
| /my-blog/images/field-guide-to-fable/02-pokemon-overhang.webp | site/dist/images/field-guide-to-fable/02-pokemon-overhang.webp (57728 bytes) | yes |
| /my-blog/images/field-guide-to-fable/03-system-prompt.webp | site/dist/images/field-guide-to-fable/03-system-prompt.webp (51274 bytes) | yes |
| /my-blog/images/field-guide-to-fable/04-ask-user-question.webp | site/dist/images/field-guide-to-fable/04-ask-user-question.webp (49632 bytes) | yes |
| /my-blog/images/field-guide-to-fable/05-blindspot-pass.webp | site/dist/images/field-guide-to-fable/05-blindspot-pass.webp (63054 bytes) | yes |
| /my-blog/images/field-guide-to-fable/06-pick-three.webp | site/dist/images/field-guide-to-fable/06-pick-three.webp (44308 bytes) | yes |

- rendered check run: yes, via `pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/field-guide-to-fable/`
- broken items and fixes: none

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| source/factual: classifier wording over-implied all related requests trigger fallback | changed to "被 classifiers 判定为涉及 ... 的请求会由 Opus 4.8 接手" | yes |
| source/factual: exact AskUserQuestion name not in transcript | clarified it is shown on the video slide | yes |
| source/factual: "unknown matrix" sounded formal | changed public prose/metadata/review plan to "unknown 四象限" | yes |
| human request: video should be embedded in the article | added the bare YouTube URL near the top so `rehype-video-embed` renders a playable embed; reran build and UI verification | yes |

## Agent review

```yaml
agent_review:
  status: publish-ready
  reviewer: agent
  date: 2026-07-06
  notes: "Writing check hard hits 0; independent writing review PASS 3.82/5; publisher editor/source/adversarial reviews all pass via independent codex exec read-only; content:check/content:sync/build/preview:prepare pass; link/image eval passes via degraded local check after codex usage limit blocked eval reviewer; playable YouTube embed added and verified in built HTML; ui-verify and ci:sanity pass."
```

## Final human blog review

Human review happens on local preview before publish/deploy, unless the user explicitly requested immediate publishing. If the human finds problems, mark `needs-rework`, remove/revert synced public-source content, and open a follow-up返工 session.

```yaml
human_blog_review:
  status: explicit-publish-request
  reviewer: human
  date: 2026-07-06
  notes: "User requested the video be embedded, then explicitly requested publish."
```

## Mechanical verification notes

- content:check: `pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/field-guide-to-fable` -> ok true, checked 2, errors 0, warnings 0
- content:sync: `pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/field-guide-to-fable` -> wrote `site/src/content/essays/field-guide-to-fable.md` and `site/src/content/links/field-guide-to-fable-video.md`
- build: `pnpm --dir site build` -> passed, 24 pages built; existing notes collection warning remains
- preview URL: http://127.0.0.1:4328/my-blog/essays/field-guide-to-fable/ (curl 200; 4327 also returned 200 but 4328 recorded for review)
- ui-verify if run: `pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/field-guide-to-fable/` -> OK true; 375/768/1440 axe 0, console errors 0, console warnings 0, overflow no; Lighthouse 93/100/100/100
- post-embed verification: generated HTML contains `.video-embed` with `data-provider="youtube"`, `youtube-nocookie` embed URL returned 200, thumbnail returned 200 image/jpeg
- ci:sanity: `pnpm ci:sanity` -> ok true; warnings: existing logs page standard-empty-message warning
- leak check: staged markdown + synced source + generated HTML passed (no /Users, kb-vault, docs/content-pipeline, private/confidential/forbidden markers)
- rejection cleanup if needed: n/a
