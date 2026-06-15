---
title: "Anthropic Contextual Retrieval"
description: "一个说明现代 RAG 不只靠向量相似度的官方工程来源:给 chunk 补上下文,再结合 BM25 和 reranking。"
date: "2026-06-15"
tags: ["rag", "retrieval", "context-engineering"]
visibility: "public"
url: "https://www.anthropic.com/engineering/contextual-retrieval"
category: "essay"
note: "官方工程文章,适合作为 RAG evidence-chain 的 retrieval/indexing 案例。"
---

这篇适合和《RAG 不是向量库,而是证据链工程》一起读。

它把一个很容易被忽略的问题说清楚:chunk 从原文里切出来以后,会丢失文档级语境。Anthropic 的做法是在 embedding 和 BM25 indexing 前,给每个 chunk 补一段简短的 chunk-specific context,再结合 reranking 过滤候选。

我收藏它不是因为这是唯一正确方案,而是因为它很好地说明了现代 RAG 的方向:检索质量不只来自“更好的向量库”,也来自 parsing、chunk boundary、lexical matching、rerank 和 context assembly 的联动。
