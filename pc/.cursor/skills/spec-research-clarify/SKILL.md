---
name: spec-research-clarify
version: 1.0.1
description: 识别复杂需求歧义与风险，生成优先级澄清问题并记录 research.md。 需求调研、方案评审或 feature-dev 判定高复杂度时触发。
---
# 需求调研与澄清

> **管控力度：** 松 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

## 目标

在编码前消除关键歧义，降低返工风险。适用于：多模块联动、权限不清、接口未定义、复杂工作台类页面。

## 步骤

1. 调研现有实现模式，生成 `research.md`
2. 向用户提问澄清（每次 1 题，最多 5 题）
3. 记录用户决策，更新 `research.md`
4. 汇报完成 → [feature-spec](../feature-spec/SKILL.md) 写入 `spec.md` §决策记录，或进入 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ②

## 步骤 1：生成 research.md

存放路径（按优先级）：

1. 用户指定的目录
2. `docs/research/<feature-name>.md`
3. `.cursor/research/<feature-name>.md`

格式：

```markdown
# <功能名> 调研记录

## 决策
- Decision: ...
- Rationale: ...
- Alternatives considered: ...

## 待确认（已解决）
- Q: ... → A: ...
```

## 步骤 2：澄清提问

**Blocker 分级（团队约定）：**

| Blocker（未决禁止 ready） | 非 blocker（标 `[待确认-低]`） |
|---------------------------|-------------------------------|
| 路由 path 未定义 | 页面类型未定义 |
| 主列表/提交接口 URL 未知 | 按钮文案 |
| 所属业务模块未定义 | 列宽 / 样式细节 |
| 权限模型与现网不一致且无决策 | 非核心字段展示格式 |
| 与现有页面冲突 | |

按以下分类扫描覆盖度（内部使用，不全量输出）：

- 功能范围与行为
- 数据模型与状态流转
- 交互与 UX（含空/错/loading）
- 接口与外部依赖
- 权限与安全
- 边界与失败处理

**提问规则：**

- 每次只问 **1 个问题**
- 最多 **5 个问题**
- 每题提供推荐选项 + 简短理由
- 只问会影响架构、数据模型、页面拆分、权限、验收标准的题
- 用户说「done」「继续」时停止提问

**推荐格式：**

```markdown
**推荐：** 选项 B — 双栏页按区块拆分 hook，便于独立 loading 与维护。

| 选项 | 说明 |
|------|------|
| A | 单文件实现 |
| B | 双栏 + 独立 hook（推荐） |
| C | 双路由拆分 |

回复选项字母，或说「推荐」采纳推荐项。
```

## 步骤 3：记录决策

用户回答后写入 `research.md` 的「决策」与「待确认（已解决）」章节。

## 步骤 4：完成汇报

- 提问数量与关键决策
- `research.md` 路径
- 建议下一步：进入 feature-dev-workflow 阶段 ② 输出文件清单

## 行为规则

- 无关键歧义时：回复「无需要正式澄清的关键歧义」，直接进入方案对齐
- 不超过 5 题；单题追问不计入新题
- 尊重用户提前终止（「停止」「先做」）
- 配额用尽仍有高影响未决项 → 标注 Deferred 并说明风险

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 产出澄清问题与决策记录
- 🚫 代替用户做 blocker 业务决策

## 交付检查

- [ ] research.md / clarify-log 已更新
