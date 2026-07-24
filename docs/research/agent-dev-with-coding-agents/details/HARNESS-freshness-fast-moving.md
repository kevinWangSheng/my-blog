# 快变领域下,开发期 harness 怎么保持有效(稳定层 vs 易变层 + 各易变点保鲜)

> 状态:**纠正版草稿**(2026-06-20)。本文是 `HARNESS-construction-for-agent-dev.md`(静态 7 类构建)的**时间维补篇**——专讲 harness 各部件**随时间老化与保鲜**:谁稳定、谁要 pin、谁要定期重核。
> 范围:**开发回路内**的 harness(个人 solo 开发者用 coding agent 造一个 AI agent 应用时围绕 coding agent 搭的脚手架),不是被造 agent 上线后的运行期护栏。
> 与已有文件的边界:静态分层 / 7 类失败模式见 `HARNESS-construction-for-agent-dev.md`;被造 agent 的**知识检索保鲜**(Context7 / web_search / vendored docs)见 `d1-knowledge-freshness.md`。本文不重复这两者,只补**「harness 自身随时间失效」**这个角度。
> 标注:**〔独立〕**=中立第三方/标准;**〔厂商〕**=厂商自报(官方文档/政策/工程文);**【推断】**=源只给上层事实、结论是据其推的;**【unverified】**=证据偏弱或仅单源,待交叉核。

---

## 0. 非专家 30 秒导航

**核心问题**:harness 不是一次搭好就一直有效。它依赖的东西——模型 id、agent 框架、MCP 协议、指令文件内容、eval 测例——**都在快变**。模型生命周期已压到 ~1 年量级(部分厂商更短),框架破坏性版本几月一次,MCP 协议官方政策给的是「约一年重核一次」的节奏。如果 harness 把这些易变层当常量写死,它会在你没注意时静默失效(代码还能跑,但跑的是错的东西)。

**对策的形状**:把 harness **显式分两层**——
- **稳定层**:很少变、值得当骨架固定下来(指令骨架结构、provider 抽象/适配器核心、固定 golden/regression eval 集)。
- **易变层**:会 churn、必须 ① 显式 **pin** 到带版本/日期的标识,② 排进**定期重核**节奏,③ 换代时用稳定层(regression eval)兜回退。

**solo 最小保鲜回路**(详见末段):每次构建 pin 全套版本进一个 manifest → 每季度重核一遍易变层 → 每次换模型/框架/协议都先跑 regression eval。

---

## 1. 稳定层 vs 易变层划分表

> 这张表把 harness 的各部件按「变化速度」分轨。**稳定层**=骨架,固定下来当不变量;**易变层**=必须 pin + 定期重核。每行给:典型变化节奏、应对实践、来源类型。
> ⚠️ 「重核周期」一列是从各层各自的弃用政策/生命周期**分别**推出的综合数字,**没有单一权威源给出统一周期表**——属【推断】,按你项目实际节奏调。

| 部件 | 层 | 典型变化节奏 | 应对实践 | 来源 |
|---|---|---|---|---|
| **指令文件结构**(分层/单一事实源/import 桥接的**架构**) | 稳定 | 很少变 | 当骨架固定;结构本身不随 stack 变 | 〔独立〕Hermes 三档分轨 |
| **provider 抽象 / transport adapter 核心** | 稳定 | 很少变 | 把 provider 怪癖隔离在适配器层,稳定 prompt 核心独立于 provider | 〔独立〕Hermes |
| **固定 golden / regression eval 集** | 稳定 | 刻意不变 | 作为「不动的尺子」;变了就无法区分模型行为变化 vs 流量变化 | 〔独立〕Confident AI |
| **成本/递归/墙钟硬上限**(见构建篇类 7) | 稳定 | 很少变 | 数值偶调,机制不变 | — |
| **模型 id** | 易变 | ~1 年量级(部分更短) | **pin 带日期 snapshot id**(非浮动别名)+ shadow mode + 用足 60 天通知窗 | 〔厂商〕Anthropic;〔独立〕Presenc |
| **请求参数**(temperature/top_p/top_k 等) | 易变 | 随模型代际 | 监控弃用;Opus 4.7+ 设非默认值直接 400,改纯 prompt 引导 | 〔厂商〕Anthropic |
| **agent 框架版本** | 易变 | 破坏性变更几月一次 | 按**各框架自己的** semver 语义 pin(不能套同一规则) | 〔厂商〕LangChain / OpenAI SDK |
| **MCP 协议版本** | 易变 | 官方政策 ≥12 月弃用窗 | pin `MCP-Protocol-Version` 头;窗口内协同升级;用 12 月重叠当缓冲 | 〔厂商〕MCP 官方 RC |
| **指令文件内容**(规则正文) | 易变 | 随 stack 变就 rot | 单一事实源 + import 桥接;周期 audit staleness/duplication/mirror-drift | 〔独立〕个人博客交叉 |
| **eval 测例** | 易变 | 随生产持续补 | 固定集之外,每次上线回退转一条新测例;周期抽审 trace 找漂移 | 〔独立〕Confident AI |
| **MCP / 框架的具体 API 知识** | 易变 | 快 | (本文不展开)走 `d1-knowledge-freshness.md` 的检索保鲜 | — |

