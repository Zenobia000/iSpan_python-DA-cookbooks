# %% 
# M2 Pandas 基礎練習

"""
本練習旨在幫助你鞏固 Pandas 基礎知識，包含了 DataFrame、Series、資料讀取、選取方法、
缺失值處理與資料型態轉換等內容。請完成以下練習題，加深對 Pandas 的理解與應用能力。

提示：每個練習題都有詳細的指引，請仔細閱讀後再作答。
若遇到困難，可參考提示或查閱相關文檔。
"""

# %%
## 環境設置

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 設定顯示選項
pd.set_option('display.max_rows', 10)  # 最多顯示10行
pd.set_option('display.max_columns', 10)  # 最多顯示10列
pd.set_option('display.width', 80)  # 顯示寬度
pd.set_option('display.precision', 2)  # 小數點位數

# %% [markdown]
# ## 練習 1: DataFrame 與 Series 基礎操作
# 
# 請完成以下練習，熟悉 Pandas 的核心數據結構。

# %%
# 1.1 創建 Series
# 提示: 使用 pd.Series() 函數創建一個包含 5 個不同水果名稱的 Series，設置索引為 1-5
# Series 基本語法: pd.Series(data, index=index)
fruits_list = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry']  # 水果列表
# 請完成以下代碼，將水果列表轉換為 Series，並設置索引為 1-5
fruits_series = pd.Series(fruits_list, index=[1, 2, 3, 4, 5])

print(f"水果 Series:\n{fruits_series}")
print(f"Series 的索引: {fruits_series.index}")
print(f"Series 的值: {fruits_series.values}")

# %%
# 1.2 創建 DataFrame
# 提示: 使用 pd.DataFrame() 函數創建一個包含學生資料的 DataFrame
# DataFrame 基本語法: pd.DataFrame(data, index=index, columns=columns)
# 請完成以下代碼，創建一個包含5名學生資料的 DataFrame，包含姓名、年齡、性別和科系欄位
students_data = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'Age': [20, 21, 19, 22, 20],
    'Gender': ['F', 'M', 'M', 'F', 'F'],
    'Major': ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology']
})

print("學生資料 DataFrame:")
print(students_data)

# %%
# 1.3 從字典創建 DataFrame
# 請完成以下代碼，創建一個產品資料字典，然後轉換為 DataFrame
# 字典應包含產品ID、名稱、價格和庫存四個欄位，至少有3個產品
products_dict = {
    'ID': [101, 102, 103],
    'Name': ['Product A', 'Product B', 'Product C'],
    'Price': [99.99, 149.99, 199.99],
    'Stock': [100, 75, 50]
}
# 將字典轉換為 DataFrame
products_df = pd.DataFrame(products_dict)

print("產品資料 DataFrame:")
print(products_df)

# %%
# 1.4 基本 DataFrame 操作
# 提示: 使用 students_data 進行基本操作

# 顯示 DataFrame 的基本信息
# 完成以下代碼 (使用 shape, columns, dtypes 等屬性)
print("DataFrame 的形狀 (列數, 行數): ")
print(students_data.shape)

print("DataFrame 的欄位名稱: ")
print(students_data.columns)

print("DataFrame 的數據類型: ")
print(students_data.dtypes)

# 顯示 DataFrame 的前 3 行和後 2 行
# 完成以下代碼 (使用 head 和 tail 方法)
print("\nDataFrame 的前 3 行:")
print(students_data.head(3))

print("\nDataFrame 的後 2 行:")
print(students_data.tail(2))

# 顯示 DataFrame 的統計摘要 (僅針對數值型欄位)
# 完成以下代碼 (使用 describe 方法)
print("\nDataFrame 的統計摘要:")
print(students_data.describe())

# %% [markdown]
# ## 練習 2: 檔案讀取與寫入
# 
# 請練習 Pandas 常見的檔案讀取與寫入功能。
# 為了練習，我們先創建一些測試資料。

