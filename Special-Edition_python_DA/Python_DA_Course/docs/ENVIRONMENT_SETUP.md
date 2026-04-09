# 環境安裝指引 | Environment Setup

本文件說明如何在本機建立執行 **Python DA 12 小時精煉課程** 所需的環境。建議使用獨立虛擬環境，避免與系統 Python 或其他專案套件衝突。

---

## 1. 系統需求

| 項目 | 最低需求 | 建議 |
| :--- | :--- | :--- |
| Python | 3.9 以上 | 3.11 或 3.12 |
| 記憶體 (RAM) | 4 GB | 8 GB 以上 |
| 硬碟空間 | 2 GB 可用空間 | 5 GB 以上 |
| 作業系統 | macOS / Windows 10+ / Linux | macOS 或 Ubuntu 22.04 |
| 瀏覽器 | 最新版 Chrome / Firefox / Edge | Chrome |

檢查 Python 版本：

```bash
python3 --version
```

如果顯示 `Python 3.9.x` 以上即可；若低於 3.9，請參考 FAQ 第 3 點升級。

---

## 2. 快速安裝

請從以下三種路徑擇一執行。本課程統一以 `requirements.txt` 管理相依套件。

### 方法 A：venv + pip（macOS / Linux，推薦）

```bash
# 1. 進入課程目錄
cd Special-Edition_python_DA/Python_DA_Course

# 2. 建立虛擬環境
python3 -m venv .venv

# 3. 啟用虛擬環境
source .venv/bin/activate

# 4. 升級 pip
python -m pip install --upgrade pip

# 5. 安裝相依套件
pip install -r requirements.txt
```

### 方法 B：venv + pip（Windows PowerShell）

```powershell
# 1. 進入課程目錄
cd Special-Edition_python_DA\Python_DA_Course

# 2. 建立虛擬環境
python -m venv .venv

# 3. 啟用虛擬環境
.\.venv\Scripts\Activate.ps1

# 4. 升級 pip
python -m pip install --upgrade pip

# 5. 安裝相依套件
pip install -r requirements.txt
```

若 PowerShell 無法執行啟用指令，請以系統管理員開啟 PowerShell 執行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 方法 C：conda 替代方案（跨平台）

```bash
# 1. 建立 conda 環境
conda create -n python-da python=3.11 -y

# 2. 啟用環境
conda activate python-da

# 3. 安裝相依套件（仍可透過 pip）
pip install -r Special-Edition_python_DA/Python_DA_Course/requirements.txt
```

若偏好純 conda 管理，可改用：

```bash
conda install -c conda-forge numpy pandas matplotlib seaborn plotly jupyter notebook ipykernel pytest
```

---

## 3. 驗證安裝

安裝完成後，執行下列 Python 片段驗證所有套件是否正常載入：

```python
import sys
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
import plotly

print(f"Python : {sys.version.split()[0]}")
print(f"numpy  : {np.__version__}")
print(f"pandas : {pd.__version__}")
print(f"mpl    : {matplotlib.__version__}")
print(f"seaborn: {sns.__version__}")
print(f"plotly : {plotly.__version__}")
print("All packages imported successfully.")
```

或直接在終端機一行執行：

```bash
python -c "import numpy, pandas, matplotlib, seaborn, plotly; print('OK', numpy.__version__, pandas.__version__)"
```

預期輸出版本應落在 `requirements.txt` 所指定的範圍內。

---

## 4. 啟動 Jupyter

本課程所有教材皆為 `.ipynb` 格式，需使用 Jupyter 執行。

### 兩種啟動方式

| 指令 | 介面 | 適用情境 |
| :--- | :--- | :--- |
| `jupyter notebook` | 傳統 Notebook UI | 介面單純、初學者友善 |
| `jupyter lab` | JupyterLab（多分頁 IDE） | 多檔案並行編輯、變數檢視器 |

### 啟動步驟

```bash
# 確認已啟用虛擬環境後
cd Special-Edition_python_DA/Python_DA_Course

# 傳統 Notebook
jupyter notebook

# 或 JupyterLab
jupyter lab
```

執行後瀏覽器會自動開啟 `http://localhost:8888`。

### 第一個要打開的 Notebook

建議從以下檔案開始：

```
M1_Numpy_Basic/S1_numpy_vectorization.ipynb
```

這是 Session 1 的教材，確認能順利執行第一個 cell（`import numpy as np`）即代表環境就緒。

---

## 5. 常見問題 FAQ

### Q1. matplotlib 繪圖中文變「豆腐字」（□□□）

matplotlib 預設字型不含中文字符，需要額外設定中文字型。詳細步驟請參考：

```
docs/CHINESE_FONT_SETUP.md
```

快速解法（macOS）：

```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['PingFang TC', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
```

快速解法（Windows）：

```python
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
```

### Q2. pip 安裝速度很慢

可改用台灣或中國境內的 PyPI 鏡像站：

```bash
# 台灣交大鏡像
pip install -r requirements.txt -i https://pypi.org/simple/

# 清華大學鏡像（速度通常最快）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 阿里雲鏡像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

設定為永久預設值：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3. Python 版本衝突（系統是 3.8 或更舊）

推薦兩種管理工具：

**pyenv（macOS / Linux）**

```bash
# macOS 安裝
brew install pyenv

# 安裝 Python 3.11
pyenv install 3.11.9
pyenv local 3.11.9

# 驗證
python --version
```

**conda（跨平台）**

直接下載 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 安裝，再依本文件「方法 C」建立環境。

### Q4. Jupyter 找不到 kernel，或 kernel 啟動失敗

將當前虛擬環境註冊為 Jupyter kernel：

```bash
# 確認虛擬環境已啟用
python -m ipykernel install --user --name python-da --display-name "Python (DA Course)"
```

之後在 Jupyter 介面右上角選擇 `Python (DA Course)` 即可。

若 kernel 仍無法啟動，請依序檢查：

1. 確認 `ipykernel` 已安裝：`pip show ipykernel`
2. 確認虛擬環境路徑正確：`which python`（macOS/Linux）或 `where python`（Windows）
3. 移除舊 kernel 後重新註冊：`jupyter kernelspec uninstall python-da`

---

## 附錄：一鍵安裝腳本（macOS / Linux）

```bash
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import numpy, pandas, matplotlib, seaborn, plotly; print('Setup completed.')"
```

將上述內容存為 `scripts/setup.sh`，執行 `bash scripts/setup.sh` 即可完成安裝與驗證。
