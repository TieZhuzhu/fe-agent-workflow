---
name: incremental-feature
version: 1.0.1
description: 在已有 Vue 页面增量加筛选、列、按钮、弹窗字段与接口；最小 diff，禁止整页重写。 用户说【增量】、在这个页面加、补字段、列表加一列时触发。
---
# 已有页面增量开发

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 最高频日常场景：**改现有页，不是新建页。** 与 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 的区别：不输出完整文件清单，只做最小 diff。

## 触发场景

- 「在 XX 页面加一个筛选字段 / 表格列 / 操作按钮」
- 「编辑弹窗里补 XX 字段」
- 「列表页加导出 / 批量操作」
- 「详情页多展示一个区块」
- 「这个页面对接新接口 / 新字段」

**不触发本 Skill 的情况** → 走其他 Skill：

| 用户意图 | 改用 |
|----------|------|
| 从零新建页面 | `feature-dev-workflow` |
| 文件过大要拆分 | `page-refactor` |
| **按规范优化、整理、types 归位** | `code-normalize` |
| 仅改字段绑定、无新 UI | `api-integration`（若只对接不改 UI） |
| 报错修复 | `bugfix-workflow` |
| 新路由（本地 routes） | `route-permission`：仅追加 path / meta，菜单由后端配置 |

---

## 流程

```
① 规范预加载 → ② 读现有代码 → ③ 影响分析 → ④ 最小改动 → ⑤ 回归验收
```

### ① 规范预加载（强制）

**必须先 Read** [shared/rules-activation.md](../shared/rules-activation.md)，并按其中「按页面类型追加」读取对应 rules。**未读取不得改码。**

### ② 读现有代码

按顺序读取（路径以用户指定为准）：

1. 目标页面 `index.vue`（标准列表主流程应在此）
2. 同目录 `services.ts` / `services.js` / `types.ts` / `constants.ts` / `hooks/` / `mixins/`
3. 相关子组件（如 `EditDialog`）
4. 模块 `routes.ts` / `routes.js`（若涉及路由或权限）

输出 **现状摘要**（3～5 行）：

- 页面类型（列表 / 表单 / 组合 / 复杂）
- 已有筛选字段、表格列、主要接口
- 逻辑在 index 还是 hooks/components

### ③ 影响分析

列出本次改动触及的文件（通常 1～4 个）：

| 变更 | 可能修改 |
|------|----------|
| 加筛选字段 | `index.vue` form；**Vue 3 须同步 `types.ts` 的 Query** |
| 加表格列 | `index.vue` column；**新字段须同步 `types.ts` 的 Item** |
| 加工具栏按钮 | `index.vue` toolbar + 新方法 + 可能新 services |
| 弹窗加字段 | `EditDialog` + 校验 + Save 接口入参 |
| 新接口 | `services.ts` / `services.js` + 调用处 |
| 新页面路由 | `route-permission`：模块 `routes.ts` 追加项 |

**禁止**：借机重命名无关符号、整文件格式化、拆文件（除非用户要求）。

#### 新页面路由（仅本地 routes）

涉及新 path 注册时，**Read 并执行** [route-permission](../route-permission/SKILL.md)：

1. 确定 path：`/{module}/{page-dir}`（如 `/product/tag-list`）
2. 创建对应目录 `views/{module}/{page-dir}/`（**与 path 一致，禁止乱定义**）
3. 在 `views/<module>/routes.ts` 追加路由，`import('./{page-dir}/index.vue')`
4. 交付「待后端配置菜单」path——侧栏与页面访问由**接口菜单树**决定
5. **禁止**为按钮加 `v-permission` / `hasButtonPermission`（无权限由接口返回）

### ④ 最小改动

原则：

