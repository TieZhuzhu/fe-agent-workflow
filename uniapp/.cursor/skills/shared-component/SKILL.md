---
name: shared-component
version: 1.0.1
description: 跨子包/跨模块 UI 公共组件（顶层 components/）。同子包多页放 subPackages/<module>/components/。无 UI 用 hooks/utils。
---
# 公共组件开发（uni-app）

> **跨子包 UI** → 顶层 `components/`  
> **同子包多页** → `subPackages/<module>/components/`  
> **纯逻辑** → `hooks/` / `common/`

## 放置位置

| 场景 | 位置 |
|------|------|
| 单页私有 | `<page>/components/` |
| 同子包多页 | `subPackages/<module>/components/` |
| **跨子包** | **`components/<Name>/`** |
| 纯逻辑 | `hooks/` / `common/` |

提升路径：页面 components → 子包 components → 顶层 components。

## 流程

① 预加载 → ② 确认层级 → ③ 调研存量组件 → ④ 定义 props/emits → ⑤ 实现 → ⑥ easycom 或手动注册

## 实现要点

- 原生组件优先，uview 补充
- 目录 `components/<Name>/index.vue`
- 组件私有 services 放同目录
- 引用：`import CustomNav from '@/components/CustomNav'`
- 小程序注意组件样式隔离与 setData 性能

复杂实现见 [reference.md](./reference.md)（按需 Read）。
