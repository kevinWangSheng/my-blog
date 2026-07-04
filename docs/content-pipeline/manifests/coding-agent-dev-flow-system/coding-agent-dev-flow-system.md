---
title: "一套给 coding agent 执行的开发流程"
description: "从 AGENTS.md 到 task packet、执行、eval、review、closeout 和 capture loop，怎么把 coding agent 开发变成可恢复的流程。"
date: "2026-07-04"
tags: ["agents", "coding-agents", "workflow", "evals"]
visibility: "public"
series: "Agent Workflows"
---
让 coding agent 写代码，改文件反而不是最难的部分。项目一旦跨过几轮会话，事情会变得很快：上一轮说到哪了，哪些决定已经授权，哪些结果只是自检通过，哪些结论经过独立 review，下一轮 agent 应该从哪里接手。

如果这些都留在聊天历史里，流程很快会变形。agent 会从一句“差不多完成了”里推断出太多东西，也会把没有验证过的状态当成事实。

我后来在 `dep-upgrade-agent` 里把这件事拆成了一套开发流程。这个项目本身是一个 learning-grade 的依赖升级 agent，但这篇不讲项目史。项目只是例子。真正想讲的是：一套给 coding agent 执行的开发流程，应该怎么从入口、任务拆分、执行、eval、review，一直走到 closeout 和下一轮。

先看整体动作。

