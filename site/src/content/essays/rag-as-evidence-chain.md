---
title: "RAG 不是向量库，而是证据链工程"
description: "把 RAG 从 embedding + top-k 的旧印象中拿出来,重新理解为外部证据进入模型上下文的选择、装配、引用和评估链条。"
date: "2026-06-15"
tags: ["rag", "context-engineering", "retrieval", "ai-systems"]
visibility: "draft"
series: "Knowledge systems"
---
很多人第一次理解 RAG,都会从一个很直接的流程开始:把文档切成 chunk,做 embedding,放进向量数据库;用户提问时再把问题 embedding,取最相似的 top-k chunk,塞进 prompt,让模型回答。

这个理解不是错的。它只是太早停下来了。

截至 2026-06-15,我更愿意把 RAG 理解成一条证据链:外部知识如何被选择、过滤、排序、压缩、引用,然后以合适的形状进入模型当前上下文。向量库只是这条链里的一个可能组件;真正的系统问题不是“有没有检索”,而是“这次回答到底需要什么证据,这些证据够不够,新不新,能不能引用,有没有权限,有没有冲突”。

## 死掉的是 lazy vector-RAG

早期 naive RAG 的价值很真实。它让模型可以回答私有文档、最新资料、内部知识库和需要引用的问题,也比微调更轻、更容易更新。作为 baseline,它仍然有用。

但 lazy vector-RAG 的隐含假设太脆弱:语义最相似的 chunk,就是回答所需的正确上下文。

问题在这里开始出现。一个 chunk 可能和问题很像,但缺少时间条件;一个 embedding 可能压掉否定、数字、版本、权限和表格结构;top-k 可能拿到很多相似片段,却没有覆盖真正需要的例外和边界。最后,模型看到“看起来相关”的材料,很容易生成一段流畅但证据不足的答案。

所以,如果有人说 RAG dead,我会先问:你说的是哪一层?如果他说的是固定 chunk、单向量、cosine top-k、prompt stuffing、没有 trace、没有 eval,那我同意。死掉的是这种懒惰形态,不是 retrieval-augmented generation 这个问题本身。

## 现代 RAG 更像上下文装配

更稳的 RAG 系统通常会把链条拆开看。

第一层是 ingestion 和 indexing。PDF、网页、Markdown、代码、表格都不应该被粗暴压成一坨纯文本。结构一旦在解析阶段丢掉,后面的 rerank、judge 和引用系统只能在坏证据上工作。好的索引会保留标题路径、章节层级、时间、权限、文档类型、实体、版本和来源。

第二层是 query processing。用户原话往往不是资料库里的表达方式。“这个能自动跑吗?”可能要被改写成“该工作流是否允许在没有 human approval 的情况下自动执行”。复杂问题可能需要拆成多个子问题;实时问题可能不该查静态知识库,而应该调用 web、API 或数据库。

第三层是 retrieval 和 ranking。Dense vector 擅长语义相似,但 API 名、错误码、版本号、人名和精确术语经常更适合 lexical search。现代系统常见的方向是 hybrid retrieval、metadata filter、宽召回、fusion、rerank,而不是只相信一个相似度分数。

第四层是 context assembly。检索结果不能原样塞进 prompt。它需要去重、排序、分组、压缩、保留引用、标出冲突和限制条件。长上下文不是保险箱;上下文越长,噪声和干扰也越可能进入模型工作区。这里的目标不是“塞更多”,而是让模型看到低噪声、可引用、覆盖完整的证据集合。

第五层是 grounded answering 和 trace/eval。最终答案里的关键 claim 应该能追到证据;证据不足时应该说不足;证据冲突时应该呈现冲突,而不是揉成一个不存在的折中结论。一次 RAG 调用如果不能回放原问题、query rewrite、filters、候选、rerank、最终 context、引用、模型版本和 index 版本,错误就很难归因。

> RAG 的本体不是“存知识”,而是让证据以正确形状进入当前推理现场。

## 为什么 long context 没有替代 RAG

长上下文是一种容量能力,不是选择能力。

如果资料很少、权限简单、噪声低,把材料直接放进上下文当然可能更省事。但真实知识系统常常不是这样:资料会更新,来源有权限,内容有冲突,问题只需要其中一小部分,而且答案最好能引用。把所有东西塞进去,并不会自动产生正确证据链。

