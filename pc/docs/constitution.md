# 项目宪法（Constitution）

> 通用原则，适用于所有中后台 Vue 前端项目。技术栈细节以 `project-conventions.md`（bootstrap 扫描）为准。

## 技术栈（默认）

- Vue 3 + Composition API + `<script setup lang="ts">`
- Element Plus + Pinia
- 页面接口：`services.ts`；类型：`types.ts`（就近）

## 不可违反原则

1. **先 spec 后代码**：新建页 / 多文件 feature 须在 `docs/features/<slug>/` 有 `design.md` + `tasks.md` 后再写码（简单增量可省略）
2. **路由 path ↔ 目录一致**：`/product/tag-list` → `views/product/tag-list/`
3. **接口入参原样透传**：禁止 `|| ''` / `|| undefined` 兜底筛选条件
4. **出参原样绑定**：禁止 `normalizeRows` 多字段链式猜测
5. **展示空值**：模板用 `?? '-'`，不用 `||`（当 `0` 合法时）
6. **禁止 mock**：除非用户明确要求
7. **types 就近**：页面级 interface 只在 `types.ts`
8. **权限**：菜单由接口树 + 统一守卫；按钮由接口鉴权，前端不做 `v-permission`
9. **最小 diff**：增量 / bugfix 不借机重构无关代码
10. **交付可验证**：feature 完成须过 `feature-verify`（spec + checklist + test/build）
11. **测试策略**：以 `project-conventions.md` §测试策略 为准（当前 **pending**，TDD strict 暂缓执行）

## 测试策略 — TDD strict（目标态，当前暂缓）

> **当前状态（2026-07-10）：`testStrategy: pending`** — `package.json` 无 `test` script，**不强制**先测后码。引入 Jest/Vitest 基建后改为 `strict`。

| 阶段 | pending（当前） | strict（基建就绪后） |
|------|-----------------|---------------------|
| 规划 | logic 项可标 `[test]` 备查 | 须标 `[test]` |
| 实现 | 先实现；`feature-verify` 的 test 行标 **skip** | 先失败测试 → 再实现 |
| 验收 | `test:unit` skip 合法 | 不得 skip |
| 豁免 | 默认即 pending，无需每次 `【no-tdd】` | 仅 `【no-tdd】` 可单次豁免 |

**基建就绪后：** 在 `project-conventions.md` 将 `testStrategy` 改为 `strict`，并配置 `npm run test:unit`。

**优先测（strict 时）：** utils / toXxxParams / constants 映射 / services 调用形态（见 `unit-test-codegen`）。

## 权威来源优先级

```
docs/constitution.md（原则）
  → .cursor/rules/*.mdc（写法）
  → .cursor/skills（流程）
  → docs/features/<slug>/（本 feature 规格）
  → .cursor/project-conventions.md（项目扫描事实）
```
