# Design: <功能名>

## 页面类型

- [ ] 列表页  [ ] 表单页  [ ] 详情页  [ ] 弹层  [ ] 复杂页

## 路由与目录

| 包类型 | pages.json path | 文件路径 | 子包 root |
|--------|-----------------|----------|-----------|
| 主包（仅 tabBar） | `pages/index/index` | `pages/index/index.vue` | — |
| 分包（默认） | `subPackages/product/list` | `subPackages/product/list.vue` | `subPackages/product` |

> **非 tabBar 页必须分包。** 优先放入已有子包。

## 布局

- 导航：系统导航栏 / 自定义导航（`navigationStyle: custom`）
- 列表：scroll-view 或 onReachBottom（与项目存量一致）
- UI：原生组件优先，uview 补充

## 文件清单

```
subPackages/<module>/<page>/
├── index.vue          # 或单文件 <page>.vue
├── services.js        # 或写入 service/<module>.js（按项目惯例）
├── constants.js       # 按需
├── types.ts           # Vue3 TS 按需
└── components/        # 按需
```

## 接口

| 用途 | Method | URL / 函数名 | 说明 |
|------|--------|--------------|------|
| 列表 | POST | | |
| 详情 | GET | | |

## 状态与交互

- 列表字段 / 筛选项：
- 表单字段：
- 跳转链路：
- 空态 / 加载态：

## 多端差异（若有）

| 平台 | 差异 |
|------|------|
| 微信小程序 | |
| H5 | |
| App | |
