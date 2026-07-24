---
paths:
  - "evals/**/*.py"
  - "evals/**/*.yaml"
  - "evals/cases/**"
---

# Eval 层规则(evals/**)

仅当 Claude 在动 `evals/` 时加载。

## grader 方法(钉死)

- 抽取字段(vendor/date/amount/currency/amount_base):**code-based grader**。
  - 文本字段:规范化后精确比对(trim、大小写按字段定)。
  - 数值字段(amount/amount_base):数值容差,默认 `abs(pred - gold) <= 0.01`,阈值在 `evals/config.yaml`,别散落到代码里。
  - **不要用 LLM 当裁判**判抽取对错——抽取有确定的对错,用代码判。
- 分类一致性(category):**pass^k**。同一输入跑 k 次(默认 k=5),k 次必须全部落同一类才算这条过。k 与判定在 `evals/config.yaml`。

## eval 是贯穿的,不是前置门也不是后置补

- 写 prompt / 改工具 / 改抽取逻辑时**同步**跑 grader(early & continuous)。
- 不是「动手前先建一套完整 eval」;也不是「代码写完再补测试」。改 `src/` 前先在 `evals/cases/` 加/改对应 case。
- `gather → act → verify` 是 agent **运行时**的循环,不是 eval 的步骤,别写进 eval 流程。

## case 与运行

- 每条 case 是 `{input(单据), gold(期望 JSON), 可选 tags}`。真实单据含 PII 的进 gitignore,提交脱敏版。
- 跑:`uv run python -m evals.run --suite extract --k 5`;只看分类一致性:`--suite classify --k 5`。
- CI 跑 evals.run,pass^k 低于阈值即红。
