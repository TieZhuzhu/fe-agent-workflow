# Design: 全项目代码规范化重构（uni-app）

> Feature slug: **project-refactor**

## 页面类型

- [x] 全项目治理（非单页新建）

## 技术约束

| 项 | 本项目 |
|----|--------|
| 框架 | Vue 2 Options API / Vue 3 script setup（按 package.json） |
| 路由 | `pages.json` + subPackages，**path 不改** |
| 列表 | 原生 scroll-view / 下拉刷新 / onReachBottom |
| 接口 | 页面级或集中式（以 `project-conventions.md` 为准） |
| UI | 原生优先，uview 补充 |

## 架构决策（必填）

### 自定义 tabBar（若适用）

若 `pages/index` 嵌入 cart/category 等作为 tab 内容：

- 这些页面**保留主包**，视为 tabBar 类页面
- 在 inventory 标注「tab 嵌入」，不强制迁 subPackages

## 模块优先级与分期

| 阶段 | 模块 | 说明 |
|------|------|------|
| P0 | 基础设施 | App、pages.json、request、login |
| P1 | product / order / cart | 交易主路径 |
| P2 | user / coupon / address | |
| P3 | 其余 subPackages + components | |

## Inventory（合规进度）

> 详细表格：**`docs/project-refactor-inventory.md`**（rules-refactor ② 创建并持续更新）。

## 文件清单（按阶段）

（随 implement 更新）

## 验收与工具

| 阶段结束 | 命令 / Skill |
|----------|----------------|
| 每模块 | `code-normalize` checklist 🔴 |
| 每模块 | e2e.md P0 相关路径冒烟 |
| 全量 | lint（build 按项目 skip 须注明） |
| 收尾 | `【verify】project-refactor` |
