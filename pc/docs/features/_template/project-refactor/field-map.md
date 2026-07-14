# Field Map: project-refactor

**N/A — 本 feature 为代码规范化重构，不新增接口、不修改字段映射。**

存量接口字段以各页面现有绑定为准；重构时遵守 `接口对接规范.mdc`：

- 入参原样透传，禁止 `|| ''` 兜底筛选条件
- 出参原样绑定，禁止 `normalizeRows` 多字段链式猜测

## 分页字段参考（不改语义，仅统一组件配置）

| 页面 | page | size | 列表路径 | 总数路径 |
|------|------|------|----------|----------|
| HiTable 默认 | `pageNo` | `pageSize` | `data.data` | `data.totalCount` |
| （例外页） | | | | |

> 若某页后端仅接受 `page`，用 HiTable `query-params` 映射，**不猜字段**。
