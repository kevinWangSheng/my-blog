---
title: "AGENTS.md 到底该写什么"
description: "AGENTS.md 给 coding agent 写开工边界。先讲它是什么,再用公开项目原文拆解哪些内容真的会改变 agent 的下一步动作。"
date: "2026-06-19"
tags: ["agents", "codex", "workflow", "context-engineering"]
visibility: "public"
series: "Agent Workflows"
---

我前面写 AGENTS.md 这篇时，犯了一个很典型的问题：我把结论讲出来了，但证据给得不够。

读者如果还不知道 AGENTS.md 是什么，前一版开头太快。读者如果想判断“这些公开项目到底怎么写”，前一版又太像我替大家消化过的二手总结。这样会有一个问题：文章看起来顺，但不够能让人信。

所以这一版我换个写法。

先讲背景：AGENTS.md 是什么、为什么会需要它、它和 README / 当前任务计划 / local 指令有什么区别。然后看公开项目原文。比如 Codex 关心 Bazel 和 snapshot，我会直接把 Codex AGENTS.md 里的相关段落摘出来，再解释它为什么值得学。后面再回到我们自己写 AGENTS.md 时应该怎么落地。

这篇文章的主张很简单：AGENTS.md 不该从模板开始写。它应该从项目里反复出错、反复需要确认、反复需要验证的地方长出来。

## AGENTS.md 是什么

可以先把它理解成：给 coding agent 的项目级工作说明。

README 通常写给人看，回答“这个项目是什么、怎么跑起来、怎么贡献”。AGENTS.md 更像 agent 开工前的边界文件，回答的是另一组问题：

- 真实源码在哪里？
- 哪些目录已经废弃？
- 动手前要先看什么？
- 哪些命令可以直接跑？
- 哪些命令有风险，要先问人？
- 改完之后怎样才算验证过？
- 哪些内容不能写进仓库、测试、日志、PR 描述？

这个差别很重要。人类维护者通常知道项目历史，知道某个旧目录已经不用了，知道某个测试会打真实云资源，知道某个 generated file 不能手改。agent 不知道。它看到一个仓库，只能从文件名、搜索结果、上下文和指令里推断。

AGENTS.md 的价值就在这里：把“只有项目里的人知道的工作边界”提前写给 agent。

我现在会把这类指令分成三层：

1. 团队共享的 AGENTS.md  
   放项目事实、命令、验证、安全、发布、生成文件、迁移、公共 API 这些所有维护者都该遵守的东西。

2. local / 用户级指令  
   放个人偏好，比如用中文回复、汇报格式、本机端口、本地脚本、自己喜欢的协作方式。

3. 当前任务计划  
   放这次要改什么、当前卡在哪里、preview 跑在哪个端口、review blocker 是什么。

这三层不能混。把当前任务计划塞进 AGENTS.md，未来 agent 会被旧状态带偏。把个人聊天偏好塞进团队文件，别人会看不懂。把团队安全边界只放在 local 指令里，换人换机器就丢了。

## 一条好规则要能改变动作

我判断 AGENTS.md 有没有用，会先问一个很粗的问题：这条规则会不会改变 agent 的下一步动作？

比如：

~~~md
- Follow best practices.
- Be careful with database changes.
- Keep the UI clean.
~~~

这些话都对，但不够。agent 看完还是不知道该搜哪个目录、跑哪个命令、什么时候停下来。

更有用的是这种：

~~~md
- Before adding a helper, search existing helpers in libs/, shared/, and test-support/.
- Do not edit applied migrations. Create a new migration and verify migrate/rollback.
- For layout changes, run ui-verify on the affected route and report axe, console, overflow, and Lighthouse results.
- Ask before adding production dependencies.
~~~

这些句子有触发条件、有动作、有验证或停手点。它们会改变 agent 的下一步。

下面看公开项目。为了避免“我替你总结”的感觉，我会先放原文摘录，再讲我从里面学到什么。

