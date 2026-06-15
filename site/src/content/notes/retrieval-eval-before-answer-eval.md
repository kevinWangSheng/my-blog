---
title: "RAG 评估要先拆开 retrieval 和 answer"
description: "最终答案错了,不等于模型或 RAG 整体错了;先看正确证据有没有进入上下文。"
date: "2026-06-15"
tags: ["rag", "evaluation", "context-engineering"]
visibility: "draft"
topic: "RAG evaluation"
related: ["rag-as-evidence-chain"]
---
RAG 系统答错时,最容易犯的错误是直接说“模型不行”或“检索不行”。这两个说法都太粗。

更好的第一刀是把评估拆成两层:

- **Retrieval eval**:回答所需的正确证据有没有被召回、过滤、排序并放进最终上下文?
- **Answer eval**:模型有没有忠实使用这些证据,有没有编造、忽略冲突或越过证据边界?

如果正确证据根本没有进入上下文,那修 prompt 通常只是粉饰。应该回到 parsing、chunking、metadata、query rewrite、hybrid search、rerank 或 source routing。

如果正确证据已经进入上下文,但答案仍然错,问题才更可能在 context assembly、引用策略、answer policy 或模型生成层。

> RAG 的可维护性来自 failure attribution,不是来自最终答案看起来顺眼。

所以一条 RAG trace 至少应该能回放:原问题、改写后的 query、filters、候选证据、rerank 结果、最终 context、答案、引用、模型版本和 index 版本。否则系统错了以后,你只能猜。
