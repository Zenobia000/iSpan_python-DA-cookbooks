# %% 
# M2 Pandas 基礎練習解答

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

# %%
# 1.1 創建 Series
fruits_series = pd.Series(['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'], index=[1, 2, 3, 4, 5])

print(f"水果 Series:\n{fruits_series}")
print(f"Series 的索引: {fruits_series.index}")
print(f"Series 的值: {fruits_series.values}")

# %%
# 1.2 創建 DataFrame
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
products_dict = {
    'ID': [101, 102, 103],
    'Name': ['Product A', 'Product B', 'Product C'],
    'Price': [99.99, 149.99, 199.99],
    'Stock': [100, 75, 50]
}
products_df = pd.DataFrame(products_dict)

print("產品資料 DataFrame:")
print(products_df)

# %%
# 1.4 基本 DataFrame 操作

# 顯示 DataFrame 的基本信息
print("DataFrame 的形狀 (列數, 行數): ")
print(students_data.shape)
print("DataFrame 的欄位名稱: ")
print(students_data.columns)
print("DataFrame 的數據類型: ")
print(students_data.dtypes)

# 顯示 DataFrame 的前 3 行和後 2 行
print("\nDataFrame 的前 3 行:")
print(students_data.head(3))

print("\nDataFrame 的後 2 行:")
print(students_data.tail(2))

# 顯示 DataFrame 的統計摘要 (僅針對數值型欄位)
print("\nDataFrame 的統計摘要:")
print(students_data.describe())

# %% [markdown]
# ## 練習 2: 檔案讀取與寫入

# %%
# 2.1 創建和儲存 CSV 檔案
# 將 DataFrame 儲存為 CSV 檔案
students_data.to_csv('students_data.csv', index=False)

print("CSV 檔案已儲存")

# %%
# 2.2 讀取 CSV 檔案
students_from_csv = pd.read_csv('students_data.csv')

print("從 CSV 讀取的資料:")
print(students_from_csv)

# %%
# 2.3 創建和處理 Excel 檔案
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
# 創建一個使用分號分隔的 CSV 檔案
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

# %%
# 3.1 創建測試資料
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
# 3.2 基本欄位選取

# 使用中括號選取單一欄位 (返回 Series)
names_series = employee_data['Name']

print("使用中括號選取的 Name 欄位 (Series):")
print(names_series[:5])  # 只顯示前 5 項

# 使用點符號選取單一欄位 (返回 Series)
dept_series = employee_data.Department

print("\n使用點符號選取的 Department 欄位 (Series):")
print(dept_series[:5])  # 只顯示前 5 項

# 使用中括號選取多個欄位 (返回 DataFrame)
selected_df = employee_data[['ID', 'Name', 'Salary']]

print("\n選取 ID、Name 和 Salary 欄位:")
print(selected_df.head())

# %%
# 3.3 使用 loc 和 iloc 選取資料

# 使用 loc 選取特定列和欄位
loc_selection = employee_data.loc[5:10, ['Name', 'Salary']]

print("使用 loc 選取的資料:")
print(loc_selection)

# 使用 iloc 選取特定列和欄位
iloc_selection = employee_data.iloc[:5, [0, 1, 3]]

print("\n使用 iloc 選取的資料:")
print(iloc_selection)

# %%
# 3.4 條件選取

# 篩選薪資大於 80000 的員工
high_salary = employee_data[employee_data['Salary'] > 80000]

print("薪資高於 80000 的員工:")
print(high_salary)

# 篩選 IT 部門且年齡小於 30 的員工
young_it = employee_data[(employee_data['Department'] == 'IT') & (employee_data['Age'] < 30)]

print("\nIT 部門且年齡小於 30 的員工:")
print(young_it)

# 篩選 Finance 或 HR 部門且評分高於 4 的員工
fin_hr_high_rating = employee_data[(employee_data['Department'].isin(['Finance', 'HR'])) & (employee_data['Rating'] > 4)]

print("\nFinance 或 HR 部門且評分高於 4 的員工:")
print(fin_hr_high_rating)

# %%
# 3.5 使用 query 方法進行篩選
experienced_marketing = employee_data.query("Department == 'Marketing' and Experience > 10")

print("Marketing 部門且經驗大於 10 年的員工:")
print(experienced_marketing)

# %% [markdown]
# ## 練習 4: 缺失值處理

# %%
# 4.1 創建包含缺失值的資料
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
# 4.2 檢測缺失值

# 檢測每個元素是否為缺失值
is_missing = missing_data.isna()

print("缺失值標記 (True 表示缺失):")
print(is_missing)

# 計算每列的缺失值數量
missing_counts = missing_data.isna().sum()

print("\n每列的缺失值數量:")
print(missing_counts)

# 計算每列的缺失值比例
missing_percentages = missing_data.isna().mean() * 100

print("\n每列的缺失值比例:")
print(missing_percentages)

# %%
# 4.3 處理缺失值 - 刪除

# 刪除包含任何缺失值的行
drop_rows = missing_data.dropna()

print("刪除包含缺失值的行後:")
print(drop_rows)

# 刪除全部為缺失值的列
drop_all_na_cols = missing_data.dropna(axis=1, how='all')

print("\n刪除全部為缺失值的列後:")
print(drop_all_na_cols)

# %%
# 4.4 處理缺失值 - 填充

# 用固定值填充缺失值
fill_fixed = missing_data.fillna({'A': 0, 'B': 0, 'C': 'Missing', 'D': 0})

print("用固定值填充後:")
print(fill_fixed)

# 使用前向填充 (forward fill)
fill_forward = missing_data.fillna(method='ffill')

print("\n使用前向填充後:")
print(fill_forward)

# 使用後向填充 (backward fill)
fill_backward = missing_data.fillna(method='bfill')

print("\n使用後向填充後:")
print(fill_backward)

# %%
# 4.5 處理缺失值 - 插值
# 創建一個新的時間序列數據
dates = pd.date_range('2023-01-01', periods=10)
ts = pd.Series([10, 11, np.nan, 13, np.nan, np.nan, 16, 17, np.nan, 19], index=dates)
print("時間序列資料:")
print(ts)

# 使用線性插值填充缺失值
ts_interpolated = ts.interpolate(method='linear')

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

# %%
# 5.1 創建包含不同資料型態的 DataFrame
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
# 5.2 資料型態轉換

# 將 Mixed_Col 轉換為整數型態
data_types_df['Mixed_Col_Int'] = data_types_df['Mixed_Col'].astype(int)

# 將 Cat_Col 轉換為類別型態
data_types_df['Cat_Col'] = data_types_df['Cat_Col'].astype('category')

# 將 Date_Col 轉換為日期型態
data_types_df['Date_Col'] = pd.to_datetime(data_types_df['Date_Col'])

print("轉換後的資料型態:")
print(data_types_df.dtypes)
print("\n轉換後的資料預覽:")
print(data_types_df)

# %%
# 5.3 處理數值資料

# 四捨五入到指定小數位數
rounded = data_types_df['Float_Col'].round(1)

print("四捨五入到 1 位小數:")
print(rounded)

# 加上百分比符號
percentage = (data_types_df['Float_Col'] * 100).round(1).astype(str) + '%'

print("\n百分比表示:")
print(percentage)

# %%
# 5.4 日期時間處理

# 從 Date_Col 提取年、月、日
data_types_df['Year'] = data_types_df['Date_Col'].dt.year
data_types_df['Month'] = data_types_df['Date_Col'].dt.month
data_types_df['Day'] = data_types_df['Date_Col'].dt.day

# 計算與現在的天數差
from datetime import datetime
today = pd.Timestamp(datetime.now().date())
data_types_df['Days_From_Today'] = (today - data_types_df['Date_Col']).dt.days

print("日期時間處理結果:")
print(data_types_df[['Date_Col', 'Year', 'Month', 'Day', 'Days_From_Today']])

# %%
# 5.5 字串處理

# 將 Str_Col 轉換為小寫
data_types_df['Str_Col_Lower'] = data_types_df['Str_Col'].str.lower()

# 將 Str_Col 與另一個字串連接
data_types_df['Str_Col_Concat'] = data_types_df['Str_Col'] + ' - ' + data_types_df['Str_Col_Lower']

print("字串處理結果:")
print(data_types_df[['Str_Col', 'Str_Col_Lower', 'Str_Col_Concat']])

# %% [markdown]
# ## 練習 6: 綜合應用 - 資料分析

# %%
# 6.1 創建銷售資料
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
# 6.2 資料檢查與清洗

# 檢查缺失值
missing_values = sales_data.isna().sum()

print("缺失值總結:")
print(missing_values)

# 處理缺失值 (使用適當的方法)
sales_data_clean = sales_data.fillna(sales_data.median())

print("\n清洗後的缺失值總結:")
print(sales_data_clean.isna().sum())

# %%
# 6.3 基本統計分析

# 計算每個產品的銷售統計
product_stats = sales_data_clean.groupby('Product').agg({
    'Sales': ['sum', 'mean', 'std'],
    'Units': ['sum', 'mean'],
    'Returns': ['sum', 'mean']
})

print("每個產品的銷售統計:")
print(product_stats)

