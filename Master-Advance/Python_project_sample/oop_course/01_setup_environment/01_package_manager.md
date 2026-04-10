# 套件管理工具入門

學會安裝、管理 Python 套件是開發的第一步。本節帶你認識三大套件管理工具，並依你的作業系統逐步操作。

---

**本節目標：**
- 了解什麼是「套件」與「套件管理工具」
- 學會使用 pip 安裝/移除/查看套件
- 認識 conda 與 Poetry，知道何時選用

## 1. 什麼是套件 (Package)？

套件 = 別人寫好的程式碼，打包起來讓你直接用。

| 你想做的事 | 你需要的套件 |
|:---|:---|
| 資料分析 | pandas |
| 畫圖表 | matplotlib |
| 網頁爬蟲 | requests |
| 機器學習 | scikit-learn |

**套件管理工具**就是幫你安裝、更新、移除這些套件的程式。

## 2. 三大工具比較

| | pip | conda | Poetry |
|:---|:---|:---|:---|
| **來源** | Python 內建 | Anaconda/Miniconda | 需額外安裝 |
| **套件來源** | PyPI | conda-forge + PyPI | PyPI |
| **虛擬環境** | 需搭配 venv | 內建 | 內建 |
| **適合對象** | 通用開發 | 資料科學 | 專案管理 |
| **難度** | 最簡單 | 簡單 | 中等 |

> **初學者建議：先學 pip，它是最基礎的工具。**

## 3. pip — Python 內建的套件管理工具

pip 隨 Python 一起安裝，不需額外設定。

### 3.1 確認 pip 已安裝

打開你的終端機（Terminal / 命令提示字元），輸入以下指令：

#### Windows
```powershell
pip --version
```

#### macOS / Linux
```bash
pip3 --version
```

> **注意：** macOS/Linux 上 `pip` 可能指向 Python 2，建議使用 `pip3` 確保對應 Python 3。
> 如果顯示版本號（如 `pip 24.x.x`），代表安裝成功。

### 3.2 常用指令速查

以下指令在所有作業系統通用（macOS/Linux 請將 `pip` 替換為 `pip3`）：

| 動作 | 指令 | 範例 |
|:---|:---|:---|
| 安裝套件 | `pip install 套件名稱` | `pip install pandas` |
| 安裝指定版本 | `pip install 套件名稱==版本` | `pip install pandas==2.1.0` |
| 更新套件 | `pip install --upgrade 套件名稱` | `pip install --upgrade pandas` |
| 移除套件 | `pip uninstall 套件名稱` | `pip uninstall pandas` |
| 查看已安裝套件 | `pip list` | |
| 搜尋特定套件 | `pip show 套件名稱` | `pip show pandas` |
| 匯出套件清單 | `pip freeze > requirements.txt` | |
| 從清單安裝 | `pip install -r requirements.txt` | |

### 3.3 動手試試看

在終端機中執行：

```bash
# 查看目前已安裝的套件
pip list

# 查看某個套件的詳細資訊
pip show pandas
```

### 3.4 requirements.txt — 記錄你的套件清單

當你想把專案分享給別人，或在新電腦上重建環境時：

```bash
# 匯出目前環境的所有套件
pip freeze > requirements.txt

# 在新環境中一次安裝所有套件
pip install -r requirements.txt
```

`requirements.txt` 長這樣：
```
pandas==2.1.0
matplotlib==3.8.0
jupyter==1.0.0
```

## 4. conda — 資料科學的好幫手

如果你安裝了 Anaconda 或 Miniconda，就已經有 conda 了。

### 何時選 conda？
- 你主要做資料分析、機器學習
- 你需要安裝有 C/C++ 依賴的科學運算套件（如 numpy、scipy）
- 你想要一個工具同時管理套件和虛擬環境

### conda 常用指令

| 動作 | 指令 |
|:---|:---|
| 安裝套件 | `conda install pandas` |
| 指定頻道安裝 | `conda install -c conda-forge 套件名稱` |
| 更新套件 | `conda update pandas` |
| 移除套件 | `conda remove pandas` |
| 查看已安裝 | `conda list` |

> **小提醒：** conda 和 pip 可以混用，但建議優先用 conda 安裝，找不到再用 pip。

## 5. Poetry — 專案級的套件管理

Poetry 適合有一定基礎、想要更嚴謹管理專案的開發者。

### 何時選 Poetry？
- 你在開發要發布的套件或應用程式
- 你想要精確鎖定每個依賴的版本
- 你需要管理開發用 vs 正式環境的套件

> **初學者不需要急著學 Poetry，先把 pip + venv 用熟就好。**

### 安裝 Poetry

#### Windows
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

#### macOS / Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

安裝後需設定 PATH（詳見 [Poetry 官方文件](https://python-poetry.org/docs/#installation)）。

驗證安裝：
```bash
poetry --version
```

### Poetry 常用指令

| 動作 | 指令 |
|:---|:---|
| 建立新專案 | `poetry new my_project` |
| 初始化既有專案 | `poetry init` |
| 安裝套件 | `poetry add pandas` |
| 安裝開發用套件 | `poetry add --group dev pytest` |
| 移除套件 | `poetry remove pandas` |
| 更新套件 | `poetry update` |
| 查看已安裝 | `poetry show` |
| 執行指令 | `poetry run python my_script.py` |

## 6. 我該選哪個工具？

```
你是初學者嗎？
  ├── 是 → 用 pip（Python 自帶，零設定）
  └── 否
        ├── 主要做資料科學？ → 用 conda
        └── 開發應用程式/套件？ → 用 Poetry
```

> 不管選哪個，都建議搭配**虛擬環境**使用（下一節會教）。

## 7. 驗證你的環境

在終端機或 Python 互動模式中執行：

```python
import sys
import platform

print(f"Python 版本: {sys.version}")
print(f"作業系統: {platform.system()} {platform.release()}")
print(f"Python 路徑: {sys.executable}")
```

檢查課程所需套件是否已安裝：

```python
required = ["jupyter", "matplotlib", "pandas", "numpy"]

for pkg in required:
    try:
        __import__(pkg)
        print(f"  {pkg}: 已安裝")
    except ImportError:
        print(f"  {pkg}: 未安裝 → 請執行 pip install {pkg}")
```

## 重點整理

| 工具 | 安裝方式 | 安裝套件 | 適合場景 |
|:---|:---|:---|:---|
| **pip** | Python 內建 | `pip install 套件` | 通用開發（初學首選） |
| **conda** | 安裝 Anaconda/Miniconda | `conda install 套件` | 資料科學 |
| **Poetry** | 官方安裝程式 | `poetry add 套件` | 專案管理 |

---

**下一節：** [02_virtual_environment.md](./02_virtual_environment.md) — 學習虛擬環境，讓每個專案有獨立的套件空間。
