---
title: "发布管线的三道门,和一张会动的流程图"
description: "给博客发布管线补齐三道门(独立 subagent 评审、链接图片机械 eval、人工验收);现成动图方案不合用,自建了 animated-flow-explainer,文中的流程图就是它生成的。"
date: "2026-07-02"
tags: ["agents", "publishing-pipeline", "eval", "svg-animation"]
visibility: "public"
period: "2026-07 第一周"
summary: "管线返工记录。评审改为强制独立 subagent,build 后加链接图片 eval,links 只收核心来源;现成动图方案不合用,自建了 animated-flow-explainer skill,文中那张会动的流程图就是它生成的。"
---

这周先没急着发新文章,把发布内容的流水线本身返工了一遍。起因是我翻自己的发布规则,看到评审环节写着"有 subagent 就用"。写稿的上下文自己演三个评审角色,自己给自己打分,这道门等于没关。

顺着这个线头往下捋,发现的问题更多。文章里的外链和图片从来没被机械检查过,哪条挂了只能等读者踩到。收藏页(links)也荒着,正文里引了二十多个来源,收藏页两周多只躺着三条。

## 三道门,两条配套规则

先把结构说破。改完的管线上有三道门,依次是独立评审、机械 eval、人工验收。人工验收原来就有,这次动的是前两道;另外补了两条配套规则,links 维护和写作弧线。

第一道门是评审,从"建议"改成了"必须"。editor、source、对抗三个评审,每个都要跑在独立 subagent 里,和写稿的上下文彻底隔开。跑不了 subagent 的环境可以降级成自查,但必须在 review 文件(每篇文章随稿的那份评审记录)里写明降级了。同一个上下文自评为什么不可信,道理不复杂,评审者知道作者的意图,就会替作者补完没写清的部分。

第二道门是新加的 eval。build 之后派一个独立的 eval subagent,只干机械活。文章里每条外链逐个请求,2xx 或 3xx 算过;站内链接和图片必须能在构建产物里找到对应文件,零字节算挂。它只报证据表,不改稿。有一条挂了,文章就到不了预览那一步。

第一条配套规则管 links 的维护。定的口径是只收核心来源,判断标准是"值不值得单独推荐给读者,并能写出一句它为什么重要"。文章围绕展开的那个视频、论点依赖的那篇文档,进 links,和文章同一个 manifest 一起走管线;顺手引的批量例证留在正文里就好。每条引用都要在 review 文件里记一笔收或不收,防止又荒回去。

第二条配套规则在写作端。实践类文章要把弧线走完,来源讲了什么、我具体做了什么、拿到了什么数据、验证了什么没验证什么、我怎么看。可以压缩措辞,不可以悄悄跳环节,某段真没有(比如还没实践)就直说。较这个真是因为,悄悄跳环节的文章给读者的只有结论,没法复核,也没法照着做。

## 一张会动的流程图

改完的管线用文字描述很绕,直接放图。流动的光点每 14 秒把整条流程走播一遍,走到哪个节点哪个节点点亮;琥珀色是两条回炉回路。

<figure class="afe afe--publish-pipeline" role="img" tabindex="0"
  aria-label="流程图:起草后进入三路并行 subagent 评审(editor、source、对抗),全部通过进门禁 agent-cleared,再 sync 加 build,eval subagent 校验链接图片,然后人工验收、发布。评审有 blocker 回炉重稿;eval 失败或人工拒绝则 needs-rework 并 revert 回炉。">
