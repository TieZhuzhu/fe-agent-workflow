# Skills 版本管理

> **权威源：** [manifest.json](../manifest.json)  
> **变更记录：** [CHANGELOG.md](../CHANGELOG.md)  
> **校验脚本：** [scripts/skills-version.py](../scripts/skills-version.py)

---

## 版本号规则（SemVer）

每个 Skill 独立版本：`MAJOR.MINOR.PATCH`

|  bump  | 何时使用 | 示例 |
|--------|----------|------|
| **MAJOR** | 流程断裂、输出格式不兼容、Skill 职责重命名/合并 | 删除阶段、改 mandatory 门禁 |
| **MINOR** | 新增章节、新能力、新子流程、扩展路由表 | prototype §F 交互原型 |
| **PATCH** | 文案修正、错别字、示例更新、无行为变化 | 修正 curl 示例 URL |

**Bundle 版本**（`manifest.json` → `bundleVersion`）：任意 Skill **MINOR+** 变更时同步 bump；仅 PATCH 时可不变。

**内核版本**（`manifest.json` → `kernelVersion`）：跨 PC / uni-app 共享的 SDD 与门禁逻辑版本；两仓库**应保持一致**。仅平台专属改动时不 bump。

**平台标识**（`manifest.json` → `platform`）：`pc` | `uniapp`，标识壳层，**不可**跨仓库复制。

同步清单见 [docs/agent-kernel-sync.md](../../../docs/agent-kernel-sync.md)。

---

## 目录与字段

### manifest.json（唯一权威）

```json
{
  "schemaVersion": 1,
  "platform": "pc",
  "kernelVersion": "1.3.1",
  "bundleVersion": "1.3.1",
  "updatedAt": "2026-07-10",
  "skills": [ ... ]
}
```

| 字段 | 说明 |
|------|------|
| `platform` | `pc` \| `uniapp`；本仓库平台壳层 |
| `kernelVersion` | 共享内核版本，与对端仓库对齐 |
| `bundleVersion` | 本仓库整体发布版本（可 ≥ kernelVersion） |
| `schemaVersion` | manifest 结构版本 |
| `updatedAt` | 最后更新日期 |

**skills[] 每项：**

| 字段 | 说明 |
|------|------|
| `name` | 与 `SKILL.md` frontmatter `name` 一致 |
| `version` | SemVer |
| `category` | `workflow` / `ingest` / `codegen` / `integration` / `quality` / `maintenance` / `infra` |
| `status` | `stable` / `experimental` / `deprecated` |
| `description` | **简短中文说明**（manifest 索引用，一行概括用途） |
| `dependsOn` | 编排依赖（文档用，非运行时加载） |
| `note` | 可选，deprecated 说明 |

`description` 与 `SKILL.md` frontmatter 的 `description`（英文触发句）**分工不同**：manifest 用中文便于维护索引；改 Skill 职责时同步更新 manifest 中文描述。

### SKILL.md frontmatter

须与 manifest **同步**（由脚本写入）：

```yaml
---
name: feature-dev-workflow
version: 1.1.0
description: ...
---
```

Agent **不依赖** frontmatter 版本做路由；版本供人读与 CHANGELOG 追溯。

---

## 日常维护流程

### 1. 修改 Skill 内容

编辑 `SKILL.md`（及 reference/checklist 等）。

### 2. Bump 版本

```bash
# 从 .cursor/skills 目录执行
python3 scripts/skills-version.py bump prototype-html-feature-dev minor "§F 交互原型 curl+MCP"
```

或手动改 `manifest.json` 中对应 `version`。

### 3. 同步 frontmatter

```bash
python3 scripts/skills-version.py sync
```

### 4. 写 CHANGELOG

在 [CHANGELOG.md](../CHANGELOG.md) 对应 Bundle 或 Skill 条目下追加说明。

### 5. 校验（提交前）

```bash
python3 scripts/skills-version.py check
python3 scripts/skills-version.py list --category ingest
```

`check` 失败时：**不得**标记维护完成。

---

## 分类一览

| category | 用途 | Skills |
|----------|------|--------|
| **workflow** | SDD 主路径、验收、增量 | feature-dev-workflow, feature-spec, feature-verify, … |
| **ingest** | PRD / 原型 / Figma 材料接入 | prd-markdown-ingest, prototype-html-feature-dev, … |
| **codegen** | 页面代码生成 | vue-page-codegen |
| **integration** | 接口联调 | api-integration, openapi-api-integration |
| **quality** | 审查、CI、探针、单测 | code-review, api-smoke, ci-fix, … |
| **maintenance** | 重构、规范化、Bug | code-normalize, rules-refactor, bugfix-workflow, … |
| **infra** | 项目约定、路由、公共组件、Skill 维护 | project-bootstrap, route-permission, shared-component, skill-creator |

---

## 依赖关系（维护提示）

修改 **上游 Skill** 时，检查 `dependsOn` 含它的下游是否需要 MINOR bump 或文档交叉引用更新：

```
feature-spec
  └── feature-dev-workflow
        ├── prd-markdown-ingest → prd-feature-dev
        ├── prototype-html-feature-dev
        ├── figma-feature-dev
        └── vue-page-codegen → feature-verify → feature-archive
                                      └── feature-e2e-verify / api-smoke
```

**ingest 类**变更（如 prototype §F）→ 同步检查 `feature-dev-workflow`、`feature-spec` 路由表是否已引用。

---

## 新增 Skill checklist

> **推荐：** 走 [skill-creator](../skill-creator/SKILL.md) 完整流程。

1. 创建 `<name>/SKILL.md`（或 `@skill-creator` 生成）
2. 在 `manifest.json` 追加条目（从 `1.0.0` 起）
3. 在 `shared/skill-metadata.yaml` 追加条目
4. `python3 scripts/skills-version.py sync`
5. `python3 scripts/skill-standardize.py --skill <name>`（可选）
6. 更新 [README.md](../README.md) 路由表 + `.cursor/rules/前端通用代码规范.mdc`
7. [CHANGELOG.md](../CHANGELOG.md) 记 Added
8. 若属 ingest/workflow，更新 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 输入识别表
9. `python3 scripts/skills-version.py check`

---

## 废弃 Skill

1. `manifest.json` → `"status": "deprecated"` + `note`
2. frontmatter 可加 `deprecated: true`（sync 不自动加，手改）
3. README 路由表移到「已废弃」或标注替代 Skill
4. CHANGELOG 记 Deprecated
