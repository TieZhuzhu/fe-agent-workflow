<template>
  <div class="hi-table">
    <div v-if="$slots.toolbar" class="hi-table__toolbar">
      <slot name="toolbar" />
    </div>

    <el-table
      ref="table"
      v-loading="loading"
      v-bind="tableBind"
      v-on="tableListeners"
    >
      <slot />
      <template slot="empty">
        <slot name="empty">
          <div class="hi-table__empty" :class="{ 'is-transparent': !tableData }">
            没有更多数据了
          </div>
        </slot>
      </template>
    </el-table>

    <div v-if="showPager" class="hi-table__footer">
      <el-row type="flex" align="middle">
        <el-col :span="10">
          <div v-if="$slots.footer" class="hi-table__footer-actions">
            <slot name="footer" />
          </div>
        </el-col>
        <el-col :span="14" class="hi-table__pager">
          <el-pagination
            :current-page="pagination.pageNo"
            :page-size="pagination.pageSize"
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

<script>
import { listRequest } from './utils/listRequest'

/** 需代理给外部的 el-table 实例方法 */
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
]

export default {
  name: 'HiTable',
  inheritAttrs: false,
  props: {
    /** 远程列表接口路径，传入后启用远程分页模式 */
    url: {
      type: String,
      default: '',
    },
    /** 远程请求方法 */
    method: {
      type: String,
      default: 'post',
    },
    /** 远程请求附加参数 */
    params: {
      type: Object,
      default: () => ({}),
    },
    /** 是否展示分页器，远程模式默认开启 */
    pager: {
      type: Boolean,
      default: true,
    },
    pageSizes: {
      type: Array,
      default: () => [10, 20, 50, 100, 200],
    },
    defaultPageSize: {
      type: Number,
      default: 10,
    },
    /** 默认排序字段 */
    sortField: {
      type: String,
      default: '',
    },
    /** 默认是否降序 */
    sortDesc: {
      type: Boolean,
      default: true,
    },
    /** 响应 data 字段格式化 */
    dataFormat: {
      type: Function,
      default: (data) => data,
    },
    /** 挂载后是否立即请求 */
    immediate: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      loading: false,
      tableData: null,
      pagination: {
        pageNo: 1,
        pageSize: this.defaultPageSize,
        total: 0,
        sortName: this.sortField,
        sortDesc: this.sortDesc,
      },
    }
  },
  computed: {
    isRemote() {
      return !!this.url
    },
    showPager() {
      return this.pager && this.isRemote && this.tableData && this.tableData.length
    },
    tableBind() {
      const data = this.isRemote ? this.tableData : (this.$attrs.data || [])
      return {
        ...this.$attrs,
        data,
      }
    },
    tableListeners() {
      const listeners = { ...this.$listeners }

      if (!this.isRemote) {
        return listeners
      }

      const userSortChange = listeners['sort-change']
      listeners['sort-change'] = (sort) => {
        this.handleRemoteSort(sort)
        if (userSortChange) {
          userSortChange(sort)
        }
      }
      return listeners
    },
  },
  watch: {
    sortField(val) {
      this.pagination.sortName = val
    },
    sortDesc(val) {
      this.pagination.sortDesc = val
    },
  },
  mounted() {
    this.bindTableRefMethods()
    if (this.isRemote && this.immediate) {
      this.load()
    }
  },
  methods: {
    bindTableRefMethods() {
      TABLE_REF_METHODS.forEach((method) => {
        this[method] = (...args) => {
          const table = this.$refs.table
          if (table && typeof table[method] === 'function') {
            return table[method](...args)
          }
          return undefined
        }
      })
    },
    getTableRef() {
      return this.$refs.table
    },
    buildQueryParams() {
      return Object.assign({}, this.pagination, this.params)
    },
    load() {
      if (!this.isRemote) {
        return Promise.resolve()
      }

      this.loading = true
      const query = this.buildQueryParams()

      return listRequest(this.url, query, this.method).then((res) => {
        const list = this.dataFormat(res.data.data || [])
        this.tableData = list
        this.pagination.total = Number(res.data.total) || 0
        this.$emit('load', {
          data: list,
          total: this.pagination.total,
        })
      }).finally(() => {
        this.loading = false
      })
    },
    reload() {
      this.pagination.pageNo = 1
      return this.load()
    },
    handleRemoteSort({ prop, order }) {
      if (order) {
        this.pagination.sortName = prop
        this.pagination.sortDesc = order !== 'ascending'
      } else {
        this.pagination.sortName = this.sortField
        this.pagination.sortDesc = this.sortDesc
      }
      this.pagination.pageNo = 1
      this.load()
    },
    handlePageChange(pageNo) {
      this.pagination.pageNo = pageNo
      this.load()
    },
    handleSizeChange(pageSize) {
      this.pagination.pageSize = pageSize
      this.pagination.pageNo = 1
      this.load()
    },
  },
}
</script>

<style lang="scss" scoped>
.hi-table__toolbar {
  display: flex;
  text-align: left;

  ::v-deep .el-button--small {
    margin: 0 0 16px;
    font-size: 14px;
    padding: 8px 16px;
  }

  ::v-deep .el-dropdown {
    margin: 0 0 16px 8px;

    .el-button {
      margin: 0;
    }
  }

  ::v-deep .el-button + .el-button {
    margin-left: 8px;
  }

  ::v-deep .el-select {
    margin: 16px 0 16px 8px;
    vertical-align: bottom;
  }
}

.hi-table__footer {
  padding-top: 16px;
}

.hi-table__footer-actions {
  ::v-deep .el-button--small {
    font-size: 14px;
  }

  ::v-deep .el-dropdown {
    margin-left: 8px;
  }

  ::v-deep .el-button + .el-button {
    margin-left: 8px;
  }

  ::v-deep .el-select {
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

.hi-table ::v-deep {
  .el-table thead {
    color: #262626;
  }

  .el-table th {
    background-color: #fafafa;
    padding: 9px 0;
    font-weight: 400;
    height: 34px;

    .cell {
      height: 34px;
      line-height: 34px;
    }
  }

  .el-table td {
    border-bottom-color: #f5f5f5;
    overflow: visible;
    position: static;

    .cell {
      overflow: visible;
      word-break: break-word;
    }
  }

  .el-table__body tr:hover .icon-edit {
    opacity: 1;
  }

  .el-table--enable-row-hover .el-table__body tr:hover > td {
    background: #eff7ff !important;
  }

  .el-pagination {
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

    .el-pager li.active {
      color: #226bf2;
      border-color: #226bf2;
    }

    .el-input--mini .el-input__inner {
      height: 32px;
    }

    .el-pagination__total {
      margin-right: 4px;
      height: 32px;
      line-height: 32px;
      font-size: 14px;
    }
  }
}
</style>
