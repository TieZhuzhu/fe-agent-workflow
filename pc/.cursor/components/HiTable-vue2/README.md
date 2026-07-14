# HiTable（Vue 2）

基于 Element UI `el-table` 的列表页表格组件（Vue 2 + Options API），API 与 Vue 3 版 HiTable 一致，配合 Cursor 代码生成规范使用。

## 与 Vue 3 版差异

| 项 | Vue 2（本目录） | Vue 3（`HiTable/`） |
|----|-----------------|---------------------|
| 源码目录 | `.cursor/components/HiTable-vue2/` | `.cursor/components/HiTable/` |
| API 风格 | Options API | `<script setup lang="ts">` |
| UI 库 | Element UI | Element Plus |
| 工具栏插槽 | `slot="toolbar"` | `#toolbar` |
| 列插槽 | `slot-scope="scope"` | `#default="{ row }"` |
| 请求工具 | `utils/listRequest.js` | `utils/listRequest.ts` |
| 刷新列表 | `this.$refs.tableRef.reload()` | `tableRef.value?.reload()` |

**Props、事件、暴露方法（`reload`、`load`、`clearSelection` 等）与 Vue 3 版相同。**

## 接入项目

1. 将 `.cursor/components/HiTable-vue2/` 整个目录复制到项目 `components/HiTable/`
2. 修改 `utils/listRequest.js` 中的 `request` 引用

## 基础用法

```vue
<HiTable ref="tableRef" url="member/List" :params="form" @load="handleLoad">
  <template slot="toolbar">
    <el-button size="small" type="primary">批量操作</el-button>
  </template>
  <el-table-column type="selection" width="48" />
  <el-table-column label="昵称" prop="nickname" min-width="120" />
  <el-table-column label="操作" width="100" fixed="right">
    <template slot-scope="scope">
      <el-button type="text" @click="handleEdit(scope.row)">编辑</el-button>
    </template>
  </el-table-column>
</HiTable>
```

```js
import HiTable from '@/components/HiTable/index.vue'

export default {
  components: { HiTable },
  methods: {
    handleSearch() {
      this.$refs.tableRef.reload()
    },
  },
}
```

## Props

| Prop | 类型 | 默认 | 说明 |
|------|------|------|------|
| `url` | String | `''` | 接口路径，传入后启用远程模式 |
| `params` | Object | `{}` | 请求附加参数 |
| `pager` | Boolean | `true` | 是否显示分页 |
| `method` | String | `'post'` | 请求方法 |
| `sortField` | String | `''` | 默认排序字段 |
| `sortDesc` | Boolean | `true` | 默认降序 |
| `immediate` | Boolean | `true` | 挂载后是否立即请求 |

## 暴露方法

| 方法 | 说明 |
|------|------|
| `reload()` | 重置到第 1 页并刷新 |
| `load()` | 按当前页刷新 |
| `clearSelection()` | 清空选中（代理 el-table） |

完整示例见 `examples/MemberList.vue`
