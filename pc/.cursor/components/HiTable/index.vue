<template>
  <div class="hi-table">
    <div v-if="$slots.toolbar" class="hi-table__toolbar">
      <slot name="toolbar" />
    </div>

    <el-table
      ref="tableRef"
      v-loading="loading"
      v-bind="tableBind"
      @sort-change="onSortChange"
    >
      <slot />
      <template #empty>
        <slot name="empty">
          <div class="hi-table__empty" :class="{ 'is-transparent': !tableData }">
            没有更多数据了
          </div>
        </slot>
      </template>
    </el-table>

    <div v-if="showPager" class="hi-table__footer">
      <el-row align="middle">
        <el-col :span="10">
          <div v-if="$slots.footer" class="hi-table__footer-actions">
            <slot name="footer" />
          </div>
        </el-col>
        <el-col :span="14" class="hi-table__pager">
          <el-pagination
            v-model:current-page="pagination.pageNo"
            v-model:page-size="pagination.pageSize"
            :page-sizes="pageSizes"
            :total="pagination.total"
            layout="total, prev, pager, next, sizes"
            @current-change="handlePageChange"
            @size-change="handleSizeChange"
          />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, useAttrs } from 'vue'
import { listRequest } from './utils/listRequest'

defineOptions({
  name: 'HiTable',
  inheritAttrs: false,
})

const TABLE_REF_METHODS = [
  'clearSelection',
  'toggleRowSelection',
  'toggleAllSelection',
  'toggleRowExpansion',
  'setCurrentRow',
  'clearSort',
  'clearFilter',
  'doLayout',
  'sort',
] as const

interface LoadPayload {
  data: unknown[]
  total: number
}

interface SortChangePayload {
  prop: string
  order: 'ascending' | 'descending' | null
}

const props = withDefaults(
  defineProps<{
    url?: string
    method?: string
    params?: Record<string, unknown>
    pager?: boolean
    pageSizes?: number[]
    defaultPageSize?: number
    sortField?: string
    sortDesc?: boolean
    dataFormat?: (data: unknown[]) => unknown[]
    immediate?: boolean
  }>(),
  {
    url: '',
    method: 'post',
    params: () => ({}),
    pager: true,
    pageSizes: () => [10, 20, 50, 100, 200],
    defaultPageSize: 10,
    sortField: '',
    sortDesc: true,
    dataFormat: (data: unknown[]) => data,
    immediate: true,
  }
)

const emit = defineEmits<{
  load: [payload: LoadPayload]
}>()

const attrs = useAttrs()

const tableRef = ref()
const loading = ref(false)
const tableData = ref<unknown[] | null>(null)
const pagination = ref({
  pageNo: 1,
  pageSize: props.defaultPageSize,
  total: 0,
  sortName: props.sortField,
  sortDesc: props.sortDesc,
})

const isRemote = computed(() => !!props.url)

const showPager = computed(() => {
  return props.pager && isRemote.value && tableData.value && tableData.value.length > 0
})

const tableBind = computed(() => {
  const data = isRemote.value ? tableData.value : ((attrs.data as unknown[]) || [])
  return { ...attrs, data }
})

watch(
  () => props.sortField,
  (val) => {
    pagination.value.sortName = val
  }
)

watch(
  () => props.sortDesc,
  (val) => {
    pagination.value.sortDesc = val
  }
)

const buildQueryParams = () => {
  return Object.assign({}, pagination.value, props.params)
}

const load = () => {
  if (!isRemote.value) {
    return Promise.resolve()
  }

  loading.value = true
  const query = buildQueryParams()

  return listRequest(props.url, query, props.method)
    .then((res) => {
      const list = props.dataFormat((res.data?.data as unknown[]) || [])
      tableData.value = list
      pagination.value.total = Number(res.data?.total) || 0
      emit('load', {
        data: list,
        total: pagination.value.total,
      })
    })
    .finally(() => {
      loading.value = false
    })
}

const reload = () => {
  pagination.value.pageNo = 1
  return load()
}

