---
name: code-normalize
version: 1.0.1
description: 按全量 rules 整理单页/单模块代码，不改业务行为。 用户说按规范优化、规范化、整理代码（单页范围）时触发；全项目用 rules-refactor。
---
# 按规范优化现有代码

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **目标：** 目标页面符合 **`.cursor/rules` 中与该页类型相关的全部规范**，**不改变产品行为**。
>
> **验收标准：** [checklist.md](./checklist.md) 全部 🔴 阻塞项 + [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) 可适用项 + [rules-activation §质量红灯](../shared/rules-activation.md)。
>
> **与 page-refactor 区别：** 本 Skill 做**规范合规整理**；单文件过大 → `page-refactor`（可组合）。
>
> **与 rules-refactor 区别：** 本 Skill 仅**单页 / 单模块**。**全项目**须 `【spec】propose project-refactor` + `rules-refactor`，不走本 Skill。
>
> **勿模仿不符合规范的现有代码：** 项目中不符合 rules 的文件**不是**模板；优化时向 rules 靠拢。

---

## 触发场景

- 「按规范优化 XX 页面 / 模块」
- 「整理代码、对齐项目规范」
- 「提取 types、消除 any、改写法」
- review 后「按审查意见改」

**不触发：** 加新功能 → `incremental-feature`；从零新建 → `feature-dev-workflow`；只审查不改 → `code-review`；**全项目重构** → `rules-refactor`

**范围边界：**

| 在本 Skill 内 | 另开 Skill |
|---------------|------------|
| types / constants / utils 归位 | 新增业务字段、新接口 |
| Vue/JS/CSS 写法、命名、alias | 改路由 path、权限产品定义 |
| HiTable、hooks 下沉、去 console | 单文件 >800 行大拆分 |
| loading、三态、submitting 补齐 | 跨模块组件提升到顶层 |
| 单页 / 单模块 | **全项目** → `rules-refactor` |

---

## 流程

```
① 预加载 → ② 判定页面类型 → ③ 全量审计 → ④ 优化清单 → ⑤ 最小改动 → ⑥ 全量验收
```

### ① 规范预加载（强制）

与 [rules-activation](../shared/rules-activation.md) **同等基线**，**不得**只 Read types 规范：

1. Read `shared/rules-activation.md`
2. Read 通用基线：`前端通用代码规范.mdc`、`项目结构与命名规范.mdc`、`TypeScript与types规范.mdc`、`Vue代码生成指南.mdc`（vue@2.x 则 `Vue2代码生成指南.mdc`）
3. **判定页面类型后**，Read rules-activation §按页面类型追加 的全部 rules
4. 若存在 `.cursor/project-conventions.md`，Read 以对齐 **request 路径、布局组件**等扫描项（**规范违背仍按 rules 改**，conventions 不是重构标准）
5. Read 目标页 + 同模块参照页；搜索 `services` 的 request import
6. Read [checklist.md](./checklist.md)
7. **复杂优化必输出** §预加载计划（列明将 Read 的 rules 清单）

### ② 判定页面类型

| 类型 | 判定 |
|------|------|
| 列表页 | 筛选 + 表格 + 分页 |
| 表单页 | 多字段录入 + 提交 |
| 详情页 | 只读信息分组 |
| 组合页 | 列表 + 弹窗编辑 |
| 复杂页 | 多区块 / Tab / 工作台 |

类型决定 ③ 审计章节（checklist §通用 + §页面类型）。

### ③ 全量审计

按 [checklist.md](./checklist.md) 逐项检查，**必须输出**「规范审计」块（含 🔴 阻塞 / 🟡 建议 / ⚪ 不改）。

**不得**只审计 types 而跳过 Vue 写法、HiTable、hooks、样式、状态等维度。

### ④ 优化清单（改码前）

在审计基础上列出本轮将修复的 **全部 🔴 项**；🟡 项说明修或不修及原因。

```markdown
## 规范优化清单
### 结构 / types
- [ ] ...
### Vue / JS 写法
- [ ] script setup；**全箭头函数**（含 composable、utils、services）；禁止 `function` 声明
- [ ] services 箭头导出
### 列表 / 表单（按页面类型）
- [ ] HiTable；逻辑进 useXxxList
### 代码质量
- [ ] 移除 console.log；补 loading
### 接口对接
- [ ] 入参无兜底；出参无 normalize 猜字段（见 `接口对接规范.mdc`）
### 不改
- 接口 URL、路由 path、交互文案
```

**先清单后改码**；未在清单中的文件不扩大改动。

### ⑤ 最小改动

1. **types 优先** → 再 constants / utils / hooks / template
2. **行为不变** — 不改 API 语义、路由、产品文案
3. **对齐同模块参照页** — HiTable、services 路径、样式引入
4. **一次聚焦** — 单页或单模块；大拆分交给 `page-refactor`

### ⑥ 全量验收（强制）

1. 执行 [lint-check](../lint-check/SKILL.md) — `npm run lint-fix` 零 error
2. 复跑 [checklist.md](./checklist.md)，全部 🔴 打勾
3. 对照 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) 可适用项
4. 过 [rules-activation §质量红灯](../shared/rules-activation.md)
5. 仍有 🟡 未修 → 交付「建议后续」列表，**不得**称「已全部符合规范」

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 命名、types、services 归位
- 🚫 改接口字段语义或交互行为

## 交付检查

**汇报内容**

1. **规范预加载**一行（含页面类型、已 Read rules 数量）
2. **规范审计**摘要（阻塞 N / 建议 M）
3. **类型迁移表**（若有 types 变动）
4. **修改文件列表** + 每项对应修复的规范点
5. **验收结果** — checklist 🔴 全部通过 / 未通过项
6. 手动验证步骤

**交付首行示例：**

```
规范预加载：Vue 3 | 列表页 | code-normalize | 已读 rules ×8 | checklist 阻塞项 0
```

**门禁**

- [ ] `lint-fix` + 行为不变说明
- [ ] 上文 §⑥ 全量验收步骤已执行

## 禁止

- 只改 types/格式，跳过 HiTable、hooks、写法、质量项却称「已优化」
- 未 Read 页面类型 rules 就改码
- 优化时加新需求（走 `incremental-feature`）
- 验收仅过 `TypeScript与types规范` 而不过全量 checklist
- 新建混放 options 与工具函数的文件
- 以项目中不符合规范的代码为模板
