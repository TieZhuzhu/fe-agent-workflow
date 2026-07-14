---
name: route-permission
version: 1.0.1
description: uni-app 新页面注册 pages.json。主包/分包判定、tabBar、子包选用。用户说「加路由」「注册页面」「pages.json」时触发。
---
# pages.json 路由注册

## 触发场景

- 新建页面需注册 `pages.json`
- 调整 navigationBar、下拉刷新、自定义导航
- 新增分包或向已有子包追加页面

**不触发：** 纯交互 bug（`bugfix-workflow`）；接口联调（`api-integration`）。

## 流程

```
① 读规范 → ② 主包/分包判定 → ③ 选子包 → ④ 建文件 + 注册 → ⑤ 验收
```

### ① 必读

1. `路由与分包规范.mdc`
2. 当前 `pages.json`（tabBar、subPackages 全貌）
3. `.cursor/project-conventions.md`（若存在）

### ② 主包 vs 分包判定

| 问题 | 是 → | 否 → |
|------|------|------|
| 是否 tabBar 页？ | 主包 `pages` | **必须分包** |
| 是否启动必要页？ | 主包（极少） | 分包 |

**默认：非 tabBar 一律 subPackages。**

### ③ 选择子包

1. Grep `pages.json` 的 `subPackages[].root`
2. 按业务域匹配：`product`、`order`、`user`、`coupon`、`address`…
3. **优先追加到已有子包**
4. 仅当无合适子包或子包过大时新建 `subPackages/<module>`

### ④ 文件与注册

**示例：商品列表（非 tabBar）**

1. 创建 `subPackages/product/list.vue`（或 `list/index.vue`）
2. 在 `subPackages` 中找到 `root: "subPackages/product"`，追加：

```json
{
  "path": "list",
  "style": {
    "navigationBarTitleText": "商品列表",
    "enablePullDownRefresh": true
  }
}
```

3. 完整路径：`/subPackages/product/list`
4. 跳转：`uni.navigateTo({ url: '/subPackages/product/list' })`

**示例：新建子包（谨慎）**

```json
{
  "root": "subPackages/coupon",
  "pages": [
    {
      "path": "list",
      "style": { "navigationBarTitleText": "我的优惠券" }
    }
  ]
}
```

并创建目录 `subPackages/coupon/list.vue`。

### ⑤ 验收清单

1. [ ] 非 tabBar 未入主包
2. [ ] 优先复用已有子包
3. [ ] 磁盘文件 path 与 pages.json 一致
4. [ ] `navigationBarTitleText` 正确
5. [ ] tabBar 跳转用 `switchTab`
6. [ ] 自定义导航已设 `navigationStyle: custom` 且页面有导航组件

## 移动端权限

- 登录拦截：按项目 `App.vue` / request 拦截器，**不在 pages.json 配权限码**
- 按钮权限：接口鉴权，前端不 v-if 隐藏

## 交付模板

```markdown
## 路由注册完成
- 类型：分包页
- 子包：subPackages/product（已有）
- path：subPackages/product/list
- 文件：subPackages/product/list.vue
- 跳转：uni.navigateTo({ url: '/subPackages/product/list' })
```