---

## 2. 各易变点的 pin / 保鲜实践

### 2.1 模型 id —— 强易变层,pin snapshot 而非别名

**事实(均经 Anthropic 一手 model-deprecations 页核实)**〔厂商〕:
- 四段生命周期 Active → Legacy → Deprecated → Retired;退役后请求**直接 fail**。
- 公开发布模型退役前**至少 60 天通知**。
- 2026 实际节奏:Sonnet 4 / Opus 4 于 **2026-06-15** 退役;Opus 4.1 于 **2026-08-05** 退役。
- 参数也会 churn:`temperature`/`top_p`/`top_k` 在 **Claude Opus 4.7 及以后**设为非默认值返回 **400**,替代是纯 prompt 引导。

**【推断】**(合理但**所引 Anthropic 官方页全文无此表述**,降级为推断,勿当一手直给):dateless 别名(如 `claude-opus-4-0`)在其底层 snapshot 退役时会一起下线,所以**用别名并不能避免迁移**。这是把别名机制 + 上面的 snapshot 退役事实组合后的推断。

**跨厂商概括**〔独立 · Presenc 聚合,需各厂商一手交叉核〕【unverified 数字】:模型生命周期在 2026 已压缩到约 **6–12 个月**(此前 18–24 月)。⚠️ 此数字与 Anthropic 一手实测有张力——Opus 4(2025-05 发布 → 2026-06-15 退役)实际约 **13 个月**,故「6–12 月」当**第三方估算**看,不作确定数字。同源还称 OpenAI 于 2026-06-11 通知 GPT-5/o3 旧 snapshot 将于 2026-12-11 从 API 移除——**仍需一手交叉核**【unverified】。

**应对实践**:
- **pin 到带日期的 snapshot id**,使上游弃用从「突发故障」变成「有计划的迁移」。
- **deployment manifest 把版本字段绑一起**:agent 版本 + code commit hash + prompt 版本 + model snapshot + tool 版本。〔独立 · Presenc〕
- 退役通知到了就用**满 60 天窗口**做迁移,别拖到 retire 当天。

### 2.2 换模型当作「会引入 silent regression 的事件」

**原则**〔厂商 · Anthropic Engineering〕:新模型会**推理不同、跟指令不同、token 计数不同、拒绝某些输入**,可能导致 prompt 不再触发工具、或输出被截断。所以**换模型不是简单 version bump**,要当成可能引入静默回退的事件处理。

**实践**(稳定层 regression eval 在这里兜底):
- 升级前后跑 **regression eval**,应**近 100% 通过**;掉分=回退信号。
- 用 **shadow mode** 跑候选模型(不对用户出输出),对比 live 输出,捕捉离线 eval 集漏掉的分布漂移。
- 把 regression eval **接进 CI/CD 当 guardrail**。

> 与构建篇类 3 的区别:类 3 讲 eval 体系**怎么搭**;这里专讲**换模型这一易变层换代时,怎么用稳定的 eval 集兜回退**。

### 2.3 eval 套件本身也会 drift —— 区分固定集与保鲜集

**事实**〔独立 · Confident AI;与 Anthropic 的 shadow-mode/regression 立场交叉印证〕:
- **eval drift** = 评测套件不再匹配它本应衡量的真实生产质量。
- 保留一个**稳定的 golden/regression 数据集**(否则流量变化会被误读成模型行为变化)——这是**稳定层**。
- 每条上线后的生产回退都**转成一个新测例**——这是**保鲜层**。
- **周期性抽审生产 trace**,发现当前 metric 没设计去抓的行为漂移。
- 告警用**联合判定**:输入漂移 + 可测的 eval 掉分;无 eval 影响的漂移视为误报。