## 大仓库先解决“去哪里改”

大型仓库里，agent 最容易输在起点。它可能搜到一个名字相似的旧目录，或者在一个巨大的 monorepo 里改错 package。

Cloudflare Workers SDK 的 AGENTS.md 直接放了一张 “WHERE TO LOOK” 表。原文是这样：

~~~md
## WHERE TO LOOK

| Task                                           | Location                                       | Notes                                                            |
| ---------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------- |
| Add/modify a CLI command                       | `packages/wrangler/src/`                       | Commands registered in `src/index.ts` (2k+ line yargs tree)      |
| Change local dev behavior                      | `packages/miniflare/src/`                      | `src/index.ts` is the main `Miniflare` class                     |
| Modify Workers runtime simulation              | `packages/miniflare/src/workers/`              | ~30 embedded worker scripts, built via `worker:` virtual imports |
| Add a test fixture                             | `fixtures/`                                    | Each fixture is a full workspace member with own `package.json`  |
| Shared config types/validation                 | `packages/workers-utils/src/config/`           | `validation.ts` is the config normalizer (large file)            |
| Test helpers (runInTempDir, seed, mockConsole) | `packages/workers-utils/src/test-helpers/`     | Shared across wrangler, miniflare, others                        |
| Cloudflare API mocks for tests                 | `packages/wrangler/src/__tests__/helpers/msw/` | MSW handlers per API domain                                      |
| CI workflows                                   | `.github/workflows/`                           | `test-and-check.yml` is the primary gate                         |
| Build/deploy scripts                           | `tools/deployments/`                           | Validation + deployment helpers, run via `esbuild-register`      |
| Changeset config and rules                     | `.changeset/README.md`                         | Must read before creating changesets                             |
~~~

这个表很朴素，但对 agent 很有用。它直接把“任务”映射到“位置”。agent 如果要改 CLI command，第一步就不会跑去 miniflare。要改 runtime simulation，也不会从 wrangler 的 CLI 入口开始乱翻。

Airflow 的 AGENTS.md 也体现了这种大仓库的思路。它把不同测试入口写得很细：

~~~md
- **Run all tests in package:** `uv run --project <PROJECT> pytest path/to/package -xvs`
- **If uv tests fail with missing system dependencies, run the tests with breeze**: `breeze run pytest <tests> -xvs`
- **Run core or provider tests suite in parallel:** `breeze testing <test_group> --run-in-parallel` (test groups: `core-tests`, `providers-tests`)
- **Run core or provider db tests suite in parallel:** `breeze testing <test_group> --run-db-tests-only --run-in-parallel` (test groups: `core-tests`, `providers-tests`)
- **Run core or provider non-db tests suite in parallel:** `breeze testing <test_group> --skip-db-tests --use-xdist` (test groups: `core-tests`, `providers-tests`)
- **Run single provider complete test suite:** `breeze testing providers-tests --test-type "Providers[PROVIDERS_LIST]"` (e.g., `Providers[google]` or `Providers[amazon]` or `"Providers[amazon,google]"`)
~~~

它还把 newsfragment 的边界写得很具体：

~~~md
For `airflow-core` (and `chart/`, `dev/mypy/`) **user-facing** changes, add a newsfragment in that distribution's `newsfragments/` directory. **Golden rule: only add a newsfragment when you are certain the change is visible to users; when in doubt, do not add one** — a maintainer will request one in review if it is needed. Build/release tooling, CI, packaging, internal refactors, and dev-only scripts are not user-facing and must not get a newsfragment:

**Do not add newsfragments for `providers/` or `airflow-ctl/`** — their release managers regenerate the changelog from `git log` and do not consume newsfragments.
~~~

我从这类项目里学到的是：大仓库的 AGENTS.md 先别急着讲“代码风格”。更重要的是告诉 agent 去哪里、跑什么、哪些看起来类似的路径其实不一样。

迁移到普通项目，可以写成：

