# Design: <功能名>

## 页面类型

- [ ] 列表页  [ ] 表单页  [ ] 详情页  [ ] 列表+弹窗  [ ] 复杂页

## 路由与目录

| 路由 path | 页面目录 | route name |
|-----------|----------|------------|
| `/module/page-dir` | `views/module/page-dir/` | `ModulePageDir` |

> path 与目录**必须一致**。菜单由后端配置，path 与上表相同。

## 布局

- 列表布局：HiTable / 项目布局组件（以 `project-conventions.md` 为准）

## 文件清单

```
views/<module>/<page-dir>/
├── index.vue
├── types.ts
├── constants.ts      # 按需
├── services.ts
├── hooks/useXxx.ts   # 按需
└── components/       # 按需
```

## 接口

| 用途 | Method | URL / 函数名 | 说明 |
|------|--------|--------------|------|
| 列表 | POST | | |
| 保存 | POST | | |

## 状态与交互

- 筛选字段：
- 表格列：
- 工具栏操作：
- 弹窗（若有）：

## 子页 / 关联路由（若有）

| path | 说明 | activeMenu |
|------|------|------------|
| | | |
