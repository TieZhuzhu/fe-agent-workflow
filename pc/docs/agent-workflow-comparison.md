# Agent 工作流对比：Current vs OpenSpec vs Spec-Kit vs Superpowers

> **对照对象：** 本仓库 Agent 工作流（Bundle **1.3.3**，31 Skills）  
> **外部方案：** [OpenSpec](https://github.com/Fission-AI/OpenSpec) · [GitHub Spec Kit](https://github.com/github/spec-kit) · [Superpowers](https://github.com/obra/superpowers)  
> **图例：** ✅ 强 / 完整 · ⚠️ 部分 / 依赖上下文 · ❌ 弱 / 缺失

---

## 总览对比表


| 维度             | 当前工作流                                          | OpenSpec                        | Spec-Kit                                    | Superpowers                   |
| -------------- | ---------------------------------------------- | ------------------------------- | ------------------------------------------- | ----------------------------- |
| **核心形态**       | Rules + Skills + SDD 文档                        | CLI + `/opsx:`* + Delta Spec    | `specify init` + `/speckit.`*               | 可组合 Skills + 自动触发             |
| **SDD 闭环**     | ✅ spec→analyze→implement→verify→finish→archive | ✅ 最完整（sync / explore / onboard） | ✅ constitution→spec→plan→implement→converge | ⚠️ 偏 plan+TDD，无正式 archive     |
| **领域专精**       | ✅ Vue2/3 中后台（列表/表单/联调/路由）                      | ❌ 与技术栈无关                        | ❌ 与技术栈无关                                    | ❌ 与技术栈无关                      |
| **编码规范深度**     | ✅ 14 条 Rules + 预加载 + 质量红灯                      | ⚠️ 依赖 spec/design，编码细节弱         | ⚠️ constitution 偏原则                         | ⚠️ 强调流程，不规定 Vue 写法            |
| **需求接入**       | ✅ PRD / 语雀 / Figma / Axure / OpenAPI           | ⚠️ 主要靠对话 `/opsx:propose`        | ⚠️ `/speckit.specify` + 模板                  | ⚠️ brainstorming 对话           |
| **实现路径**       | ✅ 新建 / 增量 / 联调 / Bug / 重构 分 Skill              | ✅ `/opsx:apply` 按 tasks         | ✅ `/speckit.implement` 按 tasks              | ✅ subagent + TDD 硬门禁          |
| **验收分层**       | ✅ L1 verify + L2 api-smoke + L3 e2e            | ✅ `/opsx:verify` 三维             | ✅ analyze + converge                        | ✅ 两阶段 review + 测试必过           |
| **CLI / 工具化**  | ⚠️ 本地 `feature-check.py`（未 npm 发行）             | ✅ `openspec` CLI + 状态机          | ✅ `specify init` + 30+ 集成                   | ⚠️ Plugin，无 change 管理 CLI     |
| **多 Agent 移植** | ❌ 绑定 Cursor + 本仓库                              | ✅ 21+ AI 工具 slash               | ✅ 30+ Agent 集成                              | ✅ 多平台 Markdown Skills         |
| **规格增量合并**     | ✅ archive → `docs/specs/` Delta                | ✅ 语义 Delta（ADDED/MODIFIED）      | ✅ spec 库累积                                  | ❌ 无 spec 主库                   |
| **TDD 强制**     | ⚠️ 可选（当前 `testStrategy: pending`）              | ❌ 不强调                           | ⚠️ strict 模式可选                              | ✅ 硬门禁：先测后码                    |
| **子 Agent 编排** | ⚠️ 主 Agent 为主                                  | ⚠️ 单 Agent + CLI 状态             | ⚠️ 单 Agent                                  | ✅ subagent-driven-development |
| **Onboarding** | ✅ `project-bootstrap` + spec-index             | ✅ `/opsx:onboard`               | ✅ `specify init`                            | ⚠️ 通用 quickstart              |
| **协作可见性**      | ⚠️ `docs/features` + Git + board               | ✅ 看板 / 多 change / 可接 Linear     | ⚠️ Git + 工件                                 | ⚠️ git worktree               |


---

## 能力雷达（定性）


| 维度                | 当前这套 | OpenSpec | Spec-Kit | Superpowers |
| ----------------- | ---- | -------- | -------- | ----------- |
| 棕地 Vue 中后台        | ✅✅✅  | ⚠️       | ⚠️       | ⚠️          |
| SDD 规格资产          | ✅✅   | ✅✅✅      | ✅✅       | ❌           |
| 质量门禁硬度            | ✅✅   | ✅✅       | ✅✅✅      | ✅✅✅         |
| 跨工具移植             | ❌    | ✅✅✅      | ✅✅✅      | ✅✅          |
| 执行纪律（TDD/子 Agent） | ⚠️   | ⚠️       | ⚠️       | ✅✅✅         |
| 需求材料接入            | ✅✅✅  | ⚠️       | ⚠️       | ❌           |
| 团队培训 / 话术         | ✅✅✅  | ✅✅       | ✅✅       | ✅           |
| 长期维护成本            | ⚠️   | ✅✅       | ✅✅       | ✅✅          |


---

## 命令 / Skill 映射


| 阶段      | 当前这套                                  | OpenSpec            | Spec-Kit             | Superpowers                      |
| ------- | ------------------------------------- | ------------------- | -------------------- | -------------------------------- |
| 探索 / 澄清 | `spec-research-clarify` + clarify-log | `/opsx:explore`     | `/speckit.clarify`   | `brainstorming`                  |
| 提案      | `【spec】` feature-spec                 | `/opsx:propose`     | `/speckit.specify`   | `writing-plans`                  |
| 写码前分析   | `【analyze】` feature-analyze           | `/opsx:verify`（规划后） | `/speckit.analyze`   | —                                |
| 技术方案    | design.md + feature-dev ②             | design.md（工件内）      | `/speckit.plan`      | plan in skill                    |
| 实现      | `【新建】` feature-dev-workflow           | `/opsx:apply`       | `/speckit.implement` | `subagent-driven-development`    |
| 验收      | `【verify】` + L2/L3                    | `/opsx:verify`      | `/speckit.converge`  | `verification-before-completion` |
| 收尾      | `【finish】` feature-finish             | —                   | —                    | `finishing-a-development-branch` |
| 归档      | `【archive】` feature-archive           | `/opsx:archive`     | spec 库累积             | —                                |
| Bug     | `【bug】` bugfix-workflow               | —                   | —                    | `systematic-debugging`           |
| TDD     | `unit-test-codegen`（pending strict）   | —                   | 模板可选                 | `test-driven-development`        |


---

## 选型建议（一句话）


| 你的情况                             | 建议                                          |
| -------------------------------- | ------------------------------------------- |
| 已在 Vue 中后台深耕、有 PRD/原型/联调         | **继续 当前这套 工作流** ✅                           |
| 要最快跨 Copilot/Cursor/Claude 试 SDD | 叠加 **OpenSpec** 或 **Spec-Kit** 作 change 壳   |
| 要强 TDD + 长任务自主跑                  | 借鉴 **Superpowers** 的 TDD / subagent（不必整体替换） |
| 要对外复制到其他非 Vue 项目                 | **OpenSpec** 作 portable 层 + 自备领域 Rules      |


---

## 本仓库已吸收的外部能力


| 来源          | 已落地                                                |
| ----------- | -------------------------------------------------- |
| OpenSpec    | `feature-check` CLI、Delta archive、`feature-verify` |
| Spec-Kit    | `feature-analyze`、clarify blocker 分级、constitution  |
| Superpowers | bugfix 四阶段、`feature-finish`、TDD pending 预留         |


---

## 可选演进（P2+）


| 优先级 | 借鉴          | 动作                                 |
| --- | ----------- | ---------------------------------- |
| P2  | Spec-Kit    | implement 后 **converge** 式补 tasks  |
| P2  | OpenSpec    | verify 输出 **三维报告**（完整性/正确性/一致性）    |
| P3  | Superpowers | test 基建就绪 → `testStrategy: strict` |
| P3  | Superpowers | 大 feature 可选 subagent 片段           |


---

*更新：2026-07-10 · Bundle 1.3.3 · 详见 [agent-workflow-training.md](./agent-workflow-training.md)*