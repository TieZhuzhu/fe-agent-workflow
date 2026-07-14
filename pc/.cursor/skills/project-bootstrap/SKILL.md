---
name: project-bootstrap
version: 1.1.1
description: 扫描 package.json、request 封装、路由、权限等真实约定，产出 project-conventions 与 spec 索引。 用户说扫描项目约定、bootstrap、对齐本项目配置、onboard 时触发。
---
# 项目约定扫描（Bootstrap）

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **在以下场景必须先执行本 Skill，再进入 feature-dev / vue-page-codegen / incremental-feature 等写码流程：**
>
> - 首次接入项目、用 Cursor 开发
> - 不存在 `.cursor/project-conventions.md` 或文件超过 30 天未更新且依赖栈有变更
> - 用户明确要求「对齐本项目」
> - Agent 无法从现有 `services.ts` 推断 request 路径或 UI 库版本
> - 需要刷新「有代码无 spec」缺口清单

---

## 目标

消除 rules/skills 中的**硬编码假设**（如 `@/config/request`、`tablePage.scss`），让后续生成代码与**当前项目扫描结果**一致。

**边界：** `project-conventions.md` 只记录扫描到的事实（技术栈、request、布局组件、路由文件位置等）。**权限模型、路由 path↔目录、接口对接、types 职责**等通用约定以 `.cursor/rules` 与 Skills 为准，bootstrap **不写入、不覆盖**这些规则。

---

## 流程

```
① 扫描关键文件 → ② 归纳约定 → ③ 写入 project-conventions.md
→ ④ 生成 docs/specs/_index.md → ⑤ 汇报摘要
```

### ① 扫描清单（按优先级 Read / Grep）

| 类别 | 扫描目标 | 提取内容 |
|------|----------|----------|
| 依赖栈 | `package.json` | vue / element-plus / element-ui / pinia / vuex / typescript / vite / webpack / **test script** |
| 构建 alias | `vite.config.*` / `vue.config.*` / `tsconfig.json` paths | `@`、`components`、`styles` 等 alias |
| 请求封装 | `src/**/request*.ts`、`src/config/request*`、任意 `services.ts` 的 import | request 默认 import 路径、响应解包结构、分页字段名 |
| 路由 | `router/index.*`、`router/modules/*.js`、`views/**/routes.ts` | 业务 path、component import、meta.title |
| 权限 | 菜单树接口、路由守卫、`beforeEach` | 菜单树结构；页面 path 拦截方式（rules 已定模型，此处只记录实现路径） |
| 样式 | `styles/tablePage.scss`、`styles/formPage.scss`、`src/styles/**` | 列表页/表单页 scss 路径（`@/` 或 `~styles/`） |
| 公共组件 | `components/HiTable`、`components/PageHead` 等 | 是否已接入 HiTable、PageHead 路径 |
| 列表分页 | 现有 HiTable / el-table 分页传参 | pageNo/pageSize 或 current/size 等 |
| 上传 | 现有 `el-upload` 用法、`Upload` 接口 | action URL、header 鉴权方式 |
| **Spec 缺口** | `docs/specs/` vs 路由表 | 有路由无 spec、进行中 feature |

**至少读取 2 个不同模块的 `services.js` / `services.ts`**，确认 request import 一致。

### ② 归纳约定

禁止猜测；扫描不到的项标注 `[待确认]`，并在交付中向用户提问。

**测试策略（必写）：**

| package.json 有 test script | project-conventions 写入 |
|-----------------------------|--------------------------|
| 否 | `testStrategy: pending` |
| 是 | `testStrategy: strict`（或团队约定的 `utils-only`） |

### ③ 输出文件 — project-conventions.md

写入 **`.cursor/project-conventions.md`**（可提交到仓库，供团队共享）：

```markdown
# 项目约定摘要

> 由 project-bootstrap 生成，日期：YYYY-MM-DD

## 技术栈
...

## 测试策略
| 项 | 值 |
|----|-----|
| testStrategy | pending / strict |
| test script | npm run test:unit / 无 |

## Spec 索引
- 路径: docs/specs/_index.md
- 刷新: python3 .cursor/skills/scripts/spec-index.py
```

### ④ 输出文件 — Spec 索引（P1-5）

**执行 CLI：**

```bash
python3 .cursor/skills/scripts/spec-index.py
```

产出 **`docs/specs/_index.md`**，包含：

| 列 | 说明 |
|----|------|
| 模块 | views 一级目录 |
| 路由 path | `router/modules` 扫描结果 |
| 视图目录 | `src/views/...` |
| 主 spec | `docs/specs/<module>/<page>.md` |
| 状态 | 已归档 / 进行中 / **缺失** |
| 进行中 feature | `docs/features/<slug>/` 匹配 |

**可选门禁：**

```bash
python3 .cursor/skills/scripts/spec-index.py --check   # 有缺失 spec → exit 1
```

**用途：**

- onboard：新同学一眼看到「哪些页有 spec、哪些缺口」
- 新建页：避免重复 path
- archive 后：重新跑 spec-index 刷新状态

### ⑤ 交付检查

**交付首行：** `项目约定：已扫描 | Vue 2 + Element UI | request @/config/request | spec-index 已刷新 | 详见 .cursor/project-conventions.md`

**汇报内容**

1. `docs/specs/_index.md` 统计（路由数 / 缺失 spec 数）
2. `testStrategy` 当前值
3. 待确认项

**门禁**

- [ ] `project-conventions.md` + spec-index 已生成

---

## 与 rules-activation 的关系

Bootstrap **不替代** rules-activation，而是为其提供**项目级变量**：

| rules-activation 默认假设 | bootstrap 后 |
|---------------------------|--------------|
| request → `@/config/request` | 以 `project-conventions.md` 为准 |
| tablePage / formPage 路径 | 以扫描结果为准 |
| Element Plus | 若为 Element UI 则触发 Vue 2 路径 |

后续所有 Skill 写码前：

1. Read `.cursor/project-conventions.md`（存在则优先）
2. Read `shared/rules-activation.md`
3. 按页面类型 Read 对应 rules

---

## 触发后禁止

- 未扫描就直接用 rules 里的默认路径写码
- 覆盖用户已手工维护且仍有效的 `project-conventions.md`（应先 Read 比对，仅更新变更项）
- 将 token、密钥写入 conventions 文件

---

## 维护

以下变更后应重新 bootstrap：

- 升级 vue / element / 构建工具 major 版本
- 更换 request 封装或响应结构
- 全局样式路径重构

**定期建议：** 每季度或 major 依赖升级后，运行一次 bootstrap 刷新 `.cursor/project-conventions.md`。

用户可说：「重新扫描项目约定」触发更新。

---

## 团队首次接入 Checklist

- [ ] 运行 bootstrap，提交 `project-conventions.md` 到仓库
- [ ] 确认 Vue 2 / Vue 3 与 conventions 中 UI 库一致
- [ ] 后续所有写码任务优先 Read conventions

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 只记录扫描事实，不覆盖 rules 通用约定
- 🚫 编造未验证的 request 路径
