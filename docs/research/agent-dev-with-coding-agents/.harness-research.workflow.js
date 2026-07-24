export const meta = {
  name: 'agent-dev-harness-research',
  description: '四簇研究 coding-agent 开发期 harness:实践案例/快变保鲜/数值证据/反例;每簇独立对抗eval(局部目标)+整体FinalEval(防跑偏),evaluator与gatherer隔离',
  phases: [
    { title: 'Gather', detail: '四簇并行抓取:A实录 B保鲜 C数值证据 D反例(只用一手/权威源)' },
    { title: 'LocalVerify', detail: '每簇独立对抗eval:时效/正确/跨厂商/实践边界/局部目标贴合' },
    { title: 'Synthesize', detail: '合成两份新档(CASES/FRESHNESS)+簇C回填草稿' },
    { title: 'FinalEval', detail: '对开发期harness总目标查跑偏/重复已有框架/打回说法' },
  ],
}

const BASE = '/Users/shenghuikevin/dev/AI/my-blog/docs/research/agent-dev-with-coding-agents'
const FLOW = `${BASE}/flow.md`
const HARNESS = `${BASE}/details/HARNESS-construction-for-agent-dev.md`
const README = `${BASE}/README.md`
const SOURCES = `${BASE}/sources.md`

const GOAL = '开发期 harness:个人开发者(solo)用 coding agent(Claude Code/Codex/Cursor)开发一个 AI agent 应用时,围绕 coding agent 搭的那套脚手架,让它把「被造 agent」写得有质量。范围只在开发回路,不是被造 agent 上线后的运行期护栏。'

const METHOD = '证据实时优先(2026);每条标 独立第三方 vs 厂商自报 vs 论文;拿不准标 unverified。只用一手/权威源。实践案例必须具名 + 能看到真实脚手架(目录/配置/eval)或具体踩坑,不收泛泛 best-practices 清单。绝不重做已有 7 类框架,只补缺口/补证据。'

const ANCHOR = `你在为一项已有研究补缺口,不是从零开题。先用 Read 读这三份文件锚定目标与已覆盖范围,再开查:
- ${FLOW}(流程正本;特别读末尾「别再引入的说法」)
- ${HARNESS}(已有 7 类 harness 框架——你的产出绝不能重复它已写的,只补它没有的)
- ${README}(研究方法纪律)

总目标:${GOAL}
方法纪律:${METHOD}
用 WebSearch / WebFetch 抓一手源;每条 finding 必带来源名/类型/url/日期/与本簇目标的相关性说明。`

const CLUSTERS = [
  {
    key: 'A',
    name: '工程实录(最高优先)',
    goal: '真实团队/个人用 coding agent 造 agent 应用的端到端实录:脚手架长啥样、怎么搭 eval、踩了哪些坑。',
    spec: `搜索方向:"how we built our agent with Claude Code / Codex"、"AGENTS.md in production"、"eval harness for LLM agents we built"、"coding agent workflow postmortem"、"用 Claude Code 开发 agent 实践"。
源靶子:Anthropic/OpenAI applied 工程博客、Cognition(Devin)、Factory、incident.io、Sourcegraph、个人深度博客、会议 talk。
收录标准:具名来源 + 能看到真实 repo 结构/配置文件 或 具体踩坑复盘;repo_examples 字段优先填能看到目录/配置的。`,
  },
  {
    key: 'B',
    name: '快变之下 harness 怎么保持有效',
    goal: 'harness 哪些是稳定骨架、哪些每隔几月要换;模型/MCP 协议/框架 churn 怎么扛;version pinning + 保鲜回路实践。',
    spec: `搜索方向:"agent framework deprecation 2026"、"MCP version migration / spec changes"、"pinning model versions in agents"、"keeping CLAUDE.md / evals current"、"agent framework churn"。
重点产出:一个「稳定层 vs 易变层」的划分 + 每个易变点的应对实践(谁稳定、谁要 pin、谁要定期重核)。`,
  },
  {
    key: 'C',
    name: '质量证据强度(给现有数字补硬证据)',
    goal: '现有 HARNESS doc 里标【示例·非规定】的数值(eval 阈值、pass^k、多agent~15× token、capability~92%/regression~98% 等)到底有没有已发表真实基准支撑。',
    spec: `先读 ${HARNESS} 找出所有带数字/阈值的断言,逐一去找:具名 benchmark / 论文 / 厂商 report 里的真实数值。
每条结论二选一:① 找到硬证据(给来源+数值,可去掉【示例·非规定】标)② 仍无硬证据(显式注明 unverified,保留标注)。不要编数。`,
  },
  {
    key: 'D',
    name: '反例(补强失败模式)',
    goal: '真实项目里省掉某块 harness 导致翻车的案例,接现有 7 类每类的「失败模式」。',
    spec: `搜索方向:"agent deleted production database"、"LLM agent cost blowup postmortem"、"no eval shipped broken agent"、"prompt injection agent incident 2026"。
每个反例标:缺了哪一类 harness(对应现有 7 类编号)→ 后果 → 本可由哪个机制挡住。`,
  },
]

