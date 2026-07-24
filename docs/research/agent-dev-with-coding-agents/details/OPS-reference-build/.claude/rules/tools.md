---
paths:
  - "src/tools/**/*.py"
---

# 工具层规则(src/tools/**)

仅当 Claude 在动 `src/tools/` 下的文件时才加载这份规则,不污染日常上下文。

## 固定工具契约

三个工具名锁死,**禁止改名 / 禁止新增同义工具**:
- `ocr_extract(file_path)` —— 读外部 OCR,花钱,无本地副作用。失败要返回 `is_error` 的 tool_result,不要静默吞掉。
- `fx_rate(currency, date)` —— 读外部汇率,**快变数据**。
- `post_ledger_entry(entry)` —— 写 `ledger.db`,**危险副作用**。

新增工具或改签名:先写 ADR,再改 `input_schema`。`input_schema` 的 description 要写**何时调用**,不只写做什么(opus 系模型对工具的触发依赖描述里的触发条件)。

## 知识保鲜(fx_rate)

- `fx_rate` 的返回是会过期的事实,**不得**写进 prompt 常量 / 长期缓存当真值。每次入账按 `entry.date` 现取。
- 若做缓存,必须带 TTL 且记录取数时间;`amount_base` 永远基于「当次取到的汇率 + 单据日期」,不要复用上次结果。
- 解析外部 API 返回用 `json.loads()`,不要裸字符串匹配。

## 危险工具(post_ledger_entry)默认不放行

- 这是不可逆写库。代码层面默认走 `DRY_RUN`/演练;真实写入只在确认后。
- **真正的阻断不在这份 .md(指引≠强制)**,在 `.claude/settings.json` + PreToolUse hook 链:`.claude/hooks/pre_tool_use_guard.sh`(第一道,matcher=Edit|Write|MultiEdit|NotebookEdit|Bash)与 `.claude/hooks/guard_ledger.py`(第二道,matcher=Bash,命中 ledger.db / post_ledger 写操作时 `sys.exit(2)` 阻断)。改这条前读 `docs/adr/ADR-0002`。
- 注意拦截边界:settings.json 的 Bash 规则与 guard hook 只覆盖「Claude Code 开发期跑 shell 碰 ledger.db」。`src/agent.py` 运行时经 SDK 调 `post_ledger_entry`,Bash hook 拦不到,运行时人审要在 agent 代码里自建。
- 工具内部要做输入校验:`amount` 是 Decimal、`currency` 合法、`needs_human=true` 时拒绝直接入账。
