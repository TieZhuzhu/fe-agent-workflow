---
name: route-permission
version: 1.0.1
description: 为新页面注册本地路由 path；菜单权限由后端接口配置，前端不做按钮级权限。 用户说加路由、注册页面路由、新页面路由时触发；常与 feature-dev-workflow 配合。
---
# 路由 + 菜单 + 权限

> **管控力度：** 严 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

## 权限模型（必读）

| 层级 | 谁负责 | 前端做什么 |
|------|--------|------------|
| **菜单 / 页面访问** | 后端接口返回当前用户菜单权限树 | 侧栏渲染菜单树；路由守卫用树数据**统一拦截** |
| **本地路由表** | 前端 | 声明**所有页面**的 path / component / meta，与菜单树**解耦** |
| **按钮 / 操作** | 后端接口鉴权 | **不做** `v-permission` / `v-if` 隐藏；无权限时接口返回错误，前端按通用错误提示处理 |

### 接口菜单树结构

```ts
interface MenuNode {
  id: string
  name: string
  path: string
  children?: MenuNode[]
}
```

- 一级菜单 → `children` 二级 → `children` 三级
- 侧栏展示与「当前用户可访问哪些 path」均来自该树
- **路由是否可访问**：目标 `to.path` 须在用户菜单树 path 集合内（或项目约定的白名单规则内），由**统一守卫**在获取菜单树后判断

**禁止**在单个路由 `meta` 上维护 `permission` / `menuCode` 等页面权限码。

**禁止**为新页面在前端配置按钮权限码或 `hasButtonPermission` / `v-permission`。

---

## 触发场景

- 新建页面，需在本地注册路由
- 详情 / 编辑子页、隐藏路由（`hidden`）等路由配置
- 路由 403：排查 path 与接口菜单树是否一致（**不改**前端权限码）

**不触发：** 按钮显隐（团队规范不做）；CI 失败（`ci-fix`）；纯交互 bug（`bugfix-workflow`）。

---

## 流程

```
① 读约定 → ② 确定 path / name → ③ 追加本地路由 → ④ 交付后端菜单配置提醒 → ⑤ 验收
```

### ① 必读

1. `路由与权限规范.mdc`
2. 同模块已有 `views/<module>/routes.ts` 写法
3. 若已执行 bootstrap，Read `.cursor/project-conventions.md` 中的 **request 路径、路由合并方式**（不涉及权限例外）

### ② path 与页面目录（强制对应）

**路由 `path` 由前端定义**，且必须与页面文件路径**一一对应**，禁止各写各的。

| 路由 path | 页面目录 | 说明 |
|-----------|----------|------|
| `/product/tag-list` | `views/product/tag-list/` | 模块名 = 第一段；页面目录 = 后续段 |
| `/product/batch-off-shelf` | `views/product/batch-off-shelf/` | 多段 kebab-case 保持一致 |
| `/product/tag-list/:id` | `views/product/tag-list/` | 动态路由挂在同一页面目录下 |

**推导规则：**

```
path: /{module}/{page-dir}/...
  → 页面目录: views/{module}/{page-dir}/
  → routes 引用: import('./{page-dir}/index.vue')
```

**示例（product 模块新增 tag-list）：**

1. 先建目录 `views/product/tag-list/index.vue`
2. 再注册路由 `path: '/product/tag-list'`
3. 后端菜单配置的 `path` 与路由 **完全一致**：`/product/tag-list`

**禁止：**

- 路由 `/product/tag-list`，页面却放在 `views/product/tags/` 或 `views/goods/tag-list/`
- 无模块前缀的 path（如 `/tag-list`）对应到任意深层目录
- 为「省事」缩短 path 或与 PRD 菜单文案拼写不一致（菜单 path 须跟路由对齐）

**模块级单页例外**（仅当页面是模块下单个 `.vue` 文件时）：

| path | 文件 |
|------|------|
| `/product/detail/:id` | `views/product/Detail.vue` |

有独立目录的页面（含 `index.vue` + hooks/services）**必须**走路由 path ↔ 目录对应，不走模块级单页例外。

### ③ 路由命名

