---
name: figma-feature-dev
version: 1.0.1
description: 基于 Figma 设计链接切页面并实现功能。移动端页面内容区要求视觉百分百还原（rpx）；系统状态栏/胶囊/安全区不写入代码。通过 Figma MCP 读取设计稿，结合 PRD/接口开发。
---
# Figma 驱动的功能开发

> 由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 调度。完成后回到主流程阶段 ②③④。

## 适用输入

- Figma 设计链接（`figma.com/design/...` 或 `figma.com/board/...`）
- 可选：PRD 文案、接口文档（**强烈建议同时提供**）

---

## 步骤 1：解析 Figma URL

从链接提取：

```
figma.com/design/:fileKey/:fileName?node-id=1-2
→ fileKey = :fileKey
→ nodeId = 1:2（`-` 替换为 `:`）
```

无 node-id 时先 `get_metadata` 定位页面 Frame。

---

## 步骤 2：读取设计稿

### MCP 可用时

1. 读 `figma-use` skill（`use_figma` 前置）
2. 调用 `get_design_context`（fileKey + nodeId）获取布局、组件、样式、文案
3. 必要时 `get_screenshot` 辅助核对

### MCP 不可用时的降级策略

按以下顺序降级，**不要因 MCP 失败就停止开发**：

1. 请用户提供设计稿截图 → 加载 [spec-analyze-ui-images](../spec-analyze-ui-images/SKILL.md)
2. 请用户补充 PRD 文字描述页面结构与字段
3. 在交付说明中标注「设计稿未读取，布局按 PRD/截图推断，需设计复核」

---

## 步骤 3：设计 → 代码映射（uni-app 移动端）

| 设计元素 | 项目实现 |
|----------|----------|
| 商品/订单列表 | `view` + `v-for` 列表项组件（如 `productItem`） |
| 筛选区 | `drop-down` / `picker` / `search`（沿用项目已有筛选组件） |
| 主按钮 | `button`（主题色 class）或 `u-button` |
| 次按钮 | `button` plain / ghost class |
| 文字链 | `text` + `@click` 或 `navigator` |
| 输入框 | `input` 或 `u-input` |
| 下拉选择 | `picker` / `drop-down` |
| 弹窗 | `u-popup` 或页面内遮罩 + `components/` |
| 分页 | `onReachBottom` + `pageNo`/`pageSize` |
| 统计卡片组 | `view` 卡片布局 + `components/SummaryCards/` |
| Tab 切换 | `u-tabs` 或自定义 tab + `v-if` 切换内容 |
| 顶栏（业务区） | `page-nav-bar` / `custom-nav`；只还原栏内 UI，不画状态栏/胶囊 |

**不要**把 Figma MCP 返回的 React/Tailwind 代码直接当最终代码；提取**尺寸与样式 token**，用 **uni-app 原生组件 + 项目自研组件** 按 rpx 重写。

---

## 视觉还原原则（移动端强制）

> **与中后台「以组件语义为准」不同：uni-app 移动端页面要求设计稿「页面内容区」视觉百分百还原。**

### 还原范围（必须 1:1）

以 Figma 中**页面内容 Frame**（不含设备外壳）为准，下列项须与稿一致（允许 ±2rpx 舍入）：

| 项 | 要求 |
|----|------|
| 布局 | 区块顺序、对齐、flex 方向与稿一致 |
| 间距 | margin / padding 按 750 稿换算 **rpx** |
| 字号 / 行高 | `font-size`、`line-height` 与稿一致 |
| 颜色 | 背景、文字、边框、分割线色值一致 |
| 圆角 / 描边 | `border-radius`、`border-width`、颜色一致 |
| 图标 / 图片 | 尺寸比例、`mode` 与稿一致 |
| 业务顶栏 | 标题、返回、右侧操作等**页面导航内容**与稿一致 |
| 业务底栏 | 固定底部操作栏样式与稿一致（含背景、按钮） |
| 文案 | label、按钮文字与稿一致（接口字段 label 以稿为准，prop 以接口为准） |

**换算：** 设计稿宽 750 → `1px = 1rpx`；其他宽度按 `设计值 / 设计宽 * 750` 换算。

### 排除范围（禁止还原进代码）

下列为**系统 / 设备 chrome**，设计稿里若画了也**不得**按像素实现：

