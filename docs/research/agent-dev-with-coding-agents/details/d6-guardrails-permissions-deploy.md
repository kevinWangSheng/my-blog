# d6 护栏/权限/多 agent/部署(草稿 · 未套 flow.md eval 修正,冲突以 ../flow.md 为准 · 出处见 ../sources.md G 段)

> ⚠️ flow.md 修正:成本/递归/时间硬上限 + evaluator 隔离 = **day-0**,不是最后;单 agent 强默认。

## 护栏原则(Anthropic building-effective-agents)
- 沙箱 + 大量测试;agent loop 带 **停止条件(max iterations)**;人类检查点 pause;第二模型筛查第一个的输入/输出;保持简单+透明。

## Claude Code 权限模式(settings.json `defaultMode`)
| 模式 | 行为 |
|---|---|
| default | 每个工具首次提示 |
| acceptEdits | 自动批文件编辑 + 常见 fs(mkdir/touch/mv/cp),不含任意 shell |
| plan | 只读探索 |
| auto | 自动批 + 后台安全分类器(research preview) |
| dontAsk | 除非预批否则自动拒 |
| bypassPermissions | 跳过提示(`rm -rf /`、`rm -rf ~` 仍熔断) |
- 求值顺序:**PreToolUse hooks → deny → ask → allow → 模式默认**。deny 优先,managed deny 无法被 `--allowedTools` 覆盖。
- ⚠️ 权限由 **harness 强制,非模型**;CLAUDE.md 只影响「想做什么」。Bash 参数约束很脆(用 deny curl/wget + WebFetch domain);Read/Edit deny 挡不住子进程(需 sandbox)。

## 危险操作 gate（PreToolUse,exit 2 阻断）
```bash
# .claude/hooks/protect-files.sh
INPUT=$(cat); FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
for p in ".env" "package-lock.json" ".git/"; do
  [[ "$FILE_PATH" == *"$p"* ]] && { echo "Blocked: $FILE_PATH ($p)" >&2; exit 2; }
done; exit 0
```
惯用:allow 放裸 `Bash`,再用 PreToolUse hook 拒少数危险命令(白名单宽+黑名单精)。

## Codex 权限(三轴)
`sandbox_mode`(read-only / workspace-write / danger-full-access)× `approval_policy`(untrusted / on-request / never)× `network_access`。低风险本地:`--sandbox workspace-write --ask-for-approval on-request`;YOLO=`danger-full-access + never`,**官方仅限隔离环境**。平台机制:macOS Seatbelt / Linux bubblewrap / Windows Sandbox。

## 按风险设自主性
| 风险 | Claude Code | Codex | 人介入 |
|---|---|---|---|
| 读/探索 | plan | read-only | 无 |
| 可逆本地写 | acceptEdits + deny 敏感路径 | workspace-write + on-request | 越界才问 |
| 不可逆/外部副作用 | default + ask 规则 gate | untrusted | 每次确认 |
| 批量自动化 | bypassPermissions **仅容器** | danger-full-access **仅隔离 CI** | 事后审 trace |
- 压短自主链(≤少数步):依据=停止条件 + 误差复合。

## 误差复合(标边界)
∏pᵢ / 0.95^N 是**上界玩具模型**,作者自承简化;只用来论证「缩短链路」,**别当实测衰减率**。对治:缩短链路、确定性子步(schema 校验)、校验+重试(best-of-N+judge)、人介入点、护栏隔离。
- ⚠️ 成本护栏 day-0:真实案例 agent 对 429 死循环 63h 烧 $4,200——budget/递归/墙钟硬上限须前置。

## 多 agent(何时值得)
- orchestrator-worker:lead 定策略并行 spawn subagent,回传 findings。Anthropic 内部研究评估 +90.2% vs 单 agent,但 **~15× token**(单 agent ~4×);token 解释 80% 性能方差。
- **何时值得**:breadth-first 可并行 + 任务价值 >> 15× token。**何时别用(官方)**:需共享 context/强依赖/实时协调;**大多数编码任务**。
- 旗舰示范:16 并行 Claude、~$20k、10 万行 C 编译器,文件锁认领任务、无 orchestrator——**能力压测非日常**。
- 判据:默认 **单 agent + 好工具 + 短链**;仅子任务真独立 + 价值够 + 不强依赖共享 context 才上多 agent。

## 安全
- AI 代码漏洞率(Veracode:45% 引入 OWASP Top10,安全通过率不随模型变大改善)——**受控基准(无安全提示)≠ 生产**,且安全厂商有立场。
- secrets 环境变量/未跟踪文件,deny `Read(.env)`/`Read(**/.env)` + sandbox。
- Replit 删库教训:事实层(code freeze+read-only 下删生产库+伪造~4000 假记录)属实;「说谎/恐慌」是模型文本非意图。**约束必须在工具/权限层强制,不能只 prompt 说 read-only**;dev/prod 隔离 + 不可逆 gate + 备份。

## 部署 + 知识回流
- 部署形态:API / SDK / MCP server(OpenAI:Responses API=一次模型+工具够用 vs Agents SDK=应用自己管编排+state)。
- 失败 trace 回流闭环:生产 trace → 在线 scorer 评分 → 失败 trace 转 eval case → eval 套件随真实行为增长 → 回归自动被抓 → CI 门(Braintrust 2026)。多数事故是 tool-call 失败/context 截断/跑飞循环,需 agent-aware instrumentation(OTel GenAI 语义约定,中立)。
- 文档/约定随版本更新:决策日志 + 稳定 agent 入口 + 执行层易变文件分离。
