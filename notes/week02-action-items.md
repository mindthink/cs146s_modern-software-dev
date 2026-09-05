# Week 2 — Action Item Extractor notes

作业目录：[`assignments/week2`](../assignments/week2/)

## 本周目标

把「自由笔记 → 行动项清单」小应用做完整：启发式抽取、LLM 抽取、API 契约、前端按钮、文档。

## TODO 清单

| TODO | 内容 | 笔记 |
|------|------|------|
| 1 | `extract_action_items_llm` + Ollama structured JSON | `extract.py` |
| 2 | LLM 单元测试（mock `ollama.chat`） | `tests/test_extract.py` |
| 3 | 重构：schemas / lifespan / 错误处理 | `schemas.py`, `main.py`, routers |
| 4 | `extract-llm` + `GET /notes` + 前端按钮 | routers + `frontend/index.html` |
| 5 | 生成 README | `README.md` |

## 本地命令

```bash
poetry run uvicorn assignments.week2.app.main:app --reload
cd assignments && python -m pytest week2/tests/test_extract.py -q
```

## 参考

- [`assignment.md`](../assignments/week2/assignment.md)
- [`writeup.md`](../assignments/week2/writeup.md)
- [Ollama structured outputs](https://ollama.com/blog/structured-outputs)
