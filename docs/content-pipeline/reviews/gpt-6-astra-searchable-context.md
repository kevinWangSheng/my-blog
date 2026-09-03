# Review: GPT-6 让 Codex 能搜索被挤出窗口的历史

## Metadata

- status: published
- source paths / source records:
  - /Users/shenghuikevin/dev/AI/report/research/gpt-6-astra-primary-sources.md
  - /Users/shenghuikevin/dev/AI/report/research/gpt-6-astra-community-signals.md
  - /Users/shenghuikevin/dev/AI/report/research/sources/claude-fable-5.1-mythos-5.1-system-card.pdf
  - /Users/shenghuikevin/.agent/diagrams/gpt-6-astra-context-management-research.html
- refreshed/primary sources:
  - https://openai.com/index/gpt-6-astra/
  - https://developers.openai.com/api/docs/models/gpt-6-astra
  - https://developers.openai.com/api/docs/guides/latest-model
  - https://learn.chatgpt.com/docs/config-file/config-reference
  - https://deploymentsafety.openai.com/gpt-6-astra
  - https://platform.claude.com/docs/en/models/fable-5-1/overview
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
  - https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20%26%20Claude%20Mythos%205.1%20System%20Card.pdf
- proposed collection: essays
- proposed slug: gpt-6-astra-searchable-context
- source type: research-derived
- target reader: 已经使用 Codex、Claude Code 或其他 coding agent，理解 token、context window、compaction 和 tool calling，正在判断 Astra 是否值得切换或启用实验功能的工程师。
- planned publishable markdown path: docs/content-pipeline/manifests/gpt-6-astra-searchable-context/gpt-6-astra-searchable-context.md
- planned manifest dir: docs/content-pipeline/manifests/gpt-6-astra-searchable-context/

## Public thesis

- memorable sentence: 长任务的关键正在从「能塞多少」转向「被挤出窗口的信息还能不能找回来」；Astra 在 Codex 里的新意，是让 compaction 从唯一真相变成 notes 加可回查历史。
- reader decision helped: 判断该把 Astra 当作更大模型、长任务运行时升级，还是仍需自建外部状态；决定是否启用实验功能，以及怎样设计一组能真正验证它的多窗口 A/B。
- strongest counterpoint / edge case: 检索会引入自己的召回、排序、过期和隐私问题；官方还没有发布隔离这项 context management 的独立 A/B。Fable 5.1 的 1M context、正式 compaction 和更便宜 cache read，也可能在具体负载里更划算。

## Complete-story check (required for learning/practice-derived items)

- [x] what the source (video/course/paper/tool) actually said is covered
- [x] source coverage completeness: this is a multi-source research synthesis focused on one mechanism, not a section-by-section deep-dive of the launch page or System Card; mechanism, API envelope, safety guardrails, Fable counterpoint and untested boundaries are covered
- [x] video/talk source is embedded as a playable video near the top, or N/A: no video/talk is the primary source
- [x] source key visuals embedded with source-credit captions, or N/A: the official pages use benchmark visuals, but the article's core mechanism is better served by an original explanatory SVG derived from the official text; no vendor image is copied
- [x] what I actually practiced is concrete, or N/A: no Astra account/runtime test was performed; the article is a multi-source mechanism analysis and says so explicitly
- [x] real results/data/outputs are included, or N/A with the practice stage: the official config, model envelope and System Card evidence are included with provenance; local CLI state, launch-day community reactions and unrun A/B results are not presented as public evidence
- [x] verified vs. untested claims are separated
- [x] my own judgment is present and clearly separated from source claims
- absent stages and why: no hands-on Astra run because the account rollout was not verified and the user asked to publish the research, not to change local model/config or spend API credits.

## Draft direction

