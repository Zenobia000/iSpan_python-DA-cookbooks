# %% 
# # M1.2 NumPy 陣列的建立方式
# 
# 本教學將詳細介紹各種建立 NumPy 陣列的方法，包括從 Python 序列建立、使用內建函數生成，以及從外部資料匯入。

# %% 
### 🎯 教學目標

**學習要點**：
- 掌握不同的 NumPy 陣列建立方法
- 了解何時該使用哪種建立方式
- 學會如何指定數據類型和陣列形狀

# %%
### 🔧 1. 環境設置與導入必要的套件

# %%
**學習要點**：
- 匯入 NumPy 套件
- 調整 NumPy 的輸出格式以利顯示浮點數

**應用場域**：
- 前置設置，用於資料分析或數值模擬的開發環境

# %%
import numpy as np
np.set_printoptions(precision=3, suppress=True)

# %%
**解說**：
- `np.set_printoptions` 可控制浮點數顯示精度與科學記號的顯示方式，提升閱讀性。
- 在教學或除錯情境中，統一輸出格式有助於結果驗證。


# %%
### 🧱 2. 從 Python 序列建立陣列

# %%
**學習要點**：
- 使用 `list` 或 `tuple` 建立 NumPy 陣列
- 使用 `.shape`, `.ndim` 獲取形狀與維度資訊

**應用場域**：
- 資料輸入的轉換與預處理
- 建立初學者的陣列基本概念

# %%
list_1d = [1, 2, 3, 4, 5]
array_1d = np.array(list_1d)
print(f"從 list 建立的 1D 陣列: \n{array_1d}")
print(f"形狀: {array_1d.shape}, 維度: {array_1d.ndim}")

list_2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
array_2d = np.array(list_2d)
print(f"\n從巢狀 list 建立的 2D 陣列: \n{array_2d}")
print(f"形狀: {array_2d.shape}, 維度: {array_2d.ndim}")

tuple_data = (10, 20, 30, 40)
array_from_tuple = np.array(tuple_data)
print(f"\n從 tuple 建立的陣列: \n{array_from_tuple}")

# %%
**解說**：
- `np.array()` 能自動偵測巢狀結構的維度，並轉為對應形狀的陣列。
- `.shape` 回傳維度大小，`.ndim` 回傳維度數（例如 1D、2D）。
- 使用 tuple 與 list 效果相同，關鍵在於是否有巢狀結構。


# %%
### 🔤 3. 指定數據類型 (dtype)

# %%
**學習要點**：
- 明確指定陣列的資料型別
- 掌握 `astype`, `dtype` 的差異與應用

**應用場域**：
- 節省記憶體（如 IoT）、避免類型錯誤（如轉 float → int）
- 精確控制模型輸入輸出格式

# %%
int_array = np.array([1, 2, 3, 4])
float_array = np.array([1.0, 2.0, 3.0, 4.0])
print(f"整數陣列的類型: {int_array.dtype}")
print(f"浮點數陣列的類型: {float_array.dtype}")

float32_array = np.array([1, 2, 3, 4], dtype=np.float32)
int64_array = np.array([1.5, 2.7, 3.9, 4.1], dtype=np.int64)
print(f"\n強制為 float32 的陣列: {float32_array}, 類型: {float32_array.dtype}")
print(f"強制為 int64 的陣列: {int64_array}, 類型: {int64_array.dtype}")

bool_array = np.array([True, False, True], dtype=bool)
complex_array = np.array([1, 2, 3], dtype=complex)
print(f"\n布林陣列: {bool_array}, 類型: {bool_array.dtype}")
print(f"複數陣列: {complex_array}, 類型: {complex_array.dtype}")

# %%
**解說**：
- 指定 `dtype` 可避免自動轉型帶來的精度問題（如 int → float）。
- 對浮點數、布林值、複數等都有內建類型支援。
- 浮點轉整數會截斷小數部分；可用於離散化特徵。


# %%
### 📦 4. 使用內建函數建立特殊陣列

# %%
**學習要點**：
- 熟悉 `zeros`, `ones`, `full`, `empty` 等初始化函數
- 認識 shape 與填充值設定方式

**應用場域**：
- 用於初始化模型、占位、測試矩陣運算

# %%
zeros_1d = np.zeros(5)
zeros_2d = np.zeros((3, 4))
print(f"1D 全零陣列: \n{zeros_1d}")
print(f"2D 全零陣列: \n{zeros_2d}")

