# CS146S 课程导读摘要

> 整理自：[The Modern Software Developer：CS146S 课程导读与实战索引](https://zhuanlan.zhihu.com/p/1985789368133261187)  
> 官网：[themodernsoftware.dev](https://themodernsoftware.dev)

## 课程在教什么

不再把编程当成「从零手写」，而是练迭代闭环：

**规划 → 用 AI 生成代码 → 编辑修正 → 重复。**

目标能力：

- 在真实复杂度项目里用好 Cursor / Claude Code 等工具
- 把 LLM 嵌进编码、文档、测试、安全等工作流
- 识别 AI 辅助开发的失效模式与陷阱
- 理性定位 AI 在软件工程中的角色

## 五段能力递进

| Phase | 周次 | 目标 |
|-------|------|------|
| A | 1–2 | 先让 LLM / Agent 闭环跑起来（提示 → 工具调用 / MCP） |
| B | 3–4 | 上下文、面向 Agent 的规格、自治边界与护栏 |
| C | 5–7 | 工程化：终端自动化、测试与安全、审查 / 调试 / 文档 |
| D | 8–9 | 端到端交付 + 上线后可观测与事故响应 |
| E | 10 | AI 优先时代角色与协作范式展望 |

## 十周速览

### Week 1 — LLM 基础与提示工程

- 主题：LLM 是什么、如何高效提示
- 作业：[`assignments/week1`](../assignments/week1/) Prompting Playground（k-shot、CoT、tool calling、self-consistency、RAG、reflexion）

### Week 2 — Coding Agents + 工具调用 + MCP

- 主题：Agent 架构、function calling、MCP
- 作业：[`assignments/week2`](../assignments/week2/)

### Week 3 — AI IDE

- 主题：大仓库上下文、面向 Agent 的 PRD/Specs、IDE 集成
- 作业：[`assignments/week3`](../assignments/week3/) 自定义 MCP Server

### Week 4 — 编程智能体模式

- 主题：自主权、护栏、人机协作
- 作业：[`assignments/week4`](../assignments/week4/) Claude Code

### Week 5 — 现代终端

- 主题：AI 增强 CLI、自动化重复 Shell 任务
- 作业：[`assignments/week5`](../assignments/week5/) Warp

### Week 6 — 测试与安全

- 主题：AI QA、SAST/DAST、安全编码
- 作业：[`assignments/week6`](../assignments/week6/)

### Week 7 — 现代软件支持

- 主题：可信度、调试、文档、AI Code Review
- 作业：[`assignments/week7`](../assignments/week7/)

### Week 8 — 自动化 UI / App 构建

- 主题：降低前端门槛、快速原型到可运行 App
- 作业：[`assignments/week8`](../assignments/week8/)

### Week 9 — 部署后的智能体

- 主题：可观测性、事故响应、故障分类与调试工作流

### Week 10 — AI 软件工程的未来

- 主题：角色演变、AI 原生协作、长期趋势

## 评分（原课程）

- 期末项目 80% · 每周作业 15% · 课堂参与 5%
