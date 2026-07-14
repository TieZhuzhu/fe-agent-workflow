# Cursor Skills 索引

**主路径：Vue 3 + hooks + TypeScript + Element Plus。** `vue@2.x` 见 `Vue2代码生成指南.mdc`。

**写码前强制预加载：** [shared/rules-activation.md](shared/rules-activation.md)

**Skills 版本管理：** [manifest.json](manifest.json) · [CHANGELOG.md](CHANGELOG.md) · [shared/skills-versioning.md](shared/skills-versioning.md) · `python3 scripts/skills-version.py check`

**Skill 编写标准（维护者）：** [shared/skill-conventions.md](shared/skill-conventions.md) · [skill-creator](skill-creator/SKILL.md) · [skill-boundaries-baseline.md](shared/skill-boundaries-baseline.md) · [project-toolbox.md](shared/project-toolbox.md) · `python3 scripts/skill-standardize.py`

**推荐 SDD 全链路（新建页）：** `【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】`（详见 [agent-workflow-roadmap.md](../../docs/agent-workflow-roadmap.md)）

---

## 首次接入（必做一次）

```
扫描项目约定，生成 project-conventions.md
```

或：`bootstrap`、`对齐本项目配置`

产出 [project-bootstrap](project-bootstrap/SKILL.md) → `.cursor/project-conventions.md`，后续写码优先 Read。**major 依赖升级后重新扫描。**

---

## 零、Skill 自动路由

Agent 应根据用户意图自动选用 Skill（用户无需说出文件名）：

| 意图关键词 | Skill |
|------------|-------|
| **新建**、按 PRD、按 Figma、按原型、从零 | `feature-dev-workflow` |
| **语雀 PRD**、Markdown 粘贴、飞书文档 | `prd-markdown-ingest` → `feature-dev-workflow` |
| **Axure 原型链接**、远程原型站、index.html# | `prototype-html-feature-dev`（curl ingest；**含交互**时 + Browser MCP P0） |
| **增量**、已有页、加一个、补字段、加一列 | `incremental-feature` |
| **联调**、对接接口、字段对一下、Swagger、**OpenAPI** | `openapi-api-integration`（有 spec）或 `api-integration` |
| **bug**、报错、异常、不生效、**点击没反应** | `bugfix-workflow`（MCP 可用时实点；否则静态读码+用户证据） |
| **拆分**、太大、拆页面、提取子组件 | `page-refactor` |
| **全项目重构**、按 rules 重构全部代码 | `rules-refactor` |
| **Vue2 升 Vue3** | `vue2-to-vue3-refactor` |
| **优化**、规范化、整理代码（单页/模块） | `code-normalize` |
| **review**、检查规范 | `code-review` |
| **路由**、注册页面路由、新 path | `route-permission` |
| **build/test 挂了**、CI 失败 | `ci-fix` |
| **lint**、eslint、未使用引入 | `lint-check` |
| **单测**、test:unit、写测试 | `unit-test-codegen` |
| **spec**、propose、先写规格 | `feature-spec` |
| **analyze**、artifact 一致性 | `feature-analyze` |
| **verify**、验收 feature | `feature-verify` |
| **finish**、PR 收尾 | `feature-finish` |
| **verify-e2e**、UI 冒烟、浏览器验收 | `feature-e2e-verify` |
| **api-smoke**、curl 探针、验证响应格式 | `api-smoke` |
| **archive**、归档 spec | `feature-archive` |
| bootstrap、扫描项目约定 | `project-bootstrap` |
| **跨模块**封装、多个模块共用 | `shared-component` |
| **新建 skill**、创建 skill、优化 skill description | `skill-creator` |
| **vue2**、Vue 2 项目 | 判定后读 `Vue2代码生成指南.mdc` |

**话术技巧：** 首句带上 **场景词**（**spec** / **analyze** / 新建 / 增量 / 联调 / verify / **finish** / **archive** / **优化** / bug / vue2），可显著提高 Skill 路由准确率。

---

## 黄金路径（固定话术，推荐复制）

### 1. 首次接入

```
扫描项目约定，生成 project-conventions.md
```

### 2. SDD 提案（新建页推荐）

```
【spec】propose product-tag-list。按 PRD 开发商品标签列表，模块 product，path /product/tag-list，列表页。附件：接口文档
```

