# Review: 让 agent 连跑几小时的是 harness,不是模型

## Metadata

- status: publish-ready
- source paths / source records:
  - Anthropic workshop transcript + understanding notes (harness-lab/video-source/, local research pack)
  - Practice artifacts: harness-lab/voyager/ (git history, harness/SETUP_LOG.md, harness/logs/timeline.tsv, test-results.json, harness/screenshots/)
  - Practice artifacts: harness-lab/kanban/ (cold-start bug case)
- refreshed/primary sources:
  - Anthropic — Build Agents That Run for Hours (AI Engineer 2026): https://www.youtube.com/watch?v=mR-WAvEPRwE
- proposed collection: essays
- proposed slug: harness-that-runs-for-hours
- source type: research-derived + public-original (learning + hands-on practice)
- target reader: 在做 coding-agent harness / loop engineering,想知道"agent 连跑数小时"背后的机制、且关心验证怎么不被骗的工程师
- planned publishable markdown path: docs/content-pipeline/manifests/harness-that-runs-for-hours/harness-that-runs-for-hours.md
- planned manifest dir: docs/content-pipeline/manifests/harness-that-runs-for-hours/

## Public thesis

- memorable sentence: 让 agent 连跑几小时的不是模型某次灵光一现,是一套把建造与评审对抗、把验证钉死在实测上、并允许你回头读原始 trace 的系统。
- reader decision helped: 搭 PGE harness 时,把力气花在哪——尤其"验证读什么字段"和"别信绿色 dashboard"。
- strongest counterpoint / edge case: 强模型下功能轴几乎一轮就过,看起来 harness 的多轮价值被稀释了;文中正面回应——价值移动到了主观设计轴与跨轨回归兜底。

## Complete-story check (required for learning/practice-derived items)

- [x] what the source (video) actually said is covered — 上半场逐块讲 PGE、三失败原因、rubric、契约、solo-vs-harness 实证、读 trace、减肥表、五 takeaways
- [x] what I actually practiced is concrete — __VOYAGE__ 契约、72 准则、Kepler oracle、对抗审计作弊清单、measured 加固逐项、run-loop verdict bug 修法
- [x] real results/data/outputs are included — 2h 收敛、iter 时长、60/60、假收敛 trace 原文、19fps 回归、VOYAGER 真实截图
- [x] verified vs. untested claims are separated — 明确"我验证了 X;强模型把多轮压到设计轴是我的判断"
- [x] my own post-practice judgment is present — 五条教训 + 结尾
- missing stages explicitly declared: 无缺失阶段。

## Draft direction

已完成的长文草稿(20KB,17 节),上/下半场结构,五张图(2 原创 SVG + 3 实践截图)。

## Rewrite plan

### Keep
- 完整故事弧;两条核心教训(measured 验证 / 读 trace 抓假收敛);真实 trace 与数字。

### Remove / anonymize
- 不暴露本地绝对路径(review metadata 里保留,正文只用相对文件名如 harness/logs/iter-5-design.txt 作为示意)。
- 不贴 Anthropic 官方 slide(公开版用原创图解替代)。

### Add / refresh
- 三轮 subagent 评审的 blocker 逐条回填。

## Project/public evidence table

| claim | evidence URL/path | date checked | supported? | unsupported claim removed? |
|---|---|---|---|---|
| 视频存在且主题一致 | https://www.youtube.com/watch?v=mR-WAvEPRwE | 2026-07-02 | yes(标题/讲者/主题) | n/a |
| METR p50 3.7≈1h→4.6≈12h | 视频转录 + understanding notes | 2026-07-02 | 转述自视频,标注为"视频引 METR" | n/a |
| VOYAGER 72/72、2h 收敛 | voyager/ git log + timeline.tsv + test-results.json(本地) | 2026-07-02 | yes(本地实证,截图/日志) | n/a |

## Required publishable frontmatter plan

Shared:
- title: 让 agent 连跑几小时的是 harness,不是模型
- description: (见草稿 frontmatter)
- date: 2026-07-02
- tags: agents / harness / eval / loop-engineering / systems
- visibility: public

