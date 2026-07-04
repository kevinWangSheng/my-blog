# Review: 一套给 coding agent 执行的开发流程

## Metadata

- status: publish-ready
- source paths / source records:
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/AGENTS.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/STATUS.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/TASKS.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/templates/task-packet.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/docs/agent-env/task-system.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/docs/agent-env/execution-protocol.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/docs/agent-env/review-protocol.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/docs/agent-env/handoff-protocol.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/docs/agent-env/capture-loop.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/evals/rubrics/implementation.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/P0-BREAKDOWN.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/P1A-BREAKDOWN.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/capture/ledger.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/tasks/0011-institutionalize-guard-negative-test-rule.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/tasks/0043-security-boundary-hardening.md
  - /Users/shenghuikevin/dev/AI/dep-upgrade-agent/reviews/2026-07-03-0041-security-boundary-hardening-review.md
- refreshed/primary sources:
  - Local project source-of-truth files above, checked 2026-07-04.
  - Writing skill check: `check.sh` passed after final edits; hard hits 0. Soft hints remain only for SVG/figure technical prose and CSS/markup context.
  - Writing skill independent review: PASS before final small fact/accessibility patch, weighted 3.84/5; AI trace 3.0; argument/examples 4.0; local/global consistency 4.0.
  - Voice note: `voice.md` remains incomplete; this draft is validated only as generic human technical voice, not author-specific voice.
- proposed collection: essays
- proposed slug: coding-agent-dev-flow-system
- source type: project-derived / public-original
- target reader: engineers building projects with coding agents across multiple sessions, roles, evals, and review gates
- planned publishable markdown path: docs/content-pipeline/manifests/coding-agent-dev-flow-system/coding-agent-dev-flow-system.md
- planned manifest dir: docs/content-pipeline/manifests/coding-agent-dev-flow-system/

## Public thesis

- memorable sentence: Coding agent development becomes reliable when project state, authorization boundaries, verification evidence, review, closeout, and capture loops live in repo artifacts instead of chat memory.
- reader decision helped: Decide when a coding-agent project needs task packets, independent review, evidence-backed eval, closeout, and process capture instead of direct ad hoc coding.
- strongest counterpoint / edge case: Small scripts, one-day experiments, and fully local reversible edits do not need the full machinery; the workflow should scale up only when cross-session recovery, risk, or repeated review friction appears.

## Complete-story check (required for learning/practice-derived items)

- [x] what the source (video/course/paper/tool) actually said is covered — N/A: this is project-process derived, not source deep-dive derived.
- [x] source deep-dive completeness: full section-by-section coverage (mechanisms/arguments/numbers/examples), not an outline or intro — N/A.
- [x] source key visuals (slides/diagrams/demo screens) embedded with source-credit captions, or N/A (no informative visuals) — N/A.
- [x] what I actually practiced is concrete (steps/code/prompts/configs) — concrete project artifacts, task ids, eval thresholds, review/capture examples are included.
- [x] real results/data/outputs are included — P0/P1a state, Method B thresholds, task packet fields, CL-0002 institutionalization, 0043 review/closeout, and command names are included.
- [x] verified vs. untested claims are separated — article frames the system as learning-grade and gives applicability boundaries.
- [x] my own judgment is present and clearly separated from source/project facts.
- absent stages and why (recorded here, not padded in the article): no external video/course/paper source and no source visuals.

## Draft direction

Publish as an essay in the Agent Workflows series. The public piece should read as a general technical process essay. `dep-upgrade-agent` appears only as a recurring example to make the flow concrete.

## Rewrite plan

### Keep

- Process-first framing: AGENTS.md entry, state restoration, task packet, risk/evidence-based breakdown, producer/evaluator split, eval, human gate, closeout, capture loop.
- Inline SVG process diagram with animated flow and loops.
- Concrete but limited examples from P0 drift, Method B, P1a isolated execution, 0043 security hardening, and CL-0002/task 0011.
- Applicability boundary for when the process is too heavy.

### Remove / anonymize

- Local filesystem paths from public prose.
- Raw reviewer outputs and private execution logs.
- Any claim that this is production-grade product maturity.
- Volatile pricing/platform details not needed for the workflow argument.

### Add / refresh

- Process-first title and description.
- SVG text equivalent (`title`, `desc`, and fuller `figcaption`) after accessibility review.
- Updated 0043 state: closed after dedicated grader security review and human results-review acceptance on 2026-07-03.
- Disclosure that the author voice file is incomplete; the draft is generic human technical voice.

## Links collection maintenance

