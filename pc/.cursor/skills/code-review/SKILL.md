---
name: code-review
version: 1.0.1
description: 对 Vue 前端改动做规范审查，只评不改、不自动修复。 用户说 review、检查是否符合规范时触发；rules-refactor 闭环中作审查步骤。
---
# 代码审查

> **管控力度：** 松 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

## 审查范围

用户指定的文件、diff 或目录。

- **Vue 3**：hooks + TS + [reference-checklist](../feature-dev-workflow/reference-checklist.md)；全量审查可用 [code-normalize/checklist.md](../code-normalize/checklist.md)
- **Vue 2**：Options API + `Vue2代码生成指南.mdc` + `reference-checklist` §Vue 2

## 审查维度

### 规范预加载与质量红灯

- [ ] 写码改动应已 Read [rules-activation.md](../shared/rules-activation.md) 对应项
- [ ] 对照 rules-activation §质量红灯（无预加载汇报、Vue 版本混用、组件层级错误等）

### 结构与命名

- [ ] `views/<module>/<page-dir>/` 目录规范
- [ ] `types.ts` 就近放置；**Query/Item/Form 不在 hook/constants/utils/index 内定义**
- [ ] `constants.ts` / `utils.ts` 无 interface/type（见 `TypeScript与types规范.mdc`）
- [ ] 英文命名，无拼音 key

### types.ts（阻塞项，Vue 3）

对照 [TypeScript与types规范.mdc](../../rules/TypeScript与types规范.mdc)：

- [ ] 列表 Query、行 Item、表单 Form 在 `types.ts`
- [ ] hook 无 `export interface` 页面级类型
- [ ] 无裸 `any[]` 业务列表（或 TODO 标注）
- [ ] 多文件共用类型只定义一次，`import type` from `./types`

### Vue 3 写法（vue@3.x 时）

- [ ] `<script setup lang="ts">`
- [ ] 方法 `const handleXxx = () => {}`；composable `export const useXxx = () => {}`；utils/services 全箭头
- [ ] **标准列表页**主逻辑在 `index.vue`；无整页上帝 hook
- [ ] 列表页 HiTable + `el-table-column`
- [ ] 表单/弹窗复杂逻辑在 `hooks/useXxxForm.ts`

### 数据与接口

对照 [接口对接规范.mdc](../../rules/接口对接规范.mdc)：

- [ ] 无 mock 数据
- [ ] loading / empty / error 三态
- [ ] 接口字段有类型；types 与文档一致
- [ ] 无入参 `||` 兜底 / `buildXxxQuery` 仅判空
- [ ] 无 `normalizeRows` 链式猜字段
- [ ] 无自写 `pruneEmpty` / `deepCopy` 等 lodash-es 等价工具

### 可维护性

- [ ] 单文件职责清晰，可拆未拆的标为建议
- [ ] 无 dead code、console.log

## 输出格式

```markdown
## 审查结论
通过 / 需修改

## 必须修改（阻塞）
1. [文件:行] 问题 — 建议
   - **types 未就近** → 迁 `types.ts` 并改 import
   - **constants/utils 含 type** → 迁 `types.ts`
   - **遗留 config 混放** → 拆 constants + utils

## 建议优化（非阻塞）
1. ...

## 已符合的要点
- ...
```

## 与 code-normalize / rules-refactor 区别

| Skill | 侧重 |
|-------|------|
| **code-review** | 只评不改 |
| **code-normalize** | 单页/单模块改码 + checklist 验收 |
| **rules-refactor** | 全项目改码 → review → 修 → 循环至 [checklist-project.md](../rules-refactor/checklist-project.md) 全 🔴 通过；**不中途询问用户** |

- review 阻塞项供 normalize / **rules-refactor** 修复
- **rules-refactor 闭环内**：Agent 按本 Skill 维度自审，有阻塞须**自动继续改**，不得问用户「是否修复」

## 原则

- 只评代码规范与可维护性，不强行改产品逻辑
- 问题要具体、可执行；引用对应 rule（如 `TypeScript与types规范.mdc`、`Vue代码生成指南.mdc`）
- 无问题时明确说「可合并」；有阻塞项时建议用户走 `code-normalize` 修复

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 输出问题清单与严重级别
- 🚫 未经要求直接改代码

## 交付检查

- [ ] 审查报告（BLOCKER/MAJOR/MINOR）