Collection-specific (essays):
- series: Agent systems
- canonical: 无

## Fact refresh checklist

- [x] Fast-moving vendor/model/protocol claims checked or scoped — METR/时长数字明确标为"视频所述",非本人 benchmark;模型能力表述转述自视频。
- [x] Benchmark/metric claims refreshed or removed — 保留但归因到视频。
- [x] Security claims phrased defensively — 无攻击性内容。
- [x] Hypothetical examples labeled — 无虚构示例;作弊场景标为"一个偷懒的 builder 会…"。
- [x] Public links/repo/demo/result claims verified — 仅一个公开链接(YouTube);VOYAGER 未宣称公开 demo/repo。

## Safety checklist

- [x] No secrets/tokens/keys.
- [x] No private marker / forbidden publish marker.
- [x] No private person/company data.
- [x] No fabricated project result / user feedback / repo/demo / endorsement — VOYAGER 结果均为本地可追溯实证,未夸大为对外产品。
- [x] Internal KB/local paths kept in review metadata, not in public prose — 正文只出现相对文件名示意(如 run-loop.sh),不含 /Users/ 绝对路径。

## Editorial quality rubric

| item | score | note |
|---|---:|---|
| Thesis | 2 | 尖锐、可记,标题=论点(editor) |
| Reader payoff | 2 | §17 五条可执行 |
| Specificity | 2 | 72 准则/34min/19fps/grep bug |
| Structure | 2 | 上下半场弧;上半场略长但完整故事弧为硬要求,保留 |
| Source grounding | 2 | 修掉 Opus/Sonnet 3.7 矛盾后达 2(修前 editor 给 1) |
| Judgment density | 2 | tradeoff/边界显式 |
| Voice | 2 | §9 note-tone 已改 |
| Safety/privacy | 2 | 无泄漏/绝对路径(adversarial+factual 确认) |
| Freshness | 2 | 加"视频所述、未独立复核"口径后达 2(修前 1) |

Total: 18/18(三轮修完回填;≥14 可 sync,≥16 可发布)

## Review loop

### Editor review
- reviewer: subagent(独立)
- pass: yes(修完 blocker 后;初判 16/18 no,唯一 blocker 已修 → 预计 17–18)
- blockers: §2 "Opus 3.7" 与时间线 "Sonnet 3.7" 自相矛盾(无 Opus 3.7)→ 已改为 Sonnet 3.7。
- major edits: 上半场复述偏重;§9 逐字搬 takeaways+私记语气 → 已重写折进自述;"读trace/全绿≠对"重复 → §9 折叠后减少。上半场保留因"完整故事弧"是硬要求。
- minor edits: 2026 数字加口径(已加);§9 语气(已改)。

### Source/factual review
- reviewer: subagent(独立)
- pass: yes
- blockers: 无
- claims needing refresh/removal: 无必修。METR/时间线数字仅溯及作者一手笔记、非独立复核,但正文已全部归因为"视频所述" → 合格;可选加 METR 一手脚注。
- notes: 逐条对本地产物核实为真——72/72(test-results.json 恰 60+12 全 true)、~2h/3 轮(timeline.tsv iter3→5 ≈1h59m)、34min builder turn(dur_s=2051,func PASS criteria_false=12)、假收敛(iter-5-design.txt 首行 preamble、第3行 NEEDS_WORK、d12 6/10)、19fps 回归(iter-6-func.txt measuredFps@0=19.0)、BORDERLINE 审计(SETUP_LOG CS-V1/2/3)。判断 vs 事实分离清晰。

### Adversarial review
- reviewer: subagent(独立)
- pass: yes(无硬 blocker)
- blockers: 无。泄漏 grep 干净(仅命中"机读 token"技术词);无绝对路径/密钥;VOYAGER 一贯定位为个人复现、无夸大;引用短且署名;故事弧完整无跳段。
- non-blocking risks: ①Opus 3.7 命名(已修);②source 标注 Europe 一致性(已统一);③verified-vs-untested 未显式标注 → 已补"我没测的"段;④Rakuten 7h 归因视频(保留,已归因)。
- required revisions: #1 #2 已修;#3(untested 声明)已补。

