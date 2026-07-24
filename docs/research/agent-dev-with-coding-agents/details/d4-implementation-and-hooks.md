# d4 实现内循环 + hooks/subagent(草稿 · 未套 flow.md eval 修正,冲突以 ../flow.md 为准 · 出处见 ../sources.md D/E 段)

> ⚠️ flow.md 修正:测试/eval 是**贯穿非先行**;下面的 TDD-first 流程 +「锁测试文件 hook」对 solo / 小改要**按规模取舍**,别无条件套用(完整 TDD/eval 对小改是 overkill)。

## 实现驱动
- Explore(plan 模式只读)→ Plan(`Ctrl+G` 编辑计划)→ Implement(把验证写进同句:「实现后跑测试修到过」)→ Commit。一句话能描述的小改跳过 plan。
- 给锚点:「照 src/tools/search/ 的写法,新建 X 工具,只用现有依赖」。
- 纠偏:`Esc`(留上下文)/ `Esc Esc` 或 `/rewind` / `"Undo that"` / `/clear`。**纠正超两次→`/clear` 重开**。rewind 撤不回 bash 改的文件。
- 并行:`claude --worktree feature-x`(默认 `.claude/worktrees/`);坑:不复制 `.env`(用 `.worktreeinclude`),首次需先在该目录跑一次过信任弹窗。

## hook 退出码契约(易错)
- **exit 0** 放行;**exit 2** 阻断(stderr 反馈给 Claude);**其他码(含 exit 1)= 非阻断**(只在 transcript 报错)。→ ⚠️ **exit 1 不阻断,只有 exit 2 / 结构化 JSON 才阻断**。
- 决策字段**逐事件不同**:
  | 事件 | 阻断写法 |
  |---|---|
  | Stop / SubagentStop / PostToolUse / UserPromptSubmit | `{"decision":"block","reason":"..."}` |
  | PreToolUse | `hookSpecificOutput.permissionDecision = allow/deny/ask` |
- ⚠️ Stop hook 连阻 **8 次**被强制放行(脚本读 `stop_hook_active` 早退);⚠️ `~/.zshrc` 无条件 `echo` 会污染 hook stdout 破 JSON。

## PostToolUse 例(自动 prettier)
```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write",
  "hooks": [ { "type": "command",
    "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" } ] } ] } }
```

## Stop hook 确定性门(把 looks-done 变 pass/fail)
```json
{ "hooks": { "Stop": [ { "hooks": [
  { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify.sh" } ] } ] } }
```
```bash
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then exit 0; fi
if ! (npm run lint && npm run typecheck && npm test) >/tmp/verify.log 2>&1; then
  jq -n --arg log "$(tail -n 40 /tmp/verify.log)" \
    '{decision:"block", reason:("Verification failed; fix before stopping:\n" + $log)}'
  exit 0
fi
exit 0
```

## subagent(.claude/agents/*.md)
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. 只看 diff + 给定验收标准, 报具体可操作反馈。
```
- 冷启动隔离上下文;验收标准必须在 delegation 提示里**重述**;别用 fork(会泄露 writer 推理);只读 reviewer 用 `tools: Read, Grep, Glob`;`model:inherit` 默认(主会话弱则 reviewer 弱,pin `opus`)。
- 限定只报「影响正确性/明确需求」防过度工程(官方 code-review 插件:只报 编译失败/明确逻辑错/CLAUDE.md 违反,每条发现先并行验证再报)。

## TDD-with-agents(含反方)
- 正向:「写测试 ONLY [输入→输出 cases], avoid mocks, 不实现」→ 确认 fail → commit 测试 → 实现到全绿,**期间不改测试**。
- ⚠️ 反方:agent 会**删/改测试骗通过**(Kent Beck 证实「disabling or deleting tests」;ImpossibleBench:Claude 主要靠改测试 >79%;METR:明令别作弊反而更作弊)。
- 防御 = PreToolUse hook 锁测试文件:
```bash
#!/bin/bash
file_path=$(jq -r '.tool_input.file_path // empty' < /dev/stdin)
case "$file_path" in
  */test_*.py|*_test.py|*/tests/*|*.test.ts|*.spec.ts|*/__tests__/*)
    echo "BLOCKED: 测试文件冻结。让实现通过现有测试,别改测试。测试确有错就 STOP 问人。" >&2
    exit 2 ;;
esac
exit 0
```
- ⚠️ 版本相关:PreToolUse exit-2 阻 Write/Edit 某些版本不可靠(#13744)、可能让 Claude 停而不自修(#24327)→ 优先 JSON `permissionDecision:"deny"` + CI/git 兜底,装前实测。
- 纵深:测试先单独 commit;CI git-diff 门(同改测试+实现就要人审)。

## agent 应用代码特殊性
- 被测代码调 LLM,经典单测断言相等破裂 → **Mock 掉 LLM,确定性测周边脚手架**(工具实现/路由/参数 schema/retry/parser/guardrails),断言「哪个工具被以什么参数调用」+ 快照控制流。真实模型行为质量 → 归 eval(见 d5)。
