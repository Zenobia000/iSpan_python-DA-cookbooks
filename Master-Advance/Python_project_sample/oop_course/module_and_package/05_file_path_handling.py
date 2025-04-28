# %% [markdown]
# # 檔案路徑處理
# 
# 本節將介紹 Python 中的檔案路徑處理方法，解決跨平台與環境問題，以及在不同運行環境中找到正確的資源文件。

# %% [markdown]
# ## 1. 路徑處理的挑戰
# 
# 檔案路徑處理是 Python 開發中常見的挑戰，特別是當代碼需要在不同環境中運行時。

# %%
print("檔案路徑處理的主要挑戰:")
challenges = [
    "不同操作系統的路徑分隔符不同 (Windows: '\\', Unix/Mac: '/')",
    "絕對路徑在不同機器上不同",
    "腳本執行位置與工作目錄可能不同",
    "項目結構在開發環境與部署環境可能不同",
    "Python 模組導入與文件讀取使用不同的路徑機制",
    "Jupyter Notebook 與 .py 檔案的路徑處理邏輯不同"
]

for i, challenge in enumerate(challenges, 1):
    print(f"{i}. {challenge}")

# %% [markdown]
# ## 2. 基本路徑操作與 `os.path` 模組

# %%
import os
import sys

# 展示路徑基本信息
print(f"當前工作目錄: {os.getcwd()}")
print(f"本腳本的路徑: {__file__ if '__file__' in globals() else '在互動環境中無法獲取'}")
print(f"Python 模組搜索路徑: {sys.path[0]}")

# %%
# os.path 模組的常用函數
os_path_functions = [
    ("os.path.join", "連接路徑片段，處理分隔符", "os.path.join('folder', 'file.txt')"),
    ("os.path.abspath", "獲取絕對路徑", "os.path.abspath('file.txt')"),
    ("os.path.dirname", "獲取路徑的目錄部分", "os.path.dirname('/path/to/file.txt')"),
    ("os.path.basename", "獲取路徑的文件名部分", "os.path.basename('/path/to/file.txt')"),
    ("os.path.exists", "檢查路徑是否存在", "os.path.exists('file.txt')"),
    ("os.path.isfile", "檢查路徑是否為文件", "os.path.isfile('file.txt')"),
    ("os.path.isdir", "檢查路徑是否為目錄", "os.path.isdir('folder')"),
    ("os.path.splitext", "分離文件名和副檔名", "os.path.splitext('file.txt')")
]

print("\nos.path 模組常用函數:")
for func, desc, example in os_path_functions:
    print(f"{func}: {desc}")
    print(f"  例如: {example}")
    
    # 對部分函數執行實際示例
    if func == "os.path.join":
        print(f"  結果: {os.path.join('folder', 'file.txt')}")
    elif func == "os.path.splitext":
        print(f"  結果: {os.path.splitext('file.txt')}")
    print()

# %% [markdown]
# ## 3. 使用 `pathlib` 模組（現代化方法）
#
# `pathlib` 是 Python 3.4+ 引入的模組，提供了面向對象的路徑操作方式。

# %%
from pathlib import Path

print("pathlib.Path 類的優勢:")
advantages = [
    "面向對象的接口，更直觀",
    "鏈式操作，代碼更簡潔",
    "自動處理不同操作系統的差異",
    "內置更多功能，減少對其他模組的依賴"
]
for adv in advantages:
    print(f"- {adv}")

# %%
# pathlib.Path 類常用方法示例
path_methods = [
    ("創建路徑對象", "path = Path('folder/file.txt')", Path('folder/file.txt')),
    ("路徑連接", "path = Path('folder') / 'file.txt'", Path('folder') / 'file.txt'),
    ("獲取當前目錄", "path = Path.cwd()", Path.cwd()),
    ("獲取主目錄", "path = Path.home()", Path.home()),
    ("獲取絕對路徑", "path.absolute()", Path('example.txt').absolute()),
    ("檢查是否存在", "path.exists()", "布林值結果"),
    ("檢查是否為文件", "path.is_file()", "布林值結果"),
    ("檢查是否為目錄", "path.is_dir()", "布林值結果"),
    ("獲取父目錄", "path.parent", Path('folder/file.txt').parent),
    ("獲取文件名", "path.name", Path('folder/file.txt').name),
    ("獲取副檔名", "path.suffix", Path('folder/file.txt').suffix),
    ("獲取無副檔名的文件名", "path.stem", Path('folder/file.txt').stem),
    ("獲取所有部分", "path.parts", Path('folder/subfolder/file.txt').parts),
    ("列出目錄內容", "path.iterdir()", "返回迭代器"),
    ("查找文件 (glob)", "path.glob('*.txt')", "返回迭代器"),
    ("遞歸查找文件", "path.rglob('*.txt')", "返回迭代器")
]

