# Spec: Vue2 → Vue3 迁移（uni-app）

> Feature slug: **vue3-migration**

## 技术需求

| ID | 需求 | 优先级 |
|----|------|--------|
| FR-1 | Vue3 + uni-app 编译通过 | P0 |
| FR-2 | 生命周期：`onLoad`/`onShow` 从 `@dcloudio/uni-app` | P0 |
| FR-3 | 无 Options API 残留 | P0 |
| FR-4 | Pinia / Vuex4 全局状态 | P0 |
| FR-5 | uview 升级或替换方案落地 | P1 |

## 验收场景

### 场景 1：首页 tab / 主导航

- **When** 切换各 tab（含自定义 tabBar 嵌入页）
- **Then** 正常，无白屏

### 场景 2：交易主路径

- 商品 → 加购 → 购物车 → 订单入口

### 场景 3：登录

- login / login-popup 正常

### 场景 4：多端

- H5 与微信小程序各跑 e2e.md P0

## 非功能

- path、接口不变；禁止混用写法
