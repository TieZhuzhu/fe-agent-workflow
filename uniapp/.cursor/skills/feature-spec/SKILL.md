---
name: feature-spec
version: 1.2.1
description: 产出 SDD 提案工件（proposal、spec、design、tasks、field-map）。 用户说【spec】、propose、先出方案再编码时触发；复杂新建须在 feature-dev-workflow 之前执行。
---
# Feature Spec（Propose）

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 对应 OpenSpec `/opsx:propose`、Spec-Kit `/speckit.specify` + `/speckit.plan`。**写码前**落盘规格，避免需求只在聊天里。

## 触发场景

- `【spec】propose product-detail`
- 「先写 spec / 方案再开发」
- 新建页 / 多文件 feature，用户未提供 feature 目录
- `feature-dev-workflow` 判定为**新建且非 trivial**（多接口、多页、复杂页）

**不触发：** 单文件增量（`incremental-feature`）、bugfix、**单页** `code-normalize`。

**全项目重构须触发（固定 slug）：** `【spec】propose project-refactor` — 见 [rules-refactor](../rules-refactor/SKILL.md)。

**Vue2→Vue3 须触发（固定 slug）：** `【spec】propose vue3-migration` — 见 [vue2-to-vue3-refactor](../vue2-to-vue3-refactor/SKILL.md)；与 project-refactor 互斥。

---

## 流程

```
① 读输入 → ② 澄清（可选）→ ③ 创建 feature 目录 → ④ 填工件 → ⑤ 评审门禁 → ⑥ 进入 implement
```

### ① 必读

1. [docs/constitution.md](../../../docs/constitution.md)
2. [docs/features/README.md](../../../docs/features/README.md)
3. [docs/features/_template/](../../../docs/features/_template/) 各模板
4. 用户 PRD / Figma / OpenAPI / 截图 / **语雀 Markdown** / **Axure 原型站 URL**
5. `.cursor/project-conventions.md`（若存在，对齐 request / 分包）

**PRD 接入分支：**

| 材料 | Skill |
|------|-------|
| 语雀 / 飞书 Markdown 粘贴 | [prd-markdown-ingest](../prd-markdown-ingest/SKILL.md) |
| 其他 PRD 文案 / 截图 | [prd-feature-dev](../prd-feature-dev/SKILL.md) |
| 远程 / 本地 HTML 原型 | [prototype-html-feature-dev](../prototype-html-feature-dev/SKILL.md) |

**交互原型（选券、开票、弹层、跨页）：** `prototype-html-feature-dev` §F — curl 批量 + Browser MCP P0 实点 → `e2e.md`。

### ② 澄清（复杂时）

执行 [spec-research-clarify](../spec-research-clarify/SKILL.md)，产出 `clarify-log.md`（模板 [docs/features/_template/clarify-log.md](../../../docs/features/_template/clarify-log.md)），决策同步写入 `spec.md` §决策记录。

**Blocker 级待确认（任一项未决 → 禁止 `Status: ready`）：**

| 类型 | 示例标记 |
|------|----------|
| pages.json path 未定义 | `path: [待确认]`、`路由未定义`、`pages.json 未注册` |
| 主列表/提交接口 URL 未知 | `接口 URL 未知`、`接口待后端` |
| 所属子包/模块未定义 | `模块未定义`、`子包未定义` |
| 与现有页面冲突 | `重复 path`、`重复功能` |

**非 blocker（不阻断 ready，须标 `[待确认-低]`）：**

- 页面类型未定义（列表/表单/详情/复杂）
- 按钮文案、样式细节、非核心字段展示格式

**门禁：**

- blocker 级 `[待确认]` **> 0** → 禁止 `ready`
- 可跑 `python3 .cursor/skills/scripts/feature-check.py spec <slug>` 校验

### ③ 创建目录

```
docs/features/<feature-slug>/
├── proposal.md
├── spec.md
├── design.md
├── tasks.md
├── field-map.md    # 无接口时可写「N/A - 无联调」
├── status.yaml     # workflow 状态（sync-status 维护）
└── e2e.md          # 可选；P0 新建页建议，供 feature-e2e-verify
```

`<feature-slug>`：kebab-case，建议 `<module>-<page>`，如 `product-detail`。

### ④ 填写要点

**proposal.md**

- 背景、In/Out Scope、成功标准
- `Status: draft` → 评审通过后改为 `ready`

**spec.md**

- 用户故事、FR 表、Given/When/Then 验收场景
- 至少 1 条主流程 + 1 条空态/错误场景
- P0 新建页：同步起草 `e2e.md`（模板 `docs/features/_template/e2e.md`）供后续 `feature-e2e-verify`
- **交互原型来源**：`prototype-html-feature-dev` §F5 清单裁剪写入 `e2e.md`；`research.md` 记录 JS 行为摘要

**design.md**

- 页面类型、**path ↔ 目录**（见 [route-permission](../route-permission/SKILL.md)）
- `pages.json` 注册项（主包/分包 root + path）
- 文件清单、接口表、布局组件

**tasks.md**

- 从模板复制，按 design 拆可勾选任务

**field-map.md**

- 有接口时：Query / Item / Form 映射表
- 有 OpenAPI → 优先 [openapi-api-integration](../openapi-api-integration/SKILL.md) 填字段

### ⑤ 评审门禁（ready）

- [ ] `design.md` 含 path、目录、页面类型（或标注全项目治理）
- [ ] `spec.md` 含 ≥1 验收场景
- [ ] `tasks.md` 已生成
- [ ] 有接口时 `field-map.md` 非空
- [ ] blocker 级待确认 = 0（见 §②）
- [ ] `python3 .cursor/skills/scripts/feature-check.py analyze <slug>` **PASS**
- [ ] `python3 .cursor/skills/scripts/feature-check.py spec <slug>` PASS
- [ ] `proposal.md` → `Status: ready`
- [ ] `status.yaml` 已创建（`feature-check sync-status <slug>`）

### ⑥ 下一步

告知用户：

```
Spec 已就绪：docs/features/<slug>/
下一步：【analyze】<slug> → 【新建】… 或继续 feature-dev-workflow 阶段 ③
```

---

## 与 feature-dev-workflow 的关系

| feature-dev 阶段 | 本 Skill |
|------------------|----------|
| ① 理解需求 | 产出 proposal + spec 摘要 |
| ② 方案对齐 | **design.md + tasks.md 为权威** |
| ③ 写码 | 须 Read 本 feature 目录 |
| ④ 验收 | 交 [feature-verify](../feature-verify/SKILL.md) |

**新建页默认路径：** `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `feature-verify` → `feature-finish` → `feature-archive`

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 创建/更新 docs/features/<slug>/ 工件
- ⚠️ blocker 未澄清不得标 ready
- 🚫 在 spec 中编造未确认的接口字段

## 交付检查

**汇报内容**

1. Feature 目录路径
2. proposal Status
3. 待确认项列表
4. 建议的【新建】话术（含 path、子包、页面类型）

**门禁**

- [ ] 运行 `feature-check spec <slug>`
- [ ] 复杂需求已产出 clarify-log / research
