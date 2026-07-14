---
name: api-integration
version: 1.0.1
description: 接口对接与字段映射。Swagger/接口文档就绪、联调报错、字段对不齐、分页参数不一致、文件上传下载时使用。有 OpenAPI/Swagger spec 时优先走 openapi-api-integration。用户说「帮我对接接口」「字段对一下」「联调报错」时触发。
---
# 接口对接

> **权威规范：** [接口对接规范.mdc](../../rules/接口对接规范.mdc)（入参透传、出参原样绑定、禁止 normalize 猜字段）。本 Skill 为**操作流程**；与规范冲突时以规范为准。
>
> **有 OpenAPI/Swagger spec（.yaml/.json/URL）？** → 优先 [openapi-api-integration](../openapi-api-integration/SKILL.md)。

## 触发场景

- 「接口文档来了，帮我对接」
- 「字段和后端对不上」
- 「联调报错，帮排查请求参数」
- 功能已生成但接口从 TODO 变为真实地址
- 分页 / 响应结构与页面 `onReachBottom` 逻辑不一致
- 文件上传、导出下载对接

---

## 步骤 0：规范预加载（强制）

**必须先 Read：**

1. [shared/rules-activation.md](../shared/rules-activation.md)
2. **[接口对接规范.mdc](../../rules/接口对接规范.mdc)**
3. 本 Skill

**request 路径**：读取目标页或项目中已有 `services.ts` 的 import，**与项目保持一致**。

---

## 步骤 1：清点接口文档

| 用途 | URL | Method | 请求字段 | 响应字段 | 分页参数 |
|------|-----|--------|----------|----------|----------|

缺字段标注 `[待确认]`，**禁止猜测 prop 名**。

**优先级：** 接口文档 > PRD > 设计稿 label。

### 响应结构判定

读 `@/config/request` 或现有 services，确认解包方式；**页面层不重复解包**。

---

## 步骤 2：更新 types.ts

- `XxxItem` / `XxxDetail` **字段名与接口文档一致**
- `XxxListParams` 与请求参数一致
- 禁止 `any`；枚举放 `constants.ts`

---

## 步骤 3：更新 services.ts

```ts
import request from '@/config/request' // 以项目为准
import type { CouponListParams } from './types'

/** 优惠券列表 */
export const GetCouponList = (data: CouponListParams) =>
  request({ url: 'Coupon/List', data, method: 'post' })
```

| 场景 | 要点 |
|------|------|
| GET 查询 | `params: data`，**入参原样传入，不兜底** |
| 文件上传 | `FormData`，字段名与文档一致 |
| 文件下载 | `responseType: 'blob'` |
| 路径参数 | `Detail/${id}` |

---

## 步骤 4：hook 绑定（不 normalize）

1. **入参**：`await GetList(filters)` 或仅做文档要求的字段改名/合并，**禁止** `buildXxxQuery` / `|| ''`
2. **出参**：`list.value = res?.records ?? []`，原样赋值
3. **模板**：`prop` 绑接口字段；`{{ row.name ?? '-' }}` 仅展示层兜底

**禁止** `normalizeRows` 多字段 `||` 链猜测（见规范 §3 反模式）。

---

## 步骤 5：列表分页

分页字段与文档不一致时，在 **request 拦截器** 或 **service 调用处一处**映射并注释。

---

## 步骤 6：错误与联调

- 拦截器统一错误提示；页面 catch 设 `error` 态
- 提交成功/失败有反馈
- 联调清单见 [接口对接规范.mdc §9](../../rules/接口对接规范.mdc)

---

## 步骤 7：接口探针（可选，有 test 环境时）

编码完成且 `field-map` / 文档就绪后，执行 [api-smoke](../api-smoke/SKILL.md)：

- 对 P0 接口用 **curl** 发最小请求（Agent 须实际执行 Shell）
- 核对响应 keys 与 field-map 一致
- 无环境 → skip，不阻塞编码交付，但 verify 报告须标注

---

## 与 incremental-feature 协作

已有页面对接新接口 → 先 [incremental-feature](../incremental-feature/SKILL.md) 定位范围，再按本 Skill + 规范更新。

---

## 交付

1. 规范预加载一行
2. 修改文件列表
3. 接口与字段映射表（文档字段 → types → 模板 prop）
4. 仍待后端确认的 TODO
