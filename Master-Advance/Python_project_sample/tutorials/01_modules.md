# 模組的概念與匯入方法

## 什麼是模組 (Module)？

模組是包含 Python 定義和語句的檔案。檔案名稱就是模組名稱，加上 `.py` 副檔名。模組允許你以邏輯方式組織 Python 程式碼，使其更易於理解和使用。

### 模組的優點

1. **程式碼重用**：可以在多個程式中使用同一模組
2. **程式碼組織**：將相關功能組織在單一檔案中
3. **命名空間管理**：避免全域變數和函數之間的命名衝突

## 模組的匯入方式

Python 提供多種方式匯入模組，每種方式有不同的用途和優缺點。

### 1. 基本匯入

```python
import module_name
```

使用時需要帶模組名稱：

```python
import math
result = math.sqrt(16)  # 結果為 4.0
```

### 2. 從模組匯入特定項目

```python
from module_name import item1, item2
```

使用時直接使用項目名稱：

```python
from math import sqrt, pi
result = sqrt(16)  # 結果為 4.0
circle_area = pi * (2 ** 2)  # 計算半徑為 2 的圓面積
```

### 3. 匯入所有項目 (不建議)

```python
from module_name import *
```

這種方式會匯入模組中所有公開項目，不建議使用，因為：
- 難以追蹤函數/變數的來源
- 可能造成命名衝突
- 使程式碼難以閱讀和維護

### 4. 用別名匯入

```python
import module_name as alias
from module_name import item as alias
```

例如：

```python
import numpy as np
data = np.array([1, 2, 3])

from datetime import datetime as dt
now = dt.now()
```

## 模組搜尋路徑

當你匯入模組時，Python 會按照以下順序在特定位置搜尋模組：

1. 當前執行指令碼所在的目錄
2. 環境變數 PYTHONPATH 所指定的目錄列表
3. Python 安裝時預設的目錄

可以透過 `sys.path` 查看目前的搜尋路徑：

```python
import sys
print(sys.path)
```

## 常見問題與解決方案

### 問題 1：ModuleNotFoundError

當 Python 在搜尋路徑中找不到要匯入的模組時，會出現：
```
ModuleNotFoundError: No module named 'some_module'
```

**解決方法**：
1. 檢查模組名稱是否拼寫正確
2. 確認模組檔案是否在正確的位置
3. 更新 `sys.path` 以包含模組所在目錄

```python
import sys
sys.path.append('/path/to/your/module')
```

### 問題 2：循環匯入 (Circular Import)

當兩個或多個模組相互匯入時，可能導致循環依賴問題。

**解決方法**：
1. 重新組織代碼結構，避免相互依賴
2. 將匯入語句移至函數或方法內部 (延遲匯入)
3. 在模組底部而非頂部匯入

### 問題 3：重複匯入的效能問題

Python 只會載入模組一次，無論匯入多少次。這避免了多次執行模組而導致的效能問題。

## 優良實踐

1. 在文件頂部進行所有匯入
2. 按照標準庫、第三方庫、本機模組的順序組織匯入語句
3. 使用明確的匯入方式而非 `import *`
4. 為長命名模組使用有意義的別名

## 實作練習

創建兩個模組並示範不同的匯入方式：

**math_utils.py**:
```python
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
```

**main.py**:
```python
# 方法 1
import math_utils
result1 = math_utils.add(5, 3)

# 方法 2
from math_utils import multiply
result2 = multiply(5, 3)

print(f"5 + 3 = {result1}")
print(f"5 × 3 = {result2}")
```

## 下一步學習

在掌握基本模組概念後，我們可以進一步學習如何組織多個模組形成一個套件，請繼續閱讀[建立自己的套件](./02_packages.md)。 