const GATHER_SCHEMA = {
  type: 'object',
  properties: {
    cluster: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          claim: { type: 'string' },
          source_name: { type: 'string' },
          source_type: { type: 'string', enum: ['独立第三方', '厂商自报', '论文', '标准/规范', '个人博客', 'unverified'] },
          url: { type: 'string' },
          date: { type: 'string' },
          relevance_note: { type: 'string' },
        },
        required: ['claim', 'source_name', 'source_type', 'relevance_note'],
      },
    },
    repo_examples: {
      type: 'array',
      items: {
        type: 'object',
        properties: { what: { type: 'string' }, url: { type: 'string' }, structure_seen: { type: 'string' } },
        required: ['what'],
      },
    },
    coverage_gaps: { type: 'array', items: { type: 'string' } },
    self_check_local_goal: { type: 'string' },
  },
  required: ['cluster', 'findings'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['pass', 'revise', 'fail'] },
    freshness_ok: { type: 'boolean' },
    correctness_ok: { type: 'boolean' },
    cross_vendor_ok: { type: 'boolean' },
    practice_boundary_ok: { type: 'boolean' },
    local_goal_aligned: { type: 'boolean' },
    problems: { type: 'array', items: { type: 'string' } },
    required_fixes: { type: 'array', items: { type: 'string' } },
    kept_findings: { type: 'array', items: { type: 'string' } },
    dropped_findings: { type: 'array', items: { type: 'string' } },
  },
  required: ['verdict', 'local_goal_aligned', 'problems'],
}

