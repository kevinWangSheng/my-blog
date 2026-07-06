---
title: "怎么评估一个 agent skill 该不该改"
description: "一套评估 agent skill 该不该改的流程,和我按它跑的一次实践:冻结变体、盲配对、双判官打分、端到端。核心教训是别用一个和被测系统同源的单判官下结论。"
date: "2026-07-06"
tags: ["agents", "skills", "eval", "llm-judge"]
visibility: "public"
series: "Agent systems"
---

手里有一份 agent skill——就是给 coding agent 的一份指令文件,规定它在某类任务里怎么做事。用久了会想改它:要么觉得它太长太啰嗦,要么怀疑里面很多规则模型早就默认会做。但"感觉该改"和"改了不掉质量"是两回事。凭感觉动一份天天在用的 skill,风险不小。

这篇讲怎么用一套 eval 流程把这件事测清楚:先说这套流程本身长什么样,再说我按它跑的一次实践,包括具体怎么打分、分数是多少。

## 理论:一套 skill eval 流程

评一份 skill 该不该改,核心是回答一个问题:改完之后,质量掉不掉、边界破不破。可以拆成五步。

**第一步,冻结变体。** 把 skill 做成几个版本:原版当基线,再加一到几个候选(比如更短的、重构过的),最好再加一个"完全不给 skill"的地板参照。全部冻结在独立目录里,别动线上那份。变体之间只有 skill 不同,其它都一样。

**第二步,准备任务。** 找一批有代表性的输入(fixture),覆盖这份 skill 实际会遇到的几类用法。合成任务好复现、好控制;真实素材更逼真,能逼出 skill 在"乱且长"的材料上的差别。两种都要有。

**第三步,两条测试线。** 一条是局部:给所有变体喂同一份输入,产出匿名成 A、B,做盲配对。这测的是"给定同样的输入,不同版本写出来的东西质量差多少"。另一条是端到端:给一个原始输入(比如一个链接),让 agent 自己去取材、自己一路做到成品。这测的是真实使用流程里,skill 前后端都靠自己时会怎样。局部干净可控,端到端逼真但更吵。

**第四步,多判官打分。** 盲评:判官只看题目、评分表和匿名的 A/B,不知道谁是谁,按几个维度打分。这一步有个坑,后面会专门讲:别只用一个和被测系统同源的判官。

**第五步,综合决策。** 把质量差、硬伤(编造/泄露/越界)、以及成本(长度、维护、上下文占用)放一起,再决定改不改、怎么改。质量打平但成本差很多时,决策就清楚了。

这套流程不复杂,难的是老老实实每步都做,尤其是不给自己省掉第四步里的交叉验证。

