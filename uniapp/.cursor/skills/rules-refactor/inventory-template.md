# 全项目重构盘点模板

> Agent 在 `rules-refactor` ② 阶段填写并持续更新，写入 **`docs/project-refactor-inventory.md`**。  
> **计划与业务验收：** `docs/features/project-refactor/`（spec / tasks / e2e）。  
> **全部行 ✅ 且 checklist-project 🔴=0 且 verify PASS 方可结束。**

## 扫描命令参考

```bash
find pages -name '*.vue' | sort
find subPackages -name '*.vue' | sort
find components -name '*.vue' | sort
find service -name '*.js' 2>/dev/null | sort
rg -l "normalize|buildListQuery|buildFilter" pages/ subPackages/
```

---

## 模块盘点表

| 模块路径 | 页面类型 | 主要违规（摘要） | 优先级 | 状态 |
|----------|----------|------------------|--------|------|
| pages/index | 首页 | | P0 | ⬜ |
| subPackages/product | 列表/详情 | | P1 | ⬜ |
| subPackages/order | 列表/表单 | | P1 | ⬜ |
| subPackages/user | 设置/资料 | | P1 | ⬜ |
| … | | | | |

**状态：** ⬜ 待改 | 🔄 进行中 | ✅ 完成

---

## 基础设施

| 项 | 状态 | 说明 |
|----|------|------|
| pages.json 主包瘦身 | ⬜ | 非 tabBar 是否误入主包 |
| request 封装 | ⬜ | |
| 接口组织 | ⬜ | 集中式/页面级是否一致 |
| store | ⬜ | |
| 公共组件 | ⬜ | |

---

## 违规类型速查

- 非 tabBar 页在主包 `pages`
- 单页新建多余 subPackage
- Element / PC 组件库
- Vue2/3 混用
- 入参兜底 / normalizeRows
- console.log 残留
- 未使用 import
