---
name: prd-feature-dev
version: 1.0.1
description: 基于 PRD 文档、原型截图、接口文档进行功能开发。语雀/飞书 Markdown 先走 prd-markdown-ingest。解析 PRD 文案与 UI 截图，提取页面结构、字段、交互与接口，生成符合 .cursor/rules 规范的 Vue 代码。在用户上传 PRD、需求文档、原型截图、接口说明并说「按 PRD 开发」「实现需求」时触发。
---
# PRD 驱动的功能开发

> 由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 调度。完成后回到主流程阶段 ②③④。

## 适用输入

| 类型 | 接入方式 |
|------|----------|
| **语雀 / 飞书 Markdown 粘贴** | 先 [prd-markdown-ingest](../prd-markdown-ingest/SKILL.md) → 本 Skill |
| PRD / 需求文档（Word 导出、本地 .md、飞书纯文本） | 本 Skill §步骤 1 起 |
| 原型截图 / 设计稿图片 | [spec-analyze-ui-images](../spec-analyze-ui-images/SKILL.md) |
| 接口文档 | Swagger / Markdown / 表格 / 口头描述 |
| **远程 Axure 原型站** | [prototype-html-feature-dev](../prototype-html-feature-dev/SKILL.md)（非本 Skill） |

以上任意组合（PRD + 截图 + 接口）时，Markdown 语雀路径仍优先走 prd-markdown-ingest。

---

## 步骤 1：材料清点

确认用户提供了什么：

| 类型     | 提取目标                                     |
| -------- | -------------------------------------------- |
| PRD 文案 | 功能描述、业务规则、字段说明、状态枚举、权限 |
| UI 截图  | 布局、组件、文案、交互状态                   |
| 接口文档 | URL、Method、请求参数、响应字段、分页结构    |

**语雀 / 飞书 Markdown 已粘贴**：执行 [prd-markdown-ingest](../prd-markdown-ingest/SKILL.md)，以输出的 **PRD Digest** 作为本阶段输入，勿重复手工解析 HTML 标签。

**缺接口文档**：从 PRD 字段推断接口需求，标注 `[待确认]`，禁止捏造字段。

**有 UI 截图**：加载 [spec-analyze-ui-images](../spec-analyze-ui-images/SKILL.md) 做结构化 UI 分析。

---

## 步骤 2：需求提取

输出结构化摘要：

```markdown
## 需求摘要

- 页面类型：列表页 / 表单页 / 详情页 / 组合
- 业务模块：<module>
- 页面目录：<page-dir>
- 路由建议：/<module>/<page-dir>

### 筛选/表单字段

| 字段 | 类型 | 必填 | 说明 |
| ---- | ---- | ---- | ---- |

### 表格列 / 展示字段

| 列名 | 字段 prop | 特殊渲染 |
| ---- | --------- | -------- |

### 操作与交互

- 按钮 / 弹窗 / 跳转 / 批量操作

### 接口

| 用途 | URL | Method | 关键字段 |
| ---- | --- | ------ | -------- |

### 待确认

- ...
```

### 页面类型判定

| 特征                         | 类型          | 代码要点                          |
| ---------------------------- | ------------- | --------------------------------- |
| 筛选区 + 列表 + 分页         | 列表页        | `onPullDownRefresh` + `onReachBottom` + 列表项组件 |
| 多字段录入 + 提交            | 表单页        | `uniapp代码生成指南.mdc` §表单 |
| 只读信息分组展示             | 详情页        | `uniapp代码生成指南.mdc` §详情 |
| 列表 + 弹窗编辑              | 组合页        | index.vue + `components/` + `u-popup` |
| 多统计卡片 + 多列表区块      | 复杂页        | 按区块拆 `components/` |
| Tab 切换，每 Tab 内容独立    | Tab 组合页    | `u-tabs` 或自定义 tab |

---

## 步骤 3：冲突处理

优先级：**接口文档 > PRD 文案 > UI 截图推断**

- 截图列名与接口字段不一致 → 以接口字段为准，label 用截图文案
- PRD 描述的状态值与接口枚举不一致 → 以接口为准，constants.ts 建映射
- 截图有但 PRD/接口未提及的功能 → 列入待确认，不擅自实现

---

## 步骤 4：缺口提问

以下任一项缺失时必须向用户确认（一次提 3～5 个最关键问题）：

1. 页面所属模块与路由 path
2. 列表接口 URL 与分页参数名（pageNo/pageSize 等）
3. 新增/编辑是独立页还是弹窗
4. 权限控制要求
5. 与现有页面的关联（跳转、复用组件）

---

## 步骤 5：进入实现

回到 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③，加载 [vue-page-codegen](../vue-page-codegen/SKILL.md) 生成代码。

### PRD 列表页映射示例

PRD 描述「商品标签管理：筛选标签名、列表展示名称/状态/关联数、新增编辑弹窗」→

```
other/tag-list/
├── list.vue              # 或 index.vue，与 pages.json path 一致
├── services.js           # 默认页面级；存量集中式见 project-conventions.md
└── components/
    └── EditPopup/
        └── index.vue
```

```js
// services.js（页面级默认）
import request from '@/common/request' // 以同模块已有 services 的 import 为准

/** 标签列表 */
export const GetTagList = (data) => request({ url: 'Product/Tag/List', data, method: 'post' })

/** 保存标签 */
export const SaveTag = (data) => request({ url: 'Product/Tag/Save', data, method: 'post' })
```

---

## 禁止事项

- 不根据截图猜测接口 URL 或字段名
- 不写 mock 数据代替真实接口
- 不用中文作代码 key / 路由 name
- 不跳过规范验收清单