const FINAL_SCHEMA = {
  type: 'object',
  properties: {
    overall_verdict: { type: 'string', enum: ['pass', 'revise', 'fail'] },
    drift_detected: { type: 'boolean' },
    drift_details: { type: 'array', items: { type: 'string' } },
    duplicates_existing_framework: { type: 'boolean' },
    reintroduces_banned_claims: { type: 'boolean' },
    banned_hits: { type: 'array', items: { type: 'string' } },
    per_cluster_goal_met: {
      type: 'object',
      properties: { A: { type: 'boolean' }, B: { type: 'boolean' }, C: { type: 'boolean' }, D: { type: 'boolean' } },
    },
    recommended_fixes: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['overall_verdict', 'drift_detected', 'per_cluster_goal_met', 'summary'],
}

function gatherPrompt(c) {
  return `${ANCHOR}

== 本簇:${c.key} — ${c.name} ==
局部目标:${c.goal}
${c.spec}

产出:按 schema 返回。findings 每条带来源类型/url/日期/相关性;能看到真实脚手架的填 repo_examples;self_check_local_goal 一句话自评是否真的命中本簇局部目标(还是跑成了泛泛清单)。`
}

function verifyPrompt(c, gathered) {
  return `你是独立对抗评审,与抓取者不是同一人(evaluator 隔离)。先 Read ${FLOW} 末尾「别再引入的说法」,再审下面这簇的抓取结果。

总目标:${GOAL}
本簇局部目标:${c.goal}

抓取结果(JSON):
${JSON.stringify(gathered, null, 2)}

逐条对抗审:
1. 时效 freshness_ok:是否 2026 现状,有没有把过期说法当现状。
2. 正确性 correctness_ok:claim 与所引来源是否真的对得上,有没有过度解读。
3. 跨厂商 cross_vendor_ok:是否只押一家、缺跨厂商佐证。
4. 实践边界 practice_boundary_ok:是否分清 solo vs 生产规模、把厂商自报当独立事实。
5. 局部目标贴合 local_goal_aligned:是否真命中本簇局部目标,还是跑偏成泛泛内容/重复了已有 7 类框架。
对每条不达标的 finding 给 required_fixes,并在 dropped_findings 列出该删的。verdict=pass/revise/fail。`
}

function synthCasesPrompt(a, d) {
  return `把下面两簇已通过对抗 eval 的素材合成为一份归档文档草稿(markdown)。

总目标:${GOAL}
文档定位:接现有研究目录,文件名 details/CASES-agent-dev-fieldnotes.md,主题=「用 coding agent 开发 agent 的真实工程实录 + 反例」。绝不重复 ${HARNESS} 已写的 7 类框架内容;这里只放真实案例/踩坑/反例,并标出每个案例印证或补充了哪一类 harness。

簇A(工程实录)已验证素材:
${JSON.stringify(a, null, 2)}

簇D(反例)已验证素材:
${JSON.stringify(d, null, 2)}

要求:开头一段定位+来源纪律说明;正文按案例组织,每个案例=出处(具名+url)/做了什么/可复用的脚手架细节或踩坑/对应 harness 类号/独立vs厂商标注;反例单列一节(缺哪类→后果→本可由哪个机制挡)。保留 unverified 标注。直接返回 markdown 全文。`
}

function synthFreshPrompt(b) {
  return `把下面这簇已通过对抗 eval 的素材合成为一份归档文档草稿(markdown)。

总目标:${GOAL}
文档定位:文件名 details/HARNESS-freshness-fast-moving.md,主题=「快变领域下 harness 怎么保持有效」。补 ${HARNESS} 没单列的角度,不重复其已有内容。

簇B 已验证素材:
${JSON.stringify(b, null, 2)}

要求:核心给一张「稳定层 vs 易变层」划分表(谁稳定/谁要 pin/谁定期重核),每个易变点配应对实践+来源;最后一段给 solo 最小保鲜回路。标独立vs厂商,保留 unverified。直接返回 markdown 全文。`
}

function synthCPrompt(c) {
  return `把下面这簇(数值证据核查)已通过对抗 eval 的素材,整理成一份「回填清单」草稿(markdown),供人工回填到 ${HARNESS}。

簇C 已验证素材:
${JSON.stringify(c, null, 2)}

要求:做成一张表,每行=现有 doc 里的某个带数字断言 / 找到的硬证据(来源+数值)或「仍无硬证据」/ 建议动作(去掉【示例·非规定】标 还是 保留并注明 unverified)。不要编数。直接返回 markdown 全文。`
}

function finalPrompt(cases, fresh, cback) {
  return `你是整体 FinalEval,独立于前面所有人。任务:对开发期 harness 总目标查这次研究有没有跑偏。先 Read 这两份:
- ${FLOW}(末尾「别再引入的说法」)
- ${HARNESS}(已有 7 类框架,查是否被重复)
也可 Read ${SOURCES} 末段「已被打回」清单。

总目标:${GOAL}
方法纪律:${METHOD}

待评三份草稿:
=== CASES 草稿 ===
${cases}

=== FRESHNESS 草稿 ===
${fresh}

=== 簇C 回填清单草稿 ===
${cback}

逐项判:
- drift_detected:整体是否偏离「开发期 harness」总目标(例如滑向被造 agent 运行期护栏、滑向通用 LLM 应用、滑向工具功能清单)。
- duplicates_existing_framework:是否重复了 ${HARNESS} 已写的 7 类内容而非补缺。
- reintroduces_banned_claims:是否引入了 flow.md/sources.md 已打回的说法(命中填 banned_hits)。
- per_cluster_goal_met:A/B/C/D 四簇各自局部目标是否达成。
给 recommended_fixes 和一句 summary。overall_verdict=pass/revise/fail。`
}

phase('Gather')
log('四簇并行抓取 + 每簇独立对抗 eval(pipeline,gather→verify 不设栅栏)')

const verified = await pipeline(
  CLUSTERS,
  (c) => agent(gatherPrompt(c), { label: `gather:${c.key}`, phase: 'Gather', schema: GATHER_SCHEMA }),
  (gathered, c) => {
    if (!gathered) return null
    return agent(verifyPrompt(c, gathered), { label: `verify:${c.key}`, phase: 'LocalVerify', schema: VERIFY_SCHEMA, effort: 'high' })
      .then((v) => ({ cluster: c.key, gathered, verdict: v }))
  }
)

const ok = verified.filter(Boolean)
const byKey = {}
ok.forEach((r) => { byKey[r.cluster] = r })
log(`局部验证完成:${ok.map((r) => `${r.cluster}=${r.verdict?.verdict}/局部贴合=${r.verdict?.local_goal_aligned}`).join('  ')}`)

phase('Synthesize')
const [casesDraft, freshDraft, cDraft] = await parallel([
  () => agent(synthCasesPrompt(byKey.A || null, byKey.D || null), { label: 'synth:cases', phase: 'Synthesize' }),
  () => agent(synthFreshPrompt(byKey.B || null), { label: 'synth:freshness', phase: 'Synthesize' }),
  () => agent(synthCPrompt(byKey.C || null), { label: 'synth:c-backfill', phase: 'Synthesize' }),
])

phase('FinalEval')
const finalEval = await agent(finalPrompt(casesDraft || '(缺)', freshDraft || '(缺)', cDraft || '(缺)'), {
  label: 'final-eval', phase: 'FinalEval', schema: FINAL_SCHEMA, effort: 'high',
})

return {
  verified: ok.map((r) => ({ cluster: r.cluster, verdict: r.verdict })),
  drafts: { cases: casesDraft, freshness: freshDraft, cBackfill: cDraft },
  finalEval,
}
