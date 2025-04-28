# %% [markdown]
# # 套件結構
# 
# 本節將介紹Python套件的概念、結構和使用方法，幫助您組織更複雜的代碼庫。

# %% [markdown]
# ## 1. 什麼是套件？
# 
# 套件是包含多個模組的目錄，能夠提供更高級別的組織結構。套件必須包含一個特殊的 `__init__.py` 文件（在Python 3.3+中可選但建議保留）。

# %%
print("套件與模組的區別:")
package_vs_module = [
    "模組: 單一的 .py 文件",
    "套件: 包含多個模組的目錄 (必須包含 __init__.py)"
]

for item in package_vs_module:
    print(f"- {item}")

# %% [markdown]
# ## 2. 套件結構示例

# %%
# 展示典型的套件結構
package_structure = """
my_package/                 # 頂層套件
    __init__.py             # 初始化頂層套件
    
    module_a.py             # 子模組 A
    module_b.py             # 子模組 B
    
    subpackage_1/           # 子套件 1
        __init__.py         # 初始化子套件 1
        module_c.py
        module_d.py
        
    subpackage_2/           # 子套件 2
        __init__.py         # 初始化子套件 2
        module_e.py
        module_f.py
"""

print("典型的套件目錄結構:")
print(package_structure)

# %% [markdown]
# ## 3. `__init__.py` 文件的作用

# %%
# 展示 __init__.py 文件的不同用途
init_examples = [
    "# 1. 最簡單的 __init__.py - 空文件",
    "# 僅標記目錄作為Python套件",
    "\n",
    "# 2. 導入特定模組或函數，以便在導入套件時可用",
    "# 文件: my_package/__init__.py",
    "from .module_a import function1, function2",
    "from .module_b import ClassX, ClassY",
    "\n",
    "# 3. 控制 * 運算符導入的內容",
    "# 文件: my_package/__init__.py",
    "__all__ = ['function1', 'function2', 'ClassX', 'ClassY']",
    "\n",
    "# 4. 定義套件版本信息",
    "# 文件: my_package/__init__.py",
    "__version__ = '0.1.0'",
    "__author__ = 'Your Name'",
    "\n",
    "# 5. 執行套件初始化代碼",
    "# 文件: my_package/__init__.py",
    "print('Initializing my_package...')",
    "# 配置日誌、設置預設值等"
]

print("__init__.py 文件的不同用途:")
for line in init_examples:
    print(line)

# %% [markdown]
# ## 4. 導入套件和模組

# %%
# 展示不同的套件導入方式
import_examples = [
    "# 導入整個套件",
    "import my_package",
    "\n",
    "# 導入套件中的特定模組",
    "import my_package.module_a",
    "import my_package.subpackage_1.module_c",
    "\n",
    "# 導入模組中的特定項目",
    "from my_package.module_a import function1, function2",
    "from my_package.subpackage_1.module_c import ClassZ",
    "\n",
    "# 使用別名",
    "import my_package as mp",
    "from my_package.module_a import function1 as f1",
    "\n",
    "# 導入套件中的所有可用項目 (如果在 __init__.py 中定義了 __all__)",
    "from my_package import *"
]

print("套件導入方式:")
for example in import_examples:
    print(example)

# %% [markdown]
# ## 5. 相對導入與絕對導入

# %%
import_types = [
    "# 絕對導入 (從項目根目錄開始)",
    "from my_package.subpackage_1 import module_c",
    "from my_package.module_a import function1",
    "\n",
    "# 相對導入 (從當前模組位置開始)",
    "# 在 my_package/subpackage_1/module_c.py 中:",
    "from . import module_d        # 導入同級目錄的模組",
    "from .. import module_a       # 導入上一級目錄的模組",
    "from ..module_b import ClassY # 導入上一級目錄特定模組中的類",
    "from ..subpackage_2 import module_e  # 導入平行子套件中的模組"
]

print("絕對導入與相對導入:")
for line in import_types:
    print(line)

print("\n注意事項:")
print("- 相對導入只能在套件內部使用，不能在頂層模組中使用")
print("- 相對導入可能在不同執行方式下表現不同 (作為腳本運行 vs 作為模組導入)")

# %% [markdown]
# ## 6. 命名空間套件 (Python 3.3+)
#
# 命名空間套件是橫跨多個目錄的套件，不需要 `__init__.py` 文件。

# %%
namespace_example = """
# 目錄結構:
path1/
    my_namespace/
        module_a.py
        
path2/
    my_namespace/
        module_b.py

# 將兩個路徑都添加到 Python 路徑中後:
import sys
sys.path.extend(['path1', 'path2'])

# 可以這樣導入:
import my_namespace.module_a
import my_namespace.module_b

# Python會自動將同名目錄組合成一個命名空間套件
"""

print("命名空間套件示例:")
print(namespace_example)

# %% [markdown]
# ## 7. 發布自己的套件

# %%
# 建立可發布套件的最基本結構
setup_example = """
my_package/
    my_package/
        __init__.py
        module_a.py
        module_b.py
    setup.py
    README.md
    LICENSE
    
# setup.py 示例:
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.18.0",
        "pandas>=1.0.0",
    ],
)
"""

print("套件發布結構示例:")
print(setup_example)

print("\n發布指令:")
print("python setup.py sdist bdist_wheel  # 建立發布檔")
print("pip install twine  # 安裝發布工具")
print("twine upload dist/*  # 上傳到 PyPI")

# %% [markdown]
# ## 8. 套件設計最佳實踐

# %%
best_practices = [
    "遵循標準目錄結構 - 使用常見的組織方式",
    "避免過深的嵌套 - 保持套件結構相對扁平",
    "謹慎使用 __init__.py - 避免複雜的初始化邏輯",
    "使用明確的導入方式 - 優先使用顯式導入而非 *",
    "遵循明確的版本控制 - 使用語義化版本號",
    "包含完善的文檔 - 添加清晰的使用說明",
    "提供測試用例 - 確保套件功能正常",
    "關注向下兼容性 - 避免輕易破壞用戶代碼"
]

print("套件設計最佳實踐:")
for i, practice in enumerate(best_practices, 1):
    print(f"{i}. {practice}")

# %% [markdown]
# ## 9. 實作練習
# 
# 1. 創建一個名為 `data_analysis` 的套件，包含以下子模組:
#    - `readers.py` - 用於讀取不同格式的資料
#    - `processors.py` - 用於處理和轉換資料
#    - `visualizers.py` - 用於視覺化資料
# 
# 2. 設計合適的 `__init__.py` 文件，讓使用者能夠方便地存取主要功能
# 
# 3. 創建一個使用該套件的範例腳本 