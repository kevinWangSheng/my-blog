"""context_config.py — expense-agent 被造 agent 运行时的
just-in-time 检索 + compaction 触发的具体配置 + 可执行触发逻辑。

范围:这是**被造 agent(expense-agent)自己运行时**怎么管 context,
      不是 Claude Code CL/开发回路那一侧(那侧见文件尾「CLI 侧」注释)。

依据(官方明文):
- just-in-time:context 里只放"轻量标识(file paths, stored queries, web links)",
  用时再用工具动态载入,不预先把全量塞进 context。〔源:effective-context-engineering〕
- compaction:对话逼近 context 窗上限时,把内容总结成高保真摘要、用摘要重启新窗;
  写 compaction prompt 先 maximize recall 再 iterate precision;
  最安全最轻的一档是 tool result clearing(深层工具原始结果不必再看)。〔源:同上 + harness-design〕
- compaction 实现路径(两选一,均可行):
  (a) 服务端自动 compaction(beta):在 Messages API 请求里加 `betas=["compact-2026-01-12"]`
      + `context_management.edits` 里配置 `{"type":"compact_20260112","trigger":{"type":
      "input_tokens","value":150000}}`(最低 50k)。支持 claude-opus-4-8 / 4.7 / 4.6 与
      sonnet-4-6。API 会自动生成 compaction 块并丢弃其前消息、自动清最旧 tool result。
      〔源:官方 compaction 文档 platform.claude.com/docs/en/build-with-claude/compaction,2026-01 起 beta〕
  (b) agent 循环里手动实现:估 token → 超阈值 → 调一次模型做摘要 → 用摘要重启。
      适用于需要精细控制摘要内容或不启用 beta 的场景。
  下面的 token 阈值/比例均为【示例·非规定】,需按真实 context 窗与成本调。

可验证性:本文件的 should_compact() / clear_stale_tool_results() / build_jit_*()
  是纯函数,有单测可跑(tests/test_context_config.py),不依赖网络。
  阈值数值本身=【示例】,无官方明文规定具体百分比。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

# ============================================================================
# A. 阈值配置(【示例·非规定】:按真实 context 窗 / 成本 / 模型调)
# ============================================================================
CONTEXT_WINDOW_TOKENS = int(os.environ.get("CTX_WINDOW_TOKENS", "200000"))
# 用量达窗口的这一比例就触发 compaction(留足余量给 compaction 自身用)。
COMPACT_TRIGGER_RATIO = float(os.environ.get("CTX_COMPACT_TRIGGER_RATIO", "0.75"))
# 单条工具结果超过这么多 token 就算「重」,优先清它(tool result clearing)。
HEAVY_TOOL_RESULT_TOKENS = int(os.environ.get("CTX_HEAVY_TOOL_TOKENS", "1500"))
# 最近 N 条消息永不清(防误伤当前推理需要的近因上下文)。
KEEP_RECENT_MESSAGES = int(os.environ.get("CTX_KEEP_RECENT", "6"))


def estimate_tokens(text: str) -> int:
    """粗估 token 数。此处接入你的 token 计数实现(tokenizer 或 API usage 字段);
    harness 不规定实现细节。真实项目建议用 tiktoken 或 API 返回的 usage.input_tokens。"""
    raise NotImplementedError(
        "此处接入你的 token 估算实现,harness 只规定约定不规定实现"
    )


# ============================================================================
# B. compaction 触发判定(纯函数,可单测)
# ============================================================================
def should_compact(used_tokens: int,
                   window: int = CONTEXT_WINDOW_TOKENS,
                   ratio: float = COMPACT_TRIGGER_RATIO) -> bool:
    """判断是否需要触发 compaction。用量达窗口 ratio 时返回 True。
    Anthropic 原则:逼近上限即 compact。〔源〕具体 ratio=0.75 为【示例】。
    此处接入你的 context 管理业务,harness 只规定触发阈值约定(见常量)不规定实现。"""
    raise NotImplementedError(
        "此处接入你的 compaction 触发判定实现,harness 只规定约定不规定实现"
    )


# compaction prompt 模板:先 recall 后 precision,是官方明文的写法原则。〔源〕
# expense-agent 专属:必须保住"已抽字段 / 已做入账决策 / 未解问题",这些是不可丢的高信号。
COMPACTION_PROMPT = """\
你正在压缩 expense-agent 的会话历史以重启一个更短的 context 窗。
第一优先级是 RECALL:不要丢任何下列信息——
  - 已从单据抽出的字段(vendor/date/amount/currency/category/confidence)及其依据;
  - 已做的入账决策(是否 post_ledger_entry、amount_base 换算用的 fx_rate 及日期);
  - 仍未解决的问题 / needs_human 触发原因 / 待人审项;
  - 用过但结果已不需重看的工具调用(ocr_extract/fx_rate 的原始大块输出可丢,只留结论)。
第二步再 PRECISION:删除寒暄、重复、已被后续覆盖的中间猜测、debug 噪声。
输出一段结构化摘要,使新窗里的 agent 无需回看原始历史即可继续。
"""


# ============================================================================
# C. tool result clearing(最轻的一档 compaction,官方点名最安全)〔源〕
# ============================================================================
@dataclass
class Message:
    role: str                 # 'user' | 'assistant' | 'tool'
    content: str
    is_tool_result: bool = False
    cleared: bool = False
    meta: dict = field(default_factory=dict)


def clear_stale_tool_results(messages: list[Message],
                             keep_recent: int = KEEP_RECENT_MESSAGES,
                             heavy_tokens: int = HEAVY_TOOL_RESULT_TOKENS) -> int:
    """把深层(非最近 keep_recent 条)的「重」工具结果替换成占位摘要,返回被清的条数。
    这是 compaction 前应先做的低风险动作(tool result clearing)。〔源〕
    此处接入你的 context 管理业务,harness 只规定约定(keep_recent / heavy_tokens 常量)不规定实现。"""
    raise NotImplementedError(
        "此处接入你的 tool-result-clearing 实现,harness 只规定约定不规定实现"
    )


# ============================================================================
# D. just-in-time 检索:context 里只放轻量标识,用时再取〔源〕
# ============================================================================
def build_jit_reference(file_path: str, kind: str = "invoice") -> dict:
    """不把整张发票原文塞进 context,只放可被工具按需载入的轻量标识。〔源〕
    约定:ref 只含 path/kind/load_via,不含全量内容;
    agent 看到这个 ref 后,自己决定何时调 ocr_extract(file_path)。
    此处接入你的 JIT 标识构造业务,harness 只规定「只放轻量标识」约定不规定实现细节。"""
    raise NotImplementedError(
        "此处接入你的 JIT reference 构造实现,harness 只规定约定不规定实现"
    )


# expense-agent 的 JIT 工具白名单 + 何时载入(给 agent 的指令,非预载数据)。〔推断·仅上层有源〕
JIT_TOOLS = {
    "ocr_extract": "仅在需要单据正文时调,用完原始大块文本可被 tool-result-clearing 清掉",
    "fx_rate":     "换算 amount_base 时才调;快变 -> 过期自动触发 web_search 保鲜",
    "post_ledger_entry": "危险写操作,默认 ask/deny,权限层强制",
}


def context_health(messages: list[Message]) -> dict:
    """一次性给出当前 context 健康度 + 该不该 compact,接进 agent 主循环每轮调用。
    此处接入你的 context 健康度计算实现,harness 只规定约定(COMPACTION_PROMPT / 常量)不规定实现。"""
    raise NotImplementedError(
        "此处接入你的 context 健康度计算实现,harness 只规定约定不规定实现"
    )
