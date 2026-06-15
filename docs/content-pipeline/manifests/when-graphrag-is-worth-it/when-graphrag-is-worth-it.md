---
title: "什么时候 GraphRAG 值得上"
description: "GraphRAG 的判断标准不是文档多,而是答案是否必须依赖关系结构和跨文档综合。"
date: "2026-06-15"
tags: ["rag", "graphrag", "architecture"]
visibility: "public"
topic: "RAG architecture"
related: ["rag-as-evidence-chain"]
---

GraphRAG 不应该被理解成“RAG 的高级版”,更不应该因为文档多就默认引入。

更准确的判断标准是:答案是否必须依赖**关系结构**。

值得考虑 GraphRAG 的情况通常长这样:

- 问题需要跨多篇文档连接实体、事件、组织、主题或 claim;
- 答案不是找一段原文,而是做全局 sensemaking;
- 用户关心“这一批材料里出现了哪些主题/派系/冲突/路径”; 
- 普通 vector top-k 总是召回局部相似片段,但无法把关系串起来。

如果只是单文档 QA、低延迟客服、FAQ、简单事实查找,GraphRAG 可能只是增加 indexing 成本、调试难度和延迟。

Microsoft GraphRAG 文档把它描述为一种 structured, hierarchical 的 RAG 方法:从文本中抽取 knowledge graph,构建 community hierarchy,生成 community summaries,再在查询时使用这些结构。这个描述很关键:它的价值来自结构,不是来自“用了图数据库”这个标签。

> 文档多不是上 GraphRAG 的理由;答案必须穿过关系网络,才是理由。
