---
name: unit-test-codegen
version: 1.0.1
description: 为 utils、toXxxParams、constants、services 生成单元测试（Vitest/Jest 按 package.json）。 用户说写单测、补测试、test:unit 时触发；不默认 E2E。
---
# 单元测试生成（Unit Test）

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **定位：** 补强 L1 — 防止 **纯逻辑 / 参数组装** 回归；**不替代** api-smoke、feature-e2e-verify。  
> **默认策略：** 以 `project-conventions.md` §测试策略 为准。当前 **`pending`**（无 test script，不强制先测后码）；`strict` 时须 RED-GREEN-REFACTOR。

---

## 触发场景

- 「给这个 utils / hook 写单测」
- 「补 test:unit」
- `feature-verify` 中 test 维度为 required
- PR 要求覆盖某模块

**不触发：** 用户未要求且 verify 未强制 test；应用 E2E 替代 utils 单测的误判。

---

## 步骤 0：判定测试栈

**Read `package.json`：**

| 信号 | 栈 |
|------|-----|
| `vitest` in devDependencies | **Vitest** |
| `jest` + `@vue/vue2-jest` / `vue-jest` | **Jest（Vue 2 常见）** |
| `@vue/cli-plugin-unit-jest` | **Vue CLI Jest** |
| 无任何 test 依赖 + `vue@2.x` | 建议 Jest + `@vue/test-utils@1`（交付「基建建议」，不擅自装 major 除非用户要求） |
| 无任何 test 依赖 + `vue@3.x` | 建议 Vitest + `@vue/test-utils@2` |

**Read `project-conventions.md`（若存在）** 是否已有 `test` / `test:unit` script。

无 script → 见 [§测试基建初始化](#测试基建初始化)。

---

## 优先测什么（ROI 序）

| 优先级 | 目标 | 示例 |
|--------|------|------|
| 🔴 高 | 纯函数 utils | `toListParams`、`formatStatusClass` |
| 🔴 高 | constants 映射表 | 枚举 → label |
| 🟡 中 | services 调用 | mock request，断言 url/method/data **形状** |
| 🟡 中 | composable / hook（Vue 3） | 列表 reload、表单校验 |
| 🟢 低 | 完整 SFC 渲染 | mock UI 库，成本高 |
| ⛔ 不做 | 真实 HTTP | 走 `api-smoke` |
| ⛔ 不做 | 跨页浏览器流 | 走 `feature-e2e-verify` |

---

## 文件位置

与源码**同目录**或 `__tests__`（以项目已有约定为准）：

```
views/<module>/<page>/
├── utils.ts
├── utils.test.ts          # 或 __tests__/utils.test.ts
├── services.ts
└── services.test.ts       # mock request

src/utils/formatXxx.ts
└── formatXxx.test.ts
```

Vue 2 项目无 TS 时：`utils.test.js`。

---

## Vitest（Vue 3 默认）

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { toListParams } from './utils'

describe('toListParams', () => {
  it('原样透传 pageNo pageSize', () => {
    expect(toListParams({ pageNo: 1, pageSize: 20, name: 'a' })).toEqual({
      pageNo: 1,
      pageSize: 20,
      name: 'a',
    })
  })
})
```

**mock services：**

```ts
vi.mock('./services', () => ({
  GetList: vi.fn(),
}))
```

---

## Jest（Vue 2 常见）

```js
import { toListParams } from './utils'

describe('toListParams', () => {
  it('原样透传 pageNo pageSize', () => {
    expect(toListParams({ pageNo: 1, pageSize: 20 })).toEqual({
      pageNo: 1,
      pageSize: 20,
    })
  })
})
```

**mock request / services：**

```js
jest.mock('@/config/request', () => jest.fn(() => Promise.resolve({ code: 0, data: {} })))
```

路径 alias 以项目 `vue.config` / `vite.config` 为准。

---

## 约定

- 测试名描述**行为**（中文或英文均可）
- **不断言** UI 文案逐字匹配（易碎）
- **不依赖**真实后端；接口形状用 fixture
- mock 数据字段名与 **field-map / OpenAPI** 一致，禁止自造一套

---

## 测试基建初始化

当 `package.json` **无 test script** 时，交付《基建建议》而非静默失败：

### Vue 3 + Vite（推荐 Vitest）

1. 安装：`vitest`、`@vue/test-utils`、`jsdom`（版本以项目 Vue 为准）
2. `package.json` 增加：`"test:unit": "vitest run"`
3. 可选 `vitest.config.ts`：alias 对齐 vite

### Vue 2 + Vue CLI（推荐 Jest）

1. `vue add unit-jest` 或手动 `@vue/cli-plugin-unit-jest`
2. `"test:unit": "vue-cli-service test:unit"`
3. `@vue/test-utils@1` 配 Vue 2.6

### 接入 feature-verify

在 `feature-verify` 报告增加：

| test:unit | pass/fail/skip（无基建） |

用户确认初始化后，再生成具体 `*.test.ts`。

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 优先纯函数与 services 形态测试
- 🚫 为通过而删断言或 mock 一切

## 交付检查

**汇报内容**

1. 测试栈判定（Vitest / Jest / 无基建）
2. 新增/修改测试文件列表
3. 运行命令与结果（`npm run test:unit` 或 skip 原因）
4. 未覆盖范围（UI E2E → `feature-e2e-verify`）

**门禁**

- [ ] 新增测试可运行（`npm run test` 相关）

## 禁止
- 未要求批量给所有页面生成测试
- 用单测 mock 代替 api-smoke 验证真实响应
- 快照滥用（整页 HTML snapshot）
- 测试里写死生产 URL / token
