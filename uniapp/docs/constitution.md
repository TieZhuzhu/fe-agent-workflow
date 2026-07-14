# 项目宪法（Constitution）

> 通用原则，适用于所有 **uni-app 移动端**项目。技术栈细节以 `project-conventions.md`（bootstrap 扫描）为准。

## 技术栈（默认）

- uni-app（H5 / 小程序 / App）
- Vue 3 + Composition API + `<script setup lang="ts">`（或 Vue 2 Options API，按项目判定，禁止混用）
- UI：**原生组件优先**，uview-ui 补充
- 路由：`pages.json` + 主包/分包
- 接口：默认页面级 `services.*`；存量集中式可沿用

## 不可违反原则

1. **先 spec 后代码**：新建页 / 多文件 feature 须在 `docs/features/<slug>/` 有 `design.md` + `tasks.md` 后再写码（简单增量可省略）
2. **非 tabBar 页禁止入主包**：业务页放 `subPackages`，控制主包体积
3. **子包按功能模块**：优先复用已有子包，禁止为单页随意新建子包
4. **path ↔ 文件一致**：`pages.json` 注册 path 与磁盘文件一一对应
5. **接口入参原样透传**：禁止 `|| ''` 兜底筛选条件
6. **出参原样绑定**：禁止 `normalizeRows` 多字段链式猜测
7. **展示空值**：模板用 `?? '-'`，不用 `||`（当 `0` 合法时）
8. **禁止 mock**：除非用户明确要求
9. **原生组件优先**：uview 仅作补充
10. **最小 diff**：增量 / bugfix 不借机重构无关代码
11. **交付可验证**：feature 完成须过 `feature-verify`
12. **测试策略**：`testStrategy: pending`（项目无 test script 时）；有单测 script 后升级为 `strict`

## 权威来源优先级

```
docs/constitution.md（原则）
  → .cursor/rules/*.mdc（写法）
  → .cursor/skills（流程）
  → docs/features/<slug>/（本 feature 规格）
  → .cursor/project-conventions.md（项目扫描事实）
```
