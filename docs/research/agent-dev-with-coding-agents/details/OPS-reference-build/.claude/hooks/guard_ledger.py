#!/usr/bin/env python3
"""
PreToolUse guard for expense-agent.

Claude Code 在每次 Bash 工具调用前,把一段 JSON 经 stdin 喂给本脚本
(见官方 hooks 文档:tool_name / tool_input.command 等字段)。本脚本只做一件事:
把『针对 ledger.db 这个文件的写操作 / 任何 post_ledger 调用』拦下来 ——
这是 settings.json 的 permissions 做不到的子串判定（Bash() 只支持命令前缀，
不支持 *ledger.db* 这种中段子串 glob，所以子串判定必须落在这里）。

阻断契约（官方硬事实,别写错）:
  - sys.exit(2)  → 阻断工具调用,stderr 文本回喂给 Claude 当错误原因。
  - sys.exit(0)  → 放行（本脚本不做决定,走正常权限流）。
  - sys.exit(1)  → 【不会阻断】被当作非阻断错误,工具照常执行。想拦就必须 exit 2。

只覆盖『开发期 Claude Code 跑 shell 碰 ledger.db』。运行时 src/agent.py 经 SDK
调 post_ledger_entry 不经过 Bash 工具,本 hook 拦不到 —— 运行时人审在 agent.py 内自建。
"""
import json
import re
import sys

# 命中即阻断的写操作模式（大小写不敏感）。只针对 ledger.db 这个文件 + post_ledger 入口。
_LEDGER = r"ledger\.db"
_BLOCK_PATTERNS = [
    # 任何提到 post_ledger 的命令（直接调入账入口）
    re.compile(r"post_ledger", re.IGNORECASE),
    # sqlite3 直接改 ledger.db（insert/update/delete/drop/alter/.import 等写操作）
    re.compile(r"sqlite3\b.*" + _LEDGER, re.IGNORECASE),
    # 删除 / 移动 / 截断 ledger.db 文件
    re.compile(r"\b(rm|mv|truncate|shred|unlink)\b.*" + _LEDGER, re.IGNORECASE),
    # 重定向写入 ledger.db（> ledger.db / >> ledger.db / tee ledger.db）
    re.compile(r"(>>?|tee\b).*" + _LEDGER, re.IGNORECASE),
    # 经 python 内联脚本写 ledger.db（execute/commit 配合 ledger.db 出现）
    re.compile(r"python3?\b.*" + _LEDGER + r".*(execute|commit|insert|update|delete)", re.IGNORECASE),
]


def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        # 解析不了输入:不做阻断决定,放行走正常权限流（exit 0,不是 1/2）。
        return 0

    if payload.get("tool_name") != "Bash":
        return 0

    command = (payload.get("tool_input") or {}).get("command", "")
    if not isinstance(command, str) or not command:
        return 0

    for pat in _BLOCK_PATTERNS:
        if pat.search(command):
            sys.stderr.write(
                "BLOCKED by guard_ledger.py: 该命令试图写/删 ledger.db 或调 post_ledger。\n"
                "写入账库是危险不可逆动作,默认禁止（见 AGENTS.md Security / ADR-0002）。\n"
                "需要真实写库请走人审:用 DRY_RUN 演练,或在 ADR 记录后由 reviewer 放行。\n"
                f"命中命令: {command}\n"
            )
            return 2  # exit 2 = 阻断（exit 1 不阻断,别写错）

    return 0


if __name__ == "__main__":
    sys.exit(main())
