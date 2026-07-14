# Spec: Vue2 → Vue3 全项目迁移

> Feature slug: **vue3-migration**

## 用户故事

- 作为**维护者**，我希望项目运行在 Vue3 技术栈，便于后续开发与生态支持。
- 作为**用户**，我希望升级后功能与现网一致。

## 技术需求（迁移 FR）

| ID | 需求 | 优先级 |
|----|------|--------|
| FR-1 | 依赖升级至 Vue3 + 配套 UI/状态库 | P0 |
| FR-2 | 无 Options API 残留（业务 SFC） | P0 |
| FR-3 | 页面 `types.ts` + `services.ts` | P1 |
| FR-4 | 列表页 HiTable（Vue3 版）或等价实现 | P1 |
| FR-5 | Pinia store 符合约定 | P0 |
| FR-6 | build + vue-tsc 通过 | P0 |

## 验收场景（业务回归 — 必填）

### 场景 1：登录与菜单

- **Given** 有效账号
- **When** 登录 → 打开核心菜单页
- **Then** 与 Vue2 版本行为一致，无白屏

### 场景 2：核心列表

- **When** 列表筛选、分页
- **Then** 数据正确，HiTable/列表组件正常

### 场景 3：表单提交

- **When** 完成一单典型表单/下单流程
- **Then** 提交成功路径与升级前一致

### 场景 4：构建

- **When** `pnpm build` / `vue-tsc`
- **Then** 通过

## 非功能

- 禁止同文件 Vue2/Vue3 混用
- 禁止改接口契约