const handleRemoteSort = ({ prop, order }: SortChangePayload) => {
  if (order) {
    pagination.value.sortName = prop
    pagination.value.sortDesc = order !== 'ascending'
  } else {
    pagination.value.sortName = props.sortField
    pagination.value.sortDesc = props.sortDesc
  }
  pagination.value.pageNo = 1
  load()
}

const onSortChange = (sort: SortChangePayload) => {
  if (isRemote.value) {
    handleRemoteSort(sort)
  }
  const handler = attrs.onSortChange as ((payload: SortChangePayload) => void) | undefined
  handler?.(sort)
}

const handlePageChange = (pageNo: number) => {
  pagination.value.pageNo = pageNo
  load()
}

const handleSizeChange = (pageSize: number) => {
  pagination.value.pageSize = pageSize
  pagination.value.pageNo = 1
  load()
}

const getTableRef = () => {
  return tableRef.value
}

const proxyTableMethod = (method: (typeof TABLE_REF_METHODS)[number]) => {
  return (...args: unknown[]) => {
    const table = tableRef.value
    if (table && typeof table[method] === 'function') {
      return table[method](...args)
    }
    return undefined
  }
}

onMounted(() => {
  if (isRemote.value && props.immediate) {
    load()
  }
})

defineExpose({
  load,
  reload,
  getTableRef,
  clearSelection: proxyTableMethod('clearSelection'),
  toggleRowSelection: proxyTableMethod('toggleRowSelection'),
  toggleAllSelection: proxyTableMethod('toggleAllSelection'),
  toggleRowExpansion: proxyTableMethod('toggleRowExpansion'),
  setCurrentRow: proxyTableMethod('setCurrentRow'),
  clearSort: proxyTableMethod('clearSort'),
  clearFilter: proxyTableMethod('clearFilter'),
  doLayout: proxyTableMethod('doLayout'),
  sort: proxyTableMethod('sort'),
})
</script>

<style lang="scss" scoped>
.hi-table__toolbar {
  display: flex;
  text-align: left;

  :deep(.el-button--small) {
    margin: 0 0 16px;
    font-size: 14px;
    padding: 8px 16px;
  }

  :deep(.el-dropdown) {
    margin: 0 0 16px 8px;

    .el-button {
      margin: 0;
    }
  }

  :deep(.el-button + .el-button) {
    margin-left: 8px;
  }

  :deep(.el-select) {
    margin: 16px 0 16px 8px;
    vertical-align: bottom;
  }
}

.hi-table__footer {
  padding-top: 16px;
}

.hi-table__footer-actions {
  :deep(.el-button--small) {
    font-size: 14px;
  }

  :deep(.el-dropdown) {
    margin-left: 8px;
  }

  :deep(.el-button + .el-button) {
    margin-left: 8px;
  }

  :deep(.el-select) {
    display: inline-block;
    vertical-align: bottom;
    margin-left: 8px;
  }
}

.hi-table__pager {
  text-align: right;
}

.hi-table__empty {
  padding: 32px 0;
  color: rgba(0, 0, 0, 0.45);

  &.is-transparent {
    color: transparent;
  }
}

.hi-table :deep(.el-table thead) {
  color: #262626;
}

.hi-table :deep(.el-table th) {
  background-color: #fafafa;
  padding: 9px 0;
  font-weight: 400;
  height: 34px;

  .cell {
    height: 34px;
    line-height: 34px;
  }
}

.hi-table :deep(.el-table td) {
  border-bottom-color: #f5f5f5;
  overflow: visible;
  position: static;

  .cell {
    overflow: visible;
    word-break: break-word;
  }
}

.hi-table :deep(.el-table__body tr:hover .icon-edit) {
  opacity: 1;
}

.hi-table :deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background: #eff7ff !important;
}

.hi-table :deep(.el-pagination) {
  margin-right: -15px;

  .el-pager li,
  button {
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    margin: 0 4px;
    font-weight: 400;
    height: 32px;
    line-height: 30px;
    min-width: 32px;
    padding: 0 8px;
  }

  .el-pager li.is-active {
    color: #226bf2;
    border-color: #226bf2;
  }

  .el-input--small .el-input__inner {
    height: 32px;
  }

  .el-pagination__total {
    margin-right: 4px;
    height: 32px;
    line-height: 32px;
    font-size: 14px;
  }
}
</style>
