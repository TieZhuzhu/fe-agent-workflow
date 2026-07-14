# Design: Vue2 → Vue3 迁移（PC）

> Feature slug: **vue3-migration**

## 迁移映射

| 项 | Vue2 | Vue3 目标 |
|----|------|-----------|
| SFC | Options API | `<script setup lang="ts">` |
| 状态 | Vuex | Pinia |
| UI | element-ui | element-plus |
| 列表 | HiTable-vue2 | `.cursor/components/HiTable/` |
| 接口 | services.js | services.ts + types.ts |
| 按钮 | type="text" | link / type="primary" link |

## 阶段

| 阶段 | 内容 |
|------|------|
| P0 | package.json、main.ts、router、Pinia、request |
| P1 | 核心列表模块 views |
| P2 | 表单/详情 |
| P3 | 其余 + 清理 Vuex 残留 |

## Inventory

维护于 **`docs/vue3-migration-inventory.md`**，与 `tasks.md` 同步。

## 模块清单

（按项目填写 views 模块表）
