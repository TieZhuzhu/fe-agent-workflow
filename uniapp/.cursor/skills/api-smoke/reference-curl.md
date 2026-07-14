# API Smoke — curl 参考（按需 Read）

> 通用模板；**URL、鉴权头、成功码**以 `project-conventions.md` 与用户当次输入为准。  
> **本 Skill 仅使用 curl**，不经过 MCP。

## 环境变量（推荐）

在 Shell 中由用户提供或从本地 env 读取，**勿写入 git**：

```bash
export BASE_URL="https://test.example.com"
export TOKEN_HEADER="Authorization"   # 或项目自定义头，如 hm-token
export TOKEN="***"
```

## GET 列表（query）

```bash
curl -sS -w "\nHTTP_CODE:%{http_code}\n" \
  -X GET "${BASE_URL}/api/example/list" \
  -H "${TOKEN_HEADER}: ${TOKEN}" \
  -G \
  --data-urlencode "pageNo=1" \
  --data-urlencode "pageSize=10"
```

## POST 列表（body）

```bash
curl -sS -w "\nHTTP_CODE:%{http_code}\n" \
  -X POST "${BASE_URL}/api/example/pageList" \
  -H "Content-Type: application/json" \
  -H "${TOKEN_HEADER}: ${TOKEN}" \
  -d '{"pageNo":1,"pageSize":10}'
```

## 详情 GET（path / query 以 services 为准）

```bash
curl -sS -w "\nHTTP_CODE:%{http_code}\n" \
  -X GET "${BASE_URL}/api/example/detail" \
  -H "${TOKEN_HEADER}: ${TOKEN}" \
  -G \
  --data-urlencode "orderId=12345"
```

## 响应快速查看 keys（jq 可选）

```bash
curl -sS ... | jq 'keys'
curl -sS ... | jq '.data | keys'
curl -sS ... | jq '.data.data[0] | keys'   # 列表首项字段
```

## 常见对照点

| 项目约定 | 探针关注 |
|----------|----------|
| request 拦截器解包 | 对照 **HTTP 原始 body**；field-map 须注明看原始还是解包后 |
| 列表分页 | 入参 `pageNo`/`pageSize`；出参 `data.data` / `totalCount` 等（以项目为准） |
| 业务成功 | `code === 0` 或 `success === true` |

## 失败分类

| 现象 | 方向 |
|------|------|
| HTTP 401/403 | token / 权限 / 环境 |
| HTTP 404 | path / gateway 前缀与 services 不一致 |
| HTTP 200 + 业务失败码 | 入参 required 缺失或环境数据问题 |
| 200 + 成功但 keys 不对 | spec drift 或前端 prop 错 |

## skip 条件

- 用户未提供 test 环境与鉴权
- 用户禁止访问外网
- 探针为写操作且用户未授权
