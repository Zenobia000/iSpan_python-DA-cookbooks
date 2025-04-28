# `.py` 與 `.ipynb` 環境差異

在 Python 程式開發中，我們通常會使用兩種不同的檔案格式：`.py` (Python 腳本) 和 `.ipynb` (Jupyter Notebook)。雖然這兩種環境都用於編寫和執行 Python 代碼，但它們在實際運作方式上存在顯著差異，特別是在檔案路徑處理、執行環境和代碼組織上。本教學將探討這些差異，並提供實用的解決方案。

## 基本概念

### Python 腳本 (`.py`)

Python 腳本是包含 Python 程式碼的純文字檔案，通常使用一般文字編輯器或整合開發環境 (IDE) 編寫，如 VS Code、PyCharm 等。

**特點**：
- 從上到下順序執行
- 通常一次性執行整個檔案
- 需要額外工具才能可視化結果
- 適合系統程式和工具開發

### Jupyter Notebook (`.ipynb`)

Jupyter Notebook 是一種互動式開發環境，它允許在網頁瀏覽器中創建和共享包含程式碼、文字說明、數學方程式、視覺化和結果的文件。

**特點**：
- 基於單元格 (cell) 執行程式碼
- 可以選擇性地執行程式碼區塊
- 結果直接呈現在代碼下方
- 支持 Markdown、LaTeX 等格式化文本
- 適合數據分析、教學和展示

## 主要差異

### 1. 執行模型

**`.py` 檔案**：
- 由 Python 解釋器從上到下完整執行
- 使用 `python script.py` 命令執行
- 變數在腳本結束後消失 (除非是模組)

```python
# example.py
print("Step 1")
x = 10
print("Step 2")
y = x * 2
print(f"Final result: {y}")
```

**`.ipynb` 檔案**：
- 由 Jupyter 核心 (kernel) 逐個單元格執行
- 單元格可以多次、非順序或選擇性執行
- 變數在核心的整個生命週期內保持活躍

```python
# 單元格 1
print("Step 1")
x = 10

# 單元格 2 (可以獨立執行)
print("Step 2")
y = x * 2
print(f"Final result: {y}")
```

### 2. 檔案路徑差異

這是兩種環境最重要的差異之一，也是初學者最容易遇到的問題。

**`.py` 檔案**：
- 有 `__file__` 變數，表示當前腳本檔案的路徑
- 可以基於腳本位置構建相對路徑

```python
# script.py
import os

# 獲取腳本所在目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, "data", "input.csv")

print(f"Script path: {__file__}")
print(f"Data file path: {data_file}")
```

**`.ipynb` 檔案**：
- **沒有** `__file__` 變數
- 路徑相對於啟動 Jupyter 服務的目錄 (當前工作目錄)

```python
# In Jupyter Notebook
import os

# 當前工作目錄 (不是 notebook 文件位置)
current_dir = os.getcwd()
data_file = os.path.join(current_dir, "data", "input.csv")

print(f"Working directory: {current_dir}")
print(f"Data file path: {data_file}")

# 如果嘗試訪問 __file__ 會出錯
# print(f"Notebook path: {__file__}")  # NameError
```

### 3. 執行環境

**`.py` 檔案**：
- 有清晰的執行入口 (`if __name__ == "__main__"`)
- 可以作為模組導入
- 環境隔離，每次執行都是全新的環境

```python
# module.py
def add(a, b):
    return a + b

# 只有直接執行時才運行
if __name__ == "__main__":
    print(add(5, 3))
```

**`.ipynb` 檔案**：
- 沒有明確的入口點
- 難以作為模組導入 (雖然可以用 nbimport 等工具)
- 狀態持續，之前執行的代碼會影響後續執行

```python
# 在 Jupyter Notebook 中
def add(a, b):
    return a + b

# 直接測試，沒有 __name__ == "__main__" 概念
add(5, 3)
```

### 4. 程式碼組織與清晰度

**`.py` 檔案**：
- 代碼組織為函數和類
- 良好的模組化和重用
- 利於版本控制和協作

**`.ipynb` 檔案**：
- 混合程式碼、文本和輸出
- 易於探索和實驗
- 版本控制較為複雜 (JSON 格式帶有輸出)

## 常見問題與解決方案

### 問題 1：在 Jupyter 中處理檔案路徑

**問題**：Jupyter 沒有 `__file__` 變數，難以構建相對路徑

**解決方案**：

```python
# 方案 1: 設定固定的專案根目錄
PROJECT_ROOT = '/path/to/your/project'

# 方案 2: 使用當前工作目錄
import os
PROJECT_ROOT = os.getcwd()

# 方案 3: 使用巧妙的方法找到專案根目錄
from pathlib import Path
import os

def find_project_root(start_dir=None):
    """尋找專案根目錄 (有 .git, pyproject.toml 等標記的目錄)"""
    start_dir = Path(start_dir or os.getcwd())
    for dir in [start_dir, *start_dir.parents]:
        if any((dir / marker).exists() for marker in ['.git', 'pyproject.toml', 'setup.py']):
            return dir
    return start_dir

PROJECT_ROOT = find_project_root()
```

### 問題 2：跨環境使用相同代碼

**問題**：如何編寫在 `.py` 和 `.ipynb` 中都能正常工作的代碼

