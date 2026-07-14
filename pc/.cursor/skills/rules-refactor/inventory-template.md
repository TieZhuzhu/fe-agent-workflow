# 全项目重构盘点模板

> Agent 在 `rules-refactor` ② 阶段填写并持续更新，写入 **`docs/project-refactor-inventory.md`**。  
> **计划与业务验收：** `docs/features/project-refactor/`（spec / tasks / e2e）。  
> **全部行 ✅ 且 checklist-project 🔴=0 且 verify PASS 方可结束。**

## 扫描命令参考

```bash
find src/views -name '*.vue' | sort
find src/components -name '*.vue' | sort
find src/service -name '*.js' -o -name '*.ts' 2>/dev/null | sort
rg -l "from '@/service'" src/
rg -l "normalize|buildListQuery|buildFilter|mapXxx" src/views/
rg -l "Index\.vue|Action\.vue" src/views/
```

---

## 模块盘点表

| 模块路径 | 页面类型 | 主要违规（摘要） | 优先级 | 状态 |
|----------|----------|------------------|--------|------|
| views/home/system-notice | 列表 | | P1 | ⬜ |
| views/product/store-goods | 列表 | | P1 | ⬜ |
| views/product/goods-detail | 详情 | | P2 | ⬜ |
| views/trade/order-manage | 列表 | | P1 | ⬜ |
| views/trade/refund | 列表 | | P1 | ⬜ |
| views/trade/return-product | 列表 | | P1 | ⬜ |
| views/trade/order-detail | 详情 | | P2 | ⬜ |
| views/trade/order-delivery | 表单 | | P2 | ⬜ |
| views/setting/admin | 列表 | | P1 | ⬜ |
| views/setting/permission-group | 列表 | | P1 | ⬜ |
| views/setting/operation-log | 列表 | | P1 | ⬜ |
| views/setting/store-settings | 复杂 | | P2 | ⬜ |
| views/login | 表单 | | P2 | ⬜ |
| … | | | | |

**状态：** ⬜ 待改 | 🔄 进行中 | ✅ 完成

---

## 基础设施

| 项 | 状态 | 备注 |
|----|------|------|
| HiTable 默认 pageResp 解包 | ⬜ | |
| 分页统一 pageNo/pageSize | ⬜ | |
| 页面级 services 迁移完成 | ⬜ | |
| src/service 无业务页引用 | ⬜ | |
| 目录 kebab-case + index.vue | ⬜ | |
| router import 路径已更新 | ⬜ | |

---

## 违规模式速查（grep 归零为目标）

| 模式 | 目标 |
|------|------|
| `:pager="true"` | 删除（默认 true） |
| `:resp-format=` | 删除（HiTable 内置） |
| `from '@/service'` 在 views 内 | 迁页面 services |
| `normalizeXxx` / `mapXxxToUi` 出参重组 | 直绑 + formatter |
| `buildXxxQuery` 入参判空 | 透传或文档映射 |
| `Index.vue` / `Action.vue` | kebab 目录 index.vue |
