# %% [markdown]
## 📘 M2.1 Pandas DataFrame 與 Series 基礎操作

本教學將介紹 Pandas 的兩個核心數據結構：`Series` 與 `DataFrame`，它們是進行數據分析的基礎。
我們將詳細講解這兩種數據結構的特性、創建方法和基本操作。

# %% [markdown]
### 🎯 教學目標

- 🔍 了解 Pandas 中 Series 和 DataFrame 的概念和關係
- 📦 學習創建和初始化 Series 和 DataFrame 的多種方法
- 🛠️ 掌握 Series 和 DataFrame 的基本屬性和方法
- 💻 練習常見的數據操作技巧

# %%
### 🧰 1. 環境設置與導入必要的套件

# %%
import numpy as np
import pandas as pd

# 設置顯示選項
pd.set_option('display.max_rows', 10)  # 最多顯示10行
pd.set_option('display.max_columns', 10)  # 最多顯示10列
pd.set_option('display.width', 80)  # 顯示寬度
pd.set_option('display.precision', 3)  # 顯示小數點後3位

# %%
# 解說：
# - `pd.set_option` 用於自定義 Pandas 的顯示設置，讓輸出結果更易閱讀
# - `display.max_rows` 和 `display.max_columns` 控制顯示的行數和列數，避免大型數據框過度輸出
# - `display.precision` 設定浮點數顯示的小數位數，保持輸出簡潔
# - 這些設置僅影響顯示，不會改變實際數據計算的精度

# %%
### 📊 2. Pandas Series 介紹

# %%
### 2.1 什麼是 Series?

# %%
# 學習要點：
# - Series 是 Pandas 中的一維標籤數組，可以存儲各種數據類型
# - Series 由索引(index)和值(values)兩部分組成
# - Series 可以看作是一個帶有標籤的一維 NumPy 數組，或類似字典的數據結構

# %% [markdown]
# Series 是 Pandas 中的一維標籤數組，可以存儲各種數據類型（整數、字符串、浮點數、Python 對象等）。
# Series 可以看作是一個帶有標籤的一維 NumPy 數組，或者是一個類似於字典的數據結構。

# %%
# 創建一個簡單的 Series
s = pd.Series([1, 3, 5, 7, 9])
print(s)
print(f"類型: {type(s)}")

# 查看 Series 的基本屬性
print(f"\n索引: {s.index}")
print(f"值: {s.values}")
print(f"形狀: {s.shape}")
print(f"維度: {s.ndim}")
print(f"數據類型: {s.dtype}")

# %%
# 解說：
# - Series 由兩部分組成：索引 (index) 和值 (values)
# - 如果未指定索引，Pandas 自動創建從 0 開始的整數索引
# - `.values` 屬性返回底層的 NumPy 數組，可用於與 NumPy 互操作
# - Series 的 `.dtype` 表示其中所有元素的數據類型，類似於 NumPy 數組
# - 雖然是一維結構，Series 比 NumPy 數組更靈活，支持標籤索引和更豐富的操作

# %%
### 2.2 Series 的創建方法

# %%
# 方法1: 從列表創建 (默認整數索引從0開始)
s1 = pd.Series([10, 20, 30, 40])
print("從列表創建 Series:")
print(s1)

# 方法2: 從NumPy數組創建
arr = np.array([100, 200, 300, 400])
s2 = pd.Series(arr)
print("\n從NumPy數組創建 Series:")
print(s2)

# 方法3: 從字典創建 (鍵作為索引)
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
s3 = pd.Series(d)
print("\n從字典創建 Series:")
print(s3)

# 方法4: 使用標量值創建
s4 = pd.Series(5, index=['a', 'b', 'c'])  # 所有值都是5
print("\n使用標量值創建 Series:")
print(s4)

# 方法5: 指定自定義索引
s5 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
print("\n指定自定義索引創建 Series:")
print(s5)

# %%
# 解說：
# - 從列表或 NumPy 數組創建 Series 時，系統默認創建整數索引
# - 從字典創建時，字典的鍵自動成為 Series 的索引，值成為 Series 的數據值
# - 使用標量創建時，該值會被重複到指定索引的每個位置
# - 可以通過 `index` 參數顯式指定自定義索引，使數據更具語義化
# - 字符串索引使數據具有更好的可讀性和可檢索性，常用於分類數據