For every external source cited in the article: promote core sources (the piece is built around them) to a `links` entry in the same manifest; batch examples and passing citations stay inline only.

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|
| N/A in staged article body | no | no external source citation in staged markdown | N/A |

Note: the built page template adds related-reading links, including an existing Anthropic article link. Those are site chrome/related content, not sources for this article.

## Project/public evidence table

Use for projects or any claim about public work, shipped results, demos, repos, users, or external validation.

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| `dep-upgrade-agent` uses AGENTS.md / STATUS.md / TASKS.md / task packets / runs / reviews / capture ledger for agent development workflow | local source files listed in metadata | 2026-07-04 | yes | n/a |
| P0 was human-accepted after Method B and overall P0 completion ratification | `STATUS.md`, `P0-BREAKDOWN.md` | 2026-07-04 | yes | n/a |
| P1a is in isolated execution work and task 0043 security hardening is closed after dedicated grader security review plus human results-review on 2026-07-03 | `STATUS.md:48-58`, `TASKS.md`, `tasks/0043-security-boundary-hardening.md:3-5`, `tasks/0043-security-boundary-hardening.md:122-149`, `reviews/2026-07-03-0041-security-boundary-hardening-review.md:70-93` | 2026-07-04 | yes | stale "awaiting human closeout" wording removed |
| CL-0002 became task 0011 and updated implementation rubric | `capture/ledger.md`, `tasks/0011...`, `evals/rubrics/implementation.md` | 2026-07-04 | yes | n/a |

## Required publishable frontmatter plan

Shared:

- title: 一套给 coding agent 执行的开发流程
- description: 从 AGENTS.md 到 task packet、执行、eval、review、closeout 和 capture loop，怎么把 coding agent 开发变成可恢复的流程。
- date: 2026-07-04
- tags: ["agents", "coding-agents", "workflow", "evals"]
- visibility: public

Collection-specific:

- essays: series: Agent Workflows

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.
- [x] Benchmark/metric claims refreshed or removed.
- [x] Security claims phrased defensively and without operational attack detail.
- [x] Hypothetical examples labeled as hypothetical.
- [x] Public links/repo/demo/result claims verified or omitted.

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [x] Internal KB/local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | Clear claim: durable coding-agent work needs artifact-backed process, not chat memory. |
| Reader payoff | 2 | Gives a threshold for when to use task packets, review, closeout, and capture loop. |
| Specificity | 2 | Uses P0 drift, Method B, task packet fields, 0043, and CL-0002 as concrete evidence. |
| Structure | 2 | Moves from overall flow diagram to entry rules, state, task packets, breakdown, execution, eval, human gate, closeout, capture, and boundary. |
| Source grounding | 2 | Local project source artifacts are recorded and checked. |
| Judgment density | 2 | Includes tradeoffs and when the workflow is too heavy. |
| Voice | 1 | Voice file remains template; writing skill passed only for general human technical voice. |
| Safety/privacy | 2 | Local paths excluded from public markdown; review metadata keeps source paths. |
| Freshness | 2 | Project state checked on 2026-07-04; 0043 state refreshed after stale-claim review. |

Total: 17/18

## Review loop

### Editor review

- reviewer: codex exec read-only subagent
- pass: yes
- blockers: none
- major edits: Non-blocking suggestion to move applicability/payoff earlier and add reader-facing framing around dense P0/P1a/Method B terms.
- minor edits: Title fits the revised article; thesis is now process-first; SVG is useful rather than decorative.

### Source/factual review

- reviewer: codex exec read-only subagent for the first pass; final re-check degraded to agent self-check because `codex exec -s read-only` hit usage limit.
- pass: yes, with degradation disclosed
- blockers: none remaining in article body.
- claims needing refresh/removal: Initial independent review found stale wording that 0043 was still awaiting human closeout. Final article now says 0043 was implemented, passed dedicated grader security review, and completed human results-review / closeout on 2026-07-03.
- notes: Manual source check verified support in `STATUS.md:48-58`, `tasks/0043-security-boundary-hardening.md:3-5`, `tasks/0043-security-boundary-hardening.md:122-149`, and `reviews/2026-07-03-0041-security-boundary-hardening-review.md:70-93`. Safe claims include AGENTS.md start protocol, task packet fields, P0 drift/D1-D6, Method B thresholds, producer/evaluator separation, 0043 residual follow-ups, and CL-0002/rubric rule.

### Adversarial review

- reviewer: codex exec read-only subagent
- pass: no for publication yet; content close.
- blockers: External eval still has to pass before preview-ready/publish-ready. SVG needed a fuller text equivalent; this was fixed with SVG `title`/`desc` and expanded figcaption.
- non-blocking risks: Local project evidence cannot be independently verified by public readers; dense internal vocabulary narrows the audience; current-state wording can age.
- required revisions: Keep project-status claims explicitly dated; do not imply product maturity beyond learning-grade; rerun external link eval in a passing environment or after public deployment.

