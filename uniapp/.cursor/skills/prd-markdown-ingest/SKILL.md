---
name: prd-markdown-ingest
version: 1.0.1
description: 语雀/飞书 PRD「复制为 Markdown」接入与清洗。解析粘贴 Markdown、提取图片 URL、输出结构化 prd-digest，供 prd-feature-dev / feature-spec 使用。用户粘贴语雀 PRD、飞书文档 Markdown、或说「语雀 PRD 接入」「PRD Markdown 粘贴」时触发。
---
# PRD Markdown 接入（语雀 / 飞书）

> 由 [feature-dev-workflow](../feature-dev-workflow/SKILL.md) 调度。**只做材料清洗与结构化**，业务提取交 [prd-feature-dev](../prd-feature-dev/SKILL.md)；写 spec 交 [feature-spec](../feature-spec/SKILL.md)。

## 触发场景

| 用户输入 | 走本 Skill |
|----------|------------|
| 粘贴语雀「复制为 Markdown」全文 | ✅ |
| 粘贴飞书 / 钉钉文档导出的 Markdown | ✅ |
| 本地 `.md` PRD 文件 | ✅（跳过 §语雀特有问题） |
| 语雀 / 飞书 **在线链接**（未粘贴正文） | ❌ 见 §在线链接限制 |
| 远程 Axure 原型站 URL | ❌ 走 [prototype-html-feature-dev](../prototype-html-feature-dev/SKILL.md) |

---

## 在线链接限制

**Browser MCP / curl 无法读取需登录的语雀正文**（常见 401）。

须告知用户任选其一：

1. **推荐**：语雀文档 → 「…」→ **复制为 Markdown** → 粘贴到对话
2. 导出 Word / PDF + 截图（走 [prd-feature-dev](../prd-feature-dev/SKILL.md) + [spec-analyze-ui-images](../spec-analyze-ui-images/SKILL.md)）
3. 公开分享链接且无需登录（少见，仍优先复制 Markdown）

**禁止**用 Browser MCP 反复尝试登录态语雀作为主路径。

---

## 流程

```
① 识别来源 → ② 清洗 Markdown → ③ 结构化提取 → ④ 图片清单 → ⑤ 输出 prd-digest → ⑥ 交接下游
```

### ① 识别来源

判断：

- **语雀导出**：混有 `<font>`、`<br/>`、`<span>` 等 HTML；表格偶发错位
- **飞书导出**：类似 HTML 残留，标题层级可能跳跃
- **纯 Markdown**：无 HTML 标签

记录：文档标题、终端类型（小程序 / PC 后台 / App）、业务模块（若可识别）。

### ② 清洗 Markdown

逐条处理，**保留业务语义，去掉排版垃圾**：

| 问题 | 处理 |
|------|------|
| `<font color="...">` / `</font>` | 删标签，保留内部文字 |
| `<br/>` / `<br>` | 换为 `\n` |
| `<span>` / `</span>` | 删标签 |
| 连续空行 >2 | 合并为 1 空行 |
| 表格列错位 | 按相邻行语义手动对齐，标注 `[表格已校正]` |
| 图片语法 `![](url)` | 保留 URL，记入 §④ |

**禁止**改写需求含义；仅做格式清洗。

### ③ 结构化提取

从清洗后正文提取：

```markdown
## PRD Digest（自动生成）

- 源：语雀 Markdown / 飞书 Markdown / 本地 .md
- 文档标题：<title>
- 终端：<小程序 | PC 后台 | App | 未识别>
- 业务域：<domain>

### 功能清单（按 H2/H3）

| 章节 | 功能点摘要 |
|------|------------|

### 字段与规则

| 字段/概念 | 类型/枚举 | 规则说明 |
|-----------|-----------|----------|

### 状态与流程

- 状态枚举、流转条件

### 接口线索（PRD 中提及的）

| 用途 | URL/名称 | 备注 |
|------|----------|------|

### 待确认

- [ ] ...
```

复杂 PRD 可选 [spec-research-clarify](../spec-research-clarify/SKILL.md)。

### ④ 图片清单

1. 正则提取 `!\[.*?\]\((https?://[^)]+)\)` 与裸 `https://.*\.(png|jpg|jpeg|gif|webp)`
2. 语雀常见域名：`cdn.nlark.com`、`yuque.com` 附件
3. **Spot check**：对前 3～5 张 `curl -sS -o /dev/null -w "%{http_code}" <url>`；200 则标记 `accessible`
4. 不可访问的图片 → `[待确认]`，提示用户重新导出或单独上传截图

有关键 UI 截图且文字不足时，加载 [spec-analyze-ui-images](../spec-analyze-ui-images/SKILL.md) 分析**用户另行上传**的截图；**不要**假设能从语雀 CDN 批量 Vision 分析（除非用户明确要求逐张分析且 URL 可访问）。

### ⑤ 落盘（feature-spec 场景）

若处于 SDD 提案阶段，将 digest 写入：

```
docs/features/<slug>/research.md   # 或 spec.md §PRD 摘要
```

并在 `proposal.md` 注明 PRD 来源：`语雀 Markdown 粘贴`。

### ⑥ 交接下游

| 用户意图 | 下一步 |
|----------|--------|
| 先写 spec | [feature-spec](../feature-spec/SKILL.md)，digest 填入 spec / design |
| 直接开发 | [prd-feature-dev](../prd-feature-dev/SKILL.md) §步骤 2 起 |
| 仅清洗 | 输出 digest 即可 |

---

## 与 prd-feature-dev 的分工

| 本 Skill | prd-feature-dev |
|----------|-----------------|
| Markdown 清洗、HTML 去噪 | 需求摘要、页面类型判定 |
| 图片 URL 清单 | UI 截图结构化分析（spec-analyze-ui-images） |
| 章节级功能清单 | 字段表、接口表、文件规划 |
| 不写 Vue 代码 | 进入 vue-page-codegen |

**优先级不变**（下游沿用）：接口文档 > PRD 文案 > UI 截图推断。

---

## 禁止事项

- 不把语雀链接当已读 PRD（未粘贴正文时）
- 不捏造接口 URL / 字段名
- 不把 PRD 示例数据写入 mock
- 不跳过清洗直接开发（HTML 残留会导致字段表错位）

---

## 话术示例

```
【spec】propose mini-goods-detail。语雀 PRD 如下：（粘贴 Markdown）
```

```
语雀 PRD 已粘贴，先清洗提取再按 PRD 开发商品详情页，模块 product
```
