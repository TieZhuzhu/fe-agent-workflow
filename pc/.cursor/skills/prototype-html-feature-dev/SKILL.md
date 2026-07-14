---
name: prototype-html-feature-dev
version: 1.1.1
description: 解析静态/Axure HTML 原型并映射为 Vue 页面；交互页 curl ingest + MCP 实点 P0。 用户说按原型开发、静态页转 Vue、Axure 链接时触发。
---
# 静态 HTML 原型驱动的功能开发

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> 由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 调度。完成后回到主流程阶段 ②③④。

## 输入识别

| 输入 | 子流程 | 典型材料 |
|------|--------|----------|
| **远程 Axure / 原型导航壳 URL** | §远程原型站 | `http://host/项目/index.html#页面.html` |
| **本地 `.html` 文件** | §本地原型文件 | `goods/tag-list.html` |
| PRD / 接口文档 | 两路径共用 §结合 PRD 与接口 | 语雀 Markdown、Swagger |

**多种材料**：UI 结构以原型 HTML 为准；业务规则与接口以 PRD/接口文档为准。

---

## §远程原型站

适用于带左侧目录 + iframe 预览的 Axure 导出导航壳（如「千金大药房 · 小程序原型」）。

### A. 探测与目录抓取

1. `curl` 访问用户给的 `index.html`（HTTP 200 且无需登录则继续）
2. 从 HTML 提取 `var SITEMAP = [...]` JSON（页面树）
3. 递归收集全部 `page` 字段 → **页面清单**（名称、文件名、路径）
4. 侧边栏文案「共 N 个页面」与清单数量交叉校验

**单页 deep link**（`index.html#商品详情页.html`）：仅定位默认页；**须抓全量 SITEMAP** 避免漏页。

### B. 逐页抓取与说明提取

对每个 `*.html`（query 截断至 `?` 前）：

```
GET {baseUrl}/{encodeURIComponent(fileName)}
```

| 提取目标 | 选择器 / 规则 |
|----------|---------------|
| 页面 UI | `body` 业务区；忽略 Axure 播放器壳 |
| **原型说明** | `.page-spec-panel__body` 内全文（标题、表格、列表） |
| 说明标题 | `.page-spec-panel__head` 或文内 `原型说明 ·` |

统计：**有说明 / 无说明** 页面分开列出。无 `page-spec-panel` 的页仍解析 UI，说明标注 `[原型无文字说明，待 PRD 补充]`。

导航壳右侧 `pageSpecPanel` **通常仅首页展示**；其余页说明在 **iframe 内各页底部**，勿只读外壳。

### C. 批量脚本（Shell + Python，可选）

```python
# 解析 SITEMAP + 检测 page-spec-panel（Agent 可在 Shell 执行）
import re, json, urllib.parse, urllib.request
index_url = "<用户 index.html URL>"
html = urllib.request.urlopen(index_url, timeout=15).read().decode("utf-8", "replace")
base = index_url.rsplit("/", 1)[0] + "/"
sitemap = json.loads(re.search(r"var SITEMAP\s*=\s*(\[[\s\S]*?\n\s*\]);", html).group(1))

def walk(nodes):
    for n in nodes:
        if n.get("page"):
            yield n["name"], n["page"]
        if n.get("children"):
            yield from walk(n["children"])

for name, page in walk(sitemap):
    file = page.split("?")[0]
    body = urllib.request.urlopen(base + urllib.parse.quote(file), timeout=8).read().decode("utf-8", "replace")
    has_spec = "page-spec-panel__body" in body
    print(("Y" if has_spec else "N") + " | " + name + " | " + page)
```

feature-spec 场景：将清单 + 各页说明摘要写入 `docs/features/<slug>/research.md` 或 `spec.md` §原型索引。

### D. 终端判定

原型可能是 **C 端小程序**（底部 Tab、手机框）或 **PC 后台**（侧栏 + 表格）。须在 digest 标明终端；**不要**把小程序原型默认映射为本项目中后台 Layout。

### E. 输出：原型站解析摘要

```markdown
## 原型站解析摘要

- 源：{index.html URL}
- 终端：小程序 / PC 后台
- 总页数：N（有说明 M 页，无说明 N-M 页）

### 页面索引

| 模块路径 | 页面名 | 文件 | 有说明 |
|----------|--------|------|--------|

### 当前页说明（page-spec-panel 摘要）

...

### 待 PRD 补充（无说明页）

- ...

### 交互规则（自 JS 源码提取，curl 阶段）

| 页面 | 关联 JS | 关键行为 |
|------|---------|----------|
| ... | resources/scripts/xxx.js | 选券 / 跳转 / localStorage |

### 交互待 MCP 实点（P0）

- [ ] ...
```

