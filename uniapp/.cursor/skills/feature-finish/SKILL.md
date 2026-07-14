---
name: feature-finish
version: 1.0.1
description: verify PASS 后产出 PR 描述、自检清单与 archive 提示。 用户说【finish】、验收通过准备合码时触发；须在 feature-verify PASS 后执行。
---
# Feature Finish（分支收尾）

> **管控力度：** 松 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 借鉴 Superpowers `finishing-a-development-branch`。verify 通过后的**交付包装**，不替代 verify / archive。

## 触发场景

- `【finish】<slug>`
- `feature-verify` 已 **PASS**
- 准备提 PR / 合码 / 上线前

**不触发：** verify FAIL；无 feature 目录。

---

## 前置条件

```bash
python3 .cursor/skills/scripts/feature-check.py verify <slug> --no-build
# 或完整 verify 已 PASS
```

---

## 流程

```
① 确认 verify PASS → ② 汇总变更 → ③ PR 描述 → ④ 自检清单 → ⑤ 更新 status → ⑥ 提示 archive
```

### ① 确认

- 最近 verify 报告 **PASS**，或 `feature-check verify` PASS
- `tasks.md` 主阶段项已勾完（backlog 除外）

### ② 汇总变更

从 git diff / 交付记录整理：

- 新增/修改文件列表（按子包/模块）
- `pages.json` path（若有）
- 接口列表（或 field-map 链接）
- Breaking / 待后端事项

### ③ PR 描述模板

```markdown
## Summary
- （1～3 条业务变更摘要）

## Feature
- Spec: `docs/features/<slug>/`
- 页面 path: `subPackages/product/detail`（若有）
- 接口: （或见 field-map.md）

## Verify
- [x] feature-verify PASS
- [x] lint 0 error（若项目有 lint script）
- [ ] build（若 verify 已跑则勾选）
- [ ] 人工冒烟（列出 3～5 步）

## Test plan
- [ ] 进入页面 → 主流程
- [ ] 筛选 / 提交 / 返回
- [ ] 与 spec 验收场景一致

## TODO / 后端
- [ ] 待后端接口就绪: `...`
```

### ④ 自检清单

- [ ] 无 `console.log`（业务代码）
- [ ] 无未使用 import
- [ ] 无 mock 残留（除非明确要求）
- [ ] `project-conventions.md` 与改动一致（request 路径等）
- [ ] 非 tabBar 页未入主包
- [ ] 规范预加载汇报已交付
- [ ] 增量范围外无无关重构

### ⑤ 更新 status

```bash
python3 .cursor/skills/scripts/feature-check.py sync-status <slug> --set done
```

### ⑥ 后续提示

```markdown
## 建议下一步
- 合码后：`【archive】<slug>`
- 可选：`【api-smoke】<slug>` / `【verify-e2e】<slug>`
- 刷新索引：`python3 .cursor/skills/scripts/spec-index.py`
```

---

## 与 feature-archive 的关系

| | feature-finish | feature-archive |
|---|----------------|-----------------|
| 时机 | verify PASS，合码前 | 上线/合码后 |
| 产出 | PR 描述 + 自检 | 合并 docs/specs/ + 移动目录 |

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 产出 PR body、合码检查清单
- 🚫 verify 未 PASS 时生成「可合并」结论

## 交付检查

**交付首行：** `Feature Finish: <slug> | verify PASS | PR 描述已生成 | 建议 【archive】`

**门禁**

- [ ] 确认 `feature-check verify` 已通过
- [ ] PR 描述与自检清单已产出（见上文 §③④）
