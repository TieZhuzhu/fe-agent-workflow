# 主 Spec 库

已上线 / 已归档功能的**现状描述**，作为系统行为真相源。

## 与 `docs/features/` 的关系

| 目录 | 用途 |
|------|------|
| `docs/features/<slug>/` | 进行中的变更（proposal → tasks） |
| `docs/specs/<module>/<page>.md` | 归档后合并的**当前行为** spec |

## 索引

运行 `python3 .cursor/skills/scripts/spec-index.py` 生成 [`_index.md`](./_index.md)：

- pages.json path ↔ 页面文件 ↔ 主 spec 状态
- 缺失 spec 缺口清单

## 归档流程

由 [feature-archive](../.cursor/skills/feature-archive/SKILL.md) 执行：

1. `feature-check archive-ready <slug>` PASS
2. 按 **Delta 合并算法** 将 feature spec 合并到 `docs/specs/`
3. 将 feature 目录移至 `docs/features/archive/<date>-<slug>/`
4. 运行 `spec-index.py` 刷新索引

## 文件命名

```
docs/specs/
├── product/
│   └── detail.md
├── order/
│   └── list.md
└── ...
```

## Spec 文件最小结构

```markdown
# <页面名>

> pages.json path: `subPackages/product/detail` | 更新: YYYY-MM-DD

## 能力摘要
## 验收场景（当前行为）
## 接口索引
## 变更历史
```

## Delta 合并（增量归档）

归档时生成 Delta 段，禁止整文件覆盖已有主 spec：

```markdown
## Delta (YYYY-MM-DD, <slug>)

### ADDED
- FR-x: ...

### MODIFIED
- 场景 1: ...

### REMOVED
- ...
```
