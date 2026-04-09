# Notebook Smoke Tests

靜態煙霧測試套件，驗證 6 個 session notebooks 的結構完整性，**無需安裝 numpy/pandas/jupyter**。

## 覆蓋項目

- **JSON 格式檢查** — 每個 `.ipynb` 可被 `json.load` 解析且包含 `cells`
- **Python 語法檢查** — 所有 code cells 串接後可被 `ast.parse`（自動剔除 `%magic` / `!shell`）
- **結構檢查** — 每個 notebook 至少含 1 個 markdown + 1 個 code cell
- **資料集存在性** — `datasets/ecommerce/` 下的 `products.csv`、`orders_raw.csv`、`customers.csv`
- **README 一致性** — 主 `README.md` 須提及 S1–S6 全部 session

## 執行方式

於 `Python_DA_Course/` 目錄下：

```bash
# 方式一：pytest（推薦）
python -m pytest tests/ -v

# 方式二：直接執行腳本
python tests/test_notebooks_static.py

# 僅收集測試（dry-run）
python -m pytest --collect-only tests/
```

## 為何不使用 nbclient / nbformat？

課程主機環境僅保證 **Python 3 stdlib + pytest**，未安裝 `nbformat`、`nbclient`、`numpy`、`pandas`。
本測試套件刻意只使用 `json`、`ast`、`pathlib`，確保在任何乾淨環境都可跑。

若需要完整執行 notebook（非靜態檢查），請另行建立 `test_notebooks_execute.py` 並安裝：

```bash
pip install nbclient nbformat pandas numpy matplotlib seaborn plotly
```

## 疑難排解

| 症狀 | 解法 |
| :--- | :--- |
| `pytest not installed` | `pip install pytest` |
| `Notebook not found` | 確認從 `Python_DA_Course/` 執行，且 worktree 完整 |
| `Syntax error in ...` | 檢查 notebook code cell 是否有未加 `%`/`!` 前綴的 shell 指令 |
| `Missing datasets` | 先執行 Unit 0 的資料生成腳本 |