**语雀 PRD：**

```
【spec】propose mini-goods-detail。语雀 PRD 如下：（粘贴 Markdown 全文）
```

**Axure 原型站：**

```
【spec】propose mini-goods-detail。原型：http://host/小程序商城/index.html 。附 PRD / 接口（若有）
```

### 2b. Artifact 分析（implement 前，推荐）

```
【analyze】product-tag-list
```

`feature-check analyze` 通过（CRITICAL=0）且 `proposal.md` 为 `Status: ready` 后，再进入【新建】。

### 3. 新建列表页（Vue 3）

```
【新建】按 docs/features/product-tag-list/ 实现商品标签列表页
```

或跳过 spec 的快捷路径：

```
【新建】按 PRD 开发商品标签列表页。模块 product，路由 /product/tag-list。页面类型：列表页。附件：接口文档
```

### 4. 增量改页

```
【增量】在 views/product/tag-list 加「状态」筛选和表格列，接口字段 status / statusDesc
```

### 5. 接口联调

```
【联调】接口文档更新了，帮我对接 product/tag-list 列表字段，附件 swagger
```

### 5b. OpenAPI / Swagger spec 联调

```
【联调】按 OpenAPI 对接 order/list，spec 路径 docs/openapi/order.yaml
```

或：粘贴 Swagger URL / 上传 `openapi.json`

### 6. Vue 2 项目

```
【vue2】【新建】在 order 模块新建退款列表页，Options API，Element UI
```

### 7. 按规范优化现有页（单页/模块）

```
【优化】按规范整理 views/product/list，全量对齐 rules（types、HiTable、hooks、写法）
```

### 7b. 全项目 Rules 重构（自主闭环，不中途询问）

```
【重构】全项目按 .cursor/rules 规范重构，Vue2 保持不变，功能不变，改完 review 循环直到全部合规，中途不要问我是否继续
```

### 7c. Vue2 → Vue3 升级

```
【vue3】全项目从 Vue2 升 Vue3，功能不变，按 rules 改完并 review 到全部通过
```

### 8. 修 Bug

```
【bug】product/tag-list 筛选后表格不刷新，帮我排查修复
```

### 9. 新页面注册路由

```
【路由】新建商品标签列表页，path /product/tag-list，待后端在「商品-基础资料」下配菜单
```

### 10. 构建 / 测试 / Lint

```
【ci】pnpm test 挂了，帮我修到全绿
```

```
【lint】跑 eslint，修未使用引入
```

### 11. Feature 验收、收尾与归档

```
【verify】product-tag-list
```

```
【api-smoke】product-tag-list
```

```
【verify-e2e】product-tag-list
```

```
【finish】product-tag-list
```

```
【archive】product-tag-list
```

验收分层见 [docs/testing/README.md](../../docs/testing/README.md)。

---

## 一、新功能开发（AI 生成代码）

| 你说 | Skill |
|------|-------|
| **先写 spec / 提案** | `feature-spec` |
| 按 PRD / 截图 / 接口开发 | `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `prd-feature-dev` |
| **语雀 / 飞书 Markdown PRD** | `prd-markdown-ingest` → `feature-spec` → `feature-analyze` → `feature-dev-workflow` |
| 按 Figma 切页面 | `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `figma-feature-dev` |
| **远程 Axure 原型站 URL** | `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `prototype-html-feature-dev` §远程 + §F |
| 按本地静态 HTML 原型开发 | `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `prototype-html-feature-dev` §本地 |
| 新建列表 / 表单 / 工作台 | `feature-spec` → `feature-analyze` → `feature-dev-workflow` → `vue-page-codegen` |
| **已有页面加功能** | `incremental-feature` |
| 需求复杂，先调研澄清 | `spec-research-clarify` |

```
feature-spec              # propose → docs/features/<slug>/
feature-analyze           # implement 前 artifact 一致性；CRITICAL>0 禁止 ready
feature-dev-workflow      # ①理解 → ②对齐 → ③codegen → ④验收
├── prd-markdown-ingest   # 语雀/飞书 Markdown 清洗
├── prd-feature-dev
├── figma-feature-dev
├── prototype-html-feature-dev   # 本地 .html + 远程 Axure；§F curl+JS + Browser MCP P0
├── vue-page-codegen
├── reference-checklist
└── spec-research-clarify（可选）
feature-verify            # L1：对照 spec / tasks / lint + build
feature-finish            # verify PASS 后 PR 描述 + 自检 + archive 提示
api-smoke                 # L2：curl 接口探针（可选）
feature-e2e-verify        # L3：Browser MCP → Playwright → 人工（可选）
feature-archive           # 合并 docs/specs/ + 归档
unit-test-codegen         # utils/services 单测（Vitest/Jest）
```

