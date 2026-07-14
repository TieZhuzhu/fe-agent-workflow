---
name: openapi-api-integration
version: 1.0.1
description: 基于 OpenAPI/Swagger 规范（JSON/YAML/URL）做接口联调。从 spec 提取路径、参数、Schema 生成 types.ts 与 services，校验页面绑定。用户说 OpenAPI、Swagger、openapi.json、按接口文档自动生成类型时触发；有 spec 时优先于纯手写 api-integration。
---
# OpenAPI 接口联调

> **权威规范：** [接口对接规范.mdc](../../rules/接口对接规范.mdc)（入参原样、出参原样、禁止 normalize 猜字段）。
>
> **与 `api-integration` 关系：** 本 Skill 是 **有 OpenAPI/Swagger spec 时的增强流程**；无 spec 时走 [api-integration](../api-integration/SKILL.md)。

---

## 何时用 OpenAPI Skill

| 条件 | 选用 |
|------|------|
| 用户提供/仓库有 `.yaml` `.json` spec 或 Swagger URL | **本 Skill** |
| 仅 Markdown/表格接口说明、无机器可读 spec | `api-integration` |
| 页面已存在，只加 1～2 个字段 | `incremental-feature` + 本 Skill 的 §字段核对 |

**触发话术：** OpenAPI、Swagger、openapi.json、按 spec 生成 types、接口文档 YAML

---

## OpenAPI 能做什么（联调价值）

| 能力 | 对前端的帮助 |
|------|----------------|
| **paths + operationId** | 唯一确定 URL、Method，消除手写路径错误 |
| **parameters / requestBody** | 入参字段名、类型、required，直接写 `types.ts` |
| **responses.schemas** | 列表项/详情字段 **以文档为准**，禁止猜 prop |
| **components.schemas** | 复用 DTO，跨接口一致 |
| **enum** | 生成 `constants.ts` 状态码映射 |
| **与实现 diff** | 联调报错时对照 spec 查「前端传错」还是「后端偏离文档」 |

**OpenAPI 不能替代：** 业务 UI label、权限码、路由；这些仍来自 PRD/设计稿。

---

## 步骤 0：规范预加载

1. [shared/rules-activation.md](../shared/rules-activation.md)
2. [接口对接规范.mdc](../../rules/接口对接规范.mdc)
3. [JavaScript通用代码生成指南.mdc](../../rules/JavaScript通用代码生成指南.mdc) §数据处理（lodash-es）
4. 本 Skill + [reference.md](./reference.md)

确认 spec 来源（优先级）：

```
仓库内 docs/openapi/*.yaml > 用户粘贴 URL > 用户上传文件 > [待确认]
```

---

## 步骤 1：定位本次涉及的 API

从 spec 中筛选与**当前页面/模块**相关的 operations：

```markdown
## OpenAPI 操作清单
| operationId | Method | Path | 用途 | 页面 |
|-------------|--------|------|------|------|
| listOrders | GET | /trade/admin/orders | 订单列表 | order/list |
```

- 用 `tags` 或 path 前缀过滤（如 `/trade/admin/`）
- 记录 **operationId**（生成 services 注释用）
- 缺 operationId 时用 `summary` + path 命名，标注 `[spec 无 operationId]`

---

## 步骤 2：Schema → types.ts

**规则：字段名与 spec 完全一致**（含 camelCase / snake_case，以 spec 为准）。

### 映射约定

| OpenAPI | types.ts |
|---------|----------|
| `components.schemas.OrderItem` | `export interface OrderItem { ... }` |
| query `parameters` | `OrderListParams` |
| `requestBody` schema | `SaveOrderPayload` |
| 分页包装（项目约定） | `PageResult<T>` 或文档中的 `records`/`totalCount` |

### 类型映射

