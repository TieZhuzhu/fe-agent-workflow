# 全项目 Rules 重构验收清单

> **用途：** `rules-refactor` 最终验收。  
> **完成条件：** 全部 🔴 = 0、**`【verify】project-refactor` PASS**、项目可编译通过（有 build script 时）。

---

## §SDD 门禁 🔴

- [ ] `docs/features/project-refactor/` 存在（proposal / spec / design / tasks / field-map）
- [ ] `spec.md` 含 ≥1 业务回归验收场景
- [ ] `e2e.md` 含 P0 冒烟路径（H5 或小程序）
- [ ] `docs/project-refactor-inventory.md` 全部模块 ✅
- [ ] `tasks.md` 全部 [x] 或 skip 理由
- [ ] `【verify】project-refactor` PASS

---

## §项目级 🔴

### 权威与范围

- [ ] 重构依据为 `.cursor/rules`
- [ ] pages.json path、接口 URL、文案未擅自改

### 目录与分包 🔴

- [ ] 非 tabBar 页均在 subPackages
- [ ] 子包按功能模块，无单页滥建新子包
- [ ] pages.json path 与文件一致
- [ ] `components/<Name>/index.vue`，无平铺
- [ ] constants / utils 分离
- [ ] `@/` alias

### 接口层 🔴

- [ ] 接口组织符合项目惯例（页面级或集中式，全项目一致）
- [ ] 入参原样透传
- [ ] 出参直绑，无 normalizeRows

### 列表页 🔴

- [ ] 原生列表 / scroll-view
- [ ] 分页/刷新与项目一致
- [ ] 空态处理

### Vue 写法 🔴

- [ ] Vue 2/3 无混用
- [ ] 原生组件优先

### 构建 🔴

- [ ] 编译 / build 通过
- [ ] lint 零 error（有 lint 时）
