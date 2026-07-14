# Skills Changelog

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。  
版本规则见 [shared/skills-versioning.md](shared/skills-versioning.md)。

---

## [Bundle 1.3.4] - 2026-07-13

### Kernel（同步 uniapp）

- **rules-refactor** `1.2.0`：全项目重构强制 `project-refactor` SDD 门禁 + verify
- `docs/features/_template/project-refactor/`、`docs/project-refactor-guide.md`
- features/README、checklist-project、manifest `kernelVersion` 1.3.2

---

## [Bundle 1.3.3] - 2026-07-10

### Added

- **skill-creator** `1.0.0`：团队版 Skill 创建/修改/优化流程（对齐 agentskills.io + skill-conventions + manifest 登记）

---

## [Bundle 1.3.2] - 2026-07-10

### Kernel（同步至 pc + uniapp）

- `manifest.json` 新增 `platform`、`kernelVersion` 字段
- 新增 `docs/agent-kernel-sync.md` 跨仓库同步清单
- `shared/skills-versioning.md` 补充内核/平台版本说明

---

## [Bundle 1.3.1] - 2026-07-10

### Changed

- **17 个 Skill**：合并 `## 交付说明` / `## 交付` / `## 交付首行` 与 `## 交付检查` 为单一交付节（**汇报内容** + **门禁**）
- **skill-conventions.md**：规定禁止重复交付章节

---

## [Bundle 1.3.0] - 2026-07-10

### Added

- **shared/skill-conventions.md**：Agent Skills 开放规范对齐（10 条原则、SKILL 结构模板）
- **shared/skill-boundaries-baseline.md**：项目级 ✅⚠️🚫 操作边界基线
- **shared/project-toolbox.md**：feature-check / spec-index / lint-fix 工具箱
- **shared/skill-metadata.yaml** + **scripts/skill-standardize.py**：批量标准化 30 个 Skill
- **scripts/sync-manifest-metadata.py**：manifest description 与 metadata 同步

### Changed

- **全部 30 个 Skill** patch bump：优化 `description`（第三人称 + 触发词）；正文增加管控力度、操作边界、交付检查
- **manifest.json** `bundleVersion` `1.2.0` → `1.3.0`

### Notes

- 对齐 [agentskills.io](https://agentskills.io) 与《前端如何写出优秀的 AI Agent Skills》最佳实践
- `prototype-html-feature-dev`（422 行）仍 ≤500 行阈值，细节保留正文；后续可拆 `references/`

---

## [Bundle 1.2.0] - 2026-07-10

### Added

- **feature-analyze** `1.0.0`：implement 前 artifact 一致性；`feature-check analyze`
- **feature-finish** `1.0.0`：verify PASS 后 PR 收尾清单
- **feature-check.py**：`analyze` / `board` / `sync-status` 子命令
- **spec-index.py**：路由 ↔ spec 缺口索引 `docs/specs/_index.md`
- **status.yaml** 模板与 workflow 状态机

### Changed

- **bugfix-workflow** `1.2.0` → `1.3.0`：四阶段系统化调试（复现→假设→验证→修复）
- **feature-spec** `1.1.0` → `1.2.0`：ready 前须 analyze PASS；clarify blocker 分级
- **feature-archive** `1.0.0` → `1.1.0`：Delta 合并算法为默认
- **project-bootstrap** `1.0.0` → `1.1.0`：集成 spec-index；测试策略 pending
- **constitution**：TDD strict 暂缓（`testStrategy: pending`）

---

## [Bundle 1.1.1] - 2026-07-08

### Changed

- **bugfix-workflow** `1.1.0` → `1.2.0`：Browser MCP 改为优先非强制；不可用/失败时正常降级静态读码与用户证据，不因无 MCP 阻塞排查

### Removed

- **vitest-codegen**：已合并至 `unit-test-codegen`，删除兼容入口目录与 manifest 登记

---

## [Bundle 1.1.0] - 2026-07-08

### Added

- **Skills 版本管理体系**：`manifest.json`、`scripts/skills-version.py`、`shared/skills-versioning.md`
- **prd-markdown-ingest** `1.0.0`：语雀/飞书 Markdown 清洗与 PRD Digest

### Changed

- **bugfix-workflow** `1.0.0` → `1.1.0`：交互类 bug 优先 Browser MCP 实点复现（点击无反应、network、snapshot 对照表）
- **prototype-html-feature-dev** `1.0.0` → `1.1.0`：远程 Axure 导航壳；§F 含 JS 交互原型（curl+JS + Browser MCP P0）
- **feature-dev-workflow** `1.0.0` → `1.1.0`：ingest 路由（语雀、Axure）；交互原型 §F 说明
- **feature-spec** `1.0.0` → `1.1.0`：交互原型 → `research.md` / `e2e.md` 落盘指引
- **prd-feature-dev**：语雀路径指向 `prd-markdown-ingest`
- **README.md** / **前端通用代码规范.mdc**：Skill 路由表更新

### Notes

- 其余 Skill 初始登记为 `1.0.0`（见 [manifest.json](manifest.json)）
---

## [Bundle 1.0.0] - 2026-07-01

### Added

- 初始 Skill 集：workflow / ingest / codegen / integration / quality / maintenance / infra（29 个）
- SDD 路径：feature-spec → feature-dev-workflow → feature-verify → feature-archive
- 验收分层：feature-verify (L1) / api-smoke (L2) / feature-e2e-verify (L3)

---

## Skill 级变更模板（维护时复制）

```markdown
### <skill-name> `<old>` → `<new>`

- 变更摘要
- 影响下游：<dependsOn 消费者>
```
