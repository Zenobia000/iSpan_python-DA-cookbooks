# %% 
# M1.5 NumPy 常用數學函數

本教學將介紹 NumPy 中最常用的數學函數，包括基本數學運算、統計函數、線性代數函數等。
這些函數是科學計算、資料分析和機器學習的基礎。

# %% 
## 教學目標

- 掌握 NumPy 的基本數學運算函數
- 學習常用的統計函數與應用
- 了解線性代數相關函數及其用途
- 實踐這些函數在資料分析中的應用

# %% 
## 1. 環境設置與導入必要的套件

# %%
import numpy as np
import matplotlib.pyplot as plt

# 設定顯示選項，使輸出更易讀
np.set_printoptions(precision=3, suppress=True)

# %% 
## 2. 基本數學運算

**學習要點**：
- 熟悉 NumPy 中的基本算術運算子及其矢量化特性
- 掌握 NumPy 通用函數(ufuncs)的使用方法與優勢
- 了解如何使用函數參數來優化計算和控制輸出
- 學習條件運算和邏輯運算的使用技巧

**應用場域**：
- 科學計算和工程分析中的大規模數據處理
- 物理、金融、生物等領域的模型計算
- 數據預處理和特徵工程
- 圖像處理和信號分析的基礎計算

# %% 
### 2.1 常見的數學運算子

# %%
# 建立範例陣列
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# 基本算術運算
print(f"加法 (a + b): {a + b}")
print(f"減法 (a - b): {a - b}")
print(f"乘法 (a * b): {a * b}")  # 元素對元素相乘
print(f"除法 (a / b): {a / b}")
print(f"冪次 (a ** 2): {a ** 2}")
print(f"模數 (a % 2): {a % 2}")

# 比較運算
print(f"\n等於 (a == 2): {a == 2}")
print(f"不等於 (a != 2): {a != 2}")
print(f"大於 (a > 2): {a > 2}")
print(f"小於等於 (a <= 2): {a <= 2}")

# 邏輯運算
mask1 = a > 2
mask2 = a < 4
print(f"\nAND (mask1 & mask2): {mask1 & mask2}")  # 只有 a[2] (值為3) 滿足
print(f"OR (mask1 | mask2): {mask1 | mask2}")  # a[0,1,2] 滿足 (1,2,3)
print(f"NOT (~mask1): {~mask1}")  # 反轉條件

# %% 
**解說**：
- NumPy 的運算子是元素級的(element-wise)，會自動應用於陣列中的每個元素
- 比較運算符返回布爾陣列，表示每個位置上的比較結果
- 邏輯運算符(`&`, `|`, `~`)用於組合多個布爾條件，注意使用時的括號以避免運算優先級問題
- 與 Python 原生列表相比，NumPy 的矢量化操作更高效，尤其是處理大型數據時
- 這些基本運算是更複雜數學操作的基礎，掌握它們對提高數據處理效率至關重要

# %% 
### 2.2 通用函數 (ufuncs)

# %%
# 數學函數
x = np.array([0, np.pi/4, np.pi/2, np.pi])  # 0, 45, 90, 180 度（弧度）
print(f"x: {x}")
print(f"sin(x): {np.sin(x)}")
print(f"cos(x): {np.cos(x)}")
print(f"tan(x): {np.tan(x)}")

# 取整函數
y = np.array([-1.7, -1.5, -0.2, 0.2, 1.5, 1.7, 2.0])
print(f"\ny: {y}")
print(f"向下取整 floor(y): {np.floor(y)}")
print(f"向上取整 ceil(y): {np.ceil(y)}")
print(f"四捨五入 round(y): {np.round(y)}")
print(f"去除小數部分 trunc(y): {np.trunc(y)}")

# 絕對值與符號
z = np.array([-2.5, -1.0, 0, 1.0, 2.5])
print(f"\nz: {z}")
print(f"絕對值 abs(z): {np.abs(z)}")
print(f"符號 sign(z): {np.sign(z)}")  # -1 (負), 0, 1 (正)

