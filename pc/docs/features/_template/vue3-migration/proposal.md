# Proposal: Vue2 → Vue3 全项目迁移

> Status: **draft** | Feature slug: **vue3-migration**

## 背景

（存量 Vue2 + Options API + Vuex + element-ui / uview2，需升级至 Vue3 技术栈）

## 目标

- 全项目统一 Vue 3 + Composition API（`<script setup lang="ts">`）
- 状态迁移（Vuex → Pinia 或 Vuex 4，按平台约定）
- UI 库升级（PC：Element Plus；uni-app：uview 3 等）
- **业务行为、路由 path、接口 URL 不变**

## 范围

### In Scope

- `package.json` 依赖 major 升级
- 全局基础设施（request、router/pages.json、store、HiTable/列表）
- 按模块迁移 `views/**` 或 `pages/**` + `subPackages/**`
- 全项目 build / vue-tsc（若有）通过

### Out of Scope

- 产品新功能
- 接口字段 / path 变更
- 与本次升级无关的 rules 大重构（可另开 `project-refactor`）

## 成功标准

- [ ] `docs/vue3-migration-inventory.md` 全部 ✅
- [ ] 无 Vue2 Options API 与 Vue3 混用
- [ ] `【verify】vue3-migration` PASS
- [ ] e2e.md P0 冒烟通过

## 风险与回滚

| 项 | 说明 |
|----|------|
| 依赖 major | 记录锁定版本；建议分支 + 分模块 PR |
| 第三方 | Element Plus / uview 3 API 差异 |
| 回滚 | 保留 Vue2 分支直至 verify PASS |
