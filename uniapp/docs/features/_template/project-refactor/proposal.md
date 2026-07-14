# Proposal: 全项目代码规范化重构

> Status: **draft** | Feature slug: **project-refactor**

## 背景

（简述存量问题：分包、命名、service 组织、与 `.cursor/rules` 差距等）

## 目标

- 全部业务代码符合 `.cursor/rules`
- 业务行为与现网一致（用户无感知）
- 分阶段可 review、可冒烟、可回滚

## 范围

### In Scope

- 基础设施（App、store、request、pages.json 对齐）
- 按模块分批 `rules-refactor`
- 列表/表单/详情规范对齐（原生组件 + uview 补充）
- lint / build（按项目能力）

### Out of Scope

- 升级 Vue 3（除非单独立项 `vue2-to-vue3-refactor`）
- 修改 pages.json path、接口 URL、产品文案
- 新增业务功能
- 为单页随意新建 subPackage

## 成功标准

- [ ] `docs/project-refactor-inventory.md` 全部模块 ✅
- [ ] `checklist-project.md` 🔴 = 0
- [ ] `【verify】project-refactor` PASS
- [ ] `tasks.md` 全部 [x]
- [ ] 手工冒烟：spec.md + e2e.md P0 通过

## 依赖与风险

| 项 | 说明 |
|----|------|
| 接口 | 不改契约；field-map N/A |
| 自定义 tabBar | 若存在嵌入 tab 页，须在 design 记录架构决策 |
| 风险 | HBuilderX 工程可能无 npm build → e2e 权重更高 |

## 关联

- 约定：`.cursor/project-conventions.md`
- 规范：`.cursor/rules/`
- 流程：`rules-refactor` / `feature-verify`
