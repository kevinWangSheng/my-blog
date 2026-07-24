<!--
NOTES.md — expense-agent「context 外工作簿」(structured note-taking / agentic memory)
依据:Anthropic effective-context-engineering 文 —— agent "regularly writes notes
persisted to memory outside of the context window",举例即 "maintaining a NOTES.md file"。
作用:对治 context rot —— 把发现的模式 / 关键依赖 / 用过的命令写在这里,需要时再注入,
      而不是塞满主 context。与 claude-progress.txt 分工:
        - claude-progress.txt = 时序状态(做了什么 / 现在什么状态 / 下一步)→ 每 session 覆写。
        - NOTES.md           = 不随时间变的「项目事实地图」(架构 / 依赖 / 速查)→ 增量沉淀。
小节名为【推断/示例·非规定】:官方只点名「a NOTES.md file」,未规定小节;下面是可照抄骨架。
-->

# expense-agent — Working NOTES

## Objectives(为什么造它,一句话锚定,防止越做越偏)
- 输入一张发票/收据(PDF/图片/文本),输出结构化入账建议 JSON:
  `{vendor, date, amount, currency, amount_base, category, confidence, needs_human}`。
- 形态约束:**单 agent + tools**(不上多 agent);Python;调 Claude API(claude-opus-4-8 / claude-sonnet-4-6)。

## Architecture map(主链路 + 固定工具名,改代码前先扫这里)
```
src/agent.py            主循环:gather(OCR) -> 抽字段 -> fx 换算 -> 给入账建议 -> (可选)post
src/tools/ocr_extract.py    ocr_extract(file_path)  -> 调外部 OCR API,返回原始文本(读外部/花钱/无本地副作用)
src/tools/fx_rate.py        fx_rate(currency,date)  -> 外部汇率 API(快变 → 保鲜路径见下)
src/tools/post_ledger_entry.py    post_ledger_entry(entry)-> 写本地 ledger.db(有副作用/危险 → 默认 ask/deny)
evals/                      抽取字段 code-based grader(精确/数值容差)+ category pass^k
ledger.db                  本地 SQLite 入账记录(唯一可写副作用面)
```
- 工具命名是**固定契约**,禁止改名;新增工具沿用 `服务_动作` 命名风格。

## Discovered patterns / gotchas(踩过的坑,沉淀在这避免重犯)
- OCR 输出脏(换行/货币符号粘连);抽 amount 前先归一化千分位/小数点,别直接 regex。
- fx_rate 是**快变数据** → 永远不要相信模型内置的汇率/API 文档,过期即走 web_search 保鲜(见 src/tools/fx_rate.py)。
- post_ledger_entry 是唯一危险写操作 → 约束必须在**权限层**(.claude/settings.json ask/deny),不靠 prompt 提醒。

## Key dependencies & versions(写 SDK 代码前先核实际版本,别信内置旧知识)
- anthropic Python SDK:版本以 `pip show anthropic` 为准(写本文时未 pin,落盘前复核)。
- web_search 工具版本:**当前 `web_search_20260318`**(支持 response_inclusion);
  `web_search_20260209` 起支持 dynamic filtering;`web_search_20250305` 为 basic。← 会变,用前查官方。
- 模型 id:`claude-opus-4-8`(主)/ `claude-sonnet-4-6`(省成本备选)。

## Quick Reference(高频命令,免得每次回忆)
```
跑主链路:      python -m src.agent samples/inv01.pdf
跑全部 eval:    python -m evals.run --suite all
单测:          pytest -q
看 fail 的 transcript: ls evals/runs/<latest>/transcripts/
查 fx 缓存:     sqlite3 .fx_cache.db "select * from fx_cache order by fetched_at desc limit 5"
```

## 不要做(scope 护栏,防止 agent 顺手扩张)
- 不上多 agent / 不加向量库 / 不做通用 KB。
- 不在 prompt 里硬编汇率或「永不写生产库」之类口头约束 —— 用权限/容差/eval 兜实。
