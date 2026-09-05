# Week 6 — Semgrep CLI notes

作业目录：[`assignments/week6`](../assignments/week6/)

## 做法

用 **Semgrep CLI**（不开 AppSec 云）：

```bash
.venv-semgrep/bin/semgrep scan --config auto assignments/week6
```

（独立 venv，避免和 week3 `mcp 2.x` 冲突。）

## 已修（≥3）

1. CORS `*` → 本地 origin 白名单
2. `/unsafe-search` f-string SQL → 绑定参数
3. `eval` → 禁用；顺带 `shell=True` / 动态 `urlopen`

复扫：**0 findings**；`pytest`：**3 passed**。Write-up：[`writeup.md`](../assignments/week6/writeup.md)