# 指數與對數
p = np.array([1, 2, 3])
print(f"\np: {p}")
print(f"指數 exp(p): {np.exp(p)}")  # e^p
print(f"自然對數 log(p): {np.log(p)}")  # ln(p)
print(f"以10為底對數 log10(p): {np.log10(p)}")
print(f"以2為底對數 log2(p): {np.log2(p)}")
print(f"平方根 sqrt(p): {np.sqrt(p)}")
print(f"立方根 cbrt(p): {np.cbrt(p)}")

# %% 
**解說**：
- 通用函數(ufuncs)是 NumPy 的核心功能，提供高效的元素級數學運算
- 三角函數(sin, cos, tan)在科學計算、信號處理和圖形渲染中廣泛應用
- 取整函數(floor, ceil, round, trunc)在不同情境下有不同用途，例如:
  - floor: 向下取整，適用於需要取最小整數的情況
  - ceil: 向上取整，適用於需要取最大整數的情況
  - round: 四捨五入，常用於數據呈現
  - trunc: 截斷小數部分，僅保留整數部分
- 指數和對數函數在統計學、機器學習(特別是優化算法)和金融建模中極為重要
- 平方根和立方根函數在幾何計算、統計學中的標準差計算等方面常用

# %% 
### 2.3 函數參數及其使用

# %%
# 許多 NumPy 函數支持 out 參數，允許將結果存儲到預先分配的陣列中
out_array = np.empty_like(a)
np.multiply(a, 2, out=out_array)
print(f"a: {a}")
print(f"out_array 結果 (a * 2): {out_array}")

# where 參數用於條件運算
result = np.power(a, 2, where=(a > 2))  # 只計算 a > 2 的元素的平方
print(f"\npower(a, 2, where=(a > 2)): {result}")

# %% 
**解說**：
- `out` 參數允許將計算結果直接寫入預先分配的陣列，這可以提高性能並減少記憶體使用：
  - 避免創建新的臨時陣列
  - 在處理大型數據時特別有用
  - 可以用於原地(in-place)操作，減少記憶體碎片
- `where` 參數實現條件計算，只在指定條件為真的元素上執行操作：
  - 可以替代複雜的索引操作
  - 結合了條件邏輯和數學運算，使代碼更簡潔
  - 未滿足條件的位置將保持原值或設為未定義
- 這些參數在數據處理管道(pipelines)中非常有用，可以構建高效的數據轉換流程

# %% 
## 3. 統計函數

**學習要點**：
- 掌握 NumPy 中常用的統計描述性函數
- 學習在多維陣列上進行統計計算的方法
- 理解加權平均和累積函數的用途與使用方法
- 探討統計描述函數在資料分析中的應用

**應用場域**：
- 數據集的探索性分析
- 科學實驗數據的統計特徵提取
- 金融數據的風險與收益分析
- 機器學習模型的數據預處理與特徵工程

# %% 
### 3.1 基本統計函數

# %%
# 建立示例數據
data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"數據: {data}")

# 基本統計量
print(f"總和 sum: {np.sum(data)}")
print(f"最小值 min: {np.min(data)}")
print(f"最大值 max: {np.max(data)}")
print(f"範圍 ptp (peak to peak): {np.ptp(data)}")  # max - min
print(f"平均值 mean: {np.mean(data)}")
print(f"中位數 median: {np.median(data)}")

# 分位數
print(f"25% 分位數: {np.percentile(data, 25)}")
print(f"50% 分位數 (中位數): {np.percentile(data, 50)}")
print(f"75% 分位數: {np.percentile(data, 75)}")

# 變異性
print(f"\n方差 var: {np.var(data)}")
print(f"標準差 std: {np.std(data)}")