1. **沿用现有风格**：import 路径、命名、hooks 拆分程度与文件内已有代码一致
2. **Vue 3 加字段必改 `types.ts`**：Query/Item/Form 新属性写入类型，**禁止**只在 hook 里 inline 或 `any`
3. **接口字段以文档为准**；入参/出参遵守 [接口对接规范.mdc](../../rules/接口对接规范.mdc)，无文档标注 `[待确认]`，不猜 prop
4. 新 services 函数：`export const GetXxx = (data) => ...`（Vue 2 / Vue 3 统一箭头函数）
5. 新交互方法：Vue 3 用 `const handleXxx = () => {}`；Vue 2 用 `methods: { handleXxx() {} }`
6. 涉及新接口 → 同步更新 [api-integration](../api-integration/SKILL.md) 字段映射表（可在交付中附表）

**Vue 2 项目**：Read `Vue2代码生成指南.mdc`，沿用 Options API，**禁止**引入 hooks / Pinia 写法。

#### 常见增量模板（Vue 3）

**列表加筛选 + 列：**

```vue
<!-- index.vue：在现有 el-form 追加表单项，在 HiTable 内追加 column -->
<el-form-item label="状态：">
  <el-select v-model="form.status" placeholder="请选择" clearable>
    <el-option v-for="item in STATUS_OPTIONS" :key="item.value" :label="item.label" :value="item.value" />
  </el-select>
</el-form-item>

<el-table-column label="状态" prop="statusDesc" min-width="100" />
```

**工具栏加按钮：**

```vue
<template #toolbar>
  <!-- 保留原有按钮 -->
  <el-button size="small" @click="handleExport">导出</el-button>
</template>
```

**services 追加：**

```ts
import request from '@/config/request' // 与现有文件 import 路径保持一致

/** 导出列表 */
export const ExportList = (data: ExportListParams) =>
  request({ url: 'Product/Export', data, method: 'post', responseType: 'blob' })
```

#### 常见增量模板（Vue 2）

**列表加筛选 + 列：**

```vue
<el-form-item label="状态：">
  <el-select v-model="form.status" placeholder="请选择" clearable>
    <el-option
      v-for="item in STATUS_OPTIONS"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</el-form-item>

<el-table-column label="状态" prop="statusDesc" min-width="100" />
```

```js
// constants.js
export const STATUS_OPTIONS = [
  { label: '启用', value: 1 },
  { label: '禁用', value: 2 },
]
```

**工具栏加按钮：**

```vue
<template slot="toolbar">
  <el-button size="small" @click="handleExport">导出</el-button>
</template>
```

**services.js 追加：**

```js
import request from '@/config/request' // 与现有文件 import 路径保持一致

/** 导出列表 */
export const ExportList = (data) =>
  request({ url: 'Product/Export', data, method: 'post', responseType: 'blob' })
```

**methods 追加：**

```js
methods: {
  handleExport() {
    ExportList(this.form).then(/* 触发下载 */)
  },
},
```

**弹窗加字段（EditDialog）：**

- `data.form` 追加字段；`rules` 追加校验
- 文字操作按钮用 `type="text"`，不用 `link`
- 弹窗仍用 `:visible.sync` 或 `value` + `@input`

### ⑤ 回归验收

对照 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md) 中与本次改动相关的项：

- [ ] 原有筛选 / 列表 / 提交流程未破坏
- [ ] 新字段有 types 或注释
- [ ] 无 mock；TODO 已标注
- [ ] 新页面已按 `route-permission` 注册本地路由；待后端菜单 path 已交付 TODO
- [ ] 规范预加载已执行

---

## 缺口提问

以下缺失时一次问 1～3 个最关键问题：

1. 新字段的接口 prop 名与类型
2. 新接口 URL / Method
3. 按钮权限由接口鉴权，**不问**前端按钮码
4. 导出/批量操作的成功提示与失败处理

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 改当前页目录与局部 services/types
- 🚫 整页重写或新建完整页面结构

## 交付检查

**汇报内容**

1. **规范预加载**一行（见 rules-activation）
2. 修改文件列表与每项改动一句话
3. 新增接口与字段映射（如有）
4. 建议用户手动验证的操作步骤
5. 待确认 TODO

**门禁**

- [ ] `npm run lint-fix`
- [ ] 规范预加载已汇报
- [ ] ⑤ 回归验收清单已对照（见上文 §⑤）

