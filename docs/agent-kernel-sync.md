# Agent 内核同步清单（Kernel Sync）

> **权威仓：** `fe-agent-workflow`  
> **PC 端：** `pc/` · `platform: pc`  
> **uni-app 端：** `uniapp/` · `platform: uniapp`  
> **版本字段：** `pc/.cursor/skills/manifest.json` / `uniapp/.cursor/skills/manifest.json` → `platform` / `kernelVersion` / `bundleVersion`

两端**并列目录、不拆公共 kernel 文件夹**；内核级文件在 `pc` ↔ `uniapp` 之间按本清单同步，然后对业务项目执行 `tools/install.sh`。

---

## 一、字段含义

| 字段 | 说明 | 两端是否一致 |
|------|------|----------------|
| `platform` | `pc` \| `uniapp` | **永不相同** |
| `kernelVersion` | SDD 流程、门禁、通用 Skill 框架 | **应保持一致** |
| `bundleVersion` | 本平台整体版本 | 可分叉 |

**升版规则：**

- 内核变更 → 两端 `kernelVersion` 同步 bump → `install.sh` 安装到业务仓
- 仅 PC 或仅 uni-app 规范 → 只改对应目录，`bundleVersion` patch，不写 Kernel CHANGELOG

---

## 二、同步分级

| 级别 | 含义 |
|------|------|
| **K0** | 内核文件，术语替换后同步 |
| **K1** | 结构同步，实现各端适配 |
| **P** | 平台专属，禁止跨端复制 |
| **R** | 业务项目本地，不同步 |

### 平台术语替换表

| 概念 | PC | uni-app |
|------|-----|---------|
| 路由 | `vue-router` / `router/modules` | `pages.json` / `subPackages` |
| 页面目录 | `views/<module>/<page>/` | `subPackages/<module>/` |
| 列表 | HiTable + el-table | 原生 + uview |
| spec-index | `router/modules` | `pages.json` |
| feature-check 路径 | `views/` | `subPackages/` `pages/` |

（完整表见历史版本 §二，维护时两端 paths 前缀为 `pc/.cursor/` 与 `uniapp/.cursor/`。）

---

## 三、K0 路径（相对各端 `.cursor/skills/`）

`feature-analyze`、`feature-finish`、`feature-archive`、`feature-spec`、`feature-verify`、`spec-research-clarify`、`bugfix-workflow`、`api-*`、`code-review`、`ci-fix`、`lint-check`、`unit-test-codegen`、`prd-*`、`prototype-html-feature-dev`（框架）、`shared/skill-conventions.md`、`shared/skills-versioning.md`、`shared/skill-when-to-use.yaml`、`shared/mcp-host-adapter.yaml`、`skill-creator/`、`CHANGELOG.md`（Kernel 段）

**docs（各端 `pc/docs/` ↔ `uniapp/docs/`）：** `features/_template/*`、`features/_template/project-refactor/*`、`features/_template/vue3-migration/*`、`features/README.md`、`project-refactor-guide.md`、`vue3-migration-guide.md`、`testing/README.md`

---

## 四、K1 路径

`scripts/feature-check.py`、`scripts/spec-index.py`、`scripts/export-agent-host.py`、`feature-dev-workflow/`、`project-bootstrap/`、`shared/project-toolbox.md`、`shared/skill-boundaries-baseline.md`、`shared/rules-activation.md`、`shared/host-rules-manifest.yaml`、`vue-page-codegen/`、`route-permission/`、`figma-feature-dev/` 等 — **结构对齐，示例按平台改写**。

---

## 五、P — 禁止跨端同步

| 路径 | 原因 |
|------|------|
| `pc/.cursor/rules/**` ↔ `uniapp/.cursor/rules/**` | 编码规范不同 |
| `pc/.cursor/components/HiTable/**` | 仅 PC |
| 各端 `docs/constitution.md` | 原则不同 |
| `project-conventions.md` | bootstrap 产物，在业务项目 |
| 各端 `docs/agent-workflow-training.md` | 培训示例分平台 |

---

## 六、推荐流程

### 内核：PC → uni-app

```text
在 fe-agent-workflow 中，把 pc/ 的内核变更同步到 uniapp/：
- 仅 K0/K1 清单
- 术语用替换表
- 不要动 rules/、vue-page-codegen 示例
- 两端 manifest kernelVersion 对齐
- python3 uniapp/.cursor/skills/scripts/skills-version.py check
- ./tools/install.sh uniapp /path/to/HiStore-mall-mobile
```

### 安装到业务项目

```bash
./tools/install.sh pc /path/to/HiStore-store-pc
./tools/install.sh uniapp /path/to/HiStore-mall-mobile
./tools/install.sh pc /path/to/HiStore-store-pc --with-docs   # 可选
```

### 仅改一端

编辑 `pc/` 或 `uniapp/` → `install.sh` 对应平台 → 不写 Kernel CHANGELOG。

---

## 七、同步后检查

- [ ] 两端 `kernelVersion` 一致
- [ ] `skills-version.py check` 两端 PASS
- [ ] K0 无对方平台术语残留
- [ ] `install.sh` 已装到业务仓（保留业务仓 `project-conventions.md`）

---

*完整条目见 `pc/docs/agent-kernel-sync.md`（历史详版）；新维护以本仓 `docs/` 为准。*