# %%
### 2.3 Series 的索引和切片

# %%
# 創建一個示例 Series
s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
print("示例 Series:")
print(s)

# 單個元素訪問
print(f"\ns['a']: {s['a']}")  # 通過標籤索引
print(f"s[0]: {s[0]}")      # 通過位置索引

# 多個元素訪問
print(f"\ns[['a', 'c', 'e']]:\n{s[['a', 'c', 'e']]}")  # 使用標籤列表

# 切片操作
print(f"\n使用位置切片 s[1:4]:\n{s[1:4]}")            # 位置切片
print(f"\n使用標籤切片 s['b':'d']:\n{s['b':'d']}")    # 標籤切片 (包含結束標籤)

# 條件過濾
print(f"\n條件過濾 s[s > 30]:\n{s[s > 30]}")

# %%
# 解說：
# - Series 提供了兩種索引方式：位置索引（整數）和標籤索引（用戶定義的索引值）
# - 使用方括號 `[]` 可以訪問單個元素，也可以傳入索引列表選擇多個元素
# - 位置切片 `s[1:4]` 不包含結束位置（類似 Python 列表），而標籤切片 `s['b':'d']` 包含結束標籤
# - 條件過濾返回滿足條件的元素子集，是數據分析中常用的強大功能
# - 這些靈活的索引方式使 Series 在數據處理時比普通列表或數組更加便捷

# %%
### 2.4 Series 基本運算

# %%
# 創建兩個 Series
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])

# 算術運算
print(f"s1 + s2:\n{s1 + s2}")
print(f"\ns1 * 2:\n{s1 * 2}")

# 帶有不同索引的 Series 運算
s3 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s4 = pd.Series([10, 20, 30, 40], index=['b', 'c', 'd', 'e'])

# 注意索引的自動對齊
print(f"\ns3 + s4:\n{s3 + s4}")  # a和e位置會變成NaN

# 統計方法
print(f"\ns1的總和: {s1.sum()}")
print(f"s1的平均值: {s1.mean()}")
print(f"s1的標準差: {s1.std()}")
print(f"s1的描述性統計:\n{s1.describe()}")

# 應用函數
print(f"\n將s1的每個元素平方:\n{s1.apply(lambda x: x**2)}")

# %%
# 解說：
# - Series 支持向量化運算，可以直接進行加減乘除等操作，無需循環迭代
# - 兩個 Series 運算時會自動按索引對齊，只有共同索引的數據參與計算
# - 不同索引的位置會產生 NaN（缺失值），這是 Pandas 的自動對齊機制
# - Series 提供豐富的統計方法（sum, mean, std 等）和描述性統計 (describe)
# - `.apply()` 方法允許對每個元素應用自定義函數，支持複雜的數據轉換
# - 這些特性使 Series 成為數據科學家處理單變量數據的首選工具

# %%
### 2.5 Series 缺失值處理

# %%
# 創建含有缺失值的 Series
s = pd.Series([1, np.nan, 3, None, 5])
print("含有缺失值的 Series:")
print(s)
print(f"是否有空值: {s.isna()}")
print(f"非空值的數量: {s.count()}")

# 處理缺失值
print(f"\n丟棄缺失值:\n{s.dropna()}")
print(f"\n填充缺失值為0:\n{s.fillna(0)}")
print(f"\n填充缺失值為前面的值:\n{s.fillna(method='ffill')}")
print(f"\n填充缺失值為後面的值:\n{s.fillna(method='bfill')}")

# 原始 Series 不變
print(f"\n原始 Series:\n{s}")

