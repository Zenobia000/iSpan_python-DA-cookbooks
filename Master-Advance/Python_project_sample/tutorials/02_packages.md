# 建立自己的套件

## 什麼是套件 (Package)？

套件是一種組織 Python 模組的方式，它是一個包含 `__init__.py` 檔案的目錄。套件讓你能夠以階層式結構組織相關模組，提供更好的名稱空間管理和程式碼組織。

```
my_package/
│
├── __init__.py          # 將目錄標記為套件
├── module_a.py          # 套件內的模組
├── module_b.py          # 另一個模組
│
└── subpackage/          # 子套件
    ├── __init__.py      # 將子目錄標記為子套件
    └── sub_module.py    # 子套件中的模組
```

## 套件與模組的區別

| 特性 | 模組 | 套件 |
|------|------|------|
| 形式 | 單一 `.py` 檔案 | 含有 `__init__.py` 的目錄 |
| 結構 | 扁平結構 | 可以有階層結構 |
| 適用場景 | 單一功能或相關功能集 | 大型專案或複雜功能組 |

## 建立套件的步驟

### 1. 創建套件目錄結構

首先，創建套件的目錄結構：

```
my_package/
├── __init__.py
├── module_a.py
└── module_b.py
```

### 2. 創建 `__init__.py` 檔案

`__init__.py` 檔案可以為空，但它的存在告訴 Python 這個目錄應該被視為一個套件。在 Python 3.3+ 版本中，空目錄可以作為「命名空間套件」，但為了兼容性，建議仍然使用 `__init__.py`。

### 3. 在模組中實現功能

在各個模組檔案中實現相應功能。

**module_a.py**:
```python
def func_a():
    return "This is function A from module A"

def another_func_a():
    return "This is another function from module A"
```

**module_b.py**:
```python
def func_b():
    return "This is function B from module B"

def internal_func_b():
    return "This is an internal function from module B"
```

### 4. 在 `__init__.py` 中定義套件介面

`__init__.py` 檔案可以用來定義套件的公開介面，決定哪些模組和函數在套件被匯入時自動可用：

```python
# 從套件內部的模組匯入並暴露特定函數
from .module_a import func_a
from .module_b import func_b

# 定義 __all__ 來控制 from package import * 的行為
__all__ = ['func_a', 'func_b']

# 可以在此定義套件的版本號或其他元資料
__version__ = '0.1.0'
```

## 匯入套件的方式

### 1. 匯入整個套件

```python
import my_package
# 使用套件中通過 __init__.py 暴露的功能
result = my_package.func_a()
```

### 2. 從套件匯入特定模組

```python
from my_package import module_a
# 使用該模組中的所有功能
result = module_a.func_a()
result2 = module_a.another_func_a()
```

### 3. 從套件的模組匯入特定函數

```python
from my_package.module_a import func_a, another_func_a
# 直接使用函數
result = func_a()
```

### 4. 匯入子套件

```python
from my_package.subpackage import sub_module
# 使用子套件中的功能
result = sub_module.sub_func()
```

## 相對匯入與絕對匯入

在套件內部的模組之間，可以使用相對匯入或絕對匯入：

### 絕對匯入 (推薦)

```python
# 在 my_package/module_b.py 中
from my_package.module_a import func_a
```

### 相對匯入

```python
# 在 my_package/module_b.py 中
from .module_a import func_a  # 同一層級的模組
from ..subpackage import sub_func  # 上一層級的子套件
```

- `.` 表示當前套件
- `..` 表示父套件
- `...` 表示父套件的父套件

**注意**：相對匯入只能在套件內部使用，不能在頂層模組中使用。

## 命名空間套件 (Python 3.3+)

從 Python 3.3 開始，套件不一定需要 `__init__.py` 檔案。這種不含 `__init__.py` 的套件稱為「命名空間套件」。它們允許多個目錄貢獻到同一套件中，但功能有所限制。

## 套件發佈與安裝

如果你想要將套件分享給他人，可以將它打包並發佈到 PyPI (Python Package Index)：

1. 創建 `setup.py` 檔案
2. 使用 `setuptools` 設定套件元資料
3. 使用 `pip` 打包並發佈

基本的 `setup.py` 範例：

```python
from setuptools import setup, find_packages

setup(
    name="my_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 列出依賴項
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    keywords="sample, package, tutorial",
    url="https://github.com/yourusername/my_package",
)
```

## 實作練習：建立自己的套件

讓我們實作一個簡單的計算套件：

1. 創建目錄結構：

```
calculator/
├── __init__.py
├── basic.py
└── advanced.py
```

2. 實現模組功能：

**basic.py**:
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

**advanced.py**:
```python
import math

def square_root(x):
    return math.sqrt(x)

def power(base, exponent):
    return base ** exponent
```

3. 在 `__init__.py` 中定義套件介面：

```python
from .basic import add, subtract
from .advanced import square_root, power

__all__ = ['add', 'subtract', 'square_root', 'power']
__version__ = '0.1.0'
```

4. 使用套件：

```python
# 匯入整個套件
import calculator
result = calculator.add(5, 3)

# 從套件匯入特定函數
from calculator import subtract, power
result1 = subtract(10, 4)
result2 = power(2, 3)
```

## 避免常見錯誤

1. **循環依賴**：避免模組間的循環匯入
2. **相對匯入錯誤**：確保相對匯入只在套件內使用
3. **`__init__.py` 過載**：避免在 `__init__.py` 中放太多程式碼
4. **命名空間污染**：謹慎使用 `from X import *`

## 套件設計最佳實踐

1. 遵循明確的層次結構
2. 保持模組功能專一
3. 提供清晰的公開 API
4. 使用 `__all__` 控制匯出
5. 提供完整的文檔

## 下一步學習

現在你已經了解了套件的基本概念，接下來讓我們深入探討 [`__init__.py` 的功能與設計](./03_init_files.md)，了解如何更有效地組織你的套件。 