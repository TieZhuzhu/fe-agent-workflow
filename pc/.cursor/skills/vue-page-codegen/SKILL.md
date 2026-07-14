---
name: vue-page-codegen
version: 1.0.1
description: 生成符合团队规范的 Vue 3 列表/表单/详情/弹窗/工作台页面代码。 由 feature-dev-workflow ③ 或【新建】独立触发；增量见 incremental-feature；vue@2.x 见 Vue2 指南。
---
# Vue 页面代码生成

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 通常由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③ 调用；也可独立用于新建/重构页面。

## 触发场景

- 新建列表页、表单页、详情页、弹窗组件
- 新建工作台、双栏页、多 Tab 组合页（见复杂页面指南）
- 新增业务模块页面
- 重构或拆分现有 Vue 文件

## 执行步骤

### 0. 规范预加载（强制）

**写码前必须 Read**（不可跳过）：

1. [shared/rules-activation.md](../shared/rules-activation.md) — 复杂任务先输出 §预加载计划
2. 判定页面类型后，Read 该类型对应的 rules
3. 搜索同模块已有页面 + 已有 `services.ts`，对齐 `request` import

交付首行标注：`规范预加载：Vue x | 页面类型 | Skill xxx | 已读 rules ×N | request 路径 xxx`

### 1. 项目类型

**默认 Vue 3**。仅当 `package.json` 中 `vue` 为 `^2.x` 时，改读 `Vue2代码生成指南.mdc` + `Vue代码生成指南.mdc` §Vue 2 + `HiTable-vue2/`。

### 2. 判定页面类型

| 类型       | 判定                   | 参考                                                         |
| ---------- | ---------------------- | ------------------------------------------------------------ |
| 列表页     | 筛选 + 表格 + 分页     | 本文 §列表页骨架                                             |
| 表单页     | 多字段录入 + 提交      | [表单与详情页开发指南](../../rules/表单与详情页开发指南.mdc) |
| 详情页     | 只读信息分组           | 同上 §详情页                                                 |
| 组合页     | 列表 + 弹窗编辑        | index + `components/EditDialog`                              |
| **复杂页** | 多区块/双栏/Tab/工作台 | [复杂页面开发指南](../../rules/复杂页面开发指南.mdc)         |

**复杂页不走单文件列表模板**，必须先输出文件拆分清单。

### 3. 确定文件位置

**列表页 HiTable**：复制 `.cursor/components/HiTable/` → 页面或模块 `components/HiTable/`。

```
views/<module>/
├── routes.ts
└── <page-dir>/
    ├── index.vue           # 标准列表：主流程在此；复杂页：布局编排
    ├── constants.ts
    ├── types.ts            # Query / Item / Form — 必建
    ├── utils.ts            # 展示格式化、文档要求的 toXxxParams（可选）
    ├── services.ts
    ├── hooks/              # 仅独立子域（表单/复杂页区块）；标准列表可不建
    └── components/
```

**types.ts 必含：** 列表 Query、行 Item；表单页加 Form DTO。**禁止**在 hook 内 `export interface` 页面级类型。

### hooks 与 index.vue 分工（强制）

| 页面 | index.vue | hooks |
|------|-----------|-------|
| 标准列表 | `query`、`loadList`、handlers、弹窗 state | 不建整页 `useXxxManage`；>400 行或弹窗复杂表单才抽 |
| 表单/详情 | 绑定、布局 | `useXxxForm` / `useXxxDetail` |
| 复杂页 | 布局 + 组合 hook | 每区块一个 hook |

**反模式：** `index.vue` 仅 `const { ...20项 } = useCustomerManage()` — 禁止。

### 4. 调研同模块代码

生成前搜索同模块已有页面，对齐目录结构与写法。

### 5. 选择页面模板

#### 列表页骨架（Vue 3，默认）