---

### F. 含 JS 交互的原型（curl + Browser MCP）

许多 Axure 导出站并非纯静态截图，而是 **HTML + JavaScript 可点击原型**（半屏弹层、Tab 切换、跨页跳转、`localStorage` 草稿）。**curl 与 Browser MCP 分工不同，须组合使用。**

#### F1. 判定是否交互原型

满足任一即视为交互原型，**须走 §F**：

| 信号 | 示例 |
|------|------|
| 外部 `<script src="resources/scripts/*.js">` | `confirm-order.js`、`product-detail.js` |
| 大段 inline `<script>` | 开具发票页个人/企业切换 |
| DOM 含 `is-hidden` / `display:none` 业务区块 | 企业税号行默认隐藏 |
| `onclick` / `addEventListener` / `initXxx()` | `initConfirmOrder({...})` |
| 跨页 `location.href` / 配置 `backUrl` | 确认订单 → 开具发票 |

全站探测：46 页原型常见 **80+ 外部 JS**（Axure 引擎 + 自研脚本），不可只抓 HTML。

#### F2. curl 能做什么 / 不能做什么

| 能力 | curl（+ 关联 JS） | Browser MCP |
|------|-------------------|-------------|
| SITEMAP 全页清单 | ✅ | ⚠️ 逐页点击，慢 |
| `page-spec-panel` 文字说明 | ✅ | ✅ |
| 交互逻辑源码（选券规则、字段显隐） | ✅ 读 JS | ❌ 不读源码 |
| 默认态以外的 UI（半屏、切换后字段） | ❌ 不执行 JS | ✅ 实点可见 |
| 点击顺序、Toast、禁用态 | ❌ | ✅ |
| 批量 46 页 ingest | ✅ 推荐 | ❌ 不适合 |

**结论：** curl **不能**等价于「人点一遍原型」；但能覆盖约 **70–85% 功能规格**（说明面板全 + JS 可读时更高）。**复杂交互页必须用 Browser MCP 补 P0 路径。**

#### F3. curl 阶段：抓取关联 JS

在 §B 逐页抓取 HTML 后，对交互页追加：

1. 正则提取 `<script src="...">` 与 inline script（>500 字符）
2. `GET {baseUrl}/{scriptPath}` 下载 `resources/scripts/*.js`
3. 从 JS 提取：
   - 入口函数：`initConfirmOrder`、`initProductDetail` 等
   - 弹层 ID：`couponSheet`、`invoiceRow`、`deliveryPanelWrap`
   - 跳转：`location.href`、`backUrl`、`开具发票页面.html`
   - 持久化：`localStorage` key（如 `rxOrderInvoiceDraft`）
   - 枚举：`TITLE_TYPE_LABELS`、`personal` / `company`
4. 写入 digest §交互规则 或 `docs/features/<slug>/research.md` §JS 行为

```python
# 提取单页 script src（Agent 可在 Shell 执行）
import re, urllib.parse, urllib.request
base = "<原型 baseUrl>/"
page = "<页面.html>"
html = urllib.request.urlopen(base + urllib.parse.quote(page), timeout=10).read().decode("utf-8", "replace")
for src in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
    if src.startswith("resources/scripts/") and "axure/" not in src:
        js = urllib.request.urlopen(base + src, timeout=10).read().decode("utf-8", "replace")
        print(src, "len", len(js))
```

**禁止**仅凭 HTML 默认可见 DOM 推断全部交互；**须**读关联 JS + `page-spec-panel`。

#### F4. Browser MCP 阶段：P0 交互实点

**触发条件（满足任一）：**

- 页面含选券 / 开票 / 弹层 / Tab / 跨页表单
- `page-spec-panel` 描述「半屏」「切换后展示」「保存回显」
- curl 阶段 JS 含 `Sheet` / `Modal` / `is-hidden` 切换逻辑
- 用户明确要求「按交互原型开发」

**不触发：** 纯展示列表、无 JS 的静态 PC 表格页（curl 足够）。

**执行要点：**

1. Read Browser MCP tool schema → `browser_navigate` 打开 `{index.html}#{页面.html}`（或 iframe 内单页 URL）
2. `browser_snapshot` 读默认可访问树；**说明文字**在 iframe 内 `page-spec-panel`
3. **实点 P0 路径**（`browser_click` / `browser_select`），每步 snapshot 或 `browser_screenshot` 记录
4. 将观察到的 **When/Then** 写入 `docs/features/<slug>/e2e.md`（模板 `docs/features/_template/e2e.md`）
5. MCP 环境要求见 [feature-e2e-verify](../feature-e2e-verify/SKILL.md) §Node ≥18；**Agent Shell 内 `nvm use` 不能修复 MCP**

