# fe-agent-workflow 统一权威仓 — 培训说明

> **适用对象：** 维护 Agent 工作流的同学、Tech Lead  
> **业务研发：** 日常在业务项目用 Cursor 即可；本节主要说明「规范从哪来、怎么更新」  
> **关联文档：** [agent-kernel-sync.md](./agent-kernel-sync.md) · [../README.md](../README.md)

---

## 一、为什么要有这个仓？

以前 PC 中后台和 uni-app 移动端**各自维护**一套 `.cursor/`，容易出现：

- 内核流程（SDD、analyze、bugfix 四阶段）两边版本不一致
- 不知道改哪个仓库才算「权威」
- 复制粘贴漏文件

`**fe-agent-workflow` 是唯一的流程权威源**；业务项目里的 `.cursor` 是**安装产物**，不是源头。

```
fe-agent-workflow/          ← 改规范、改 Skill 在这里
    ├── pc/
    └── uniapp/
         ↓ install.sh
HiStore-store-pc/.cursor/   ← 业务项目消费
HiStore-mall-mobile/.cursor/
```

---

## 二、目录结构（不拆公共内核）

```
fe-agent-workflow/
├── README.md
├── docs/
│   ├── agent-kernel-sync.md       # pc ↔ uniapp 内核同步清单
│   └── agent-workflow-repo-guide.md  # 本文
├── tools/
│   └── install.sh                 # 安装到业务项目
├── pc/                            # 中后台整套
│   ├── .cursor/rules|skills|components
│   └── docs/
└── uniapp/                        # 移动端整套
    ├── .cursor/
    └── docs/
```

**刻意不做** `kernel/` + `platforms/` 物理拆分——维护简单：改哪端就进哪个目录。

---

## 三、安装到业务项目（必会）

### 方式 A：本地已 clone（维护者常用）

在 `fe-agent-workflow` 根目录执行：

```bash
# 中后台
./tools/install.sh pc /path/to/HiStore-store-pc

# uni-app
./tools/install.sh uniapp /path/to/HiStore-mall-mobile

# 可选：同步 docs 模板（constitution、features/_template 等）
./tools/install.sh pc /path/to/HiStore-store-pc --with-docs
```

### 方式 B：直接从 Git 安装（业务研发推荐）

**无需**事先 clone 工作流仓库。

**推荐：一键远程安装**（默认拉取 https://github.com/TieZhuzhu/fe-agent-workflow.git）

```bash
curl -fsSL https://raw.githubusercontent.com/TieZhuzhu/fe-agent-workflow/master/tools/remote-install.sh \
  | bash -s -- uniapp /path/to/HiStore-mall-mobile --with-docs

# 或本地已有脚本：
bash tools/remote-install.sh uniapp /path/to/HiStore-mall-mobile --with-docs
```

**或使用 install.sh + --from-git**（支持独立仓与父仓嵌套布局）：

```bash
bash tools/install.sh uniapp /path/to/HiStore-mall-mobile \
  --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git \
  --with-docs

# 锁定版本（分支或 tag）
bash tools/install.sh uniapp /path/to/HiStore-mall-mobile \
  --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git \
  --ref master \
  --with-docs
```

`remote-install.sh` 与 `--from-git` 均会 shallow clone 到临时目录，安装完成后**自动清理**。

**行为说明：**


| 项    | 说明                                                          |
| ---- | ----------------------------------------------------------- |
| 覆盖范围 | 整包覆盖目标 `.cursor/`（rules + skills + 组件）                      |
| 保留文件 | 目标项目已有 `project-conventions.md` **不会**被删                    |
| 不安装  | `project-conventions.md` 不纳入本仓（各项目 bootstrap 生成）            |
| docs | 默认只装 `.cursor`；`--with-docs` 同步 SDD 模板，不含 `specs/_index.md` |
| `--from-git` | shallow clone 远程仓，无需本地 fe-agent-workflow 副本              |
| `--ref` | 配合 `--from-git` 指定分支或 tag；省略则用远程默认分支                      |


**培训话术（给团队）：**

> 业务仓不要直接改 `.cursor` 提交流程规范；到 `fe-agent-workflow` 改完，跑 `install.sh` 装回来。

---

## 四、日常维护三种场景


