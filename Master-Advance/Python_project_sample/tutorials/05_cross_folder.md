# 跨資料夾存取檔案

在實際的 Python 專案中，我們常常需要在不同模組、不同目錄間讀取和寫入檔案。這種跨資料夾存取檔案的需求，特別是在模組化設計和套件開發中，是一個常見的挑戰。本教學將詳細介紹如何正確地處理這類問題。

## 問題情境

考慮一個典型的專案結構：

```
my_project/
│
├── main.py                 # 入口程式
├── config/                 # 設定檔案目錄
│   ├── settings.json
│   └── defaults.py
│
├── data/                   # 資料目錄
│   ├── input.csv
│   └── processed/
│       └── output.csv
│
└── src/                    # 源碼目錄
    ├── __init__.py
    ├── data_processor.py   # 需要存取 data/ 目錄中的檔案
    └── utils/
        ├── __init__.py
        └── file_utils.py   # 需要存取 config/ 目錄中的設定
```

在這個結構中，各個模組可能需要讀取不同目錄下的檔案：
- `main.py` 可能需要讀取 `config/settings.json`
- `src/data_processor.py` 可能需要讀取 `data/input.csv`
- `src/utils/file_utils.py` 可能需要寫入 `data/processed/output.csv`

## 主要挑戰

跨資料夾存取檔案的主要挑戰在於：

1. **相對路徑問題**: 由於 Python 的當前工作目錄是執行指令碼的位置而非指令碼所在位置，使用相對路徑常常導致錯誤
2. **模組匯入與執行**: 當模組被直接執行 vs. 被匯入執行時，路徑解析方式不同
3. **套件內資源存取**: 套件安裝後，資源檔案的位置可能變化
4. **跨平台兼容性**: 不同作業系統的路徑表示方式不同

## 解決方案

### 1. 基於專案根目錄的路徑解析

最常見且推薦的方法是基於專案根目錄建立所有路徑。

#### 方法 A: 在每個模組中導航到根目錄

```python
# src/data_processor.py
import os

# 獲取當前模組的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

# 導航到專案根目錄 (src/ 的上一層)
project_root = os.path.dirname(current_dir)

# 構建資料檔案的絕對路徑
input_file = os.path.join(project_root, 'data', 'input.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'output.csv')

# 使用絕對路徑讀取和寫入檔案
with open(input_file, 'r') as f:
    data = f.read()
    
# 處理數據...

with open(output_file, 'w') as f:
    f.write(processed_data)
```

#### 方法 B: 使用 pathlib (Python 3.4+)

```python
# src/data_processor.py
from pathlib import Path

# 獲取當前模組的路徑
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent

# 構建資料檔案的路徑
input_file = project_root / 'data' / 'input.csv'
output_file = project_root / 'data' / 'processed' / 'output.csv'

# 使用路徑物件
with open(input_file, 'r') as f:
    data = f.read()

# 處理數據...

with open(output_file, 'w') as f:
    f.write(processed_data)
```

### 2. 集中式路徑管理

更好的方法是將所有路徑邏輯集中在一個模組中，便於維護和更新。

```python
# src/utils/paths.py
import os
from pathlib import Path

class ProjectPaths:
    def __init__(self):
        # 獲取專案根目錄
        self.root = Path(__file__).resolve().parent.parent.parent
        
        # 定義常用目錄
        self.config_dir = self.root / 'config'
        self.data_dir = self.root / 'data'
        self.processed_dir = self.data_dir / 'processed'
        
        # 確保必要目錄存在
        self.processed_dir.mkdir(exist_ok=True, parents=True)
    
    def get_config_file(self, filename):
        """獲取設定檔案路徑"""
        return self.config_dir / filename
    
    def get_input_file(self, filename):
        """獲取輸入資料檔案路徑"""
        return self.data_dir / filename
    
    def get_output_file(self, filename):
        """獲取輸出資料檔案路徑"""
        return self.processed_dir / filename

# 創建單例實例
project_paths = ProjectPaths()
```

然後在其他模組中使用這個集中式路徑管理：

```python
# src/data_processor.py
from .utils.paths import project_paths

# 獲取文件路徑
input_file = project_paths.get_input_file('input.csv')
output_file = project_paths.get_output_file('output.csv')

# 使用路徑
with open(input_file, 'r') as f:
    data = f.read()
```

