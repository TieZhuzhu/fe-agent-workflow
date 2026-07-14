---
name: project-bootstrap
version: 1.1.1
description: 扫描 package.json、pages.json、request 封装等真实约定，产出 project-conventions 与 spec 索引。 用户说扫描项目约定、bootstrap、对齐本项目配置、onboard 时触发。
---
# 项目约定扫描（Bootstrap）

> **管控力度：** 中 | **规范：** [skill-conventions](../shared/skill-conventions.md) | **边界：** [baseline](../shared/skill-boundaries-baseline.md) | **工具：** [toolbox](../shared/project-toolbox.md)

> **写码前若不存在 `.cursor/project-conventions.md`，须先执行本 Skill。**

## 目标

消除 rules/skills 硬编码假设，让生成代码与**当前 uni-app 项目扫描结果**一致。

**边界：** conventions 只记录扫描事实；**路由分包、接口对接、命名**等通用规则以 `.cursor/rules` 为准。

## 流程

```
① 扫描关键文件 → ② 归纳约定 → ③ 写入 project-conventions.md
→ ④ 生成 docs/specs/_index.md → ⑤ 汇报摘要
```

### ① 扫描清单

| 类别 | 扫描目标 | 提取内容 |
|------|----------|----------|
| 框架 | `manifest.json`、`pages.json` | appid、平台、tabBar、subPackages 列表 |
| 依赖 | `package.json` | vue 版本、vuex/pinia、uview 版本、**test script** |
| 构建 | `vite.config.*`、`vue.config.js` | alias |
| 请求 | `common/request*`、`utils/request*`、任意 service 的 import | request 路径、token 头、响应结构、分页字段 |
| 接口组织 | `service/`、`services/`、页面 `services.js` | **集中式 / 页面级 / 混合** |
| 状态 | `store/` | vuex 或 pinia 结构 |
| 样式 | `uni.scss`、`common/`、`static/` | 全局变量、公共 scss |
| UI | `uni_modules/uview-ui`、`pages.json` easycom | uview 版本、easycom 规则 |
| 导航 | 自定义导航组件路径 | custom-nav、page-nav-bar 等 |
| 登录 | `App.vue`、login 相关 | token 存储、拦截方式 |
| **Spec 缺口** | `docs/specs/` vs `pages.json` | 有页面无 spec、进行中 feature |

**至少读 2 个不同子包的页面或 service 文件**，确认 request import 与接口组织一致。

### ② 归纳约定

禁止猜测；扫描不到标 `[待确认]` 并向用户提问。

**测试策略（必写）：**

| package.json 有 test script | project-conventions 写入 |
|-----------------------------|--------------------------|
| 否 | `testStrategy: pending` |
| 是 | `testStrategy: strict`（或团队约定的 `utils-only`） |

### ③ 输出 — project-conventions.md

写入 `.cursor/project-conventions.md`（模板见历史版本 §技术栈/请求层/路由与分包）。

### ④ 生成 spec 索引

```bash
python3 .cursor/skills/scripts/spec-index.py
```

产出 `docs/specs/_index.md`：pages.json path ↔ 页面文件 ↔ 主 spec 缺口。

### ⑤ 汇报

```
项目约定：已扫描 | uni-app Vue 2 + uview | request @/common/request | 接口集中式 service/ | spec 缺口 N 项 | 详见 .cursor/project-conventions.md
```

## 操作边界

基线：[skill-boundaries-baseline.md](../shared/skill-boundaries-baseline.md)

- ✅ 写入 conventions 与 spec 索引
- 🚫 将 token、密钥写入 conventions
- 🚫 用 conventions 覆盖 rules 中的分包/接口原则

## 交付检查

**交付首行：** `Bootstrap 完成 | testStrategy: pending/strict | spec 缺口 N`

**门禁**

- [ ] `project-conventions.md` 已写入
- [ ] `spec-index.py` 已执行

## 维护

以下变更后重新 bootstrap：Vue major 升级、request 重构、分包大规模调整、接口组织模式变更。

用户可说：「重新扫描项目约定」。
