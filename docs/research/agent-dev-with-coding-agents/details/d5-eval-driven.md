# d5 eval 驱动 / 非确定性调试 / 可观测(草稿 · 未套 flow.md eval 修正,冲突以 ../flow.md 为准 · 出处见 ../sources.md F 段)

> ⚠️ flow.md 边界:eval-driven 是应然非现状(89% tracing 但 52% 离线/37% 在线 eval、30% 不做);eval 须与被测 agent **隔离**否则被刷分;solo 早期降级为 tracing+抽检。

## 心智模型
agent 非确定,质量靠 eval(定义对错)+ traces(看实际怎么走)。Anthropic 命名 eval-driven development。

## eval 8 步(Anthropic《Demystifying evals》2026-01-09,可照抄)
1. 从 **20-50 条来自真实失败**的简单任务起步(挖 bug tracker / 客服队列 / 发布前手验的行为),别等攒几百条。
2. 每条任务要「两个领域专家独立判都得同一 pass/fail」的明确性。
3. 给 reference solution 证明任务可解。
4. harness 每个 trial 从干净环境隔离起步(防 correlated failure)。
5. grader 优先 deterministic;**判结果不判 tool-call 顺序**(否则 brittle);多组件给 partial credit。
6. 定期读 transcript 校准 grader。
7. 监控 eval saturation(逼近 100% 就没信号,加难任务)。
8. 区分 capability eval(低分起步,当「爬的山」)vs regression eval(近 100%,通过后毕业进回归集)。
- 指标:**pass@k**(k 次至少 1 次对,工具场景)vs **pass^k**(k 次全对,agent 场景,如 0.75³≈42%)。pass^k 由 Anthropic《Demystifying evals》页直接定义(「probability that all k trials succeed」),即一手出处。
- 坑:低分常是 eval 的 bug(Anthropic 例:CORE-Bench 42%→修死板 grader→95%,数字厂商自报)。

## 三层 eval
- 单步:dataset 输入=消息历史,只调单 node。
- 端到端/trajectory:跑全图,LLM-judge 判最终答案;轨迹用 `agentevals` 的 `create_trajectory_match_evaluator`(strict/unordered/superset/subset)。
- 多轮:会话结束触发,评 intent/outcome/trajectory。

## 工具接入
- **Anthropic Console**(零代码起步):提示编辑器→Evaluate 标签;prompt 需 1-2 个 `{{变量}}`;+Add Row / Generate Test Case / CSV;side-by-side + 5 分制 + prompt versioning。
- **LangSmith**:`langsmith` + `LANGSMITH_TRACING=true`;埋点 `@traceable`/`wrap_openai()`/框架集成;OTEL `https://api.smith.langchain.com/otel`;`Client().evaluate(target, data, evaluators, experiment_prefix, metadata)`;`openevals`(LLM-judge)/`agentevals`(轨迹)。
- **Braintrust**:`Eval(project,{data,task,scores})`;`autoevals`(ExactMatch/Levenshtein/JSONDiff/Factuality);CLI `bt eval --watch`;**experiment diff(score delta/红绿/regression 排序)做 hill-climbing**;CI `fail_on_regression:true`。
- ⚠️ **OpenAI 托管 Evals 平台弃用:2026-10-31 只读、2026-11-30 关停**(2026 别押;官方迁移建议改用 Datasets)。开源 `openai/evals` 还在但只收 model-graded YAML。

## hill-climbing 内循环
埋点采集 → 采样有问题 run 进 dataset → LLM-judge 标+人校 → 写 evaluator → 跑离线 experiment 看 trace+分 → 改 prompt/tool/model re-run **并排对比** → 在线 evaluator 持续盯。**每个 commit 跑 eval** 当第一道防线。
- 「eval 占开发 60-80%」= 从业者口径(Hamel/Shreya),非受控测量,标 unverified;且原义偏「error analysis/看数据」。

## 非确定性调试
- temp 0 仍漂的真因:浮点不结合 + kernel 缺 batch-invariance,随 endpoint 负载漂(Thinking Machines;数字厂商自报)。
- 战术:锁 temp 0/seed/版本(只消单机随机,消不掉共享 endpoint batch 漂);token 级 trace-diff 找首个分叉;batch size 1 专用 runner 复现;record-replay 工具/检索 + 冻时钟,只留模型一个变量。

## reward hacking 防御
- 现象:`sys.exit(0)`/改 verifier 返回 true/硬编码期望/`AlwaysEqual`(`__eq__` 永真)。模型一学会 reward-hack 会泛化出 misalignment(Anthropic ~12% 破坏尝试)。
- 防御:① grader 判结果抗 bypass;② **evaluator 与被测 agent 强隔离(Berkeley RDI:non-negotiable;8/8 benchmark 可刷分)**;③ hidden/held-out test split;④ mutation testing 当 grader 鲁棒性信号;⑤ inoculation prompting(Anthropic,削减 >75%,厂商自报)。

## 工具质量 = 质量杠杆
精修 tool description/命名显著降错误率(Anthropic SWE-bench);用 eval 迭代工具,追 accuracy/runtime/tool-call 数/token/tool errors;读 CoT 找卡壳/冗余调用,甚至把 transcript 喂回让 agent 自己改工具。