# %% 
**解說**：
- `sum`, `min`, `max` 等基本統計函數提供了數據集的整體概況
- `ptp` (peak to peak) 計算數據範圍（最大值減最小值），顯示數據的跨度
- `mean` 和 `median` 提供了中心趨勢的不同度量：
  - 平均值受極端值影響較大，中位數對異常值更穩健
  - 比較兩者可以初步判斷數據分布的偏斜程度
- 分位數提供了數據分布的更完整圖景：
  - 25%和75%分位數（即第一和第三四分位數）反映了數據的散布情況
  - 分位數差(IQR)常用於識別異常值
- 方差和標準差量化了數據的離散程度：
  - 標準差是方差的平方根，與原數據單位相同，便於解釋
  - 兩者都是衡量數據穩定性和一致性的重要指標

# %% 
### 3.2 多維陣列的統計

# %%
# 建立多維示例數據
data_2d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(f"2D 數據:\n{data_2d}")

# 沿著不同軸計算統計量
print(f"\n沿著 axis=0 (列) 的總和:\n{np.sum(data_2d, axis=0)}")
print(f"沿著 axis=1 (行) 的總和:\n{np.sum(data_2d, axis=1)}")

print(f"\n沿著 axis=0 (列) 的平均值:\n{np.mean(data_2d, axis=0)}")
print(f"沿著 axis=1 (行) 的平均值:\n{np.mean(data_2d, axis=1)}")

print(f"\n沿著 axis=0 (列) 的最大值:\n{np.max(data_2d, axis=0)}")
print(f"沿著 axis=1 (行) 的最大值:\n{np.max(data_2d, axis=1)}")

# %% 
**解說**：
- 多維陣列的統計計算使用 `axis` 參數控制計算方向：
  - `axis=0` 沿著列方向（垂直方向），對每列進行計算
  - `axis=1` 沿著行方向（水平方向），對每行進行計算
  - 不指定 `axis` 則對整個陣列所有元素計算
- 這種靈活性使得數據分析能夠從不同維度探索數據特性：
  - 在表格數據中，行通常代表樣本，列代表特徵
  - `axis=0` 的計算可以得到每個特徵的統計屬性
  - `axis=1` 的計算可以得到每個樣本的綜合指標
- 在圖像處理中，多維統計應用廣泛：
  - 可用於計算每個顏色通道的特性
  - 在卷積神經網絡中用於計算特徵圖的統計屬性

# %% 
### 3.3 加權平均與累積函數

# %%
# 加權平均
values = np.array([1, 2, 3, 4])
weights = np.array([0.1, 0.2, 0.3, 0.4])  # 權重總和為 1
weighted_avg = np.average(values, weights=weights)
print(f"值: {values}")
print(f"權重: {weights}")
print(f"加權平均: {weighted_avg}")

# 累積函數
print(f"\n累積總和 cumsum: {np.cumsum(values)}")
print(f"累積乘積 cumprod: {np.cumprod(values)}")

# 在多維陣列上的累積函數
print(f"\n2D 數據:\n{data_2d}")
print(f"沿著 axis=0 (列) 的累積總和:\n{np.cumsum(data_2d, axis=0)}")
print(f"沿著 axis=1 (行) 的累積總和:\n{np.cumsum(data_2d, axis=1)}")

# %% 
**解說**：
- 加權平均(`average`)在許多應用中比簡單平均更有用：
  - 允許對不同數據點賦予不同的重要性
  - 在時間序列分析中可給予最新數據更高權重
  - 在機器學習中用於集成模型的投票權重
- 累積函數計算累加或累乘的數列：
  - `cumsum` 返回累積和，每個位置的值是到該位置所有元素的總和
  - `cumprod` 返回累積乘積，每個位置的值是到該位置所有元素的乘積
  - 這些函數保留原始陣列的形狀，便於與原數據對比
- 在金融分析中，累積函數應用廣泛：
  - 用於計算累積收益率
  - 繪製資金曲線
  - 分析投資組合的歷史表現

# %% 
### 3.4 統計描述函數

# %%
# 隨機生成一組正態分布的數據
normal_data = np.random.normal(loc=0, scale=1, size=1000)  # 均值=0, 標準差=1

# 使用 matplotlib 繪製直方圖
plt.figure(figsize=(10, 6))
plt.hist(normal_data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(np.mean(normal_data), color='red', linestyle='dashed', linewidth=1, label=f'Mean: {np.mean(normal_data):.2f}')
plt.axvline(np.median(normal_data), color='green', linestyle='dashed', linewidth=1, label=f'Median: {np.median(normal_data):.2f}')
plt.axvline(np.mean(normal_data) + np.std(normal_data), color='orange', linestyle='dotted', linewidth=1, label=f'Mean+Std: {np.mean(normal_data)+np.std(normal_data):.2f}')
plt.axvline(np.mean(normal_data) - np.std(normal_data), color='orange', linestyle='dotted', linewidth=1)
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()
plt.grid(alpha=0.3)

# 統計摘要
print(f"均值: {np.mean(normal_data):.4f}")
print(f"中位數: {np.median(normal_data):.4f}")
print(f"標準差: {np.std(normal_data):.4f}")
print(f"偏度 (skewness): {np.mean(((normal_data - np.mean(normal_data)) / np.std(normal_data)) ** 3):.4f}")
print(f"峰度 (kurtosis): {np.mean(((normal_data - np.mean(normal_data)) / np.std(normal_data)) ** 4) - 3:.4f}")

# %% 
**解說**：
- 統計描述函數提供了數據分布的全面了解：
  - 直方圖可視化數據的頻率分布
  - 均值和中位數顯示中心趨勢
  - 標準差表示數據的離散程度
- 在正態分布中：
  - 約68%的數據落在均值±標準差範圍內
  - 約95%的數據落在均值±2標準差範圍內
  - 約99.7%的數據落在均值±3標準差範圍內
- 偏度(skewness)衡量分布的不對稱性：
  - 正偏度表示分布右側拖尾(右偏)
  - 負偏度表示分布左側拖尾(左偏)
  - 偏度為0表示完全對稱(如正態分布)
- 峰度(kurtosis)衡量分布的"尖峰度"：
  - 正峰度表示比正態分布更尖銳(瘦高)
  - 負峰度表示比正態分布更平坦(矮胖)
  - 通常減去3以使正態分布的峰度為0

# %% 
## 4. 線性代數函數

**學習要點**：
- 掌握 NumPy 中基本矩陣運算的方法
- 理解矩陣分解技術及其數學原理
- 學習如何計算並應用特徵值和特徵向量
- 熟悉使用 NumPy 求解線性方程組的方法

**應用場域**：
- 機器學習算法中的矩陣運算
- 圖像處理和計算機視覺中的轉換
- 物理模擬和工程計算
- 數據降維和特徵提取

# %% 
### 4.1 基本矩陣運算

# %%
# 建立示例矩陣
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(f"矩陣 A:\n{A}")
print(f"矩陣 B:\n{B}")

# 矩陣乘法
C = np.dot(A, B)  # 或者使用 A @ B (Python 3.5+)
print(f"\n矩陣乘法 (A @ B):\n{C}")

# 矩陣轉置
A_T = A.T
print(f"\n矩陣轉置 (A.T):\n{A_T}")

# 矩陣行列式
det_A = np.linalg.det(A)
print(f"\n矩陣行列式 det(A): {det_A}")

# 矩陣的跡 (對角線元素和)
trace_A = np.trace(A)
print(f"矩陣的跡 trace(A): {trace_A}")

# 矩陣求逆
inv_A = np.linalg.inv(A)
print(f"\n矩陣求逆 inv(A):\n{inv_A}")

# 驗證 A*A^(-1) = I
I = np.dot(A, inv_A)
print(f"A @ inv(A) (應接近單位矩陣):\n{I}")

# %% 
**解說**：
- 矩陣乘法(`np.dot`或`@`運算符)是線性代數中最基本和重要的運算：
  - 不同於元素級乘法(`*`)，矩陣乘法考慮了矩陣間的內積關係
  - 要求第一個矩陣的列數等於第二個矩陣的行數
  - 結果矩陣大小為(第一個矩陣的行數 × 第二個矩陣的列數)
- 矩陣轉置(`.T`)交換行與列：
  - 在數據分析中常用於特徵與樣本維度的轉換
  - 在計算中可以優化某些運算的效率
- 行列式(`np.linalg.det`)表示矩陣的「體積縮放因子」：
  - 若為0，表示矩陣是奇異的（不可逆）
  - 在空間變換中代表體積的縮放比例
- 矩陣的跡(`np.trace`)是對角線元素之和：
  - 在物理學中與系統的能量相關
  - 矩陣的特徵值之和等於矩陣的跡
- 矩陣求逆(`np.linalg.inv`)計算矩陣的逆：
  - 僅適用於非奇異方陣
  - 在數值計算中，直接使用逆矩陣可能導致數值不穩定性
  - 實際應用中，通常優先考慮使用`np.linalg.solve`解線性方程組

# %% 
### 4.2 矩陣分解

# %%
# 建立一個示例矩陣
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"矩陣 X:\n{X}")