ones_1d = np.ones(4)
ones_2d = np.ones((2, 3))
print(f"\n1D 全一陣列: \n{ones_1d}")
print(f"2D 全一陣列: \n{ones_2d}")

full_array = np.full((2, 3), 7)
print(f"\n全 7 的 2x3 陣列: \n{full_array}")

empty_array = np.empty((2, 2))
print(f"\n空陣列 (未初始化): \n{empty_array}")

# %%
**解說**：
- `empty` 建立未初始化陣列，速度最快但內容不保證。
- `full` 可建立固定初始值矩陣，適合建立預設輸入模板。


# %%
### 4.2 等差序列 (arange, linspace)

# %%
**學習要點**：
- 使用 `arange`, `linspace` 建立規則遞增陣列
- 理解等距與等點數的差異

**應用場域**：
- 建立時間序列、模擬輸入、繪圖坐標

# %%
arange_1 = np.arange(5)
arange_2 = np.arange(1, 10, 2)
print(f"arange(5): \n{arange_1}")
print(f"arange(1, 10, 2): \n{arange_2}")

linspace_1 = np.linspace(0, 1, 5)
linspace_2 = np.linspace(0, 10, 11)
print(f"\nlinspace(0, 1, 5): \n{linspace_1}")
print(f"linspace(0, 10, 11): \n{linspace_2}")

# %%
**解說**：
- `arange` 基於步長，右界不包含；`linspace` 基於點數，包含兩端點。
- 建立浮點序列時 `linspace` 精度更穩定。


# %%
### 4.3 對數與幾何等比序列

# %%
**學習要點**：
- 使用 `logspace`, `geomspace` 建立對數與幾何遞增序列

**應用場域**：
- 用於學習率、頻率、倍率的數值模擬

# %%
logspace = np.logspace(0, 3, 4)
print(f"logspace(0, 3, 4): \n{logspace}")

geomspace = np.geomspace(1, 1000, 4)
print(f"\ngeomspace(1, 1000, 4): \n{geomspace}")

# %%
**解說**：
- `logspace(0, 3, 4)` 表示 `10^0 ~ 10^3` 間的 4 個點。
- `geomspace` 可處理非 10 為底的等比級數。


# %%
### 4.4 單位矩陣與對角矩陣

# %%
**學習要點**：
- 使用 `eye`, `diag` 建立單位矩陣與對角矩陣
- 學會提取對角線元素

**應用場域**：
- 線性代數、機器學習模型的初始化或判別

# %%
identity_matrix = np.eye(3)
print(f"3x3 單位矩陣: \n{identity_matrix}")

diag_array = np.diag([1, 2, 3, 4])
print(f"\n對角矩陣: \n{diag_array}")

matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
diag_elements = np.diag(matrix)
print(f"\n原始矩陣: \n{matrix}")
print(f"對角線元素: {diag_elements}")

# %%
**解說**：
- `eye(n)` 產生 n 維單位矩陣；`diag` 可建立與抽取對角線。
- 對角矩陣常用於正規化、變異矩陣、轉換基底等用途。


# %%
### 🎲 5. 隨機數陣列

# %%
**學習要點**：
- 使用 `random` 子模組產生各種分布的隨機數
- 包含均勻分布、常態分布、整數、隨機抽樣與打亂

**應用場域**：
- 模擬資料生成、機器學習隨機初始化、抽樣演算法

# %%
np.random.seed(42)

rand_uniform = np.random.rand(3, 3)
print(f"均勻分布隨機數 [0,1): \n{rand_uniform}")

rand_normal = np.random.randn(3, 3)
print(f"\n標準常態分布隨機數: \n{rand_normal}")

rand_integers = np.random.randint(1, 100, size=(2, 4))
print(f"\n1 到 99 之間的隨機整數: \n{rand_integers}")

rand_choice = np.random.choice([1, 2, 3, 4, 5], size=10)
print(f"\n從序列中隨機選取: \n{rand_choice}")

arr = np.arange(10)
np.random.shuffle(arr)
print(f"\n打亂後的陣列: \n{arr}")

# %%
**解說**：
- `rand`, `randn`, `randint` 分別對應均勻、常態與離散整數抽樣。
- `shuffle` 是 in-place 操作，會改變原陣列。

# %%
### 🪞 6. 建立與現有陣列形狀一致的新陣列

# %%
**學習要點**：
- 使用 `*_like` 系列函數快速建立形狀相同的陣列
- 指定預設值如全零、全一、固定值或空值

**應用場域**：
- 模型占位陣列建立、資料結構複製初始化