| OpenAPI | TypeScript |
|---------|------------|
| `string` | `string` |
| `integer` / `number` | `number` |
| `boolean` | `boolean` |
| `array` | `T[]` |
| `$ref` | 解析到 components 同名 interface |
| `enum` | 联合类型或 `constants.ts` + `type XxxCode = ...` |
| `format: int64` | `number`（注释标注） |
| `nullable: true` | `T \| null` 或 `T?`（与项目风格一致） |

**禁止：** 自造 spec 中不存在的字段；禁止 `normalizeRows` 合并多实体。

### 可选：代码生成

若项目已配置生成器（`openapi-typescript`、`@hey-api/openapi-ts` 等）：

1. Read `package.json` / `project-conventions.md` 是否已有脚本
2. **有脚本** → 运行项目约定命令，再将生成物 **对齐到页面 `types.ts` 就近原则**（勿整包覆盖页面目录）
3. **无脚本** → Agent **手写** types（从 spec 摘录），交付中建议后续接入生成器

---

## 步骤 3：paths → services.ts

按 spec 写请求，**入参原样透传**：

```ts
import request from '@/config/request' // 以项目为准
import type { OrderListParams, OrderPageResult } from './types'

/** listOrders — GET /trade/admin/orders */
export const GetOrderList = (params: OrderListParams) =>
  request<OrderPageResult>({ url: '/trade/admin/orders', method: 'get', params })
```

| spec | services |
|------|----------|
| `path` 参数 `{id}` | `` `/orders/${id}` `` |
| `query` parameters | `params` 对象，**不兜底** |
| `requestBody` | `data` |
| `multipart/form-data` | `FormData` |

**baseUrl：** spec 的 `servers[0].url` 仅作参考；实际以项目 `request` baseURL + gateway 为准（读 `project-conventions.md`）。

---

## 步骤 4：hook / 模板绑定

1. hook：`list.value = res?.records ?? []`（字段名来自 **response schema**）
2. 模板：`prop` = schema 属性名；label = 设计稿中文
3. 枚举展示：`constants.ts` 映射，不用 `row.a || row.b`

---

## 步骤 5：OpenAPI 联调核对（diff）

联调报错或字段不对时，按顺序查：

```
1. 请求 Method / Path 是否与 spec 一致
2. 入参名、类型、required 是否与 parameters / requestBody 一致
3. 响应是否比 spec 多/少字段（后端偏离 → 记 TODO 更新 spec 或临时 types 注释）
4. 分页字段名是否与 spec 或项目约定一致
5. 鉴权 header 是否在 spec security 中声明（如 Bearer / 自定义 token）
```

交付 **OpenAPI 核对表**（见 [reference.md](./reference.md)）。

---

## 步骤 5b：接口探针（可选，有 test 环境时）

OpenAPI diff 通过后，执行 [api-smoke](../api-smoke/SKILL.md) 对 P0 operation 用 **curl** 发实况请求。无 test 环境 / 无鉴权 → skip。

---

## 步骤 6：spec 变更维护

| 变更 | 动作 |
|------|------|
| 后端发新 spec | 重新执行 §1～§3 diff，只改受影响页面 |
| 字段重命名 | 改 types + 模板 prop，**不**写 adapter normalize |
| 字段删除 | 删绑定 + 类型，查编译错误 |
| spec 与线上一致性存疑 | 以**实际响应**为准更新 types，并标注 `// spec drift: xxx` |

建议约定：`docs/openapi/<service>.yaml` 纳入版本管理，联调时 `@` 该文件。

---

## 交付

1. 规范预加载一行
2. **OpenAPI 操作清单**（operationId / path / 页面）
3. **Schema → types 映射表**
4. 修改文件列表（types / services / hooks / constants）
5. OpenAPI 核对表 + 仍待确认的 TODO

---

## 禁止

- 无 spec 时假装「按 OpenAPI」猜字段
- 用 OpenAPI 当借口写 `normalizeRows` 万能字段
- 入参 `|| ''` / `buildXxxQuery` 兜底（见接口对接规范）
- 全量 codegen 覆盖页面目录、破坏就近 `types.ts` 结构