这也是 context engineering 的关键:系统要决定写入什么、保留什么、压缩什么、隔离什么、恢复什么。RAG 是其中负责外部证据供应的一段。Memory 负责跨会话长期状态;tools/API 负责读取或改变外部系统;long context 只是提供更大的工作区。它们不是互相取代的关系,而是边界不同。

一个 agent 回答错了,需要先归因。当前资料没查到,偏 RAG;历史决策没记住,偏 memory;资料在上下文里但模型没用好,偏 context assembly;外部系统调用失败,偏 tool/API。只有拆清楚错误层级,系统才有修复路径。

## 新名词其实是链条里的不同补强

GraphRAG、Agentic RAG、Multimodal RAG 这些词容易让人误以为每个方向都是新范式。更简单的理解是:它们在证据链的不同位置补强。

GraphRAG 适合答案依赖实体关系、跨文档结构、全局主题或多跳关系的场景。Microsoft 的 GraphRAG 项目把文本抽取、网络分析、LLM summarization 等步骤组合起来,用图和 community summaries 增强查询时的上下文。但这不意味着所有问题都需要图。简单事实问答、单文档 QA、低延迟客服,硬上 GraphRAG 往往只是更贵、更慢、更难 debug。

Agentic RAG 是把 retrieval 变成受约束的动态控制流。简单问题走 simple RAG;多源、多跳、需要补查、验证和工具调用的问题,才进入 agentic loop。这里的关键是 routing,不是让所有问题都默认交给 agent 自由探索。

Multimodal RAG 则提醒我们:证据不总是文本。表格、图表、页面版式、截图、视频时间戳、PDF 结构都可能是答案的一部分。如果答案依赖行列关系、图中趋势或视觉位置,纯 OCR 文本只是弱 baseline。

这些延伸方向都在回答同一个问题:证据以什么形态存在,应该怎么被检索、组织、压缩和验证。

## 官方工具也在暗示同一个方向

从公开文档看,主流工具也不再把 RAG 描述成单一向量检索。Anthropic 的 Contextual Retrieval 强调给 chunk 补充文档级语境,再结合 contextual embeddings、BM25 和 reranking。OpenAI 的 File Search 文档把外部文档知识接入 assistant,并说明系统会解析、切分、embedding,同时结合 vector 和 keyword search。Google 的 RAG Engine 和 Microsoft GraphRAG 也都在不同层面把 RAG 往托管索引、检索增强、图结构和私有数据理解推进。

这些不是要证明某个厂商方案最好,而是说明一个趋势:生产 RAG 的竞争点已经从“我有一个 vector DB”移动到“我能否稳定构造可审计的证据上下文”。

## 安全也在证据链里

RAG 安全不能靠模型自律。

权限最好在 indexing/storage 阶段就进入 metadata,在 retrieval 阶段强制 pre-filter。无权文档不应该进入候选池,更不应该进入 rerank、summary、cache、log 或 citation。否则,哪怕最终答案没有直接泄露,中间路径也可能形成旁路。

检索内容也要被视为 untrusted data。文档里可能包含间接 prompt injection,诱导模型忽略规则或调用危险工具。如果 agent 还能执行 API,风险就不只是错误回答,而可能是越权动作。安全的方向不是让模型“更听话”,而是最小权限、schema 限制、sandbox、审计日志和必要的人类审批。

## 我现在的判断

RAG 没死。死掉的是把 RAG 当作“向量数据库应用”的偷懒想象。

真正长期存在的问题是:外部证据如何进入当前上下文。模型上下文变大、工具调用增强、多模态模型出现,都没有消灭这个问题,只是让它更像一条完整的 context engineering 链条。

下一次设计 RAG 系统时,我会先问这些问题:

- 这个任务需要哪些外部证据,证据在哪些形态里?
- 语义相似是否足够,还是需要 lexical、metadata、graph、symbol 或 multimodal retrieval?
- 证据是否需要权限过滤、版本过滤、时间过滤?
- 答案需要 coverage、diversity、引用和冲突呈现吗?
- 错误发生后,我们能否回放 retrieval、rerank、assembly 和 generation?
- simple RAG 够不够,什么时候才值得进入 GraphRAG 或 agentic loop?

如果这些问题都没有答案,那系统可能只是一个 demo。真正的 RAG 是证据链工程:让模型在该知道的时候知道该知道的东西,并且让人能追溯它为什么这样回答。
