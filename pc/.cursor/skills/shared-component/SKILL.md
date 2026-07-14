---
name: shared-component
version: 1.0.1
description: 封装跨模块 UI 公共组件至顶层 components/；同模块多页放 views/<module>/components/。 用户说跨模块封装、封装公共组件、多个模块共用、提取组件时触发。
---
# 公共组件开发

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **本 Skill：** 跨模块 UI → 顶层 `components/`。
> **同模块多页** → `views/<module>/components/`（不走本 Skill）。
> **纯逻辑** → `hooks/` / `utils/`（不走本 Skill）。
>
> 示例、目录模板、完整验收见 [reference.md](./reference.md)（**按需 Read，非预加载**）。

---

## 何时创建 / 放置位置

| 场景 | 放置位置 | 走哪个 Skill |
|------|----------|--------------|
| 仅当前页面（UI） | `views/<module>/<page>/components/` | page-refactor |
| 同模块多页（UI） | `views/<module>/components/` | 模块规范 |
| **跨模块（UI）** | **`components/<Name>/`** | **本 Skill** |
| 纯函数 / 无 UI | `hooks/` 或 `utils/` | 不走本 Skill |

提升路径：`页面 components/` → `views/<module>/components/` → `components/`（逐级，禁止跳级）。

跨模块 `components/` 须满足：**>=2 个不同业务模块**复用、无模块专属接口绑定、Grep 无重复。

---

## 流程

```
① 预加载 -> ② 确认层级 -> ③ 调研 -> ④ 定义 API -> ⑤ 实现 -> ⑥ 导出
```

### ① 规范预加载

Read [rules-activation.md](../shared/rules-activation.md) + 本文件。Vue 3/2 指南按版本选读。复杂实现再 Read [reference.md](./reference.md)。

### ② 确认层级

交付首行：`组件层级：页面 / 模块 / 跨模块 / hooks|utils`

### ③ 调研

Grep 顶层 `components/` 与 `views/<module>/components/`，禁止 duplicate。

### ④ 定义 API

先输出 Props / Events 表；Props 不带组件名前缀。

### ⑤ ⑥ 实现与导出

- Vue 3：类型 `types.ts`，枚举 `constants.ts`
- 不写页面级 services；示例见 reference.md
- 更新 `components/index` 或模块 `components/index` 导出

---

## 与 page-refactor 区别

| | page-refactor | 模块 components | shared-component |
|--|---------------|-----------------|------------------|
| 复用 | 单页 | 同模块多页 | 跨模块 |
| 位置 | 页面 `components/` | `views/<module>/components/` | `components/` |

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 确认跨模块复用后再提升顶层
- 🚫 业务页面逻辑塞进公共组件

## 交付检查

**汇报内容**

1. 组件层级 + 规范预加载
2. 文件列表 + Props/Events 表
3. import 路径 + TODO

**门禁**

- [ ] 组件 API 已文档化
- [ ] `npm run lint-fix`
