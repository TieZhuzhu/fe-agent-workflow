---
name: feature-archive
version: 1.1.1
description: 将已验收 spec 合并至 docs/specs/ 并归档 docs/features/<slug>/。 用户说【archive】、功能上线归档时触发；须 feature-verify PASS 后执行。
---
# Feature Archive

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 对应 OpenSpec `/opsx:archive`、Spec-Kit 归档 + spec 回写。关闭变更循环，保留审计痕迹。

## 触发场景

- `【archive】product-detail`
- feature-verify 已 PASS
- 功能已合并 / 准备发布

**不触发：** verify FAIL；无 `docs/features/<slug>/` 目录。

---

## 前置条件

- [ ] [feature-verify](../feature-verify/SKILL.md) 报告 **PASS**
- [ ] `proposal.md` 可改为 `Status: implemented`
- [ ] 用户确认归档（或 verify PASS 且用户明确说 archive）

---

## 流程

```
① 确认 PASS → ② 合并主 spec → ③ 移动 feature 目录 → ④ 更新 proposal → ⑤ 汇报
```

### ① 确认

Read 最近 verify 报告或运行：

```bash
python3 .cursor/skills/scripts/feature-check.py archive-ready <slug>
```

须 PASS 后再归档。

### ② 合并到 docs/specs/

从 `design.md` 取 module / page-dir，写入：

```
docs/specs/<module>/<page-dir>.md
```

**合并算法（默认，对齐 OpenSpec Delta）：**

1. 若主 spec **不存在** → 新建全文 + 变更历史首行
2. 若主 spec **已存在** → **禁止整文件覆盖**，按 Delta 段合并：
   - `### ADDED` → 追加到「能力摘要」「验收场景」
   - `### MODIFIED` → 按**场景标题**或 **FR 编号**替换对应条目
   - `### REMOVED` → 删除或标注 `deprecated`
   - 变更历史表追加一行
3. 合并完成后运行 `python3 .cursor/skills/scripts/spec-index.py` 刷新索引
4. `feature-check sync-status <slug> --set archived`

内容结构（新建时）：

```markdown
# <页面标题>

> pages.json path: `subPackages/product/detail` | 更新: YYYY-MM-DD | Feature: <slug>

## 能力摘要
<!-- 从 spec.md FR + 用户故事提炼 -->

## 验收场景（当前行为）
<!-- 从 spec.md 复制已实现的场景 -->

## 接口索引
<!-- 从 design.md + field-map.md 提炼 -->

## 变更历史

| 日期 | Feature | 说明 |
|------|---------|------|
| YYYY-MM-DD | <slug> | 初始 / 增量描述 |
```

若主 spec 已存在 → 使用上文 **合并算法**，不重复粘贴此模板全文。

### ③ 归档 feature 目录

```
docs/features/<slug>/  →  docs/features/archive/YYYY-MM-DD-<slug>/
```

日期用当天 `YYYY-MM-DD`。

### ④ 更新 proposal

归档前将 `proposal.md` 中 `Status: implemented`。

### ⑤ 汇报

```markdown
## Archive 完成

- Feature: <slug>
- 主 spec: docs/specs/<module>/<page>.md
- 归档: docs/features/archive/YYYY-MM-DD-<slug>/
```

---

## Delta 标记（归档默认）

合并 spec 时**必须**生成 Delta 段（对齐 OpenSpec ADDED/MODIFIED/REMOVED）：

```markdown
## Delta (YYYY-MM-DD, <slug>)

### ADDED
- FR-x: ...

### MODIFIED
- 场景 1: ...

### REMOVED
- ...
```

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ Delta 合并 spec、运行 spec-index.py
- 🚫 verify 未 PASS 合并主库

## 交付检查

**交付首行：** `Feature Archive: <slug> | spec → docs/specs/<module>/<page>.md | archived`

**门禁**

- [ ] `feature-check archive-ready <slug>`
- [ ] `spec-index.py` 已刷新