# %%
# 解說：
# - Pandas 將 `np.nan` 和 `None` 都視為缺失值，使用 `.isna()` 或 `.isnull()` 方法可檢測它們
# - `.count()` 返回非缺失值的數量，常用於計算有效數據比例
# - 處理缺失值的主要策略包括：
#   - 刪除：使用 `.dropna()` 移除含有缺失值的記錄
#   - 填充固定值：使用 `.fillna(值)` 將缺失值替換為特定值
#   - 前向填充：使用 `.fillna(method='ffill')` 用前一個有效值填充
#   - 後向填充：使用 `.fillna(method='bfill')` 用後一個有效值填充
# - 這些方法默認返回新的 Series，不會修改原始數據，除非指定 `inplace=True`
# - 缺失值處理是數據清洗中的關鍵步驟，選擇適當的策略取決於具體的數據背景

# %% [markdown]
# ## 3. Pandas DataFrame 介紹

# %% 
### 3.1 什麼是 DataFrame?

# %% 
# 學習要點：
# - DataFrame 是 Pandas 中的二維表格數據結構，類似於 Excel 工作表或 SQL 表格
# - DataFrame 由行和列組成，每一列可以看作是一個 Series
# - DataFrame 有行索引（index）和列標籤（columns）兩個軸

# %% [markdown]
# DataFrame 是 Pandas 中的一個二維標籤數據結構，類似於 Excel 電子表格或 SQL 表。
# 它由行和列組成，可以看作是由多個共享相同索引的 Series 組成的字典結構。
# DataFrame 是數據分析中最常用的數據結構，用於處理和分析表格數據。

# %%
# 創建一個簡單的 DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Boston', 'Chicago', 'Denver'],
    'Salary': [50000, 60000, 70000, 80000]
})

print("DataFrame 示例:")
print(df)

# 查看 DataFrame 的基本信息
print(f"\nDataFrame 形狀: {df.shape}")
print(f"DataFrame 列名: {df.columns}")
print(f"DataFrame 索引: {df.index}")
print(f"DataFrame 數據類型:\n{df.dtypes}")

# 查看數據摘要
print("\nDataFrame 頭部數據:")
print(df.head(2))
print("\nDataFrame 尾部數據:")
print(df.tail(2))
print("\nDataFrame 基本描述統計:")
print(df.describe())

# %%
# 解說：
# - DataFrame 是 Pandas 的核心數據結構，可視為由多個 Series 組成的二維表格
# - 每一列都是一個 Series，共享相同的索引（行標籤）
# - `.shape` 返回行數和列數，`.columns` 返回列名列表，`.index` 返回行索引
# - `.dtypes` 顯示每一列的數據類型，Pandas 自動推斷最佳類型
# - `.head()` 和 `.tail()` 用於快速查看數據的開頭和結尾部分，參數表示顯示的行數
# - `.describe()` 提供數值列的統計摘要，包括計數、平均值、標準差、最小值、四分位數和最大值
# - 這些方法使數據結構透明且易於探索，是數據分析的第一步

# %%
### 3.2 DataFrame 的創建方法

# %%
# 方法1: 從字典創建（字典的鍵作為列名）
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Boston', 'Chicago']
}
df1 = pd.DataFrame(data)
print("從字典創建 DataFrame:")
print(df1)

# 方法2: 從嵌套列表創建
data_list = [
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'Boston'],
    ['Charlie', 35, 'Chicago']
]
df2 = pd.DataFrame(data_list, columns=['Name', 'Age', 'City'])
print("\n從嵌套列表創建 DataFrame:")
print(df2)

# 方法3: 從字典列表創建
dict_list = [
    {'Name': 'Alice', 'Age': 25, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 30, 'City': 'Boston'},
    {'Name': 'Charlie', 'Age': 35, 'City': 'Chicago'}
]
df3 = pd.DataFrame(dict_list)
print("\n從字典列表創建 DataFrame:")
print(df3)

# 方法4: 從NumPy二維數組創建
arr = np.array([['Alice', 25, 'New York'],
                ['Bob', 30, 'Boston'],
                ['Charlie', 35, 'Chicago']])
df4 = pd.DataFrame(arr, columns=['Name', 'Age', 'City'])
print("\n從NumPy數組創建 DataFrame:")
print(df4)

# 方法5: 從Series創建
s1 = pd.Series(['Alice', 'Bob', 'Charlie'], name='Name')
s2 = pd.Series([25, 30, 35], name='Age')
s3 = pd.Series(['New York', 'Boston', 'Chicago'], name='City')
df5 = pd.DataFrame([s1, s2, s3]).T  # 轉置(T)使Series變為列
print("\n從Series創建 DataFrame:")
print(df5)