# 計算每個區域的銷售統計
region_stats = sales_data_clean.groupby('Region').agg({
    'Sales': ['sum', 'mean', 'std'],
    'Units': ['sum', 'mean'],
    'Returns': ['sum', 'mean']
})

print("\n每個區域的銷售統計:")
print(region_stats)

# 計算每月的銷售統計
sales_data_clean['Month'] = sales_data_clean['Date'].dt.strftime('%Y-%m')
monthly_stats = sales_data_clean.groupby('Month').agg({
    'Sales': ['sum', 'mean', 'count'],
    'Units': ['sum', 'mean'],
    'Returns': ['sum', 'mean']
})

print("\n每月的銷售統計:")
print(monthly_stats)

# %%
# 6.4 資料視覺化

# 繪製每個產品的總銷售額條形圖
plt.figure(figsize=(10, 6))
product_sales = sales_data_clean.groupby('Product')['Sales'].sum()
product_sales.plot(kind='bar', color='skyblue')
plt.title('產品銷售總額', fontsize=14)
plt.xlabel('產品', fontsize=12)
plt.ylabel('銷售總額', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.xticks(rotation=0)
plt.tight_layout()

# 繪製每月銷售趨勢線圖
plt.figure(figsize=(12, 6))
monthly_sales = sales_data_clean.groupby(sales_data_clean['Date'].dt.strftime('%Y-%m'))['Sales'].sum()
monthly_sales.plot(marker='o', linestyle='-', color='green')
plt.title('每月銷售趨勢', fontsize=14)
plt.xlabel('月份', fontsize=12)
plt.ylabel('銷售總額', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# %%
# 6.5 資料分析與解讀

# 計算退貨率 (Returns/Units)
sales_data_clean['Return_Rate'] = sales_data_clean['Returns'] / sales_data_clean['Units']

# 找出退貨率最高的產品和區域
product_return_rate = sales_data_clean.groupby('Product')['Return_Rate'].mean().sort_values(ascending=False)
region_return_rate = sales_data_clean.groupby('Region')['Return_Rate'].mean().sort_values(ascending=False)

print("產品退貨率 (從高到低):")
print(product_return_rate)
print("\n區域退貨率 (從高到低):")
print(region_return_rate)

# 找出銷售表現最好和最差的區域產品組合
region_product_sales = sales_data_clean.groupby(['Region', 'Product'])['Sales'].sum().reset_index()
# 最好的組合
best_combo = region_product_sales.sort_values('Sales', ascending=False).head(3)
# 最差的組合
worst_combo = region_product_sales.sort_values('Sales').head(3)

print("\n銷售表現最好的區域-產品組合:")
print(best_combo)
print("\n銷售表現最差的區域-產品組合:")
print(worst_combo)

# %% [markdown]
# ## 挑戰題 (選做)

# %%
# 挑戰 1: 資料透視表 (Pivot Table)
sales_pivot = pd.pivot_table(
    sales_data_clean, 
    values='Sales', 
    index='Region', 
    columns='Product',
    aggfunc=['sum', 'mean']
)

print("銷售資料透視表:")
print(sales_pivot)

# 更簡潔的透視表 - 只顯示總和
sales_pivot_simple = pd.pivot_table(
    sales_data_clean, 
    values='Sales', 
    index='Region', 
    columns='Product',
    aggfunc='sum'
)

print("\n簡化的銷售資料透視表 (僅總和):")
print(sales_pivot_simple)

# %%
# 挑戰 2: 時間序列分析

# 設置日期為索引
time_series_data = sales_data_clean.set_index('Date')

# 按週重採樣，計算每週總銷售額
weekly_sales = time_series_data.resample('W')['Sales'].sum()

print("每週銷售總額:")
print(weekly_sales.head())

# 計算 7 天移動平均
rolling_mean = time_series_data['Sales'].rolling(window=7).mean()

# 繪製原始資料和移動平均
plt.figure(figsize=(14, 7))
time_series_data['Sales'].plot(alpha=0.5, label='每日銷售', color='gray')
rolling_mean.plot(label='7天移動平均', linewidth=2, color='crimson')
plt.title('每日銷售與7天移動平均', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('銷售額', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 繪製按月和按週的銷售比較
plt.figure(figsize=(14, 7))

# 按月重採樣
monthly_sales = time_series_data.resample('M')['Sales'].sum()
monthly_sales.plot(label='月度銷售總額', marker='o', linestyle='-', color='blue')

# 按週重採樣 (已計算)
weekly_sales.plot(label='週度銷售總額', marker='.', linestyle='--', color='green', alpha=0.7)

plt.title('月度與週度銷售額比較', fontsize=14)
plt.xlabel('日期', fontsize=12)
plt.ylabel('銷售總額', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout() 