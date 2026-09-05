# Week 1 — LLM 提示工程笔记

作业目录：[`assignments/week1`](../assignments/week1/)

## 本周在练什么

把「和模型对话」变成**可验证的实验**：同一任务、不同提示技术，观察稳定性与正确性。

| 文件 | 技术 | 要点 |
|------|------|------|
| `k_shot_prompting.py` | K-shot | 用输入→输出样例约束格式与行为 |
| `chain_of_thought.py` | CoT | 引导逐步推理 |
| `tool_calling.py` | Tool calling | 让模型调用工具再给答案 |
| `self_consistency_prompting.py` | Self-consistency | 多样本投票提高正确率 |
| `rag.py` | RAG | 先检索文档再生成；无 Context 会瞎编 API |
| `reflexion.py` | Reflexion | 根据失败反馈再改一轮 |

## RAG 小实验结论

- `YOUR_CONTEXT_PROVIDER` 返回 `[]` → 模型猜 Bearer / 错 URL，测试失败
- 返回 API 文档 → 能写出 `X-API-Key`、`/users/` 等正确片段

本质：**检索到的私有知识必须塞进 Context，生成才可靠。**

## 运行

```bash
source .venv/bin/activate
python assignments/week1/k_shot_prompting.py
python assignments/week1/rag.py
```

## 参考

- 导读：[课程大纲索引](./00-course-index.md)
- 专栏：https://zhuanlan.zhihu.com/p/1985789368133261187