| 项 | 规范 | 示例 |
|----|------|------|
| `path` | `/{module}/{page-dir}`，kebab-case | `/product/tag-list` |
| `name` | PascalCase 英文 | `ProductTagList` |
| `meta.title` | 中文，面包屑/页签 | `'商品标签'` |

**禁止**：中文 route name。

### ④ 追加本地路由

模块级路由（推荐）：

```ts
// views/product/routes.ts  
export default [
  {
    path: '/product/tag-list',
    name: 'productTagList',
    component: () => import(/* webpackChunkName: "productTagList" */ './tag-list/index.vue'),
    meta: {
      title: '商品标签',
      keepAlive: true,
    },
  },
  {
    path: '/product/tag-list/:id',
    name: 'productTagDetail',
    component: () => import(/* webpackChunkName: "productTagDetail" */ './tag-list/Detail.vue'),
    meta: {
      title: '标签详情',
    },
  },
]
```

```ts
// router/index.ts
import productRoutes from '@/views/product/routes'

export const routes = [
  ...productRoutes,
]
```

#### meta 常用字段（无权限码）

| 字段 | 用途 |
|------|------|
| `title` | 页面标题（必填） |
| `activeMenu` | 子页高亮父级菜单 path |
| `hidden` | 不在侧栏展示的路由（侧栏仍由接口树驱动） |
| `keepAlive` | 列表页缓存 |
| `public` | 登录页等无需菜单校验 |

**新增页面只做路由注册**，不维护 `meta.permission` / `menuCode`，不修改侧栏静态配置（侧栏数据来自接口菜单树）。

### ⑤ 后端 / 运维配合（交付 TODO）

新页面上线前，须在**后台权限系统**配置菜单节点，保证：

- 菜单树中存在与本地路由一致的 `path`
- `path` 与前端路由**完全一致**（含前缀、尾斜杠、动态段规则以项目为准）

汇报时在「待后端配置菜单」块中列出：

```markdown
## 待后端配置菜单
- path: `/product/tag-list`
- name: 商品标签
- 挂载：商品 → 基础资料 → 三级（以 PRD 为准）
```

### ⑥ 交付检查

完成路由注册时须汇报并确认：

**汇报内容**

1. 修改文件：模块 `routes.ts` / `router/index.ts`
2. 新增路由：`path`、`name`、`meta.title` 添加 `webpackChunkName`
3. **待后端配置菜单** path 列表（格式见 §⑤）
4. 建议验证：后端配好菜单后，有权限账号可进、无权限被统一守卫拦截

**门禁**

- [ ] **path 与 `views/<module>/<page-dir>/` 一一对应**（见 §②）
- [ ] `views/<module>/routes.ts` 已追加；主路由已合并（新模块时）
- [ ] `path` / `name` / `meta.title` 符合规范
- [ ] 详情子页已设 `activeMenu`（若需要）
- [ ] **未**添加 `meta.permission` / `menuCode` / 按钮 `v-permission`
- [ ] 交付含「待后端配置菜单」path 列表
- [ ] path 已记录到 spec；有权限账号配置菜单后可访问

---

## 403 / 菜单不显示排查

1. 接口返回的菜单树是否包含该 `path`
2. 本地路由 `path` 与菜单 `path` 是否一致（大小写、前缀、`/admin` base）
3. 统一路由守卫是否在菜单树加载**之后**才做校验
4. **不要**通过在前端加权限码或写死菜单来「绕过」

---

## 与新建 / 增量 Skill 的关系

| 场景 | 主 Skill | 本 Skill |
|------|----------|----------|
| 从零新建页 | `feature-dev-workflow` | 阶段 ③ 后仅注册本地路由 |
| 老页加路由入口 | `incremental-feature` | 仅追加 routes 项 |
| 加工具栏按钮 | `incremental-feature` | **不需要**本 Skill（无按钮权限前端处理） |

---

## 缺口提问（一次 1～3 个）

1. 页面 `path`（默认 `/{module}/{page-dir}`，与目录同步创建）
2. 列表 / 详情是否共用 path 前缀、`activeMenu` 指向
3. 是否 `keepAlive` / `hidden`

**不要问**前端按钮权限码——团队规范由接口鉴权。

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 只增路由注册，path 与用户确认
- 🚫 擅自改已有路由 path；加 v-permission
