"""src/agent.py — expense-agent 被造 agent 入口占位。

此文件是「被造 agent 业务实现」的契约占位。
run_expense_agent() 的签名与 docstring 是 harness 约定的接口;
业务体(调 Claude API + 工具循环 + post_ledger_entry 人审门)
由 agent 开发者实现,harness 不规定实现细节。

harness 侧约定:
  - evals/run_agent.py 通过 `from src.agent import run_expense_agent` 调用此函数
  - 参数名与 evals/dataset/*.jsonl 的 input 字段对齐
  - 返回值 dict 字段与 evals/dataset/*.jsonl 的 reference 字段对齐:
      {vendor, date, amount, currency, amount_base, category, confidence, needs_human}
  - 若 agent 未实现,run_agent.py 会在 import 时捕获异常并以 exit 2 报错,
    不会静默伪造输出
"""
from __future__ import annotations


def run_expense_agent(
    file_path: str,
    base_currency: str = "USD",
    as_of_date: str | None = None,
) -> dict:
    """Run the expense agent on one invoice/receipt and return extracted fields.

    此处接入被造 agent 的业务逻辑。harness 不规定实现方式。
    典型实现包括:
      1. 调 ocr_extract(file_path) 获取原始文本
      2. 调 Claude API (claude-opus-4-8 / claude-sonnet-4-6) 抽取字段
      3. 若 currency != base_currency,调 fx_rate(currency, date) 换算 amount_base
      4. 若 needs_human=True 或 confidence 低,设 needs_human=True 等待人审
      5. (可选,须人审通过)调 post_ledger_entry(entry) 写入 ledger.db

    Args:
        file_path: 发票/收据文件路径(PDF/图片/文本),与 evals/dataset 的 input.file_path 对齐。
        base_currency: 记账本币 ISO 4217 三字母码,默认 "USD"。
        as_of_date: 取汇率用的日期 "YYYY-MM-DD";None 时用单据日期。

    Returns:
        dict with keys:
          vendor (str): 供应商名称
          date (str): 发票日期 "YYYY-MM-DD"
          amount (float): 原币金额
          currency (str): 原币 ISO 4217 代码
          amount_base (float): 换算后本币金额
          category (str): 费用类别,值域见 src/tools/schemas.py POST_LEDGER_ENTRY_TOOL enum
          confidence (float): 0.0–1.0 抽取置信度
          needs_human (bool): True 表示需要人审后才能入账

    Raises:
        NotImplementedError: 业务体尚未实现时。
    """
    raise NotImplementedError(
        "run_expense_agent is a placeholder. "
        "Implement the agent business logic in src/agent.py. "
        "The harness (evals/run_agent.py) calls this function; "
        "it must return a dict with the fields listed in the docstring."
    )
