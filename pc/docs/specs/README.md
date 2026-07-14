# 主 Spec 库

已上线 / 已归档功能的**现状描述**，作为系统行为真相源。

## 与 `docs/features/` 的关系

| 目录 | 用途 |
|------|------|
| `docs/features/<slug>/` | 进行中的变更（proposal → tasks） |
| `docs/specs/<module>/<page>.md` | 归档后合并的**当前行为** spec |
| **`docs/specs/_index.md`** | **路由 ↔ 视图 ↔ spec 缺口索引**（`spec-index.py` 生成） |

刷新索引：

```bash
python3 .cursor/skills/scripts/spec-index.py
```

## 归档流程

由 [feature-archive](../.cursor/skills/feature-archive/SKILL.md) 执行：

1. 将 `docs/features/<slug>/spec.md` 合并到 `docs/specs/`
2. 将 feature 目录移至 `docs/features/archive/<date>-<slug>/`
3. 更新 spec 内 `Status: archived`

## Delta 合并（archive 默认）

对齐 OpenSpec `ADDED` / `MODIFIED` / `REMOVED`：

| Delta 段 | 合并到主 spec |
|----------|---------------|
| ADDED | 追加「能力摘要」「验收场景」 |
| MODIFIED | 按场景标题或 FR 编号替换条目 |
| REMOVED | 删除或标 `deprecated` |
| 变更历史 | 表末追加一行 |

禁止整文件覆盖已有主 spec。详见 [feature-archive](../.cursor/skills/feature-archive/SKILL.md)。

## 文件命名

```
docs/specs/
├── product/
│   └── tag-list.md
├── order/
│   └── list.md
└── ...
```

## Spec 文件最小结构

```markdown
# <页面名>

> 路由: `/module/page-dir` | 更新: YYYY-MM-DD

## 能力摘要
## 验收场景（当前行为）
## 接口索引
## 变更历史
```
