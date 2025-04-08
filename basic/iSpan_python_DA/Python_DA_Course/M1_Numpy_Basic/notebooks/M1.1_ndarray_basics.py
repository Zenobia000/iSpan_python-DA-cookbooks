## 📘 M1.1 NumPy ndarray 與 Python list 的差異

本教學將介紹 NumPy 的核心數據結構 `ndarray` 與 Python 內建 `list` 的關鍵差異，
並說明為何在數據分析和科學計算中，NumPy 的 `ndarray` 是更好的選擇。

### 🎯 教學目標

- 🔍 了解 NumPy `ndarray` 與 Python `list` 的差異
- 📌 學會選擇適當的資料結構
- 🚀 掌握 `ndarray` 在效能與功能上的優勢

# %%
### 🧰 1. 環境設置與導入必要的套件

# %%
**學習要點**：
- 掌握 NumPy 基本套件導入方式
- 熟悉設定輸出格式的常見選項

**應用場域**：
- 資料前處理時需要控制輸出精度（如財務分析、物理實驗）

# %%
import numpy as np
import time
import sys
np.set_printoptions(precision=3, suppress=True)

# %%
### 🔎 2. 基本比較：ndarray vs list

# %%
**學習要點**：
- 理解兩者在資料結構與語法上的基本差異
- 認識 `type()` 對型別的判定

**應用場域**：
- 教學與原型設計中釐清結構差異
- 作為後續選擇適合資料結構的基礎

# %%
py_list = [1, 2, 3, 4, 5]
np_array = np.array([1, 2, 3, 4, 5])

print(f"Python list: {py_list}, 類型: {type(py_list)}")
print(f"NumPy array: {np_array}, 類型: {type(np_array)}")

# %%
**解說**：
- Python `list` 是通用容器，可儲存各種資料型別
- NumPy `ndarray` 為同質資料陣列，適合數值計算

# %%
### 💾 3. 記憶體佔用比較

# %%
**學習要點**：
- 使用 `sys.getsizeof` 分析記憶體用量
- 掌握 `ndarray` 在大資料處理上的記憶體優勢

**應用場域**：
- 大數據分析、嵌入式系統需嚴格管理記憶體資源的場景

# %%
def get_size(obj):
    return sys.getsizeof(obj)

small_list = list(range(100))
small_array = np.arange(100)
medium_list = list(range(10000))
medium_array = np.arange(10000)
large_list = list(range(1000000))
large_array = np.arange(1000000)

print("小型數據 (100 元素):")
print(f"Python list: {get_size(small_list)} bytes")
print(f"NumPy array: {get_size(small_array)} bytes")

# %%
**解說**：
- Python `list` 每個元素有額外物件封裝開銷
- `ndarray` 使用連續記憶體塊，效率更高

# %%
### ⏱️ 4. 運算速度比較

# %%
**學習要點**：
- 比較 `list comprehension` 與 NumPy 向量化速度差異
- 學習計算執行時間的方式

**應用場域**：
- 機器學習資料預處理、即時分析服務需強調效率的工作流

# %%
n = 1000000
py_list = list(range(n))
np_array = np.arange(n)

start_time = time.time()
result_list = [x * 2 for x in py_list]
list_time = time.time() - start_time

start_time = time.time()
result_array = np_array * 2
array_time = time.time() - start_time

print(f"Python list 運算時間: {list_time:.6f} 秒")
print(f"NumPy 運算時間: {array_time:.6f} 秒")

# %%
**解說**：
- Python `list` 使用迴圈
- NumPy 使用 C 實作的向量化運算，大幅加速

# %%
### 📐 5. 多維數據處理比較

# %%
**學習要點**：
- 建立與操作 2D 陣列的基礎能力
- 理解 `.shape`, `.ndim` 等常見屬性

**應用場域**：
- 影像處理、矩陣演算（如線性代數、CNN）

# %%
list_2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
array_2d = np.array(list_2d)

print(array_2d)
print(array_2d.shape)
print(array_2d.ndim)

# %%
**解說**：
- Python 巢狀 `list` 缺乏統一維度結構
- NumPy 陣列具備明確維度與形狀，有助於數據操作

# %%
### ➕ 6. 數學運算比較

# %%
**學習要點**：
- 熟悉向量化運算與 dot product 的基礎
- 掌握基本數學操作與語法

**應用場域**：
- 財務模型、機器學習特徵轉換、科學計算

# %%
list_a = [1, 2, 3, 4]
list_b = [5, 6, 7, 8]
list_sum = [a + b for a, b in zip(list_a, list_b)]

array_a = np.array(list_a)
array_b = np.array(list_b)
array_sum = array_a + array_b

print(array_sum)
print(array_a * array_b)
print(array_a ** 2)
print(np.dot(array_a, array_b))

# %%
**解說**：
- Python `list` 運算需搭配 zip 與 comprehension
- NumPy 支援向量化與矩陣乘法

# %%
### 🧬 7. 資料類型一致性比較

# %%
**學習要點**：
- 觀察 Python `list` 與 NumPy 陣列的型別管理方式
- 認識 NumPy 的型別自動提升機制（type promotion）

**應用場域**：
- 結構化數據處理、避免資料類型錯誤導致的模型失效

# %%
mixed_list = [1, 'hello', 3.14, True]
mixed_array = np.array(mixed_list)

print(mixed_array)
print(mixed_array.dtype)

num_array = np.array([1, 2.5, 3, 4.8])
print(num_array)
print(num_array.dtype)

# %%
**解說**：
- `list` 可混合類型，彈性高但效率低
- `ndarray` 強制同型別，提升計算一致性與效率

# %%
### 🛠️ 8. 功能方法比較

# %%
**學習要點**：
- 熟悉 NumPy 提供的統計與排序方法
- 理解原地操作與非原地操作的差異

**應用場域**：
- 資料探索性分析（EDA）、特徵工程前的摘要統計

# %%
py_list = [3, 1, 4, 1, 5, 9, 2, 6]
np_array = np.array(py_list)

print(len(np_array))
print(np_array.max())
print(np_array.sum())
print(np.median(np_array))
print(np.sort(np_array))

# %%
**解說**：
- NumPy 提供大量內建方法，支援統計、排序、矩陣操作
- 相較之下，Python `list` 需要外部函數或手動處理

# %%
### 🧾 9. 總結：NumPy ndarray vs Python list

# %%
**學習要點**：
- 總結適用場景與設計選擇的依據
- 養成根據任務目標選用適當資料結構的能力

**應用場域**：
- 建立處理流程時的資料架構選型
- 作為跨模組團隊共用資料時的規格依據

#### ✅ NumPy `ndarray` 優點：
- 高效能與記憶體使用
- 支援向量化、矩陣操作、科學函數
- 適合大型資料與多維運算

#### ☑️ 適用場景：
- 機器學習、資料分析、數值模擬
- 科學計算、工程模擬

#### 🔁 使用 `list` 的情境：
- 當資料型別不一致
- 須動態增減元素
- 小型、非數值導向的資料處理
