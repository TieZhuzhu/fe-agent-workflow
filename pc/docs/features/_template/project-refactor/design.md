# Design: 全项目代码规范化重构（PC）

> Feature slug: **project-refactor**

## 页面类型

- [x] 全项目治理（非单页新建）

## 技术约束

| 项 | 本项目 |
|----|--------|
| 框架 | Vue 2 Options API / Vue 3 script setup（按 package.json） |
| 列表 | HiTable + `.list-page` / `.page-panel` |
| 接口 | 页面 `services.js` / `services.ts` |
| 路由 | `vue-router`，**path 不改** |

## 模块优先级与分期

| 阶段 | 模块 | 说明 |
|------|------|------|
| P0 | 基础设施 | App、store、mock 清理 |
| P1 | 核心业务模块 | （填写：product、trade 等） |
| P2 | 设置 / 系统 | |
| P3 | 其余 | |

## Inventory（合规进度）

> 详细表格维护在 **`docs/project-refactor-inventory.md`**（与 tasks.md 阶段同步更新）。

Agent 在 `rules-refactor` ② 阶段创建/更新该文件，design 此处只引用路径与统计摘要。

## 文件清单（按阶段）

（列出各阶段主要改动文件，随 implement 更新）

## 验收与工具

| 阶段结束 | 命令 / Skill |
|----------|----------------|
| 每模块 | `code-normalize` checklist 🔴 |
| 每模块 | spec 场景相关手工冒烟 |
| 全量 | `npm run build` + `npm run lint-fix` |
| 收尾 | `【verify】project-refactor` |
