# Tasks: <功能名>

> 实现时逐项勾选 `- [x]`。`feature-verify` 须全部完成或标注跳过理由。

## 0. Spec

- [ ] proposal.md / spec.md / design.md 已评审
- [ ] `[待确认]` 已清零或已写入 spec 决策

## 1. 脚手架

- [ ] 创建 `views/<module>/<page-dir>/`（与 path 一致）
- [ ] `types.ts` / `constants.ts` / `services.ts`
- [ ] 模块 `routes.ts` 注册（见 `.cursor/skills/route-permission/SKILL.md`）

## 2. UI 与逻辑

- [ ] 布局与筛选区
- [ ] 表格 / 表单 / 详情区
- [ ] hooks 与事件处理
- [ ] 弹窗子组件（若有）

## 3. 接口

- [ ] services 对接
- [ ] field-map.md 与 types 一致
- [ ] loading / empty / error

## 4. 验收

- [ ] reference-checklist 相关项
- [ ] `pnpm test`（若有）
- [ ] `pnpm build`
- [ ] feature-verify 通过

## 5. 交付

- [ ] 待后端配置菜单 path 已列出
- [ ] PR / 交付说明
