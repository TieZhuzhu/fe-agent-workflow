# Spec: 全项目代码规范化重构

> Feature slug: **project-refactor**

## 用户故事

- 作为**前端维护者**，我希望存量 uni-app 代码符合统一规范。
- 作为**商城用户**，我希望重构后下单、购物车、登录等主流程与现网一致。

## 功能需求（重构类 FR）

| ID | 需求 | 优先级 |
|----|------|--------|
| FR-1 | 清理 dead code、业务 console.log | P0 |
| FR-2 | pages.json path 与磁盘文件一致 | P0 |
| FR-3 | 组件 PascalCase 目录 + index.vue | P1 |
| FR-4 | 接口组织符合 conventions，入参透传、出参直绑 | P1 |
| FR-5 | lint 零 error（有 script 时） | P0 |
| FR-6 | 分阶段模块冒烟无功能退化 | P0 |

## 验收场景（业务回归 — 必填）

### 场景 1：首页与 tab / 主导航

- **Given** 已登录或未登录（按场景）
- **When** 打开首页，切换 tab（或自定义 tabBar 各入口）
- **Then** 各 tab 内容正常，无白屏与控制台报错

### 场景 2：商品 → 购物车 → 下单

- **Given** 有效商品
- **When** 搜索/进入详情 → 加购 → 购物车 → 提交订单入口
- **Then** 与重构前行为一致

### 场景 3：订单与售后

- **Given** 有历史订单
- **When** 订单列表 → 详情 → 退款/物流等操作入口
- **Then** 页面与操作正常

### 场景 4：登录

- **When** 登录页 / login-popup 完成登录
- **Then** token 生效，个人中心数据刷新

### 场景 5：静态检查

- **When** `npm run lint-fix`（若有）
- **Then** 零 error

> 补充路径见 `e2e.md`（H5 / 微信小程序分别列出）。

## 非功能

- **行为不变**：pages.json path、接口 URL、文案不变
- **原生组件优先**，uview 补充
- **禁止 mock**

## 模块优先级

（与 design.md、inventory 一致）

## 决策记录

| 日期 | 决策 | 理由 |
|------|------|------|
| | 自定义 tabBar 页保留主包 | 嵌入 index 架构，不迁分包 |