# %%
# 解說：
# - 從字典創建是最常用的方法，字典的鍵成為列名，值成為列數據
# - 從嵌套列表創建時，需要明確指定列名，否則使用數字索引
# - 從字典列表創建時，每個字典代表一行數據，鍵成為列名
# - 從NumPy數組創建時，數組的形狀決定DataFrame的形狀，通常需要指定列名
# - 從Series創建時，每個Series成為一行或一列，需要注意轉置(T)以得到預期的形狀
# - 創建DataFrame時可以指定索引(index)和列名(columns)，使數據更具語義化
# - 選擇合適的創建方法取決於數據的來源和格式，Pandas提供了靈活性來處理各種情況

# %%
### 3.3 DataFrame 的索引和切片

# %%
# 創建示例 DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 40, 45],
    'City': ['New York', 'Boston', 'Chicago', 'Denver', 'Miami'],
    'Salary': [50000, 60000, 70000, 80000, 90000],
    'Department': ['HR', 'IT', 'Finance', 'IT', 'Marketing']
})
print("示例 DataFrame:")
print(df)

# 1. 選擇列
print("\n選擇單列 (Series 格式):")
print(df['Name'])
print("\n選擇多列 (DataFrame 格式):")
print(df[['Name', 'Age']])

# 2. 選擇行 - 使用位置索引
print("\n使用 .iloc 選擇行 (基於位置):")
print(df.iloc[0])  # 第一行
print("\n選擇多行:")
print(df.iloc[1:3])  # 第二行到第三行

# 3. 選擇行 - 使用標籤索引
print("\n使用 .loc 選擇行 (基於標籤):")
print(df.loc[2])  # 索引為2的行
print("\n選擇多行:")
print(df.loc[1:3])  # 索引為1到3的行 (包含3)

# 4. 選擇行和列 (同時)
print("\n使用 .loc 選擇特定行和列:")
print(df.loc[1:3, ['Name', 'Salary']])  # 索引1到3的行，只選Name和Salary列

print("\n使用 .iloc 選擇特定行和列:")
print(df.iloc[1:3, [0, 3]])  # 第二行到第三行，第一列和第四列

# 5. 簡單條件選擇
print("\n條件選擇 - 選擇年齡大於35的記錄:")
print(df[df['Age'] > 35])

print("\n條件選擇 - 選擇在IT部門的記錄:")
print(df[df['Department'] == 'IT'])

print("\n複合條件 - 選擇年齡大於30且薪水大於70000的記錄:")
print(df[(df['Age'] > 30) & (df['Salary'] > 70000)])

# %%
# 解說：
# - DataFrame 提供多種索引和切片方式，適用於不同的數據選擇需求
# - 選擇列的方法：
#   - 單括號 `df['列名']` 返回單列作為 Series
#   - 雙括號 `df[['列名1', '列名2']]` 返回多列作為 DataFrame
# - 按位置選擇行的方法：
#   - `.iloc[i]` 選擇第 i 行（從0開始）
#   - `.iloc[i:j]` 選擇第 i 行到第 j-1 行（不包含j）
# - 按標籤選擇行的方法：
#   - `.loc[i]` 選擇索引為 i 的行
#   - `.loc[i:j]` 選擇索引從 i 到 j 的行（包含j）
# - 同時選擇行和列：
#   - `.loc[行範圍, 列範圍]` 使用標籤
#   - `.iloc[行範圍, 列範圍]` 使用位置
# - 這些靈活的選擇方法使 DataFrame 成為數據分析的強大工具

# %%
### 3.4 DataFrame 的基本操作

# %%
# 創建示例 DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Boston', 'Chicago']
})
print("原始 DataFrame:")
print(df)

# 1. 添加新列
df['Salary'] = [50000, 60000, 70000]  # 直接賦值
df['YearsEmployed'] = df['Age'] - 20  # 基於現有列計算
print("\n添加新列後的 DataFrame:")
print(df)

