# Proposal: 全项目代码规范化重构

> Status: **draft** | Feature slug: **project-refactor**

## 背景

（简述存量问题：命名混乱、列表实现不统一、mock 残留、与 `.cursor/rules` 差距等）

## 目标

- 全部业务代码符合 `.cursor/rules`
- 业务行为与现网一致（用户无感知）
- 分阶段可 review、可冒烟、可回滚

## 范围

### In Scope

- 基础设施（App、store、request、死代码）
- 按模块分批 `rules-refactor` / `code-normalize`
- 列表/表单/详情规范对齐（PC：HiTable + tablePage.scss）
- lint / build 通过

### Out of Scope

- 升级 Vue 3 / Element Plus（除非单独立项）
- 修改路由 path、接口 URL、产品文案
- 新增业务功能
- 一次性 Big Bang 全量 PR

## 成功标准

- [ ] `docs/project-refactor-inventory.md`（或 design §inventory）全部模块 ✅
- [ ] [checklist-project.md](../../../../.cursor/skills/rules-refactor/checklist-project.md) 🔴 = 0
- [ ] `【verify】project-refactor` PASS
- [ ] `tasks.md` 全部 [x] 或标注 skip 理由
- [ ] 手工冒烟：spec.md 场景 1–N 通过

## 依赖与风险

| 项 | 说明 |
|----|------|
| 接口 | 不改契约；field-map N/A |
| 菜单/路由 | path 不变 |
| 风险 | 大范围 diff → **必须分模块 PR + 每阶段冒烟** |

## 关联

- 约定：`.cursor/project-conventions.md`
- 规范：`.cursor/rules/`
- 流程：`rules-refactor` / `feature-verify`
