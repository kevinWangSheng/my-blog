# expense-agent

单据/发票抽取 + 入账建议 agent。喂一张发票/收据(PDF/图片/文本),抽出结构化字段并给入账建议;危险动作(写 ledger.db)默认拦在人审后面。

## Overview

- 形态:**单 agent + tools**(不是多 agent;见 `docs/adr/ADR-0001`)。Python,调 Claude API。
- 模型:默认 `claude-opus-4-8`;高吞吐/省钱路径可切 `claude-sonnet-4-6`。不要追加日期后缀,不要凭记忆写别的 model id。
- 思考参数:【推断/unverified,需实跑验证】`thinking={"type":"adaptive"}` + `output_config={"effort":"high"}`。**不要用** `budget_tokens`(据报在 opus-4-8 上返回 400,未经本仓库实测验证)。不要传 `temperature`/`top_p`/`top_k`(据报同样 400,未经本仓库实测验证)。prefill(assistant 预填)同样报告返回 400,待验证。
- 输入:一张发票/收据(PDF / 图片 / 纯文本)。
- 工具(固定命名,全仓统一,禁止改名):
  - `ocr_extract(file_path)` → 调外部 OCR API,返回原始文本。读外部、花钱、**无本地副作用**。
  - `fx_rate(currency, date)` → 调外部汇率 API。快变数据,结果**不得长期缓存当事实**(见 `.claude/rules/tools.md`)。
  - `post_ledger_entry(entry)` → 写入本地 `ledger.db` 入账记录。**有副作用、危险**,默认 ask/deny,写库前必须人审(见三档约束块 + `docs/adr/ADR-0002`)。
- 输出 JSON(字段固定):`{vendor, date, amount, currency, amount_base, category, confidence, needs_human}`。
- 代码布局:主代码 `src/agent.py`,工具 `src/tools/`,eval 在 `evals/`,入账库 `ledger.db`(仓库根,gitignore)。

## Build & Test 命令

```bash
# 装依赖(用 uv;没有就 pip install -e ".[dev]")
uv sync

# 跑全部测试
uv run pytest

# 只跑一个用例
uv run pytest tests/test_extract.py::test_vendor_exact -q

# lint + 格式(提交前必过;CI 同款)
uv run ruff check src/ tests/ evals/
uv run ruff format --check src/ tests/ evals/

# 类型检查
uv run mypy src/

# 跑 eval grader(抽取字段精确/容差 + 分类 pass^k)
uv run python -m evals.run --suite extract --k 5

# 本地起 agent 处理一张单据(不写库:DRY_RUN=1 让 post_ledger_entry 走演练)
DRY_RUN=1 uv run python -m src.agent --file samples/invoice_001.pdf
```

环境变量:`ANTHROPIC_API_KEY`(必需)、`OCR_API_KEY`、`FX_API_KEY`。本地开发用 `.env`(gitignore),别硬编码进代码。

## Code style

- Python 3.11+。格式/lint 用 `ruff`(行宽 100),类型用 `mypy`(`src/` 必须通过,no untyped def)。
- 工具函数签名与文档串严格对齐 `input_schema`:Claude 靠 docstring 决定何时调工具,描述要写**何时调用**(不只是「做什么」)。
- 工具名固定:`ocr_extract` / `fx_rate` / `post_ledger_entry`。新增工具走 ADR,不许就地改名。
- 金额一律用 `Decimal`,不用 `float`;货币用 ISO 4217 三字母码。
- 解析模型返回的工具入参用 `json.loads()`,不要对序列化字符串做裸字符串匹配(opus-4-8 可能改变转义)。
- 输出 JSON 用 `output_config.format`(json_schema)约束,不要用已废弃的 `output_format`。

## Testing

