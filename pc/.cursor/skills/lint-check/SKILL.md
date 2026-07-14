---
name: lint-check
version: 1.0.1
description: 执行 ESLint 检查并修复未使用引入、no-unused-vars 等；交付前零 error。 用户说 lint、eslint、未使用引入时触发；大批量改码后自动衔接。
---
# Lint 检查与修复

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **目标：** 改动涉及的源码 **ESLint 零 error**，优先删除未使用引入与变量，最小 diff 修复。
>
> **时机：** 大批量改码、重构、新建/增量功能 **编码完成后**、**build 之前或之后**（与 build 一并作为交付门禁）。

---

## 触发场景

- `rules-refactor`、`code-normalize`、`vue2-to-vue3-refactor` 每批或最终闭环
- `feature-dev-workflow`、`incremental-feature`、`page-refactor` 改码完成
- `feature-verify` 命令验证环节
- 用户说「跑 lint」「修 eslint」「未使用引入」
- `ci-fix` 若失败日志为 ESLint 报错

**不触发：** 纯问答、只读 review（`code-review` 可提示 lint 问题但不强制跑命令）。

---

## 与 ci-fix 边界

| | `lint-check` | `ci-fix` |
|---|--------------|----------|
| 范围 | ESLint / 代码风格 / 未使用符号 | build、test、类型编译 |
| 命令 | `npm run lint-fix` 或 `package.json` 中 lint 相关 script | `npm run build`、`pnpm test` 等 |
| 顺序 | 改码后 → **lint** → build | build/test 失败时 |

二者可串联：**lint 绿 → build 绿**。

---

## 流程

```
① 读 package.json scripts → ② 跑 lint → ③ 分类 → ④ 最小修复 → ⑤ 重跑至零 error → ⑥ 交付
```

### ① 确认 lint 命令

**必须先 Read** `package.json` `scripts`：

| 本项目（Vue CLI） | 命令 |
|-------------------|------|
| 检查并自动修复 | `npm run lint-fix` |

其他项目常见：`pnpm lint`、`npm run lint`、`eslint --fix ...` — **以 package.json 为准**，禁止臆造 script 名。

### ② 执行 lint

```bash
npm run lint-fix
```

若无 `--fix` 专用 script，先跑 lint，再对可安全 auto-fix 项使用 `--fix`。

### ③ 失败分类与修复原则

| 规则 | 典型信号 | 处理 |
|------|----------|------|
| **未使用引入** | `'X' is defined but never used` | **删除** import 行或具名导入项 |
| **未使用变量** | `'X' is assigned a value but never used` | 删除声明；确需占位用 `_` 前缀（项目允许时） |
| **未使用表达式** | `no-unused-expressions` | 改为显式 `if` / 赋值，勿留短路副作用表达式 |
| **其他** | 见 ESLint 规则名 | 最小改动对齐项目 `.eslintrc` |

**铁律（与 rules 一致）：**

- **删除未使用引入** — 重构/删代码后 import 必须同步清理，不得留 dead import
- **禁止**为消 lint 而：`eslint-disable` 整文件、关规则、改 `.eslintrc` 降标准
- **禁止**借机大范围格式化无关文件
- 第三方组件 JSX 类型错误（若项目约定忽略）— 不扩大修复范围

### ④ 最小修复

1. 按报错 **文件 + 行号** Read 源文件
2. 优先删未使用 import / 变量（最常见于大批量重构后）
3. 仅改 lint 报错相关行；不重构业务逻辑
4. 修复后 **重跑 lint**，直至 **0 errors**

### ⑤ 与 build 串联（推荐）

大批量任务闭环顺序：

```bash
npm run lint-fix   # 或项目等价命令
npm run build
```

`rules-refactor` / `feature-verify` 交付前：**lint 与 build 均须通过**（项目有 lint script 时）。

### ⑥ 交付检查

**汇报内容**

1. lint 命令与结果（error 数 → 0）
2. 修改文件列表 + 每项规则（如 `no-unused-vars`）
3. 若与 build 串联：build 是否通过

**交付首行示例：**

```
Lint：7 errors → 0 | 删除未使用引入 5 处 | lint-fix ✅ build ✅
```

**门禁**

- [ ] ESLint 零 error 已确认

---

## 规范预加载

- 改 Vue/JS 业务代码时：Read [rules-activation.md](../shared/rules-activation.md) 基线
- **必读** `前端通用代码规范.mdc` §代码质量 — 删除未使用引入

---

## 衔接 Skills（完成后自动执行 lint-check）

| 前置 Skill | 衔接时机 |
|------------|----------|
| `rules-refactor` | 每批改码后 + 最终验收前 |
| `code-normalize` | ⑥ 全量验收前 |
| `feature-dev-workflow` | ④ 编码验收前 |
| `incremental-feature` | 改码完成、交付前 |
| `page-refactor` | 拆分完成、build 前 |
| `feature-verify` | ⑥ 命令验证（与 build 并列） |
| `vue2-to-vue3-refactor` | 每批 + 最终闭环 |

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ npm run lint-fix + 手动清残留 error
- 🚫 eslint-disable 整文件