### 3. 環境變數設定根目錄

對於更複雜的專案，可以使用環境變數設定專案根目錄：

```python
# src/utils/paths.py
import os
from pathlib import Path

# 從環境變數讀取專案根目錄，若未設定則嘗試推導
PROJECT_ROOT = os.environ.get(
    'PROJECT_ROOT',
    str(Path(__file__).resolve().parent.parent.parent)
)

def get_project_path(relative_path):
    """獲取相對於專案根目錄的檔案路徑"""
    return os.path.join(PROJECT_ROOT, relative_path)

# 使用
config_file = get_project_path('config/settings.json')
```

### 4. 使用套件資源系統

對於已封裝為套件的專案，可以使用 Python 的套件資源系統：

```python
# 使用 pkg_resources (setuptools)
import pkg_resources

# 獲取套件資源路徑
config_path = pkg_resources.resource_filename('my_package', 'config/settings.json')
template_str = pkg_resources.resource_string('my_package', 'templates/base.html').decode('utf-8')

# 使用 importlib.resources (Python 3.7+)
from importlib import resources

with resources.open_text('my_package.config', 'settings.json') as f:
    config_data = f.read()
```

## 不同執行情境的處理

### 1. 直接執行 vs. 模組匯入

當一個 Python 檔案既可能被直接執行，也可能被作為模組匯入時，可以使用以下模式：

```python
# src/data_processor.py
import os
import sys

def get_project_root():
    """獲取專案根目錄，適用於直接執行和模組匯入"""
    file_path = os.path.abspath(__file__)
    if getattr(sys, 'frozen', False):
        # 處理打包後的執行檔案 (如 PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # 正常執行環境
        return os.path.dirname(os.path.dirname(file_path))

def process_data():
    project_root = get_project_root()
    input_file = os.path.join(project_root, 'data', 'input.csv')
    # 處理數據...

if __name__ == "__main__":
    # 當作為主程式執行時
    process_data()
```

### 2. Jupyter Notebook 環境

在 Jupyter Notebook 中，由於沒有 `__file__` 變數，需要使用替代方法：

```python
# 在 Jupyter Notebook 中
import os
from pathlib import Path

# 方法 1: 明確設定專案根目錄
PROJECT_ROOT = '/path/to/my_project'

# 方法 2: 假設當前工作目錄是專案根目錄
PROJECT_ROOT = os.getcwd()

# 方法 3: 向上找尋特定標記檔案 (如 .git, pyproject.toml)
def find_project_root(start_dir=None):
    """向上搜尋專案根目錄 (尋找標記檔案)"""
    start_dir = Path(start_dir or os.getcwd())
    for dir in [start_dir, *start_dir.parents]:
        # 檢查是否有標記專案根目錄的檔案
        if (dir / '.git').exists() or (dir / 'pyproject.toml').exists():
            return dir
    # 若未找到，使用當前目錄
    return start_dir

PROJECT_ROOT = find_project_root()
```

## 跨平台考量

為確保代碼在不同作業系統上正常工作：

```python
# 永遠使用 os.path.join 或 pathlib.Path 處理路徑
# 不好的做法
file_path = project_root + '/data/input.csv'  # 在 Windows 上可能失效

# 好的做法 (os.path)
file_path = os.path.join(project_root, 'data', 'input.csv')

# 好的做法 (pathlib)
file_path = project_root / 'data' / 'input.csv'
```

## 實例：完整的跨目錄檔案存取解決方案

以下是一個完整的解決方案，將所有路徑邏輯封裝在一個類中，並處理不同執行環境：

