---
title: "Agent 工程的两个循环"
description: "完整解析 AI Engineer 大会 Mutagent 的 talk:七个阶段、两个循环怎么把 agent 的迭代交给 agent 跑;eval 为什么是终止条件;诊断怎么在百万 traces 下活下来。含视频关键 slides。"
date: "2026-07-02"
tags: ["agents", "eval", "agent-engineering", "video-notes"]
visibility: "public"
---
这篇是对一场 talk 的完整解析,AI Engineer 大会上 Mutagent 的 CEO Benedikt Sanftl 和 CTO Burak(视频开场两人如此自我介绍)合讲的 [The Agentic AI Engineer](https://www.youtube.com/watch?v=pSto5YaNGUo),35 分钟。他们要回答的问题只有一个,agent 的迭代循环能不能也交给 agent 来跑。下面按演讲顺序把内容讲完,配图截自视频里的 slides;最后一节才是我自己的评注,和视频内容分开。

https://www.youtube.com/watch?v=pSto5YaNGUo

## 为什么:人是循环里的瓶颈

今天构建 agent 的迭代周期大多靠人手动转。出一个 issue,改实现(用 coding agent 的话叫 vibe implement),给新特性造测试样本,肉眼翻 traces 看结果长什么样,再 AB 测试上线。每一环的反馈都靠人,一圈下来很慢,瓶颈就是 human review 和人的构建时间。组织里如果打算铺开上百个 agent,这个人力上限直接封死迭代速度。

他们给了一张吞吐量对比图。同一个时间窗口,人跑循环以周为单位,能塞进 12 个开发周期;agent 跑循环以分钟为单位,能塞 242 个。每个周期都可能让 agent 变好一点,所以 slides 上那句话说得很重,throughput is the moat,吞吐量就是护城河。

![吞吐量对比:人以周为单位 12 个周期,agent 以分钟为单位 242 个周期](/my-blog/images/agent-engineering-two-loops/01-throughput.webp)
*视频 03:00 画面,© Mutagent(AI Engineer 大会)*

## 全景:七个阶段,两条入口,两个循环

整套生命周期是七个阶段,spec、build、eval、ship、monitor、diagnose、optimize,由一个 orchestrator 从头串到尾。左进右出:进的是新需求或意图(冷启动路径),或者存量 agent 的 bug、事故、增强需求(存量路径);出的是 code PR、agent 更新、skill 更新。

发布前的那半边是离线循环,构建和评估往复到全绿;发布后进入在线循环,监控、诊断、优化、再评估。我把这个框架画成了下面这张图。

<figure class="afe afe--two-loops" role="img" tabindex="0"
  aria-label="流程图:两个循环。离线循环里 spec 定义后构建,构建与评估往复,评估全绿才上线;上线后进入在线循环,监控 traces、诊断根因、生成修改与新评估,回到评估,全绿再部署。流动的光点循环走播 评估、上线、监控、诊断、优化 这条主环。">
<style>
.afe--two-loops {
  --afe-bg: #faf7f2; --afe-node: #ffffff; --afe-border: #d6cdbf;
  --afe-edge: #8a7a63; --afe-accent: #c2410c; --afe-loop: #9f7d18;
  --afe-ok: #3f6212; --afe-text: #292524; --afe-dim: #78716c;
  margin: 0; padding: 1rem 0; overflow-x: auto;
}
@media (prefers-color-scheme: dark) {
  .afe--two-loops {
    --afe-bg: #1c1917; --afe-node: #292524; --afe-border: #44403c;
    --afe-edge: #a8a29e; --afe-accent: #fb923c; --afe-loop: #eab308;
    --afe-ok: #a3e635; --afe-text: #e7e5e4; --afe-dim: #a8a29e;
  }
}
.afe--two-loops svg { display: block; width: 100%; min-width: 760px; height: auto; background: var(--afe-bg); border: 1px solid var(--afe-border); border-radius: 8px; }
.afe--two-loops text { font: 600 13px/1 system-ui, sans-serif; fill: var(--afe-text); }
.afe--two-loops .sub { font-weight: 400; font-size: 10.5px; fill: var(--afe-dim); }
.afe--two-loops .tag { font-weight: 600; font-size: 10.5px; }
.afe--two-loops .node rect { fill: var(--afe-node); stroke: var(--afe-border); stroke-width: 1.5; }
.afe--two-loops .glyph { stroke: var(--afe-accent); stroke-width: 1.8; fill: none; stroke-linecap: round; stroke-linejoin: round; }
.afe--two-loops .edge-base { fill: none; stroke: var(--afe-edge); stroke-width: 1.5; opacity: .35; }
.afe--two-loops .edge-flow { fill: none; stroke: var(--afe-edge); stroke-width: 2; stroke-dasharray: 5 9; stroke-linecap: round; animation: afe-flow 1.6s linear infinite; opacity: .35; }
.afe--two-loops .edge-flow--loop { stroke: var(--afe-loop); animation-duration: 2.2s; opacity: .75; }
.afe--two-loops .arrow { fill: var(--afe-edge); }
.afe--two-loops .arrow--loop { fill: var(--afe-loop); }
@keyframes afe-flow { to { stroke-dashoffset: -14; } }
.afe--two-loops .wk { animation: afe-hot 14s linear infinite; animation-delay: var(--wk, 0s); }
@keyframes afe-hot {
  0%, 9% { stroke: var(--afe-accent); stroke-width: 2.5; }
  13%, 100% { stroke: var(--afe-border); stroke-width: 1.5; }
}
.afe--two-loops .pkt { fill: var(--afe-accent); stroke: var(--afe-bg); stroke-width: 2; opacity: 0; animation: afe-pkt 14s linear infinite; animation-delay: var(--wk, 0s); }
@keyframes afe-pkt {
  0% { offset-distance: 0%; opacity: 0; }
  0.7% { opacity: 1; }
  6.3% { opacity: 1; }
  7% { offset-distance: 100%; opacity: 0; }
  100% { offset-distance: 100%; opacity: 0; }
}
.afe--two-loops .st { opacity: 0; animation: afe-in .5s ease forwards; }
.afe--two-loops .st-1 { animation-delay: .1s; }  .afe--two-loops .st-2 { animation-delay: .35s; }
.afe--two-loops .st-3 { animation-delay: .6s; }  .afe--two-loops .st-4 { animation-delay: .9s; }
.afe--two-loops .st-5 { animation-delay: 1.15s; } .afe--two-loops .st-6 { animation-delay: 1.4s; }
.afe--two-loops .st-7 { animation-delay: 1.65s; } .afe--two-loops .st-8 { animation-delay: 1.9s; }
@keyframes afe-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.afe--two-loops figcaption { font: 400 12.5px/1.5 system-ui, sans-serif; color: var(--afe-dim); margin-top: .5rem; }
@media (prefers-reduced-motion: reduce) {
  .afe--two-loops * { animation: none !important; }
  .afe--two-loops .st { opacity: 1; transform: none; }
}
</style>
<svg viewBox="0 0 900 430" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <!-- zone tags -->
  <g class="st st-8">
    <text class="tag" x="255" y="40" text-anchor="middle" style="fill: var(--afe-dim)">离线循环 · 发布前</text>
    <text class="tag" x="600" y="40" text-anchor="middle" style="fill: var(--afe-dim)">在线循环 · 发布后</text>
  </g>
  <!-- spec (entry, one-time) -->
  <g class="node st st-1">
    <rect x="20" y="187" width="120" height="56" rx="8"/>
    <g class="glyph" transform="translate(36,202)">
      <path d="M0 0 h9 l5 5 v13 h-14 z"/><path d="M9 0 v5 h5"/><path d="M3 10 h8 M3 14 h8"/>
    </g>
    <text x="64" y="213">spec 规格</text>
    <text class="sub" x="64" y="231">职责 · 判据</text>
  </g>
  <!-- entry edge spec -> build -->
  <g class="st st-2">
    <path class="edge-base" d="M140 205 C 168 205, 168 108, 190 108"/><path class="edge-flow" d="M140 205 C 168 205, 168 108, 190 108" pathLength="100"/><path class="arrow" d="M190 108 l-8 -4 v8 z"/>
  </g>
  <!-- build -->
  <g class="node st st-2">
    <rect x="190" y="80" width="130" height="56" rx="8"/>
    <g class="glyph" transform="translate(206,95)"><path d="M6 3 l-5 6 5 6"/><path d="M12 3 l5 6 -5 6"/></g>
    <text x="234" y="105">build 构建</text>
    <text class="sub" x="234" y="123">harness 可替换</text>
  </g>
  <!-- offline inner loop build <-> eval -->
  <g class="st st-3">
    <path class="edge-base" d="M235 136 V294"/><path class="edge-flow" d="M235 136 V294" pathLength="100"/><path class="arrow" d="M235 294 l-4 -8 h8 z"/>
    <path class="edge-base" d="M275 294 V136"/><path class="edge-flow edge-flow--loop" d="M275 294 V136" pathLength="100"/><path class="arrow arrow--loop" d="M275 136 l-4 8 h8 z"/>
    <text class="tag" x="255" y="382" text-anchor="middle" style="fill: var(--afe-loop)">评估不过 → 改了再评</text>
  </g>
  <!-- eval (cycle junction) -->
  <g class="node st st-3">
    <rect class="wk" style="--wk:2.4s" x="190" y="294" width="140" height="56" rx="8"/>
    <g class="glyph" transform="translate(206,309)"><rect x="0" y="0" width="14" height="18" rx="2"/><path d="M3 5 h8 M3 9 h8"/><path d="M3 13 l2 2 4 -4"/></g>
    <text x="234" y="319">eval 评估</text>
    <text class="sub" x="234" y="337">二元判据 · 数据集</text>
  </g>
  <!-- e1 eval -> ship -->
  <g class="st st-4">
    <path class="edge-base" d="M330 322 C 385 322, 385 108, 420 108"/><path class="edge-flow" d="M330 322 C 385 322, 385 108, 420 108" pathLength="100"/><path class="arrow" d="M420 108 l-8 -4 v8 z"/>
  </g>
  <!-- ship -->
  <g class="node st st-4">
    <rect class="wk" style="--wk:4.7s" x="420" y="80" width="130" height="56" rx="8"/>
    <g class="glyph" transform="translate(436,95)"><path d="M0 10 L18 2 L11 17 L8 11 z"/><path d="M18 2 L8 11"/></g>
    <text x="464" y="105">ship 上线</text>
    <text class="sub" x="464" y="123">eval 全绿才走</text>
  </g>
  <!-- e2 ship -> monitor -->
  <g class="st st-5">
    <path class="edge-base" d="M550 108 H650"/><path class="edge-flow" d="M550 108 H650" pathLength="100"/><path class="arrow" d="M650 108 l-8 -4 v8 z"/>
  </g>
  <!-- monitor -->
  <g class="node st st-5">
    <rect class="wk" style="--wk:7s" x="650" y="80" width="130" height="56" rx="8"/>
    <g class="glyph" transform="translate(666,95)"><rect x="0" y="2" width="18" height="13" rx="2"/><path d="M2 9 h4 l2 -4 3 8 2 -4 h3"/></g>
    <text x="694" y="105">monitor 监控</text>
    <text class="sub" x="694" y="123">traces · 触发</text>
  </g>
  <!-- e3 monitor -> diagnose -->
  <g class="st st-6">
    <path class="edge-base" d="M715 136 V294"/><path class="edge-flow" d="M715 136 V294" pathLength="100"/><path class="arrow" d="M715 294 l-4 -8 h8 z"/>
  </g>
  <!-- diagnose -->
  <g class="node st st-6">
    <rect class="wk" style="--wk:9.3s" x="650" y="294" width="140" height="56" rx="8"/>
    <g class="glyph" transform="translate(666,309)"><circle cx="7" cy="7" r="5"/><path d="M11 11 l5 5"/></g>
    <text x="694" y="319">diagnose 诊断</text>
    <text class="sub" x="694" y="337">根因聚类</text>
  </g>
  <!-- e4 diagnose -> optimize -->
  <g class="st st-7">
    <path class="edge-base" d="M650 322 H550"/><path class="edge-flow" d="M650 322 H550" pathLength="100"/><path class="arrow" d="M550 322 l8 -4 v8 z"/>
  </g>
  <!-- optimize -->
  <g class="node st st-7">
    <rect class="wk" style="--wk:11.6s" x="420" y="294" width="130" height="56" rx="8"/>
    <g class="glyph" transform="translate(436,309)"><path d="M0 4 h16"/><circle cx="5" cy="4" r="2"/><path d="M0 10 h16"/><circle cx="11" cy="10" r="2"/><path d="M0 16 h16"/><circle cx="7" cy="16" r="2"/></g>
    <text x="464" y="319">optimize 优化</text>
    <text class="sub" x="464" y="337">修改 + 新评估</text>
  </g>
  <!-- e5 optimize -> eval -->
  <g class="st st-8">
    <path class="edge-base" d="M420 322 H330"/><path class="edge-flow" d="M420 322 H330" pathLength="100"/><path class="arrow" d="M330 322 l8 -4 v8 z"/>
  </g>
  <!-- walkthrough packets: main cycle eval->ship->monitor->diagnose->optimize->eval -->
  <g aria-hidden="true">
    <circle class="pkt" r="5" style="--wk:3.7s; offset-path: path('M330 322 C 385 322, 385 108, 420 108')"/>
    <circle class="pkt" r="5" style="--wk:6s; offset-path: path('M550 108 L650 108')"/>
    <circle class="pkt" r="5" style="--wk:8.3s; offset-path: path('M715 136 L715 294')"/>
    <circle class="pkt" r="5" style="--wk:10.6s; offset-path: path('M650 322 L550 322')"/>
    <circle class="pkt" r="5" style="--wk:12.9s; offset-path: path('M420 322 L330 322')"/>
  </g>
</svg>
<figcaption>Mutagent 讲的双循环:左边是离线循环,新意图从 spec 进入,构建和评估往复到全绿;上线后进入在线循环,监控、诊断、优化、再评估。按视频里的说法,新的评估判据会长回 spec 和评估集;我据此把两个循环画成共用同一道 eval 门。</figcaption>
</figure>

官方 slides 上的全景版本长这样,信息更全,两条入口和右侧的产出都在:

![The AI Engineer 全生命周期图:冷启动与存量两条入口,七个阶段,右侧输出 code PR 与 agent/skill 更新](/my-blog/images/agent-engineering-two-loops/02-lifecycle-map.webp)
*视频 06:35 画面,© Mutagent(AI Engineer 大会);动图没画的两条入口和右侧产出,这张全景图上都有*

## spec:把 why 和 how 写进同一份文件

spec 阶段要捕获需求,尤其是成功判据。输入是 business context、intent/goal、constraints 三样;文件里 DEFINE 的部分写为什么做和「good 是什么意思」(也就是验收判据),DESIGN 的部分写 agent 的形状,routines、工具、决策逻辑。还要写清 agent 负责什么、不负责什么,以及边界和约束。

签署后的 spec 是后续所有阶段的基准。slides 上的总结是,Build 照着它写,Evaluate 按它定义的 good 打分,Optimize 要打败它。另外 spec 是环境特化的,不同公司同类 agent 处理的流程差别很大,所以这份文件必须捕获你自己环境里的 context 需求和集成需求。

![spec 阶段 slide:define why + design how,business context/intent/constraints 汇入签署的 spec](/my-blog/images/agent-engineering-two-loops/03-spec.webp)
*视频 07:55 画面,© Mutagent(AI Engineer 大会)*

## build:让 coding agent 生成 agent

spec 告诉 coding agent 造什么,目标平台随你选。coding agent 拿着 spec 产出 agent 的初版,可以定制到任何平台上跑。slides 上列的支持面:生成端是 Claude Code、Codex、Cursor、Pi、Hermes 这类 coding agent;运行端本地跑在你的 coding agent 里,云上跑在托管框架里(Claude、Vercel、Mastra、DeepAgents)。

![build 阶段 slide:签署的 spec 交给你选的 coding agent 生成 agent,同一个 agent 可在本地或云端任意 harness 上跑](/my-blog/images/agent-engineering-two-loops/03b-build.webp)
*视频 09:00 画面,© Mutagent(AI Engineer 大会)*

spec 和实现隔离的理由来自他们自己的经历。他们做了三年 agent,时不时被框架或 harness 的能力边界卡住,要等上游解决,一等就很久;他们的判断是现在这批框架一年左右可能就要换(talk 里点名了 Hermes、deep agents 这波更替)。spec 不绑实现,换 harness 的时候需求不用重写。

## eval:把 good 变成可测量的

这是全场讲得最重的部分。他们管这叫 eval-driven development,对应写代码的 TDD。出发点是 agent 需要终止条件,「什么时候算够好」,等价于代码的单元测试,这是你验证 agent 能不能用的方式。

### 判据和用例从哪来

评估系统由两部分组成,判据(criteria)和用例集(datasets)。判据有两个来源:GUIDED,冷启动时和团队一起从 spec 里定,不需要数据;DISCOVERED,从生产 traces 里推导,成功的运行告诉你该保住什么,失败的告诉你该检查什么。用例也有两个来源:SYNTHESIZE,从 spec、历史导出或已知好例合成;DISTILL,从真实 traces 里蒸馏有代表性的。

他们特别强调评估集写不全是常态。别指望开工前和领域专家把评估集预猜完整,真正完整的评估集是发现的产物,来自用户反馈和生产失败的持续沉淀,边角 case 和硬 case 大多从这里来。

slides 上给了评估面板的样子:用例逐条 pass/fail,判据每条都是二元检查(引用了真实来源、无编造事实、用对了工具、输出格式合法、遵守政策),最后汇成一个 0 到 100 的成功率给循环去追。

![eval 系统 slide:判据 GUIDED/DISCOVERED 两来源,用例 SYNTHESIZE/DISTILL 两来源,右侧二元检查面板与 61/100 成功率](/my-blog/images/agent-engineering-two-loops/04-eval-system.webp)
*视频 12:20 画面,© Mutagent(AI Engineer 大会)*

### 为什么这一步必须 agent 化

一个 200 条的用例集,没有自动 evals,靠人眼滚 observability dashboard 和日志,每轮评估时间被拉得很长;要评的特性一多,想快、想并行都不可能,人就是瓶颈。所以让 evaluator agent 去筛 traces,你的工作变成设计这些循环,给每个循环配上清晰的 eval 门或者说终止门。

### 评什么:每一层都要打分

agent 是一整条运行轨迹,所以每一层都要打分。大多数 agent 失败在最终答案里根本看不出来,藏在它走的路径、调的工具、拿到的上下文和跑在其上的 harness 里。具体检查:context 是否完整,agent 有没有拿到端到端完成任务所需的全部上下文;轨迹里每个工具输出要逐步链检,一次错误的工具输出就足以把最终输出带歪;harness 对 agent 行为影响很大,本身也是一个优化向量。要整体评,不评孤立点。

![评估层次 slide:trajectory、tool calls 与 outputs、context、harness 四层都要打分](/my-blog/images/agent-engineering-two-loops/05-grade-layers.webp)
*视频 16:10 画面,© Mutagent(AI Engineer 大会)*

### 什么样的 eval 值得信

slides 给了一条 ONE RULE,被测的 agent 永远不给自己打分,evaluator 必须独立,否则等于给自己的作业盖章。往下是四个属性:Falsifiable,能被证伪,一个具体的 pass/fail 回答;Reproducible,低方差,确定性的 judge,锁住 judge 的模型、prompt 和 seed,让分数量的是 agent 而不是裁判噪声;Valid,绑定真实结果,不是看起来漂亮的代理指标;Actionable,失败要能定位原因。

actionable 这条给了正反例。「Helpfulness: 7.3/10」不可行动,数字每次跑都会漂,你学不到该改什么;「每条断言都引用了真实来源?挂」是可行动的,挂了就点名了缺口,下一轮知道修什么。这也是二元判据好过打分的原因,除非 rubric 写得极好,分数不告诉你修什么。LLM 当 judge 还必须校准方差,LLM 不是确定性的,同一个 judge 对同一个问题两次跑出不同结论,你就没法下结论说改进版比初版好。

![eval 可信度 slide:ONE RULE 被测者不自评,四属性 Falsifiable/Reproducible/Valid/Actionable,及可行动与不可行动的对照例](/my-blog/images/agent-engineering-two-loops/06-eval-trust.webp)
*视频 17:45 画面,© Mutagent(AI Engineer 大会)*

## 上线之后:ship、monitor、diagnose

ship 的形态可以是一次代码更新、agent 平台上的直接更新,或本地 harness agent 的更新。talk 对 ship 本身着墨不多,没有展开灰度或回滚,重心都压在门上。上线后 agent 被持续监控,按触发条件启动自动诊断,触发可以基于 trace 量,也可以是每日每周的定时任务。

诊断在规模下怎么活。你读不完一百万条失败 traces,让 LLM 通读的成本比执行本身还贵。做法是三步:Cluster,把长得像的失败聚成簇,几百条 trace 归成一簇,没有人一条条读;Categorize,按失败种类给每簇打标,missing context、wrong tool、off-path,每个桶对应一个可修的原因;Rank,按影响排序,先修最大的原因,不是最响的症状。slides 上的示例量级,missing context 1.2k 次、wrong tool use 880、off-path looping 610、unsupported claim 430、format/policy miss 210。

![诊断规模化 slide:百万失败 traces 经 cluster/categorize/rank 收敛为按影响排序的原因短名单](/my-blog/images/agent-engineering-two-loops/07-diagnose-scale.webp)
*视频 20:40 画面,© Mutagent(AI Engineer 大会)*

失败模式会沉淀。前期有一笔先付成本,要深读 LLM traces 才知道发生了什么;随着时间给每种失败模式积累出「代码可检的指标」,某些特定内容片段或特定工具调用序列一出现就知道要出事,之后大部分诊断不再需要 LLM 读 trace,配合代表性采样(多层过滤,先让 LLM 浅读一小部分判断有没有明显问题,再决定聚焦哪个失败模式),成本才压得住。另外还有 guided search 模式,你自己或用户报了一个具体问题,diagnostics 就定向找同类事故的全部发生。

诊断的产出有两样,先是能检测这类失败的新评估判据,然后才是针对性的修复。新判据会长回 spec、agent 和评估集,每个 agent 的历史失败数据持续积累,随时可查。

## optimize:只有赢家能上线

有了评估集,自主优化循环才能转起来。变更特性、更新提示或工具,甚至跑 auto-research 式的实验(自动生成多个变体分别去测),候选版本要过一道 success gate,两个条件,分数过线,而且赢过当前线上版本。过了就自动 ship 成 v+1;没过回 optimize 再迭代。关键在于每过一次,v+1 就成了新 baseline,下一个候选要打败它,bar 只会往上走。build、eval、optimize 这个内环自己转,收益是叠加的,不是每轮清零。

![优化阶段 slide:build→eval→success gate(过线且赢过线上版)→ship v+1,失败回 optimize 迭代](/my-blog/images/agent-engineering-two-loops/08-optimize-gate.webp)
*视频 22:45 画面,© Mutagent(AI Engineer 大会)*

## 产品与 demo

他们把这套做成了产品。以下是转述,我没用过,不评价。

部署形态:跑在你自己的环境里,本地和云都行,以 agent 的形式装进你已有的 coding agent,traces 和代码不离开你的机器。证据源的连接器覆盖 Langfuse、Datadog、LangSmith 等六家主流观测平台(完整名单见下图),事故也可以从 ticketing 系统或 Slack 进来。一个 orchestrator 给每个阶段派一个 agent,目前 evaluator 和 diagnostics 两个处于 research preview,其余阶段的 agent 还在做。输出端写向 GitHub 自动 PR、coding agent 的 md 文件(Claude Code、Codex、Cursor)、agent 框架(Mastra、DeepAgents)或托管服务;后面会出托管平台。

![产品环境 slide:六家观测平台连接器,orchestrator 每阶段一个 agent,evaluator 与 diagnostics 两个 research preview,输出到 GitHub/md/框架/托管](/my-blog/images/agent-engineering-two-loops/09-environment.webp)
*视频 25:30 画面,© Mutagent(AI Engineer 大会)*

demo 演示的是 diagnostics agent,在 Claude Code 里跑。启动后先给一个 dashboard,列出可用阶段、代码库里已有的 agents 和既有配置;输入 diagnose 触发诊断,范围可以指到某个 agent,也可以指到某个 skill(比如诊断某技能的全部调用);traces 从你配置的源拉取,LangFuse、本地的 Claude transcripts,或者观测平台导出的 JSONL 都行。

产出是一份 HTML 诊断报告。overview 列出检出的问题和给定时间窗内的出现频率;每个失败模式一个 tab,带问题解释、一条递归的 why 链(告诉你问题从哪里来)、修复建议(多选,可以只挑推荐项);还有一个 assumptions block,因为读 traces 时不一定有代码权限,LLM 做了哪些假设都列出来,错了人可以当场纠正。

![demo 诊断报告:失败模式 F-001 的问题描述、证据 trace、递归 why 链](/my-blog/images/agent-engineering-two-loops/10-demo-finding.webp)
*视频 32:05 画面,© Mutagent(AI Engineer 大会)*

走完所有问题后是 decisions 页,有个通用反馈框,对速记类工具友好,直接对麦克风说也行;确认后把全部修复决定生成一份 markdown 任务书,回到终端交给你的 coding agent 去执行。闭环到此接上,诊断的产出直接变成下一轮 build 的输入。

![demo decisions 页:通用反馈框加实时预览的修复任务书 markdown,一键复制交给 coding agent](/my-blog/images/agent-engineering-two-loops/11-demo-decisions.webp)
*视频 33:50 画面,© Mutagent(AI Engineer 大会)*

## 我的评注

以下三条是我的判断,不是视频内容。

「eval 是终止条件」这个说法比「eval 是质量分」有用得多。终止条件必须二元、可执行,循环才知道什么时候停;打分制的评估集在这个视角下是个残缺的循环控制器。他们那个 7.3/10 的反例值得贴在墙上。

ONE RULE(被测者不自评)是全场我最认同的一条。评审者知道作者的意图,就会不自觉替作者补完没写清的部分,独立上下文是唯一干净的解。我自己博客的发布管线用的是同款规则(独立 subagent 评审,过程记在[《发布管线的三道门,和一张会动的流程图》](/my-blog/logs/publish-pipeline-three-gates/)),这里不展开。

保留意见一条。他们展望的终局是评估全绿就自动部署,但评估集又是发现的产物,冷启动阶段覆盖率撑不起「值得托付」这四个字,这两个说法之间的张力视频里轻轻带过了。公平地说,他们现在的产品留着人工勾选决策的门,矛盾说的是终局愿景。个人博客错一篇没多大成本,尚且要人看一眼预览;生产 agent 想撤人工门,前提条件比这苛刻得多。我先按保留意见记着。
