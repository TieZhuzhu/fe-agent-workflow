# Cursor Skills 索引（uni-app 移动端）

**Bundle 1.3.3** | **适用范围：uni-app 项目（H5 / 小程序 / App）。** Vue 2 / Vue 3 按 `package.json` 判定，禁止混用。

**写码前强制预加载：** [shared/rules-activation.md](shared/rules-activation.md)

**Skills 版本：** [manifest.json](manifest.json) · [CHANGELOG.md](CHANGELOG.md) · `python3 scripts/skills-version.py check`

**Skill 编写标准（维护者）：** [skill-conventions](shared/skill-conventions.md) · [skill-creator](skill-creator/SKILL.md) · [project-toolbox](shared/project-toolbox.md) · `python3 scripts/skill-standardize.py`

**推荐 SDD 全链路：** `【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】`（详见 [agent-workflow-roadmap.md](../../docs/agent-workflow-roadmap.md)）

---

## 首次接入

```
扫描项目约定，生成 project-conventions.md
```

产出 [project-bootstrap](project-bootstrap/SKILL.md) → `.cursor/project-conventions.md`

---

## Skill 自动路由

| 意图关键词 | Skill |
|------------|-------|
| **新建**、PRD、Figma（内容区百分百还原） | `feature-dev-workflow` |
| **增量**、加字段、加按钮 | `incremental-feature` |
| **联调**、Swagger、OpenAPI | `openapi-api-integration` / `api-integration` |
| **bug**、报错、不生效 | `bugfix-workflow` |
| **拆分**、文件太大 | `page-refactor` |
| **全项目重构** | `rules-refactor` |
| **Vue2 升 Vue3** | `vue2-to-vue3-refactor` |
| **优化**、规范化 | `code-normalize` |
| **review** | `code-review` |
| **路由**、pages.json | `route-permission` |
| **CI/build 失败** | `ci-fix` |
| **lint** | `lint-check` |
| **spec / analyze / verify / finish / archive** | `feature-spec` / `feature-analyze` / `feature-verify` / `feature-finish` / `feature-archive` |
| **verify-e2e** | `feature-e2e-verify` |
| **api-smoke** | `api-smoke` |
| bootstrap | `project-bootstrap` |
| **跨模块组件** | `shared-component` |
| **新建 skill**、创建 skill、优化 skill description | `skill-creator` |

---

## 黄金路径

### 1. 首次接入

```
扫描项目约定，生成 project-conventions.md
```

### 2. SDD 提案

```
【spec】propose product-detail。商品详情页，分包 subPackages/product，列表点进详情。附接口文档
【analyze】product-detail
```

### 3. 新建页面

```
【新建】按 docs/features/product-detail/ 实现商品详情页
```

或快捷：

```
【新建】按 PRD 开发优惠券列表。子包 coupon，页面类型列表页。附接口
```

### 4. 增量

```
【增量】在 subPackages/order/list 加「待评价」Tab 筛选
```

### 5. 注册路由

```
【路由】新建积分明细页，子包 user，path integral-log
```

### 6. 验收与收尾

```
【verify】product-detail
【finish】product-detail
【archive】product-detail
```

**看板：**

```bash
python3 .cursor/skills/scripts/feature-check.py board
```

---

## 开发工作流

```
feature-spec → feature-analyze → feature-dev-workflow → feature-verify → feature-finish → feature-archive
                    ↓
              vue-page-codegen
              route-permission
              api-integration
```

**工具箱：** [shared/project-toolbox.md](shared/project-toolbox.md) | **边界：** [shared/skill-boundaries-baseline.md](shared/skill-boundaries-baseline.md)

---

## Rules 索引

| 规则 | 用途 |
|------|------|
| `前端通用代码规范.mdc` | **Always Apply** |
| `uniapp代码生成指南.mdc` | uni-app 主指南 |
| `Vue代码生成指南.mdc` | Vue 3 |
| `Vue2代码生成指南.mdc` | Vue 2 |
| `项目结构与命名规范.mdc` | 目录 |
| `路由与分包规范.mdc` | pages.json / 主包分包 |
| `接口对接规范.mdc` | 联调 |
| `JavaScript/HTML/TypeScript` | 按页面类型 |
| `代码规范示例参考.mdc` | 仅查阅 |

---

## 质量红灯

| 红灯 | 说明 |
|------|------|
| 非 tabBar 入主包 | 违反分包规范 |
| Vue2/3 混用 | 版本判错 |
| 无预加载汇报 | 未走 rules-activation |
| 无 pages.json 注册 | 路由遗漏 |
| 新建无 spec 且未声明跳过 | 须 feature-spec |

---

## 权威来源

| 主题 | 文件 |
|------|------|
| **内核同步** | `docs/agent-kernel-sync.md` |
| Skill 路由 | **本 README** |
| 预加载 | `shared/rules-activation.md` |
| 编码约定 | `.cursor/rules/*.mdc` |
| 项目原则 | `docs/constitution.md` |
| Feature 规格 | `docs/features/<slug>/` |
| 项目扫描 | `.cursor/project-conventions.md` |