---

## 二、AI + 人协作（开发过程中）

| 阶段 | 你说 | Skill |
|------|------|-------|
| **首次接入** | 「扫描项目约定」 | `project-bootstrap` |
| **联调**、对接接口、字段对一下、Swagger、**OpenAPI** | `openapi-api-integration`（有 spec）或 `api-integration` |
| **增量** | 「在这个页面加一列」 | `incremental-feature` |
| 修 Bug | 「这个报错怎么回事」「xxx 点击没反应」 | `bugfix-workflow`（MCP 优先，可降级静态排查） |
| 重构 | 「文件太大拆分一下」 | `page-refactor` |
| **全项目 rules 重构** | 「全量重构」「所有代码按规范改」 | `rules-refactor` |
| **Vue2→Vue3** | 「升 Vue3」「迁移 Vue3」 | `vue2-to-vue3-refactor` |
| **规范优化（单页）** | 「按规范优化」「整理代码」 | `code-normalize` |
| 跨模块公共组件 | 「跨模块封装 CategoryPicker」 | `shared-component` |
| 提交前 | 「review 一下」 | `code-review` |
| **新页本地路由** | 「注册路由」「加 path」 | `route-permission` |
| **build/test 失败** | 「CI 挂了」「build 失败」 | `ci-fix` |
| **lint / 未使用引入** | 「跑 lint」「eslint 报错」 | `lint-check` |
| **SDD 提案** | 「先写 spec」「propose」 | `feature-spec` |
| **Artifact 分析** | 「【analyze】」「ready 前评审」 | `feature-analyze` |
| **Feature 验收 L1** | 「verify」「对照 spec 验收」 | `feature-verify` |
| **接口探针 L2** | 「api-smoke」「curl 探针」 | `api-smoke` |
| **UI 冒烟 L3** | 「verify-e2e」「浏览器验收」 | `feature-e2e-verify` |
| **PR 收尾** | 「【finish】」「验收通过准备合码」 | `feature-finish` |
| **Feature 归档** | 「archive」「合并 spec」 | `feature-archive` |
| 补单测 | 「给 utils 写单测」「test:unit」 | `unit-test-codegen` |

---

## 配置约定

Vue 2/3 对照、request 路径、按钮 type 等**完整表**以 [rules-activation.md](shared/rules-activation.md) §配置约定 为准；本节仅保留速查。

| 项 | Vue 3 | Vue 2 |
|----|-------|-------|
| 接口文件 | `services.ts` | `services.js` |
| 函数写法 | 全箭头函数（含 composable、utils） | services 箭头；methods Options API |
| 文字按钮 | `type="primary" link` | `type="text"` |

---

## 文档权威来源（避免重复读错）

| 主题 | 权威文件 |
|------|----------|
| **PC ↔ uni-app 内核同步** | `docs/agent-kernel-sync.md` |
| Skill 路由、黄金话术、质量红灯 | **本文件 README** |
| **Skills 版本 / 分类 / bump 流程** | **manifest.json** + **shared/skills-versioning.md** + **CHANGELOG.md** |
| 预加载计划、禁止预加载列表 | `shared/rules-activation.md` |
| **通用编码约定**（权限、路由、接口、types） | **`.cursor/rules/*.mdc` + Skills** |
| **项目原则** | `docs/constitution.md` |
| **进行中 Feature 规格** | `docs/features/<slug>/` |
| **验收分层说明** | `docs/testing/README.md` |
| **已归档行为 spec** | `docs/specs/` |
| 单项目扫描结果（request 路径、布局组件、网关等） | `.cursor/project-conventions.md`（bootstrap 产出，**扫描快照**；**重构权威仍是 rules**，见 `rules-refactor`） |
| Vue 3 页面写法 | `Vue代码生成指南.mdc` + 按页面类型 rules |
| **hooks 拆分边界** | **`Vue代码生成指南.mdc` §hooks 拆分边界** |
| **函数箭头写法** | **`JavaScript通用代码生成指南.mdc` §Vue 3 函数写法** |
| **types.ts 职责** | **`TypeScript与types规范.mdc`** |
| **规范优化全量验收** | **`code-normalize/checklist.md`** + `reference-checklist.md` |
| Vue 2 页面写法 | `Vue2代码生成指南.mdc` |
| 代码示例（非预加载） | `代码规范示例参考.mdc` |
| 阶段④验收 | `feature-dev-workflow/reference-checklist.md` |
| 跨模块 UI 组件 | `shared-component/SKILL.md` + 按需 `reference.md` |

