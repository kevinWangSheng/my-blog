# Review: 评审 Coding Agent：关键不是多一个 Agent，而是隔离

## Metadata

- status: preview-ready
- source paths / source records:
  - User conversation on 2026-06-15/2026-06-16 asking how to use another agent to evaluate coding-agent planning and decisions.
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/best-practices
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://developers.openai.com/codex/subagents
  - https://developers.openai.com/codex/noninteractive
  - https://developers.openai.com/codex/integrations/github
  - https://developers.openai.com/codex/learn/best-practices
  - https://developers.openai.com/api/docs/guides/agent-evals
  - https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/
  - https://arxiv.org/abs/2305.14325
  - https://arxiv.org/abs/2511.07784
  - https://openreview.net/forum?id=Sx038qxjek
  - https://arxiv.org/abs/2604.22891
- refreshed/primary sources:
  - Claude Code subagents docs, checked 2026-06-16.
  - Anthropic agent evals engineering article, checked 2026-06-16.
  - OpenAI Codex subagents and GitHub code review docs, checked 2026-06-16.
  - OpenAI Codex non-interactive mode and agent workflow eval docs, checked 2026-06-16.
  - Promptfoo coding-agent eval guide, checked 2026-06-16 as third-party practice guidance.
  - arXiv/OpenReview paper pages listed above, checked 2026-06-16.
- proposed collection: essays
- proposed slug: coding-agent-eval-needs-isolation
- source type: public-original
- target reader: solo developers using coding agents for planning, implementation, and review
- planned publishable markdown path: docs/content-pipeline/manifests/coding-agent-eval-needs-isolation/coding-agent-eval-needs-isolation.md
- planned manifest dir: docs/content-pipeline/manifests/coding-agent-eval-needs-isolation/

## Public thesis

- memorable sentence: 有效评审不靠 agent 数量，而靠隔离、冻结 artifact、运行证据和明确 rubric。
- reader decision helped: 帮读者判断什么时候用同会话 subagent、什么时候新开会话/`codex exec`、什么时候该做正式 rubric/eval。
- strongest counterpoint / edge case: For tiny reversible tasks, a second agent may add token cost and friction without catching anything that tests or a diff review would catch.

## Draft direction

Write a practical essay, not a survey. Start from the common mistake: treating "more agents" as the quality mechanism. Then give a decision model with three tiers: subagent, fresh session, formal eval/rubric. Include source freshness notes and evidence strength.

## Rewrite plan

### Keep

- Practical distinction between same-session subagent, fresh session, and formal eval.
- Strong claim that isolation, frozen artifacts, and rubric matter more than agent count.
- Human judgment stays at high-impact decision gates.

### Remove / anonymize

- Remove local repo-specific references and private workflow details from public prose.
- Do not claim a definitive paper proves same-session subagents are better or worse than fresh sessions for coding planning review.
- Do not expose local paths.

### Add / refresh

- Refresh official Claude Code and Codex docs on subagents/review.
- Refresh Anthropic agent eval guidance on isolated trials, clear rubrics, calibrated LLM judges, transcript review, and human review.
- Add paper caveats: multi-agent debate can help, but newer controlled work says intrinsic model strength/diversity dominate and group pressure can suppress correction.
- Add LLM judge bias caveat from the 2026 self-preference bias paper.

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---:|---|---|
| Claude Code subagents have separate context and are useful for context management | https://code.claude.com/docs/en/sub-agents | 2026-06-16 | yes | n/a |
| OpenAI Codex subagents are useful for parallel codebase exploration/multi-step plans and cost more tokens | https://developers.openai.com/codex/subagents | 2026-06-16 | yes | n/a |
| Codex code review is positioned as another high-signal review pass focused on serious issues | https://developers.openai.com/codex/integrations/github | 2026-06-16 | yes | n/a |
| Effective agent evals need isolated trials, clear rubrics, calibrated LLM judges, and transcript review | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | 2026-06-16 | yes | n/a |
| Multi-agent debate always improves coding planning decisions | n/a | 2026-06-16 | no | yes, replaced with narrower caveated claim |

## Required publishable frontmatter plan

Shared:

- title: "评审 Coding Agent：关键不是多一个 Agent，而是隔离"
- description: "什么时候用 subagent、什么时候新开会话、什么时候该把评审做成正式 rubric。"
- date: 2026-06-16
- tags: ["agents", "evals", "coding-agents", "workflow"]
- visibility: public