### Eval review (links/images, after build)

- reviewer: degraded self-check; required eval subagent could not be spawned because `codex exec` hit usage limit.
- pass: no
- link results:

| url | status | pass? |
|---|---|---|
| staged Markdown external links | none found except SVG namespace string `http://www.w3.org/2000/svg` | yes / not a navigational link |
| built HTML `https://kevinwangsheng.github.io/my-blog/essays/coding-agent-dev-flow-system` | 404 | no |
| built HTML `https://kevinwangsheng.github.io/my-blog/og.png` | 200 | yes |
| built HTML `https://fonts.googleapis.com` | 404 | no |
| built HTML `https://fonts.gstatic.com` | 404 | no |
| built HTML Google Fonts CSS URL | 200 | yes |
| built HTML `https://www.anthropic.com/research/building-effective-agents` | 200 | yes |
| built HTML site-internal hrefs | resolve under local preview mount or are hash anchors with matching sections | yes |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| staged Markdown images | none found; article uses inline SVG, not `<img>` | yes |
| built HTML `<img src>` tags | none found | yes |

- rendered check run: yes. `ui-verify` loaded the local route and checked 375/768/1440 px.
- broken items and fixes: The canonical article URL 404s because this page is not deployed yet. Font provider root URLs return 404 while the actual CSS URL returns 200; these root links come from built page resource hints/site shell, not the article body. Because eval is degraded and not fully passing, the item remains `synced`, not `preview-ready`.

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| voice.md incomplete | User explicitly chose generic writing because voice samples are insufficient; final report must disclose this limitation | yes |
| article was too project-specific | Rewrote around the general coding-agent development workflow; project details are embedded as examples | yes |
| missing/weak process visual | Added inline animated SVG flow diagram with loops, human gate, closeout, and capture loop | yes |
| SVG accessibility concern | Added SVG `role`, `title`, `desc`, and expanded figcaption; `ui-verify` axe critical/serious count is 0 | yes |
| stale 0043 current-state claim | Updated public article to closed/human-accepted 2026-07-03 wording and refreshed source evidence | yes |
| external eval / preview-ready gate | Degraded eval still has failing URL checks; do not mark preview-ready or publish-ready | no |

## Agent review

```yaml
agent_review:
  status: publish-ready
  reviewer: agent
  date: 2026-07-04
  notes: Staged markdown, manifest, and synced essay passed local verification and the user explicitly approved publishing. Writing check passed with hard hits 0; content:check, content:sync, build, preview:prepare, leak check, and ui-verify passed. Source final re-check and eval review were degraded because codex subagent spawning hit usage limits. Generated external URLs include the not-yet-deployed canonical URL; verify the live route after deploy.
```

## Final human blog review

Human review happens on local preview before publish/deploy, unless the user explicitly requested immediate publishing. If the human finds problems, mark `needs-rework`, remove/revert synced public-source content, and open a follow-up rework session.

```yaml
human_blog_review:
  status: approved-for-publish
  reviewer: human
  date: 2026-07-04
  notes: User explicitly said "好了,可以发布了"; proceed through push, CI/deploy, and live URL verification.
```

## Mechanical verification notes

- content:check: `pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/coding-agent-dev-flow-system --overwrite` passed; ok true, checked 1, errors/warnings empty.
- content:sync: `pnpm --dir site content:sync -- --input ../docs/content-pipeline/manifests/coding-agent-dev-flow-system --overwrite` passed; wrote `site/src/content/essays/coding-agent-dev-flow-system.md`.
- build: `pnpm --dir site build` passed; generated `/essays/coding-agent-dev-flow-system/index.html`.
- preview URL: latest `ui-verify` served `http://127.0.0.1:58524/my-blog/essays/coding-agent-dev-flow-system/`; earlier local static preview server may still serve `http://127.0.0.1:4328/my-blog/essays/coding-agent-dev-flow-system/`.
- ui-verify if run: `pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/coding-agent-dev-flow-system/` passed; 375/768/1440 px screenshots, axe 0 critical/serious, console errors/warnings 0, overflow no, Lighthouse performance 99, accessibility 100, best-practices 100, SEO 100.
- leak check: passed on staged public markdown, synced source, and generated HTML for `/Users/`, `kb-vault`, `docs/content-pipeline`, private/forbidden markers, and Chinese private markers.
- rejection cleanup if needed: not needed yet; item is synced for local review but not preview-ready because eval did not pass.