<style>
.afe--publish-pipeline {
  --afe-bg: #faf7f2; --afe-node: #ffffff; --afe-border: #d6cdbf;
  --afe-edge: #8a7a63; --afe-accent: #c2410c; --afe-loop: #9f7d18;
  --afe-ok: #3f6212; --afe-text: #292524; --afe-dim: #78716c;
  margin: 0; padding: 1rem 0; overflow-x: auto;
}
@media (prefers-color-scheme: dark) {
  .afe--publish-pipeline {
    --afe-bg: #1c1917; --afe-node: #292524; --afe-border: #44403c;
    --afe-edge: #a8a29e; --afe-accent: #fb923c; --afe-loop: #eab308;
    --afe-ok: #a3e635; --afe-text: #e7e5e4; --afe-dim: #a8a29e;
  }
}
.afe--publish-pipeline svg { display: block; width: 100%; min-width: 760px; height: auto; background: var(--afe-bg); border: 1px solid var(--afe-border); border-radius: 8px; }
.afe--publish-pipeline text { font: 600 13px/1 system-ui, sans-serif; fill: var(--afe-text); }
.afe--publish-pipeline .sub { font-weight: 400; font-size: 10.5px; fill: var(--afe-dim); }
.afe--publish-pipeline .tag { font-weight: 600; font-size: 10.5px; }
.afe--publish-pipeline .node rect { fill: var(--afe-node); stroke: var(--afe-border); stroke-width: 1.5; }
.afe--publish-pipeline .glyph { stroke: var(--afe-accent); stroke-width: 1.8; fill: none; stroke-linecap: round; stroke-linejoin: round; }
.afe--publish-pipeline .node--human rect { stroke-dasharray: 5 4; }
.afe--publish-pipeline .node--human .glyph { stroke: var(--afe-ok); }
.afe--publish-pipeline .edge-base { fill: none; stroke: var(--afe-edge); stroke-width: 1.5; opacity: .35; }
.afe--publish-pipeline .edge-flow { fill: none; stroke: var(--afe-edge); stroke-width: 2; stroke-dasharray: 5 9; stroke-linecap: round; animation: afe-flow 1.6s linear infinite; opacity: .35; }
.afe--publish-pipeline .edge-flow--loop { stroke: var(--afe-loop); animation-duration: 2.2s; opacity: .75; }
.afe--publish-pipeline .arrow { fill: var(--afe-edge); }
.afe--publish-pipeline .arrow--loop { fill: var(--afe-loop); }
@keyframes afe-flow { to { stroke-dashoffset: -14; } }
.afe--publish-pipeline .halo { fill: var(--afe-accent); opacity: 0; transform-origin: center; transform-box: fill-box; animation: afe-pulse 2.4s ease-in-out infinite; }
@keyframes afe-pulse { 0%,100% { opacity: 0; transform: scale(.92); } 50% { opacity: .16; transform: scale(1.08); } }
/* ---- master-timeline walkthrough: one 14s cycle, per-element delays ---- */
.afe--publish-pipeline .wk { animation: afe-hot 14s linear infinite; animation-delay: var(--wk, 0s); }
@keyframes afe-hot {
  0%, 9% { stroke: var(--afe-accent); stroke-width: 2.5; }
  13%, 100% { stroke: var(--afe-border); stroke-width: 1.5; }
}
.afe--publish-pipeline .pkt { fill: var(--afe-accent); stroke: var(--afe-bg); stroke-width: 2; opacity: 0; animation: afe-pkt 14s linear infinite; animation-delay: var(--wk, 0s); }
@keyframes afe-pkt {
  0% { offset-distance: 0%; opacity: 0; }
  0.7% { opacity: 1; }
  6.3% { opacity: 1; }
  7% { offset-distance: 100%; opacity: 0; }
  100% { offset-distance: 100%; opacity: 0; }
}
.afe--publish-pipeline .pub { opacity: .55; animation: afe-hot-op 14s linear infinite; animation-delay: var(--wk, 0s); }
@keyframes afe-hot-op { 0%, 8% { opacity: 1; } 12%, 100% { opacity: .55; } }
.afe--publish-pipeline .st { opacity: 0; animation: afe-in .5s ease forwards; }
.afe--publish-pipeline .st-1 { animation-delay: .1s; }  .afe--publish-pipeline .st-2 { animation-delay: .4s; }
.afe--publish-pipeline .st-3 { animation-delay: .7s; }  .afe--publish-pipeline .st-4 { animation-delay: 1s; }
.afe--publish-pipeline .st-5 { animation-delay: 1.3s; } .afe--publish-pipeline .st-6 { animation-delay: 1.55s; }
.afe--publish-pipeline .st-7 { animation-delay: 1.8s; } .afe--publish-pipeline .st-8 { animation-delay: 2.05s; }
.afe--publish-pipeline .st-9 { animation-delay: 2.3s; }
@keyframes afe-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.afe--publish-pipeline figcaption { font: 400 12.5px/1.5 system-ui, sans-serif; color: var(--afe-dim); margin-top: .5rem; }
@media (prefers-reduced-motion: reduce) {
  .afe--publish-pipeline * { animation: none !important; }
  .afe--publish-pipeline .st { opacity: 1; transform: none; }
  .afe--publish-pipeline .halo { opacity: .12; }
}
</style>
<svg viewBox="0 0 900 460" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <!-- stage 1: draft -->
  <g class="node st st-1">
    <rect class="wk" style="--wk:2.4s" x="40" y="93" width="140" height="64" rx="8"/>
    <g class="glyph" transform="translate(56,108)">
      <path d="M0 0 h9 l5 5 v13 h-14 z"/><path d="M9 0 v5 h5"/><path d="M3 10 h8 M3 14 h8"/>
    </g>
    <text x="84" y="119">起草 draft</text>
    <text class="sub" x="84" y="137">完整叙事 + brief</text>
  </g>
  <!-- stage 2: three parallel subagent reviews -->
  <g class="st st-2">
    <path class="edge-base" d="M180 118 C 230 118, 230 58, 280 58"/><path class="edge-flow" d="M180 118 C 230 118, 230 58, 280 58" pathLength="100"/><path class="arrow" d="M280 58 l-8 -4 v8 z"/>
    <path class="edge-base" d="M180 125 C 230 125, 230 146, 280 146"/><path class="edge-flow" d="M180 125 C 230 125, 230 146, 280 146" pathLength="100"/><path class="arrow" d="M280 146 l-8 -4 v8 z"/>
    <path class="edge-base" d="M180 132 C 230 132, 230 234, 280 234"/><path class="edge-flow" d="M180 132 C 230 132, 230 234, 280 234" pathLength="100"/><path class="arrow" d="M280 234 l-8 -4 v8 z"/>
    <g class="node">
      <rect class="wk" style="--wk:4.5s" x="280" y="30" width="160" height="56" rx="8"/>
      <g class="glyph" transform="translate(296,43)"><path d="M2 16 l10 -10 3 3 -10 10 -4 1 z"/><path d="M12 6 l3 3"/></g>
      <text x="324" y="54">editor 评审</text>
      <text class="sub" x="324" y="72">可读性 · 结构 · 标题</text>
    </g>
    <g class="node">
      <rect class="wk" style="--wk:4.5s" x="280" y="118" width="160" height="56" rx="8"/>
      <g class="glyph" transform="translate(296,131)"><circle cx="7" cy="7" r="5"/><path d="M11 11 l5 5"/></g>
      <text x="324" y="142">source 评审</text>
      <text class="sub" x="324" y="160">事实 · 来源可溯</text>
    </g>
    <g class="node">
      <rect class="wk" style="--wk:4.5s" x="280" y="206" width="160" height="56" rx="8"/>
      <g class="glyph" transform="translate(296,219)"><path d="M9 0 l8 3 v6 c0 5 -4 7 -8 9 c-4 -2 -8 -4 -8 -9 v-6 z"/><path d="M5 8 l3 3 5 -5"/></g>
      <text x="324" y="230">对抗评审</text>
      <text class="sub" x="324" y="248">隐私 · 风险 · 平庸</text>
    </g>
    <text class="tag" x="360" y="18" text-anchor="middle" style="fill: var(--afe-dim)">三路独立 subagent 并行</text>
  </g>
  <!-- stage 3: converge to gate -->
  <g class="st st-3">
    <path class="edge-base" d="M440 58 C 485 58, 485 138, 530 138"/><path class="edge-flow" d="M440 58 C 485 58, 485 138, 530 138" pathLength="100"/><path class="arrow" d="M530 138 l-8 -4 v8 z"/>
    <path class="edge-base" d="M440 146 H530"/><path class="edge-flow" d="M440 146 H530" pathLength="100"/><path class="arrow" d="M530 146 l-8 -4 v8 z"/>
    <path class="edge-base" d="M440 234 C 485 234, 485 154, 530 154"/><path class="edge-flow" d="M440 234 C 485 234, 485 154, 530 154" pathLength="100"/><path class="arrow" d="M530 154 l-8 -4 v8 z"/>
    <g class="node">
      <rect class="wk" style="--wk:7s" x="530" y="114" width="170" height="64" rx="8"/>
      <g class="glyph" transform="translate(546,129)"><rect x="0" y="0" width="14" height="18" rx="2"/><path d="M3 5 h8 M3 9 h8"/><path d="M3 13 l2 2 4 -4"/></g>
      <text x="574" y="140">agent-cleared</text>
      <text class="sub" x="574" y="158">评分达标 · 0 blocker</text>
    </g>
  </g>
  <!-- loop A: review blockers back to draft -->
  <g class="st st-4">
    <path class="edge-base" d="M360 30 C 320 4, 150 4, 110 93"/>
    <path class="edge-flow edge-flow--loop" d="M360 30 C 320 4, 150 4, 110 93" pathLength="100"/>
    <path class="arrow arrow--loop" d="M110 93 l-4 -8 h8 z"/>
    <text class="tag" x="196" y="20" text-anchor="middle" style="fill: var(--afe-loop)">有 blocker → 回炉重稿</text>
  </g>
  <!-- stage 5: sync + build -->
  <g class="st st-5">
    <path class="edge-base" d="M615 178 V300"/><path class="edge-flow" d="M615 178 V300" pathLength="100"/><path class="arrow" d="M615 300 l-4 -8 h8 z"/>
    <g class="node">
      <rect class="wk" style="--wk:9s" x="540" y="300" width="160" height="64" rx="8"/>
      <g class="glyph" transform="translate(556,315)">
        <circle cx="9" cy="9" r="5"/>
        <path d="M9 0v3M9 15v3M0 9h3M15 9h3M2.6 2.6l2.1 2.1M13.3 13.3l2.1 2.1M15.4 2.6l-2.1 2.1M4.7 13.3l-2.1 2.1"/>
      </g>
      <text x="584" y="326">sync + build</text>
      <text class="sub" x="584" y="344">content:sync · build</text>
    </g>
  </g>
  <!-- stage 6: eval subagent (current focus: pulse halo) -->
  <g class="st st-6">
    <path class="edge-base" d="M540 332 H460"/><path class="edge-flow" d="M540 332 H460" pathLength="100"/><path class="arrow" d="M460 332 l8 -4 v8 z"/>
    <g class="node">
      <rect class="halo" x="304" y="295" width="162" height="74" rx="12"/>
      <rect class="wk" style="--wk:10.9s" x="310" y="300" width="150" height="64" rx="8"/>
      <g class="glyph" transform="translate(326,315)">
        <rect x="0" y="2" width="18" height="14" rx="2"/><circle cx="5" cy="7" r="1.5"/><path d="M2 13 l4 -4 3 3 4 -5 3 4"/>
      </g>
      <text x="354" y="326">eval subagent</text>
      <text class="sub" x="354" y="344">链接/图片全通过?</text>
    </g>
  </g>
  <!-- stage 7: human gate (dashed = waiting, no motion) -->
  <g class="st st-7">
    <path class="edge-base" d="M310 332 H250"/><path class="edge-flow" d="M310 332 H250" pathLength="100"/><path class="arrow" d="M250 332 l8 -4 v8 z"/>
    <g class="node node--human">
      <rect class="wk" style="--wk:13.1s" x="110" y="300" width="140" height="64" rx="8"/>
      <g class="glyph" transform="translate(124,315)"><circle cx="7" cy="5" r="4"/><path d="M-1 19 c0-5 4-8 8-8 s8 3 8 8"/></g>
      <text x="152" y="326">人工验收</text>
      <text class="sub" x="152" y="344">preview → OK?</text>
    </g>
  </g>
  <!-- loop B: eval fail / human reject -> rework rail -->
  <g class="st st-8">
    <path class="edge-base" d="M385 364 V420 H68 V157"/>
    <path class="edge-flow edge-flow--loop" d="M385 364 V420 H68 V157" pathLength="100"/>
    <path class="edge-base" d="M180 364 V420"/>
    <path class="edge-flow edge-flow--loop" d="M180 364 V420" pathLength="100"/>
    <path class="arrow arrow--loop" d="M68 157 l-4 8 h8 z"/>
    <text class="tag" x="255" y="442" text-anchor="middle" style="fill: var(--afe-loop)">eval 挂 / 人工拒绝 → needs-rework · revert sync</text>
  </g>
  <!-- stage 9: publish (only after human OK, explicit request) -->
  <g class="st st-9">
    <path class="edge-base" d="M180 300 V258"/><path class="edge-flow" d="M180 300 V258" pathLength="100"/>
    <path class="arrow pub" d="M180 250 l-4 8 h8 z" style="fill: var(--afe-ok); --wk:15.2s"/>
    <text class="tag pub" x="180" y="240" text-anchor="middle" style="fill: var(--afe-ok); --wk:15.2s">发布 gh-pages</text>
  </g>
  <!-- walkthrough packets (one full process per 14s cycle) -->
  <g aria-hidden="true">
    <circle class="pkt" r="5" style="--wk:3.5s; offset-path: path('M180 118 C 230 118, 230 58, 280 58')"/>
    <circle class="pkt" r="5" style="--wk:3.5s; offset-path: path('M180 125 C 230 125, 230 146, 280 146')"/>
    <circle class="pkt" r="5" style="--wk:3.5s; offset-path: path('M180 132 C 230 132, 230 234, 280 234')"/>
    <circle class="pkt" r="5" style="--wk:6s; offset-path: path('M440 58 C 485 58, 485 138, 530 138')"/>
    <circle class="pkt" r="5" style="--wk:6s; offset-path: path('M440 146 L530 146')"/>
    <circle class="pkt" r="5" style="--wk:6s; offset-path: path('M440 234 C 485 234, 485 154, 530 154')"/>
    <circle class="pkt" r="5" style="--wk:8.1s; offset-path: path('M615 178 L615 300')"/>
    <circle class="pkt" r="5" style="--wk:10.2s; offset-path: path('M540 332 L460 332')"/>
    <circle class="pkt" r="5" style="--wk:12.1s; offset-path: path('M310 332 L250 332')"/>
    <circle class="pkt" r="5" style="--wk:14.3s; offset-path: path('M180 300 L180 254')"/>
  </g>