---

## 三、Rules 索引（`.cursor/rules/*.mdc`）

| 规则 | 用途 | 预加载 |
|------|------|--------|
| `前端通用代码规范.mdc` | **Always Apply** | 自动 |
| `Vue代码生成指南.mdc` | Vue 3 主路径 | ✅ 基线 |
| `Vue2代码生成指南.mdc` | vue@2.x 专用 | ✅ vue2 时 |
| `项目结构与命名规范.mdc` | 目录与命名 | ✅ 基线 |
| **`TypeScript与types规范.mdc`** | types 就近、constants/utils 职责 | ✅ Vue3 TS 基线 |
| `JavaScript/HTML/表单/复杂页/路由/状态/高级表单` | 按页面类型 | ✅ 按需 |
| `代码规范示例参考.mdc` | 可复制示例 | ❌ **仅查阅** |

完整预加载清单见 [rules-activation.md](shared/rules-activation.md)。

---

## SDD 完整路径（新建页）

与 [agent-workflow-roadmap.md](../../docs/agent-workflow-roadmap.md) 一致：

```
【spec】→ 【analyze】→ 【新建】→ 【verify】→ 【finish】→ 【archive】
   ↓          ↓           ↓          ↓          ↓          ↓
propose    门禁 PASS    写码+勾tasks  L1 验收   PR 收尾   docs/specs/
```

| 阶段 | Skill / CLI | 说明 |
|------|-------------|------|
| ⓪ spec | `feature-spec` | 产出 `docs/features/<slug>/` |
| ⓪b analyze | `feature-analyze` · `feature-check analyze` | CRITICAL=0 且 `Status: ready` 后再 implement |
| ③ implement | `feature-dev-workflow` | 写码 + 勾选 `tasks.md` |
| ④ verify | `feature-verify` · `feature-check verify` | lint-fix + build（L1 门禁） |
| ④b finish | `feature-finish` | verify PASS 后 PR 描述与自检 |
| ⑤ archive | `feature-archive` · `feature-check archive-ready` | 合并主 spec 库 |

**可选加强：** L2 `api-smoke` · L3 `feature-e2e-verify`（在 verify 前后均可，不替代 L1）。

**跳过 spec/analyze：** 仅当用户明确「直接写码」且 scope 为单页 trivial；**增量**走 `incremental-feature`，不走本路径。

对应 OpenSpec / Spec-Kit 能力：

| 本体系 | OpenSpec | Spec-Kit |
|--------|----------|----------|
| `feature-spec` | `/opsx:propose` | `/speckit.specify` + plan |
| `feature-analyze` | — | `/speckit.analyze` |
| `feature-dev-workflow` | `/opsx:apply` | `/speckit.implement` |
| `feature-verify` | `/opsx:verify` | converge |
| `feature-finish` | — | PR / handoff |
| `feature-archive` | `/opsx:archive` | archive + spec merge |
| `docs/constitution.md` | constitution | constitution |
| `docs/specs/` | `specs/` 主库 | 主 spec 库 |

---

## 四、组件资产

| 用途 | 目录 |
|------|------|
| Vue 3 列表页 | `.cursor/components/HiTable/` |
| Vue 2 列表页 | `.cursor/components/HiTable-vue2/` |

---

## 五、页面类型 → 规范

| 类型 | 规范 |
|------|------|
| 列表页 | HiTable + `Vue代码生成指南` |
| 表单 / 详情 | Vue 3：`表单与详情页开发指南`；Vue 2：`Vue2代码生成指南` §表单 |
| 列表 + 弹窗 | 列表 + `EditDialog` |
| 工作台 / 双栏 | Vue 3：`复杂页面开发指南`；Vue 2：`Vue2代码生成指南` §复杂页 |