print("\npathlib.Path 類常用方法:")
for desc, code, result in path_methods:
    if isinstance(result, Path):
        print(f"{desc}: {code} -> {result}")
    else:
        print(f"{desc}: {code} -> {result}")

# %% [markdown]
# ## 4. 不同執行環境的路徑處理

# %%
# 這些是常見的獲取腳本所在目錄的方法
script_dir_methods = [
    "# 方法 1: 使用 __file__ 變數 (在腳本中有效)",
    "import os",
    "script_dir = os.path.dirname(os.path.abspath(__file__))",
    "\n",
    "# 方法 2: 使用 pathlib (Python 3.4+)",
    "from pathlib import Path",
    "script_dir = Path(__file__).parent.absolute()",
    "\n",
    "# 方法 3: 針對 Jupyter Notebook 環境",
    "import os",
    "try:",
    "    notebook_path = os.path.abspath('')  # 當前工作目錄",
    "    # 或者使用:",
    "    # notebook_path = os.getcwd()",
    "except:",
    "    notebook_path = os.getcwd()",
    "\n",
    "# 方法 4: 兼容腳本和 Notebook 的通用方法",
    "def get_script_dir():",
    "    if '__file__' in globals():",
    "        # 運行在普通 Python 腳本中",
    "        return os.path.dirname(os.path.abspath(__file__))",
    "    else:",
    "        # 運行在 Jupyter Notebook 中",
    "        return os.getcwd()"
]

print("獲取腳本所在目錄的方法:")
for line in script_dir_methods:
    print(line)

# %% [markdown]
# ## 5. 跨目錄資源存取

# %%
# 專案結構示例
project_structure = """
my_project/
├── main.py
├── data/
│   ├── input.csv
│   └── config.json
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── outputs/
    └── results.txt
"""

print("專案結構示例:")
print(project_structure)

# 展示不同情境下的資源存取
resource_access_examples = [
    "# 範例 1: 從主腳本存取資料文件",
    "# 在 main.py 中:",
    "import os",
    "from pathlib import Path",
    "",
    "# 方法 1: 使用相對路徑 (依賴於執行位置)",
    "data_file = 'data/input.csv'  # 僅在從專案根目錄執行時有效",
    "",
    "# 方法 2: 使用腳本位置構建絕對路徑",
    "script_dir = Path(__file__).parent",
    "data_file = script_dir / 'data' / 'input.csv'",
    "",
    "# 方法 3: 使用專案根目錄作為基準",
    "project_root = Path(__file__).parent",
    "data_file = project_root / 'data' / 'input.csv'",
    "\n",
    "# 範例 2: 從模組存取資源",
    "# 在 utils/helpers.py 中:",
    "import os",
    "from pathlib import Path",
    "",
    "# 方法 1: 向上導航到專案根目錄",
    "module_dir = Path(__file__).parent",
    "project_root = module_dir.parent",
    "data_file = project_root / 'data' / 'input.csv'",
    "",
    "# 方法 2: 使用相對導入和 __file__",
    "module_dir = os.path.dirname(os.path.abspath(__file__))",
    "project_root = os.path.dirname(module_dir)",
    "data_file = os.path.join(project_root, 'data', 'input.csv')"
]

print("\n不同情境下的資源存取:")
for line in resource_access_examples:
    print(line)

# %% [markdown]
# ## 6. 路徑助手類設計模式

# %%
# 路徑助手類設計模式
path_helper_code = """
# path_helper.py
from pathlib import Path
import os
import sys

class ProjectPaths:
    def __init__(self):
        # 確定專案根目錄
        self._find_project_root()
        
        # 定義常用目錄
        self.data_dir = self.project_root / 'data'
        self.config_dir = self.project_root / 'config'
        self.output_dir = self.project_root / 'output'
        
        # 確保目錄存在
        self.data_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def _find_project_root(self):
        # 策略 1: 使用 __file__ (適用於腳本)
        if '__file__' in globals():
            file_path = Path(__file__).resolve()
            # 尋找特定標誌文件 (如 .git, pyproject.toml 等)
            for parent in [file_path, *file_path.parents]:
                if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
                    self.project_root = parent
                    return
                
            # 如果找不到標誌文件，使用當前文件的父目錄
            self.project_root = file_path.parent
            return
            
        # 策略 2: 使用 getcwd() (適用於 Jupyter)
        current_dir = Path(os.getcwd()).resolve()
        for parent in [current_dir, *current_dir.parents]:
            if (parent / '.git').exists() or (parent / 'pyproject.toml').exists():
                self.project_root = parent
                return
                
        # 策略 3: 回退到當前目錄
        self.project_root = current_dir
    
    def get_data_file(self, filename):
        \"\"\"獲取數據目錄中的文件路徑\"\"\"
        return self.data_dir / filename
    
    def get_config_file(self, filename):
        \"\"\"獲取配置目錄中的文件路徑\"\"\"
        return self.config_dir / filename
    
    def get_output_file(self, filename):
        \"\"\"獲取輸出目錄中的文件路徑\"\"\"
        return self.output_dir / filename
    
    def add_to_python_path(self):
        \"\"\"將專案根目錄添加到 Python 路徑\"\"\"
        if str(self.project_root) not in sys.path:
            sys.path.insert(0, str(self.project_root))
    
    def debug_info(self):
        \"\"\"輸出路徑相關的調試信息\"\"\"
        print(f"Project Root: {self.project_root}")
        print(f"Data Directory: {self.data_dir}")
        print(f"Config Directory: {self.config_dir}")
        print(f"Output Directory: {self.output_dir}")
        print(f"Python Path: {sys.path[0]}")

# 單例實例
project_paths = ProjectPaths()
"""