# %%
# 2.1 創建和儲存 CSV 檔案
# 提示: 利用上面創建的 students_data DataFrame 儲存為 CSV 檔案
# 完成以下代碼
# 將 DataFrame 儲存為 CSV 檔案
students_data.to_csv('students_data.csv', index=False)

print("CSV 檔案已儲存")

# %%
# 2.2 讀取 CSV 檔案
# 提示: 使用 pd.read_csv() 函數讀取剛剛儲存的檔案
# 完成以下代碼
students_from_csv = pd.read_csv('students_data.csv')

print("從 CSV 讀取的資料:")
print(students_from_csv)

# %%
# 2.3 創建和處理 Excel 檔案
# 提示: 將 products_df 儲存為 Excel 檔案，然後讀取
# 首先需要確認是否安裝 openpyxl (pip install openpyxl)
# 完成以下代碼
try:
    # 將 DataFrame 儲存為 Excel 檔案
    products_df.to_excel('products_data.xlsx', index=False)

    print("Excel 檔案已儲存")
    
    # 讀取 Excel 檔案
    products_from_excel = pd.read_excel('products_data.xlsx')

    print("從 Excel 讀取的資料:")
    print(products_from_excel)
except Exception as e:
    print(f"Excel 操作失敗: {e}")
    print("請確認是否安裝 openpyxl 套件 (pip install openpyxl)")

# %%
# 2.4 處理不同格式的 CSV 檔案
# 提示: 創建一個自訂分隔符號的檔案，然後讀取
# 完成以下代碼

# 我們已經創建好一個 DataFrame 用於示範
custom_df = pd.DataFrame({
    'ID': [101, 102, 103],
    'Name': ['Product A', 'Product B', 'Product C'],
    'Price': [99.99, 149.99, 199.99]
})

# 儲存為分號分隔的 CSV 檔案
custom_df.to_csv('custom_data.csv', sep=';', index=False)

print("自訂分隔符號的 CSV 檔案已儲存")

# 讀取自訂分隔符號的 CSV 檔案
custom_from_csv = pd.read_csv('custom_data.csv', sep=';')

print("從自訂分隔符號的 CSV 讀取的資料:")
print(custom_from_csv)

# %% [markdown]
# ## 練習 3: 資料選取與篩選
# 
# 請練習 Pandas 的各種資料選取和篩選方法。

# %%
# 我們已經創建好一個較大的 DataFrame 用於資料選取練習
np.random.seed(42)  # 設定隨機種子以便結果可重現
employee_data = pd.DataFrame({
    'ID': range(1, 21),
    'Name': ['Emp' + str(i) for i in range(1, 21)],
    'Department': np.random.choice(['HR', 'IT', 'Finance', 'Marketing'], 20),
    'Salary': np.random.randint(30000, 100000, 20),
    'Age': np.random.randint(22, 60, 20),
    'Experience': np.random.randint(1, 30, 20),
    'Rating': np.random.uniform(1, 5, 20).round(1)
})

print("員工資料 DataFrame:")
print(employee_data)

# %%
# 3.1 基本欄位選取
# 提示: 使用不同方法選取 DataFrame 的欄位

# 使用中括號選取單一欄位 (返回 Series)
# 語法: df['column_name']
# 完成以下代碼
names_series = employee_data['Name']

print("使用中括號選取的 Name 欄位 (Series):")
print(names_series[:5])  # 只顯示前 5 項

# 使用點符號選取單一欄位 (返回 Series)
# 語法: df.column_name
# 注意: 僅當欄位名稱是有效的 Python 識別符時才能使用
# 完成以下代碼
dept_series = employee_data['Department']

print("\n使用點符號選取的 Department 欄位 (Series):")
print(dept_series[:5])  # 只顯示前 5 項

# 使用中括號選取多個欄位 (返回 DataFrame)
# 語法: df[['column1', 'column2', ...]]
# 完成以下代碼
selected_df = employee_data[['ID', 'Name', 'Salary']]

print("\n選取 ID、Name 和 Salary 欄位:")
print(selected_df.head())

# %%
# 3.2 使用 loc 和 iloc 選取資料
# 提示: 練習使用 loc (基於標籤) 和 iloc (基於位置) 進行資料選取

