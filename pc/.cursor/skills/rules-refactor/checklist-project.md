# 全项目 Rules 重构验收清单

> **用途：** `rules-refactor` ⑤ 最终验收 + 每轮闭环。  
> **权威：** `.cursor/rules`；单页细则叠加 [code-normalize/checklist.md](../code-normalize/checklist.md)。  
> **完成条件：** 本节全部 🔴 = 0 且 `npm run build` 通过。

---

## §项目级 🔴

### 权威与范围

- [ ] 重构依据为 `.cursor/rules`
- [ ] **`docs/features/project-refactor/`** 存在且 `【verify】project-refactor` PASS
- [ ] **`docs/project-refactor-inventory.md`** 全部业务模块 ✅
- [ ] **`tasks.md`** 全部 [x] 或标注 skip
- [ ] 路由 path、接口 URL、文案未擅自改

### 执行流程

- [ ] 未在中途向用户询问「是否继续改 xxx」（用户未说暂停）
- [ ] 至少一轮 build + 全项目 review 闭环已执行
- [ ] 最终交付含重构报告 + 冒烟建议

### 目录与命名 🔴

- [ ] `views/<module>/<page-dir>/` kebab-case，入口 `index.vue`
- [ ] 无 `Index.vue` / `Action.vue` 等 PascalCase 单文件页（已迁 `action/index.vue` 等）
- [ ] 顶层 `components/<ComponentName>/index.vue`，无 `components/Foo.vue` 平铺
- [ ] 页面 `components/<ComponentName>/index.vue`，无页面子组件 `Foo.vue` 平铺
- [ ] 组件独有 `services` / `constants` / `types` / `utils` 在同组件目录内
- [ ] 页面 `constants.js` 与 `utils.js` 分离，constants 文件无工具函数 export
- [ ] `@/` alias，无深层 `../../../` 引用

### 接口层 🔴

- [ ] 业务页 API 在页面目录 `services.js` / `services.ts`
- [ ] 无 `views/<module>/services.js` 堆砌单页接口（须拆回各页；模块级仅 ≥2 页真实共用）
- [ ] App.vue / store / 多模块共用 API 在 **`src/services.js`**
- [ ] 组件独有 API 在 `components/<Name>/services.js`，无 `components/services.js` 集中文件
- [ ] `views/**` 无 `from '@/service'`（公共组件除外且需有注释说明）
- [ ] 入参原样透传，无 `buildXxxQuery` 仅判空
- [ ] 出参直绑，无 `normalizeRow` / `mapXxxToDetailUi` 整包重组（展示用 formatter 除外）
- [ ] 分页入参 `pageNo` + `pageSize`，禁止 `page`

### 列表页 🔴

- [ ] 全部列表页使用 HiTable（Vue2 → HiTable-vue2 规范）
- [ ] 无 `:pager="true"` 冗余
- [ ] 无页面级 `:resp-format`（HiTable 内置解包）
- [ ] 无 `:data-format` 行字段重组

### Vue 版本 🔴

- [ ] Vue2 项目：Options API，无 script setup / Pinia
- [ ] Vue3 项目：script setup + 全箭头函数等（见 rules）

### 代码质量 🔴

- [ ] 无未引用 mock / dead code
- [ ] 无业务 `console.log`
- [ ] `npm run lint-fix` 通过（零 ESLint error；见 `lint-check`）
- [ ] `npm run build` 通过，**无** `export 'Xxx' was not found` 等缺失引入/导出警告

---

## §按模块复验

对每个 `views/**/index.vue` 业务页，复跑 [code-normalize/checklist.md](../code-normalize/checklist.md) 中适用 🔴 项。

---

## §审查结论模板

```markdown
## 全项目 Review（rules-refactor 闭环）
- 结论：通过 / 未通过
- 阻塞项：N
- build：通过 / 失败

### 阻塞项（须自动继续修复，勿询问用户）
1. ...

### 已通过要点
- ...
```

**未通过 → 自动回到改码，不得交付「重构完成」。**