Collection-specific:

- essays: canonical? none, series? "Agent Workflows"

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
| Thesis | 2 | Clear central judgment. |
| Reader payoff | 2 | Gives an operational decision model. |
| Specificity | 2 | Distinguishes task sizes and review modes. |
| Structure | 2 | Practical arc from mistake to model to caveats. |
| Source grounding | 2 | Official docs and primary papers refreshed. |
| Judgment density | 2 | Tradeoffs and limits are explicit. |
| Voice | 2 | Public essay voice, not internal note tone. |
| Safety/privacy | 2 | No private/local prose exposure. |
| Freshness | 2 | Checked on 2026-06-16. |

Total: 17/18

## Review loop

### Editor review

- reviewer: subagent
- pass: yes
- blockers: none
- major edits: title was stiff; add concrete mini-case; make evidence section less memo-like.
- minor edits: fixed heading capitalization; clarified `codex exec` as fresh/headless run; retained decision table.

### Source/factual review

- reviewer: subagent
- pass: yes
- blockers: none
- claims needing refresh/removal: original thesis missed environment/trace evidence; added runtime/evidence requirements and OpenAI agent workflow eval / Promptfoo practice sources.
- notes: same-session subagents, fresh `codex exec` runs, and formal eval/rubric should be framed as execution patterns, not proof of quality by themselves.

### Adversarial review

- reviewer: subagent
- pass: yes after revisions
- blockers: initial blocker: review artifact still pending; first-person authority risk; evidence labels too strong.
- non-blocking risks: recent arXiv papers are caveats, not settled doctrine for coding planning.
- required revisions: completed: filled review sections, removed unsubstantiated "I use" framing, softened evidence headings, added bad/good review packet example, recorded blockers.

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| Review file had pending passes while claiming high score | Filled editor/source/adversarial results and reduced score to reflect review feedback. | yes |
| Public prose implied unverified personal practice authority | Rephrased "I use" and "I actually use" to a practical operating model/table. | yes |
| Evidence labels sounded too settled | Changed headings to docs support / eval guidance / research caveats and kept hierarchy as practical inference. | yes |
| Missing concrete failure case | Added bad/good reviewer packet example. | yes |
| Missing environment/trace evidence emphasis | Added runtime/evidence to rubric and workflow; added current OpenAI agent eval and Codex non-interactive sources. | yes |
| Public article was drafted in English | Rewrote title, description, and body in Chinese while preserving source links and checked-date labels. | yes |
| Live list/home links omitted trailing slash and 404ed on GitHub Pages | Updated `sitePath()` to add trailing slash for page routes while preserving static assets such as `.xml` and `.ico`. | yes |

## Agent review

```yaml
agent_review:
  status: preview-ready
  reviewer: Codex
  date: 2026-06-16
  notes: "Three-pass review completed with adversarial blockers resolved; synced, built, leak-checked, and UI-verified for local human preview."
```

## Final human blog review

Human review happens on local preview before publish/deploy, unless the user explicitly requested immediate publishing. If the human finds problems, mark `needs-rework`, remove/revert synced public-source content, and open a follow-up返工 session.

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Mechanical verification notes

- content:check: passed before sync, `pnpm --dir site content:check -- --input ../docs/content-pipeline/manifests/coding-agent-eval-needs-isolation`; after sync the same manifest check correctly reports target-exists conflict because `site/src/content/essays/coding-agent-eval-needs-isolation.md` is already present
- content:sync: passed, wrote `site/src/content/essays/coding-agent-eval-needs-isolation.md`
- build: passed after Chinese rewrite and trailing-slash route fix, `pnpm --dir site build`; generated `/essays/coding-agent-eval-needs-isolation/index.html`
- preview URL: local preview verified at `/my-blog/essays/coding-agent-eval-needs-isolation/`; list/home generated hrefs now include a single trailing slash
- ui-verify if run: passed, `pnpm ui-verify -- --serve out/ui-serve --path /my-blog/essays/coding-agent-eval-needs-isolation/`; `out/summary.json` ok=true, axe 0, console errors/warnings 0, overflow no, Lighthouse 100/100/100/100
- leak check: passed; no matches for `/Users/`, `kb-vault`, `docs/content-pipeline`, private/confidential/forbidden-publish markers in staged markdown, synced source, or generated HTML
- rejection cleanup if needed: pending