~~~md
## Where to work

- UI routes and components: apps/web/
- Public API handlers: services/api/
- Background jobs: workers/
- Shared generated clients: packages/client/, do not edit by hand
- Deprecated implementation: legacy/, read only for reference
~~~

这比“熟悉项目结构后再修改”有用。它直接给 agent 一个安全起点。

## 有真实资源风险时，要把命令分级

有些仓库里，命令不是中性的。一个测试命令可能会创建真实云资源，跑出成本，或者需要账号权限。

Terraform AWS Provider 的 AGENTS.md 对这点写得很明确：

~~~md
- Do not prompt for confirmation before running any of the safe commands above.
  - Any other commands may be unsafe and should not be run without confirmation.

#### Running tests
- Every PR must leave tests in a passing state.
- All existing tests must pass.
  - Use `make test` to run unit tests.
  - If your change breaks an existing test, fix it.
- CI is the gate. Run `make ci-quick`.
  - PRs with failing tests do not merge.
~~~

更关键的是 acceptance test 那段：

~~~md
- Do not modify `go.mod`/`go.sum` without running `go mod tidy`.
- Do not add new external dependencies without explicit approval.
- Beware of running acceptance tests (`make testacc`) without explicit approval — they create real AWS resources.
- The `website/` directory follows different conventions; see `docs/end-user-documentation.md`.

## Verification

Before finishing:
- `make build` — must compile cleanly.
- `make ci-quick` — zero warnings.
~~~

这里最值得学的是“safe commands”和“ask-before commands”的区分。很多 AGENTS.md 只写“改完跑测试”，但在这类项目里，这句话会误导 agent。测试并不都安全。

Tracecat 的主要风险落在客户数据和 CI 权限上。它的 AGENTS.md 写得更像安全边界：

~~~md
- Never copy customer-provided identifiers, customer names, URLs, tenant IDs,
  subscription IDs, workspace names, resource group names, incident IDs, emails,
  domains, tokens, or other potentially sensitive values into tests, docs,
  fixtures, snapshots, examples, logs, committed code, commit messages, PR or
  issue titles/bodies, PR comments, issue comments, review comments, or any
  other published repository text. Use generic phrasing such as "affected
  customer" or clearly synthetic placeholders instead, and search for the
  original strings before committing, pushing, or publishing PR/issue text.
~~~

它对 GitHub Actions 的手动触发也写得很具体：

~~~md
- Treat `workflow_dispatch` as a privileged path, not a convenience default.
- Guard privileged manual workflows with `TRUSTED_CI_ACTORS_JSON`.
- If another workflow triggers guarded `workflow_dispatch`, account for
  `github-actions[bot]` explicitly instead of weakening the allowlist.
- Keep workflow permissions read-only by default and grant write scopes only at
  the job level when a step demonstrably needs them.
- Do not add `pull-requests: write`, `packages: write`, or `id-token: write`
  unless a specific job step requires them.
~~~

这就是我想要的证据密度。它把“注意安全”拆成了可执行边界：哪些信息不能进入哪些载体，替代写法是什么；哪些 workflow 是 privileged path，权限默认是什么，哪些 write scope 不能随便加。

迁移写法可以很直接：

~~~md
## Safe commands

- Unit tests: make test
- Quick local CI: make ci-quick
- Build: make build

## Ask before

- Running tests that create real cloud resources.
- Adding production dependencies.
- Changing workflow permissions.
- Triggering privileged manual workflows.

## Never

- Copy customer identifiers, tenant IDs, URLs, emails, logs, or tokens into tests, fixtures, snapshots, examples, commits, PR text, or issue text.
~~~

## SaaS 项目的边界常常不在框架里

SaaS 项目很容易把 AGENTS.md 写成技术栈介绍：React、Node、Postgres、Redis、测试命令。那些当然有用，但我看公开案例时，真正有价值的常常是“仓库边界”和“安全热区”。

