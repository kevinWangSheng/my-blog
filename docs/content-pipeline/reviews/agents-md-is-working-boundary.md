# Review: AGENTS.md 到底该写什么

## Metadata

- status: publish-ready
- source paths / source records:
  - current interactive learning session about AGENTS.md structure, team/local split, examples, and eval loop
  - Codex manual fetched via openai-docs helper on 2026-06-19
  - https://github.com/apache/airflow/blob/main/AGENTS.md
  - https://github.com/hashicorp/terraform-provider-aws/blob/main/AGENTS.md
  - https://github.com/TracecatHQ/tracecat/blob/main/AGENTS.md
  - https://github.com/outline/outline/blob/main/AGENTS.md
  - https://github.com/Unleash/unleash/blob/main/AGENTS.md
  - https://github.com/openai/codex/blob/main/AGENTS.md
  - https://github.com/openai/openai-agents-python/blob/main/AGENTS.md
  - https://github.com/cloudflare/workers-sdk/blob/main/AGENTS.md
  - https://github.com/databricks/cli/blob/main/AGENTS.md
  - https://github.com/vinceglb/FileKit/blob/main/AGENTS.md
- refreshed/primary sources:
  - OpenAI Codex Manual, section "Custom instructions with AGENTS.md", refreshed 2026-06-19
  - Public GitHub AGENTS.md files listed above, fetched/checked 2026-06-19
- proposed collection: essays
- proposed slug: agents-md-is-working-boundary
- source type: public-original
- target reader: engineers using coding agents who want to understand how to write AGENTS.md from mechanism, boundaries, and public examples
- planned publishable markdown path: docs/content-pipeline/manifests/agents-md-is-working-boundary/agents-md-is-working-boundary.md
- planned manifest dir: docs/content-pipeline/manifests/agents-md-is-working-boundary/

## Public thesis

- memorable sentence: AGENTS.md 不该从模板开始写,而应该从项目里反复出错、反复需要确认、反复需要验证的地方长出来。
- reader decision helped: Understand what AGENTS.md is, how it differs from README/local/current-task notes, and how to write evidence-backed rules from real project boundaries.
- strongest counterpoint / edge case: Very small projects may only need a short file; overly detailed AGENTS.md can become stale noise.

## Draft direction

Write an essay, not a reference manual. Use the recent learning path as synthesis, but keep public prose focused on a durable mental model and practical structure.

## Rewrite plan

### Keep

- The corrected loading model: global, project root, nested/cwd; closer guidance wins; built once per run/session.
- The distinction between stable rules and task plans.
- Team vs local split.
- Public examples as patterns, not absolute best templates.
- Type-based conclusions from public AGENTS.md examples, without adding a full SaaS template.

### Remove / anonymize

- Internal local paths, raw command logs, temporary cache paths.
- Chat-specific process details that do not help public readers.
- Any claim that a final independent subagent was actually run in this environment.

### Add / refresh

- Official Codex AGENTS.md behavior from the refreshed manual.
- Links to public case studies.
- Strong caveat that templates must be tailored by project risk.

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| Codex reads AGENTS.md before work and layers global/project/nested guidance | OpenAI Codex Manual, Custom instructions with AGENTS.md | 2026-06-19 | yes | n/a |
| Public projects use AGENTS.md for repo-specific agent guidance | public GitHub files listed above | 2026-06-19 | yes | n/a |

## Required publishable frontmatter plan

Shared:

- title: AGENTS.md 到底该写什么
- description: AGENTS.md 给 coding agent 写开工边界。先讲它是什么,再用公开项目原文拆解哪些内容真的会改变 agent 的下一步动作。
- date: 2026-06-19
- tags: ["agents", "codex", "workflow", "context-engineering"]
- visibility: public

Collection-specific:

- essays: series: Agent Workflows

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
| Thesis | 2 | Clear central claim: boundary, not documentation dump. |
| Reader payoff | 2 | Gives decisions for team/local/nested/case-based writing. |
| Specificity | 2 | Includes examples and project-type mapping. |
| Structure | 2 | Adds background, then moves through public evidence blocks, transfer lessons, template caveat, and a practical rule filter. |
| Source grounding | 2 | Official Codex behavior and public examples recorded. |
| Judgment density | 2 | Clear cautions against overlong/general rules. |
| Voice | 1 | Voice file is template; draft uses general personal technical voice. |
| Safety/privacy | 2 | No private paths in public article. |
| Freshness | 2 | Official manual and public examples refreshed today. |

Total: 17/18

## Review loop

### Editor review

- reviewer: agent
- pass: yes
- blockers: first pass failed due repeated negative-contrast phrasing and title/ending sounding too polished.
- major edits: Retitled the article, removed repeated "not X but Y" phrasing, rewrote the ending as practical review questions.
- minor edits: Removed "chain/link" wording and reduced abstract summary sentences.

### Source/factual review

- reviewer: agent
- pass: yes
- blockers: none
- claims needing refresh/removal: Avoid saying public examples are "best"; call them learning cases.
- notes: Official loading behavior is based on refreshed Codex manual.

### Adversarial review

- reviewer: agent
- pass: yes
- blockers: none
- non-blocking risks: Voice file remains template; independent review can only confirm general human technical voice, not exact author match. Half-width punctuation remains stylistically rough but non-blocking.
- required revisions: State that local guidance must not hide team-critical rules.

### Independent writing review

- reviewer: codex exec read-only review.sh
- pass: yes
- result: final PASS on the background-plus-evidence rewrite, weighted average 3.89/5; AI trace cleanup 4.0/5; argument/examples 4.0/5; local/global consistency 4.0/5.
- limitation: voice.md still contains placeholders, so "looks like author" could not be evaluated; review only confirms general human voice.
- first pass: FAIL, weighted average 3.32/5; AI trace cleanup 2/5.
- resolution: added AGENTS.md background, local/team/current-task split, public AGENTS.md source excerpts in code blocks, template counterpoint, public source links, then reran check.sh and review.sh successfully.

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Voice file incomplete | Use general human technical voice and disclose in final handoff | yes |
| Risk of overclaiming public examples | Reworded as learning cases | yes |
| Risk of exposing local paths | Kept local paths out of public markdown | yes |
| First writing review failed AI-trace gate | Revised title, transitions, and ending; reran review.sh and passed | yes |
| Earlier draft felt generic and under-supported | Rewrote around 10 public AGENTS.md cases with concrete paths, commands, risks, and transfer lessons | yes |
| Public cases lacked traceable public links | Added a compact public-source list at the end of the article | yes |
| User flagged missing background and insufficient evidence | Added background explanation and full relevant public excerpts for key cases, especially Codex sandbox/Bazel/test/snapshot sections | yes |

## Agent review

~~~yaml
agent_review:
  status: publish-ready
  reviewer: agent
  date: 2026-06-20
  notes: "User explicitly requested deploy. Latest rewrite adds AGENTS.md background plus public source excerpts. check.sh passed with 0 hard and 0 soft hits. read-only review.sh passed with weighted 3.89/5. Content check, sync, build, leak check, preview prepare, 4327 preview, and UI verify passed."
~~~

## Final human blog review

~~~yaml
human_blog_review:
  status: approved-for-deploy
  reviewer: human
  date: 2026-06-20
  notes: "User said: 可以的,走后续的部署流程吧"
~~~

## Mechanical verification notes

- content:check: PASS, pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/agents-md-is-working-boundary --overwrite
- content:sync: PASS, wrote site/src/content/essays/agents-md-is-working-boundary.md with --overwrite after user-directed revision
- build: PASS, pnpm --dir site build, 23 pages
- preview URL: http://127.0.0.1:4327/my-blog/essays/agents-md-is-working-boundary/ confirmed 200 with title "AGENTS.md 到底该写什么 · Essays"
- ui-verify if run: PASS, axe 0 at 375/768/1440, console errors 0, console warnings 0, overflow no, Lighthouse performance/accessibility/best-practices/seo 100/100/100/100, summary out/summary.json
- leak check: PASS, no matches for local path/private/forbidden markers in staged markdown, synced source, or generated HTML
- rejection cleanup if needed:
