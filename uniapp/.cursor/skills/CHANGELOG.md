# Skills Changelog

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。  
版本规则见 [shared/skills-versioning.md](shared/skills-versioning.md)。

---

## [Bundle 1.3.4] - 2026-07-13

### Kernel（同步 pc + uniapp）

- **rules-refactor** `1.2.0`：全项目重构强制 `project-refactor` SDD 门禁
- **vue2-to-vue3-refactor** `1.2.0`：强制 `vue3-migration` SDD 门禁（与 project-refactor 互斥）
- 新增 `docs/features/_template/project-refactor/`、`vue3-migration/` 模板
- 新增 `docs/project-refactor-guide.md`、`docs/vue3-migration-guide.md`
- **features/README.md**：区分单页 code-normalize（可省略 spec）vs 全项目 rules-refactor（不可省略）
- **checklist-project**、**inventory-template**、**skill-when-to-use**、**manifest** 同步

---

## [Bundle 1.3.3] - 2026-07-10

### Kernel（同步自 pc）

- **skill-creator** `1.0.0`：团队版 Skill 创建/修改/优化流程
- **skill-metadata.yaml**、**skill-when-to-use.yaml**：skill-standardize / 跨 Host 导出元数据
- **export-agent-host.py**、**mcp-host-adapter.yaml**、**host-rules-manifest.yaml**（uni-app rules 清单）
- **docs/agent-workflow-roadmap.md**

### Platform (uniapp)

- `host-rules-manifest.yaml` 适配 11 条 uni-app rules（含 `uniapp代码生成指南`、`路由与分包规范`）

---

## [Bundle 1.3.2] - 2026-07-10

### Kernel（同步至 pc + uniapp）

- `manifest.json` 新增 `platform`、`kernelVersion` 字段
- 新增 `docs/agent-kernel-sync.md` 跨仓库同步清单
- `shared/skills-versioning.md` 补充内核/平台版本说明

---

## [Bundle 1.3.1] - 2026-07-10

### Changed

- **17 个 Skill**：合并 `## 交付说明` / `## 交付` 与 `## 交付检查` 为单一交付节（**汇报内容** + **门禁**）
- **skill-conventions.md**：规定禁止重复交付章节
- 同步自 PC 中后台 Bundle 1.3.1，适配 uni-app（pages.json / subPackages / 无 HiTable）

---

## [Bundle 1.3.0] - 2026-07-10

### Added

- **shared/skill-conventions.md**：Agent Skills 开放规范对齐
- **shared/skill-boundaries-baseline.md**：uni-app 项目级 ✅⚠️🚫 操作边界
- **shared/project-toolbox.md**：feature-check / spec-index 工具箱
- **scripts/skill-standardize.py**、**scripts/sync-manifest-metadata.py**

### Changed

- **全部 30 个 Skill** patch bump：优化 description；正文增加管控力度、操作边界、交付检查
- **manifest.json** `bundleVersion` `1.2.0` → `1.3.0`

---

## [Bundle 1.2.0] - 2026-07-10

### Added

- **feature-analyze** `1.0.0`：implement 前 artifact 一致性；`feature-check analyze`
- **feature-finish** `1.0.0`：verify PASS 后 PR 收尾清单
- **feature-check.py**（uni-app 版）：`analyze` / `board` / `sync-status` 子命令
- **spec-index.py**（uni-app 版）：解析 `pages.json` → `docs/specs/_index.md`
- **status.yaml** / **clarify-log.md** 模板与 workflow 状态机

### Changed

- **bugfix-workflow** `1.0.0` → `1.3.1`：四阶段系统化调试（复现→假设→验证→修复）
- **feature-spec** `1.0.0` → `1.2.1`：ready 前须 analyze PASS；clarify blocker 分级
- **feature-archive** `1.0.0` → `1.1.1`：Delta 合并算法为默认
- **project-bootstrap** `1.0.0` → `1.1.1`：集成 spec-index；测试策略 pending
- **constitution**：`testStrategy: pending`（无 test script 时）

---

## [Bundle 1.1.0] - 2026-07-08

### Added

- **Skills 版本管理体系**：`manifest.json`、`scripts/skills-version.py`、`shared/skills-versioning.md`
- **prd-markdown-ingest** `1.0.0`：语雀/飞书 Markdown 清洗与 PRD Digest

### Changed

- **bugfix-workflow** `1.0.0` → `1.1.0`：Browser MCP 优先非强制
- **prototype-html-feature-dev** `1.0.0` → `1.1.0`：远程 Axure；§F 交互原型
- **feature-dev-workflow** `1.0.0` → `1.1.0`：ingest 路由
- **feature-spec** `1.0.0` → `1.1.0`：交互原型 → e2e.md 落盘指引

---

## [Bundle 1.0.0] - 2026-07-08

### Added

- uni-app 专用 rules：`uniapp代码生成指南`、`路由与分包规范` 等
- SDD 流程（feature-spec → dev → verify → archive）
- 28 个 Skills（workflow / ingest / codegen / integration / quality / maintenance / infra）

### Notes

- 仅适用于 uni-app 移动端，不含 PC 中后台
- 接口组织以 `project-conventions.md`（bootstrap）为准
- Vue 2 / Vue 3 按项目判定，禁止混用
- UI：原生组件 + uview-ui 补充

---

## Skill 级变更模板（维护时复制）

```markdown
### <skill-name> `<old>` → `<new>`

- 变更摘要
- 影响下游：<dependsOn 消费者>
```
