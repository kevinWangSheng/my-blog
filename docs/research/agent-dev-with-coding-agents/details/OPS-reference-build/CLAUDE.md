@AGENTS.md

## Claude Code

本仓库的工程约定全部写在 `AGENTS.md` 里(上面那行已把它整篇导入)。Claude Code 不原生读 `AGENTS.md`,靠这一行 @import 转发,与 Codex / Cursor 等读 AGENTS.md 的 agent 共用同一份事实源,不重复维护。

决策日志(为什么这么配,改配置前先读):见 `docs/adr/`
- ADR-0001 单 agent + tools(不拆多 agent)
- ADR-0002 post_ledger_entry 走 ask/deny + PreToolUse 硬阻断(写库前必须人审)
- ADR-0003 eval 用 code-based grader + pass^k,贯穿开发(不是写完再补)

硬阻断 vs 指引的边界:本文件与 `AGENTS.md`、`.claude/rules/*.md` 都是「上下文/指引」,Claude 读了「尽量」遵守,不是强制层。要真正拦住一个动作(开发期跑 shell 碰 ledger.db),必须靠 `.claude/settings.json` 的 permissions + `.claude/hooks/pre_tool_use_guard.sh`(PreToolUse 链第一道) + `.claude/hooks/guard_ledger.py`(PreToolUse 链第二道,exit 2 才阻断)。见三档约束块的「🚫Never」。
