# Agent 内核同步清单（Kernel Sync）

> **权威仓：** `fe-agent-workflow` · **本端目录：** `uniapp/` · `platform: uniapp` · `kernelVersion: 1.3.1`  
> **对端目录：** `pc/` · `platform: pc`  
> **业务项目：** `HiStore-mall-mobile`（`./tools/install.sh uniapp …` 安装）  
> **根目录摘要：** [../../docs/agent-kernel-sync.md](../../docs/agent-kernel-sync.md)

---

## 一、字段含义

| 字段 | 说明 | 两仓库是否一致 |
|------|------|----------------|
| `platform` | 平台壳层标识：`pc` \| `uniapp` | **永不相同** |
| `kernelVersion` | **共享内核**版本（SDD 流程、门禁逻辑、通用 Skill 框架） | **应保持一致** |
| `bundleVersion` | **本仓库整体**发布版本（含平台专属改动） | 可相同，也可因平台 patch 分叉 |

**升版规则：**

- 只改 SDD / analyze / bugfix 四阶段等 **内核** → 两仓库 `kernelVersion` **同步 bump**，`bundleVersion` 建议同步
- 只改 uni-app 分包 / rpx / pages.json → 仅本仓库 `bundleVersion` patch bump，`kernelVersion` 不变
- 对端 `kernelVersion` 落后时 → 按本文 **§二** 做定向同步，**不要**整目录覆盖

---

## 二、同步分级

| 级别 | 含义 | Agent / 人工动作 |
|------|------|------------------|
| **K0 原样同步** | 内核文件，仅替换平台术语 | diff → 合并 → 术语表替换 |
| **K1 逻辑同步** | 流程相同，实现/示例因平台而异 | 同步结构与门禁，**手写适配** |
| **P 平台专属** | 绝不跨仓库复制 | 各仓库独立维护 |
| **R 仓库本地** | 扫描产物 / 进行中需求 | 不同步 |

### 平台术语替换表（K0 / K1 必用）

| 概念 | PC（`pc`） | uni-app（`uniapp`） |
|------|------------|---------------------|
| 路由注册 | `vue-router` / `router/modules` | `pages.json` / `subPackages` |
| 页面目录 | `views/<module>/<page>/` | `subPackages/<module>/` 或 `pages/` |
| 路由 path 示例 | `/product/tag-list` | `subPackages/product/list` |
| 列表组件 | `HiTable` + `el-table-column` | 原生 `scroll-view` / `view` + uview |
| UI 库 | Element Plus / Element UI | 原生组件 + uview-ui |
| 导航 | `router.push` | `uni.navigateTo` / `$navigateTo` |
| 权限 | 菜单树接口 + 路由守卫 | 登录拦截 / 页面内逻辑（无按钮级 v-permission） |
| 样式 | `scss` + `tablePage.scss` | `rpx` + `uni.scss` |
| spec-index 数据源 | `src/router/modules/*.js` | `pages.json` |
| feature-check 路径正则 | `views/` `components/` | `subPackages/` `pages/` `service/` |

---

## 三、K0 — 原样同步（改内核时两边一起改）

> 路径均相对于 `.cursor/skills/` 或 `docs/`。同步后运行 `python3 .cursor/skills/scripts/skills-version.py check`。

### SDD 工作流 Skills

| 路径 | 说明 |
|------|------|
| `feature-analyze/SKILL.md` | 规划门禁；术语按 §二替换 |
| `feature-finish/SKILL.md` | verify 后 PR 收尾 |
| `feature-archive/SKILL.md` | Delta 合并算法 |
| `feature-spec/SKILL.md` | blocker 分级、ready 门禁（术语替换） |
| `feature-verify/SKILL.md` | L1 验收框架 |
| `spec-research-clarify/SKILL.md` | 澄清流程 |

### 质量 / 联调 Skills（流程级）

| 路径 | 说明 |
|------|------|
| `bugfix-workflow/SKILL.md` | 四阶段调试框架 |
| `api-integration/SKILL.md` | 入参透传、出参直绑原则 |
| `openapi-api-integration/SKILL.md` | OpenAPI 生成流程 |
| `api-smoke/SKILL.md` | L2 curl 探针 |
| `code-review/SKILL.md` | 审查流程 |
| `ci-fix/SKILL.md` | 构建失败修复循环 |
| `lint-check/SKILL.md` | ESLint 交付门禁 |
| `unit-test-codegen/SKILL.md` | 单测范围约定 |

