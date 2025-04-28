# 相對與絕對路徑

在 Python 程式中處理檔案路徑是一個常見但卻容易出錯的任務，特別是當你的程式需要在不同環境或作業系統上運行時。本教學將介紹 Python 中處理檔案路徑的基本概念和最佳實踐。

## 路徑的基本概念

### 絕對路徑

絕對路徑是從檔案系統的根目錄開始的完整路徑。它們始終指向同一位置，無論當前工作目錄是什麼。

**Windows 範例**:
```
C:\Users\username\Documents\project\data.txt
```

**Unix/Linux/macOS 範例**:
```
/home/username/Documents/project/data.txt
```

### 相對路徑

相對路徑是相對於當前工作目錄的路徑。它們的解析取決於程式的執行位置。

**範例**:
```
data/file.txt           # 相對於當前目錄的 data 子目錄
../logs/error.log       # 上一級目錄中的 logs 子目錄
./config.ini            # 當前目錄 (. 可省略)
```

## Python 中的路徑處理

### 當前工作目錄

Python 的當前工作目錄是執行 Python 指令碼的目錄，而不一定是指令碼檔案所在的目錄。這常常是路徑相關問題的根源。

```python
import os

# 獲取當前工作目錄
current_dir = os.getcwd()
print(f"當前工作目錄: {current_dir}")

# 改變當前工作目錄
os.chdir('/path/to/new/directory')
```

### 指令碼所在目錄

獲取執行中的 Python 指令碼所在目錄：

```python
import os
import sys

# 獲取當前指令碼的絕對路徑
script_path = os.path.abspath(__file__)
print(f"指令碼絕對路徑: {script_path}")

# 獲取指令碼所在的目錄
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"指令碼所在目錄: {script_dir}")
```

## `os.path` 模組

Python 的 `os.path` 模組提供了處理檔案路徑的基本功能：

### 路徑組合

```python
import os.path

# 組合路徑 (適用於所有作業系統)
data_dir = os.path.join('project', 'data')
file_path = os.path.join(data_dir, 'file.txt')
print(file_path)  # 在 Windows: project\data\file.txt
                  # 在 Unix: project/data/file.txt
```

### 路徑規範化

```python
import os.path

# 規範化路徑 (解析 . 和 .. 符號)
path = os.path.normpath('project/../data/./file.txt')
print(path)  # 輸出: data/file.txt

# 取得絕對路徑
abs_path = os.path.abspath('data/file.txt')
print(abs_path)  # 完整的絕對路徑
```

### 路徑分解

```python
import os.path

path = '/home/user/project/data/file.txt'

# 分離目錄和檔案名
dirname = os.path.dirname(path)   # /home/user/project/data
filename = os.path.basename(path) # file.txt

# 分離檔案名和副檔名
name, ext = os.path.splitext(filename)  # name='file', ext='.txt'
```

## `pathlib` 模組 (Python 3.4+)

Python 3.4 引入了 `pathlib` 模組，提供了一個更現代、物件導向的方式來處理檔案路徑：

```python
from pathlib import Path

# 創建路徑物件
path = Path('project') / 'data' / 'file.txt'
print(path)  # project/data/file.txt

# 獲取當前目錄
current_dir = Path.cwd()

# 獲取絕對路徑
abs_path = path.absolute()

# 相對路徑
rel_path = path.relative_to(Path.cwd())

# 路徑屬性
print(path.name)      # file.txt
print(path.stem)      # file
print(path.suffix)    # .txt
print(path.parent)    # project/data
```

## 常見問題與解決方案

### 問題 1: 在不同工作目錄執行時路徑錯誤

**解決方法**: 使用指令碼所在目錄作為基準

```python
import os

# 獲取指令碼所在目錄
base_dir = os.path.dirname(os.path.abspath(__file__))

# 從指令碼位置構建絕對路徑
config_path = os.path.join(base_dir, 'config.ini')
```

### 問題 2: 跨平台路徑問題

**解決方法**: 始終使用 `os.path.join()` 或 `pathlib.Path` 構建路徑

```python
# 不好的做法 - 不同平台表現不一致
path = 'data/file.txt'  # 在 Windows 上可能無法正常工作

# 好的做法 - 適用於所有平台
path = os.path.join('data', 'file.txt')
# 或
path = Path('data') / 'file.txt'
```

### 問題 3: 讀取套件內的資源檔案

**解決方法**: 使用相對於套件位置的路徑

