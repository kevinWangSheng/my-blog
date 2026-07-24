# d2 规划与任务拆分(草稿 · 未套 flow.md eval 修正,冲突以 ../flow.md 为准 · 出处见 ../sources.md A 段)

> ⚠️ 注意 flow.md 的 eval 修正:eval 不是「先建」而是贯穿;spec-driven 对 solo/小改是 overkill(轻量直接做)。本草稿的模板仍可用,但「先写完整 spec」要按规模取舍。

## 三套方法定位
- **Spec-Kit**(重,绿地/多人):`/speckit.constitution→specify→clarify→plan→tasks→implement`,每阶段产 md。
- **Anthropic Plan Mode**(轻):只读探查→出计划→人批准→才改;`claude --permission-mode plan` 或 `Shift+Tab`。
- **Addy Osmani agent-skills**(中):`planning-and-task-breakdown` skill,粒度规则 + task 模板。

## Spec 骨架(Spec-Kit spec-template.md,可复制)
```markdown
# Feature Specification: [FEATURE NAME]
**Feature Branch**: `[###-feature-name]`  **Status**: Draft
## User Scenarios & Testing *(mandatory)*
### User Story 1 - [Title] (Priority: P1)
**Independent Test**: [能独立测试并交付价值的方式]
**Acceptance Scenarios**:
1. **Given** [state], **When** [action], **Then** [outcome]
### Edge Cases
- What happens when [boundary]?
## Requirements *(mandatory)*
- **FR-001**: System MUST [capability]
- **FR-006**: System MUST [...] [NEEDS CLARIFICATION: 未指定项?]
### Key Entities *(if data involved)*
## Success Criteria *(mandatory)*
- **SC-001**: [可测,如「2 分钟内完成注册」]
## Assumptions
- [范围边界,如「移动端 v1 不做」]
```
要点:User Story 带 Priority + Independent Test;验收用 Given/When/Then;FR-### MUST;`[NEEDS CLARIFICATION]` 逼出澄清;Success Criteria 必须可测。

## Task 模板(Addy Osmani,自带验收+验证,推荐)
```markdown
## Task [N]: [title]
**Description:** 一段说明完成什么。
**Acceptance criteria:**
- [ ] [可测条件]
**Verification:**
- [ ] Tests pass: `npm test -- --grep "x"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [...]
**Dependencies:** [task 号 / None]
**Files likely touched:** [...]
**Estimated scope:** [Small/Medium/Large]
```
- Sizing 红线:S=1-2 文件/单会话;L+ **必须再拆**。
- 「验收标准写不出来 = 没拆对」。
- 规划 5 步:只读 map 依赖 → 画依赖图 → **垂直切片**(拒绝先全 DB 再全 API) → 套模板 → 按依赖排序 + 插 checkpoint。

## Spec-Kit tasks.md 条目格式
`[ID] [P?] [Story] Description`,如 `- [ ] T012 [P] [US1] Create Entity1 model in src/models/...`。`[P]`=可并行;五 phase:Setup→Foundational→User Stories→Polish→Dependencies。Story 内序:tests→models→services→endpoints。

## agent 应用特有的拆分维度(写函数之外)
推荐依赖顺序(自下而上,**此排序是综合推断,非单一权威源**):
```
工具(tools)契约 → system prompt → 编排/控制流 → 护栏 → eval 集 → 可观测
                  ↑ eval 集尽早建骨架,TDD 式并行扩充
```
每维套上面 task 模板,关键验收:
- 工具:每个 tool 有 name/desc/schema + example + 边界;沙箱跑样例迭代到 model 不用错。
- 编排:有 **max iterations 停止条件**;触发「应停止」路径不死循环。
- 护栏:pre-LLM(PII/注入)+ post-LLM(输出/动作校验);红队样例被拦 + 正常不误伤。
- eval 集:≥N golden cases 覆盖每条 Acceptance Scenario;有 pass 阈值。