Unleash 的 AGENTS.md 一上来就讲 OSS 和 Enterprise 的关系：

~~~md
**Enterprise** extends OSS via a separate repository (`unleash-enterprise`) using a hook-based architecture. Enterprise does not fork OSS; it injects additional functionality through `preRouterHook`. If the user says that this is an enterprise feature, you need to ask where the enterprise repository is located and work across both this repository and the enterprise repository.
~~~

后面还继续展开 enterprise 怎么接进去：

~~~md
## Enterprise Integration

Enterprise extends OSS through hooks without forking:

1. **Entry**: `unleash-enterprise/src/index.ts` wraps OSS `start()`/`create()`
2. **Hook**: `preRouterHook` runs after OSS init, before route binding
3. **Extension**: Adds 50+ services, 30+ stores, 50+ controllers
4. **Gating**: License middleware restricts enterprise features

**Enterprise-Only Features**: Change Requests, SSO (SAML/OIDC), Service Accounts, Signals & Actions, Insights, SCIM, Private Projects, Release Plans, Safeguards

**Enterprise Composition**:
- `enterprise/src/util/setup-stores.ts` → Creates enterprise stores, merges with OSS stores
- `enterprise/src/util/setup-services.ts` → Creates enterprise services with combined stores
- `enterprise/src/create-enterprise-routes.ts` → Wires everything in `preRouterHook`
~~~

这个规则会直接改变 agent 的动作。用户说“这是 enterprise feature”，agent 不应该在 OSS repo 里硬造一个实现。它应该先确认 enterprise repo 在哪里，再判断要改 OSS hook、enterprise route，还是两边都要改。

Outline 的例子更窄，但也很有价值：

~~~md
- Always use `sanitizeUrl()` when setting `href` or `src` from user-controlled data in ProseMirror `toDOM` methods, regardless of whether it is imported via an alias or a relative path. Unlike React components, `toDOM` writes raw DOM and does not sanitize attribute values.
- Use CSRF protection.
- Use rateLimiter middleware for sensitive endpoints.
- Follow OWASP guidelines.
~~~

这条规则已经写到函数级了。它不适合所有项目，但很适合 Outline。因为它告诉 agent：这个项目里有一个具体 API，表面上像普通 DOM 输出，实际上绕开了 React 的保护，需要手动 sanitize。

我从 SaaS 项目里得到的判断是：AGENTS.md 不要只写框架和目录。它应该写清这些问题：

- 功能到底在 OSS repo、Enterprise repo，还是通过 hook 接入？
- 客户数据、tenant 信息、日志、fixture 的边界是什么？
- 哪些 workflow、权限、部署动作不能当普通开发便利？
- 哪些 API 或渲染方法有项目特有的安全坑？

## SDK 项目要把用户契约写在前面

SDK 项目的风险不只是“代码能不能跑”。它还要保护用户契约。

OpenAI Agents Python 的 AGENTS.md 对 public API 兼容性写得很直：

~~~md
Treat the parameter and dataclass field order of exported runtime APIs as a compatibility contract.

- For public constructors (for example `RunConfig`, `FunctionTool`, `AgentHookContext`), preserve existing positional argument meaning. Do not insert new constructor parameters or dataclass fields in the middle of existing public order.
- When adding a new optional public field/parameter, append it to the end whenever possible and keep old fields in the same order.
- If reordering is unavoidable, add an explicit compatibility layer and regression tests that exercise the old positional call pattern.
- Prefer keyword arguments at call sites to reduce accidental breakage, but do not rely on this to justify breaking positional compatibility for public APIs.
~~~

这段特别适合写给 agent。因为 agent 很容易“整理” public constructor：把参数挪一挪，把 dataclass 顺序调得更顺，把字段插到看起来更合理的位置。对 SDK 用户来说，这种整理可能就是 breaking change。

同一份文件还把跨模块影响面写出来：