- type: 深度解析 / explainer
- voice: `blog-writing-specialist/references/voice.md` is still mostly placeholders, so use clean first-person Chinese; no em dashes, almost no exclamation marks, no hype, no invented personal experience.
- progression: compaction loss -> notes plus searchable history -> where the feature can and cannot matter -> compact Fable counterpoint -> falsifiable multi-window A/B with model-level safety guardrails.
- public payoff: readers should leave with a system boundary and a test protocol, not a benchmark winner.

### Private source coverage ledger

| source theme | mechanism / evidence | planned article location | handling |
|---|---|---|---|
| identity and product naming | GPT-6 Astra; API `gpt-6-astra`; ChatGPT display GPT-6 Pro | title and opening | keep only GPT-6 Astra; omit API/display-name taxonomy because it does not change the mechanism |
| model envelope | 1.05M context, 128K output, $10/$50, >272K pricing tier | three-layer model and comparison | keep only decision-relevant fields |
| Codex context management | notes across windows, searchable earlier windows, config flag off by default | core mechanism | keep in full with config snippet and diagram |
| API agent features | async tools, mid-turn steering, reasoning updates, instruction sensitivity | none | omit; not needed to explain searchable history |
| System Card | Critical cyber, lower severity flags in 54K sim, monitorability regression, safety interruptions | A/B design | keep only to justify recording overreach and false stops; explicitly say model-level evidence does not predict the context-management treatment effect |
| benchmark profile | AutomationBench, DeepSWE, TB4, HLE, AA index | none | omit; none isolates searchable context |
| Fable 5.1 | 1M/128K, same base price, $0.25 cache read, compaction, no official equivalent old-window search found | compact comparison | keep short and link to existing Fable essay |
| X / Reddit | AA, Dan Shipper, Kieran, two Reddit threads | none | omit from blog; retain in the standalone research report because launch-day anecdotes do not isolate the mechanism |
| rollout quotas and every customer quote | fast-moving and secondary to thesis | none | omit |
| detailed exploit benchmark instructions | security relevance but unnecessary operational detail | none | omit; defensive framing only |

## Rewrite plan

### Keep

- The distinction between model context, Codex single-task context management and cross-session Memories.
- Exact configuration key from the official reference.
- System Card monitorability and interruption evidence only as guardrails for the proposed A/B.
- A small Fable comparison rather than a second full Fable review.

### Remove / anonymize

- All local paths and internal workflow details from public prose.
- Raw research log language and tool outputs.
- Unconfirmed Aeon/persistent-mode leaks.
- Dynamic X/Reddit engagement counts.

### Add / refresh

- Original SVG showing recursive-summary compaction versus notes plus searchable windows.
- Internal link to the already-published Fable 5.1 article.
- A reproducible multi-window A/B checklist.

## Links collection maintenance

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| https://openai.com/index/gpt-6-astra/ | research only | not cited / omitted because automated GET returns 403 | |
| https://developers.openai.com/api/docs/models/gpt-6-astra | no | inline-only | |
| https://developers.openai.com/api/docs/guides/latest-model | no | not cited / omitted | |
| https://learn.chatgpt.com/docs/config-file/config-reference | yes | promote | codex-searchable-context-config |
| https://deploymentsafety.openai.com/gpt-6-astra | yes | promote | gpt-6-astra-system-card |
| https://platform.claude.com/docs/en/models/fable-5-1/overview | no | inline-only | |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | no | already-exists | prompting-claude-fable-5-1 |
| https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | no | inline-only | |
| https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20%26%20Claude%20Mythos%205.1%20System%20Card.pdf | research only | not cited / omitted | |
| https://artificialanalysis.ai/methodology | research only | not cited / omitted | |
| https://x.com/ArtificialAnlys/status/2095595489031000350 | research only | not cited / omitted | |
| https://x.com/danshipper/status/2095593705214300394 | research only | not cited / omitted | |
| https://x.com/kieranklaassen/status/2095594035033563178 | research only | not cited / omitted | |
| https://www.reddit.com/r/codex/comments/1w6jf62/tldr_what_we_actually_know_about_gpt6_astra_after/ | research only | not cited / omitted | |
| https://www.reddit.com/r/codex/comments/1w6jh9e/astra_is_good_but_maybe_we_should_calm_down_with_the_hype/ | research only | not cited / omitted | |

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| GPT-6 Astra model envelope | https://developers.openai.com/api/docs/models/gpt-6-astra | 2026-09-03 | yes | n/a |
| config key is documented and off by default | https://learn.chatgpt.com/docs/config-file/config-reference | 2026-09-03 | yes | n/a |
| System Card risks and safeguards exist | https://deploymentsafety.openai.com/gpt-6-astra | 2026-09-03 | yes | n/a |
| hands-on Astra performance | no local run | 2026-09-03 | no | any first-person performance claim removed |

