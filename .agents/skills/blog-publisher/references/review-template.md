# Review: <title>

## Metadata

- status: draft|draft-review-passed|agent-cleared|synced|preview-ready|publish-ready|published|needs-rework
- source paths / source records:
  - example: /Users/shenghuikevin/kb-vault/...
  - example: docs/path/to/draft.md
  - example: https://primary-source.example/...
- refreshed/primary sources:
  - ...
- proposed collection: essays|notes|logs|links|projects
- proposed slug:
- source type: kb-derived|draft-derived|research-derived|link-derived|project-derived|public-original
- target reader:
- planned publishable markdown path: docs/content-pipeline/manifests/<slug>/<slug>.md
- planned manifest dir: docs/content-pipeline/manifests/<slug>/

## Public thesis

- memorable sentence:
- reader decision helped:
- strongest counterpoint / edge case:

## Complete-story check (required for learning/practice-derived items)

The arc binds only stages whose material actually exists. Mark N/A (with reason) for absent stages; forcing an absent stage with tangential material is a blocker.

- [ ] what the source (video/course/paper/tool) actually said is covered
- [ ] source deep-dive completeness: full section-by-section coverage (mechanisms/arguments/numbers/examples), not an outline or intro
- [ ] video/talk source is embedded as a playable video near the top, or N/A with reason (embed forbidden/unavailable/non-video source)
- [ ] source key visuals (slides/diagrams/demo screens) embedded with source-credit captions, or N/A (no informative visuals)
- [ ] what I actually practiced is concrete (steps/code/prompts/configs) — or N/A: no practice material, piece written as pure deep-dive
- [ ] real results/data/outputs are included — or N/A with the practice stage
- [ ] verified vs. untested claims are separated (for pure deep-dives: source claims the author cannot check are marked as the speaker's claims)
- [ ] my own judgment is present and clearly separated from the source's content
- absent stages and why (recorded here, not padded in the article):

## Draft direction

## Rewrite plan

### Keep

### Remove / anonymize

### Add / refresh

## Links collection maintenance

For every external source cited in the article: promote core sources (the piece is built around them) to a `links` entry in the same manifest; batch examples and passing citations stay inline only.

| cited source (url) | core source? | decision (promote / inline-only / already-exists) | links slug (if promoted) |
|---|---|---|---|

## Project/public evidence table

Use for projects or any claim about public work, shipped results, demos, repos, users, or external validation.

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|

## Required publishable frontmatter plan

Shared:

- title:
- description:
- date:
- tags:
- visibility: public

Collection-specific:

- essays: canonical?, series?
- notes: topic
- logs: period, summary
- links: url, category, note
- projects: status, role, period, repo?, demo?

## Fact refresh checklist

- [ ] Fast-moving vendor/model/protocol claims checked against official/primary source or scoped as uncertain.
- [ ] Benchmark/metric claims refreshed or removed.
- [ ] Security claims phrased defensively and without operational attack detail.
- [ ] Hypothetical examples labeled as hypothetical.
- [ ] Public links/repo/demo/result claims verified.

## Safety checklist

- [ ] No secrets/tokens/keys.
- [ ] No private marker / forbidden publish marker.
- [ ] No private person/company data.
- [ ] No fabricated project result, customer/user feedback, repo/demo, personal experience, or external endorsement.
- [ ] Internal KB/local paths are kept in review metadata, not exposed as public article prose.

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis |  |  |
| Reader payoff |  |  |
| Specificity |  |  |
| Structure |  |  |
| Source grounding |  |  |
| Judgment density |  |  |
| Voice |  |  |
| Safety/privacy |  |  |
| Freshness |  |  |

Total: /18

## Review loop

### Editor review

- reviewer: agent|subagent
- pass: yes|no
- blockers:
- major edits:
- minor edits:

### Source/factual review

- reviewer: agent|subagent
- pass: yes|no
- blockers:
- claims needing refresh/removal:
- notes:

### Adversarial review

- reviewer: agent|subagent
- pass: yes|no
- blockers:
- non-blocking risks:
- required revisions:

### Eval review (links/images, after build)

- reviewer: subagent (required; if degraded to self-check, say why)
- pass: yes|no
- link results:

| url | status | pass? |
|---|---|---|

- image results:

| src | resolved location / status | pass? |
|---|---|---|

- rendered check run: yes|no
- broken items and fixes:

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|

## Agent review

```yaml
agent_review:
  status: draft
  reviewer: agent
  date:
  notes:
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

- content:check:
- content:sync:
- build:
- preview URL:
- ui-verify if run:
- leak check:
- rejection cleanup if needed:
