# %% 
# M1 NumPy 基礎練習

本練習旨在幫助你鞏固 NumPy 基礎知識，包含了陣列建立、索引切片、廣播機制、數學函數與小型統計分析等內容。
請完成以下練習題，加深對 NumPy 的理解與應用能力。

# %%
## 環境設置

import numpy as np
import matplotlib.pyplot as plt

# 設定顯示選項，使輸出更易讀
np.set_printoptions(precision=3, suppress=True)

# %% [markdown]
# ## 練習 1: NumPy ndarray 與 Python list 的差異
# 
# 請完成以下練習，比較 NumPy 陣列和 Python 列表的差異。

# %%
# 1.1 建立一個包含數字 1 到 5 的 Python 列表和 NumPy 陣列
# 提示: 使用 np.array() 函數將列表轉換為陣列
python_list = 
numpy_array = 

print(f"Python list: {python_list}, 型別: {type(python_list)}")
print(f"NumPy array: {numpy_array}, 型別: {type(numpy_array)}")

# %%
# 1.2 比較兩者的運算效率: 計算每個元素的平方
# 提示: 使用列表推導式和 NumPy 的向量化操作

# 使用列表推導式計算平方
# 完成以下代碼
squared_list = 

# 使用 NumPy 向量化操作計算平方
# 完成以下代碼
squared_array = 

print(f"Squared list: {squared_list}")
print(f"Squared array: {squared_array}")

# %%
# 1.3 實現一個簡單的效能測試，比較兩者在大陣列下的計算速度
# 提示: 使用 time 模組測量運行時間

import time

# 建立大型列表和陣列 (100萬個元素)
large_list = list(range(1000000))
large_array = np.arange(1000000)

# 測量列表計算時間
start_time = time.time()
list_result = [x * 2 for x in large_list]
list_time = time.time() - start_time

# 測量 NumPy 計算時間
start_time = time.time()
array_result = large_array * 2
array_time = time.time() - start_time

print(f"Python list 運算時間: {list_time:.6f} 秒")
print(f"NumPy array 運算時間: {array_time:.6f} 秒")
print(f"NumPy 加速比: {list_time/array_time:.2f}x")

# %% [markdown]
# ## 練習 2: 陣列的建立方式
# 
# 請使用不同方法建立 NumPy 陣列，並熟悉其屬性。

# %%
# 2.1 使用 np.array() 從列表和元組建立陣列
# 完成以下代碼
array1 = 
array2 = 

print(f"從列表建立: {array1}, 形狀: {array1.shape}, 維度: {array1.ndim}")
print(f"從元組建立: {array2}, 形狀: {array2.shape}, 維度: {array2.ndim}")

# %%
# 2.2 使用 numpy 內建函數建立特殊陣列
# 完成以下代碼

# 建立一個 1 到 20 間隔為 2 的陣列
# 提示: 使用 np.arange()
array3 = 

# 建立一個 0 到 1 之間均勻分布的 5 個點
# 提示: 使用 np.linspace()
array4 = 

# 建立一個 3x3 的單位矩陣
# 提示: 使用 np.eye()
array5 = 

# 建立一個 2x3 的全零陣列和 2x3 的全一陣列
# 提示: 使用 np.zeros() 和 np.ones()
array6 = 
array7 = 

print(f"arange: {array3}")
print(f"linspace: {array4}")
print(f"單位矩陣:\n{array5}")
print(f"全零陣列:\n{array6}")
print(f"全一陣列:\n{array7}")

# %%
# 2.3 建立隨機數陣列
# 完成以下代碼

# 設定隨機種子以便結果可重現
np.random.seed(42)

# 建立 2x3 的 0-1 均勻分布隨機數
# 提示: 使用 np.random.rand()
random1 = 

# 建立 2x3 的標準常態分布隨機數
# 提示: 使用 np.random.randn()
random2 = 

# 建立 10 個 1 到 100 間的隨機整數
# 提示: 使用 np.random.randint()
random3 = 

print(f"均勻分布隨機數:\n{random1}")
print(f"常態分布隨機數:\n{random2}")
print(f"隨機整數: {random3}")

# %%
# 2.4 改變陣列形狀
# 完成以下代碼

arr = np.arange(12)
print(f"原始陣列: {arr}")

# 將陣列重塑為 3x4 矩陣
# 提示: 使用 reshape 方法
reshaped = 

# 將矩陣轉置
# 提示: 使用 T 屬性
transposed = 

print(f"重塑後的陣列:\n{reshaped}")
print(f"轉置後的陣列:\n{transposed}")

# %% [markdown]
# ## 練習 3: 索引與切片
# 
# 請練習 NumPy 陣列的不同索引和切片方法。

# %%
# 3.1 一維陣列的索引與切片
arr_1d = np.arange(10)
print(f"一維陣列: {arr_1d}")

# 選取第一個、最後一個和倒數第二個元素
# 完成以下代碼
first = 
last = 
second_last = 

# 選取前三個元素
# 完成以下代碼
first_three = 

# 每隔一個元素選取
# 完成以下代碼
every_other = 

# 反轉陣列
# 完成以下代碼
reversed_arr = 

print(f"第一個元素: {first}")
print(f"最後一個元素: {last}")
print(f"倒數第二個元素: {second_last}")
print(f"前三個元素: {first_three}")
print(f"每隔一個元素: {every_other}")
print(f"反轉陣列: {reversed_arr}")

# %%
# 3.2 二維陣列的索引與切片
arr_2d = np.arange(16).reshape(4, 4)
print(f"二維陣列:\n{arr_2d}")

# 選取第一列第二行的元素 (索引 [0, 1])
# 完成以下代碼
element = 

# 選取第一列的所有元素
# 完成以下代碼
first_row = 

# 選取第一行的所有元素
# 完成以下代碼
first_col = 

# 選取子矩陣: 前兩列的前兩行
# 完成以下代碼
sub_matrix = 

print(f"元素 [0, 1]: {element}")
print(f"第一列: {first_row}")
print(f"第一行: {first_col}")
print(f"子矩陣:\n{sub_matrix}")

# %%
# 3.3 布林索引
arr = np.arange(10)
print(f"陣列: {arr}")

# 選取所有大於 5 的元素
# 完成以下代碼
greater_than_5 = 

# 選取所有偶數
# 完成以下代碼
even_numbers = 

# 選取所有處於 3 和 8 之間的元素 (包含)
# 完成以下代碼
between_3_and_8 = 

print(f"大於 5 的元素: {greater_than_5}")
print(f"偶數: {even_numbers}")
print(f"3 和 8 之間的元素: {between_3_and_8}")

# %%
# 3.4 花式索引
arr = np.arange(10) * 10  # [0, 10, 20, ..., 90]
print(f"陣列: {arr}")

# 使用索引陣列獲取特定位置的元素
indices = [1, 3, 5, 8]
# 完成以下代碼
selected = 

print(f"選取的元素: {selected}")

# 在二維陣列上使用花式索引
arr_2d = np.arange(16).reshape(4, 4)
print(f"二維陣列:\n{arr_2d}")

# 選取第 0、2 和 3 列
row_indices = [0, 2, 3]
# 完成以下代碼
selected_rows = 

print(f"選取的列:\n{selected_rows}")

# %% [markdown]
# ## 練習 4: Broadcasting 機制
# 
# 請練習 NumPy 的廣播機制，理解不同形狀陣列間的運算規則。

# %%
# 4.1 基本廣播: 標量與陣列
arr = np.array([1, 2, 3, 4, 5])

# 將陣列的每個元素加 10
# 完成以下代碼
result1 = 

# 將陣列的每個元素乘 2
# 完成以下代碼
result2 = 

print(f"原始陣列: {arr}")
print(f"加 10 後: {result1}")
print(f"乘 2 後: {result2}")

# %%
# 4.2 一維陣列與二維陣列的廣播
arr_2d = np.ones((3, 4))
arr_1d = np.array([1, 2, 3, 4])

print(f"二維陣列 (3x4):\n{arr_2d}")
print(f"一維陣列: {arr_1d}")

# 將一維陣列加到二維陣列的每一列
# 完成以下代碼
result3 = 

print(f"廣播結果:\n{result3}")

# %%
# 4.3 使用 reshape 和 newaxis 輔助廣播
arr = np.array([1, 2, 3])
print(f"陣列: {arr}")

# 將一維陣列轉為列向量 (3x1)
# 完成以下代碼
col_vector = 

# 將一維陣列轉為行向量 (1x3)
# 完成以下代碼
row_vector = 

print(f"列向量:\n{col_vector}")
print(f"行向量:\n{row_vector}")

# 計算外積 (每個元素對的乘積)
# 完成以下代碼
outer_product = 

print(f"外積結果:\n{outer_product}")

# %%
# 4.4 應用: 數據標準化
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"原始數據:\n{data}")

# 計算每列的均值
# 完成以下代碼
col_means = 

# 計算每列的標準差
# 完成以下代碼
col_stds = 

print(f"列均值: {col_means}")
print(f"列標準差: {col_stds}")

# 標準化數據 (減去均值並除以標準差)
# 完成以下代碼
standardized = 

print(f"標準化後的數據:\n{standardized}")

# %% [markdown]
# ## 練習 5: NumPy 數學函數
# 
# 請練習 NumPy 提供的各種數學函數，包括基本運算、統計函數和線性代數函數。

# %%
# 5.1 基本數學函數
x = np.array([-3, -2, -1, 0, 1, 2, 3])
print(f"陣列: {x}")

# 計算絕對值
# 完成以下代碼
abs_x = 

# 計算平方根 (忽略負數的警告)
# 完成以下代碼
sqrt_x = 

# 計算指數 (e^x)
# 完成以下代碼
exp_x = 

# 計算自然對數 (忽略負數的警告)
# 完成以下代碼
log_x = 

print(f"絕對值: {abs_x}")
print(f"平方根 (忽略警告): {sqrt_x}")
print(f"指數: {exp_x}")
print(f"自然對數 (忽略警告): {log_x}")

# %%
# 5.2 三角函數
angles = np.array([0, np.pi/4, np.pi/2, np.pi])
print(f"角度 (弧度): {angles}")

# 計算正弦值
# 完成以下代碼
sin_values = 

# 計算餘弦值
# 完成以下代碼
cos_values = 

# 計算正切值
# 完成以下代碼
tan_values = 

print(f"正弦值: {sin_values}")
print(f"餘弦值: {cos_values}")
print(f"正切值: {tan_values}")

# %%
# 5.3 統計函數
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"數據: {data}")

# 計算均值
# 完成以下代碼
mean_value = 

# 計算中位數
# 完成以下代碼
median_value = 

# 計算標準差
# 完成以下代碼
std_value = 

# 計算最小值和最大值
# 完成以下代碼
min_value = 
max_value = 

# 計算總和
# 完成以下代碼
sum_value = 

print(f"均值: {mean_value}")
print(f"中位數: {median_value}")
print(f"標準差: {std_value}")
print(f"最小值: {min_value}")
print(f"最大值: {max_value}")
print(f"總和: {sum_value}")

# %%
# 5.4 線性代數函數
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(f"矩陣 A:\n{A}")
print(f"矩陣 B:\n{B}")

# 計算矩陣乘法
# 完成以下代碼
matrix_product = 

# 計算矩陣的行列式
# 完成以下代碼
det_A = 

# 計算矩陣的逆
# 完成以下代碼
inv_A = 

# 計算特徵值和特徵向量
# 完成以下代碼
eigenvalues, eigenvectors = 

print(f"矩陣乘法 (A @ B):\n{matrix_product}")
print(f"A 的行列式: {det_A}")
print(f"A 的逆矩陣:\n{inv_A}")
print(f"A 的特徵值: {eigenvalues}")
print(f"A 的特徵向量:\n{eigenvectors}")

# %%
# 5.5 求解線性方程組 Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
print(f"矩陣 A:\n{A}")
print(f"向量 b: {b}")

# 求解方程 Ax = b
# 完成以下代碼
x = 

print(f"解向量 x: {x}")
print(f"驗證 A @ x = {A @ x}")

# %% [markdown]
# ## 練習 6: 小型統計分析應用
# 
# 請完成一個小型統計分析，綜合運用前面學到的 NumPy 技巧。

# %%
# 6.1 生成模擬數據
np.random.seed(42)

# 生成兩組正態分布數據，均值和標準差不同
# 第一組: 均值為 170，標準差為 7 的 50 個數據點 (代表身高)
heights = 

# 第二組: 均值為 65，標準差為 10 的 50 個數據點 (代表體重)
weights = 

print(f"身高數據 (前 5 個): {heights[:5]}")
print(f"體重數據 (前 5 個): {weights[:5]}")

# %%
# 6.2 數據分析
# 計算身高和體重的基本統計量
height_stats = {
    'mean': np.mean(heights),
    'median': np.median(heights),
    'std': np.std(heights),
    'min': np.min(heights),
    'max': np.max(heights)
}

weight_stats = {
    'mean': np.mean(weights),
    'median': np.median(weights),
    'std': np.std(weights),
    'min': np.min(weights),
    'max': np.max(weights)
}

print("身高統計量:")
for key, value in height_stats.items():
    print(f"  {key}: {value:.2f}")

print("\n體重統計量:")
for key, value in weight_stats.items():
    print(f"  {key}: {value:.2f}")

# %%
# 6.3 計算 BMI 指數
# BMI = 體重(kg) / 身高(m)^2

# 將身高從 cm 轉換為 m
heights_m = heights / 100

# 計算 BMI
bmi = weights / heights_m**2

print(f"BMI 數據 (前 5 個): {bmi[:5]}")
print(f"BMI 均值: {np.mean(bmi):.2f}")
print(f"BMI 標準差: {np.std(bmi):.2f}")

# %%
# 6.4 數據視覺化
plt.figure(figsize=(12, 5))

