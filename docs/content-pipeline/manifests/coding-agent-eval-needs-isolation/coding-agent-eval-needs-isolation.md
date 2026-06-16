---
title: "评审 Coding Agent：关键不是多一个 Agent，而是隔离"
description: "什么时候用 subagent、什么时候新开会话、什么时候该把评审做成正式 rubric。"
date: "2026-06-16"
tags: ["agents", "evals", "coding-agents", "workflow"]
visibility: "public"
series: "Agent Workflows"
---

一个很自然的想法是：如果一个 coding agent 写了计划，那就再找另一个 agent 来评审。

这个想法有用，但容易抓错重点。真正有效的不是“多一个 agent”，而是**评审独立性**：评审者应该拿到一个冻结的 artifact，在有限上下文里，按明确 rubric 判断。第二个 agent 如果继承了第一个 agent 的叙事和暗示，仍然可能只是礼貌地点头。新开会话如果输入包很糟，也一样会评出噪声。正式 eval 如果 rubric 含糊，也会制造假确定性。

所以第一问题不是“用 subagent 还是新会话”。第一问题应该是：

1. 被评审的 artifact 是什么？
2. 评审者应该看到哪些上下文，又不应该看到哪些？
3. 什么叫 `PASS`、`REVISE`、`BLOCK`？
4. 有什么运行证据或 trace 能证明 agent 真的做过对应检查？
5. 最终决策权留给谁？

这些问题清楚之后，才轮到选择执行形态。

## 三种有用的评审形态

日常 coding-agent 工作里，可以把评审分成三层。

### 1. 同会话 subagent：低摩擦的局部挑刺

适合用于低风险、局部、可逆、边界已经清楚的任务：

- 实现前审一下 plan；
- 实现后看 diff 有没有漏掉 edge case；
- 检查任务列表是否真的覆盖 acceptance criteria；
- 对文章或设计稿做事实源检查；
- 探索一个代码区域，但不污染主会话上下文。

这是日常性价比最高的形态。Claude Code 文档把 subagent 描述为有独立上下文窗口的专门助手；OpenAI Codex 文档也把 subagents 放在并行探索、代码库调查、多步骤计划等场景里，同时提醒它会消耗更多 token。这里真正有价值的属性不是“它也是一个 agent”，而是它能把探索和评审上下文从主线程里隔离出去。

限制也很明显：同会话 subagent 有上下文隔离，但不等于完全独立。主 agent 仍然决定给它什么 artifact、什么问题、什么措辞。如果提示词是“帮我确认这个计划没问题”，评审已经被污染了。

更好的提示应该像这样：

```text
Review this frozen plan as a skeptical staff engineer.
Return PASS / REVISE / BLOCK.
Focus on missing requirements, unsafe assumptions, unverified claims,
bad sequencing, and tests that would not prove the stated acceptance criteria.
Do not rewrite the plan unless you identify a blocker.
```

这不是仪式感，而是在给 reviewer 说“不”的权力。

一个常见坏例子是：

```text
Bad review packet:
"Check whether this plan looks good. I think it covers the requirements."

Likely result:
"Looks good. Maybe add tests."
```

这不是 eval，只是礼貌互动。一个更冷、更窄的评审包应该像这样：

```text
Artifact: plan.md
Goal: implement the content publishing path without changing deploy behavior.
Constraints: no new dependencies, no publish, no local paths in public prose.
Evidence available: source links, manifest draft, content-check output.
Rubric: PASS / REVISE / BLOCK for goal fit, privacy, source freshness,
verification, rollback, and human decision gates.
Reviewer instruction: try to block publication if any claim is unsupported.
```

同一个模型，在第二种输入下会更像评审者，因为任务本身变得可判断了。

### 2. 新会话或 headless run：给高影响决策更强隔离

当评审对象不只是一个 patch，而是方向选择时，应该提高隔离强度：

- 架构决策；
- 技术栈选择；
- 部署、迁移、清理方案；
- 长期 repo 规则；
- 任何第一个 agent 可能已经“爱上自己方案”的任务。

这时可以新开一个会话，或者用 `codex exec` 这类 headless / non-interactive run。重点是让评审者只看一个小包：

- 目标；
- 约束；
- 冻结 proposal；
- 相关文件或来源链接；
- 验收标准；
- 已知不确定性；
- 期待输出：pass、revise、block，还是比较多个方案。

它比 subagent 贵一点，但换来更干净的读法。非交互式运行还可以留下事件输出、结构化结果或日志，比临时聊天更容易归档给下一个 agent。

关键动作是先冻结 artifact。评审一个正在滚动的聊天，很容易评到会话里的势能；评审一个文件，才更容易攻击真实方案。

### 3. 正式 rubric / eval：重复出现的质量门

如果同一种判断会反复出现，就不要每次临时“找另一个 agent 看看”。把它做成 rubric。

典型例子：

- 这个实现是否满足 acceptance criteria？
- 这篇文章是否有来源刷新、是否泄漏私有信息？
- 迁移计划是否包含 rollback？
- PR 是否引入 auth、secret、数据丢失或兼容性风险？
- agent 输出是否区分了已检查事实、推断和建议？

Anthropic 的 agent eval 指南在这里很有用：任务要明确到两个领域专家能独立给出相近判定；eval trial 要从隔离环境开始；grader 应更关注结果质量，而不是脆弱的工具调用路径；LLM judge 需要和 human expert 校准；多维度任务可以拆成多个独立 judge 或多个 rubric。