| 场景                    | 操作                                                                                                                               |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **只改 PC**             | 编辑 `pc/` → `install.sh pc …` → CHANGELOG `Platform (pc)`                                                                         |
| **只改 uni-app**        | 编辑 `uniapp/` → `install.sh uniapp …` → CHANGELOG `Platform (uniapp)`                                                             |
| **改内核（SDD/通用 Skill）** | 在一端改 → 按 [agent-kernel-sync.md](./agent-kernel-sync.md) K0/K1 同步到另一端 → 两端分别 install → CHANGELOG `Kernel` + 两端 `kernelVersion` 对齐 |


**内核示例：** `feature-analyze`、`bugfix-workflow` 四阶段、`skill-creator`、feature-check 门禁逻辑。

**平台专属示例：** `rules/*.mdc`、`vue-page-codegen`、`HiTable`（仅 pc）、`路由与分包规范`（仅 uniapp）。

---

## 五、版本字段（manifest.json）

各平台 `.cursor/skills/manifest.json`：


| 字段              | 含义                |
| --------------- | ----------------- |
| `platform`      | `pc` | `uniapp`   |
| `kernelVersion` | 内核版本，**两端应对齐**    |
| `bundleVersion` | 本平台整体版本，可独立 patch |


校验：

```bash
python3 pc/.cursor/skills/scripts/skills-version.py check
python3 uniapp/.cursor/skills/scripts/skills-version.py check
```

---

## 六、与业务项目 docs 的关系


| 位置                           | 内容                                              |
| ---------------------------- | ----------------------------------------------- |
| `fe-agent-workflow/*/docs/`  | constitution 模板、features/_template、培训文档、roadmap |
| 业务项目 `docs/features/<slug>/` | **进行中需求**，留在业务仓                                 |
| 业务项目 `docs/specs/_index.md`  | bootstrap 生成，不纳入权威仓                             |


`--with-docs` 适合统一升级模板；**不要**用 install 覆盖业务进行中的 feature 目录。

---

## 七、新增 Skill / 改流程（维护者）

1. 在 `pc/` 或 `uniapp/` 使用 `**skill-creator`** Skill（或手改）
2. 若内核级 → 同步到另一端 → 两端 `kernelVersion` bump
3. `skills-version.py check` 两端 PASS
4. `install.sh` 装到业务项目
5. 培训文档：更新对应平台 `docs/agent-workflow-training.md`；跨平台约定更新本文或 `agent-kernel-sync.md`

---

## 八、FAQ

**Q：我能直接在 HiStore-mall-mobile 里改 `.cursor` 吗？**  
A：可以本地试，但**合码前**应回写到 `fe-agent-workflow/uniapp/` 并 install，否则下次 install 会被覆盖，且 pc/uniapp 会再次分叉。

**Q：内核同步一定要手动吗？**  
A：按 `agent-kernel-sync.md` 清单 diff 同步；可用 AI：「把 fe-agent-workflow/pc 的内核变更同步到 uniapp/，按 agent-kernel-sync K0/K1」。

**Q：project-conventions 放哪？**  
A：只在业务项目，由 `project-bootstrap` 生成；不进 fe-agent-workflow。

**Q：install 会删我业务项目的 HiTable 自定义吗？**  
A：install 只动 `.cursor/`；业务 `src/` 代码不受影响。若你在业务仓改过 `.cursor` 且未回写权威仓，会被覆盖——所以规范改动走权威仓。

---

## 九、一页纸速查（分享用）

```
┌──────────────────────────────────────────────────────────┐
│  fe-agent-workflow 统一权威仓                             │
├──────────────────────────────────────────────────────────┤
│  权威源：fe-agent-workflow/pc | fe-agent-workflow/uniapp │
│  安装：./tools/install.sh <pc|uniapp> <业务项目路径>      │
│  保留：业务项目 project-conventions.md                   │
│  内核同步：docs/agent-kernel-sync.md（pc ↔ uniapp）       │
│  版本：manifest → platform / kernelVersion / bundleVersion│
│  业务仓 .cursor = 安装产物，规范改动请回写权威仓          │
└──────────────────────────────────────────────────────────┘
```

---

*平台专属培训：PC → `pc/docs/agent-workflow-training.md`；uni-app → `uniapp/docs/agent-workflow-training.md`。*