~~~md
- Adding new tool/output/approval item types requires coordinated updates across:
  - `src/agents/items.py` (RunItem types and conversions)
  - `src/agents/run_internal/run_steps.py` (ProcessedResponse and tool run structs)
  - `src/agents/run_internal/turn_resolution.py` (model output processing, run item extraction)
  - `src/agents/run_internal/tool_execution.py` and `src/agents/run_internal/tool_planning.py`
  - `src/agents/run_internal/items.py` (normalization, dedupe, approval filtering)
  - `src/agents/stream_events.py` (stream event names)
  - `src/agents/run_state.py` (RunState serialization/deserialization)
  - `src/agents/run_internal/session_persistence.py` (session save/rewind)
- If the serialized RunState shape changes, update `CURRENT_SCHEMA_VERSION` in `src/agents/run_state.py` and the related serialization/deserialization logic.
~~~

这段已经超出了普通目录说明。它在告诉 agent：某类 change 会跨 item、run step、turn resolution、stream event、session persistence、schema version。没有这段，agent 很容易只改它当前看到的文件，然后漏掉系统状态。

迁移到 SDK 项目，我会写：

~~~md
## Public API compatibility

- Treat public constructor parameter order and dataclass field order as user-facing.
- Append optional public parameters when possible.
- If reordering is unavoidable, add compatibility handling and regression tests.
- If a serialized state shape changes, update schema versioning and backward-read logic.
- Do not edit generated translated docs by hand.
~~~

## Codex 的 AGENTS.md 证明：复杂项目要写“系统边界”

Codex 自己的 AGENTS.md 很适合说明一件事：复杂项目的规则不能停在“这是 Rust 项目”这种层级。它要写系统边界。

比如 sandbox 环境变量这段：

~~~md
- Never add or modify any code related to `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` or `CODEX_SANDBOX_ENV_VAR`.
  - You operate in a sandbox where `CODEX_SANDBOX_NETWORK_DISABLED=1` will be set whenever you use the `shell` tool. Any existing code that uses `CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR` was authored with this fact in mind. It is often used to early exit out of tests that the author knew you would not be able to run given your sandbox limitations.
  - Similarly, when you spawn a process using Seatbelt (`/usr/bin/sandbox-exec`), `CODEX_SANDBOX=seatbelt` will be set on the child process. Integration tests that want to run Seatbelt themselves cannot be run under Seatbelt, so checks for `CODEX_SANDBOX=seatbelt` are also often used to early exit out of tests, as appropriate.
~~~

这段在保护测试语义。agent 如果看到某个测试因为 sandbox env early exit，可能会以为这段逻辑多余，然后“清理”掉。AGENTS.md 直接告诉它：别碰，这跟 agent 自己运行工具时的 sandbox 能力有关。

再看 Cargo 和 Bazel 的差异：

~~~md
- If you change Rust dependencies (`Cargo.toml` or `Cargo.lock`), run `just bazel-lock-update` from the
  repo root to refresh `MODULE.bazel.lock`, and include that lockfile update in the same change.
- After dependency changes, run `just bazel-lock-check` from the repo root so lockfile drift is caught
  locally before CI.
- Bazel does not automatically make source-tree files available to compile-time Rust file access. If
  you add `include_str!`, `include_bytes!`, `sqlx::migrate!`, or similar build-time file or
  directory reads, update the crate's `BUILD.bazel` (`compile_data`, `build_script_data`, or test
  data) or Bazel may fail even when Cargo passes.
~~~

这段就很像你说的“不要只说 Codex 关心 Bazel”。应该把原文放出来。读者看到这里才会明白：这个项目里 Cargo 过了不代表 Bazel 过了，依赖和 compile-time file access 都有额外动作。

Codex 的测试入口也写得很具体：

~~~md
Run `just fmt` (in the `codex-rs` directory) automatically after you have finished making code changes anywhere in this repository; do not ask for approval to run it. Additionally, run the tests:

1. Do not run `cargo test` directly. Use `just test` so test execution follows the repo defaults.
2. Run the test for the specific project that was changed. For example, if changes were made in `codex-rs/tui`, run `just test -p codex-tui`.
3. Once those pass, if any changes were made in common, core, or protocol, run the complete test suite with `just test`. Avoid `--all-features` for routine local runs because it expands the build matrix and can significantly increase `target/` disk usage; use it only when you specifically need full feature coverage. project-specific or individual tests can be run without asking the user, but do ask the user before running the complete test suite.
~~~

还有 TUI snapshot 这一段：

~~~md
This repo uses snapshot tests (via `insta`), especially in `codex-rs/tui`, to validate rendered output.

**Requirement:** any change that affects user-visible UI (including adding new UI) must include
corresponding `insta` snapshot coverage (add a new snapshot test if one doesn't exist yet, or
update the existing snapshot). Review and accept snapshot updates as part of the PR so UI impact
is easy to review and future diffs stay visual.

When UI or text output changes intentionally, update the snapshots as follows:

- Run tests to generate any updated snapshots:
  - `just test -p codex-tui`
- Check what’s pending:
  - `cargo insta pending-snapshots -p codex-tui`
- Review changes by reading the generated `*.snap.new` files directly in the repo, or preview a specific file:
  - `cargo insta show -p codex-tui path/to/file.snap.new`
- Only if you intend to accept all new snapshots in this crate, run:
  - `cargo insta accept -p codex-tui`
~~~

这段证据说明了一个关键点：AGENTS.md 可以写得很细，只要这个细节真的改变工作方式。Codex 的 TUI 改动不能停在“跑过测试”，UI/text output 的变化要通过 snapshot 让 review 能看见。对这种项目，AGENTS.md 里写 snapshot 命令是在保护 review 质量。

我会把这类项目的 AGENTS.md 写成系统边界清单：

~~~md
## System boundaries

- Do not modify sandbox capability checks unless the change is explicitly about sandbox behavior.
- Cargo passing is not enough for dependency or compile-time file changes; update Bazel metadata too.
- Use project test wrappers, not raw language defaults.
- UI or text output changes require snapshot generation, review, and acceptance.
- Large or full-suite commands require explicit confirmation when they are expensive.
~~~

## CLI 项目适合写 reviewer 热点

Databricks CLI 的 AGENTS.md 很像把 reviewer 反复说的话提前写给 agent：

~~~md
**RULE: Do not modify or remove existing comments in code you didn't write.** Comments often encode non-obvious context (a bug reference, a workaround, a reason the code is shaped a certain way) that is lost if rewritten. Leave them alone unless the user explicitly asks for a change.

**RULE: Prefer simplicity over cleverness. Avoid speculative fallbacks and default values.** If you catch yourself adding a fallback branch "just in case," identify the correct path and use only that one. Reviewers in this repo reject speculative flexibility.

**RULE: Keep each PR focused on one change.** If you notice an unrelated cleanup, bug fix, or refactor while making your primary change, leave it alone or put it in a separate PR. Reviewers consistently ask to split mixed PRs, especially when a dependency bump or schema diff rides along with a feature change.

**RULE: Before adding a new helper, search the codebase for an existing one.** Common homes: `libs/` (shared utilities), `libs/databrickscfg/` (config), `libs/git/`, `libs/filer/`, `libs/cmdio/` (CLI I/O, spinners, prompts), `libs/env/` (env vars), `libs/testserver/`, `libs/structpath/` and `libs/dyn/` (path / dynamic values), `acceptance/bin/` (acceptance test helpers), `internal/mocks/` (generated mocks).
~~~

它后面还有更具体的 reviewer 热点：

~~~md
**RULE: When adding a direct Go dependency, annotate its license in `go.mod` and update `NOTICE`.** Before picking the SPDX identifier, read `internal/build/license_test.go` to see the current allowlist (the `spdxLicenses` map). That test is the source of truth and will fail CI if a direct `require` line lacks a matching SPDX suffix comment (e.g. `// MIT`). Also add a corresponding entry to `NOTICE` under the matching license section. If a dep's license isn't on the allowlist, discuss before adding.

