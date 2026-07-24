# details/ — Phase 2 执行层素材(草稿)

> ⚠️ **状态:DRAFT,未最终化。** 这些是 Phase 2「照着能做」深钻时采集的原始素材(命令/模板/配置/脚本/表),由 subagent 搜索 + 初步对抗验证得到,**但尚未套用流程正本(`../flow.md`)那一轮 eval 的修正**(如 eval-first 降级、单 agent 默认、护栏 day-0)。
>
> **使用规则(深钻某步时)**:① 以 `../flow.md` 为准,与本草稿冲突时信 flow.md;② 重新核对时效(2026,版本号/价格/弃用会变);③ 用 subagent 对抗 eval 通过后,再把对应内容提炼为该步的正式 `SX-*.md`;④ 别把 `../sources.md` 末段「已被打回」的说法重新引入。
>
> 这批素材是抢救性落盘(否则随会话丢失)。**每条的一手出处见 `../sources.md`。**

## 文件 → 对应流程步
- `d1-knowledge-freshness.md` — 知识保鲜接入(横切 / S2)
- `d2-planning-and-tasks.md` — 规划与任务拆分(S1 / S2)
- `d3-context-files.md` — 上下文工程文件体系(S2 / S3)
- `d4-implementation-and-hooks.md` — 实现内循环 + hooks/subagent(S3)
- `d5-eval-driven.md` — eval 驱动 / 可观测(S4)
- `d6-guardrails-permissions-deploy.md` — 护栏/权限/多 agent/部署(S2 day-0 / S5)

> **正向索引(步→草稿)见 `../flow.md`「步 → 底料草稿 正向索引」。** 注意:文件名 d1–d6 **不**对应 S1–S6;**S0 暂无草稿**(从 flow.md S0 行 + ../sources.md A/I 段起)。