# 奇異值分解 (SVD)
U, sigma, V = np.linalg.svd(X)
print(f"\nSVD 分解:")
print(f"U (左奇異向量):\n{U}")
print(f"sigma (奇異值): {sigma}")
print(f"V (右奇異向量):\n{V}")

# 重構原始矩陣
sigma_mat = np.zeros_like(X, dtype=float)
np.fill_diagonal(sigma_mat, sigma)
X_reconstructed = U @ sigma_mat @ V
print(f"\n重構的矩陣:\n{X_reconstructed}")
print(f"原始矩陣與重構矩陣是否相等: {np.allclose(X, X_reconstructed)}")

# LU 分解
P, L, U = scipy.linalg.lu(X) if 'scipy' in globals() else (None, None, None)
if P is not None:
    print(f"\nLU 分解:")
    print(f"P (置換矩陣):\n{P}")
    print(f"L (下三角矩陣):\n{L}")
    print(f"U (上三角矩陣):\n{U}")
    print(f"P @ L @ U:\n{P @ L @ U}")

# QR 分解
Q, R = np.linalg.qr(X)
print(f"\nQR 分解:")
print(f"Q (正交矩陣):\n{Q}")
print(f"R (上三角矩陣):\n{R}")
print(f"Q @ R:\n{Q @ R}")

# %% 
**解說**：
- 奇異值分解(SVD)是最強大的矩陣分解方法之一：
  - 將任意矩陣分解為三個矩陣的乘積：U×Σ×V^T
  - U和V包含正交向量，Σ是對角線上的奇異值
  - 廣泛應用於數據壓縮、降維(如PCA)、噪聲濾除、推薦系統等
  - 可以用來求解最小二乘問題、計算矩陣的偽逆以及圖像處理
- LU分解將矩陣分解為下三角矩陣L和上三角矩陣U的乘積：
  - 通常包含置換矩陣P，即P×A=L×U
  - 主要用於有效求解線性方程組
  - 只需分解一次，然後可以高效求解多個右側向量
- QR分解將矩陣分解為正交矩陣Q和上三角矩陣R的乘積：
  - Q的列向量形成正交基
  - 廣泛用於最小二乘問題、特徵值計算和QR算法
  - 在機器學習中用於矩陣正交化過程

# %% 
### 4.3 特徵值與特徵向量

# %%
# 建立對稱矩陣
M = np.array([[2, -1], [-1, 2]])
print(f"矩陣 M:\n{M}")

# 計算特徵值和特徵向量
eigenvalues, eigenvectors = np.linalg.eig(M)
print(f"\n特徵值: {eigenvalues}")
print(f"特徵向量 (每列是一個特徵向量):\n{eigenvectors}")