# 使用 loc 選取特定列和欄位
# 語法: df.loc[row_labels, column_labels]
# 完成以下代碼 (選取索引 5 到 10 的 Name 和 Salary 欄位)
loc_selection = employee_data.loc[5:10, ['Name', 'Salary']]

print("使用 loc 選取的資料:")
print(loc_selection)

# 使用 iloc 選取特定列和欄位
# 語法: df.iloc[row_positions, column_positions]
# 完成以下代碼 (選取前 5 列的第 0, 1, 3 欄)
iloc_selection = employee_data.iloc[:5, [0, 1, 3]]

print("\n使用 iloc 選取的資料:")
print(iloc_selection)

# %%
# 3.3 條件選取
# 提示: 使用布林表達式進行資料篩選

# 篩選薪資大於 80000 的員工
# 語法: df[df['column'] > value]
# 完成以下代碼
high_salary = employee_data[employee_data['Salary'] > 80000]

print("薪資高於 80000 的員工:")
print(high_salary)

# 篩選 IT 部門且年齡小於 30 的員工
# 語法: df[(condition1) & (condition2)]
# 提示: 使用 & 運算符組合條件，記得用括號括住每個條件
# 完成以下代碼
young_it = employee_data[(employee_data['Department'] == 'IT') & (employee_data['Age'] < 30)]

print("\nIT 部門且年齡小於 30 的員工:")
print(young_it)

# 篩選 Finance 或 HR 部門且評分高於 4 的員工
# 語法: df[(condition1 | condition2) & (condition3)]
# 提示: 使用 | 運算符表示或，使用 & 運算符表示且，記得正確使用括號
# 完成以下代碼
fin_hr_high_rating = employee_data[(employee_data['Department'].isin(['Finance', 'HR'])) & (employee_data['Rating'] > 4)]

print("\nFinance 或 HR 部門且評分高於 4 的員工:")
print(fin_hr_high_rating)

# %%
# 3.4 使用 query 方法進行篩選
# 提示: 使用 DataFrame 的 query 方法進行更易讀的篩選操作
# 語法: df.query('condition')
# 完成以下代碼 (篩選 Marketing 部門且經驗大於 10 年的員工)
experienced_marketing = employee_data[employee_data['Department'] == 'Marketing']

print("Marketing 部門且經驗大於 10 年的員工:")
print(experienced_marketing)

# %% [markdown]
# ## 練習 4: 缺失值處理
# 
# 請練習識別和處理 Pandas 中的缺失值。

# %%
# 我們已經創建好一個包含缺失值的 DataFrame
np.random.seed(42)
rows = 10
missing_data = pd.DataFrame({
    'A': np.random.choice([np.nan, 1, 2, 3, 4, 5], rows),
    'B': np.random.choice([np.nan, 10, 20, 30, 40, 50], rows),
    'C': np.random.choice([None, 'X', 'Y', 'Z'], rows),
    'D': np.random.choice([np.nan, 100, 200, 300], rows)
})

print("包含缺失值的 DataFrame:")
print(missing_data)

# %%
# 4.1 檢測缺失值
# 提示: 使用 isna(), isnull(), notna(), notnull() 方法檢測缺失值

# 檢測每個元素是否為缺失值
# 語法: df.isna() 或 df.isnull()
# 完成以下代碼
is_missing = missing_data.isna().any()

print("缺失值標記 (True 表示缺失):")
print(is_missing)

# 計算每列的缺失值數量
# 語法: df.isna().sum()
# 完成以下代碼
missing_counts = missing_data.isna().sum()

print("\n每列的缺失值數量:")
print(missing_counts)

# 計算每列的缺失值比例
# 語法: df.isna().mean()
# 完成以下代碼
missing_percentages = missing_data.isna().mean()

print("\n每列的缺失值比例:")
print(missing_percentages)

# %%
# 4.2 處理缺失值 - 刪除
# 提示: 使用 dropna() 方法刪除包含缺失值的行或列

# 刪除包含任何缺失值的行
# 語法: df.dropna()
# 完成以下代碼
drop_rows = missing_data.dropna()

print("刪除包含缺失值的行後:")
print(drop_rows)

# 刪除全部為缺失值的列
# 語法: df.dropna(axis=1, how='all')
# 完成以下代碼
drop_all_na_cols = missing_data.dropna(axis=1, how='all')

print("\n刪除全部為缺失值的列後:")
print(drop_all_na_cols)

# %%
# 4.3 處理缺失值 - 填充
# 提示: 使用 fillna() 方法填充缺失值

# 用固定值填充缺失值
# 語法: df.fillna(value)
# 完成以下代碼 (將缺失值填充為 0)
fill_fixed = missing_data.fillna(0)

print("用固定值填充後:")
print(fill_fixed)

# 使用前向填充 (forward fill)
# 語法: df.fillna(method='ffill') 或 df.ffill()
# 完成以下代碼
fill_forward = missing_data.ffill()

print("\n使用前向填充後:")
print(fill_forward)

# 使用後向填充 (backward fill)
# 語法: df.fillna(method='bfill') 或 df.bfill()
# 完成以下代碼
fill_backward = missing_data.bfill()

print("\n使用後向填充後:")
print(fill_backward)

# %%
# 4.4 處理缺失值 - 插值
# 已經創建好一個時間序列數據用於練習
dates = pd.date_range('2023-01-01', periods=10)
ts = pd.Series([10, 11, np.nan, 13, np.nan, np.nan, 16, 17, np.nan, 19], index=dates)
print("時間序列資料:")
print(ts)

# 使用線性插值填充缺失值
# 語法: series.interpolate() 或 series.interpolate(method='linear')
# 完成以下代碼
ts_interpolated = ts.interpolate()

print("\n使用線性插值後:")
print(ts_interpolated)

# 繪製原始數據和插值後的數據
plt.figure(figsize=(10, 6))
ts.plot(marker='o', linestyle='-', label='原始資料', color='blue')
ts_interpolated.plot(marker='o', linestyle='-', label='插值後', color='red')
plt.title('缺失值插值示例')
plt.legend()
plt.grid(True)
plt.tight_layout()

# %% [markdown]
# ## 練習 5: 資料型態轉換與處理
# 
# 請練習 Pandas 中的資料型態轉換與處理功能。

# %%
# 已經創建好一個包含不同資料型態的 DataFrame
data_types_df = pd.DataFrame({
    'Int_Col': [1, 2, 3, 4, 5],
    'Float_Col': [1.1, 2.2, 3.3, 4.4, 5.5],
    'Str_Col': ['A', 'B', 'C', 'D', 'E'],
    'Bool_Col': [True, False, True, False, True],
    'Date_Col': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'],
    'Cat_Col': ['Red', 'Green', 'Blue', 'Red', 'Green'],
    'Mixed_Col': ['1', '2', '3', '4', '5']
})

print("原始資料型態 DataFrame:")
print(data_types_df.dtypes)
print("\n資料預覽:")
print(data_types_df)

# %%
# 5.1 資料型態轉換
# 提示: 使用 astype() 方法進行資料型態轉換

# 將 Mixed_Col 轉換為整數型態
# 語法: df['column'].astype(dtype)
# 完成以下代碼
data_types_df['Mixed_Col_Int'] = data_types_df['Mixed_Col'].astype('int')

# 將 Cat_Col 轉換為類別型態
# 語法: df['column'].astype('category')
# 完成以下代碼
data_types_df['Cat_Col'] = data_types_df['Cat_Col'].astype('category')

# 將 Date_Col 轉換為日期型態
# 語法: pd.to_datetime(df['column'])
# 完成以下代碼
data_types_df['Date_Col'] = pd.to_datetime(data_types_df['Date_Col'])

print("轉換後的資料型態:")
print(data_types_df.dtypes)
print("\n轉換後的資料預覽:")
print(data_types_df)

# %%
# 5.2 處理數值資料
# 提示: 練習數值資料的轉換與操作

# 四捨五入到指定小數位數
# 語法: series.round(decimals)
# 完成以下代碼 (將 Float_Col 四捨五入到 1 位小數)
rounded = data_types_df['Float_Col'].round(1)