<figure class="afe afe--evalflow">
<style>
.afe--evalflow{margin:2rem 0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
.afe--evalflow *{box-sizing:border-box}
.afe--evalflow{--bg:#f7f7f4;--panel:#fff;--ink:#1c1e22;--soft:#5d626b;--line:#dad8d0;--same:#b0483a;--cross:#1f6f6b;--ship:#2f7d4f;--track:#c7c5bd;--shadow:0 1px 2px rgba(20,25,25,.06),0 6px 20px rgba(20,25,25,.05)}
@media (prefers-color-scheme:dark){.afe--evalflow{--bg:#15171b;--panel:#1c1f24;--ink:#e7e8ea;--soft:#9aa0a8;--line:#2c3038;--same:#e0776a;--cross:#5ec7bf;--ship:#63c088;--track:#3a3f47;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 26px rgba(0,0,0,.4)}}
.afe--evalflow .wrap{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:20px 18px 14px;box-shadow:var(--shadow);overflow-x:auto}
.afe--evalflow .wrap:focus-visible{outline:2px solid var(--cross);outline-offset:2px}
.afe--evalflow .board{min-width:680px}
.afe--evalflow svg{width:100%;height:auto;display:block}
.afe--evalflow .cap{color:var(--soft);font-size:12.5px;line-height:1.55;margin:12px 4px 2px}
.afe--evalflow .cap b{color:var(--ink)}
.afe--evalflow .lbl{fill:var(--ink);font-size:14px;font-weight:650}
.afe--evalflow .sub{fill:var(--soft);font-size:11.5px}
.afe--evalflow .vd{font-size:13px;font-weight:750}
.afe--evalflow .box{fill:var(--panel);stroke:var(--line);stroke-width:1.5}
.afe--evalflow .glyph{fill:none;stroke:var(--soft);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.afe--evalflow .same .box{stroke:var(--same);fill:color-mix(in srgb,var(--same) 9%,var(--panel))}
.afe--evalflow .same .lbl,.afe--evalflow .same .vd{fill:var(--same)}
.afe--evalflow .same .glyph{stroke:var(--same)}
.afe--evalflow .cross .box{stroke:var(--cross);fill:color-mix(in srgb,var(--cross) 10%,var(--panel))}
.afe--evalflow .cross .lbl,.afe--evalflow .cross .vd{fill:var(--cross)}
.afe--evalflow .cross .glyph{stroke:var(--cross)}
.afe--evalflow .ship .box{stroke:var(--ship);fill:color-mix(in srgb,var(--ship) 12%,var(--panel))}
.afe--evalflow .ship .lbl{fill:var(--ship)}
.afe--evalflow .ship .glyph{stroke:var(--ship)}
.afe--evalflow .edge{stroke:var(--track);stroke-width:2;fill:none}
.afe--evalflow .flow{stroke-width:2;fill:none;stroke-linecap:round;stroke-dasharray:4 8;stroke:var(--soft);animation:afe-run 1.2s linear infinite}
.afe--evalflow .flow.r{stroke:var(--same)}
.afe--evalflow .flow.c{stroke:var(--cross)}
@keyframes afe-run{to{stroke-dashoffset:-24}}
@media (prefers-reduced-motion:reduce){.afe--evalflow .flow{animation:none}}
</style>
<div class="wrap" tabindex="0" role="group" aria-label="Skill eval 流程图:冻结变体后走局部盲配对和端到端两条线,再由同源与异源两个判官打分,得出相反结论,最后综合决策">
<div class="board">
<svg viewBox="0 0 760 300" xmlns="http://www.w3.org/2000/svg" role="img"><title>Skill eval 流程:变体到局部盲配对与端到端,再到同源判官(短版赢)与异源判官(打平)的相反结论,最后综合决策</title>
<g>
<path class="edge" d="M150 150 C172 150 174 92 196 92"/>
<path class="edge" d="M150 150 C172 150 174 236 196 236"/>
<path class="edge" d="M340 92 C360 92 362 60 380 60"/>
<path class="edge" d="M340 92 C360 92 362 128 380 128"/>
<path class="edge" d="M540 60 C566 60 566 140 588 148"/>
<path class="edge" d="M540 128 C566 128 566 148 588 152"/>
<path class="edge" d="M340 236 C470 236 468 172 588 158"/>
<path class="flow" d="M150 150 C172 150 174 92 196 92"/>
<path class="flow" d="M150 150 C172 150 174 236 196 236"/>
<path class="flow r" d="M340 92 C360 92 362 60 380 60"/>
<path class="flow c" d="M340 92 C360 92 362 128 380 128"/>
<path class="flow r" d="M540 60 C566 60 566 140 588 148"/>
<path class="flow c" d="M540 128 C566 128 566 148 588 152"/>
<path class="flow" d="M340 236 C470 236 468 172 588 158"/>
</g>
<g transform="translate(20,116)">
<rect class="box" x="0" y="0" width="130" height="68" rx="10"/>
<path class="glyph" d="M18 20 h20 l6 6 v26 h-26 z M24 34 h20 M24 42 h20"/>
<text class="lbl" x="82" y="30" text-anchor="middle">冻结变体</text>
<text class="sub" x="82" y="50" text-anchor="middle">原版+候选+地板</text>
</g>
<g transform="translate(196,64)">
<rect class="box" x="0" y="0" width="144" height="56" rx="10"/>
<path class="glyph" d="M16 18 h16 v20 h-16z M20 24 h8 M20 30 h8"/>
<text class="lbl" x="86" y="24" text-anchor="middle">局部盲配对</text>
<text class="sub" x="86" y="42" text-anchor="middle">同输入 A/B</text>
</g>
<g transform="translate(196,208)">
<rect class="box" x="0" y="0" width="144" height="56" rx="10"/>
<path class="glyph" d="M26 28 a10 10 0 1 0 .01 0 M26 28 l6 -4"/>
<text class="lbl" x="88" y="24" text-anchor="middle">端到端</text>
<text class="sub" x="88" y="42" text-anchor="middle">裸输入自抓</text>
</g>
<g class="same" transform="translate(380,32)">
<rect class="box" x="0" y="0" width="160" height="56" rx="10"/>
<path class="glyph" d="M16 40 l10 -22 l10 22 M18 40 h16 M26 18 v-5"/>
<text class="lbl" x="94" y="24" text-anchor="middle">同源判官</text>
<text class="vd" x="94" y="43" text-anchor="middle">判:短版赢</text>
</g>
<g class="cross" transform="translate(380,100)">
<rect class="box" x="0" y="0" width="160" height="56" rx="10"/>
<path class="glyph" d="M26 40 l-8 -22 M26 40 l8 -22 M18 18 h16 M26 18 v-5"/>
<text class="lbl" x="94" y="24" text-anchor="middle">异源判官</text>
<text class="vd" x="94" y="43" text-anchor="middle">判:打平</text>
</g>
<g class="ship" transform="translate(588,116)">
<rect class="box" x="0" y="0" width="152" height="68" rx="10"/>
<path class="glyph" d="M18 22 l14 -6 l14 6 v18 l-14 6 l-14 -6z M18 22 l14 6 l14 -6 M32 28 v18"/>
<text class="lbl" x="92" y="30" text-anchor="middle">综合决策</text>
<text class="sub" x="92" y="50" text-anchor="middle">质量打平,砍</text>
</g>
<text class="sub" x="462" y="20" text-anchor="middle" font-style="italic">同一批输出,两种判决</text>
</svg>
</div>
<p class="cap"><b>同源单判官会骗你。</b> 同一批匿名输出,和被测系统同家族的判官判"短版明显赢",换一个异源判官判"打平"——差异来自同源判官偏爱精简,压低了又长又密的原版。加一个异源判官,结论直接翻案。这也是为什么第四步的交叉验证省不得。</p>
</div>
</figure>

## 实践:我按这套流程跑了一次

我拿一份三百多行的 skill 试了一遍。它是那种典型的"操作手册":模板、规则、检查清单、一堆自评门,能塞的都塞了。我想知道它能不能大幅砍短。

**变体**这样切:原版(371 行)当基线;一个重构版(79 行,把大部分细节从主文件下沉到按需加载的引用文件);一个极简版(31 行,只留最核心的边界和硬门禁);还有一个中间版(37 行);外加一个完全不给 skill 的地板。

**任务**用了五个:四个合成任务(把脑暴、源笔记、踩坑故事写成成品),外加一个真实素材——一段一小时的技术访谈转录,让它整理成一篇文章。合成的负责可复现,真实的负责逼真。

**局部盲配对**:每个任务里,把原版和某个候选的产出匿名成 A、B,随机排序,交给判官只按八个维度打分、选胜者。判官看不到哪个是长版哪个是短版。

一开始我图省事,只用了一个判官:再起一个和生成同一套工具链的实例来当评委。

### 打分:第一个判官说的话不能全信

单判官跑完,结论很干脆,而且一边倒:短版更好,几乎每一对里短版都压过长版。候选普遍 4.6 以上,原版垫底,最好的候选到 4.74。看着就是"砍就对了,越短越好"。

我差点信了。但有个地方不对劲:评委和选手是同一个模型家族。要注意,问题不是它偏袒"自家产出"——长版和短版都是同一套工具链生成的,真偏袒的话该一起抬高才对,解释不了为什么只有长版被压。真正的问题更朴素:这个判官带着和生成方一样的风格口味,它就是偏爱精简紧凑的写法。于是它给短候选打高,给那份又长又密的原版打低。这是一种风格偏好,不是判官在偏袒同族。

于是我加了第二个判官,换一个不同家族的模型来重评同样几组对。同一批匿名产出,结论直接被掀了。下面每行是一次独立的盲 A/B 配对(所以基线每行的分数本就不同),每格是"候选分 / 基线分",八维均分满分 5:

| 候选 | 同源判官 | 异源判官 |
| --- | --- | --- |
| 重构版(79 行) | 4.74 / 4.51 | 4.63 / 4.63 |
| 极简版(31 行) | 4.64 / 4.47 | 4.65 / 4.60 |
| 中间版(37 行) | 4.65 / 4.53 | 4.60 / 4.75 |

关键在基线那两列。同源判官把这个又长又密的原版压在 4.5 上下;换成异源判官,它就爬到 4.6 到 4.75。候选自己的分数在两家之间变化不大(动得最多的重构版也就 0.11);真正被同源判官系统性压低的,是那份长版。也就是说,短版排在前面不是因为它分高,而是因为同源判官把长版打低了。换一个公正的判官,长版分数就回来了。

真正被掀翻的不是分数大小,是方向。同源判官下,短版在几乎每一对里都压过长版,一边倒,看着像个真信号。换成异源判官,这个"短压长"的方向就散了:有的候选略高、有的反而略低,散在基线上下。那个一致的方向来自判官的口味,不来自文字本身的好坏。几个版本其实都挤在 4.5 到 4.75 的窄带里,谁也没明显更好或更差。砍到很短不掉质量,但也不是"短就更好"。

这一条我认为比"砍了多少行"值钱得多:别用一个和被测系统同源的单判官下结论,它会用一个看起来很自信的分数骗你。加一个异源判官,成本很低,能直接翻案。

## 端到端:让它自己从原始输入跑到成品

到这一步测的还只是"给定同一段文字,版本长短影响质量"。但真实用起来,skill 得自己去取材、判断、再产出。这些前后端我一直手动替它做了(先把素材整理好再喂进去),等于没测。

于是我加了第二条线:直接把一个原始链接当输入,让 agent 自己联网、自己抓取原始素材、自己清洗、自己做到成品,把只读沙箱换成带网络和可写目录的模式。每个变体各跑一遍。

这条线跑出两个结论。

一是边界很稳。所有变体,包括最短的极简版和完全不给 skill 的地板,都自己抓到了素材,把原文里那些夸张的数字当成"原作者的说法"而不是已证实的事实,老实标注自动转写里可能出错的名字和数值,不编造、不越界、不泄露本地信息。连不给 skill 都做对了。这说明现在的强模型在"守边界"这件事上默认就不差,skill 的边际价值主要集中在那些模型不会默认做对的地方,而不是重复它已经会的东西。

二是一个我没预料到的失效。原版和几个较长的候选里都有一道"独立评审门":产出前自动再起一个实例给草稿打分把关。可在这个端到端环境里,这道门全部跑不起来——嵌套的实例起不来,报权限错误。带这道门的变体都老实报告了"评审门没跑成",没有一个假装通过。

这就有点讽刺:那套看起来最严谨、最负责任的重门禁,在真实流程里是死的。它写在指令里读着很安心,但不交付。长不等于稳,重门禁不等于真保障。

## 结果与诚实的缺口

综合下来:质量打平、零硬伤、重门禁在真实流程里失效。于是我把线上那份从三百多行砍到几十行,细节下沉到按需加载的引用文件。

但我不想把话说满,几个缺口得摆出来:

- 每个任务只跑了一遍,每对只有一个判官打分,样本量小,结论是方向性的强信号,不是统计意义上的定论。
- 只测了产出质量和边界,没测触发——也就是这份 skill 会不会在该用的时候被正确激活,那是另一套测法。
- 这次是一份写作类 skill 的经验;换一份门禁是安全关键的 skill,砍之前得更保守。

## 带走的几条

- 好 skill 是删出来的。先问每一行:模型默认不看它会不会照做?会,就是废话。只有部分场景才用的细节,下沉到单独文件按需加载,别常驻主文件。
- 别用同源单判官下结论。它和生成方共享同一套风格口味,会给你一个一致但虚假的排名,方向是错的。加一个异源判官,成本很低,能直接翻案。
- 写在 skill 里让人安心的重门禁,不一定在真实流程里跑得起来。把它当端到端测一遍,别默认它有效。
- 强模型默认就守很多边界。把字数花在模型真不会默认做对的地方。
- 连给文章配的图,也要过一遍对抗检查——数字对不对、画得清不清楚,都得有人专门挑。省了这一步,漏的往往就是最显眼的那个问题。