```python
import os
import pkg_resources

# 方法 1: 使用 pkg_resources (適用於已安裝的套件)
data_path = pkg_resources.resource_filename('my_package', 'data/file.txt')

# 方法 2: 使用相對於套件位置的路徑
package_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(package_dir, 'data', 'file.txt')
```

## `.py` 與 `.ipynb` 環境的差異

Python 指令碼 (`.py`) 和 Jupyter Notebook (`.ipynb`) 處理檔案路徑有重要差異：

### Python 腳本 (`.py`)

- `__file__` 變數可用，指向當前指令碼檔案
- 可以使用 `os.path.dirname(os.path.abspath(__file__))` 取得指令碼所在目錄

```python
# 在 .py 檔案中
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data', 'file.txt')
```

### Jupyter Notebook (`.ipynb`)

- **沒有** `__file__` 變數
- 需要使用其他方式確定基礎路徑

```python
# 在 .ipynb 中取得當前工作目錄
import os
notebook_dir = os.getcwd()

# 或明確指定基礎路徑
base_dir = '/path/to/project'
data_path = os.path.join(base_dir, 'data', 'file.txt')
```

## 最佳實踐

### 1. 使用絕對路徑進行檔案操作

```python
import os

# 獲取指令碼所在目錄
base_dir = os.path.dirname(os.path.abspath(__file__))

# 構建絕對路徑
data_path = os.path.join(base_dir, 'data', 'file.txt')

# 進行檔案操作
with open(data_path, 'r') as file:
    content = file.read()
```

### 2. 集中定義路徑常數

```python
import os

# 在模組頂部定義所有基礎路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 使用這些常數
with open(CONFIG_PATH, 'r') as config_file:
    # ...
```

### 3. 創建路徑輔助函數

```python
import os

def get_project_path(relative_path):
    """獲取相對於專案根目錄的檔案路徑"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)

# 使用
config_path = get_project_path('config/settings.ini')
data_path = get_project_path('data/sample.csv')
```

### 4. 使用 `pathlib` (Python 3.4+)

```python
from pathlib import Path

# 獲取專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent

# 構建路徑
config_path = BASE_DIR / 'config' / 'settings.ini'
data_path = BASE_DIR / 'data' / 'sample.csv'

# 檔案操作
with open(config_path, 'r') as file:
    content = file.read()
```

### 5. 使用環境變數設定基礎路徑

```python
import os

# 從環境變數獲取專案根目錄
PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))

# 構建路徑
data_path = os.path.join(PROJECT_ROOT, 'data', 'file.txt')
```

## 範例：堅固的檔案路徑處理

結合上述最佳實踐，以下是一個堅固的路徑處理範例：

```python
import os
import sys
from pathlib import Path

def get_base_dir():
    """獲取專案基礎目錄，適用於不同環境"""
    try:
        # 嘗試使用 __file__ 變數 (.py 檔案)
        return Path(__file__).resolve().parent
    except NameError:
        # 在沒有 __file__ 的環境中 (.ipynb)
        return Path.cwd()

class ProjectPaths:
    """管理專案中所有路徑的類別"""
    
    def __init__(self, base_dir=None):
        # 設定基礎目錄
        self.base_dir = Path(base_dir) if base_dir else get_base_dir()
        
        # 定義專案子目錄
        self.data_dir = self.base_dir / 'data'
        self.config_dir = self.base_dir / 'config'
        self.output_dir = self.base_dir / 'output'
        
        # 確保必要目錄存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """確保必要目錄存在"""
        for directory in [self.data_dir, self.config_dir, self.output_dir]:
            directory.mkdir(exist_ok=True, parents=True)
    
    def get_data_file(self, filename):
        """獲取數據檔案的完整路徑"""
        return self.data_dir / filename
    
    def get_config_file(self, filename):
        """獲取設定檔案的完整路徑"""
        return self.config_dir / filename
    
    def get_output_file(self, filename):
        """獲取輸出檔案的完整路徑"""
        return self.output_dir / filename

# 使用
paths = ProjectPaths()
data_file = paths.get_data_file('sample.csv')
config_file = paths.get_config_file('settings.json')

# 讀取檔案
if data_file.exists():
    with open(data_file, 'r') as f:
        data = f.read()
else:
    print(f"找不到檔案: {data_file}")
```

## 下一步學習

現在你已經了解了如何正確處理檔案路徑，接下來讓我們學習如何處理[跨資料夾存取檔案](./05_cross_folder.md)的問題，這是構建更複雜 Python 應用程式的重要步驟。 