### Ingest Skills（材料接入 — 流程级）

| 路径 | 说明 |
|------|------|
| `prd-markdown-ingest/SKILL.md` | 语雀/飞书 Markdown |
| `prd-feature-dev/SKILL.md` | PRD 解析主流程 |
| `prototype-html-feature-dev/SKILL.md` | §A–E 与 §F 框架（平台示例不照搬） |

### 共享规范

| 路径 | 说明 |
|------|------|
| `shared/skill-conventions.md` | Skill 编写规范 |
| `shared/skills-versioning.md` | 版本规则（含 `platform` / `kernelVersion` 说明） |
| `CHANGELOG.md` | 仅同步 **`### Kernel`** 或 **`[Bundle x.y.z]`** 中标注为内核的条目 |

### docs 模板（SDD 工件）

| 路径 | 说明 |
|------|------|
| `docs/features/_template/status.yaml` | workflow 状态机 |
| `docs/features/_template/clarify-log.md` | blocker 清单（术语替换） |
| `docs/features/_template/proposal.md` | 若内核改 proposal 结构 |
| `docs/features/_template/spec.md` | 若内核改验收场景格式 |
| `docs/features/_template/tasks.md` | 若内核改任务拆法 |
| `docs/features/README.md` | **仅**生命周期表 / 话术表 |
| `docs/testing/README.md` | **仅** L1/L2/L3 三层模型章节 |

### 脚本（共享逻辑部分）

| 路径 | 说明 |
|------|------|
| `scripts/skills-version.py` | 版本校验 |
| `scripts/sync-manifest-metadata.py` | manifest 元数据同步 |
| `scripts/skill-standardize.py` | Skill 批量标准化 |
| `scripts/export-agent-host.py` | 跨 Host 导出（Claude Code / Codex） |
| `scripts/feature-check.py` | **子命令与门禁逻辑**（路径正则见 K1） |

### 共享元数据（内核维护）

| 路径 | 说明 |
|------|------|
| `shared/skill-metadata.yaml` | skill-standardize 数据源 |
| `shared/skill-when-to-use.yaml` | 跨 Host 导出 when_to_use |
| `shared/mcp-host-adapter.yaml` | MCP 能力映射 |
| `skill-creator/SKILL.md` | 新建/修改 Skill 流程 |

### docs（内核文档）

| 路径 | 说明 |
|------|------|
| `docs/agent-workflow-roadmap.md` | SDD 演进路线图 |
| `docs/agent-host-export.md` | 跨 Host 导出说明（rules 清单因平台而异） |

---

## 四、K1 — 逻辑同步（结构对齐，实现各写各的）

| 路径 | PC 要点 | uni-app 要点 |
|------|---------|--------------|
| `scripts/feature-check.py` | `views/` `router` | `pages/` `subPackages/` `service/` |
| `scripts/spec-index.py` | 解析 `router/modules` | 解析 `pages.json`（含注释 strip） |
| `scripts/export-agent-host.py` | PC rules 清单 | uni-app rules 清单；脚本逻辑 K0 同步 |
| `feature-dev-workflow/SKILL.md` | ingest 表 + 四阶段 | 同结构；子 Skill 链相同 |
| `incremental-feature/SKILL.md` | 列表加列 / HiTable | 列表加筛 / 原生列表 |
| `project-bootstrap/SKILL.md` | 扫描 router、HiTable | 扫描 pages.json、分包、uview |
| `shared/project-toolbox.md` | `npm run start`、HiTable | HBuilderX / `build:h5`、无 HiTable |
| `shared/skill-boundaries-baseline.md` | `views/`、HiTable | `subPackages/`、禁止非 tabBar 入主包 |
| `shared/rules-activation.md` | 中后台 rules 列表 | uniapp rules 列表 |
| `figma-feature-dev/SKILL.md` | 管理端布局 | **内容区 rpx 1:1**；排除状态栏/胶囊 |
| `spec-analyze-ui-images/SKILL.md` | 桌面布局 | 移动端布局 + 还原范围 |
| `vue-page-codegen/SKILL.md` | HiTable 列表页 | 原生列表 / 表单 / 弹层 |
| `route-permission/SKILL.md` | `router/modules` | `pages.json` 主包/分包 |
| `shared-component/SKILL.md` | `src/components/` | 顶层 `components/` |
| `page-refactor/SKILL.md` | 拆 `views` 大文件 | 拆 `subPackages` 大文件 |
| `rules-refactor/SKILL.md` | 闭环流程 + **project-refactor SDD 门禁** | 同流程；checklist 各用各的 |
| `code-normalize/checklist.md` | Element / HiTable 项 | uni-app / uview 项 |
| `feature-dev-workflow/reference-checklist.md` | 中后台验收项 | 分包 / 导航验收项 |
| `manifest.json` | `platform: pc` | `platform: uniapp`；`kernelVersion` 对齐 |

