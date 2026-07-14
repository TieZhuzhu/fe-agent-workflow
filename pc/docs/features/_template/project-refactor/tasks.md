# Tasks: 全项目代码规范化重构

> 实现时逐项勾选。每阶段完成后 build + 冒烟再进入下一阶段。  
> Feature slug: **project-refactor**

## 0. Spec 门禁

- [ ] `proposal.md` / `spec.md` / `design.md` 已填写
- [ ] `field-map.md` 标注 N/A（不改接口）
- [ ] `e2e.md` P0 冒烟路径已列
- [ ] `【analyze】project-refactor` PASS（或 CRITICAL=0，status: ready）
- [ ] `project-conventions.md` 已生成（bootstrap）

## 1. 阶段 P0 — 基础设施

- [ ] inventory 已创建（`docs/project-refactor-inventory.md`）
- [ ] （填写具体项：App.vue、store、mock 等）
- [ ] `npm run build` 通过
- [ ] 冒烟：登录 + 任一列表页

## 2. 阶段 P1 — （模块名）

- [ ] （模块任务项）
- [ ] inventory 该模块 ✅
- [ ] `code-normalize` checklist 🔴 通过
- [ ] build + 模块冒烟

## 3. 全局收尾

- [ ] inventory 全部 ✅
- [ ] `checklist-project.md` 🔴 = 0
- [ ] `npm run lint-fix` 零 error
- [ ] `npm run build` 最终通过
- [ ] `【verify】project-refactor` PASS
- [ ] `【finish】project-refactor`

## 4. Backlog（Out of Scope）

- [ ] （记录后续阶段，不阻塞本次完成声明）
