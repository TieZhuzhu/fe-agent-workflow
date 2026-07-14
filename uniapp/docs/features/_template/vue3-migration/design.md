# Design: Vue2 → Vue3 迁移（uni-app）

## 迁移映射

| 项 | Vue2 | Vue3 |
|----|------|------|
| SFC | Options API | script setup + TS |
| 生命周期 | 选项式 onLoad | `onLoad` from `@dcloudio/uni-app` |
| 状态 | Vuex 3 | Pinia / Vuex 4 |
| UI | uview-ui 2 | uview-plus 等 |
| 接口 | services.js | services.ts |

## 架构注意

- 自定义 tabBar 嵌入页：迁移时保持主包策略，design 记录决策
- `getApp()` / `Vue.prototype` → provide/inject 或 store

## Inventory

**`docs/vue3-migration-inventory.md`**

## 阶段

P0 依赖/App → P1 product/order → P2 user/其余 → P3 components
