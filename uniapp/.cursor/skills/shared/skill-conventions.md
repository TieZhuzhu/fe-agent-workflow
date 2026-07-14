# Skill 编写规范（团队标准）

> 对齐 [Agent Skills 开放规范](https://agentskills.io/specification) 与《前端如何写出优秀的 AI Agent Skills》10 条原则。  
> **所有 SKILL.md 须符合本节；细则见各 Skill 正文。**

---

## SKILL.md 结构（强制）

```markdown
---
name: kebab-case-name          # 与目录名一致
version: x.y.z
description: 第三人称。能力 + 触发场景 + 关键词（≤1024 字符）
---

# 标题

> 管控力度：严|中|松 | 边界：[skill-boundaries-baseline](skill-boundaries-baseline.md) | 工具：[project-toolbox](project-toolbox.md)

## 何时使用 / 何时不用
## 流程（编号清单）
## 操作边界（✅ ⚠️ 🚫，Skill 特有项）
## 交付检查（汇报内容 + 门禁 checklist，唯一交付节）
## 禁止
```

---

## description 写法（Agent 匹配关键）

| 规则 | ✅ | ❌ |
|------|----|----|
| 第三人称 | 「生成 Vue 列表页…」「对照 spec 验收…」 | 「我可以帮你…」「帮你写…」 |
| 能力 + 时机 | 「…Use when 用户说【spec】、propose…」 | 「Helps with Vue stuff」 |
| 触发词 | 【新建】【增量】【bug】【verify】、联调、Swagger | 无场景词 |
| 不重复正文 | 只写何时触发，不写完整流程 | 在 description 里列 5 步流程 |

---

## 管控力度（原则二）

| 力度 | 适用 Skill 类型 | Agent 自由度 |
|------|-----------------|-------------|
| **严** | archive、rules-refactor、vue2→vue3、route path、analyze ready 门禁 | 按步骤执行，不跳步 |
| **中** | 新建页、增量、联调、codegen、normalize | 模板 + 规范，细节可调 |
| **松** | review、clarify、截图分析 | 给方向，方案灵活 |

每个 Skill 正文首行 `> 管控力度：` 必填。

---

## 渐进式加载（原则三）

| 层级 | 放哪 | 限制 |
|------|------|------|
| L1 | frontmatter `name` + `description` | ~100 词 |
| L2 | SKILL.md 正文 | **≤500 行**；超则拆 `references/` |
| L3 | `references/`、`scripts/`、`.cursor/components/` | 按需 Read；**引用仅一层深** |

**交付章节：** 只用 `## 交付检查` 一节，内含「汇报内容」+ 门禁 checklist；**禁止**再单独写 `## 交付说明` / `## 交付` 重复同一清单。

**禁止预加载：** `代码规范示例参考.mdc`、过大 `reference.md`（见 rules-activation）。

---

## 操作边界（原则五）

通用基线：[skill-boundaries-baseline.md](skill-boundaries-baseline.md)  
每个 Skill **追加**本场景特有 ✅⚠️🚫，不重复抄全文。

---

## 项目工具箱（原则七、十）

确定性操作用脚本，不手写：

| 脚本 | 用途 |
|------|------|
| `scripts/feature-check.py` | spec / analyze / verify / board |
| `scripts/spec-index.py` | 路由↔spec 索引 |
| `scripts/skills-version.py` | Skill 版本校验 |

清单：[project-toolbox.md](project-toolbox.md)

---

## 交付检查（原则八）

写码类 Skill 交付前须汇报：

```
规范预加载：Vue x | 页面类型 | Skill xxx | 已读 rules ×N | request 路径
```

Feature 类须衔接 `feature-check verify` 或对应子命令。  
详见各 Skill §交付检查 与 [rules-activation §质量红灯](rules-activation.md)。

---

## 与 Rules 分工（原则一）

| 写什么 | 放哪 |
|--------|------|
| 团队潜规则、Vue 写法、目录结构 | `.cursor/rules/*.mdc` |
| 什么时候做什么、步骤、边界 | `.cursor/skills/*/SKILL.md` |
| 项目扫描事实（request 路径） | `project-conventions.md` |
| 进行中需求 | `docs/features/<slug>/` |

**Skill 不重复教** React/Vue 基础语法；只写流程与边界。