## Required publishable frontmatter plan

Shared:

- title: GPT-6 让 Codex 能搜索被挤出窗口的历史
- description: Astra 在 Codex 里的关键变化包括跨窗口 notes 和早期历史搜索。本文拆解这个机制的适用边界，并设计一次多窗口 A/B，验证它能否在摘要漏掉细节后减少返工。
- date: 2026-09-03T15:30:00-07:00
- tags: agents, codex, gpt-6, context-engineering, model-release
- visibility: public

Collection-specific:

- essays: series `Agent systems`; no canonical.

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.
- [x] Benchmark/metric claims refreshed or removed.
- [x] Security claims phrased defensively and without operational attack detail.
- [x] Hypothetical examples labeled as hypothetical.
- [x] Public links/repo/demo/result claims verified or queued for post-build eval.

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [x] Internal local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | Clear claim: searchable history matters only if it recovers evidence missed by notes and reduces rework. |
| Reader payoff | 2 | Gives a three-layer model, enablement key, fit boundary and falsifiable A/B. |
| Specificity | 2 | Includes config, window/output limits, pricing threshold, trial counts and outcome measures. |
| Structure | 2 | Progresses from compaction loss to mechanism, counterpoint and evaluation. |
| Source grounding | 2 | Every vendor fact is tied to accessible first-party documentation; no hands-on result is implied. |
| Judgment density | 2 | Separates vendor mechanism, author inference, counterevidence and unknowns throughout. |
| Voice | 2 | Clean first-person Chinese with no hard AI-phrase hits; personal voice samples are unavailable and not fabricated. |
| Safety/privacy | 2 | No secrets, private markers, local paths or operational attack detail in public artifacts. |
| Freshness | 2 | Model/config/System Card/Fable claims refreshed on 2026-09-03. |

Total: 18/18

## Review loop

### Editor review

- reviewer: independent `editor_review` subagent
- pass: yes
- blockers: none
- major edits: none; confirmed the Fable section stays subordinate to the Astra mechanism and the ending gives a concrete acceptance condition
- minor edits: improved the window-exhaustion sentence, softened diagram recovery language, and synchronized the private source ledger

### Source/factual review

- reviewer: independent `factual_review` subagent
- pass: yes after revision and re-review
- blockers: none remaining
- claims needing refresh/removal: removed unproven cross-project Memories wording and the launch card's first-disclosure claim; changed the opening from a community-majority claim to a page-level observation
- notes: confirmed Astra model envelope, config/account/default state, System Card evidence, Fable envelope/pricing/compaction, and the scoped no-equivalent-search-found wording against first-party sources

### Adversarial review

- reviewer: independent `adversarial_review` subagent
- pass: yes after revision and re-review
- blockers: none remaining
- non-blocking risks: title compresses the Astra model and Codex runtime relationship, but the body explicitly separates those layers
- required revisions: removed the 403 launch-page item and unsupported launch-only claim; softened diagram/alt recovery language; removed unrelated benchmark numbers; synchronized this review record with the final article

### Eval review (links/images, after build)

