# Skill 操作边界（项目基线）

> 各 Skill 正文须**引用本基线**并追加场景特有边界。对齐文章「原则五：能做、要问、别碰」。

---

## ✅ 放手做（默认允许）

- 在 `views/<module>/<page>/` 下新增/修改业务页面文件
- 在 `docs/features/<slug>/` 读写 spec 工件
- 调用 `npm run lint-fix`、`npm run build`（交付验证）
- 调用 `.cursor/skills/scripts/feature-check.py`、`spec-index.py`
- 复制 `.cursor/components/HiTable/` 到页面 `components/`
- 按 `project-conventions.md` 使用 `@/config/request`

---

## ⚠️ 先问用户

- 修改 `src/components/` 顶层公共组件（应用 `shared-component` Skill 并确认）
- 修改 `vue.config.js` / `package.json` / ESLint 配置
- 新增 npm 依赖
- 修改路由 **path**（影响菜单/书签）
- 删除已有测试用例或大范围格式化无关文件
- 全项目 `rules-refactor` / `vue2-to-vue3-refactor` 中途暂停以外的 scope 扩展

---

## 🚫 绝对不要

- 提交 `.env`、token、密钥到仓库
- 未经用户要求写入 mock 数据
- `eslint-disable` 整文件或降低 lint 规则通过检查
- 为通过 CI 删除测试、改 workflow 降标准
- 接口入参 `|| ''` 兜底、出参 `normalizeRows` 猜字段
- 同文件混用 Vue 2 / Vue 3 写法
- 按钮级 `v-permission`（本项目菜单接口鉴权）
- 跳过 `feature-verify` 声称 feature 完成（新建 feature）

---

## 按风险加严

| 场景 | 额外 🚫 |
|------|---------|
| `feature-archive` | verify 未 PASS 不得合并 spec |
| `rules-refactor` | 不得改业务行为、不得中途询问；**无 project-refactor spec 不得大规模改码** |
| `vue2-to-vue3-refactor` | 不得无 **vue3-migration** spec 改码；不得 Vue2/Vue3 混用 |
| `api-smoke` | token 不得写入仓库或 conventions |
| `incremental-feature` | 禁止整页重写 |
