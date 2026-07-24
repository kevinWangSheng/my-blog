# _STATUS — OPS-reference-build (v2) 出处 / 裁决 / 实测(权威)

> 这一目录把 7 类 harness 策略钻到**操作层**:围绕中性 toy 参考 agent `expense-agent`(单据/发票抽取 + 入账建议),给出 7 类各自的**真实可落地 harness 文件**(完整内容 + 验证命令 + 杀的失败模式)。导览见 `README.md`,策略层原稿见 `../HARNESS-construction-for-agent-dev.md`。

## v2 是什么、为什么重做

v1 有一个被用户抓出的方向偏差:**把"工具设计"做成了"工具业务实现"**——产出了 `ocr_extract.py` 里真实 httpx 调用、`context_config.py` 业务运行时、`test_fx_rate.py` 业务断言。这些是"实现这个 agent",不是"用 coding agent 开发 agent 的 harness"。

v2 用**强监督 + 弱执行 + 对的尺子**重做,把这条边界焊死:
- **强监督盯弱执行**:`opus·high` 当方向定锚 + 逐节点守门,`sonnet` 当执行;偏了带纠正回炉(≤2 轮)。
- **执行前**:强模型先产 7 张「操作层边界卡」(每类该产什么 harness 构件、哪些业务实现只能占位),喂给弱执行 agent。
- **执行后**:守门 rubric 新增 `business_impl_leak` / `is_harness_not_business`,泄漏业务实现即打回。
- 这套监督模式可复用于后续同类研究。

## 核心边界:harness ≠ 被造 agent 业务实现

- **harness(产全、可跑)**:配置/约束/门 + 通用护栏机制。即 `.claude/*`、`.codex/config.toml`、`evals/grader.py`+`check_isolation.py`、工具 `schemas.py`(inputSchema 定义)、`guards.py`/`otel.py`/`prompt_wrap.py`(成本上限/埋点/注入防护,day-0 铁律要求写代码)、pre-commit/release-please/CI。
- **被造 agent 业务实现(一律占位)**:工具 handler 内部怎么调 API、运行时业务逻辑、业务测试。本目录里 `src/tools/ocr_extract.py`·`fx_rate.py`·`post_ledger_entry.py`、`src/agent.py`、`src/context_config.py`、`tests/test_*.py` 全是**接口契约占位**(签名 + docstring「此处接入你的业务,harness 不规定」+ `NotImplementedError`/`pytest.skip`)。

## FinalEval 裁决(对研究总目标:solo 用 coding agent 给一个 agent 搭出「照着能做」的 harness)

| 维度 | 结果 |
|---|---|
| coverage_ok(7 类见操作底) | ✅ |
| day0_present(成本递归硬上限·evaluator 隔离·约束在权限沙箱层) | ✅ |
| no_bloat_ok | ✅ |
| harness_not_business_ok(没滑成实现 agent,业务已占位) | ✅ |
| consistency_ok(跨类自洽) | ✅ |
| goal_drift | ✅ false |
| **整体 passed** | ✅ **True** |

守门 7 类全过(`leak=False` 全部,rounds 1–3)。这是 v1 没达到的(v1 卡在 consistency + 未守 harness/业务边界)。

## 我落盘后做的修复 + 实测(亲自跑的)

1. **路径规整**:v2 部分文件带 `expense-agent/` 嵌套前缀,统一去前缀拍平到目录根。
2. **reconcile prose-clobber 修复**:reconcile 对它**编辑**(非新建)的 5 个文件,`corrected_content` 错填成"改动描述"而非完整文件内容。我照搬覆盖坏了 `settings.json`/`AGENTS.md`/`tools.md`/`NOTES.md`/`claude-progress.txt` → 已全部从执行节点原文恢复完整内容;其中 AGENTS.md/tools.md 原文本就含两道 hook 链(reconcile 那条"修正"是冗余),NOTES.md/progress 的 stale `post_ledger.py`→`post_ledger_entry.py` 已修。
3. **chmod 0444** grader + dataset(evaluator 隔离 C1)。
4. **实测**:`python3 evals/check_isolation.py` → **7/7 PASS, exit 0**;全量 `py_compile`/`json.load`/`bash -n`/`tomllib` 语法全过;grep 确认 handler 无 `httpx`/`sqlite3.connect`/`resp.json` 业务残留、护栏文件无 `NotImplementedError`。
5. v1(含早先手改)已备份到 `/tmp/OPS-reference-build.v1-backup-*`,可逆。

## 没消除的边界(读者必读,别当已验收)

- **只验了语法 + 隔离门**。未跑 `pytest`/`ruff`/`mypy`/真实 agent(需依赖、API key、真实 OCR/汇率)。"能跑"目前是语法级 + 逻辑级,非端到端运行级。
- **标注分级**:每文件标 〔源〕(可溯官方文档)/【推断】(仅上层有源)/【示例】(模板/数值,未在项目验证)。落到你项目要核版本/价格/flag。
- `fx_rate.py` 占位取了 c5 的缓存+保鲜形态;c2 的直连简版仅在 workflow 输出里(需要可取)。
- 这是 `docs/research/` 下的**惰性参考件**:此处 `.claude/*` 不会被真实 harness 加载,搬进真实 repo 根才生效。

## 指针

- `README.md` — 7 类操作层导览(自动产出)。
- `../HARNESS-construction-for-agent-dev.md` — 被操作化的**策略层**原稿。
- `../../flow.md` — 流程正本;末「已被打回」清单(本组装已核对无泄漏)。
