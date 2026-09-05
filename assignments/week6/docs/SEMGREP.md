# Week 6 — Semgrep CLI 使用过程

本文记录本机用 **Semgrep 命令行**（不登录 AppSec 云平台）扫描、分诊、修复、复验的完整流程。

作业要求见 [`assignment.md`](../assignment.md)；修复说明见 [`writeup.md`](../writeup.md)。

---

## 1. 为什么用 CLI

- Semgrep **CLI 开源免费**，适合本作业。
- AppSec Platform / 付费账号不是必须。
- 本仓库 Poetry 里已有 `mcp 2.x`（week3），与当前 Semgrep 依赖的 `mcp 1.x` **冲突**，因此 **不要** `poetry add semgrep`，改用独立虚拟环境。

---

## 2. 安装（一次性）

在**仓库根目录**执行：

```bash
cd /path/to/modern-software-dev-assignments

python3 -m venv .venv-semgrep
.venv-semgrep/bin/pip install -U pip semgrep

.venv-semgrep/bin/semgrep --version
# 期望类似：1.176.x
```

`.venv-semgrep/` 已写入根目录 `.gitignore`，不会进 git。

可选：在 shell 里加别名：

```bash
alias semgrep='$PWD/.venv-semgrep/bin/semgrep'   # 需在仓库根目录时使用
```

---

## 3. 扫描

### 3.1 作业推荐的“整包”思路

课程原文（仓库尚未改路径时）类似：

```bash
semgrep ci --subdir week6
```

本仓库作业在 `assignments/week6/`，且我们用本地 CLI + 社区规则包，等价实用命令为：

```bash
# 在仓库根目录
.venv-semgrep/bin/semgrep scan --config auto assignments/week6
```

说明：

| 参数 | 含义 |
|------|------|
| `scan` | 本地扫描（不必 `semgrep login`） |
| `--config auto` | 拉取/使用通用安全规则包（SAST 等） |
| 路径 | 只扫 week6，避免误报其它周 |

### 3.2 可选：更聚焦的规则

```bash
# 密钥类（若包可用）
.venv-semgrep/bin/semgrep scan --config p/secrets assignments/week6

# JSON 输出便于归档
.venv-semgrep/bin/semgrep scan --config auto --json -o /tmp/week6-semgrep.json assignments/week6
```

### 3.3 首次扫描结果摘要（修复前）

当时 CLI 报出 **5 个 blocking Code Findings**（均为 SAST）：

1. **Wildcard CORS** — `backend/app/main.py`（`allow_origins=["*"]`）
2. **SQL 注入风险** — `backend/app/routers/notes.py` `/unsafe-search`（f-string 拼进 `sqlalchemy.text`）
3. **`eval()`** — `/debug/eval`
4. **`subprocess(..., shell=True)`** — `/debug/run`
5. **动态 `urllib.urlopen`** — `/debug/fetch`

作业要求至少修 **3** 个；本周实际修了上述 1–5（write-up 重点写了前 3 个）。

---

## 4. 分诊与修复原则

1. 先看 **规则 ID + 风险说明**（Semgrep 终端里的 Details 链接）。
2. 优先修：**注入 / RCE / 过宽 CORS**，再考虑弱哈希、路径读取等 demo 接口。
3. 改动尽量小：能绑参数就不要整段删掉业务；危险 demo 可以改为拒绝执行。
4. 每修一类，可再扫一次确认该 finding 消失。

本周具体改法见 [`writeup.md`](../writeup.md) 的 Fix #1–#3。

---

## 5. 复验

### 5.1 再跑 Semgrep

```bash
# 仓库根目录
.venv-semgrep/bin/semgrep scan --config auto assignments/week6
```

期望：**0 Code Findings**（exit code 0）。

### 5.2 跑测试（修完必须还能跑）

```bash
cd assignments/week6
PYTHONPATH=. poetry run pytest -q backend/tests
# 或：make test
```

期望：**3 passed**（或当前测试套件全绿）。

### 5.3 可选：启动应用手测

```bash
cd assignments/week6
make run
# 浏览器 http://127.0.0.1:8000
```

---

## 6. 推荐工作流（速查）

```text
安装 .venv-semgrep
    → semgrep scan --config auto assignments/week6
    → 记下 ≥3 个 finding
    → 最小改动修复
    → 再 scan + pytest
    → 填写 writeup.md
    → git commit / push
```

### GitHub Actions（仓库 CI）

推送到 `main` / 开 PR 时会跑 [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml)：

1. **Lint** — `black --check` + `ruff`（`assignments/week4`、`assignments/week6`）
2. **Test week4 / week6** — `pytest`
3. **Semgrep week6** — `semgrep scan --config auto --error assignments/week6`

本地等价：

```bash
# 仓库根
poetry run black --check assignments/week4 assignments/week6
poetry run ruff check assignments/week4 assignments/week6

cd assignments/week4 && PYTHONPATH=. poetry run pytest -q backend/tests
cd ../week6 && PYTHONPATH=. poetry run pytest -q backend/tests

# 根目录
.venv-semgrep/bin/semgrep scan --config auto --error assignments/week6
```

---

## 7. 常见问题

**Q: `semgrep ci` 要登录？**
A: `ci` 有时会走登录/平台流程。本作业用 `semgrep scan --config auto` 即可，无需账号。GitHub Actions 里用官方 `semgrep/semgrep` 镜像同样免登录。

**Q: `PermissionError` 写 `~/.semgrep/semgrep.log`？**
A: 确保在非沙箱环境执行，或检查对 `~/.semgrep` 的写权限。

**Q: Poetry 里装 semgrep 失败？**
A: 与 `mcp[cli] ^2` 版本冲突属预期；继续用仓库根目录的 `.venv-semgrep`，或在 CI 里用容器镜像。

**Q: 路径是 `week6` 还是 `assignments/week6`？**
A: 以本仓库为准，扫 **`assignments/week6`**。

---

## 8. 相关文件

| 文件 | 作用 |
|------|------|
| [`assignment.md`](../assignment.md) | 作业说明 |
| [`writeup.md`](../writeup.md) | 三个修复的 before/after 论述 |
| [`backend/app/main.py`](../backend/app/main.py) | CORS 修复 |
| [`backend/app/routers/notes.py`](../backend/app/routers/notes.py) | SQLi / eval / subprocess / fetch 修复 |
| 仓库根 `.venv-semgrep/` | 本机 Semgrep CLI（不提交） |
| [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml) | lint + tests + Semgrep |
