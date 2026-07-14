---
name: bugfix-workflow
version: 1.3.1
description: 四阶段系统化调试（复现→假设→验证→修复）前端 Bug；MCP 可用时实点，否则静态读码+用户证据。 用户说【bug】、报错、异常、点击无反应时触发。
---
# Bug 排查与修复

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **与 feature-e2e-verify 分工：** 本 Skill 是**问题驱动**的排查修复；`feature-e2e-verify` 是**验收驱动**的对照 `e2e.md` 跑 P0。

## 流程（四阶段 + 回归）

```
① 规范预加载
② Phase 1 复现 → Phase 2 假设 → Phase 3 验证 → Phase 4 修复
③ ⑥ 回归
```

> **四阶段为强制 checklist**（借鉴 Superpowers systematic-debugging）。每阶段未完成不得进入下一阶段改码。

---

### ① 规范预加载

改码前 Read [rules-activation.md](../shared/rules-activation.md)：**至少通用基线**；涉及表单/路由/复杂页时再读对应 rule。简单 bugfix **可省略**预加载计划。

### ② 表象分类（Phase 1 前置）

| 表象 | 典型话术 | 推荐路径 |
|------|----------|----------|
| **交互无响应** | 「xxx 点击没反应」 | MCP 实点 → 静态读 `@click`/遮罩/`v-if` |
| **交互结果错** | 「点了但跳错页」 | MCP + network；静态读数据流 |
| **白屏 / 不渲染** | 「页面空白」 | console 栈 → services → 模板条件 |
| **接口 / 数据错** | 「字段不对」 | services + 响应对照 |
| **纯构建 / 类型** | build 报错 | 静态读码 |
| **样式错位** | 「布局乱了」 | 截图 + CSS |

**信息不足时**一次问清：URL/path、步骤、预期 vs 实际、是否必现、最近改码、console/network。

---

## 四阶段系统化调试（强制）

### Phase 1 — 复现 Reproduce

**门禁：** 未完成本阶段不得改业务代码。

```markdown
## Phase 1 复现

- [ ] 最小复现步骤（≤5 步）已记录
- [ ] 预期 vs 实际已写明
- [ ] 环境：path / 分支 / 是否 mock / dev URL
- [ ] 证据来源：MCP / 用户粘贴 / 静态推演
- [ ] 必现 or 偶现
```

**MCP 实点**（可用时，见下文 §③-A）产出《复现笔记》；**无 MCP** 时用户粘贴 console/network 或静态推演步骤。

---

### Phase 2 — 假设 Hypothesize

**门禁：** 至少 2 个可能根因，标注最可能 1 个。

```markdown
## Phase 2 假设

| # | 假设 | 可能性 | 验证方式 |
|---|------|--------|----------|
| 1 | 未绑定 @click / handler early return | 高 | 读模板 + MCP 点按无 network |
| 2 | 接口 4xx 导致静默失败 | 中 | Network 面板 |
| 3 | 列表未 reload | 中 | 读 loadList 调用链 |
```

**分类提示：**

| 观察 | 假设方向 |
|------|----------|
| 无按钮 | v-if、权限、路由错页 |
| 点后无变化、无 network | 未绑定、遮罩、disabled |
| network 4xx/5xx | services、token、参数 |
| 200 但 UI 不变 | 赋值字段错、未 reload |
| console 报错 | 栈顶文件打断 handler |

---

### Phase 3 — 验证 Verify hypothesis

**门禁：** 用证据确认或排除 Phase 2 最可能假设；**禁止**无证据改码。

```markdown
## Phase 3 验证

- [ ] 假设 1：已确认 / 已排除（证据：文件:行 或 network）
- [ ] 假设 2：已确认 / 已排除
- [ ] 根因结论：（一句话，须有证据引用）
```

**证据优先级：** MCP snapshot/network > 用户 console/network > 静态读码推演

---

### Phase 4 — 修复 Fix

**门禁：** 仅针对 Phase 3 确认的根因做**最小 diff**。

- 只改与 bug 相关的符号/文件
- 不借机重构无关代码
- 保持项目 Vue 版本写法（Vue 2 Options API / Vue 3 Composition API）
- 接口字段问题同步 types / JSDoc

---

### ③ 收集证据（MCP 优先，非强制）

**原则：** 修复前须有**至少一类**可核对证据，来源不限于 MCP：

| 证据类型 | 适用 | 说明 |
|----------|------|------|
| **Browser MCP** | UI/交互类，环境可用时 | 首选，能直接观察 DOM/network |
| **用户粘贴** | 任意 | console 报错栈、Network 请求/响应、操作录屏描述 |
| **静态读码** | 任意 | 读 Vue/services/路由，推演数据流与事件绑定 |
| **终端日志** | 构建/类型/接口 | build 输出、curl（**不**用于验证「点击无反应」） |

**探针顺序（建议，非门禁）：**

```
Browser MCP 可用？
  ├─ 是 → ③-A MCP 实点（交互类推荐）
  ├─ 否 / 失败 → ③-B 静态 + 用户证据（正常路径，非次等）
  └─ 证据仍不足 → 向用户索要 console/network，或做最小试探修复并标注待验证
```

**禁止：** 在**无任何证据**（无 MCP、无用户材料、未读相关代码）的情况下大面积改代码或声称「已修复」。

#### A. Browser MCP 实点（**推荐**，可用时）

**适用：** 点击无反应、弹层不出现、表单不提交、路由不跳、数据不刷新等运行时行为问题。

**MCP 失败处理：** 记录失败原因（errored、超时、无法登录等），**立即切换 ③-B**，不要求用户必须先修好 MCP 才能继续排查。

**实点流程（以「xxx 点击没有反应」为例）**