**禁止：**

- 用 curl 默认态宣称「已覆盖全部交互」
- 对 46 页全站逐页 MCP 点击（仅 **当前 feature 相关 P0**）
- 用 curl 代替 Browser MCP 做交互态验收（实现后验收仍走 `feature-e2e-verify`）

#### F5. P0 交互路径清单（模板 · 小程序商城）

按当前 feature 裁剪，以下为常见 P0（千金大药房类原型）：

**商品详情页（非处方药）**

| 步序 | 操作 | 期望 |
|------|------|------|
| 1 | 打开页面 | 双 Tab：商品详情 / 服务评价 |
| 2 | 点底部「购物车」预览 | 半屏购物车展开 |
| 3 | 点「领优惠券」 | 领券弹层；领取后状态变化 |
| 4 | 点「优惠券」行 | 选券半屏；未达门槛不可选 |
| 5 | 点「发票」行 | 跳转「开具发票页面」 |
| 6 | 开具发票保存返回 | 发票行回显摘要；与 page-spec 数据同步规则一致 |

**确认订单（非处方药）**

| 步序 | 操作 | 期望 |
|------|------|------|
| 1 | 打开页面 | 配送方式默认（骑手/快递/自提可切换） |
| 2 | 切换配送方式 | 面板内容随模式变化 |
| 3 | 点「优惠券」 | 半屏选券；实付/明细刷新 |
| 4 | 点「发票」 | 跳转开具发票；或回显已填摘要 |
| 5 | 点「立即支付」 | 按原型示意（或标注 TODO 接真实支付） |

**开具发票页面**

| 步序 | 操作 | 期望 |
|------|------|------|
| 1 | 打开页面 | 默认「不开发票」或已有草稿回显 |
| 2 | 切换抬头类型：个人 → 企业 | 企业字段（税号等）展示；个人隐藏 |
| 3 | 切换回个人 | 企业字段隐藏 |
| 4 | 选常用抬头 | 表单填充 |
| 5 | 保存 | Toast；返回上一页并回显 |
| 6 | 取消 / 返回 | 不保存，原状态保持 |

**落盘：**

```
docs/features/<slug>/
├── research.md     # §原型索引 + §JS 行为摘要
├── spec.md         # Given/When/Then（来自 panel + MCP）
└── e2e.md          # §F5 裁剪后的 P0 表（供 feature-e2e-verify）
```

#### F6. 三源合并优先级（交互页）

```
接口文档  >  page-spec-panel  >  JS 源码推断  >  MCP 实点观察  >  HTML 默认态 DOM
```

MCP 实点与 panel/JS **冲突**时：以 panel 为准并 `[待确认]`；无 panel 时以 MCP + JS 为准。

---

## §本地原型文件

### 步骤 1：读取原型文件

1. 读取用户提供的 `.html` 完整内容
2. 忽略原型壳层：`app-shell`、`sidebar`、`topbar`、`canvas-toolbar`、Axure 导航壳（`sitemapTree`、`previewFrame` 外层）等（项目已有 Layout）
3. 聚焦 `#screenRoot` / `.screen-card` / `.admin-list-page` 等业务内容区
4. 若存在 `.page-spec-panel__body`，**同等提取**文字说明（与 §远程原型站 B 相同）

---

## 步骤 2：DOM 结构解析（本地 / 远程共用）

从 HTML 提取：

### 列表页识别

```html
.admin-list-page .admin-list-toolbar → HiTable #toolbar 插槽 .admin-list-table → HiTable + el-table-column .pagination-bar → HiTable 内置分页（无需手写）
```

### 表单/弹窗识别

```html
.modal / .inventory-modal-wrap .modal-header-bar h4 → el-dialog title .brand-modal-row → el-form-item .required-dot → 必填 rules .footer-actions → dialog footer 按钮
```

### 字段提取表

| 原型 label | 控件类型 | 推断 prop | 必填 |
| ---------- | -------- | --------- | ---- |

### 表格列提取

从 `<thead><th>` 与 `<tbody><td>` 样本行提取列 label；**prop 名从接口文档获取**，不从 td 文本猜。

### 小程序页识别（C 端原型）

| 特征 | 说明 |
|------|------|
| 底部 `navigation` / Tab | 主 Tab 路由，非 PC 侧栏 |
| 手机状态栏 `9:41` | 忽略，非业务字段 |
| `page-spec-panel` | **优先读说明**，再解析 UI |
| 半屏弹层 / 底部工具栏 | 映射为小程序组件或 `el-drawer`（按目标栈） |