---

## 五、P — 平台专属（绝不跨仓库同步）

| 路径 | 原因 |
|------|------|
| `.cursor/rules/**` | 编码规范完全不同；**混用必乱套** |
| `.cursor/components/HiTable/**` | 仅 PC |
| `vue-page-codegen/SKILL.md` 中的代码示例 | 组件 API 不可互用 |
| `docs/constitution.md` | 原则级差异（分包 vs 菜单路由） |
| `.cursor/project-conventions.md` | 各仓库 bootstrap 扫描产物 |
| `docs/agent-workflow-training.md` | 培训示例按平台定制 |
| `openapi-api-integration/reference.md` | 示例 URL 因项目而异 |
| `api-smoke/reference-curl.md` | 环境 / token 因项目而异 |

---

## 六、R — 仓库本地（禁止当作同步源）

| 路径 | 说明 |
|------|------|
| `docs/specs/_index.md` | `spec-index.py` 生成物 |
| `docs/specs/<module>/*.md` | 已归档行为 spec |
| `docs/features/<slug>/` | 进行中 feature（业务需求） |
| `docs/features/archive/**` | 历史归档 |
| `CHANGELOG.md` 中 **`### Platform (uniapp|pc)`** 段 | 平台专属变更记录 |

---

## 七、推荐同步流程

### 场景 A：PC 升了内核，同步到 uni-app

```text
请把 HiStore-store-pc 的 Agent **内核**变更同步到 HiStore-mall-mobile：

- 对端 kernelVersion：1.3.1 → 1.4.0
- 仅按 docs/agent-kernel-sync.md 的 K0/K1 清单
- platform 保持 uniapp，术语用替换表
- 不要动 .cursor/rules、vue-page-codegen 代码示例、project-conventions.md
- 同步后 bump manifest kernelVersion + bundleVersion，更新 CHANGELOG Kernel 段
- 运行 skills-version.py check
```

### 场景 B：只改了 uni-app 分包规范

```text
仅更新本仓库 bundleVersion patch，不同步到 PC，不写 CHANGELOG Kernel 段。
```

### 场景 C：新增内核 Skill（如 feature-xxx）

1. 在一边仓库实现，manifest 登记，`kernelVersion` minor bump  
2. 按 K0 复制到对端，做术语替换（K1 若含路径）  
3. 两边 `README.md` 路由表、`rules-activation.md` **各自**追加  
4. `skills-version.py check` 两边都跑  

---

## 八、同步后检查清单

- [ ] `manifest.json` → `platform` 未变、`kernelVersion` 与对端一致
- [ ] `python3 .cursor/skills/scripts/skills-version.py check` PASS
- [ ] K0 文件无 PC 术语残留（`HiTable` `views/` `el-table` `router/modules`）
- [ ] K1 脚本在本地可运行（`feature-check.py list` / `spec-index.py --no-write`）
- [ ] `CHANGELOG.md` 已区分 **Kernel** / **Platform** 条目
- [ ] 未误覆盖 `docs/constitution.md` 与 `.cursor/rules/`

---

## 九、CHANGELOG 写法约定（两仓库统一）

```markdown
## [Bundle 1.4.0] - YYYY-MM-DD

### Kernel（同步至 pc + uniapp）
- feature-analyze：……

### Platform (uniapp)（仅本仓库）
- route-permission：分包……
```

对端仓库对应写 `### Platform (pc)`。

---

## 十、快速对照表

| 目录 | PC | uni-app | 同步级别 |
|------|----|---------|----------|
| SDD feature-* 流程 | ✓ | ✓ | K0 |
| bugfix 四阶段 | ✓ | ✓ | K0 |
| feature-check / spec-index | ✓ | ✓ | K1 |
| rules/*.mdc | PC | uni-app | **P** |
| vue-page-codegen | PC | uni-app | **P** |
| project-conventions | 扫描 | 扫描 | **P** |
| docs/features 进行中 | 业务 | 业务 | **R** |

---

*维护：内核升版时先改 `kernelVersion`，再按本清单同步对端。完整培训见 `docs/agent-workflow-training.md`。*