映射到 coding-agent 工作里，一个评审 prompt 本质上就是小型 eval harness。并且对 coding agent 来说，不能只看最终回答，还要看环境和 trace：

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

有了这套东西，“哪个 agent 来评审”就不再神秘。任何足够强的 reviewer 都可以跑这个门，记录也能被后续复查。

## 当前证据支持到哪里

截至 2026-06-16，我会这样分层看证据。

**官方文档支持机制，不支持迷信。** Claude Code 和 Codex 都把 subagent 放在上下文隔离、专门任务、并行探索这类场景里。Codex 也把代码评审定位为另一个高信号 pass，用于找严重问题，并受 repo 指令约束。这支持“subagent 有用”，但不支持“agent 数量越多越可靠”。

**eval 指南支持纪律。** Anthropic 和 OpenAI 的 eval 材料都指向同一个方向：任务要明确，环境要隔离，输出要可评分，trace / dataset / grader 要能复查。规划评审虽然不是传统 benchmark，但本质仍是评分问题：这个 artifact 是否在真实约束下满足目标？

**多 agent 研究只能给 caveat，不能给万能公式。** 2023 年 multiagent debate 论文报告过事实性和推理任务上的提升；但这不等于每个 coding plan 都适合 debate。更新的 controlled study 也提醒，模型本身的推理能力和 agent 多样性往往比“辩论结构”更重要，群体压力还可能压制少数正确意见。

**LLM judge 也会偏。** 2026 年关于 self-preference bias 的论文指出，LLM judge 可能系统性偏向或排斥自己的输出。这是为什么“同一条推理路径自己评自己”不能当最终门禁。

**实践结论不是定律。** 日常任务优先同会话 subagent，高影响决策用新会话或 headless run，重复质量门做成 rubric / eval。这不是某篇论文直接证明的结论，而是从当前工具文档、eval 指南和已知 judge / debate 失效模式里合成出来的工程判断。

## 一个实用决策表

| 场景 | 更合适的评审形态 | 原因 |
|---|---|---|
| 小型本地实现计划 | 同会话 subagent | 摩擦低，隔离够用，能抓明显遗漏。 |
| 实现后的 diff review | 同会话 subagent 或内置 review 命令 | artifact 具体、可逆。 |
| 架构或技术栈决策 | 新会话 / 单独 `codex exec` | 减少原会话 framing 污染。 |
| 发布、迁移、删除 | 新会话 + human gate | 影响面大，需要独立审计和人类判断。 |
| 内容、来源、安全等重复门禁 | 固定 rubric，必要时 LLM judge + human spot check | 可重复性比临时发挥更重要。 |
| 多个竞争方案 | 多个 agent 分别拿独立 brief，再综合 | 只有方案真的能并行拆开时才值得。 |
| 极小的显然修复 | 不需要第二个 agent | 测试、diff 和比例合适的检查就够了。 |

反模式是用更多 agent 弥补目标不清。如果没人知道什么叫“好”，三个 agent 只会给出三段自信文字，而不是 ground truth。

## 最小可靠流程

规划和决策评审，可以压到这个最小闭环：

1. 主 agent 起草 plan 或 decision note。
2. 主 agent 把它冻结成文件或明确边界的消息。
3. reviewer agent 只拿 artifact、来源、约束、运行证据和 rubric。
4. reviewer 返回 `PASS`、`REVISE` 或 `BLOCK`。
5. 主 agent 修订或记录异议。
6. 只有真正属于人类判断的地方才交给 human。

实现任务可以再加一层：

```text
implement
-> run tests/build/checks
-> freeze diff + evidence
-> reviewer agent checks risks and acceptance criteria
-> fix blockers
-> human review only if the decision is genuinely human-owned
```

这样 human 不需要当上下文搬运工，agent 也不能假装自己已经批准了自己的假设。

## 最后规则

需要快速挑刺，用 subagent。

需要摆脱原会话 framing，用新会话或 headless run。

同类判断会重复，用正式 rubric。

方向、风险、所有权、公开暴露面发生变化，让 human 做最终判断。

不要数 agent 数量。数隔离、证据、rubric 清晰度，以及 reviewer 有没有权力说“不”。

## 已检查来源

- [Claude Code: Create custom subagents](https://code.claude.com/docs/en/sub-agents)，检查于 2026-06-16。
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices)，检查于 2026-06-16。
- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)，检查于 2026-06-16。
- [OpenAI Codex: Subagents](https://developers.openai.com/codex/subagents)，检查于 2026-06-16。
- [OpenAI Codex: Non-interactive mode](https://developers.openai.com/codex/noninteractive)，检查于 2026-06-16。
- [OpenAI Codex: Code review in GitHub](https://developers.openai.com/codex/integrations/github)，检查于 2026-06-16。
- [OpenAI Codex best practices](https://developers.openai.com/codex/learn/best-practices)，检查于 2026-06-16。
- [OpenAI: Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals)，检查于 2026-06-16。
- [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325)，arXiv 2023。
- [Can LLM Agents Really Debate?](https://arxiv.org/abs/2511.07784)，arXiv 2025。
- [CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing](https://openreview.net/forum?id=Sx038qxjek)，ICLR 2024。
- [Quantifying and Mitigating Self-Preference Bias of LLM Judges](https://arxiv.org/abs/2604.22891)，arXiv 2026。
- [Promptfoo: Evaluate Coding Agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/)，作为第三方实践材料检查于 2026-06-16。
