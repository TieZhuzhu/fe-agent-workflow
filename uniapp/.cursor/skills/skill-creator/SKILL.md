---
name: skill-creator
version: 1.0.0
description: 按团队规范创建、修改或优化 Cursor Agent Skill（SKILL.md、manifest、触发词）。用户说新建 skill、创建 skill、优化 skill description、把这段流程做成 skill、skill-creator 时触发。维护现有业务 Skill 见 skill-conventions，不写 Vue 业务代码。
---
# Skill Creator（团队版）

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

借鉴 [anthropics/skills skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) 与 [agentskills.io](https://agentskills.io/specification)，对齐本仓库 **30+ Skill 编排体系**。

## 何时使用

- 用户要把**工作流 / 团队约定**沉淀为新 Skill
- 修改已有 Skill 的 description、边界、流程
- 拆分过长 SKILL.md（>500 行）到 `references/`
- 新增 Skill 后登记 manifest / README / CHANGELOG

## 何时不用

| 用户意图 | 改用 |
|----------|------|
| 写 Vue 页面 / 联调 / Bug | 对应业务 Skill（`feature-dev-workflow` 等） |
| 改 `.cursor/rules/*.mdc` 编码规范 | 直接改 rules，**不**新建 Skill |
| 仅问 Agent Skills 概念、不写文件 | 直接回答，不必走本 Skill |

---

## 流程

按以下顺序执行，不要跳步：

### ① 捕获意图（Discovery）

从对话或用户描述提取：

1. **做什么** — Skill 能力一句话
2. **何时触发** — 场景词、用户原话（写入 description）
3. **管控力度** — 严 / 中 / 松（见 skill-conventions）
4. **与现有 Skill 关系** — 是否重复？应 `dependsOn` 谁？

**必读：** [README.md](../README.md) 路由表 + [manifest.json](../manifest.json)，避免与已有 30 个 Skill 职责重叠。

一次问 1～3 个关键问题（若缺失）：

- 新 Skill 名（kebab-case，与目录名一致）
- category（workflow / ingest / codegen / integration / quality / maintenance / **infra**）
- 是否需 `scripts/` 或 `references/`

### ② 设计（Design）

1. 选定 **name**（小写、连字符、≤64 字符、与目录同名）
2. 起草 **description**（第三人称 + 能力 + WHEN + 触发词，≤1024 字符）
3. 列出正文章节：何时使用 → 流程（编号）→ 操作边界 → 交付检查 → 禁止
4. 判定是否拆 `references/`（正文预计 >400 行时提前拆）

**脚手架：** [references/skill-template.md](references/skill-template.md)

**description 示例：**

```yaml
# ✅
description: 对 OpenAPI spec 生成 types 与 services 并联调页面绑定。用户说 OpenAPI、Swagger、openapi.json 时触发；有 spec 时优先于 api-integration。

# ❌ 太模糊
description: Helps with skills.
```

### ③ 实现（Implement）

1. 创建 `.cursor/skills/<name>/SKILL.md`（frontmatter + 正文）
2. 可选：`references/`、`scripts/`（确定性操作用脚本，见 project-toolbox）
3. 在 [manifest.json](../manifest.json) 追加条目（`version: 1.0.0`）
4. 在 [shared/skill-metadata.yaml](../shared/skill-metadata.yaml) 追加 metadata（供 skill-standardize 同步）
5. 更新 [README.md](../README.md) §Skill 自动路由
6. 若影响主工作流 → 更新 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 输入识别表（如 ingest/workflow 类）
7. 若需全局路由 → 更新 `.cursor/rules/前端通用代码规范.mdc` §Skill 路由

**同步命令：**

```bash
python3 .cursor/skills/scripts/skills-version.py sync
python3 .cursor/skills/scripts/skill-standardize.py --skill <name>
python3 .cursor/skills/scripts/skills-version.py check
```

### ④ 验证（Validate）

**规范校验：**

| 检查项 | 方式 |
|--------|------|
| name 与目录一致 | `skills-version.py check` |
| description 长度与触发词 | 人工 + skill-metadata |
| 正文 ≤500 行 | `wc -l SKILL.md` |
| 单一 `## 交付检查` | 无重复「交付说明」节 |
| 引用仅一层深 | 无 references 套 references |

**触发测试（至少 3 条）：**

| 类型 | 示例 |
|------|------|
| 应触发 | 用户原话 + 期望选用 `<name>` |
| 不应触发 | 相近意图应走其他 Skill |
| 边界 | 用户只说概念、不要求写 Skill → 不创建文件 |

用户确认 description 是否「够主动」—— 略写全触发场景，减少 undertrigger（参考 Anthropic skill-creator 建议）。

### ⑤ 发布（Release）

1. [CHANGELOG.md](../CHANGELOG.md) 记 **Added** `<name> 1.0.0`
2. bump `manifest.json` → `bundleVersion`（新 Skill = MINOR）
3. `python3 .cursor/skills/scripts/skills-version.py check`

---

## 修改已有 Skill

1. 判断 bump 级别：PATCH 文案 / MINOR 新章节流程 / MAJOR 职责变更
2. `python3 scripts/skills-version.py bump <name> <patch|minor|major> "说明"`
3. 改 `SKILL.md`；若改 description → 同步 `skill-metadata.yaml` → `skill-standardize.py`
4. CHANGELOG + check

---

## 与 Rules 分工（勿重复）

| 内容 | 放哪 |
|------|------|
| Vue 怎么写、types 规范 | `.cursor/rules/*.mdc` |
| 什么时候做什么、步骤、边界 | Skill `SKILL.md` |
| Skill 怎么写 | `shared/skill-conventions.md` + **本 Skill** |

**只写 Agent 不知道的：** 团队 request 路径、SDD 链路、feature-check 门禁 —— 不教 Vue 基础语法。

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 创建/修改 `.cursor/skills/`、`manifest.json`、README、CHANGELOG
- ✅ 更新 `skill-metadata.yaml` 与 skill-conventions 交叉引用
- ⚠️ 改 `feature-dev-workflow` 路由表前先确认 category 与 dependsOn
- 🚫 把 Vue 业务规范塞进 Skill（应放 rules）
- 🚫 未跑 `skills-version.py check` 即声称 Skill 已发布
- 🚫 创建与现有 Skill 职责 80% 重叠的新 Skill（应扩展已有 Skill）

## 交付检查

**汇报内容**

1. Skill 名、category、管控力度、dependsOn
2. 新建/修改文件列表
3. description 全文 + 3 条触发测试话术结果
4. `skills-version.py check` 结果

**门禁**

- [ ] `skills-version.py check` PASS
- [ ] SKILL.md ≤500 行
- [ ] README 路由表已更新
- [ ] CHANGELOG 已记 Added/Changed

## 禁止

- 在 `~/.cursor/skills-cursor/` 写 Skill（Cursor 内置目录）
- 个人全局 Skill 与项目 Skill 混放（本项目 Skill 只在 `.cursor/skills/`）
- description 用第一人称（「我可以帮你…」）
- 无 frontmatter `name` / `description`
