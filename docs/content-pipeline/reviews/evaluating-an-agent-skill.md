# Review: agent-skill-eval-judge-self-preference

status: draft-review-passed
type: essays (+ 1 links)
date: 2026-07-06

## Source
- 第一人称复盘,素材来自作者本人这次对 blog-writing-specialist skill 的 eval 工作(变体、fixture、局部+端到端、双判官打分)。所有数字来自实际 eval 结果,非编造。
- 理论源:Matt Pocock `writing-great-skills`(github.com/mattpocock/skills)。
- eval fixture 用到两个公开 YouTube 访谈(Matt Pocock workflow / Ryan Lopopolo, Latent Space)——作为测试输入提及,非推荐源。
- Freshness:gpt-5.5 / codex-cli 0.142.5,当前有效。

## Links maintenance
| 源 | promote / inline | 理由 |
|---|---|---|
| github.com/mattpocock/skills | promote(links 条目) | 核心理论判据,可独立推荐 |
| YouTube: Matt Pocock workflow | inline | eval fixture,测试输入 |
| YouTube: Ryan Lopopolo talk | inline | e2e 测试输入 |

## Voice
通用稿。voice.md 占位模板,无个人嗓音签名要保留。保持干净真人中文,不套 house style。

## Quality gate
- 编辑评审:已由独立(异源 Claude)评审跑过,PASS(加权 4.26,无维度 <3),核心修订(补 current 在同源判官下的分数、去黑话"链路"、软化 self-preference 断言、v2 离群点标注)已落实。
- 机器门:writing 侧 check.sh 无硬命中。
- 待跑:对抗/隐私评审子代理 + eval(links/图)子代理 + 泄露 grep。

## Safety
- 无 source/safety blocker。
- 正文只用泛化说法描述本地路径,不含 /Users/ 等真实路径(泄露检查阶段确认)。