- 抽取字段(vendor/date/amount/currency/...)用 **code-based grader**:字符串精确比对,金额做数值容差(默认 `abs(a-b) <= 0.01`)。不要让 LLM 当裁判去判抽取对错。
- 分类一致性(category)用 **pass^k**:同一输入跑 k 次(默认 k=5),全部命中同一类才算过。阈值与 k 在 `evals/config.yaml`。
- eval 是 **early & continuous** 的:写 prompt / 改工具的同时就跑 grader,不是「动手前先建完整 eval」,也不是「代码写完再补测试」。改 `src/` 前先在 `evals/cases/` 加/改 case。
- 新增/改抽取逻辑:先在 `evals/cases/` 加/改 case,再改 `src/`,跑 `python -m evals.run` 看回归。
- `gather → act → verify` 是**运行时**循环(agent 跑单据时的行为),不是开发流程的一步,别拿它当开发清单。

## Security

- `post_ledger_entry` 写 `ledger.db` 是危险动作:默认 ask/deny,**只有人审通过才放行**。
  - 开发期强制底:`.claude/settings.json`(permissions deny `Bash(rm:*)` / `Bash(sqlite3:*)`)+ PreToolUse hook 链:`.claude/hooks/pre_tool_use_guard.sh`(第一道,拦截通用危险写操作)与 `.claude/hooks/guard_ledger.py`(第二道,专门命中 ledger.db / post_ledger 写操作 exit 2 阻断)。这只管「Claude Code 开发期跑 shell 碰 ledger.db」。
  - 运行时强制底:`src/agent.py` 经 SDK 调 `post_ledger_entry` 时,在 manual tool loop 里自建 human-in-the-loop 确认 + DRY_RUN(Claude Code 的 Bash hook 拦不到运行时 SDK 调用)。
  - 本文件这段话只是指引(指引≠强制),真正拦截在上面两层。
- 永不硬编码/打印/外传密钥(`ANTHROPIC_API_KEY` / `OCR_API_KEY` / `FX_API_KEY`)。密钥从环境读。
- `ledger.db`、`.env`、`samples/` 里的真实单据进 `.gitignore`,不进版本库。
- `ocr_extract` 把单据原文发给外部 OCR:含 PII,日志里不要落原始单据全文。
- 危险/不可逆动作(改库 schema、批量回写、删 ledger.db)按 review-gated hard stop 处理:先说清命令+影响+回滚,等确认。

## PR 规范

- commit 用 **Conventional Commits v1.0.0**:`<type>[scope]: <desc>`。type ∈ feat/fix/docs/style/refactor/perf/test/build/ci/chore。破坏性变更用 `feat!:` 或加 `BREAKING CHANGE:` footer。
  - 例:`feat(tools): add fx_rate staleness guard` / `fix(grader): tolerate trailing whitespace in vendor`
- PR 描述必含:改了什么、为什么、跑了哪些证据(`pytest` 输出、`evals.run` 的 pass^k 结果)。
- 改 `src/tools/post_ledger_entry*` 或 `ledger.db` schema → PR 必须点名 reviewer,并贴 DRY_RUN 演练输出。
- push / 开 PR / release 需显式请求或项目工作流允许,不自作主张。CI 必过:ruff + mypy + pytest + evals.run。

## 三档约束

✅ Always:
- 提交前跑 `uv run ruff check` + `uv run pytest`
- 工具名用且只用 `ocr_extract` / `fx_rate` / `post_ledger_entry`
- 金额字段用 `Decimal`,货币用 ISO 4217
- 密钥从环境变量读,不硬编码

⚠️ Ask before:
- 新增依赖(pyproject.toml / uv.lock)
- 新增工具或改工具签名(先写 ADR)
- 改 `ledger.db` schema 或运行批量回写
- 改 `.claude/settings.json` 的 permissions / hooks

🚫 Never(散文指引,真正强制靠 settings.json + hooks):
- 硬编码 / 打印 / 外传 `ANTHROPIC_API_KEY` / `OCR_API_KEY` / `FX_API_KEY`
- 改 `ocr_extract` / `fx_rate` / `post_ledger_entry` 工具名
- 把 `fx_rate` 返回写进 prompt 常量或长期缓存当事实
- 未经人审直接写 `ledger.db`
- 用 LLM 当裁判判抽取字段对错
- 把 `ledger.db` / `.env` / 真实单据提交进版本库
