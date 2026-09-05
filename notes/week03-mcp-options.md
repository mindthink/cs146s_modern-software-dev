# Week 3 — Custom MCP Server notes

作业目录：[`assignments/week3`](../assignments/week3/)

## 本周目标

用 MCP 包一层真实外部 API：≥2 个 tools、STDIO 本地可跑、文档齐全；不抄官方 weather quickstart。

## 选题

**US equity options** — Yahoo Finance via `yfinance`（无需 API key）。

| Tool | 作用 |
|------|------|
| `get_option_expirations` | 到期日列表 + spot |
| `get_option_chain` | 近 ATM 精简期权链 |

## 设计要点

- **STDIO**：日志只写 stderr，stdout 留给 MCP JSON-RPC。
- **响应体量**：期权链字段裁剪 + 按距离 spot 截断，避免撑爆上下文。
- **韧性**：参数校验、空结果/错误 JSON、失败短退避重试（Yahoo 限流）。
- **SDK**：mcp 2.x 用 `MCPServer`（原 `FastMCP`）。

## 本地命令

```bash
poetry install
poetry run python assignments/week3/server/main.py
```

Cursor MCP：`command=poetry`，`args=["run","python","assignments/week3/server/main.py"]`，`cwd=仓库根目录`。

## 参考

- [`assignment.md`](../assignments/week3/assignment.md)
- [`README.md`](../assignments/week3/README.md)
- [MCP server quickstart](https://modelcontextprotocol.io/quickstart/server)
- [mcp 2.x migration (FastMCP → MCPServer)](https://py.sdk.modelcontextprotocol.io/v2/migration/)