<figure class="afe afe--coding-agent-flow" role="img" tabindex="0" aria-label="动态流程图: coding agent 从入口规则读取状态,生成任务包,执行实现,运行验证,进入独立评审和 eval;失败回到任务或实现,通过后进入人类确认、closeout 和 capture loop,再生成下一轮任务">
<style>
.afe--coding-agent-flow {
  --afe-bg: #fbfaf7;
  --afe-node: #ffffff;
  --afe-node-soft: #f3f7f4;
  --afe-border: #d8d2c7;
  --afe-edge: #7a756c;
  --afe-text: #24211d;
  --afe-muted: #746f66;
  --afe-accent: #0f766e;
  --afe-warn: #a16207;
  --afe-human: #7c3aed;
  --afe-ok: #3f6212;
  margin: 1.4rem 0 1.6rem;
  overflow-x: auto;
}
html[data-theme="dark"] .afe--coding-agent-flow {
  --afe-bg: #181614;
  --afe-node: #24211f;
  --afe-node-soft: #1d2a25;
  --afe-border: #49433d;
  --afe-edge: #aaa39a;
  --afe-text: #ede9e2;
  --afe-muted: #b8b0a6;
  --afe-accent: #2dd4bf;
  --afe-warn: #facc15;
  --afe-human: #c4b5fd;
  --afe-ok: #bef264;
}
@media (prefers-color-scheme: dark) {
  html:not([data-theme="light"]) .afe--coding-agent-flow {
    --afe-bg: #181614;
    --afe-node: #24211f;
    --afe-node-soft: #1d2a25;
    --afe-border: #49433d;
    --afe-edge: #aaa39a;
    --afe-text: #ede9e2;
    --afe-muted: #b8b0a6;
    --afe-accent: #2dd4bf;
    --afe-warn: #facc15;
    --afe-human: #c4b5fd;
    --afe-ok: #bef264;
  }
}
.afe--coding-agent-flow svg {
  display: block;
  width: 100%;
  min-width: 820px;
  height: auto;
  background:
    linear-gradient(90deg, color-mix(in srgb, var(--afe-border) 18%, transparent) 1px, transparent 1px),
    linear-gradient(180deg, color-mix(in srgb, var(--afe-border) 14%, transparent) 1px, transparent 1px),
    var(--afe-bg);
  background-size: 42px 42px;
  border: 1px solid var(--afe-border);
  border-radius: 8px;
}
.afe--coding-agent-flow text {
  font: 600 13px/1 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  fill: var(--afe-text);
}
.afe--coding-agent-flow .sub {
  font-weight: 400;
  font-size: 10.5px;
  fill: var(--afe-muted);
}
.afe--coding-agent-flow .lane {
  fill: color-mix(in srgb, var(--afe-node) 58%, transparent);
  stroke: var(--afe-border);
  stroke-width: 1;
}
.afe--coding-agent-flow .lane-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .04em;
  fill: var(--afe-muted);
}
.afe--coding-agent-flow .node rect {
  fill: var(--afe-node);
  stroke: var(--afe-border);
  stroke-width: 1.5;
  rx: 8;
}
.afe--coding-agent-flow .node--soft rect {
  fill: var(--afe-node-soft);
}
.afe--coding-agent-flow .node--human rect {
  stroke: var(--afe-human);
  stroke-dasharray: 5 4;
}
.afe--coding-agent-flow .glyph {
  stroke: var(--afe-accent);
  stroke-width: 1.8;
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.afe--coding-agent-flow .node--human .glyph {
  stroke: var(--afe-human);
}
.afe--coding-agent-flow .node--ok .glyph {
  stroke: var(--afe-ok);
}
.afe--coding-agent-flow .edge-base,
.afe--coding-agent-flow .edge-flow,
.afe--coding-agent-flow .edge-hot {
  fill: none;
  stroke-linecap: round;
}
.afe--coding-agent-flow .edge-base {
  stroke: var(--afe-edge);
  stroke-width: 1.4;
  opacity: .34;
}
.afe--coding-agent-flow .edge-flow {
  stroke: var(--afe-edge);
  stroke-width: 1.9;
  stroke-dasharray: 5 9;
  opacity: .35;
  animation: caf-ambient 1.8s linear infinite;
}
.afe--coding-agent-flow .edge-flow--loop {
  stroke: var(--afe-warn);
}
.afe--coding-agent-flow .edge-hot {
  stroke: var(--afe-accent);
  stroke-width: 3;
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  opacity: 0;
  animation: caf-hot-edge 16s linear infinite;
  animation-delay: var(--wk, 0s);
}
.afe--coding-agent-flow .node .hot-ring {
  fill: transparent;
  stroke: var(--afe-accent);
  stroke-width: 2.5;
  opacity: 0;
  animation: caf-hot-node 16s linear infinite;
  animation-delay: var(--wk, 0s);
}
.afe--coding-agent-flow .pkt {
  fill: var(--afe-accent);
  opacity: 0;
  animation: caf-packet 16s linear infinite;
  animation-delay: var(--wk, 0s);
}
.afe--coding-agent-flow .pkt--loop {
  fill: var(--afe-warn);
}
.afe--coding-agent-flow .arrow {
  fill: var(--afe-edge);
}
.afe--coding-agent-flow .arrow--loop {
  fill: var(--afe-warn);
}
@keyframes caf-ambient {
  to { stroke-dashoffset: -14; }
}
@keyframes caf-hot-edge {
  0% { opacity: 0; stroke-dashoffset: 100; }
  1%, 7% { opacity: 1; }
  8% { opacity: 0; stroke-dashoffset: 0; }
  100% { opacity: 0; stroke-dashoffset: 0; }
}
@keyframes caf-hot-node {
  0%, 4% { opacity: 0; }
  5%, 11% { opacity: .95; }
  13%, 100% { opacity: 0; }
}
@keyframes caf-packet {
  0% { offset-distance: 0%; opacity: 0; }
  1%, 7% { opacity: 1; }
  8% { offset-distance: 100%; opacity: 0; }
  100% { offset-distance: 100%; opacity: 0; }
}
.afe--coding-agent-flow .st {
  opacity: 0;
  transform: translateY(6px);
  animation: caf-in .5s ease forwards;
}
.afe--coding-agent-flow .st-1 { animation-delay: .10s; }
.afe--coding-agent-flow .st-2 { animation-delay: .28s; }
.afe--coding-agent-flow .st-3 { animation-delay: .46s; }
.afe--coding-agent-flow .st-4 { animation-delay: .64s; }
.afe--coding-agent-flow .st-5 { animation-delay: .82s; }
.afe--coding-agent-flow .st-6 { animation-delay: 1.00s; }
.afe--coding-agent-flow .st-7 { animation-delay: 1.18s; }
.afe--coding-agent-flow .st-8 { animation-delay: 1.36s; }
.afe--coding-agent-flow .st-9 { animation-delay: 1.54s; }
@keyframes caf-in {
  to { opacity: 1; transform: none; }
}
.afe--coding-agent-flow figcaption {
  margin-top: .55rem;
  color: var(--afe-muted);
  font: 400 12.5px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
@media (prefers-reduced-motion: reduce) {
  .afe--coding-agent-flow * {
    animation: none !important;
    transition: none !important;
  }
  .afe--coding-agent-flow .st {
    opacity: 1;
    transform: none;
  }
  .afe--coding-agent-flow .edge-hot {
    opacity: .42;
    stroke-dashoffset: 0;
  }
  .afe--coding-agent-flow .node .hot-ring {
    opacity: .22;
  }
  .afe--coding-agent-flow .pkt {
    opacity: 0;
  }
}
</style>
<svg viewBox="0 0 920 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="caf-title caf-desc">
  <title id="caf-title">Coding agent 开发流程图</title>
  <desc id="caf-desc">流程从入口规则读取状态开始,经过状态扫描、任务包、producer 执行、确定性检查、独立评审和产品 eval。失败路径回到实现或任务包;通过后进入人类确认、closeout 和 capture loop,再把重复信号沉淀成下一轮任务或规则。</desc>
  <defs>
    <path id="caf-p1" d="M148 88 H224"/>
    <path id="caf-p2" d="M326 88 H394"/>
    <path id="caf-p3" d="M496 88 H570"/>
    <path id="caf-p4" d="M682 88 C730 88 738 156 738 188"/>
    <path id="caf-p5" d="M690 220 H574"/>
    <path id="caf-p6" d="M464 220 H342"/>
    <path id="caf-p7" d="M232 220 C184 220 166 292 208 328"/>
    <path id="caf-p8" d="M328 344 H426"/>
    <path id="caf-p9" d="M536 344 H628"/>
    <path id="caf-loop1" d="M520 262 C500 306 420 312 342 248"/>
    <path id="caf-loop2" d="M730 386 C704 452 236 452 184 382 C150 336 162 272 232 248"/>
  </defs>

  <rect class="lane st st-1" x="20" y="42" width="878" height="94" rx="12"/>
  <text class="lane-label st st-1" x="36" y="66">ENTRY / CONTEXT</text>
  <rect class="lane st st-2" x="20" y="174" width="878" height="96" rx="12"/>
  <text class="lane-label st st-2" x="36" y="198">BUILD / VERIFY</text>
  <rect class="lane st st-3" x="20" y="306" width="878" height="96" rx="12"/>
  <text class="lane-label st st-3" x="36" y="330">REVIEW / CLOSEOUT</text>

  <g class="node st st-1" style="--wk: 0s">
    <rect class="hot-ring" x="34" y="58" width="116" height="60" rx="10"/>
    <rect x="38" y="62" width="108" height="52" rx="8"/>
    <g class="glyph" transform="translate(50,76)">
      <path d="M0 0 h10 l5 5 v15 h-15 z"/><path d="M10 0 v5 h5"/><path d="M4 11 h8 M4 15 h7"/>
    </g>
    <text x="75" y="84">入口规则</text>
    <text class="sub" x="75" y="101">AGENTS.md</text>
  </g>

  <g class="node st st-2" style="--wk: 1.7s">
    <rect class="hot-ring" x="220" y="58" width="110" height="60" rx="10"/>
    <rect x="224" y="62" width="102" height="52" rx="8"/>
    <g class="glyph" transform="translate(238,77)">
      <circle cx="7" cy="7" r="6"/><path d="M12 12 l6 6"/>
    </g>
    <text x="265" y="84">状态扫描</text>
    <text class="sub" x="265" y="101">STATUS / TASKS</text>
  </g>

  <g class="node node--soft st st-3" style="--wk: 3.4s">
    <rect class="hot-ring" x="390" y="58" width="110" height="60" rx="10"/>
    <rect x="394" y="62" width="102" height="52" rx="8"/>
    <g class="glyph" transform="translate(408,76)">
      <path d="M0 2 h16 v18 h-16 z"/><path d="M4 7 h8 M4 12 h8 M4 17 h5"/>
    </g>
    <text x="435" y="84">任务包</text>
    <text class="sub" x="435" y="101">scope / gates</text>
  </g>

  <g class="node st st-4" style="--wk: 5.1s">
    <rect class="hot-ring" x="566" y="58" width="120" height="60" rx="10"/>
    <rect x="570" y="62" width="112" height="52" rx="8"/>
    <g class="glyph" transform="translate(584,77)">
      <circle cx="9" cy="9" r="5"/><path d="M9 0v3M9 15v3M0 9h3M15 9h3M2.5 2.5l2.2 2.2M13.3 13.3l2.2 2.2M15.5 2.5l-2.2 2.2M4.7 13.3l-2.2 2.2"/>
    </g>
    <text x="613" y="84">producer 执行</text>
    <text class="sub" x="613" y="101">build / run evidence</text>
  </g>

  <g class="node st st-5" style="--wk: 6.8s">
    <rect class="hot-ring" x="688" y="188" width="112" height="64" rx="10"/>
    <rect x="692" y="192" width="104" height="56" rx="8"/>
    <g class="glyph" transform="translate(706,208)">
      <path d="M2 10 l5 5 l11 -13"/>
    </g>
    <text x="733" y="214">确定性检查</text>
    <text class="sub" x="733" y="232">test / build / smoke</text>
  </g>

  <g class="node node--soft st st-6" style="--wk: 8.5s">
    <rect class="hot-ring" x="462" y="188" width="116" height="64" rx="10"/>
    <rect x="466" y="192" width="108" height="56" rx="8"/>
    <g class="glyph" transform="translate(480,207)">
      <circle cx="8" cy="5" r="4"/><path d="M0 20 c0-6 4-9 8-9 s8 3 8 9"/>
    </g>
    <text x="508" y="214">独立评审</text>
    <text class="sub" x="508" y="232">reviewer / grader</text>
  </g>

  <g class="node st st-7" style="--wk: 10.2s">
    <rect class="hot-ring" x="230" y="188" width="116" height="64" rx="10"/>
    <rect x="234" y="192" width="108" height="56" rx="8"/>
    <g class="glyph" transform="translate(248,207)">
      <path d="M0 18 h18"/><path d="M3 18 V8 M9 18 V3 M15 18 v-12"/>
    </g>
    <text x="276" y="214">产品 eval</text>
    <text class="sub" x="276" y="232">quality / false-safe</text>
  </g>

  <g class="node node--human st st-8" style="--wk: 11.9s">
    <rect class="hot-ring" x="204" y="320" width="128" height="64" rx="10"/>
    <rect x="208" y="324" width="120" height="56" rx="8"/>
    <g class="glyph" transform="translate(222,339)">
      <circle cx="8" cy="5" r="4"/><path d="M0 20 c0-6 4-9 8-9 s8 3 8 9"/>
    </g>
    <text x="252" y="346">人类确认</text>
    <text class="sub" x="252" y="364">irreversible gates</text>
  </g>

  <g class="node node--ok st st-9" style="--wk: 13.6s">
    <rect class="hot-ring" x="424" y="320" width="116" height="64" rx="10"/>
    <rect x="428" y="324" width="108" height="56" rx="8"/>
    <g class="glyph" transform="translate(442,339)">
      <path d="M2 10 l5 5 l11 -13"/><path d="M2 20 h16"/>
    </g>
    <text x="471" y="346">closeout</text>
    <text class="sub" x="471" y="364">runs / reviews / state</text>
  </g>

  <g class="node st st-9" style="--wk: 15.0s">
    <rect class="hot-ring" x="626" y="320" width="116" height="64" rx="10"/>
    <rect x="630" y="324" width="108" height="56" rx="8"/>
    <g class="glyph" transform="translate(644,339)">
      <path d="M9 0 v20"/><path d="M1 8 c4-8 12 8 16 0"/><path d="M1 14 c4-8 12 8 16 0"/>
    </g>
    <text x="672" y="346">capture loop</text>
    <text class="sub" x="672" y="364">repeat signal → rule</text>
  </g>

  <g class="st st-2">
    <use href="#caf-p1" class="edge-base"/><use href="#caf-p1" class="edge-flow"/><use href="#caf-p1" class="edge-hot" style="--wk:.9s"/><path class="arrow" d="M224 88 l-8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:.9s; offset-path:path('M148 88 H224')"/>
  </g>
  <g class="st st-3">
    <use href="#caf-p2" class="edge-base"/><use href="#caf-p2" class="edge-flow"/><use href="#caf-p2" class="edge-hot" style="--wk:2.6s"/><path class="arrow" d="M394 88 l-8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:2.6s; offset-path:path('M326 88 H394')"/>
  </g>
  <g class="st st-4">
    <use href="#caf-p3" class="edge-base"/><use href="#caf-p3" class="edge-flow"/><use href="#caf-p3" class="edge-hot" style="--wk:4.3s"/><path class="arrow" d="M570 88 l-8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:4.3s; offset-path:path('M496 88 H570')"/>
  </g>
  <g class="st st-5">
    <use href="#caf-p4" class="edge-base"/><use href="#caf-p4" class="edge-flow"/><use href="#caf-p4" class="edge-hot" style="--wk:6.0s"/><path class="arrow" d="M738 188 l-5 -8 h10 z"/>
    <circle class="pkt" r="5" style="--wk:6.0s; offset-path:path('M682 88 C730 88 738 156 738 188')"/>
  </g>
  <g class="st st-6">
    <use href="#caf-p5" class="edge-base"/><use href="#caf-p5" class="edge-flow"/><use href="#caf-p5" class="edge-hot" style="--wk:7.7s"/><path class="arrow" d="M574 220 l8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:7.7s; offset-path:path('M690 220 H574')"/>
  </g>
  <g class="st st-7">
    <use href="#caf-p6" class="edge-base"/><use href="#caf-p6" class="edge-flow"/><use href="#caf-p6" class="edge-hot" style="--wk:9.4s"/><path class="arrow" d="M342 220 l8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:9.4s; offset-path:path('M464 220 H342')"/>
  </g>
  <g class="st st-8">
    <use href="#caf-p7" class="edge-base"/><use href="#caf-p7" class="edge-flow"/><use href="#caf-p7" class="edge-hot" style="--wk:11.1s"/><path class="arrow" d="M208 328 l-8 -4 l5 9 z"/>
    <circle class="pkt" r="5" style="--wk:11.1s; offset-path:path('M232 220 C184 220 166 292 208 328')"/>
  </g>
  <g class="st st-9">
    <use href="#caf-p8" class="edge-base"/><use href="#caf-p8" class="edge-flow"/><use href="#caf-p8" class="edge-hot" style="--wk:12.8s"/><path class="arrow" d="M426 344 l-8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:12.8s; offset-path:path('M328 344 H426')"/>
  </g>
  <g class="st st-9">
    <use href="#caf-p9" class="edge-base"/><use href="#caf-p9" class="edge-flow"/><use href="#caf-p9" class="edge-hot" style="--wk:14.2s"/><path class="arrow" d="M628 344 l-8 -4 v8 z"/>
    <circle class="pkt" r="5" style="--wk:14.2s; offset-path:path('M536 344 H628')"/>
  </g>

  <g class="st st-7">
    <use href="#caf-loop1" class="edge-base"/>
    <use href="#caf-loop1" class="edge-flow edge-flow--loop"/>
    <path class="arrow arrow--loop" d="M342 248 l9 -1 l-5 8 z"/>
    <text class="sub" x="430" y="302" text-anchor="middle" style="fill:var(--afe-warn);font-weight:700">needs-rework → 回到实现或任务包</text>
  </g>
  <g class="st st-9">
    <use href="#caf-loop2" class="edge-base"/>
    <use href="#caf-loop2" class="edge-flow edge-flow--loop"/>
    <path class="arrow arrow--loop" d="M232 248 l-9 -1 l5 8 z"/>
    <text class="sub" x="456" y="456" text-anchor="middle" style="fill:var(--afe-warn);font-weight:700">capture 生成后续任务或规则,再进下一轮</text>
  </g>
</svg>
<figcaption>这张图用一条“工作项”走完整个流程:入口规则、状态扫描、任务包、producer 执行、确定性检查、独立评审、产品 eval、人类确认、closeout、capture loop。蓝绿色高亮表示当前推进路径,黄色回路表示 rework 或流程规则反哺;人类确认节点用虚线框,表示这里不是自动流动,而是明确等待授权。</figcaption>
</figure>

这张图里有两个重点。

第一,流程的主线比“agent 写代码”长得多。写代码只是中间一段。前面要有状态恢复和任务授权,后面要有验证、独立评审、eval、closeout。少掉任何一段,下一轮 agent 都可能接错上下文。

第二,流程必须允许回炉。review 发现问题,不能靠一句“我修好了”直接穿过去;eval 暴露质量问题,也不能只改报告口径。回路是系统的一部分,不是流程失败的尴尬插曲。

## 入口规则只负责带 agent 到现场

一个 coding agent 进仓库时,最先需要的是入口动作,不是长篇项目介绍。

我会把入口规则写成很窄的几件事:

```text
1. Confirm the working directory is this repository.
2. Read STATUS.md for the current state.
3. Read TASKS.md for the task queue.
4. Read the relevant task packet under tasks/ if the work is tied to a non-trivial task.
5. Read only the additional source-of-truth files needed for the current task.
```

这几行不负责解释项目愿景,它们负责阻止 agent 从聊天历史里猜状态。聊天里说过“P0 基本完成”,不等于 repo 里已经有通过记录。agent 每次重进现场,都要先看当前状态、任务队列和任务包。

`dep-upgrade-agent` 里的 `AGENTS.md` 就是这个角色。它不会把所有状态都塞进去,只规定 agent 开工前该读哪些 source of truth,以及遇到冲突时要停。入口文件越想包办一切,越容易变成另一份过期文档。

## 状态面和任务面要分开

入口之后,agent 要先恢复两个视角。

`STATUS.md` 回答“现在项目实际在哪里”。它应该告诉下一轮 agent:当前 phase 是什么、哪些 milestone 已经被接受、有没有人类 gate、下一步是什么。

`TASKS.md` 回答“任务队列怎么走过来”。它是索引和历史,记录哪些任务关闭了,哪些任务还在等 review,哪些任务只是实现完成但没有 closeout。

这两个文件会有交叉,但不能混成一个。状态面太长,下一轮 agent 找不到当前判断;任务面太短,又恢复不了历史证据。

写这篇时,`dep-upgrade-agent` 的状态面和任务索引合起来给出的是: P0 已经被人类接受, P1a 进入 isolated execution;前几轮把真实执行 runtime、upgrade executor、`analyze --live --execute` 串起来,后面安全边界 hardening 已实现、通过 dedicated grader security review,并在 2026-07-03 完成人类 results-review / closeout。这里的具体任务编号以后会过期,但它展示了状态面该回答的问题:现在能不能继续,卡在哪个 gate,下一轮应该接哪里。

我以前会下意识多塞 context。后来发现,更重要的是把 context 写成可重新进入的形状。

## 非平凡需求先变成 task packet

小改动可以直接做。低风险、本地、范围清楚,agent 看完上下文就改,然后跑对应检查。

但只要任务会改变架构、依赖、执行环境、安全边界、eval 口径、外部事实或交接方式,就不应该直接让 agent 开写。先做 task packet。

一个可执行的 task packet 至少要讲清这些事:

```text
Goal
Context
Non-Goals
Scope
Source Of Truth
Expected Artifact
Acceptance Criteria / Done When
Eval Plan
Verification Plan
Review Gate
Stop Conditions
Allowed Changes
Disallowed Changes
Handoff
```

字段看起来多,但它们都在限制一种具体失控。

比如只说“把 P1a 做一下”,agent 很容易直接进入实现。写着写着,它会顺手决定执行运行时、untrusted code 边界、secret 处理、执行结果能不能当 ground truth、报告格式怎么变。每个决定都像是局部小事,合起来就是未经授权的架构变更。

task packet 的价值,就是把“这次能补的空白”和“必须停下来等人判断的空白”分开。Goal 约束目标,Non-Goals 约束不做什么,Scope 约束文件和模块边界,Stop Conditions 约束什么时候不能继续猜。

## 需求拆分看风险和证据

很多 agent workflow 会自然按目录拆任务:先 core,再 cli,再 tests,再 docs。这个拆法有时可以,但它抓不住真正的风险。

更好的拆分方式是问三件事:

- 这次引入了什么新风险?
- 需要什么新证据才能证明它成立?
- 哪些决定还没有授权?

`dep-upgrade-agent` 的 P0 一开始 bottom-up 推进: scaffold、Go detector、CLI report、Summary、Control、fake eval、real provider,一块块搭上去。每块都通过了检查,但后来复查时发现,它们加起来还不是 `SCOPE.md` 里的 P0。

真正的 P0 还需要对真实 `go.mod` 工作:从 Go proxy 解析版本,查 OSV/GHSA,抓 release notes、tag diff、CHANGELOG,把证据 freeze 成 bounded context。早期状态文件甚至把 registry/version resolution 记到了 P1。后来补 `P0-BREAKDOWN.md` 时,才把这个 drift 写出来,并经过人类确认。

这就是按风险拆分的例子。问题不在“哪个目录还没写”,而在“P0 的证据链还没闭合”。确认之后,拆分才变成 D1 候选检测、D2 证据获取、D3 Summary/Control、D4 报告、D5 eval、D6 hardening carry-forwards。

到了 P1a,新复杂度只有一个: isolated execution。于是边界就应该钉在执行隔离、baseline/upgrade build-test、报告和 eval 接入。code modification、PR、scheduler、第二生态都先不进来。

## 执行层要拆出 producer 和 evaluator

让同一个 agent 一边写实现、一边判断自己是否真的完成,风险很高。它刚构造完自己的解释,最容易把缺口补成合理路径。

所以流程里要把 producer 和 evaluator 分开。

producer 可以产出计划、代码、run evidence、状态更新。evaluator 默认只读被评估的 artifact,可以写 review/eval 记录,但不顺手修实现。

一个实现任务大概这样走:

```text
ready task packet
-> builder 按 scope 实施
-> builder 写 run evidence
-> deterministic checks 通过
-> reviewer / grader 独立读 task、diff、run、rubric
-> pass / pass-with-notes / needs-rework / escalate
-> maintainer closeout
```

如果 review 返回 `needs-rework`,任务回到 builder。改完后重新 verification,再 review。review 不跳过 verification,也不替 builder 悄悄修实现。

这条规则听起来有点重,但它解决的是一个很实际的问题:每一次“通过”都能在 repo 里找到证据。通过不靠“agent 说它看过了”,而是 task、run、review、状态都能对上。

## Eval 要分成工程检查和产品质量

工程检查和产品质量 eval 要分开看。

第一层是工程检查:typecheck、lint、build、unit test、CLI smoke、no-key deterministic gate。这些回答“实现有没有按工程规则跑起来”。在实现任务里,它们应该是 primary gate。

第二层是产品质量 eval。它回答“这个系统做出的判断是否可靠”。

对 `dep-upgrade-agent` 来说,这两层差别很明显。fake track 可以完全 deterministic,用冻结 case 保护 false-safe guard。real-model track 要真实调用模型,测 Summary extraction、Control on gold summary、overall accuracy、false safe 和 cost。

早期只看 fake eval,`overall_accuracy 3/3` 会显得很漂亮。真实模型跑起来后,问题才具体:Control 在 gold summary 下还可以,瓶颈反而在 Summary extraction 和 calibration。最后 P0 的质量门设成 Method B:

```text
false_safe_rate == 0/6
control_on_gold_summary_accuracy >= 5/6
summary_extraction_accuracy >= 4/6
overall_accuracy >= 3/6
```

这个门槛不完美,样本也小。但它至少能告诉我是哪一层坏了。单个 aggregate accuracy 做不到这件事。

到了 isolated execution 阶段,eval 又要升级。baseline 和 upgraded 版本能真实跑 build/test 后,case label 可以有 execution-produced ground truth。但这个 ground truth 也有边界:执行绿了,只说明当前测试覆盖下没破。测试没覆盖的行为仍然未知。这个限制要写进 label rationale,否则执行结果会变成新的幻觉来源。

## 人类 gate 要写进流程,不要藏在聊天里

不是所有事情都应该自动继续。

遇到这些情况,流程要明确等待人类确认:

- 改变长期架构或稳定协议;
- 新增依赖、执行环境、外部服务;
- 涉及 secrets、安全边界、生产或发布;
- 缩小原本已经接受的 scope;
- eval 阈值和产品质量口径需要取舍。

`dep-upgrade-agent` 里有些任务是 governed task,原因不一定是实现更复杂,而是它们会改变授权边界。安全边界 hardening 就是这种任务:实现侧可以交出 artifact,grader 也可以给 pass-with-notes,但 review notes 里仍然保留了需要人类看的结果,例如错误信息 redaction、残余 crash-leak window、egress enforcement 延后。人类看完并接受这些 low-risk follow-up 后,任务才 closeout。这个 gate 的结果必须写进任务和状态文件,不能只留在会话里。

人类 gate 不是“打断 agent”。它是让流程知道哪里不能自动推断。

## Closeout 才是一次任务真正上线

这里说的“上线”,不一定是生产部署。对一个 coding-agent 项目来说,很多时候上线是 phase delivery:这一轮工作已经被 repo 接住,下一轮 agent 可以安全接手。

closeout 要落到文件里:

- `runs/*.md`:本轮读了什么、改了什么、跑了什么检查、结果怎样;
- `reviews/*.md`:独立 review 的结论、风险、pass-with-notes;
- `tasks/*.md`:任务状态、eval result、handoff;
- `TASKS.md`:队列变化;
- `STATUS.md`:当前态变化;
- `PROGRESS.md`:阶段历史变化;
- `capture/ledger.md`:重复或严重信号。

一个例子是 P0 closeout。P0 最终关闭,靠的是 gate 里把 Method B at-threshold 结果和整体 P0 completion 一起做人类 ratification,不是某次聊天里说“差不多了”。`STATUS.md` 里记录了复查命令和接受记录。后面的 agent 不需要问我“P0 真的完了吗”,它能在 repo 里找到证据。

如果 closeout 缺失,下一轮 agent 只能猜。猜一次可能没事,猜多了项目状态就会变形。

## Capture loop 把重复摩擦变成规则

流程最后还有一层:把反复出现的问题升级成规则。

一次 review note 留在原任务里就够了。多次出现,就说明流程有洞。

`dep-upgrade-agent` 里有个很典型的信号:早期几个 implementation task 都把 defensive / negative tests 往后推。schema rejection、candidate mismatch、`maxChars` over-bound 这些 guard path,一开始都容易被 happy path 测试盖过去。

后来 task 0008 第一次 review 发现 missing evidence 还能被高置信 `auto_upgrade` 掩过去,于是 rework 加了 deterministic `evidenceMissing` guard,才通过 re-review。这个信号进了 capture ledger,变成 task 0011,最后写进 implementation rubric:

```text
When an implementation adds or changes validation, parsing, bounded-context checks,
false-safe guards, downgrade logic, or defensive failure handling,
deterministic checks include negative/guard tests for the new failure/guard paths,
or the task packet/run record explicitly justifies a scoped waiver.
```

这条规则改变了后面的默认行为。再有人加 parser、guard、false-safe、downgrade,就不能只交 happy path test,除非把 waiver 和 follow-up 写清楚。

这就是 capture loop 的价值:把“这次注意一下”变成“以后默认会检查”。

## 什么时候值得用这套流程

这套流程有成本。小脚本、一次性 demo、当天能写完又能全量理解的本地改动,不需要完整 task packet、独立 grader、run/review/closeout 全套。

我会在这些信号出现时启用它:

- 任务会跨会话,下一轮 agent 需要恢复状态;
- 任务会改变架构、依赖、执行环境、安全边界、稳定协议或 eval 口径;
- 任务结果会被后续 task 当成前提;
- 任务里有真实外部事实,比如价格、平台能力、API 行为、漏洞数据库;
- 失败会让项目产生错误信心,比如模型质量、false-safe、untrusted code execution;
- 同类问题已经在 review 里出现过两次以上。

它慢在前面,但省掉的是更贵的返工:上下文丢失、任务漂移、自评过松、没有验证却以为完成。

我现在对 coding agent 开发流程的判断很简单:不要把模型当成一次性写代码的人,要把它放进一个能恢复、能验收、能回炉、能留下证据的系统里。

`dep-upgrade-agent` 还不是成熟产品。但这套开发流程已经开始像一个能长期运转的系统了。这才是我这轮最想留下来的东西。
