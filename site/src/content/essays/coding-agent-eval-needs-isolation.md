---
title: "Evaluate Coding Agents by Isolation, Not Headcount"
description: "When to use a subagent, a fresh session, or a formal rubric to review coding-agent planning and decisions."
date: "2026-06-16"
tags: ["agents", "evals", "coding-agents", "workflow"]
visibility: "public"
series: "Agent Workflows"
---
The tempting rule is simple: if one coding agent made the plan, ask another agent to evaluate it.

That is useful, but it is not the real mechanism. The real mechanism is **reviewer independence**: a reviewer should inspect a frozen artifact, with bounded context, against an explicit rubric. A second agent that inherits all of the first agent's framing can still rubber-stamp the wrong thing. A fresh evaluator with a bad task description can still be noisy. A formal eval with a vague rubric can still produce false confidence.

So the first question is not "Should this be a subagent or a new session?" It is:

1. What artifact is being judged?
2. What context should the reviewer see, and what context should it not see?
3. What counts as pass, revise, or block?
4. What trace or runtime evidence proves the reviewer is judging what actually happened?
5. Who keeps final decision authority?

Only after that does the execution shape become obvious.

## The Three Useful Review Modes

For day-to-day coding-agent work, a useful operating model has three levels.

### 1. Same-session subagent: cheap friction for local skepticism

Use this when the task is local, reversible, and already bounded:

- review a plan before implementation;
- inspect a diff for missed edge cases;
- check whether a task list matches acceptance criteria;
- run a factual/source pass on an article or design note;
- explore a codebase slice without flooding the main conversation.

This is the everyday sweet spot. Claude Code describes subagents as specialized assistants that run in their own context window and return a summary, which is exactly the property you want when exploration output would pollute the main thread. OpenAI's Codex docs similarly frame subagents as useful for highly parallel work such as codebase exploration or multi-step feature plans, while warning that subagents consume more tokens than comparable single-agent runs.

The limitation is subtle: a same-session subagent is isolated in context, but not necessarily independent in framing. The parent agent chooses the prompt, the artifact, and the question. If the parent asks, "confirm this plan is good," the review is already compromised. The prompt should sound more like:

```text
Review this frozen plan as a skeptical staff engineer.
Return PASS / REVISE / BLOCK.
Focus on missing requirements, unsafe assumptions, unverified claims,
bad sequencing, and tests that would not prove the stated acceptance criteria.
Do not rewrite the plan unless you identify a blocker.
```

That is not bureaucracy. It is the difference between a reviewer and a cheerleader.

Here is the small failure mode to avoid:

```text
Bad review packet:
"Check whether this plan looks good. I think it covers the requirements."

Likely result:
"Looks good. Maybe add tests."
```

That is not an eval. It is a politeness ritual. A better packet is narrower and colder:

```text
Artifact: plan.md
Goal: implement the content publishing path without changing deploy behavior.
Constraints: no new dependencies, no publish, no local paths in public prose.
Evidence available: source links, manifest draft, content-check output.
Rubric: PASS / REVISE / BLOCK for goal fit, privacy, source freshness,
verification, rollback, and human decision gates.
Reviewer instruction: try to block publication if any claim is unsupported.
```

The same second model can produce much better review simply because the task became judgeable.

### 2. Fresh session or headless run: stronger independence for high-impact choices

Use a fresh session, a headless run, or `codex exec` when the review target is not just a patch, but a direction:

- architecture decisions;
- technology stack choices;
- deployment or migration plans;
- irreversible cleanup;
- long-lived repo rules;
- anything where the first agent may have become attached to its own plan.

The fresh evaluator should not read the whole prior conversation. Give it a small packet:

- goal;
- constraints;
- frozen proposal;
- relevant files or source links;
- acceptance criteria;
- known uncertainty;
- what kind of answer you want: pass, revise, block, or compare alternatives.

This is more expensive than a subagent, but it buys a cleaner read. A non-interactive run can also leave event output or structured results that are easier to archive than a live chat turn. It also makes the review durable: the next agent can inspect the artifact instead of reconstructing the argument from chat history.

The important move is to freeze the artifact first. If the evaluator reviews a moving conversation, it will evaluate the social momentum of the session. If it reviews a file, it can attack the actual plan.

### 3. Formal rubric or eval: for repeated gates

If the same judgment recurs, do not keep improvising with "ask another agent." Turn it into a rubric.

Examples:

- Does this implementation satisfy the acceptance criteria?
- Does this article have source freshness and no private leakage?
- Does this migration plan include rollback?
- Does this PR introduce auth, secrets, data-loss, or compatibility risk?
- Does this agent output distinguish checked facts, inference, and recommendation?

Anthropic's agent-eval guidance is useful here: tasks should be unambiguous enough that two domain experts would independently reach the same pass/fail verdict; eval trials should start from isolated environments; graders should prefer output quality over brittle tool-call paths; LLM judges need calibration against human experts; and for multi-component work, separate rubrics or isolated judges per dimension can be better than one giant judge.

That maps cleanly to coding-agent practice. A good reviewer prompt is just a small eval harness, and for coding agents it should include environment and trace evidence, not just the final answer:

```text
Artifact: plan.md
Runtime/evidence:
- clean worktree status
- tests/build command output
- relevant logs or trace summary
- files the agent changed or proposes to change
Rubric:
- Goal fit: pass/revise/block
- Missing constraints: pass/revise/block
- Evidence quality: pass/revise/block
- Implementation risk: pass/revise/block
- Verification plan: pass/revise/block
- Human decision required: yes/no

Rules:
- If evidence is missing, say "unverified"; do not infer.
- If a blocker exists, stop at BLOCK and explain the smallest fix.
- Do not reward a plan for sounding complete.
```

Once this exists, the question "which agent should eval?" becomes less mystical. Any capable reviewer can run the gate, and the record is legible.

## What the Evidence Actually Supports

As of 2026-06-16, I would grade the evidence like this.

**Docs support the mechanism, not the hype:** subagents are a real tool for context separation and parallel work. Claude Code and Codex both document this pattern. Codex also documents code review as another high-signal pass on pull requests, focused on serious issues and guided by repository instructions.

**Eval guidance supports the discipline:** agent evaluation quality depends on task clarity, isolated trials, good graders, transcript review, and calibration. OpenAI's current agent workflow eval guidance also points toward traces and datasets when debugging becomes repeatable evaluation. This is not specific to coding-agent planning, but it transfers well because planning review is a grading problem: does this artifact satisfy the user's goal under the real constraints?

**Research gives caveats, not a universal recipe:** multi-agent debate can improve factuality or reasoning in some settings. The 2023 multiagent debate paper reported gains on mathematical, strategic, and factual tasks. But this does not prove that every coding plan benefits from debate.

**The caution signs matter:** newer controlled work on multi-agent debate finds that intrinsic reasoning strength and group diversity dominate, while debate structure alone gives limited gains; it also identifies failure modes such as majority pressure suppressing independent correction. LLM-as-judge research also reports self-preference bias: judge models can systematically favor or disfavor their own outputs, which is one reason to distrust "the same reasoning path grades itself" as a final gate.

**Practical inference, not proven law:** for coding-agent planning, same-session subagents are usually the best default; fresh sessions are better for high-impact decisions; formal rubrics are better for repeated quality gates. I have not found a definitive study proving this exact hierarchy. It is an engineering synthesis from current tool docs, eval guidance, and known LLM judge/debate failure modes.

## A Practical Decision Table

| Situation | Best reviewer shape | Why |
|---|---|---|
| Small local implementation plan | Same-session subagent | Low friction, enough context isolation, catches obvious omissions. |
| Diff review after coding | Same-session subagent or built-in review command | The artifact is concrete and reversible. |
| Architecture or stack decision | Fresh session / separate `codex exec` | Stronger framing independence. |
| Release, deploy, migration, deletion | Fresh session plus human gate | High blast radius needs a separate audit and explicit human judgment. |
| Recurring content/source/security gate | Formal rubric, possibly LLM judge plus spot human review | Repeatability matters more than improvisation. |
| Competing designs | Multiple agents with separate briefs, then synthesis | Parallelism helps if each agent explores a genuinely different path. |
| Tiny obvious fix | No second agent | Tests, diff, and proportional checks are enough. |

The anti-pattern is using more agents to compensate for unclear ownership. If nobody knows what "good" means, three agents will produce three confident paragraphs and no ground truth.

## The Minimal Workflow

For planning and decision review, this is the smallest loop that feels reliable:

1. Main agent drafts a plan or decision note.
2. Main agent freezes it in a file or clearly bounded message.
3. Reviewer agent gets only the artifact, relevant sources, constraints, runtime evidence, and rubric.
4. Reviewer returns `PASS`, `REVISE`, or `BLOCK`.
5. Main agent revises or records the objection.
6. Human decides only at the real judgment gate.

For code implementation, I would extend it:

```text
implement
-> run tests/build/checks
-> freeze diff + evidence
-> reviewer agent checks risks and acceptance criteria
-> fix blockers
-> human review only if the decision is genuinely human-owned
```

This keeps the human out of courier work without pretending the agent can approve its own assumptions.

## The Rule

Use a subagent when you need a quick skeptical pass.

Use a fresh session when you need independence from the original framing.

Use a formal rubric when the judgment will repeat.

Use a human when the decision changes direction, risk, ownership, or public exposure.

And do not count agents. Count isolation, evidence, rubric clarity, and whether the reviewer is allowed to say no.

## Sources Checked

- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents), checked 2026-06-16.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices), checked 2026-06-16.
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), checked 2026-06-16.
- [OpenAI Codex: Subagents](https://developers.openai.com/codex/subagents), checked 2026-06-16.
- [OpenAI Codex: Non-interactive mode](https://developers.openai.com/codex/noninteractive), checked 2026-06-16.
- [OpenAI Codex: Code review in GitHub](https://developers.openai.com/codex/integrations/github), checked 2026-06-16.
- [OpenAI Codex best practices](https://developers.openai.com/codex/learn/best-practices), checked 2026-06-16.
- [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals), checked 2026-06-16.
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325), arXiv 2023.
- [Can LLM Agents Really Debate?](https://arxiv.org/abs/2511.07784), arXiv 2025.
- [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://openreview.net/forum?id=Sx038qxjek), ICLR 2024.
- [Quantifying and Mitigating Self-Preference Bias of LLM Judges](https://arxiv.org/abs/2604.22891), arXiv 2026.
- [Promptfoo: Evaluate Coding Agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/), checked 2026-06-16 as third-party practice guidance.