# 繪製身高分布
plt.subplot(1, 3, 1)
plt.hist(heights, bins=10, color='skyblue', edgecolor='black')
plt.title('身高分布')
plt.xlabel('身高 (cm)')
plt.ylabel('頻率')

# 繪製體重分布
plt.subplot(1, 3, 2)
plt.hist(weights, bins=10, color='lightgreen', edgecolor='black')
plt.title('體重分布')
plt.xlabel('體重 (kg)')
plt.ylabel('頻率')

# 繪製 BMI 分布
plt.subplot(1, 3, 3)
plt.hist(bmi, bins=10, color='salmon', edgecolor='black')
plt.title('BMI 分布')
plt.xlabel('BMI')
plt.ylabel('頻率')

plt.tight_layout()

# %%
# 6.5 數據分類與布林索引
# 根據 BMI 將數據分為不同類別
# BMI < 18.5: 過輕
# 18.5 <= BMI < 24: 正常
# 24 <= BMI < 28: 過重
# BMI >= 28: 肥胖

# 使用布林索引分類
underweight = bmi < 18.5
normal = (bmi >= 18.5) & (bmi < 24)
overweight = (bmi >= 24) & (bmi < 28)
obese = bmi >= 28

# 計算各類別人數與佔比
total = len(bmi)
underweight_count = np.sum(underweight)
normal_count = np.sum(normal)
overweight_count = np.sum(overweight)
obese_count = np.sum(obese)

print("BMI 分類統計:")
print(f"過輕: {underweight_count} 人 ({underweight_count/total*100:.1f}%)")
print(f"正常: {normal_count} 人 ({normal_count/total*100:.1f}%)")
print(f"過重: {overweight_count} 人 ({overweight_count/total*100:.1f}%)")
print(f"肥胖: {obese_count} 人 ({obese_count/total*100:.1f}%)")

# %%
# 6.6 高級分析: 身高體重相關性
# 計算身高與體重的相關係數
correlation = np.corrcoef(heights, weights)[0, 1]
print(f"身高與體重的相關係數: {correlation:.4f}")

# 使用 NumPy 的 polyfit 進行線性回歸
slope, intercept = np.polyfit(heights, weights, 1)
print(f"線性回歸結果: 體重 = {slope:.4f} × 身高 + {intercept:.4f}")

# 繪製散點圖與回歸線
plt.figure(figsize=(8, 6))
plt.scatter(heights, weights, alpha=0.7)
plt.plot(heights, slope * heights + intercept, 'r-', label='回歸線')
plt.title(f'身高與體重的關係 (相關係數: {correlation:.4f})')
plt.xlabel('身高 (cm)')
plt.ylabel('體重 (kg)')
plt.grid(True, alpha=0.3)
plt.legend()

# %% [markdown]
# ## 挑戰題 (選做)

# %%
# 挑戰 1: 使用 NumPy 實現簡單的圖像操作
# 創建一個模擬的灰度圖像 (10x10 的矩陣)
np.random.seed(42)
image = np.random.randint(0, 256, size=(10, 10))
print("原始圖像:")
print(image)

# 將圖像旋轉 90 度 (提示: 使用 np.rot90)


# 將圖像沿著水平方向翻轉 (提示: 使用 np.fliplr)


# 提取圖像的中心 4x4 區域


# 將圖像的亮度提高 (所有像素值加 50，但不超過 255)


# %%
# 挑戰 2: 實現蒙地卡羅模擬估算圓周率
# 提示: 在單位正方形內隨機生成點，計算落在單位圓內的點的比例
np.random.seed(42)

# 生成大量隨機點 (x, y)，其中 x, y 均勻分布在 [-1, 1] 之間
n_points = 10000
points = 

# 計算每個點到原點的距離
distances = 

# 計算落在單位圓內的點的數量 (距離 <= 1)
in_circle = 

# 估算圓周率 (圓內點數 / 總點數 * 4)
pi_estimate = 

print(f"蒙地卡羅方法估算的圓周率: {pi_estimate}")
print(f"實際圓周率 (np.pi): {np.pi}")
print(f"誤差: {abs(pi_estimate - np.pi)}")

# 視覺化
plt.figure(figsize=(6, 6))
in_circle_points = points[in_circle]
out_circle_points = points[~in_circle]
plt.scatter(in_circle_points[:, 0], in_circle_points[:, 1], s=1, c='blue', alpha=0.5, label='圓內')
plt.scatter(out_circle_points[:, 0], out_circle_points[:, 1], s=1, c='red', alpha=0.5, label='圓外')
plt.axis('equal')
plt.title(f'蒙地卡羅估算圓周率: {pi_estimate:.6f}')
plt.legend()
plt.grid(True, alpha=0.3) 