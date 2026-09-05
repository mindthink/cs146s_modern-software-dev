# CS146S · The Modern Software Developer

个人学习仓库：跟学斯坦福 [CS146S](https://themodernsoftware.dev)（现代软件开发者），用 AI 工具重构软件开发生命周期。

## 仓库结构

```text
.
├── AGENTS.md      # 跨工具 Agent 约定（提交规范等）
├── CLAUDE.md      # Claude Code 入口，引用 AGENTS.md
├── assignments/   # 官方作业与代码（week1–week8）
├── notes/         # 学习笔记、大纲索引、个人总结
├── pyproject.toml # Poetry 依赖
└── README.md
```

| 目录 | 用途 |
|------|------|
| [`assignments/`](./assignments/) | 存放每周作业代码与 `assignment.md` |
| [`notes/`](./notes/) | 存放课程笔记、导读与阅读摘录 |

## 导读与大纲

中文课程导读（大纲索引）：
[The Modern Software Developer：CS146S 课程导读与实战索引](https://zhuanlan.zhihu.com/p/1985789368133261187)

课程官网：https://themodernsoftware.dev

扩展阅读：
- [提示工程指南（中文）](https://www.promptingguide.ai/zh)
- [动手学大模型 Dive into LLMs](https://github.com/Lordog/dive-into-llms/tree/main)

详见 [`notes/reading-list.md`](./notes/reading-list.md)。

## 能力递进（五段）

1. **Week 1–2**：提示工程 → Coding Agent / MCP（先把 AI 闭环跑起来）
2. **Week 3–4**：上下文、面向 Agent 的规格（PRD/Specs）与护栏
3. **Week 5–7**：工程化（终端自动化、测试与安全、代码审查/文档）
4. **Week 8–9**：端到端 App 构建、上线后可观测与事故响应
5. **Week 10**：AI 优先时代的软件工程角色演变

## 环境

Python 3.12 + Poetry（或 Conda `cs146s`）：

```bash
poetry install --no-interaction
source .venv/bin/activate   # 若使用 in-project venv
```

Ollama（Week 1 等本地模型练习）：

```bash
ollama run mistral-nemo:12b
ollama run llama3.1:8b
```

运行示例：

```bash
python assignments/week1/rag.py
```

## 上游

作业原仓库：[mihail911/modern-software-dev-assignments](https://github.com/mihail911/modern-software-dev-assignments)（本仓库 remote 为 `upstream`）。
