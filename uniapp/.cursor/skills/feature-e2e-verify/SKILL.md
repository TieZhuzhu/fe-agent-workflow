---
name: feature-e2e-verify
version: 1.0.1
description: Feature UI/交互冒烟验收。对照 e2e.md 在 H5 浏览器或微信开发者工具执行 P0 路径。优先 Browser MCP；不可用则人工清单。
---
# Feature E2E 冒烟验收

> **定位：** L3 — 验证关键路径可点、可渲染。  
> **环境：** H5 用 Browser MCP；小程序用开发者工具或真机；App 用模拟器。  
> **路径示例：** 首页 → 商品列表 → 详情 → 加购 → 下单

---

## 触发场景

- `【verify-e2e】<feature-slug>`
- `feature-verify` PASS 后，用户要求 UI 回归
- 大改列表/表单/路由后，需确认主流程可点
- spec 中 Given/When/Then 需**运行时**验证

**不触发：** 纯 utils/refactor 无 UI；用户禁止浏览器自动化。

---

## 与 feature-verify 的关系

| | feature-verify | feature-e2e-verify（本 Skill） |
|---|----------------|--------------------------------|
| 对照物 | spec/design/field-map/tasks、lint/build | `e2e.md` + spec 主流程 |
| 环境 | 本地命令 | 浏览器 + 可访问 dev/test |
| 无 Browser MCP | 仍可做 L1 | 先按 §② 修复环境；仍失败则 **skip E2E** 或 Playwright 降级 |

推荐顺序：

```
feature-verify（L1）→ api-smoke（L2，可选）→ feature-e2e-verify（L3，可选）
```

---

## 流程

```
① 定位 feature + e2e.md → ② 浏览器探针门禁 → ③ 执行 P0 场景 → ④ 截图/日志 → ⑤ 报告
```

探针优先级（**须按序尝试，不得跳步**）：

```
Browser MCP 可用？（Read descriptors，非 STATUS errored）
  ├─ 否 → 提示用户 B1：本机 nvm default 20 + 重启 MCP/Cursor（Agent Shell nvm 不能修 MCP）
  ├─ 用户已修复 → 重试 A
  ├─ 仍否 → Playwright（Shell 内 bash -lc 'nvm use 20; …'）
  └─ 仍否 → E2E SKIP + 人工清单
```

### ① 定位工件

- `docs/features/<slug>/e2e.md` — **P0 可执行步骤**（无则 Read `spec.md` §验收场景 临时生成，并建议补录 e2e.md）
- `design.md` — path、页面入口
- `project-conventions.md` — 登录 URL、publicPath、默认账号说明（**不含密码入库**）

`e2e.md` 模板见 [docs/features/_template/e2e.md](../../../docs/features/_template/e2e.md)。

### ② 浏览器探针门禁（强制按序）

#### A. Browser MCP（首选）

1. Read MCP tool descriptors（`plugin-browse-browser` 等）
2. **可用** → 继续 ③，报告中标注 `MCP: Browser`
3. **不可用 / errored** → 进入 B，**不得**直接 skip 或报 PASS

#### B. Node 版本与 Browser MCP（重要：两套环境）

Browser MCP **要求 Node.js ≥ 18**，但 **Agent Shell 里的 `nvm use` 不会自动修复 Browser MCP**。

| 环境 | 谁控制 | `nvm use 20` 是否生效 |
|------|--------|----------------------|
| **Browser MCP 进程** | Cursor 启动 MCP 时用的 Node（IDE 进程 / 启动 Cursor 时的 PATH） | ❌ Agent 在 Shell 里切换**无效** |
| **Agent Shell**（Playwright、`npm run` 等） | 每次 `Shell` 工具调用的子进程 | ✅ 须在命令前 `nvm use 20` |

**B1. 修复 Browser MCP（须用户侧或重载 MCP，Agent 不能单靠 Shell 完成）**

1. 用户在**本机终端**（非仅 Agent Shell）执行：
   ```bash
   nvm ls
   nvm use 20          # 或 nvm alias default 20
   node -v             # 确认 >= 18
   ```