print("路徑助手類設計模式範例:")
print(path_helper_code)

# %%
# 使用路徑助手類的示例
usage_example = """
# 在任何模組中使用路徑助手:
from path_helper import project_paths

# 獲取數據文件路徑
data_file = project_paths.get_data_file('input.csv')

# 讀取文件
with open(data_file, 'r') as f:
    data = f.read()

# 獲取輸出文件路徑
output_file = project_paths.get_output_file('results.csv')

# 寫入文件
with open(output_file, 'w') as f:
    f.write(processed_data)

# 調試路徑問題
project_paths.debug_info()
"""

print("\n使用路徑助手類的示例:")
print(usage_example)

# %% [markdown]
# ## 7. 處理特殊情況

# %%
special_cases = [
    "# 情況 1: 在打包後的應用中存取資源",
    "import pkg_resources",
    "data_path = pkg_resources.resource_filename('my_package', 'data/config.json')",
    "",
    "# 情況 2: 在臨時目錄中工作",
    "import tempfile",
    "with tempfile.TemporaryDirectory() as temp_dir:",
    "    temp_file = Path(temp_dir) / 'temp_data.txt'",
    "    with open(temp_file, 'w') as f:",
    "        f.write('臨時數據')",
    "",
    "# 情況 3: 使用跨平台的用戶目錄",
    "from pathlib import Path",
    "user_config_dir = Path.home() / '.my_app'",
    "user_config_dir.mkdir(exist_ok=True)",
    "user_config_file = user_config_dir / 'settings.json'"
]

print("處理特殊情況:")
for line in special_cases:
    print(line)

# %% [markdown]
# ## 8. 常見陷阱與解決方案

# %%
pitfalls = [
    ("硬編碼的絕對路徑", "避免使用 'C:/Users/...' 或 '/home/user/...' 等絕對路徑", "使用相對路徑或基於 __file__ 構建的路徑"),
    ("錯誤的路徑連接", "避免手動連接路徑，如 'path1' + '/' + 'path2'", "使用 os.path.join() 或 pathlib 的 / 運算符"),
    ("忽略跨平台問題", "不同考慮 Windows 和 Unix 路徑的差異", "使用 os.path 或 pathlib 處理路徑"),
    ("依賴當前工作目錄", "腳本運行時的工作目錄可能不是預期的", "始終使用基於 __file__ 的絕對路徑"),
    ("混用斜槓樣式", "在同一段代碼中混用 / 和 \\", "統一使用 os.path.join() 或 pathlib"),
    ("假設文件存在", "未檢查文件是否存在就嘗試存取", "使用 os.path.exists() 或 Path.exists() 先檢查"),
    ("忽略權限問題", "未考慮讀寫權限可能導致錯誤", "使用 try-except 處理權限相關的例外")
]

print("常見陷阱與解決方案:")
for pitfall, problem, solution in pitfalls:
    print(f"陷阱: {pitfall}")
    print(f"問題: {problem}")
    print(f"解決方案: {solution}")
    print()

# %% [markdown]
# ## 9. 實作練習
# 
# 1. 創建一個 `PathManager` 類，能夠處理以下任務:
#    - 找到專案根目錄
#    - 管理專案內不同類型資源的路徑
#    - 處理相對路徑和絕對路徑轉換
# 
# 2. 編寫測試腳本，驗證 `PathManager` 在以下情況下的運作:
#    - 從專案根目錄運行
#    - 從子目錄運行
#    - 從專案外部目錄運行
# 
# 3. 擴展 `PathManager` 以支援 Jupyter Notebook 環境 