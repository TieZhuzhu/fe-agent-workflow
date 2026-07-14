---
name: ci-fix
version: 1.0.1
description: 修复构建与测试失败。pnpm build、pnpm test、vue-tsc 类型检查、Vite 编译报错时触发。在失败日志基础上最小改动修复，循环重跑直到通过。用户说「CI 挂了」「build 失败」「test 挂了」时使用。
---
# 构建 / CI 修复

> 目标：**用项目真实命令把 build / test 跑绿**，不做无关重构。思路参考 PR babysit 的 CI 环节，但聚焦本地与当前分支改动。

## 触发场景

- `pnpm build` 失败
- `pnpm test`（`vitest run`）失败
- 类型错误导致编译失败（`vue-tsc`、Vite TS 检查）
- PR / 流水线报构建或测试红

**不触发：** 页面交互 bug（`bugfix-workflow`）；仅为通过而改 CI 配置或降标准。

---

## 流程

```
① 复现 → ② 分类 → ③ 最小修复 → ④ 重跑 → ⑤ 交付
```

### ① 复现（强制先跑）

**必须先 Read** `package.json` `scripts`，再执行失败命令：

```bash
# 按 package.json 实际 scripts 为准，例如：
pnpm test
pnpm build
```

记录：

- 完整报错栈（首个 error 优先）
- 失败文件路径与行号
- 是否仅本次改动引入（`git diff`）

**环境：**

- Vite 5+ / 6 通常需 **Node 18+ 或 20+**；若报 `crypto.getRandomValues` / `import.meta` 等，先确认 `node -v`
- 依赖异常时：`pnpm install` 后重试（勿随意升级 major 依赖）

### ② 失败分类

| 类型 | 典型信号 | 处理方向 |
|------|----------|----------|
| **类型** | `TS23xx`、`vue-tsc`、props 不匹配 | 改 types / 调用处，不删类型 |
| **导入** | `Cannot find module`、`is not exported` | 对齐路径 alias、export |
| **运行时测试** | `vitest` assertion failed | 修逻辑或更新测试（须说明业务依据） |
| **构建** | Vite rollup、chunk、SCSS | 改引用或配置，最小范围 |
| **缺失导出** | `export 'Xxx' was not found` | 对齐 services 实际 export 或修正 import 路径 |
| **快照** | snapshot mismatch | 确认预期变更后再更新 snapshot |

**原则：**

- 先修**根因文件**，不堆 `// @ts-ignore`
- 测试失败：区分「代码错了」vs「测试过时」；后者须写明原因再改测试
- **禁止**为通过而：删用例、改 CI workflow、关闭严格检查、大范围格式化

### ③ 最小修复

1. Read 报错涉及的源文件与测试文件
2. 只改与失败相关的符号/文件
3. 不借机重构无关模块
4. 若失败与当前 PR **无关**：先 `git merge` / `rebase` 最新主分支再重跑（可能已被他人修复）

### ④ 重跑循环

修复后**按顺序**重跑（除非用户指定只修 test）：

```bash
npm run lint-fix   # 若有 lint script；ESLint 报错时也可走 lint-check
pnpm test
pnpm build
```

- 仍有失败 → 回到 ②，直到全绿或遇到需用户决策的冲突
- 不提交除非用户要求

### ⑤ 交付

1. **根因**一句话
2. 修改文件列表
3. 重跑结果（test / build 是否通过）
4. 若需用户决策：是否更新测试预期、是否后端字段变更

---

## 与 bugfix-workflow 的区别

| | `bugfix-workflow` | `ci-fix` |
|---|-------------------|----------|
| 现象 | 页面/接口/交互不对 | 命令行 build/test 红 |
| 手段 | 浏览器复现、网络面板 | 终端日志、vitest、vite |
| 验收 | 手动点页面 | `pnpm test` + `pnpm build` 绿 |

二者可串联：先 `ci-fix` 跑绿，再手动验页面。

---

## 常见命令速查

| 命令 | 说明 |
|------|------|
| `pnpm test` | 以 `package.json` 为准，常见为 `vitest run` |
| `pnpm build` | 以 `package.json` 为准，常见为 `vite build` |
| `pnpm dev` | 本地开发（一般不用于 CI 修复结论） |

当前无 `lint` script 时不要臆造 `pnpm lint`；以 `package.json` 实际 scripts 为准。ESLint 专项修复走 Skill **`lint-check`**。

---

## 规范预加载

- **可省略**预加载计划
- 改业务代码时：若触及 Vue/TS 页面，Read `rules-activation.md` 基线
- 纯测试断言 / 类型修补：可不读页面 rules

---

## 交付首行示例

```
CI 修复：vitest 1 failed → 修正 permission.test 期望值 | test ✅ build ✅
```
