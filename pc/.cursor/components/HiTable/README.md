# HiTable

基于 Element Plus `el-table` 的列表页表格组件（**Vue 3** + `<script setup>`），配合 Cursor 代码生成规范使用。

> Vue 2 项目请使用 `.cursor/components/HiTable-vue2/`，API 相同，语法为 Options API + Element UI。

## 设计原则

- `inheritAttrs: false` + `v-bind="$attrs"` 透传 el-table 全部属性
- 列定义使用原生 `el-table-column`
- **操作列**（最后一列）设 `align="right"`；其余数据列不设 `align`
- 远程模式默认开启分页（`pager` 默认 `true`）
- 通过 `defineExpose` 暴露 `reload`、`clearSelection` 等方法

## 接入项目

1. 将 `.cursor/components/HiTable/` 整个目录复制到项目 `components/HiTable/`
2. 修改 `utils/listRequest.ts` 中的 `request` 引用，对接项目请求封装

## 基础用法

```vue
<HiTable ref="tableRef" url="member/List" :params="form" @load="handleLoad">
  <el-table-column type="selection" width="48" />
  <el-table-column label="昵称" prop="nickname" min-width="120" />
  <el-table-column label="操作" width="100" align="right">
    <template #default="{ row }">
      <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
    </template>
  </el-table-column>
</HiTable>
```

```vue
<script setup lang="ts">
import { ref } from 'vue'
import HiTable from '@/components/HiTable/index.vue'

const tableRef = ref<InstanceType<typeof HiTable>>()

const handleSearch = () => {
  tableRef.value?.reload()
}
</script>
```

## Props

| Prop         | 类型     | 默认           | 说明                         |
| ------------ | -------- | -------------- | ---------------------------- |
| `url`        | String   | `''`           | 接口路径，传入后启用远程模式 |
| `params`     | Object   | `{}`           | 请求附加参数                 |
| `pager`      | Boolean  | `true`         | 是否显示分页                 |
| `method`     | String   | `'post'`       | 请求方法                     |
| `sortField`  | String   | `''`           | 默认排序字段                 |
| `sortDesc`   | Boolean  | `true`         | 默认降序                     |
| `immediate`  | Boolean  | `true`         | 挂载后是否立即请求           |
| `dataFormat` | Function | `data => data` | 响应 data 格式化             |

## 暴露方法

| 方法               | 说明                      |
| ------------------ | ------------------------- |
| `reload()`         | 重置到第 1 页并刷新       |
| `load()`           | 按当前页刷新              |
| `clearSelection()` | 清空选中（代理 el-table） |

## 完整示例

见 `examples/MemberList.vue`
