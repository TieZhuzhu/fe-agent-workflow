# Skill 操作边界（项目基线 — uni-app）

> 各 Skill 正文须**引用本基线**并追加场景特有边界。对齐文章「原则五：能做、要问、别碰」。

---

## ✅ 放手做（默认允许）

- 在 `pages/`、`subPackages/<module>/` 下新增/修改业务页面文件
- 在 `docs/features/<slug>/` 读写 spec 工件
- 调用 `npm run lint` / `npm run build:*`（若 package.json 有 script）
- 调用 `.cursor/skills/scripts/feature-check.py`、`spec-index.py`
- 在页面目录或 `components/` 下新增模块内组件
- 按 `project-conventions.md` 使用 request 路径与接口组织方式

---

## ⚠️ 先问用户

- 修改顶层 `components/` 公共组件（应用 `shared-component` Skill 并确认）
- 修改 `manifest.json` / `pages.json` tabBar 配置
- 新增 npm 依赖或 uni_modules
- 修改 `pages.json` **path**（影响分包体积与跳转）
- 新建 subPackage root（须符合路由与分包规范）
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
- 非 tabBar 业务页放入主包 `pages`（违反分包规范）
- 为单页随意新建 subPackage
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
| `figma-feature-dev` | 禁止将状态栏/胶囊/Home 条写入页面代码 |