</svg>
<figcaption>my-blog 发布管线:流动的光点每 14 秒完整走播一轮流程(起草,三路并行评审,agent-cleared 门禁,sync + build,eval subagent 校验链接图片,人工验收,发布),走到哪个节点哪个节点点亮;背景暗色虚线只表示通道方向。琥珀色是两条回炉回路,评审有 blocker 回炉重稿,eval 失败或人工拒绝则 needs-rework 并 revert 已同步内容;虚线框的人工验收表示「等待中,无自动流动」。</figcaption>
</figure>

这张图本身也是这次的产出。我想要能内嵌进 markdown 的动图,节点带语义图标,连线动画对应真实流向;Mermaid 那种方框加箭头满足不了。先找了现成的,本地已有的工具产出的都是完整的独立页面;社区里最接近的是 [architecture-diagram-skill](https://github.com/konraddzbik/architecture-diagram-skill)(MIT,数据包动画、分步点亮都有),可惜输出同样是独立交互页面,嵌进文章得套 iframe。

最后自建了一个,叫 animated-flow-explainer。默认输出就是上面那种片段,一个 figure 标签,scoped CSS 加内联 SVG,零外部依赖。走播的实现比想象中省事,所有元素挂同一条 14 秒的 CSS 动画时间轴,各自错开延迟,包飞完一段,下一站的节点描边刚好点亮。不用 JS。

## 验证了什么,没验证什么

图过了四项检查。桌面 1280 和移动 375 宽度无重叠,暗色主题配色正确,reduced-motion 下动画全停但整图仍完整可读,console 无报错。移动端走横向滚动,不硬缩。

两件事还没验证。RSS 阅读器会怎么处理这段内嵌 style 和 SVG,大概率动画被剥掉,退化成什么样没测过。外链 eval 对反爬严格的站点会不会误报,规则里写了 HEAD 被拒就换 GET 重试,但还没遇到真实案例。

## 落点

这轮返工让我确认了一个分法。判断类检查(值不值得发、论证撑不撑得住)交给独立评审,机械类检查(链接通不通、图片在不在)交给 eval 按清单跑,两类混在同一个环节里,哪个都不可信。

动图那边单独记一条。连线的流动要对应真实的流向,走播要对应真实的阶段顺序,动画一旦和过程脱钩,就只剩装饰价值。

管线变重了一点,一篇文章要过三道评审加一道 eval 才见得到人。目前我的判断是值得,返工一篇已经发出去的错文章,比多跑四个 subagent 贵得多。先记到这。