- reviewer: independent `postbuild_eval` subagent
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://learn.chatgpt.com/docs/config-file/config-reference | GET 200, 3 occurrences | yes |
| https://deploymentsafety.openai.com/gpt-6-astra | GET 200, 3 occurrences | yes |
| https://developers.openai.com/api/docs/models/gpt-6-astra | GET 200 | yes |
| https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool | GET 200 | yes |
| https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | GET 200 | yes |
| https://platform.claude.com/docs/en/models/fable-5-1/overview | GET 200 | yes |
| /my-blog/essays/gpt-6-astra-searchable-context/ | local preview GET 200 | yes |
| /my-blog/essays/fable-5-1-day-one/ | local preview GET 200; dist target exists | yes |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| /my-blog/images/gpt-6-astra-searchable-context/context-memory.svg | source, dist and preview mount each 6231 bytes; byte-identical; image/svg+xml; xmllint PASS; preview GET 200 | yes |

- rendered check run: strict UI verify at 375, 768 and 1440; all page statuses 200, no console errors/warnings, no horizontal overflow, axe 0, Lighthouse performance/accessibility/best-practices/SEO all 100
- broken items and fixes: OpenAI launch URL returned 403 before build and was removed from the public article, Links collection and manifest; final eval found no broken items

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Draft became a launch-roundup after the mechanism explanation | Removed standalone benchmark/community sections; made the A/B the single ending | yes |
| Fable comparison omitted its strongest compaction counterpoint | Added its explicit preservation guidance and separated application-owned memory files from old-window search | yes |
| Memories was described as cross-project | Replaced with the officially supported earlier-chats-to-future-work boundary | yes |
| OpenAI launch URL returned 403 in automated evaluation | Removed the public link card, manifest item, inline link and launch-only future-default claim | yes |
| Diagram implied guaranteed recall | Changed article alt and SVG to “有机会找回”, “仍可搜索” and “可搜索，不等于必召回” | yes |
| Opening implied majority community consensus | Rephrased as what is visually prominent, without a population claim | yes |
| Review metadata no longer matched the shortened article | Updated source coverage, omitted topics, links maintenance and evidence table | yes |

## Agent review

```yaml
agent_review:
  status: published
  reviewer: agent
  date: 2026-09-03
  notes: Editor, factual, adversarial and post-build eval subagents all passed after blocker revisions. Content check, sync, build, strict responsive UI verification, leak checks, CI, Pages deployment and public URL verification pass.
```

## Final human blog review

```yaml
human_blog_review:
  status: explicit-publish-request-approved
  reviewer: human
  date: 2026-09-03
  notes: 用户明确要求“把它作为 blog 发布”，并授权内容形式由 agent 决定。
```

## Mechanical verification notes

- content:check: PASS; 3 manifest items checked, no errors or warnings
- content:sync: PASS; wrote 1 essay and 2 link records
- build: PASS; 26 static pages built; pre-existing empty `notes` collection warning remains non-blocking
- preview URL: /my-blog/essays/gpt-6-astra-searchable-context/ under `out/ui-serve`
- ui-verify if run: PASS in strict mode at 375/768/1440; `out/summary.json` has `ok: true`
- leak check: PASS across manifest drafts, synced content and built essay HTML; no local paths, secrets, private markers or draft markers
- publish commit: `6e64784`; pushed fast-forward to `origin/main`
- CI: PASS, GitHub Actions run `33817682728`
- deployment: PASS, GitHub Pages run `33817706946`
- public article: https://kevinwangsheng.github.io/my-blog/essays/gpt-6-astra-searchable-context/ returned 200 and 21263 bytes; expected title, image reference and Fable internal link present
- public image: https://kevinwangsheng.github.io/my-blog/images/gpt-6-astra-searchable-context/context-memory.svg returned 200 and 6231 bytes
- public links index: https://kevinwangsheng.github.io/my-blog/links/ returned 200; both promoted source cards present
- public RSS: https://kevinwangsheng.github.io/my-blog/rss.xml returned 200; article title present
- rejection cleanup if needed: n/a, explicit publish request
