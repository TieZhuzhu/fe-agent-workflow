# Proposal: Vue2 → Vue3 全项目迁移（uni-app）

> Status: **draft** | Feature slug: **vue3-migration**

## 背景

（uni-app Vue2 + Options API + Vuex + uview-ui 2.x，需升级 Vue3）

## 目标

- 全项目 `<script setup lang="ts">` + Composition API
- Vuex → Pinia 或 Vuex 4（按 uni-app 官方与项目约定）
- uview-ui 2 → uview-plus / uview 3（按项目选型）
- **pages.json path、接口、业务行为不变**

## 范围

### In Scope

- manifest / package 依赖升级
- main.js → main.ts、App.vue 迁移
- pages + subPackages 按模块迁移
- H5 + 微信小程序冒烟（e2e.md）

### Out of Scope

- 新功能、改 path/接口
- 同版本 rules 整理（另开 `project-refactor`）

## 成功标准

- [ ] `docs/vue3-migration-inventory.md` 全部 ✅
- [ ] 无 Vue2/Vue3 混用
- [ ] `【verify】vue3-migration` PASS

## 风险

| 项 | 说明 |
|----|------|
| 小程序 | 须微信开发者工具实机验证 |
| 自定义 tabBar | 嵌入页迁移须单独冒烟 |
| 条件编译 | `#ifdef` 块保持，逐端验证 |