**解決方案**：使用環境檢測和路徑輔助函數

```python
import os
from pathlib import Path

def get_project_root():
    """獲取專案根目錄，適用於 .py 和 .ipynb 環境"""
    try:
        # 嘗試使用 __file__ (.py 環境)
        script_path = Path(__file__).resolve()
        return script_path.parent.parent  # 根據實際層級調整
    except NameError:
        # 在 Jupyter 環境中尋找項目標記
        current_dir = Path.cwd()
        for dir in [current_dir, *current_dir.parents]:
            if any((dir / marker).exists() for marker in ['.git', 'pyproject.toml']):
                return dir
        # 如果找不到標記，使用當前目錄
        return current_dir

def get_data_path(relative_path):
    """獲取數據檔案的路徑"""
    return get_project_root() / 'data' / relative_path

# 使用範例
data_file = get_data_path('input.csv')
```

### 問題 3：從 `.ipynb` 導入函數到其他文件

**問題**：Jupyter Notebook 不易作為模組導入

**解決方案**：提取重要功能到 `.py` 文件

1. 將 notebook 中的核心函數複製到一個 `.py` 文件中
2. 在 notebook 中導入這個 `.py` 文件而不是反向操作

```python
# 在 utils.py 中
def process_data(data):
    # 數據處理邏輯
    return processed_data

# 在 notebook 中
from utils import process_data

# 使用導入的函數
result = process_data(my_data)
```

另一個選擇是使用 `nbconvert` 將 notebook 轉換為 Python 腳本：

```bash
jupyter nbconvert --to python your_notebook.ipynb
```

### 問題 4：筆記本中的環境隔離

**問題**：Jupyter Notebook 中狀態持續，可能導致"隱藏狀態"問題

**解決方案**：採用良好的重啟和重執行習慣

1. 使用 "Restart & Run All" 功能測試整個筆記本
2. 明確定義和初始化所有變數
3. 避免依賴特定的執行順序
4. 模組化功能，減少狀態依賴

## `.py` 和 `.ipynb` 的適用場景

### 適合 `.py` 的場景

- 系統程式和實用工具
- 需要重複和自動化執行的腳本
- 可重用的函數庫和模組
- 命令行介面和 API
- 大型專案和生產環境代碼

### 適合 `.ipynb` 的場景

- 數據探索和分析
- 視覺化和圖表生成
- 教學和演示材料
- 互動式實驗
- 結果與解釋並重的報告

## 混合使用的最佳實踐

### 1. 創建可重用的 Python 模組

將通用功能放在 `.py` 文件中，並在 notebooks 中導入使用：

```python
# utils.py
def load_data(file_path):
    # 加載數據的代碼
    return data

def process_data(data, param1, param2):
    # 處理數據的代碼
    return processed_data
```

```python
# analysis.ipynb
from utils import load_data, process_data

# 使用模組功能
data = load_data('data/mydata.csv')
result = process_data(data, param1=10, param2='value')
```

### 2. 使用公共路徑處理函數

建立一個處理路徑的公共模組，適用於所有環境：

```python
# paths.py
import os
from pathlib import Path

def get_project_root():
    """獲取專案根目錄"""
    try:
        # 嘗試使用 __file__ (.py 環境)
        return Path(__file__).resolve().parent
    except NameError:
        # Jupyter 環境
        return Path.cwd()

def get_data_file(filename):
    """獲取數據檔案路徑"""
    return get_project_root() / 'data' / filename

def get_config_file(filename):
    """獲取設定檔案路徑"""
    return get_project_root() / 'config' / filename
```

### 3. 使用環境變數設定路徑

在所有環境中使用環境變數設定關鍵路徑：

```python
# 在 .env 檔案中設定
PROJECT_ROOT=/path/to/your/project
DATA_DIR=/path/to/your/data

# 在 Python 代碼中使用
import os
from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = os.environ.get('PROJECT_ROOT')
DATA_DIR = os.environ.get('DATA_DIR')
```

### 4. 開發流程建議

1. 在 Jupyter Notebook 中**探索並開發**
2. 將穩定的功能**提取到 `.py` 模組**中
3. 在 notebook 中**導入和使用**模組
4. 使用 notebook 進行**實驗和視覺化**
5. 使用 `.py` 腳本進行**自動化和生產**

## 結論與最佳實踐總結

1. **了解環境差異**：認識 `.py` 和 `.ipynb` 的基本差異，特別是路徑處理
2. **模組化功能**：將核心功能放在 `.py` 文件中，便於重用和測試
3. **共用路徑工具**：創建適用於兩種環境的路徑處理工具
4. **環境適應性**：編寫能自動檢測環境並適應的代碼
5. **正確性檢查**：始終測試代碼在不同環境中的行為
6. **明確依賴**：避免隱藏狀態，明確定義所有依賴
7. **組合優勢**：利用兩種環境的優勢，`.py` 用於穩定代碼，`.ipynb` 用於探索和展示

## 下一步學習

現在你已經了解了 `.py` 和 `.ipynb` 環境的差異及處理技巧，可以進一步學習如何從函數式編程過渡到[物件導向設計](./07_functions_to_classes.md)，這將幫助你組織更複雜的程式邏輯。