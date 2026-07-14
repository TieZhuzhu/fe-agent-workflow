# OpenAPI 联调参考模板

## 操作清单模板

```markdown
| operationId | Method | Path | Tag | 页面/Hook | 说明 |
|-------------|--------|------|-----|-----------|------|
| listProducts | GET | /trade/admin/products | Product | product/list | 商品分页列表 |
```

## Schema → types 映射表模板

```markdown
| OpenAPI Schema | 属性 | TS 类型 | 必填 | 用于 |
|----------------|------|---------|------|------|
| ProductItem | productId | number | Y | 表格 row-key |
| ProductItem | productName | string | N | 列 prop |
| ProductListParams | pageNo | number | Y | 分页 |
| ProductListParams | keyword | string | N | 筛选 |
```

## 联调核对表模板

```markdown
| 检查项 | spec 约定 | 前端实现 | 结果 |
|--------|-----------|----------|------|
| Path | GET /orders | GetOrderList url | ✅ |
| Query pageNo | integer, required | query.pageNo | ✅ |
| Response records | array OrderItem | list.value 类型 OrderItem[] | ✅ |
| 字段 saleStatus | integer | prop="saleStatus" | ✅ |
| customerKeyword | spec 无此字段 | 未传 | ✅ |
```

## 常见 OpenAPI 3 片段读法

### 分页列表响应

```yaml
responses:
  '200':
    content:
      application/json:
        schema:
          properties:
            records:
              type: array
              items:
                $ref: '#/components/schemas/OrderItem'
            totalCount:
              type: integer
```

→ `types.ts`:

```ts
export interface OrderPageResult {
  records: OrderItem[]
  totalCount: number
}
```

### Query 参数

```yaml
parameters:
  - name: orderStatusCode
    in: query
    schema:
      type: string
```

→ `OrderListParams.orderStatusCode?: string`，hook 原样传入 filters。

### 枚举

```yaml
saleStatus:
  type: integer
  enum: [1, 2]
  description: 1-上架 2-下架
```

→ `constants.ts`:

```ts
export const SALE_STATUS = { ON_SALE: 1, OFF_SALE: 2 } as const
```

## 可选工具链（按项目选用）

| 工具 | 用途 | 备注 |
|------|------|------|
| [openapi-typescript](https://github.com/drwpow/openapi-typescript) | spec → `.ts` 类型 | 轻量，适合只生成类型 |
| [@hey-api/openapi-ts](https://github.com/hey-api/openapi-ts) | 类型 + SDK | 可生成 client |
| Swagger UI / Redoc | 人工查阅 | 不生成代码 |
| `openapi-diff` | 对比两版 spec | 升级联调 |

**接入生成器时：** 生成物放 `src/api/generated/` 或模块级 `types.api.ts`，页面 `types.ts` **re-export 或 pick 子集**，保持就近原则。

## 与项目 request 包装层对齐

读 spec 前必须先确认项目响应形态，常见两种：

| 项目拦截器 | spec 中的 `200` schema 指 |
|------------|---------------------------|
| 解包为 `data` | 通常是 `data` 字段内的业务体 |
| 直出业务体 | 与 `responses.200` 一致 |

**以 `project-conventions.md` 与 `request` 源码为准**，勿假设。
