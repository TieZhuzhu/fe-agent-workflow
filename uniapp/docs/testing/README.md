# 验收分层（uni-app 移动端）

> 与 `.cursor/skills` 配套；**不绑定某一业务仓库**。具体命令以各项目 `package.json` / `project-conventions.md` 为准。

## 三层模型

```
L3  feature-e2e-verify     浏览器 P0 冒烟（Browser MCP → Playwright → 人工）
L2  api-smoke               测试环境 curl 接口探针
L1  feature-verify          SDD + lint + build (+ test:unit 可选)
```

| 层 | 验证什么 | 抓 AI 哪类问题 |
|----|----------|----------------|
| L1 | 需求是否写进代码、能否编译 | 漏字段、目录错、未使用引入 |
| L2 | 真实接口 JSON 形状 | URL/分页/嵌套解包错、spec drift |
| L3 | 能点、能看、主流程通 | 路由、交互、UI 绑定错 |

**任一层不能单独代表「可上线」**；L1 是门禁，L2/L3 按环境可选加强。

## 推荐话术

| 目的 | 话术 |
|------|------|
| 静态 + 构建 | `【verify】<slug>` |
| 接口探针 | `【api-smoke】<slug>` 或联调后「curl 探针验证」 |
| UI 冒烟 | `【verify-e2e】<slug>` |
| 补单测 | 「给 `<path>/utils` 写单测」→ `unit-test-codegen` |

## L2 说明（api-smoke）

- **仅 curl**：Agent 通过 Shell 执行，需 test 环境与鉴权（token **不入库**）
- 无环境 → skip，不冒充 pass

## L3 说明（feature-e2e-verify）

探针顺序（**须按序，不得跳步**）：

1. **Browser MCP**（首选）— 可用性看 Cursor MCP 进程，**不是** Agent Shell 的 `node -v`
2. MCP errored → **用户侧** `nvm alias default 20` + **Settings → MCP 重启**（或重启 Cursor）；Agent Shell `nvm use` **不能**代替此步
3. 仍不可用 → **Playwright**（Agent Shell 内 `nvm use 20` + `npx playwright`）
4. 均失败 → skip + `e2e.md` 人工步骤

**常见误区：** 用户在终端 `nvm use 20` 后 MCP 已好，但 Agent 会话里 MCP 仍显示 errored → 需 **重载 MCP 或新开 Agent 对话** 后再跑 `【verify-e2e】`。

## Feature 文档

新建 P0 功能建议在 `docs/features/<slug>/` 增加：

- `e2e.md` — 模板 [`../features/_template/e2e.md`](../features/_template/e2e.md)

## Skill 索引

| Skill | 文件 |
|-------|------|
| feature-verify | `.cursor/skills/feature-verify/SKILL.md` |
| api-smoke | `.cursor/skills/api-smoke/SKILL.md` |
| feature-e2e-verify | `.cursor/skills/feature-e2e-verify/SKILL.md` |
| unit-test-codegen | `.cursor/skills/unit-test-codegen/SKILL.md` |