print("四捨五入到 1 位小數:")
print(rounded)

# 加上百分比符號
# 提示: 先將數值乘以 100，再轉換為字串，然後加上 '%'
# 完成以下代碼
percentage = (data_types_df['Float_Col'] * 100).astype('str') + '%'

print("\n百分比表示:")
print(percentage)

# %%
# 5.3 日期時間處理
# 提示: 練習日期時間的處理和操作
# 完成以下代碼

# 從 Date_Col 提取年、月、日
# 語法: df['column'].dt.year, df['column'].dt.month, df['column'].dt.day
data_types_df['Year'] = data_types_df['Date_Col'].dt.year
data_types_df['Month'] = data_types_df['Date_Col'].dt.month
data_types_df['Day'] = data_types_df['Date_Col'].dt.day

# 計算與現在的天數差
# 提示: 使用 datetime 模組和 dt 屬性計算日期差
from datetime import datetime
today = pd.Timestamp(datetime.now().date())
data_types_df['Days_From_Today'] = (today - data_types_df['Date_Col'].dt.date).dt.days

print("日期時間處理結果:")
print(data_types_df[['Date_Col', 'Year', 'Month', 'Day', 'Days_From_Today']])

# %%
# 5.4 字串處理
# 提示: 使用 str 存取器處理字串欄位

# 將 Str_Col 轉換為小寫
# 語法: df['column'].str.lower()
# 完成以下代碼
data_types_df['Str_Col_Lower'] = data_types_df['Str_Col'].str.lower()

# 將 Str_Col 與另一個字串連接
# 語法: df['column'] + string
# 完成以下代碼
data_types_df['Str_Col_Concat'] = data_types_df['Str_Col'] + ' - ' + data_types_df['Str_Col_Lower']

print("字串處理結果:")
print(data_types_df[['Str_Col', 'Str_Col_Lower', 'Str_Col_Concat']])

# %% [markdown]
# ## 練習 6: 綜合應用 - 資料分析
# 
# 請使用前面學到的知識，進行一個簡單的資料分析。

# %%
# 已經創建好一個銷售資料 DataFrame 用於綜合練習
np.random.seed(42)
sales_data = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=100, freq='D'),
    'Product': np.random.choice(['A', 'B', 'C', 'D'], 100),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
    'Sales': np.random.randint(10, 1000, 100),
    'Units': np.random.randint(1, 50, 100),
    'Returns': np.random.randint(0, 10, 100)
})

# 插入一些缺失值
sales_data.loc[np.random.choice(sales_data.index, 10), 'Sales'] = np.nan
sales_data.loc[np.random.choice(sales_data.index, 10), 'Units'] = np.nan

print("銷售資料 DataFrame:")
print(sales_data.head())
print(f"\n資料形狀: {sales_data.shape}")
print(f"資料型態:\n{sales_data.dtypes}")

# %%
# 6.1 資料檢查與清洗
# 提示: 檢查並處理缺失值，必要時進行資料型態轉換

# 檢查缺失值
# 語法: df.isna().sum()
# 完成以下代碼
missing_values = sales_data.isna().sum()

print("缺失值總結:")
print(missing_values)

# 處理缺失值 (使用適當的方法)
# 可以使用多種方法：dropna(), fillna(), interpolate() 等
# 完成以下代碼
sales_data_clean = sales_data.dropna()

print("\n清洗後的缺失值總結:")
print(sales_data_clean.isna().sum())

# %%
# 6.2 基本統計分析
# 提示: 進行基本的探索性資料分析

# 計算每個產品的銷售統計
# 語法: df.groupby('column').agg({'column': function})
# 完成以下代碼
product_stats = sales_data_clean.groupby('Product').agg({'Sales': 'sum', 'Units': 'sum', 'Returns': 'sum'})

print("每個產品的銷售統計:")
print(product_stats)

# 計算每個區域的銷售統計
# 完成以下代碼
region_stats = sales_data_clean.groupby('Region').agg({'Sales': 'sum', 'Units': 'sum', 'Returns': 'sum'})

