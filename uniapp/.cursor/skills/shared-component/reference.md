# shared-component 参考手册

> 主流程见 [SKILL.md](./SKILL.md)。本节为**按需 Read**的示例、目录模板与验收细节，非预加载必选项。

---

## 组件拆分要求

| 情况 | 做法 |
|------|------|
| 组件 > 300 行或含 2+ 独立 UI 区块 | 拆 `components/Xxx/SubPart/index.vue` |
| 选择器 + 预览区 + 操作栏 | 父组件组装，子目录各管一块 |
| 复杂交互逻辑（Vue 3） | 抽 `useXxx.ts` 放组件目录内 |
| 复杂交互逻辑（Vue 2） | 抽 `mixins/xxxMixin.js` 或 `methods` 分组 |

```
components/MediaPicker/
├── index.vue
├── types.ts
├── constants.ts
├── hooks/useMediaPicker.ts
├── components/
│   ├── ThumbnailList/index.vue
│   └── UploadTrigger/index.vue
└── README.md
```

---

## 目录结构模板

**跨模块（顶层，Vue 3）：**

```
components/CategoryPicker/
├── index.vue
├── services.ts          # 组件独有接口（禁止堆到 components/services.ts）
├── types.ts
├── constants.ts
├── utils.ts
├── hooks/useXxx.ts
├── components/
└── README.md
```

**同模块（Vue 2）：**

```
subPackages/product/components/CategoryPicker/
├── index.vue
├── constants.js
└── index.js
```

**类型与枚举（Vue 3）：**

- 类型 → `types.ts`；枚举 / 静态 options → `constants.ts`
- 禁止在 `index.vue` 内联可复用 interface

```ts
// types.ts
export interface CategoryOption {
  id: number
  name: string
}
```

```ts
// constants.ts
export const DEFAULT_PLACEHOLDER = '请选择分类'
```

---

## Vue 2 完整示例（picker 选择器）

```vue
<template>
  <picker :range="options" range-key="name" :value="pickerIndex" :disabled="disabled" @change="handleChange">
    <view class="picker-value">{{ displayLabel || placeholder }}</view>
  </picker>
</template>

<script>
export default {
  name: 'CategoryPicker',
  props: {
    value: { type: [Number, String], default: '' },
    options: { type: Array, default: () => [] },
    disabled: { type: Boolean, default: false },
    placeholder: { type: String, default: '请选择分类' },
  },
  computed: {
    pickerIndex() {
      return Math.max(0, this.options.findIndex((item) => item.id === this.value))
    },
    displayLabel() {
      const item = this.options.find((o) => o.id === this.value)
      return item ? item.name : ''
    },
  },
  methods: {
    handleChange(e) {
      const item = this.options[e.detail.value]
      this.$emit('input', item ? item.id : '')
      this.$emit('change', item ? item.id : '')
    },
  },
}
</script>
```

---

## 导出示例

```ts
// components/index.ts
export { default as CategoryPicker } from './CategoryPicker/index.vue'

// subPackages/product/components/index.js
export { default as CategoryPicker } from './CategoryPicker/index.vue'
```

---

## README 模板

```markdown
# CategoryPicker

跨模块分类选择器。

## Props
| 名 | 类型 | 默认 | 说明 |
|----|------|------|------|
| modelValue | number \| string | - | v-model |

## Events
| 名 | payload | 说明 |
|----|---------|------|
| change | value | 选中变化 |
```

---

## 边界原则（完整）

| 应该 | 不应该 |
|------|--------|
| UI + 通用交互 | 绑定具体页面路由名 |
| props 收数据 | 由父组件传入；组件内不直接 import 页面 `services` |
| 跨模块 UI → 顶层 `components/` | 同模块多页也放顶层 |
| 跨模块纯逻辑 → `hooks/useXxx.ts` | 为纯逻辑建空壳 `.vue` |
| Vue 3 类型 / 枚举分离文件 | 内联可复用类型 |

---

## 验收清单

- [ ] 放置层级正确
- [ ] Props / Events 有 types.ts 或 JSDoc
- [ ] 无页面级 services 依赖
- [ ] 已更新 index 导出
- [ ] README 或注释含用法示例