PC 后台原型仍走 `.admin-list-page` / HiTable 路径。

---

## 步骤 3：原型 → Vue 映射规则

| 原型 class / 元素 | Vue 实现                   |
| ----------------- | -------------------------- |
| `.primary-btn`    | `el-button type="primary"` |
| `.ghost-btn`      | `el-button` 默认           |
| `.link`           | Vue 3：`el-button type="primary" link`；Vue 2：`type="text"` |
| `.input`          | `el-input`                 |
| `.table`          | HiTable + el-table-column  |
| `.radio-line`     | el-radio-group             |
| `.modal`          | el-dialog in components/   |
| `.screen-title`   | 页面标题 / breadcrumb      |
| `.screen-desc`    | tooltip 或页面说明区       |

**禁止**复制原型 CSS 类名到 Vue；使用项目 `filter`、`formPage`、`tablePage` 规范样式。

---

## 步骤 4：结合 PRD 与接口

```
原型 HTML / page-spec-panel  →  布局 + label + 交互 + 页面说明
PRD 文案（可先 prd-markdown-ingest）  →  业务规则 + 状态枚举 + 边界说明
接口文档   →  prop 名 + URL + 请求/响应结构
```

冲突优先级：**接口文档 > PRD 文案 / page-spec-panel > 原型 HTML 样本数据**

语雀 PRD 粘贴 → 先 [prd-markdown-ingest](../prd-markdown-ingest/SKILL.md)，再与本节合并。

原型 tbody 中的「新品」「86」等是**示例数据**，不是 mock，不得写入代码。

---

## 步骤 5：输出解析摘要

以 `tag-list.html` 为例：

```markdown
## 原型解析摘要

- 源文件：goods/tag-list.html
- 页面：商品标签列表
- 模块：product / 页面目录：tag-list

### 页面结构

- 工具栏：新增标签
- 表格列：标签名称、展示状态、关联商品数、操作(编辑)
- 弹窗：新增标签（标签名称\*、展示状态 展示/隐藏）

### 接口映射

| 操作 | URL              | 说明      |
| ---- | ---------------- | --------- |
| 列表 | Product/Tag/List | 分页      |
| 保存 | Product/Tag/Save | 新增/编辑 |

### 文件规划

views/product/tag-list/
├── index.vue
├── services.ts
└── components/EditDialog/index.vue
```

---

## 步骤 6：缺口提问

以下缺失时询问用户：

1. 列表/保存/删除接口 URL 与字段
2. 编辑是弹窗还是独立页（原型同时展示列表+弹窗 → 通常弹窗）
3. 「展示状态」枚举值（接口返回值）
4. 路由 path
5. **交互原型**：curl+JS 无法确定的弹层态 / 分支（是否已 MCP 实点？）

**交互原型且未 MCP 实点**：复杂页（选券、开票、多 Tab）须先完成 §F4 或明确用户接受「仅 panel+JS，交互态待联调确认」。

---

## 步骤 7：进入实现

1. 回到 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③
2. 加载 [vue-page-codegen](../vue-page-codegen/SKILL.md)
3. 列表页骨架：

```vue
<HiTable ref="tableRef" url="Product/Tag/List" :params="form">
  <template #toolbar>
    <el-button type="primary" size="small" @click="handleCreate">新增标签</el-button>
  </template>
  <el-table-column label="标签名称" prop="name" min-width="120" />
  <el-table-column label="展示状态" prop="statusDesc" min-width="100" />
  <el-table-column label="关联商品数" prop="productCount" min-width="100" />
  <el-table-column label="操作" width="100" align="right">
    <template #default="{ row }">
      <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
    </template>
  </el-table-column>
</HiTable>
<EditDialog v-model="dialogVisible" :record="currentRow" @success="handleSearch" />
```

4. 执行 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md)

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 解析 DOM/page-spec-panel，交互页须 MCP P0
- 🚫 无原型依据添加业务字段

## 交付检查

- [ ] 交互页 P0 路径已实点或列人工清单

## 禁止事项

- 不复制原型外层 app-shell 布局
- 不引入原型 `styles.css` 的 class
- 不把 tbody 样本数据当 mock 写入
- 不保留原型 `site.ts` / `routes.ts` 逻辑
- **不仅用 curl 默认态 HTML 宣称已覆盖全部交互**（须 §F：JS + MCP P0）
- **不用 curl 代替 Browser MCP 验证半屏/切换/跨页回显**