# 2. 刪除列
df_drop_col = df.drop('YearsEmployed', axis=1)  # axis=1表示列
print("\n刪除'YearsEmployed'列後的 DataFrame:")
print(df_drop_col)

# 3. 刪除行
df_drop_row = df.drop(1, axis=0)  # axis=0表示行，刪除索引為1的行
print("\n刪除索引為1的行後的 DataFrame:")
print(df_drop_row)

# 4. 重命名列
df_renamed = df.rename(columns={'Name': 'FullName', 'City': 'Location'})
print("\n重命名列後的 DataFrame:")
print(df_renamed)

# 5. 排序
df_sorted_by_age = df.sort_values('Age', ascending=False)  # 按年齡降序排列
print("\n按年齡降序排序後的 DataFrame:")
print(df_sorted_by_age)

# 6. 轉置
df_transposed = df.T  # 行和列互換
print("\n轉置後的 DataFrame:")
print(df_transposed)

# %%
# 解說：
# - 添加新列可以通過直接賦值或基於現有列的計算
# - 刪除操作使用 `drop()` 方法，需要指定 axis 參數（0表示行，1表示列）
# - 這些方法默認返回新的 DataFrame，不修改原始數據，除非指定 `inplace=True`
# - 重命名列使用 `rename()` 方法，傳入字典映射舊名稱到新名稱
# - 排序使用 `sort_values()` 方法，可以按單列或多列排序，控制升序或降序
# - 轉置操作使用 `.T` 屬性，將行和列互換，對於寬表格變長表格很有用
# - 這些基本操作為數據分析和預處理提供了豐富的工具集

# %% [markdown]
# ## 📋 5. 總結與最佳實踐

# %% [markdown]
# ### 5.1 Series 與 DataFrame 的核心概念

# %% [markdown]
# - **Series**: 一維標籤數組，索引-值對，類似於字典
# - **DataFrame**: 二維標籤數據結構，可以看作是共享索引的 Series 集合
# - 兩者都支持標籤索引和位置索引
# - 自動對齊和廣播機制使數據處理更加直覺和便捷

# %%
# 解說：
# - Series 適合處理單變量數據，如時間序列、一維測量結果或類別頻率
# - DataFrame 適合處理多變量數據，如表格數據、多特徵觀測或關係數據
# - 兩者的關鍵優勢是標籤索引、自動對齊和整合的數據處理方法
# - Series 可視為 DataFrame 的構建塊，許多 DataFrame 方法在 Series 上也適用
# - 這些數據結構的設計理念影響了現代數據分析工具的發展

# %% [markdown]
# ### 5.2 常用技巧

# %% [markdown]
# - 使用 `.loc[]` 和 `.iloc[]` 進行更精確的數據選擇
# - 充分利用條件過濾簡化複雜的數據篩選邏輯
# - 使用 `describe()` 快速了解數據的統計特性
# - 熟悉 Series 和 DataFrame 之間的互操作

# %%
# 解說：
# - `.loc[]` 和 `.iloc[]` 分別提供基於標籤和位置的精確索引，避免混淆和歧義
# - 條件過濾允許簡潔地表達選擇條件，例如 `df[df['Age'] > 30]`
# - `describe()` 提供快速統計概覽，幫助識別數據特徵和分布
# - 了解何時使用 Series 與 DataFrame，以及如何在兩者之間轉換，可以大大提高分析靈活性
# - 掌握這些技巧可以使代碼更簡潔、更高效，並提供更深入的數據洞察

# %% [markdown]
# ### 5.3 下一步學習

# %% [markdown]
# - 探索更多DataFrame和Series的選取方法
# - 學習處理缺失數據和數據類型轉換
# - 了解如何讀取和寫入不同格式的文件
# - 進階數據清洗和預處理技術
# - 數據分組和聚合操作

# %%
# 解說：
# - Pandas提供了豐富的數據處理功能，本課程只是入門
# - 隨著您的技能提升，可以探索更多Pandas的進階功能
# - 實際項目經驗是鞏固這些技能的最佳方式，建議結合真實數據集進行練習
# - 下一課我們將學習如何使用Pandas進行更詳細的數據選取和索引操作 