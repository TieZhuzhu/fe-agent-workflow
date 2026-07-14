---
name: vue2-to-vue3-refactor
version: 1.2.0
description: uni-app Vue2 升 Vue3。须先 docs/features/vue3-migration/ ready，收尾【verify】vue3-migration。用户说「升 Vue3」「迁移 Vue3」时触发。
---
# uni-app Vue 2 → Vue 3 升级

> **计划与回归：** `docs/features/vue3-migration/`（**强制**，固定 slug）。  
> **进度：** `docs/vue3-migration-inventory.md`。  
> 仅做技术栈升级，不改业务行为。同版本规范整理 → `rules-refactor` + `project-refactor`。

---

## ⓪ SDD 门禁（强制）

| 条件 | 动作 |
|------|------|
| 无 `docs/features/vue3-migration/` | `【spec】propose vue3-migration` |
| ready | 开始迁移 |

详见 `docs/vue3-migration-guide.md`。与 `project-refactor` **互斥**。

---

## 范围

- Options API → `<script setup lang="ts">`
- Vuex → Pinia / Vuex 4
- 生命周期：`onLoad`/`onShow` from `@dcloudio/uni-app`
- uview 2 → uview 3 / uview-plus（按项目）

## 铁律

1. 不改 pages.json path
2. 不改接口 URL 与字段语义
3. 全项目统一 Vue 3，禁止混用
4. 无 vue3-migration spec ready **禁止**大规模改码
5. 自主执行至 verify PASS，中途不询问

## 流程

```
⓪ vue3-migration spec ready
① 预加载 rules + Read feature 工件
② 盘点 → docs/vue3-migration-inventory.md
③ 依赖 / main / App / store
④ 分批迁移 pages + subPackages
⑤ 每批编译 + 更新 tasks + e2e 冒烟
⑥ 【verify】vue3-migration
```

## uni-app 特别注意

- 条件编译保持不变
- 微信小程序实机验证（e2e.md）
- 自定义 tabBar 嵌入页单独记录于 design

## 与 rules-refactor

| 场景 | slug | Skill |
|------|------|-------|
| 不升栈，只规范 | `project-refactor` | `rules-refactor` |
| Vue2→Vue3 | `vue3-migration` | **本 Skill** |

---

## 触发话术

```
【spec】propose vue3-migration
【vue3】按 tasks 迁移，功能不变
【verify】vue3-migration
```