2. **重启 Browser MCP**：Cursor **Settings → MCP** → 重启 `browser` 服务；仍失败则 **完全退出并重新打开 Cursor**（若从终端启动 Cursor，须在 `nvm use 20` 之后启动）
3. Agent **回到 A** 再读 MCP descriptors；`tools/*.json` 出现且非 `STATUS.md errored` 才算可用

**B2. Agent Shell 探针（仅服务于 Playwright 降级，不修复 MCP）**

执行 Playwright / `npm` 前，Agent 须在**同一条** Shell 命令内切换 Node：

```bash
bash -lc 'export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 20; node -v; …'
```

- 不得在报告里写「已 nvm use 20」就认定 Browser MCP 已修复
- `nvm ls` 无 ≥18 → 提示用户 `nvm install 20` 后走 B1

**B3. MCP 仍 errored** → 进入 C（Playwright）；报告中须写明「MCP Node 与 Shell Node 可能不一致」

#### C. Playwright 降级（仅 A+B 仍失败）

- 用 **Shell + Playwright**（如 `npx playwright` 一次性脚本）执行 `e2e.md` P0 步骤
- **不得**用 curl 代替浏览器点击验收
- 报告中标注 `MCP: Playwright (fallback)`

#### D. 均不可用

- Verdict: `E2E SKIP`
- 输出《人工冒烟清单》（逐步来自 e2e.md）
- 注明已尝试：Browser MCP（含 Node 修复）/ Playwright

### ③ 执行 P0 场景（Browser MCP 或 Playwright 可用时）

**范围控制：**

- 仅跑 `e2e.md` 中标记 **P0** 的场景（默认 ≤5 步/场景）
- 不写操作：删库、批量导出生产、真实支付
- 登录：使用用户提供的测试账号或已登录会话；**禁止**把密码写入仓库

**每场景记录：**

| 步骤 | 操作 | 期望 | 实际 | 结果 |
|------|------|------|------|------|
| 1 | 打开 `/module/page` | 列表渲染 | | pass/fail |

**可选：**

- 关键步骤截图（存对话/附件，**不默认** commit 到仓库）
- 控制台 error（过滤已知第三方噪音）

**选择器优先级：**

1. `data-testid`（design 推荐新增）
2. role + accessible name
3. 稳定文案（避免 volatile 数字/时间）

### ④ 失败处理

- fail → 区分：前端 bug（`bugfix-workflow`）、环境/数据（标注 blocker）、用例过时（更新 e2e.md）
- 不通过时 **不可 archive**

### ⑤ 报告

```markdown
## Feature E2E: <slug>

| 场景 | 结果 | 备注 |
|------|------|------|
| P0-1 列表加载 | pass/fail/skip | |

- MCP: Browser / Playwright (fallback) / skip
- Node（验收时）: vXX（若曾切换 nvm 须记录）
- 控制台 fatal: 有/无

### Blockers
- ...

### 人工补测（若 skip）
1. ...
```

**交付首行：**

```
Feature E2E: <slug> | PASS/FAIL/SKIP | P0 x/y | Browser/Playwright/skip
```

---

## 何时编写 e2e.md

| 时机 | 动作 |
|------|------|
| `feature-spec` | P0 新建页建议同时起草 `e2e.md`（可与 spec 场景同步） |
| `feature-dev` 完成 | 补全选择器、测试数据说明 |
| `verify-e2e` 首次 skip | 从 spec 生成人工清单并回写 e2e.md |

---

## 禁止

- 未区分 **MCP Node** 与 **Shell Node**，误以为 Agent `nvm use` 可修复 Browser MCP
- 未尝试 Browser MCP + 用户侧重载，直接 Playwright 或 skip
- 无 Browser MCP / Playwright 却报 E2E PASS
- 全站截图 pixel diff 作为默认门禁（成本高，仅用户明确要求）
- 在 E2E 中依赖生产环境或真实用户数据
- 用 E2E 替代 api-smoke 的 JSON 结构验证
