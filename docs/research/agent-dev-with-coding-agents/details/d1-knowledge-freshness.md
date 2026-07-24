# d1 知识保鲜接入(草稿 · 未套 flow.md eval 修正,冲突以 ../flow.md 为准 · 出处见 ../sources.md B 段)

目的:对治 coding agent 内置知识陈旧 + SDK 更新快。轻→重组合用。

## 决策框架(轻→重)
1. 实时检索(临时/最新/用一次)→ coding agent 内置联网
2. MCP 文档服务器(版本对齐官方 docs、跨会话)→ Context7 / Ref / 厂商官方 docs MCP
3. 落盘 vendored docs / llms.txt(强 pin 版本、离线、进 review)
4. research 落盘(一次性深调研供后续读)
5. 验证层(版本对齐 + 对照官方 + 静态校验)贯穿

## 1. 内置实时检索
**Claude API / Agent 应用内**(当前版本号,会变,落盘前复核):
```json
"tools": [
  { "type": "web_search_20260209", "name": "web_search" },
  { "type": "web_fetch_20260209",  "name": "web_fetch" }
]
```
- dynamic filtering 需同时开 code execution tool;`max_uses` 控成本;`allowed_domains`/`blocked_domains`。价格 $10/1000 次(厂商自报)。Console 须先启用。
**Claude Code CLI**:best-practices「Give URLs / Let Claude fetch what it needs」;`/permissions` allowlist 常用文档域。
**Codex `config.toml`**:`web_search = "cached"`(默认)/`"live"`(=`--search`)/`"disabled"`。坑:cached 可能给过时 SDK 文档,核最新 API 用 `--search`。

什么场景先查:任何「这个 SDK 最新 API/版本/breaking change」——别信内置知识。稳定知识(语言基础/已在上下文里)不必查。

## 2. Context7 MCP(可复制)
- 概念:`resolve-library-id`(库名→Context7 ID,如 `/vercel/next.js`)+ `query-docs`(取版本特定文档)。
- 接入 Claude Code（stdio）：
```sh
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```
- 接入 Claude Code（远端 HTTP）：
```sh
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```
- `.mcp.json`（stdio）：
```json
{ "mcpServers": { "context7": { "command": "npx",
  "args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"] } } }
```
- `.mcp.json`（HTTP）：`{ "mcpServers": { "context7": { "url": "https://mcp.context7.com/mcp", "headers": { "CONTEXT7_API_KEY": "YOUR_API_KEY" } } } }`
- ⚠️ secrets 坑:别把 key 明文写进入 git 的 `.mcp.json`;Cursor 用 `${env:NAME}` 插值,Claude Code 用 user-scope / 未跟踪本地配置。
- pin 版本:提示里写版本(`Next.js 14 ... use context7`)或带版本 slug(`/vercel/next.js/v15.0.0`)。
- ⚠️ 让 agent 真用它:在 AGENTS.md/CLAUDE.md 写明触发条件「写 SDK 代码前先用 Context7 查当前版本文档」。
- 性能数字(token -65%/latency -38%)= **厂商自报,无独立验证**。

**Cursor MCP**(`.cursor/mcp.json`):`{ "mcpServers": { "name": { "command": "python", "args": ["mcp-server.py"], "env": { "API_KEY": "${env:API_KEY}" } } } }`;远端用 `url`+`headers`。
**厂商官方 docs MCP**(Stripe/Microsoft Learn 等,比聚合器权威):注册方式同构。Ref 的确切 endpoint **未核**。

## 3. 文档落盘
- 放仓库 `docs/`;格式:`llms.txt`(索引)/ `llms-full.txt`(全文内嵌)/ vendored `.md`(强 pin、可 review、手动更新)。
- 在 CLAUDE.md/AGENTS.md `@import`:`@docs/sdk/claude-agent-sdk-v0.X.md`;文件名带版本号钉死版本;顶部声明「以 @docs/sdk 为准,别用内置旧 API」。
- ⚠️ 别把整本 SDK 文档塞进 CLAUDE.md(过长被忽略);用 @import 分文件或放 skill。
- ⚠️ llms.txt 采用率仅 ~10%、主流 AI 平台不解析;对「agent 按需读文档」可用,别当 web 标准。

## 4. research 落盘再读
1. 派 subagent 调研(隔离上下文):`Use subagents to investigate <SDK> 当前 X API`,要求带官方 URL + 版本号 + 标 unverified;
2. 落盘 `research.md`(版本、API 签名+URL、breaking change、不确定点);
3. 实现阶段 `@research.md` 读回;4. 完成归档 `docs/archive/`(目录首次需自建)。
- ⚠️ 别让调研 agent 直接接实现不落盘——上下文一长会忘掉早期核实的版本。

## 5. 验证防过时/幻觉 API
- 版本对齐:先读 lockfile/`package.json` 拿实际版本,据此查文档(非 latest)。
- 对照官方一手源;冲突时信官方。
- 静态校验:`tsc`/类型/`build`/import resolve/smoke test——幻觉 API 在此暴露。Stop hook 钉死「实现后跑类型+构建,失败改到过」。
