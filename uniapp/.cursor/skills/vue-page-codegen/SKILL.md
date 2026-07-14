---
name: vue-page-codegen
version: 1.0.1
description: 生成 uni-app 页面/组件代码。新建列表/表单/详情/弹层页时触发。Vue 2/3 按项目版本。由 feature-dev-workflow ③ 或独立触发。
---
# uni-app 页面代码生成

> 由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③ 调用；也可独立触发。

## 0. 规范预加载（强制）

1. [shared/rules-activation.md](../shared/rules-activation.md)
2. `uniapp代码生成指南.mdc` + Vue 版本指南
3. `路由与分包规范.mdc`（新建页）
4. 同子包已有页面 + request import 对齐

交付首行：`规范预加载：Vue x | uni-app 列表页 | ... | 分包 subPackages/xxx`

## 1. 判定 Vue 版本

读取 `package.json`：`vue@^2.x` → `Vue2代码生成指南.mdc`；否则 `Vue代码生成指南.mdc`。

## 2. 判定页面类型

| 类型 | 参考 |
|------|------|
| 列表页 | uniapp指南 §列表页 |
| 表单页 | uniapp指南 §表单页 |
| 详情页 | uniapp指南 §详情页 |
| 弹层 | uniapp指南 §弹层 / u-popup |
| 复杂页 | 先输出文件拆分清单 |

## 3. 确定文件位置（分包优先）

```
① 是否 tabBar 页？
   是 → pages/<module>/<page>.vue
   否 → subPackages/<module>/<page>.vue 或 <page>/index.vue

② 子包是否已存在？
   是 → 追加到已有 subPackages/<module>
   否 → 评估是否需新建子包（见路由与分包规范）

③ 同步注册 pages.json
```

### 页面级文件（推荐新建）

```
subPackages/order/list/
├── index.vue
├── services.js       # 或沿用 service/order.js（conventions）
├── constants.js
├── types.ts          # Vue3 TS
└── components/
```

## 4. 列表页骨架（Vue 3）

```vue
<template>
  <view class="page">
    <scroll-view
      scroll-y
      class="list-scroll"
      @scrolltolower="handleLoadMore"
    >
      <view v-for="item in list" :key="item.id" class="list-item">
        <text>{{ item.name ?? '-' }}</text>
      </view>
      <view v-if="!list.length && !loading" class="empty">暂无数据</view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad, onPullDownRefresh } from '@dcloudio/uni-app'
import { GetList } from './services'
import type { ListItem } from './types'

const list = ref<ListItem[]>([])
const loading = ref(false)
const query = ref({ pageNo: 1, pageSize: 20 })
const finished = ref(false)

const loadList = async (reset = false) => {
  if (loading.value) return
  if (reset) {
    query.value.pageNo = 1
    finished.value = false
  }
  if (finished.value) return
  loading.value = true
  try {
    const res = await GetList(query.value)
    const rows = res.data ?? []
    list.value = reset ? rows : [...list.value, ...rows]
    if (rows.length < query.value.pageSize) finished.value = true
    else query.value.pageNo += 1
  } finally {
    loading.value = false
  }
}

const handleLoadMore = () => loadList()

onLoad(() => loadList(true))

onPullDownRefresh(() => {
  loadList(true).finally(() => uni.stopPullDownRefresh())
})
</script>
```

## 5. 表单页要点

- 原生 `input` / `textarea` / `picker` 优先
- 提交 `handleSubmit`，防重复
- 校验失败 `uni.showToast({ icon: 'none' })`

## 6. pages.json 注册

```json
{
  "root": "subPackages/product",
  "pages": [
    {
      "path": "list",
      "style": {
        "navigationBarTitleText": "商品列表",
        "enablePullDownRefresh": true
      }
    }
  ]
}
```

配合 [route-permission](../route-permission/SKILL.md) 执行。

## 7. 调研同模块

生成前 Read 同子包 1～2 个存量页，对齐：接口组织、列表方案、导航栏、空态样式。

## 禁止

- 非 tabBar 页放主包
- 未注册 pages.json 就交付
- mock 数据（除非用户要求）