### Eval review (links/images, after build)
- reviewer: subagent(独立,非起草 agent)
- pass: yes
- link results:

| url | status | pass? |
|---|---|---|
| https://www.youtube.com/watch?v=mR-WAvEPRwE(正文脚注) | 200 | yes |
| fonts.googleapis.com css2(字体样式) | 200 | yes |
| kevinwangsheng.github.io/my-blog/og.png | 200 | yes |
| preconnect 裸域名 ×2(googleapis/gstatic) | 404 | n/a(preconnect origin 正常响应) |
| canonical/og:url 指向本文未来公开 URL | 404 | 发布后解(同站 /essays/ 根为 200) |

- image results:

| src | resolved location / status | pass? |
|---|---|---|
| three-failure-modes.svg | site/dist/images/voyager-harness/…(2154B) | yes |
| pge-loop.svg | site/dist/…(3159B) | yes |
| voyager-launch.webp | site/dist/…(64158B) | yes |
| voyager-explore-annotated.webp | site/dist/…(122882B) | yes |
| voyager-galaxy.webp | site/dist/…(82250B) | yes |

- rendered check run: yes(headless 载入 out/ui-serve,5 张 naturalWidth 均 >0:SVG 300、webp 1200;零 404)
- broken items and fixes: 无。3 个 404 为 preconnect origin + 未发布 canonical,非破损链接/图片。

## Blocker resolution log

| blocker | action taken | resolved? |
|---|---|---|
| §2 "Opus 3.7"(不存在)与 "Sonnet 3.7" 矛盾 | 统一改为 Sonnet 3.7 | yes |
| source 标注 Europe 一致性(frontmatter vs 正文) | frontmatter 改为 "AI Engineer, Europe 2026" | yes |
| 2026 模型/benchmark 数字新鲜度未标注 | §2 加"转述自视频、未独立复核"口径 | yes |
| §9 逐字搬 takeaways + 私记语气 | 重写折进自述,点出真复测的两条 | yes |
| verified-vs-untested 未显式 | §16 末补"我没测的"(软件GL/跨浏览器/>2h/设计对齐) | yes |

## Agent review

```yaml
agent_review:
  status: agent-cleared
  reviewer: agent
  date: 2026-07-02
  notes: 三轮独立 subagent 评审(editor/factual/adversarial)完成;factual+adversarial PASS,editor 唯一 blocker(模型名矛盾)已修;editorial 18/18;所有 blocker 有解决记录;无泄漏/捏造。可进 content:sync + eval 子 agent + 本地预览。
```

## Final human blog review

```yaml
human_blog_review:
  status: pending-final-review
  reviewer: human
  date:
  notes:
```

## Mechanical verification notes

- content:check: ok=true(0 error;仅"目标已存在"因二次 sync,--overwrite 处理)
- content:sync: ok=true → site/src/content/essays/harness-that-runs-for-hours.md(由评审过的 manifest 生成)
- build: 26 页通过(移除 frontmatter source 字段以绕开 toFrontmatter 嵌套对象 bug;出处改为正文脚注链接)
- preview URL: http://127.0.0.1:4327/my-blog/essays/harness-that-runs-for-hours/(本地静态预览)
- ui-verify: OK=true — Lighthouse 性能 95 / a11y 100 / best-practices 100 / SEO 100;axe crit 0 serious 0;console 0;overflow 无(3 断点 375/768/1440)。图片转 WebP 后性能 71→95。
- leak check: 干净(staged md + synced source + 生成 HTML 均无 /Users/、kb-vault、私有/禁止发布标记)
- eval subagent(链接/图片): PASS(见 Eval review 表)
- 已知管线 bug(非本文内容问题):content-shared.mjs:83 toFrontmatter 不序列化嵌套对象(source:{label,url}→[]);本文以去除 source 字段规避,建议后续修脚本以支持带 url 的 source。
- rejection cleanup if needed: 若人审否决 → 置 needs-rework 并移除 site/src/content/essays/harness-that-runs-for-hours.md。