1. **Read** Browser MCP tool schema（`browser_navigate` / `browser_snapshot` / `browser_click` / `browser_network` 等）
2. **打开页面**：`browser_navigate` → 用户给的 URL 或 `project-conventions.md` 中 dev 入口 + path
3. **开网络采集**（涉及提交/加载时）：`browser_network` action `on`
4. **快照基线**：`browser_snapshot`（compact）
5. **实点操作**：`browser_click` ref；无 ref 则 `browser_scroll` 后再 snapshot
6. **观察结果**：再次 snapshot / network capture / screenshot（可选）
7. **记录《复现笔记》**：

```markdown
## Bug 复现笔记

- 表象：xxx 点击没有反应
- 证据来源：MCP
- URL：...
- 操作：点击「xxx」(@ref)
- 预期：...
- 实际：snapshot 前后无变化 / 无 network 请求 / 有请求但 4xx
- 控制台：...
- 网络：...
```

**「点击无反应」常见根因对照（观察 → 代码方向）**

| 观察 | 可能根因 | 代码排查方向 |
|------|----------|--------------|
| **无该按钮** | 权限 v-if、条件渲染、路由错页 | 模板 `v-if`、菜单/路由 |
| 有按钮，点后 **无变化、无 network** | 未绑定 handler、遮罩、`disabled` | `@click`、z-index、`pointer-events` |
| **network 4xx/5xx** | 接口错、未登录、参数错 | `services`、`request` 拦截器 |
| **200 但 UI 不更新** | 未赋值、错字段、列表未 refresh | 赋值、`handleSearch`、`data-key` |
| 点击后 **跳错页** | 路由 path、query 错误 | `router.push`、`$route` |
| **控制台报错** | 运行时异常中断 handler | 报错栈对应文件行 |

**选择器优先级：** `data-testid` → role + name（snapshot）→ 稳定文案。

**登录：** 使用用户提供的测试账号或已登录会话；**禁止**密码入库。

#### B. 静态降级 / 用户证据（**与 MCP 同等有效**）

**触发：** MCP 不可用、MCP 实点失败、用户未开 dev 环境、或问题已有明确 console/build 栈。

1. **Read 相关 Vue/JS/services** 文件，按用户步骤静态推演
2. 结合用户提供的 **console 报错、Network 面板、截图** 定位
3. 输出根因假设；**最小修复**；交付中标注 `MCP: 未使用` 及验证方式（用户待点 / lint / build）
4. 可选：提示用户若需浏览器复现可配置 MCP（Node≥18 + 重启 MCP），**不阻塞**当前修复

**静态排查清单（交互类无 MCP 时）**

- [ ] 目标元素是否有 `@click` / `v-on` 绑定（Vue 2 注意 `.native`）
- [ ] 是否被 `v-if` / `v-show` / 权限逻辑隐藏
- [ ] 是否有全屏遮罩、`pointer-events: none`、`disabled`
- [ ] handler 内是否 early return、未 `await`、异常被吞
- [ ] 提交后是否调用了列表 `reload` / 赋值是否用了错字段
- [ ] 最近 diff 是否改动了相关文件

#### C. 通用收集项

- 页面路由 / 完整操作步骤
- 预期 vs 实际
- 是否最近有相关代码变更
- 接口响应（MCP network 或用户粘贴）

---

### ④ 定位根因

**已并入 Phase 2～3。** 本步 = Phase 3 结论确认后进入 Phase 4。

---

### ⑤ 最小修复

**已并入 Phase 4。**

---

### ⑥ 回归检查

**交互类 bug：** MCP 可用时 **建议** 复点同一操作；不可用时由 **用户确认** 或基于静态证据 + lint/build 回归。

- [ ] 原问题已解决（MCP 复点 / 用户确认 / 构建与逻辑推演一致）
- [ ] 同页主流程未破坏（列表/提交/返回）
- [ ] 无新增 console.error（MCP 或用户反馈）
- [ ] 符合 `.cursor/rules/*.mdc`
- [ ] 若 feature 有 `e2e.md`，可选跑 [feature-e2e-verify](../feature-e2e-verify/SKILL.md) P0

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 先收集运行时证据再改码
- 🚫 无证据大范围重构

## 交付检查

**汇报模板**

```markdown
## Bugfix 报告

### 四阶段摘要
- Phase 1 复现：（≤5 步 + 预期/实际）
- Phase 2 假设：（列出 2～3 个，最可能：…）
- Phase 3 验证：（根因 + 证据 文件:行 / network）
- Phase 4 修复：（文件列表）

- 表象：...
- 根因：（一句话）
- 证据：MCP / 用户 console / 静态读码
- 修改：...
- 回归：MCP 复点 / 用户待验证 / lint+build
```

**交付首行：** `Bugfix: <模块/页面> | 四阶段完成 | 根因摘要 | 证据: MCP / 静态+用户`

**门禁**

- [ ] 根因与验证步骤已说明
- [ ] `npm run lint-fix`（若改码）
- [ ] 上文 §回归 清单已对照

## 禁止

- **无任何证据**就大面积改代码或声称「已在浏览器验证」
- 用 **curl** 代替浏览器验证「点击无反应」类问题（curl 不能验证 DOM 事件）
- 混淆 **bugfix-workflow**（排查修复）与 **feature-e2e-verify**（验收清单）
- **因 MCP 不可用而拒绝排查**——应降级静态读码继续
- Agent Shell `nvm use` 误认为已修复 Browser MCP（见 feature-e2e-verify §B）
- 未定位根因就重构整页

---

## 话术示例

```
【bug】订单列表「查询」点击没反应，path /trade/manage，本地 http://localhost:8101/store/
```

```
【bug】商品详情加购后购物车数字不更新，控制台无报错，帮静态排查并修
```
