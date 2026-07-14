# fe-agent-workflow

HiShop 前端 Agent 工作流**权威源**（Cursor rules + skills + SDD 文档）。

两套平台**并列维护，不拆公共内核目录**；内核级变更按 `docs/agent-kernel-sync.md` 在 `pc` ↔ `uniapp` 之间同步。

## 文档

| 文档 | 说明 |
|------|------|
| [docs/vue3-migration-guide.md](docs/vue3-migration-guide.md) | **Vue2→Vue3 迁移 SDD**（固定 slug `vue3-migration`） |
| [docs/project-refactor-guide.md](docs/project-refactor-guide.md) | **全项目重构 SDD**（固定 slug `project-refactor`） |
| [docs/agent-workflow-repo-guide.md](docs/agent-workflow-repo-guide.md) | **统一仓培训**（install、权威源、内核同步） |
| [docs/agent-kernel-sync.md](docs/agent-kernel-sync.md) | pc ↔ uniapp 内核同步清单 |
| `pc/docs/agent-workflow-training.md` | PC 平台培训 |
| `uniapp/docs/agent-workflow-training.md` | uni-app 平台培训 |

## 目录

```
fe-agent-workflow/
├── README.md
├── docs/                 # 跨平台说明（同步清单）
├── tools/
│   └── install.sh        # 安装到业务项目
├── pc/                   # platform: pc（中后台 Vue）
│   ├── .cursor/
│   │   ├── rules/
│   │   ├── skills/
│   │   └── components/   # HiTable 等
│   └── docs/             # constitution、features 模板、培训文档
└── uniapp/               # platform: uniapp（移动端）
    ├── .cursor/
    └── docs/
```

## 安装到业务项目

### 本地已 clone（维护者常用）

```bash
# 中后台
./tools/install.sh pc /path/to/HiStore-store-pc

# uni-app 移动端
./tools/install.sh uniapp /path/to/HiStore-mall-mobile

# 可选：同步 SDD 文档模板
./tools/install.sh uniapp /path/to/HiStore-mall-mobile --with-docs
```

### 直接从 Git 安装（无需本地 clone）

权威仓：https://github.com/TieZhuzhu/fe-agent-workflow

**推荐：一键远程安装**（克隆 → 安装 → 自动清理）

```bash
# curl 一键安装
curl -fsSL https://raw.githubusercontent.com/TieZhuzhu/fe-agent-workflow/master/tools/remote-install.sh \
  | bash -s -- uniapp /path/to/HiStore-mall-mobile --with-docs

# 或本地已有脚本时：
bash tools/remote-install.sh uniapp /path/to/HiStore-mall-mobile --with-docs

# 指定分支或 tag
bash tools/remote-install.sh uniapp /path/to/HiStore-mall-mobile \
  --ref master --with-docs
```

**或使用 install.sh + --from-git**：

```bash
bash tools/install.sh uniapp /path/to/HiStore-mall-mobile \
  --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git \
  --with-docs

# 指定分支或 tag
bash tools/install.sh uniapp /path/to/HiStore-mall-mobile \
  --from-git https://github.com/TieZhuzhu/fe-agent-workflow.git \
  --ref master \
  --with-docs
```

`--from-git` / `remote-install.sh` 自动识别 **独立仓**（根目录即工作流，推荐）与 **父仓嵌套**（`fe-agent-workflow/` 子目录）两种布局。

将 `pc/.cursor` 或 `uniapp/.cursor` **整包覆盖**到目标项目根目录的 `.cursor/`（保留目标项目已有的 `project-conventions.md`）。

## 日常维护

| 场景 | 做法 |
|------|------|
| 改 PC 规范 / Skill | 编辑 `pc/`，`install.sh pc …` |
| 改 uni-app 规范 / Skill | 编辑 `uniapp/`，`install.sh uniapp …` |
| 改 SDD 流程 / 通用 Skill（内核） | 在一端改完 → 按 `docs/agent-kernel-sync.md` 同步到另一端 → 两端分别 install |
| 业务项目约定 | **不要**提交到本仓；在业务项目跑 `project-bootstrap` 生成 `project-conventions.md` |

## 版本字段

各平台 `manifest.json`：

- `platform`: `pc` | `uniapp`
- `kernelVersion`: 内核版本（两端应对齐）
- `bundleVersion`: 本平台整体版本

校验：

```bash
python3 pc/.cursor/skills/scripts/skills-version.py check
python3 uniapp/.cursor/skills/scripts/skills-version.py check
```

## 业务仓库

| 平台 | 消费项目 |
|------|----------|
| pc | `HiStore-store-pc` |
| uniapp | `HiStore-mall-mobile` |

业务仓 `.cursor` 视为**安装产物**；流程变更请在本仓修改后执行 `install.sh`。
