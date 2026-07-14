---
name: api-smoke
version: 1.0.1
description: 用 curl 对 test/staging 发最小请求，核对 status、业务 code 与 field-map/OpenAPI 一致。 用户说接口探针、HTTP 冒烟、curl 验证、联调验收时触发。
---
# 接口 Smoke 探针（curl）

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **定位：** L2 验收 — 用 **curl** 验证真实环境下接口可达、响应形状与文档一致。  
> **不替代：** L1 静态 SDD verify（spec/field-map 对照代码）、L3 浏览器 E2E（`feature-e2e-verify`）。  
> **权威规范：** [接口对接规范.mdc](../../rules/接口对接规范.mdc)（探针通过后仍须入参透传、出参直绑）。  
> **实现方式：** 仅 **Shell + curl**（可选 `jq` 看 keys）。

---

## 触发场景

- `api-integration` / `openapi-api-integration` **编码完成后**
- `【api-smoke】<slug>` 或 `【verify】` 前的接口实况验收
- feature 含 `field-map.md` 且用户有可用的 test 环境
- 联调报错：「接口 200 但页面空」「字段对不上」需区分文档 vs 后端 vs 前端
- 用户说「HTTP 探针」「curl 打一下接口」「验证响应格式」

**不触发：** 无接口的纯 UI 改动；用户明确禁止访问外网/测试环境。

---

## 与联调 Skill 的衔接

| 前置 Skill | 衔接时机 |
|------------|----------|
| `api-integration` | 步骤 7 → 本 Skill |
| `openapi-api-integration` | 步骤 5b → 本 Skill |
| `feature-verify` | ⑥b 可选 L2 |
| `incremental-feature` | 新增/变更接口后 |

---

## 流程

```
① 环境门禁 → ② 选探针接口 → ③ curl 发请求 → ④ 对照结构 → ⑤ 报告
```

### ① 环境门禁（强制）

**必须先 Read：**

1. `package.json`（proxy / env 模式）
2. `.cursor/project-conventions.md`（若存在）：baseURL、gateway、token 头名、成功 code 规则
3. 页面 `services.js` / `services.ts` 与 `field-map.md` 或 OpenAPI

**环境信息来源（优先级）：**

| 来源 | 用途 |
|------|------|
| 用户当次提供的 test URL + 鉴权 | 首选 |
| `project-conventions.md` | baseURL、token 头 |
| `.env.*` / `vue.config` proxy | 仅读**变量名**，禁止把 secret 写入 spec/docs |

**硬约束：**

- **禁止**将 token、密码、cookie 写入仓库、`docs/features/`、Skill 产出物
- 无 test 环境 / 无鉴权 → **skip**，报告标注 `api-smoke: skip（无环境）`，不伪造通过
- 用户未授权访问外网 → skip
- curl 不可用（无 Shell）→ skip

### ② 选探针接口

每个 feature **至少 1 个、最多 3 个** P0 接口：

| 页面类型 | 优先探针 |
|----------|----------|
| 列表页 | 列表查询（最小分页 `pageNo` + `pageSize`） |
| 详情页 | 详情 GET（需用户给合法 id 或文档示例 id） |
| 表单提交 | 仅当用户允许写操作；否则 skip 写接口 |
| 导出/上传 | 通常 skip（副作用大），改测列表 |

从 `field-map.md` / OpenAPI / `services` 提取：

- Method、Path（与 services 中 `url` 一致，含 gateway 前缀）
- 最小合法 body / query（**入参原样**，仅填 required）
- 期望：HTTP 状态、业务 `code`/`success`、列表容器字段名（如 `data`/`records`/`totalCount`/`pageResp`）

### ③ curl 发请求（强制用 Shell）

**Agent 必须实际执行 curl**（`Shell` 工具），不得臆造响应。

#### POST JSON（中后台列表常见）

```bash
curl -sS -w "\nHTTP_CODE:%{http_code}\n" \
  -X POST "${BASE_URL}/gateway/path/to/api" \
  -H "Content-Type: application/json" \
  -H "${TOKEN_HEADER}: ${TOKEN}" \
  -d '{"pageNo":1,"pageSize":10}'
```

#### GET query

```bash
curl -sS -w "\nHTTP_CODE:%{http_code}\n" \
  -X GET "${BASE_URL}/gateway/path/to/api" \
  -H "${TOKEN_HEADER}: ${TOKEN}" \
  -G \
  --data-urlencode "pageNo=1" \
  --data-urlencode "pageSize=10"
```

**约定：**

- `BASE_URL`、`TOKEN_HEADER`、`TOKEN` 来自用户当次输入或 shell 环境变量，**不得** commit
- Method、Path、body 字段名与页面 `services` **一致**
- 响应体过大时：保存前 2 条列表项 + 顶层 keys 即可
- 有 `jq` 时可辅助：`curl ... | jq 'keys'`、`jq '.data | keys'`（非必须）

更多模板见 [reference-curl.md](./reference-curl.md)。

### ④ 对照结构

输出 **探针核对表**：

| 项 | 文档/field-map | 实际响应 | 结果 |
|----|----------------|----------|------|
| HTTP status | 200 | | pass/fail |
| 业务成功码 | code=0 或 success=true | | pass/fail |
| 列表容器 | e.g. `data.data` | | pass/fail |
| 总数 | e.g. `totalCount` | | pass/fail |
| Item 关键字段 | name, status, … | keys 存在？ | pass/fail/skip |

**判定：**

- 文档 vs 实际 keys 不一致 → **spec drift** 或 **前端 binding 错误**，给出修 types/services/HiTable 建议
- 401/403 → 鉴权问题
- 5xx → 后端 blocker

**禁止：** 为探针通过而改 `normalizeRows` 猜字段。

### ⑤ 交付检查

**汇报模板**

```markdown
## API Smoke: <feature-slug 或页面>

| 接口 | 环境 | 方式 | 结果 |
|------|------|------|------|
| GetXxxList | test | curl | pass/fail/skip |

### 结构 diff（若有）
- ...

### 建议
- pass → 可进入 feature-verify / archive
- fail → 回到 api-integration 或确认后端/spec
- skip → 人工联调清单
```

**交付首行：** `API Smoke: <slug> | pass/fail/skip | 探针 2/2 | curl`

**门禁**

- [ ] 探针结果表（endpoint/status/结论）

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 最小探针请求，记录响应摘要
- 🚫 token 写入仓库；对 prod 未授权写操作

## 禁止

- 无环境、未执行 curl 却报 pass
- 把 secret 写入仓库或 feature 文档
- 用探针结果整包重写响应（仅允许修正文档对齐的 binding）
- 使用 MCP 代替本 Skill（本 Skill 仅 curl）
- 代替 `feature-e2e-verify` 做 UI 验证

---

## 参考

- [reference-curl.md](./reference-curl.md) — GET/POST 模板、jq、失败分类