---

## 六、质量红灯（交付自检）

Agent 交付若出现以下情况，视为未按规范执行：

| 红灯 | 说明 |
|------|------|
| 无「规范预加载」汇报行 | 未走 rules-activation |
| 无「预加载计划」 | 复杂任务未先列 Read 清单 |
| request 路径与 project-conventions 不一致 | 未 bootstrap 或未 Read conventions |
| Vue 2 出现 script setup / Pinia | 版本判错 |
| 同模块组件放顶层 components/ | shared-component 层级错 |
| 纯逻辑写成空壳 .vue | 应放 hooks/utils |
| **types 留在 hook/constants/utils** | 应迁 `types.ts`，走 code-normalize |
| **新建页无 design.md/tasks.md 且未声明跳过 spec** | 须先 `feature-spec` |
| **非 trivial 新建未 analyze PASS 即 implement** | 须先 `feature-analyze`（CRITICAL=0） |
| **新建 feature 未 feature-verify PASS 即交付** | 阶段 ④ 未完成 |
| **verify PASS 后未 finish 即声称可合码** | 须 `feature-finish` 或用户声明跳过 |
| **优化仅过 types、未过全量 checklist** | 见 code-normalize/checklist.md |

详见 [rules-activation §质量红灯](shared/rules-activation.md)。

---

## 七、版本管理

**Bundle 当前版本：** 见 [manifest.json](manifest.json) → `bundleVersion`（现 `1.3.3`）

| 命令 | 说明 |
|------|------|
| `python3 scripts/skills-version.py list` | 列出全部 Skill 版本与分类 |
| `python3 scripts/skills-version.py list --category ingest` | 按分类筛选 |
| `python3 scripts/skills-version.py check` | 校验 manifest ↔ SKILL.md 一致 |
| `python3 scripts/skills-version.py sync` | 将 manifest 版本写入各 SKILL.md |
| `python3 scripts/skills-version.py bump <name> minor "说明"` | bump 单 Skill（并提示写 CHANGELOG） |
| `python3 .cursor/skills/scripts/feature-check.py verify <slug>` | Feature 验收门禁（lint-fix + build） |
| `python3 .cursor/skills/scripts/feature-check.py analyze <slug>` | Artifact 一致性（implement 前） |
| `python3 .cursor/skills/scripts/feature-check.py board` | Feature 看板 |
| `python3 .cursor/skills/scripts/spec-index.py` | 刷新 docs/specs/_index.md 路由↔spec 索引 |

完整规则：[shared/skills-versioning.md](shared/skills-versioning.md) · 变更记录：[CHANGELOG.md](CHANGELOG.md)

**维护顺序：** 改 SKILL → bump → sync → 写 CHANGELOG → `check`

---

```
# 语雀 PRD + 全链路
【spec】propose mini-goods-detail。语雀 PRD：（粘贴 Markdown）
【analyze】mini-goods-detail
【新建】按 docs/features/mini-goods-detail/ 实现

# Axure 原型站 + 开发
【spec】propose mini-goods-detail。原型 http://host/小程序商城/index.html#商品详情页.html
【analyze】mini-goods-detail
【新建】按 docs/features/mini-goods-detail/ 实现

# 表单页
【spec】propose coupon-create。按 PRD 开发优惠券创建页，模块 marketing
【analyze】coupon-create
【新建】按 docs/features/coupon-create/ 实现

# 验收收尾
【verify】product-tag-list
【finish】product-tag-list
【archive】product-tag-list

# 重构
【拆分】AdminWorkbench.vue 太大了，按规范拆成 hooks 和子组件

# 公共组件（跨模块）
【跨模块】封装 CategoryPicker 到顶层 components/，product 和 order 都要用

# 模块内共用
【增量】views/product 下多页共用 CategoryPicker，放到 product/components/

# 规范优化
【优化】按规范整理 views/product/list，全量对齐 rules

# Review
【review】帮我 review views/product/tag-list 是否符合规范

# 新建 Skill
【skill-creator】帮我把「导出 Excel 校验流程」沉淀成一个 Skill，category quality
```