**RULE: Do not use `os.Exit()` outside of `main.go`.** `main.go` owns the exit path; calling `os.Exit()` elsewhere skips deferred cleanup and complicates testing.

**RULE: Do not remove or skip failing tests to fix CI.** Fix the underlying issue instead.

**RULE: Do not leave debug print statements in committed code.** `fmt.Println`, `log.Printf`, or similar. Always scrub before committing.
~~~

这类规则看起来碎，但很真实。它们通常来自 review 摩擦：有人改了旧注释，有人加了 speculative fallback，有人顺手清理 unrelated diff，有人新增 helper 前没搜，有人加依赖忘了 license，有人用 os.Exit 绕过 cleanup。

AGENTS.md 很适合放这种 reviewer 热点。因为它们会改变 agent 的动作。

## 小项目不用写成大厂手册

FileKit 的 AGENTS.md 很短，但它把该说的说了：

~~~md
FileKit is split across multiplatform modules: `filekit-core` contains platform-agnostic APIs, while dialogs, Compose bindings, and Coil integration live in `filekit-dialogs`, `filekit-dialogs-compose`, and `filekit-coil`. Shared source sets live under `src/*Main`, with platform tests in sibling `src/*Test` directories. Sample apps under `samples/` (`sample-core`, `sample-compose`, `sample-file-explorer`) demonstrate integration patterns; update them alongside library changes when user-facing behaviour shifts. API docs and release notes are tracked in `docs/` and `documentation-v0.8.8.md`.

## Build, Test, and Development Commands
Use `./gradlew assemble` to ensure all published artifacts compile before raising a PR. Run `./gradlew :filekit-core:check :filekit-dialogs:check` to execute the multiplatform test matrix for the primary modules. Sample apps can be exercised with `./gradlew :samples:sample-compose:composeApp:run` (desktop) or by opening the Gradle targets in Android Studio for mobile builds.
~~~

测试和 PR 规则也不长：

~~~md
## Testing Guidelines
Add unit tests in the closest `src/<target>Test` directory; default to `commonTest` when behaviour is shared and mirror target-specific coverage otherwise. Test names follow the `Subject_action_expectation` convention (e.g., `FilePicker_openDirectory_returnsFolder`). Run `./gradlew check` locally before every push and ensure new features include regression coverage for at least one non-JVM target. When behaviour depends on native APIs, document manual verification steps in the PR description.

## Commit & Pull Request Guidelines
Commits are short, imperative statements and often begin with an emoji category (e.g., `✨ Add WASM picker`); keep related changes squashed together. Each PR should describe the change, note affected platforms, call out doc updates, and link issues or discussions when relevant. Attach screenshots or screen recordings when UI behaviour changes.
~~~

这份文件说明：AGENTS.md 不需要为了显得专业而变长。小项目只要讲清模块边界、命令、sample app、测试位置、UI 证据，就够有用。

## 模板什么时候有用

我不建议从模板开始写，不代表模板没有价值。

模板适合当检查表。比如你已经从项目摩擦里写出第一版 AGENTS.md 之后，可以拿模板扫一遍：有没有写 build/test 命令，有没有写 ask-before，有没有写 never，有没有写验证证据，有没有写 local 和 team 的边界。

但模板不适合当正文来源。因为模板不知道你的项目怕什么。它不知道 acceptance test 会不会创建真实资源，不知道 Enterprise 功能是不是在另一个仓库，不知道 public constructor 参数顺序是不是用户契约，也不知道某个 UI 输出是不是必须走 snapshot review。

所以我的顺序是：先从真实摩擦写，再用模板补漏。

## 回到我们自己怎么写

看完这些案例，我现在会先列项目最近三类摩擦：

1. agent 容易走错哪里  
   比如旧目录、废弃实现、生成文件、monorepo package 边界。