### 2.4 agent 框架 —— 高 churn,但 pin 策略按各家 semver 定

**关键:不同框架 semver 语义不同,不能套同一规则。**

- **LangChain**〔厂商 · release-policy 逐字核实〕:经历 2023–2025 三年 v0.x 破坏性变更,1.0 于 2025-10 才发布;`AgentExecutor`/`initialize_agent`/`create_react_agent` 全部弃用(改 `create_agent`)。**1.0 起承诺 semver**:破坏性变更(含移除弃用功能)**只在 major**(如 2.0);minor 只加功能不破坏;弃用功能**贯穿整个 1.x** 并给迁移指引。
  → pin 策略:可信任 minor 升级,把破坏性预期锚在 major 边界。
- **OpenAI Agents SDK**〔厂商 · release 页逐字核实〕:仍处 **0.Y.Z** 阶段(前导 0 = 仍在快速演进),破坏性变更发生在 **minor(Y)**、patch(Z)才非破坏。官方明确建议:**「pin 到 0.0.x 版本」** 以避免破坏性变更。
  → pin 策略:对快变框架 pin 到 **patch 级**。

**对照结论**:LangChain 破坏在 **major**,OpenAI 破坏在 **minor**——同样一句「pin 框架」,落到两家是完全不同的版本粒度。**pin 策略必须按各框架自己的发布政策定。**

### 2.5 MCP 协议 —— 易变层,但官方给了 ≥12 月弃用重叠窗

> ⚠️ **时效框定**:截至今天(2026-06-20),MCP 2026-07-28 spec 仍是 **RC(RC lock 2026-05-21)**,final **未发布**。以下是**即将生效的 RC/草案**,不是已落地的现状。

**RC(2026-07-28)拟确立的内容**〔厂商 · MCP 官方 RC 博客,逐条核实〕:
- **首个正式弃用政策**:三段生命周期 Active → Deprecated → Removed,弃用到最早移除之间**至少 12 个月**(引 SEP-2596)。
- 本次是发布以来最大改动:**移除协议层 session 模型**(取消 initialize/initialized 握手);Roots/Sampling/Logging 被弃用(替代:tool 参数 / resource URI、直连 LLM provider API、stderr 或 OTel)。

**迁移的具体改动**〔个人博客 + 官方 RC 交叉,核心政策与一手一致〕:客户端每请求新增必填头 `MCP-Protocol-Version: 2026-07-28`、`Mcp-Method`(须等于 body.method)、`Mcp-Name`(须等于工具名);删除 initialize 请求与 `Mcp-Session-Id` 头;服务端错误码 `-32002` 改为标准 `-32602`。具体 header 示例**当操作示意**看。

**【推断 · 一手 spec 暂无明确背书,原引文已剔除】**:那篇个人博客**未记录任何向后协商策略**,默认在 RC→final 的 **10 周窗口**内协同升级。可直接引用的原文要点只有「10 周窗口是刻意设计的」;「MCP 无内建 fallback 协商」是抓取者据此推断的结论,**缺一手 spec 明确背书**,标【unverified】。

**应对实践**:
- **显式 pin** `MCP-Protocol-Version` 头,不假设自动兼容。
- 把官方 **≥12 个月弃用重叠窗**当缓冲,据此排「约一年重核一次 MCP」的节奏。
- 客户端/服务端在升级窗口内**协同升级**(若「无 fallback 协商」成立则更刚性);solo 在 10 周窗口内具体降风险 playbook **仍 unverified**。

### 2.6 指令文件内容会 rot —— 周期 audit 防漂移

**事实**〔个人博客,已自标;150–200 上限与单一事实源做法与构建篇类 1 一致〕:
- 指令文件(`CLAUDE.md`/`AGENTS.md`)**像任何文档一样会 rot——stack 变了就得更新指令**。
- 双文件并存会 **drift**(一处改了另一处忘改,几周后 pytest/vitest 设定打架)。
- **膨胀会让 LLM 整体忽略指令**:前沿模型可靠跟随约 **150–200 条**,而 Claude Code 系统提示已占约 50 条。