print("\n每個區域的銷售統計:")
print(region_stats)

# 計算每月的銷售統計
# 提示: 先創建一個月份欄位，然後按月份分組
# 完成以下代碼
sales_data_clean['Month'] = sales_data_clean['Date'].dt.strftime('%Y-%m-%d').dt.strftime('%m')
monthly_stats = sales_data_clean.groupby('Month').agg({'Sales': 'sum', 'Units': 'sum', 'Returns': 'sum'})

print("\n每月的銷售統計:")
print(monthly_stats)

# %%
# 6.3 資料視覺化
# 提示: 使用 matplotlib 或 pandas 內建的繪圖功能進行視覺化

# 繪製每個產品的總銷售額條形圖
# 完成以下代碼
plt.figure(figsize=(10, 6))
product_sales = sales_data_clean.groupby('Product')['Sales'].sum()
product_sales.plot(kind='bar')
plt.title('產品銷售總額')
plt.xlabel('產品')
plt.ylabel('銷售總額')
plt.grid(axis='y')
plt.tight_layout()

# 繪製每月銷售趨勢線圖
# 完成以下代碼
plt.figure(figsize=(12, 6))
monthly_sales = sales_data_clean.groupby('Date').sum()['Sales']
monthly_sales.plot(marker='o')
plt.title('每月銷售趨勢')
plt.xlabel('月份')
plt.ylabel('銷售總額')
plt.grid(True)
plt.tight_layout()

# %%
# 6.4 資料分析與解讀
# 提示: 分析資料並提出見解

# 計算退貨率 (Returns/Units)
# 完成以下代碼
sales_data_clean['Return_Rate'] = sales_data_clean['Returns'] / sales_data_clean['Units']

# 找出退貨率最高的產品和區域
# 完成以下代碼
product_return_rate = sales_data_clean.groupby('Product')['Return_Rate'].mean()
region_return_rate = sales_data_clean.groupby('Region')['Return_Rate'].mean()

print("產品退貨率:")
print(product_return_rate)
print("\n區域退貨率:")
print(region_return_rate)

# 找出銷售表現最好和最差的區域產品組合
# 完成以下代碼
region_product_sales = sales_data_clean.groupby(['Region', 'Product']).agg({'Sales': 'sum', 'Returns': 'sum'})
region_product_sales = region_product_sales.reset_index().sort_values(by=['Region', 'Sales'], ascending=[True, False])

print("\n區域-產品銷售表現:")
print(region_product_sales)

# %% [markdown]
# ## 挑戰題 (選做)

# %%
# 挑戰 1: 資料透視表 (Pivot Table)
# 提示: 使用 pivot_table 建立銷售資料的多維度分析
# 語法: pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc)
# 完成以下代碼 (分析每個區域、產品的平均銷售額和總銷售額)
sales_pivot = sales_data_clean.pivot_table(index='Region', columns='Product', values='Sales', aggfunc='sum')

print("銷售資料透視表:")
print(sales_pivot)

# %%
# 挑戰 2: 時間序列分析
# 提示: 對銷售數據進行重採樣 (Resampling) 和移動平均 (Rolling Mean) 分析
# 完成以下代碼

# 按週重採樣，計算每週總銷售額
# 提示: 首先需要將 Date 列設為索引，然後使用 resample 方法
# 語法: df.set_index('Date').resample('W').sum()
weekly_sales = sales_data_clean.resample('W').sum()

print("每週銷售總額:")
print(weekly_sales.head())

# 計算 7 天移動平均
# 語法: series.rolling(window=7).mean()
rolling_mean = sales_data_clean['Sales'].rolling(window=7).mean()

# 繪製原始資料和移動平均
plt.figure(figsize=(12, 6))
daily_sales = sales_data_clean['Sales']
daily_sales.plot(alpha=0.5, label='每日銷售')
rolling_mean.plot(label='7天移動平均', linewidth=2)
plt.title('每日銷售與7天移動平均')
plt.legend()
plt.grid(True)
plt.tight_layout() 