| 排除项 | 正确做法 |
|--------|----------|
| 系统状态栏（时间、电量、信号） | 不画；`statusBarHeight` 仅作占位 |
| 微信小程序胶囊按钮 | 不画假胶囊；自定义导航栏用 `page-nav-bar` / `custom-nav` 留白 |
| 底部 Home 指示条（小横条） | 不画；`env(safe-area-inset-bottom)` 留白 |
| 手机外壳 / 设备边框 / 刘海装饰 | 忽略 |
| 设计稿中的假 TabBar（若项目用自定义 tab） | 用项目 tab 组件，尺寸对齐稿中**业务 tab 区域** |

自定义导航页：`pages.json` → `"navigationStyle": "custom"`，顶栏用项目 `page-nav-bar` / `custom-nav`，**只还原导航栏内的业务 UI**，不还原系统状态栏与胶囊图形。

### 实现优先级

| 优先级 | 做法 |
|--------|------|
| 1 | 从 Figma 提取间距、字号、色值、圆角，写入 scoped scss（rpx） |
| 2 | 布局用 flex + rpx，**禁止**用绝对定位堆叠替代可 flex 实现的结构 |
| 3 | 组件语义映射：原生 / uview / 项目组件（见下表） |
| 4 | 组件库默认值与稿不符时，**以稿为准**覆盖样式 |
| 5 | 交付前 `get_screenshot` 与实现页对比内容区（MCP 可用时） |

---

## 步骤 4：结合 PRD / 接口

设计稿通常缺少：

- 接口 URL 与字段 prop 映射
- 业务校验规则
- 权限与边界状态

| 信息来源 | 用途 |
|----------|------|
| Figma | 布局、视觉、文案 label、组件类型 |
| 接口文档 | 表格 prop、表单字段 key、请求参数 |
| PRD | 业务规则、状态枚举、交互分支 |

字段 prop **必须以接口文档为准**；Figma 列标题仅作 label。

---

## 步骤 5：输出设计摘要

```markdown
## Figma 设计摘要

- 节点：{nodeId} / {frameName}
- 页面类型：列表页 / 表单页 / 复杂页 / ...
- 模块：<module> / <page-dir>
- MCP 状态：已读取 / 降级为截图
- 还原范围：内容 Frame `{frameName}`；已排除状态栏/胶囊/安全区指示条

### 样式 token（来自 Figma）
| 用途 | 值 |
|------|-----|
| 主色 | #... |
| 标题字号 | 32rpx / 行高 ... |
| 页边距 | 24rpx |
| ... | ... |

### 区域划分
- 筛选区字段：...
- 列表展示字段：label → 接口 prop
- 工具栏按钮：...
- 弹窗/抽屉：...

### 接口映射
| 操作 | URL | 字段 |
|------|-----|------|

### 待确认
- ...
```

---

## 步骤 6：缺口提问

设计稿无法确定时询问用户：

1. 列表展示字段对应的接口 prop
2. 列表/表单接口 URL
3. 按钮触发的交互（弹窗 or 跳转 or 直接请求）
4. 未出稿的状态（空数据、loading、错误）
5. 多区块页面是否为复杂页，各区块数据接口

---

## 步骤 7：进入实现

回到 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③：

1. 加载 [vue-page-codegen](../vue-page-codegen/SKILL.md)
2. 按 `subPackages/<module>/` 或 `pages/` 目录规范创建文件
3. **样式：** 从 Figma 提取 token，scoped scss 用 **rpx** 百分百还原内容区；系统栏/胶囊/安全区仅留白
4. 路由按 [route-permission](../route-permission/SKILL.md) 注册 `pages.json`
5. 执行 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md)
6. MCP 可用时 `get_screenshot` 核对内容区视觉

---

## Figma MCP 工具速查

| 目的 | 工具 |
|------|------|
| 读设计结构与参考代码 | `get_design_context` |
| 视觉核对 | `get_screenshot` |
| 页面层级浏览 | `get_metadata` |
| FigJam 流程图 | `get_figjam` |

---

## 禁止事项

- 不照搬 Figma MCP 返回的 React/Tailwind 代码
- **不**在页面内绘制系统状态栏、微信胶囊、底部 Home 指示条
- **不**因「组件库默认样式」偏离设计稿内容区（须覆盖到一致）
- 不为缺失接口的设计字段编造 prop 名
- 不使用 mock 数据
- MCP 失败时不应放弃开发，应走降级策略；降级时标注「视觉待设计复核」
