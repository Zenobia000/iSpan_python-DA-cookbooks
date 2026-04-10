# 虛擬環境管理入門

虛擬環境讓每個專案擁有獨立的套件空間，避免版本衝突。本節帶你學會建立與管理虛擬環境。

---

**本節目標：**
- 了解為什麼需要虛擬環境
- 學會用 venv 建立/啟動/停用虛擬環境
- 認識 conda 與 Poetry 的虛擬環境管理
- 學會在 Jupyter Notebook 中使用虛擬環境

## 1. 為什麼需要虛擬環境？

想像你同時在做兩個專案：

| | 專案 A | 專案 B |
|:---|:---|:---|
| 需要 pandas | 1.5 版 | 2.1 版 |

如果共用同一個環境，兩個版本會互相衝突。

**虛擬環境 = 每個專案一個獨立的 Python 環境**，套件互不干擾。

```
電腦
 ├── 專案 A/
 │    └── .venv/          ← pandas 1.5
 └── 專案 B/
      └── .venv/          ← pandas 2.1
```

## 2. 三種虛擬環境工具

| | venv | conda env | Poetry |
|:---|:---|:---|:---|
| **來源** | Python 內建 | Anaconda/Miniconda | 需額外安裝 |
| **搭配的套件工具** | pip | conda | poetry |
| **適合對象** | 通用開發 | 資料科學 | 專案管理 |
| **難度** | 最簡單 | 簡單 | 中等 |

> **初學者建議：先學 venv，它是 Python 內建的，不需要額外安裝。**

## 3. venv — Python 內建虛擬環境

venv 是 Python 3.3+ 內建的模組，使用最簡單。

### 3.1 建立虛擬環境

先用終端機進入你的專案資料夾，然後：

#### 所有作業系統通用
```bash
python -m venv .venv
```

> **說明：**
> - `python -m venv` = 使用 Python 的 venv 模組
> - `.venv` = 虛擬環境的資料夾名稱（慣例命名）
> - macOS/Linux 上如果 `python` 指向 Python 2，請改用 `python3 -m venv .venv`

### 3.2 啟動虛擬環境

建立後需要「啟動」才能使用：

#### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

> **PowerShell 權限問題？** 如果出現「無法載入...因為這個系統上已停用指令碼執行」，請先執行：
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

#### Windows (CMD)
```cmd
.venv\Scripts\activate.bat
```

#### macOS / Linux
```bash
source .venv/bin/activate
```

啟動成功後，終端機提示符前面會出現 `(.venv)`：
```
(.venv) $ _
```

### 3.3 在虛擬環境中安裝套件

啟動虛擬環境後，用 pip 安裝的套件只會裝在這個環境裡：

```bash
# 安裝課程所需套件
pip install jupyter matplotlib pandas numpy

# 確認套件安裝在虛擬環境中
pip list
```

### 3.4 停用虛擬環境

#### 所有作業系統通用
```bash
deactivate
```

停用後，提示符前面的 `(.venv)` 會消失。

### 3.5 刪除虛擬環境

虛擬環境就是一個資料夾，刪除它就好：

#### Windows
```powershell
Remove-Item -Recurse -Force .venv
```

#### macOS / Linux
```bash
rm -rf .venv
```

### 3.6 venv 指令速查表

| 動作 | Windows (PowerShell) | macOS / Linux |
|:---|:---|:---|
| 建立 | `python -m venv .venv` | `python3 -m venv .venv` |
| 啟動 | `.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` |
| 停用 | `deactivate` | `deactivate` |
| 刪除 | `Remove-Item -Recurse -Force .venv` | `rm -rf .venv` |

## 4. conda 虛擬環境

如果你使用 Anaconda 或 Miniconda，conda 自帶虛擬環境管理。

### conda 環境指令（所有 OS 通用）

| 動作 | 指令 |
|:---|:---|
| 建立環境 | `conda create -n myenv python=3.11` |
| 啟動環境 | `conda activate myenv` |
| 停用環境 | `conda deactivate` |
| 查看所有環境 | `conda env list` |
| 刪除環境 | `conda env remove -n myenv` |
| 匯出環境 | `conda env export > environment.yml` |
| 從檔案建立 | `conda env create -f environment.yml` |

> **conda vs venv 差異：** conda 環境預設存在集中位置（`~/anaconda3/envs/`），而 venv 存在專案資料夾內。

## 5. Poetry 虛擬環境

Poetry 會自動為每個專案建立虛擬環境，你不需要手動管理。

### Poetry 環境指令

| 動作 | 指令 |
|:---|:---|
| 建立專案（自動建環境） | `poetry new my_project` |
| 安裝依賴（自動建環境） | `poetry install` |
| 查看環境資訊 | `poetry env info` |
| 進入環境 shell | `poetry shell` |
| 在環境中執行指令 | `poetry run python script.py` |
| 刪除環境 | `poetry env remove python` |

### Poetry 專案結構

```
my_project/
 ├── pyproject.toml     ← 專案設定與套件依賴
 ├── poetry.lock        ← 鎖定的版本（自動產生）
 ├── src/
 │    └── my_project/
 │         └── __init__.py
 └── tests/
      └── __init__.py
```

> `pyproject.toml` 類似 pip 的 `requirements.txt`，但功能更強大。

## 6. 在 Jupyter Notebook 中使用虛擬環境

建立虛擬環境後，需要額外設定才能在 Jupyter 中使用它。

### 步驟（適用 venv 與 Poetry）

```bash
# 1. 啟動虛擬環境（venv 範例）
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\Activate.ps1      # Windows

# 2. 安裝 ipykernel
pip install ipykernel

# 3. 將虛擬環境註冊為 Jupyter kernel
python -m ipykernel install --user --name=my_project --display-name="My Project"

# 4. 啟動 Jupyter Notebook
jupyter notebook
```

在 Notebook 中選擇 **Kernel > Change Kernel > My Project** 即可使用該虛擬環境。

### 管理 Jupyter Kernel

```bash
# 查看所有已註冊的 kernel
jupyter kernelspec list

# 移除不需要的 kernel
jupyter kernelspec remove my_project
```

## 7. 動手驗證

在 Python 互動模式或腳本中執行：

```python
import sys

# 檢查目前是否在虛擬環境中
in_venv = sys.prefix != sys.base_prefix
print(f"是否在虛擬環境中: {in_venv}")
print(f"Python 路徑: {sys.executable}")
print(f"環境前綴: {sys.prefix}")
```

## 8. 實作練習

請依照以下步驟操作（在終端機中執行）：

1. 建立一個練習用資料夾：`mkdir my_practice && cd my_practice`
2. 建立虛擬環境：`python -m venv .venv`（或 `python3 -m venv .venv`）
3. 啟動虛擬環境（依你的 OS 選擇指令）
4. 安裝 pandas：`pip install pandas`
5. 確認安裝：`pip list`
6. 停用虛擬環境：`deactivate`
7. 再次執行 `pip list`，比較差異

## 重點整理

| 工具 | 建立環境 | 啟動環境 | 停用 |
|:---|:---|:---|:---|
| **venv** | `python -m venv .venv` | `source .venv/bin/activate` (Mac/Linux) | `deactivate` |
| | | `.venv\Scripts\Activate.ps1` (Windows) | |
| **conda** | `conda create -n env python=3.11` | `conda activate env` | `conda deactivate` |
| **Poetry** | `poetry new project` | `poetry shell` | `exit` |

---

**下一節：** [03_version_control_intro.md](./03_version_control_intro.md) — 學習用 Git 做版本控制。