# %%
original = np.array([[1, 2, 3], [4, 5, 6]])

zeros_like = np.zeros_like(original)
print(f"zeros_like: \n{zeros_like}")

ones_like = np.ones_like(original)
print(f"\nones_like: \n{ones_like}")

full_like = np.full_like(original, 9)
print(f"\nfull_like (值為 9): \n{full_like}")

empty_like = np.empty_like(original)
print(f"\nempty_like: \n{empty_like}")

# %%
**解說**：
- `*_like` 函數可節省手動輸入形狀的麻煩。
- `empty_like` 僅建立容器，內容為記憶體中原始值，不可預期。


# %%
### 🔄 7. 陣列重塑與多維建立

# %%
**學習要點**：
- 使用 `reshape` 將一維資料轉換為多維結構
- 使用 `-1` 自動推斷維度

**應用場域**：
- 資料前處理、神經網路輸入格式調整

# %%
flat_array = np.arange(12)
reshaped_2d = flat_array.reshape(3, 4)
reshaped_3d = flat_array.reshape(2, 2, 3)

print(f"原始 1D 陣列: \n{flat_array}")
print(f"\n重塑為 3x4 陣列: \n{reshaped_2d}")
print(f"\n重塑為 2x2x3 陣列: \n{reshaped_3d}")

auto_reshape = flat_array.reshape(3, -1)
print(f"\n自動計算列數 (3, -1): \n{auto_reshape}")

# %%
**解說**：
- `reshape` 通常不會複製資料，只調整 shape metadata。
- 使用 `-1` 可由 NumPy 自動推算剩餘維度，非常方便。


# %%
### 🗂️ 8. 從外部資料建立陣列

# %%
**學習要點**：
- 使用 `np.loadtxt` 讀取文字檔
- 使用 `np.asarray` 轉換巢狀列表為陣列

**應用場域**：
- 檔案資料讀取與前處理
- 將外部來源（CSV、log）轉為分析格式

# %%
import tempfile
import os

temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
temp_file.write(b"1.0 2.0 3.0\n4.0 5.0 6.0\n7.0 8.0 9.0")
temp_file.close()

array_from_txt = np.loadtxt(temp_file.name)
print(f"從文本文件載入的陣列: \n{array_from_txt}")

os.unlink(temp_file.name)

data = [[1, 2, 3], [4, 5, 6]]
array_from_data = np.asarray(data)
print(f"\n從列表列表載入: \n{array_from_data}")

# %%
**解說**：
- `loadtxt` 適合讀取簡單、空白分隔的純數值資料。
- `asarray` 可避免不必要的複製（與 `array` 最大差異）。


# %%
### 🧩 9. 向量與張量

# %%
**學習要點**：
- 了解 NumPy 如何表示行向量、列向量與高維張量
- 掌握 `.reshape()` 的實務應用

**應用場域**：
- 機器學習中的資料格式轉換
- 圖像處理中的多維結構（如 RGB）

# %%
row_vector = np.array([1, 2, 3, 4])
print(f"行向量形狀: {row_vector.shape}")

column_vector = row_vector.reshape(-1, 1)
print(f"\n列向量: \n{column_vector}")
print(f"列向量形狀: {column_vector.shape}")

tensor_3d = np.ones((2, 3, 4))
print(f"\n3D 張量形狀: {tensor_3d.shape}")
print(f"第一個 3x4 矩陣: \n{tensor_3d[0]}")

# %%
**解說**：
- NumPy 的一維陣列不是矩陣；需用 `.reshape` 顯式轉為 (n,1) 或 (1,n)。
- 3D 張量常見於影像、語音與影片等多維資料。


# %%
### ✅ 10. 總結與最佳實踐建議

# %%
**學習要點**：
- 回顧各種建立陣列的方式與函數
- 理解何時該使用哪一種建立法

**應用場域**：
- 實作中快速選擇最合適、最高效的陣列建立策略

# %%
# 建立方式總覽
print("常見建立方式：")
print("1. np.array([1, 2, 3])")
print("2. np.zeros((3, 3))")
print("3. np.ones((2, 4))")
print("4. np.full((2, 2), 7)")
print("5. np.arange(10), np.linspace(0, 1, 5)")
print("6. np.eye(3)")
print("7. np.random.rand(3, 3)")

# %%
**解說**：
- `array` 適合已知數據；`zeros`, `ones`, `full` 適合初始化。
- `arange` 適合整數序列，`linspace` 適合浮點數精準區間。
- `empty` 效率最佳但不可預期；`asarray` 可避免複製。