2. agent 容易跑错什么  
   比如真实云资源测试、昂贵全量测试、需要凭证的 e2e、生产或发布命令。

3. agent 容易漏掉什么  
   比如 snapshot、schema version、docs、sample app、changelog、license、NOTICE、UI 证据、compat regression。

然后把它们写成能改变动作的规则。

一个最小版本可以这样：

~~~md
# AGENTS.md

## Stable facts

- Current implementation lives in <path>.
- Deprecated implementation lives in <path>; read only for reference.
- Generated files are not edited by hand.

## Where to work

- UI routes and components: apps/web/
- API handlers: services/api/
- Background jobs: workers/
- Shared clients: packages/client/

## Before editing

- Run git status.
- Inspect nearby call sites.
- Search existing helpers before adding new utilities.
- If the change touches public API, migration, deployment, auth, or generated files, identify the boundary first.

## Verification

- Backend changes: <command>.
- UI changes: <command> on the affected route, with screenshot / console / accessibility evidence.
- CLI output changes: update snapshots or acceptance output.
- Do not say "verified" without reporting the exact command or runtime check.

## Ask before

- Adding production dependencies.
- Running tests that create real external resources.
- Changing deployment, migration strategy, public API compatibility, workflow permissions, or production data.
- Pushing, releasing, or touching production.

## Never

- Commit secrets.
- Copy customer data into fixtures, logs, examples, commits, PR text, or issue text.
- Restore deprecated pipelines.
- Modify applied migrations in place.
~~~

这只是起点。真正要留下哪些条目，要看项目自己的风险。

如果是大 monorepo，补 “WHERE TO LOOK”。  
如果是云 provider，补 safe commands / ask-before commands。  
如果是 SaaS，补客户数据、tenant、workflow 权限、enterprise/OSS 边界。  
如果是 SDK，补 public API、schema、generated docs、compat tests。  
如果是 CLI，补 helper 搜索、输出 snapshot、依赖 license、debug print。  
如果是小 library，删掉大部分，只保留模块边界和验证命令。

## 检查一条规则值不值得放进去

我现在会问这些问题：

- 它会不会改变 agent 的下一步动作？
- 它有没有触发条件？
- 它说清了要做什么、不要做什么吗？
- 它说清了怎么验证吗？
- 它是不是团队共享规则？
- 它是不是当前任务状态？
- 它是不是个人偏好？
- 它离对应代码够近吗？要不要下沉到子目录？
- 它来自真实摩擦，还是来自想象中的最佳实践？

AGENTS.md 写得好不好，不看它像不像一份完整文档。看 agent 读完以后，会不会少犯一个真实错误。

这也是我看完这些公开案例后最想保留的判断：AGENTS.md 是从返工里长出来的开工边界。它要把项目里那些最容易走错、最难靠模型常识补上的东西，放到 agent 动手之前。

参考过的公开文件：

- [Apache Airflow AGENTS.md](https://github.com/apache/airflow/blob/main/AGENTS.md)
- [Cloudflare Workers SDK AGENTS.md](https://github.com/cloudflare/workers-sdk/blob/main/AGENTS.md)
- [Terraform AWS Provider AGENTS.md](https://github.com/hashicorp/terraform-provider-aws/blob/main/AGENTS.md)
- [Tracecat AGENTS.md](https://github.com/TracecatHQ/tracecat/blob/main/AGENTS.md)
- [Unleash AGENTS.md](https://github.com/Unleash/unleash/blob/main/AGENTS.md)
- [Outline AGENTS.md](https://github.com/outline/outline/blob/main/AGENTS.md)
- [OpenAI Agents Python AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md)
- [OpenAI Codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)
- [Databricks CLI AGENTS.md](https://github.com/databricks/cli/blob/main/AGENTS.md)
- [FileKit AGENTS.md](https://github.com/vinceglb/FileKit/blob/main/AGENTS.md)
