# Week 8 — multi-stack notes (self-study)

作业：[`assignments/week8`](../assignments/week8/) — 只做了 **A + C**（无 Bolt）。

| 版 | 目录 | 栈 | 端口 |
|----|------|----|------|
| A | `fastapi-notes/` | FastAPI + SQLite + 静态前端 | 8008 |
| C | `flask-notes/` | Flask（非 JS 后端）+ SQLite | 8009 |

```bash
cd assignments/week8/fastapi-notes && poetry run uvicorn app:app --reload --port 8008
cd assignments/week8/flask-notes && python app.py   # 先 pip install -r requirements.txt
```