```python
# src/utils/paths.py
import os
import sys
from pathlib import Path

class ProjectPaths:
    """專案路徑管理器"""
    
    def __init__(self, base_dir=None):
        """初始化路徑管理器
        
        Args:
            base_dir: 明確指定的專案根目錄，若未指定則自動檢測
        """
        self.base_dir = Path(base_dir) if base_dir else self._detect_base_dir()
        
        # 定義常用目錄
        self.config_dir = self.base_dir / 'config'
        self.data_dir = self.base_dir / 'data'
        self.logs_dir = self.base_dir / 'logs'
        self.src_dir = self.base_dir / 'src'
        
        # 資料處理相關目錄
        self.raw_data_dir = self.data_dir / 'raw'
        self.processed_data_dir = self.data_dir / 'processed'
        
        # 確保關鍵目錄存在
        self._ensure_directories()
        
        # 記錄調試信息
        self._log_path_info()
    
    def _detect_base_dir(self):
        """自動檢測專案根目錄"""
        try:
            # 嘗試從 __file__ 導航 (適用於一般 Python 檔案)
            current_file = Path(__file__).resolve()
            # 從 src/utils/paths.py 向上導航兩級
            return current_file.parent.parent.parent
        except NameError:
            # 處理沒有 __file__ 的環境 (如 Jupyter Notebook)
            return self._find_base_dir_by_markers()
    
    def _find_base_dir_by_markers(self, start_dir=None):
        """通過標記檔案查找專案根目錄"""
        start_dir = Path(start_dir or os.getcwd())
        
        # 專案標記檔案，任一存在即視為專案根目錄
        markers = ['.git', 'pyproject.toml', 'setup.py', 'main.py']
        
        # 向上搜尋，找到包含標記檔案的目錄
        for directory in [start_dir, *start_dir.parents]:
            for marker in markers:
                if (directory / marker).exists():
                    return directory
        
        # 未找到標記，使用當前目錄
        return Path(os.getcwd())
    
    def _ensure_directories(self):
        """確保所有需要的目錄存在"""
        for directory in [
            self.data_dir, self.logs_dir, 
            self.raw_data_dir, self.processed_data_dir
        ]:
            directory.mkdir(exist_ok=True, parents=True)
    
    def _log_path_info(self):
        """記錄路徑信息（用於調試）"""
        print(f"專案根目錄: {self.base_dir}")
        print(f"當前工作目錄: {os.getcwd()}")
    
    # 檔案路徑獲取方法
    def get_config_file(self, filename):
        """獲取設定檔案路徑"""
        return self.config_dir / filename
    
    def get_raw_data_file(self, filename):
        """獲取原始資料檔案路徑"""
        return self.raw_data_dir / filename
    
    def get_processed_data_file(self, filename):
        """獲取處理後資料檔案路徑"""
        return self.processed_data_dir / filename
    
    def get_log_file(self, filename):
        """獲取日誌檔案路徑"""
        return self.logs_dir / filename
    
    # 通用方法
    def get_file_path(self, relative_path):
        """獲取相對於專案根目錄的任意檔案路徑"""
        return self.base_dir / relative_path

# 創建單例實例，可在整個專案中匯入使用
try:
    project_paths = ProjectPaths()
except Exception as e:
    print(f"警告: 路徑初始化失敗: {e}")
    # 提供一個後備方案
    project_paths = None
```

### 使用範例

```python
# src/data_processor.py
from .utils.paths import project_paths

def process_data():
    # 獲取檔案路徑
    input_file = project_paths.get_raw_data_file('input.csv')
    output_file = project_paths.get_processed_data_file('output.csv')
    config_file = project_paths.get_config_file('settings.json')
    
    # 讀取設定
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # 讀取資料
    with open(input_file, 'r') as f:
        data = f.read()
    
    # 處理資料
    processed_data = data.upper() if config.get('to_upper') else data
    
    # 寫入結果
    with open(output_file, 'w') as f:
        f.write(processed_data)
    
    return processed_data
```

## 跨資料夾存取的最佳實踐

1. **使用絕對路徑**: 總是基於專案根目錄構建絕對路徑，避免相對路徑
2. **集中式路徑管理**: 將所有路徑邏輯集中在一個專用模組中
3. **環境檢測**: 代碼應能自動檢測當前執行環境並適應
4. **跨平台兼容**: 使用 `os.path.join()` 或 `pathlib.Path` 而非字串拼接
5. **路徑封裝**: 隱藏路徑細節，使用描述性的方法名稱 (如 `get_config_file`)
6. **目錄結構一致**: 保持目錄結構一致，避免特殊情況

## 下一步學習

現在你已經了解了如何正確處理跨資料夾檔案存取的問題，接下來讓我們了解 [`.py` 與 `.ipynb` 環境差異](./06_py_vs_ipynb.md)，這將幫助你在不同 Python 執行環境下寫出更健壯的代碼。 