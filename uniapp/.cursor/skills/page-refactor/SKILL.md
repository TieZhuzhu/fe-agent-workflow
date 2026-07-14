---
name: page-refactor
version: 1.0.1
description: 拆分过大 Vue 页面、提取页面子组件/hooks、消除重复逻辑。用户说「拆分这个页面」「文件太大了」时触发。跨模块公共组件见 shared-component。
---
# 页面拆分与重构

## 何时拆分

满足任一即拆（不必等 800 行建议上限）：

- 多个独立 UI 区块可组件化
- 表单/列表逻辑混杂难以阅读
- 同逻辑可在其他页面复用
- 单 hook 承担多个数据域

## 拆分策略（Vue 3）

```
subPackages/<module>/<page>/
├── index.vue              # 仅布局与事件编排
├── mixins/                # Vue 2 可选
│   └── listMixin.js
└── components/
    ├── FilterBar/
    └── EditPopup/
```

| 原位置 | 拆到哪 |
|--------|--------|
| 筛选区 template + 状态 | `components/FilterForm` 或 `useFilters` |
| 列表项 + 列表请求 | 保留列表 template 在 index，逻辑进 `listMixin` / `methods` |
| 弹窗表单 | `components/EditDialog` + `useEditForm` |
| 跨区块编排 | 留 `index.vue` |

## 步骤

0. Read [shared/rules-activation.md](../shared/rules-activation.md) 及原页面类型对应 rules；**Read [TypeScript与types规范.mdc](../../rules/TypeScript与types规范.mdc)**
1. 读完整文件，标出 UI 区块与数据域；**标出所有 interface/type/any 位置**
2. 输出拆分清单（新建文件 + 职责）**先给用户确认**（大范围拆分时）
3. **类型归位：** 拆分前/同时将页面级类型写入 `types.ts`；hook 内 `export interface` 迁出
4. 先抽 hooks（逻辑），再抽 components（视图）
5. `index.vue` 改为组装，import 子模块
6. 执行 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) §types

## 与 code-normalize 区别

| Skill | 侧重 |
|-------|------|
| **page-refactor** | 文件过大、区块拆分、新 hooks/components |
| **code-normalize** | types 归位、constants/utils 职责分离、消除 any，不必大拆 |

二者可组合：先 `code-normalize` 归位类型，再 `page-refactor` 拆文件。

## 与 shared-component 区别

- **page-refactor**：单页面内拆分 → `subPackages/.../<page>/components/`
- **模块 components**：同模块多页复用 → `subPackages/<module>/components/` 或顶层 `components/`
- **shared-component**：跨模块复用 → 顶层 `components/`

## 禁止

- 拆分时改变业务行为
- 顺便改命名/改接口（除非用户要求）
- 拆成过多一层目录（单区块不必再套 `components/X/Y/Z`）

## 交付

1. 拆分前后结构对比
2. 新文件列表与各文件职责
3. 行为不变的说明