**应对实践**:
- 以 **AGENTS.md 为单一事实源**,CLAUDE.md 用 **@import 桥接**(本仓库正是这么做的)。
- **周期性 audit**:查 staleness / duplication / mirror-drift。

> 与构建篇类 1 的区别:类 1 讲指令的**静态分层结构**;这里补**随时间维护、防 rot**的角度。

---

## 3. 可验证的真实脚手架:稳定/易变显式分轨

**Hermes agent harness**〔独立 · Arize 分析,指向 `github.com/NousResearch/hermes-agent`,约 27k stars〕——一个**可去 repo 核对**的开源 harness,把 system prompt 显式分三档:

- **Stable 档**:身份 `SOUL.md`、已启用工具的指引、skills 索引、环境/平台提示。
- **Context 档**:从 cwd 读 `AGENTS.md`/`CLAUDE.md`/`.cursorrules`,**载入前做 prompt-injection 扫描**。
- **Volatile 档**:memory 快照、用户画像、外部 memory provider、带 model/provider 元数据的时间戳行(**逐 turn 变**)。

**provider churn 被隔离在 transport adapter 层**:同一 runtime 驱动 chat-completions / Anthropic Messages / Codex Responses / Bedrock,工具调用格式与 provider 怪癖由适配器**归一化**,使稳定 prompt 核心**独立于 provider 变化**。

> 这是「稳定层 vs 易变层分轨」+「模型 provider 易变层隔离」的可验证落地。⚠️ 具体目录/文件名未在二手分析中逐一列出,**需到 repo 核对**。

---

## 4. solo 最小保鲜回路

> ⚠️ 未找到 solo 个人开发者把「稳定骨架 / 季度重核 / 每次 pin」写成清单的**一手案例**;下面是从 Hermes 三档 + 各厂商弃用政策 + eval drift **综合推断**的 solo 版,**非单一权威源直接给出**。version pinning 的真实 solo 脚手架文件证据也偏弱(有官方政策 pin-to-0.0.x / pin snapshot id,但未抓到一个具名 solo repo 的 lockfile/manifest 把 model id + framework + MCP server 版本一起 pin 的可看实例)【unverified】。

**① 固定下来(稳定骨架,搭一次)**
- 指令骨架结构(单一事实源 + import 桥接)。
- provider 抽象 / adapter 核心(把 provider churn 关在一层里)。
- 一个固定的 golden/regression eval 集 + 成本/递归硬上限。

**② 每次构建都 pin(写进一个 manifest)**
- model **snapshot id**(带日期,非别名)。
- framework 版本(按各家 semver 粒度:LangChain 锚 major、OpenAI SDK pin 0.0.x)。
- MCP `MCP-Protocol-Version` 头 + MCP server 版本。
- 连同 code commit hash + prompt 版本一起绑。

**③ 每季度重核一遍易变层**(周期属【推断】,按项目调)
- 查各厂商 model-deprecations 页:有没有你 pin 的 snapshot 进了 Deprecated;参数(temperature 等)有没有新限制。
- 查框架 release notes:有没有跨过破坏性边界(LangChain major / OpenAI minor)。
- 查 MCP:RC/final 状态、弃用窗倒计时(用 ≥12 月重叠当缓冲)。
- audit 指令文件:staleness / duplication / mirror-drift。
- 抽审生产 trace:把当前 metric 没抓到的漂移补成新 eval 测例。

**④ 每次换模型/框架/协议都过 regression**
- 换前换后跑固定 regression eval,近 100% 才放行,掉分=回退。
- 高风险换代用 shadow mode 跑候选、对比 live。
- 把每条生产回退转成一条新测例,喂回固定集。

> 一句话:**稳定层当尺子,易变层每次 pin、每季度重核、每次换代用尺子量一遍。**

---

> 标注复核:本文「6–12 月生命周期」「各层重核周期」「MCP 无 fallback 协商」「dateless 别名不防迁移」均已按对抗 eval 结论降级标注(第三方估算 / 推断 / unverified);其余〔厂商〕〔独立〕可溯到对应一手政策页或第三方分析。与 `../flow.md` 冲突以 flow.md 为准;静态 7 类见 `HARNESS-construction-for-agent-dev.md`,被造 agent 知识检索保鲜见 `d1-knowledge-freshness.md`。