# 驗證 M @ v = λ * v
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lambda_v = eigenvalues[i] * v
    m_v = M @ v
    print(f"\n特徵值 {i+1} (λ = {eigenvalues[i]:.2f}):")
    print(f"特徵向量 v{i+1}: {v}")
    print(f"M @ v{i+1}: {m_v}")
    print(f"λ * v{i+1}: {lambda_v}")
    print(f"M @ v{i+1} ≈ λ * v{i+1}: {np.allclose(m_v, lambda_v)}")

# %% 
**解說**：
- 特徵值和特徵向量是理解矩陣作為線性變換的關鍵：
  - 特徵向量是經過矩陣變換後方向保持不變的向量
  - 特徵值表示沿特徵向量方向的縮放係數
  - 方程 Av = λv 中，v是特徵向量，λ是對應的特徵值
- 應用範圍廣泛：
  - 主成分分析(PCA)中用於降維
  - 在振動分析中表示自然振動模式和頻率
  - 量子力學中的能量本徵態
  - 網頁排名算法(如PageRank)中用於找到重要節點
- 對稱矩陣的特殊性質：
  - 所有特徵值都是實數
  - 特徵向量相互正交
  - 可以通過特徵分解被對角化：M = QΛQ^T
- NumPy的`linalg.eig`返回特徵值和特徵向量，每列是一個特徵向量

# %% 
### 4.4 求解線性方程組

# %%
# 線性方程組: Ax = b
A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
print(f"A:\n{A}")
print(f"b: {b}")

# 求解 x
x = np.linalg.solve(A, b)
print(f"\nx 解: {x}")

# 驗證解
print(f"A @ x: {A @ x}")
print(f"A @ x ≈ b: {np.allclose(A @ x, b)}")

# 使用矩陣求逆求解
x_inv = np.linalg.inv(A) @ b
print(f"\n使用矩陣求逆求得的 x: {x_inv}")
print(f"兩種方法結果是否相等: {np.allclose(x, x_inv)}")

# %% 
**解說**：
- 線性方程組是許多科學和工程問題的數學模型：
  - 表示為形式 Ax = b，其中 A 是係數矩陣，b 是常數向量，x 是未知數
- NumPy提供兩種主要解法：
  - `np.linalg.solve`直接求解線性方程組
  - 使用矩陣求逆方法：x = A^(-1)b
- 從數值計算角度，`solve`方法通常優於矩陣求逆：
  - 計算效率更高，特別是對大型系統
  - 數值穩定性更好，減少舍入誤差
  - 內部使用更高效的算法(如LU分解)而非顯式計算逆矩陣
- 線性方程組求解的應用廣泛：
  - 最小二乘擬合
  - 有限元分析
  - 平衡方程求解
  - 電路分析和網絡流

# %% 
## 5. 實際應用：數據分析案例

**學習要點**：
- 運用 NumPy 數學函數解決實際問題
- 學習結合多種函數實現複雜計算
- 透過視覺化理解數據特性和關聯性
- 掌握數據計算與資料轉換的技巧

**應用場域**：
- 健康與醫療數據分析
- 多變量數據的相關性研究
- 人口統計數據分析
- 生物統計學和臨床研究

# %% 
# ### 5.1 計算 BMI 指數

# %%
# 建立身高(cm)和體重(kg)數據
heights = np.array([175, 168, 182, 177, 165, 190])
weights = np.array([75, 68, 85, 80, 60, 95])

# 將身高從 cm 轉換為 m
heights_m = heights / 100

# 計算 BMI (體重/身高^2)
bmi = weights / heights_m**2

print(f"身高 (cm): {heights}")
print(f"體重 (kg): {weights}")
print(f"BMI 指數: {bmi}")

# BMI 分類
categories = ['過輕', '正常', '過重', '輕度肥胖', '中度肥胖', '重度肥胖']
thresholds = [0, 18.5, 24, 27, 30, 35, 100]

# 為每個 BMI 值分配類別
bmi_categories = []
for b in bmi:
    for i in range(len(thresholds) - 1):
        if thresholds[i] <= b < thresholds[i+1]:
            bmi_categories.append(categories[i])
            break

# 顯示結果
for h, w, b, c in zip(heights, weights, bmi, bmi_categories):
    print(f"身高: {h} cm, 體重: {w} kg, BMI: {b:.2f}, 分類: {c}")

# 繪製 BMI 分布
plt.figure(figsize=(10, 6))
plt.bar(range(len(bmi)), bmi, color='skyblue')
plt.axhline(y=18.5, color='green', linestyle='-', alpha=0.7, label='過輕/正常')
plt.axhline(y=24, color='yellow', linestyle='-', alpha=0.7, label='正常/過重')
plt.axhline(y=27, color='orange', linestyle='-', alpha=0.7, label='過重/輕度肥胖')
plt.axhline(y=30, color='red', linestyle='-', alpha=0.7, label='輕度/中度肥胖')
plt.axhline(y=35, color='purple', linestyle='-', alpha=0.7, label='中度/重度肥胖')
plt.xticks(range(len(bmi)), [f"P{i+1}" for i in range(len(bmi))])
plt.ylabel('BMI')
plt.title('BMI 分布')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# %% 
**解說**：
- BMI(身體質量指數)計算是數學函數應用的基本實例：
  - 使用公式：BMI = 體重(kg) / 身高(m)²
  - 單位轉換(cm到m)通過簡單除法實現
  - 使用矢量化運算同時處理多個人的數據
- 分類邏輯運用了範圍比較：
  - 使用閾值陣列定義各分類的界限
  - 透過遍歷方式為每個BMI值分配適當類別
  - 實際應用中可以用NumPy的`np.digitize`函數更高效地實現
- 結果視覺化：
  - 條形圖直觀顯示每個人的BMI值
  - 水平線標明不同BMI分類的閾值
  - 結合數值結果和視覺效果更全面地理解數據
- 此例展示了NumPy在健康數據分析中的簡單應用，類似方法可用於其他醫療指標計算

# %% 
# ### 5.2 多維數據分析：相關性矩陣

# %%
# 創建一個多變量數據集
np.random.seed(42)
n_samples = 100

# 假設有這幾個變量: 年齡, 身高, 體重, 收入
age = np.random.normal(35, 10, n_samples)  # 均值=35, 標準差=10
height = 160 + 0.3 * age + np.random.normal(0, 5, n_samples)  # 與年齡正相關
weight = 50 + 0.4 * height + np.random.normal(0, 10, n_samples)  # 與身高正相關
income = 20000 + 1000 * age + np.random.normal(0, 5000, n_samples)  # 與年齡正相關

# 組合數據
data = np.column_stack((age, height, weight, income))
print(f"數據形狀: {data.shape}")
print(f"前5行數據:\n{data[:5]}")

# 計算相關係數矩陣 (使用 numpy.corrcoef)
corr_matrix = np.corrcoef(data, rowvar=False)
print(f"\n相關係數矩陣:\n{corr_matrix}")

# 使用 matplotlib 繪製相關係數矩陣的熱力圖
plt.figure(figsize=(8, 6))
plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(label='Correlation Coefficient')
plt.xticks(range(4), ['Age', 'Height', 'Weight', 'Income'])
plt.yticks(range(4), ['Age', 'Height', 'Weight', 'Income'])
plt.title('Correlation Matrix')

# 在熱力圖上標註相關係數值
for i in range(4):
    for j in range(4):
        plt.text(j, i, f'{corr_matrix[i, j]:.2f}', 
                 ha='center', va='center', 
                 color='white' if abs(corr_matrix[i, j]) > 0.5 else 'black')

# %% 
**解說**：
- 相關性分析是探索變量間關係的關鍵統計方法：
  - 相關係數範圍從-1到1，表示線性關係的強度和方向
  - 1代表完全正相關，-1代表完全負相關，0代表無線性相關
  - NumPy的`corrcoef`函數計算Pearson相關係數矩陣
