---
name: figma-feature-dev
version: 1.0.1
description: 通过 Figma MCP 读取设计稿并切符合团队规范的 Vue 页面。 用户粘贴 figma.com 链接并说按设计稿开发、Figma 实现时触发。
---
# Figma 驱动的功能开发

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

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
3. 在交付检查汇报中标注「设计稿未读取，布局按 PRD/截图推断，需设计复核」

---

## 步骤 3：设计 → 代码映射

| 设计元素 | 项目实现 |
|----------|----------|
| 表格列表 | HiTable + el-table-column |
| 筛选表单 | el-form inline + class="filter" |
| 主按钮 | el-button type="primary" |
| 次按钮 | el-button 默认 / plain |
| 文字按钮 | el-button type="primary" link |
| 输入框 | el-input |
| 下拉 | el-select + el-option |
| 弹窗 | el-dialog + 页面 components/ |
| 分页 | HiTable 内置（远程 url 模式） |
| 统计卡片组 | 复杂页 → `components/SummaryCards/` |
| 双栏布局 | 复杂页 → `el-row` + 独立子组件 |
| Tab 切换 | el-tabs lazy + 每 Tab 子目录 |

**不要**把 Figma MCP 返回的 React/Tailwind 代码直接当最终代码；提取布局意图，用 Element Plus + 项目规范重写。

### 视觉还原原则

| 优先级 | 做法 |
|--------|------|
| 1 | 布局结构、信息层级、交互入口与 Figma 一致 |
| 2 | 组件类型映射到 Element Plus（表格、表单、按钮） |
| 3 | 间距/颜色优先用项目全局 SCSS 变量 |
| 4 | 组件库无法表达的差异，用 scoped scss 微调 |
| 5 | **不追求**像素级还原绝对定位布局 |

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

### 区域划分
- 筛选区字段：...
- 表格列：label → prop
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

1. 表格列对应的接口字段 prop
2. 列表/表单接口 URL
3. 按钮触发的交互（弹窗 or 跳转 or 直接请求）
4. 未出稿的状态（空数据、loading、错误）
5. 多区块页面是否为复杂页，各区块数据接口

---

## 步骤 7：进入实现

回到 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 阶段 ③：

1. 加载 [vue-page-codegen](../vue-page-codegen/SKILL.md)
2. 复杂页加载 [复杂页面开发指南](../../rules/复杂页面开发指南.mdc)
3. 按 views 目录规范创建文件
4. 样式：优先 Element + 公共 scss，仅补 Figma 中组件库无法表达的差异
5. 路由按 [路由与权限规范](../../rules/路由与权限规范.mdc)
6. 执行 [reference-checklist.md](../feature-dev-workflow/reference-checklist.md)

---

## Figma MCP 工具速查

| 目的 | 工具 |
|------|------|
| 读设计结构与参考代码 | `get_design_context` |
| 视觉核对 | `get_screenshot` |
| 页面层级浏览 | `get_metadata` |
| FigJam 流程图 | `get_figjam` |

---

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ MCP 读设计 + 对齐 project conventions
- 🚫 无 Figma 依据臆造布局

## 交付检查

- [ ] 设计关键区块已对照实现

## 禁止事项

- 不照搬 Figma MCP 返回的 React/Tailwind 代码
- 不硬编码 Figma 绝对定位布局替代 Element 表格/表单
- 不为缺失接口的设计字段编造 prop 名
- 不使用 mock 数据
- MCP 失败时不应放弃开发，应走降级策略