```vue
<template>
  <div>
    <el-form inline :model="form" class="filter" size="small" label-width="100px">
      <el-form-item label="名称：">
        <el-input v-model="form.name" placeholder="请输入" />
      </el-form-item>
      <el-form-item class="filter-actions">
        <el-button type="primary" class="button-small" @click="handleSearch">筛选</el-button>
        <el-button type="primary" link class="button-reset" @click="handleClear">重置</el-button>
      </el-form-item>
    </el-form>
    <HiTable ref="tableRef" url="Product/batchList" :params="form">
      <el-table-column label="名称" prop="name" min-width="100" />
      <el-table-column label="操作" width="120" align="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
        </template>
      </el-table-column>
    </HiTable>
    <EditDialog v-model="dialogVisible" :record="currentRow" @success="handleSearch" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import HiTable from '@/components/HiTable/index.vue'
import { EditDialog } from './components'

const tableRef = ref<InstanceType<typeof HiTable>>()
const form = reactive({ name: '' })
const dialogVisible = ref(false)
const currentRow = ref<Record<string, unknown>>()

const handleSearch = () => {
  tableRef.value?.reload()
}

const handleClear = () => {
  form.name = ''
  handleSearch()
}

const handleEdit = (row: Record<string, unknown>) => {
  currentRow.value = row
  dialogVisible.value = true
}
</script>

<style lang="scss" scoped>
@use 'styles/tablePage.scss';
</style>
```

#### 复杂页骨架（Vue 3）

```
views/<module>/workbench/
├── index.vue              # 布局编排 + 组合各区块 hook
├── services.ts
├── hooks/useSummary.ts
├── hooks/useTaskList.ts
└── components/
    ├── SummaryCards/index.vue
    ├── TaskPanel/index.vue
    └── index.ts
```

详见 [复杂页面开发指南](../../rules/复杂页面开发指南.mdc)。

#### 表单页骨架（Vue 3）

详见 [表单与详情页开发指南](../../rules/表单与详情页开发指南.mdc)。核心：`hooks/useXxxForm.ts` + `formPage.scss` + `FormRules` 校验。

```vue
<script setup lang="ts">
import { useCouponForm } from './hooks/useCouponForm'
const { formRef, form, rules, submitting, handleSubmit, handleCancel } = useCouponForm()
</script>
```

#### services.ts

```ts
import request from '@/config/request'

/** 批量列表 */
export const GetBatchList = (data: Record<string, unknown>) =>
  request({ url: 'Product/batchList', data, method: 'post' })
```

#### 模块 routes.ts

```ts
export default [
  {
    path: '/product/batch-off-shelf',
    name: 'productBatchOffShelf',
    component: () => import(/* webpackChunkName: "productBatchOffShelf" */ './batch-off-shelf/index.vue'),
    meta: {
      title: '批量下架',
      keepAlive: true,
    }
  }
]
```

详见 [路由与权限规范](../../rules/路由与权限规范.mdc)。

### 6. 自检清单

- [ ] 页面类型判定正确（列表/复杂页未混用模板）
- [ ] 目录：`views/<module>/<page-dir>/`，**与路由 path `/<module>/<page-dir>` 一致**
- [ ] 表单/详情：见表单与详情页指南；loading/empty/error 见状态与异步数据规范
- [ ] Vue 3：`<script setup lang="ts">`、hooks、HiTable
- [ ] 组件：PascalCase 目录 + `index.vue`；`components/index.ts` 统一导出
- [ ] 列表：HiTable + el-table-column；操作列 `align="right"`，其余列不设 `align`
- [ ] 接口：页面目录 `services.ts`，`export const GetXxx = (data) =>` 箭头函数
- [ ] 标准列表：主逻辑在 `index.vue`；无整页上帝 hook
- [ ] script setup / composable / utils：**箭头函数**，禁止 `function` 声明
- [ ] 路径使用 `@/` alias；scoped scss；无 mock
- [ ] 单文件建议 ≤800 行；职责可拆时已拆分

## 规则引用

完整清单见 [shared/rules-activation.md](../shared/rules-activation.md)。核心：

1. `.cursor/rules/前端通用代码规范.mdc`
2. `.cursor/rules/项目结构与命名规范.mdc`
3. `.cursor/rules/Vue代码生成指南.mdc`
4. `.cursor/rules/HTML与CSS代码生成指南.mdc`
5. `.cursor/rules/JavaScript通用代码生成指南.mdc`
6. `.cursor/rules/复杂页面开发指南.mdc`
7. `.cursor/rules/路由与权限规范.mdc`
8. `.cursor/rules/表单与详情页开发指南.mdc`
9. `.cursor/rules/状态与异步数据规范.mdc`

## Vue 2 兼容（低优先级）

`vue@2.x` 时见 `Vue2代码生成指南.mdc` + `Vue代码生成指南.mdc` §Vue 2 + `HiTable-vue2/`。日常开发以 Vue 3 为准。

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 写码前 Read rules-activation 与页面类型 rules
- 🚫 未预加载直接生成页面

## 交付检查

- [ ] 规范预加载汇报 + lint-fix