- 數據生成模型中設置了以下關係：
  - 年齡與身高正相關 (年齡增加，身高傾向增加)
  - 身高與體重正相關 (身高增加，體重傾向增加)
  - 年齡與收入正相關 (年齡增加，收入傾向增加)
  - 添加隨機噪聲使關係更符合現實
- 熱力圖視覺化相關性：
  - 顏色強度反映相關性強度
  - 冷色調(藍色)表示負相關，暖色調(紅色)表示正相關
  - 對角線始終為1，表示變量與自身完全相關
- 實際應用：
  - 在特徵工程中識別冗餘變量
  - 發現潛在因果關係的初步證據
  - 幫助選擇預測模型的輸入特徵

# %% 
## 6. 總結與最佳實踐

**學習要點**：
- 回顧 NumPy 數學函數的使用原則和技巧
- 整理常用數學函數的速查表
- 理解各類數學函數的適用場景和限制
- 掌握數學函數使用的最佳實踐和效能考量

**應用場域**：
- 數據分析工作流程優化
- 科學計算代碼的效能提升
- 複雜模型開發和優化
- 教學和知識分享

# %% 
### NumPy 數學函數使用建議

1. **向量化操作優於迴圈**: 儘量使用 NumPy 的向量化函數而非 Python 迴圈，它們更快且更易讀
2. **注意 axis 參數**: 多維陣列計算時，明確指定 axis 可避免混淆
3. **使用適當的數據類型**: 根據需要選擇正確的數據類型可提高效能並節省記憶體
4. **了解廣播規則**: 廣播可以大幅簡化程式碼，但需了解其規則避免錯誤
5. **使用 out 參數**: 對大型計算，使用 out 參數可避免額外的記憶體分配

### 常用數學函數速查表

#### 基本數學函數
- 加減乘除: `+`, `-`, `*`, `/`
- 次方: `**` 或 `np.power()`
- 平方根: `np.sqrt()`
- 對數: `np.log()`, `np.log10()`, `np.log2()`
- 指數: `np.exp()`
- 三角函數: `np.sin()`, `np.cos()`, `np.tan()`

#### 統計函數
- 總和: `np.sum()`
- 平均值: `np.mean()`
- 中位數: `np.median()`
- 標準差: `np.std()`
- 方差: `np.var()`
- 分位數: `np.percentile()`

#### 線性代數
- 矩陣乘法: `@` 或 `np.dot()`
- 轉置: `.T`
- 求逆: `np.linalg.inv()`
- 行列式: `np.linalg.det()`
- 特徵值分解: `np.linalg.eig()`
- 奇異值分解: `np.linalg.svd()`
- 解線性方程組: `np.linalg.solve()`

# %% 
**解說**：
- 向量化操作是 NumPy 最重要的效能優勢：
  - 向量化代碼不僅執行更快，而且更簡潔、更少出錯
  - 例如： `np.sum(a)` 比 `sum([a[i] for i in range(len(a))])` 快得多
  - 避免使用顯式Python循環遍歷NumPy陣列
- `axis` 參數的正確使用至關重要：
  - 當應用於多維陣列時，很多函數的行為依賴於 axis 設置
  - `axis=0` 通常沿列(垂直)方向操作，`axis=1` 沿行(水平)方向操作
  - 當不確定時，先在小型測試陣列上驗證行為
- 內存管理技巧能顯著提升效能：
  - 使用 `out` 參數避免創建中間陣列，特別是在重複計算中
  - 針對大數據集，考慮使用較小的數據類型(如 `float32` 代替 `float64`)
  - 對於大型數據處理，考慮使用 `np.memmap` 或分批處理
- 速查表提供了快速參考：
  - 根據任務選擇合適的函數而非重新發明輪子
  - 組合使用不同類別的函數可以解決複雜問題
  - 高效利用 NumPy 生態系統能大幅提升數據分析效率和可靠性 