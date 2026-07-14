# Skill 脚手架模板

> 复制为 `.cursor/skills/<name>/SKILL.md` 起点，再按 [skill-conventions.md](../../shared/skill-conventions.md) 填写。

```markdown
---
name: <kebab-case-name>
version: 1.0.0
description: <第三人称。能力 + 触发场景 + 关键词。≤1024 字符>
---

# <中文标题>

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

## 何时使用

- …

## 何时不用

| 用户意图 | 改用 |
|----------|------|
| … | `other-skill` |

## 流程

按以下顺序执行，不要跳步：

1. …
2. …

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ …
- ⚠️ …
- 🚫 …

## 交付检查

**汇报内容**

1. …

**门禁**

- [ ] …

## 禁止

- …
```

## manifest.json 条目模板

```json
{
  "name": "<kebab-case-name>",
  "version": "1.0.0",
  "category": "workflow|ingest|codegen|integration|quality|maintenance|infra",
  "status": "stable",
  "description": "<一行中文索引说明>",
  "dependsOn": []
}
```

## 触发测试话术（至少 3 条）

| # | 用户话术 | 应触发 | 不应误触 |
|---|----------|--------|----------|
| 1 | | ✅ | |
| 2 | | ✅ | |
| 3 | | ❌ 应走 xxx | |
