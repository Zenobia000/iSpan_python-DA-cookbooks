# %% [markdown]
# # 📘 M3 Pandas 進階應用 - 練習題
# 
# 本練習將幫助您鞏固 Pandas 進階模組中學到的知識，包括條件篩選、分組聚合、樞紐表與交叉表、數據合併以及時間序列分析等技術。

# %% [markdown]
# ## 🧰 環境設置

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 100)
pd.set_option('display.precision', 2)

# 設置隨機種子確保結果可重現
np.random.seed(42)

# %% [markdown]
# ## 📊 練習資料準備
# 
# 我們將使用一個模擬的電子商務數據集進行練習。

# %%
# 創建日期範圍
dates = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')

# 創建訂單數據
n_orders = 5000
order_data = {
    'order_id': np.arange(1, n_orders + 1),
    'order_date': np.random.choice(dates, n_orders),
    'customer_id': np.random.randint(1, 501, n_orders),
    'product_id': np.random.randint(1, 101, n_orders),
    'quantity': np.random.randint(1, 10, n_orders),
    'unit_price': np.random.uniform(10, 1000, n_orders).round(2),
    'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'], n_orders),
    'shipping_method': np.random.choice(['Standard', 'Express', 'Next Day'], n_orders, p=[0.7, 0.2, 0.1]),
    'order_status': np.random.choice(['Completed', 'Shipped', 'Processing', 'Cancelled'], n_orders, p=[0.8, 0.1, 0.05, 0.05])
}

# 創建訂單 DataFrame
orders_df = pd.DataFrame(order_data)

# 計算訂單總金額
orders_df['total_amount'] = orders_df['quantity'] * orders_df['unit_price']

# 創建客戶數據
n_customers = 500
customer_data = {
    'customer_id': np.arange(1, n_customers + 1),
    'customer_name': [f'Customer_{i}' for i in range(1, n_customers + 1)],
    'customer_segment': np.random.choice(['Retail', 'Wholesale', 'Online'], n_customers, p=[0.6, 0.3, 0.1]),
    'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia', 'Japan'], n_customers),
    'join_date': pd.date_range(start='2020-01-01', periods=n_customers)
}

# 創建客戶 DataFrame
customers_df = pd.DataFrame(customer_data)

# 創建產品數據
n_products = 100
product_data = {
    'product_id': np.arange(1, n_products + 1),
    'product_name': [f'Product_{i}' for i in range(1, n_products + 1)],
    'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], n_products),
    'supplier_id': np.random.randint(1, 21, n_products),
    'stock_quantity': np.random.randint(0, 1000, n_products)
}

# 創建產品 DataFrame
products_df = pd.DataFrame(product_data)

# 顯示數據預覽
print("訂單數據預覽:")
print(orders_df.head())
print("\n客戶數據預覽:")
print(customers_df.head())
print("\n產品數據預覽:")
print(products_df.head())

# %% [markdown]
# ## 🔍 練習 1: 進階條件篩選
# 
# 使用 M3.1 中學到的進階條件篩選技術完成以下任務。

# %% [markdown]
# ### 1.1 使用複雜條件組合
# 
# 篩選出符合以下條件的訂單:
# - 訂單金額大於 500 或數量大於 5
# - 支付方式為 "Credit Card" 或 "PayPal"
# - 訂單狀態不是 "Cancelled"

# %%
# 在此編寫您的代碼
filtered_orders = None  # 替換為您的篩選代碼

# 顯示結果
print(f"符合條件的訂單數量: {len(filtered_orders)}")
print(filtered_orders.head())

# %% [markdown]
# ### 1.2 使用 query() 方法
# 
# 使用 query() 方法篩選出:
# - 2022年第一季度 (1-3月)
# - "Electronics" 類別的產品
# - 訂單金額大於 1000
# 
# 提示: 您需要先合併訂單和產品數據。

# %%
# 在此編寫您的代碼
# 1. 合併訂單和產品數據
merged_data = None  # 替換為您的合併代碼

# 2. 使用 query() 進行篩選
q1_electronics = None  # 替換為您的篩選代碼

# 顯示結果
print(f"符合條件的訂單數量: {len(q1_electronics)}")
print(q1_electronics.head())

# %% [markdown]
# ### 1.3 使用字符串方法和正則表達式
# 
# 找出客戶名稱中包含數字 "5" 的客戶，並顯示他們的訂單總數和總金額。

# %%
# 在此編寫您的代碼
customers_with_5 = None  # 替換為您的篩選代碼

# 合併客戶和訂單數據
customer_orders = None  # 替換為您的合併和聚合代碼

# 顯示結果
print(f"名稱中包含數字5的客戶數量: {len(customers_with_5)}")
print(customer_orders.head())

# %% [markdown]
# ## 🔄 練習 2: 分組與聚合進階應用
# 
# 使用 M3.2 中學到的分組與聚合技術完成以下任務。

# %% [markdown]
# ### 2.1 多種聚合函數組合
# 
# 按產品類別分組，計算以下指標:
# - 訂單總數
# - 總銷售金額
# - 平均訂單金額
# - 最大和最小訂單金額
# - 訂單金額的標準差

# %%
# 在此編寫您的代碼
# 合併訂單和產品數據
merged_data = None  # 替換為您的合併代碼

# 按類別分組並計算多種聚合指標
category_stats = None  # 替換為您的分組聚合代碼

# 顯示結果
print(category_stats)

# %% [markdown]
# ### 2.2 使用 transform 進行組內標準化
# 
# 對每個產品類別內的訂單金額進行標準化，計算:
# - 每筆訂單金額與該類別平均訂單金額的差異百分比
# - 每筆訂單金額在該類別中的百分位數

# %%
# 在此編寫您的代碼
# 合併訂單和產品數據
merged_data = None  # 替換為您的合併代碼

# 使用 transform 進行組內標準化
merged_data['category_avg'] = None  # 替換為您的 transform 代碼
merged_data['diff_from_avg_pct'] = None  # 替換為您的計算代碼

# 計算組內百分位數
merged_data['category_percentile'] = None  # 替換為您的百分位數計算代碼

# 顯示結果
print(merged_data[['category', 'total_amount', 'category_avg', 'diff_from_avg_pct', 'category_percentile']].head(10))

# %% [markdown]
# ### 2.3 使用 apply 進行複雜的組內操作
# 
# 對每個客戶，找出他們購買金額最高的前3個訂單，並計算這些訂單佔該客戶總消費的百分比。

# %%
# 在此編寫您的代碼
# 定義一個函數來找出每個客戶的前3個訂單
def top_orders(group):
    # 在此編寫您的函數內容
    pass

# 應用函數到每個客戶組
top_customer_orders = None  # 替換為您的 apply 代碼

# 顯示結果
print(top_customer_orders.head(10))

# %% [markdown]
# ## 📊 練習 3: 樞紐表與交叉表
# 
# 使用 M3.3 中學到的樞紐表與交叉表技術完成以下任務。

# %% [markdown]
# ### 3.1 創建多層次樞紐表
# 
# 創建一個樞紐表，顯示:
# - 行: 產品類別和支付方式
# - 列: 訂單月份和訂單狀態
# - 值: 訂單總金額(總和)和訂單數量(計數)

# %%
# 在此編寫您的代碼
# 準備數據
merged_data = None  # 替換為您的合併代碼
merged_data['order_month'] = None  # 提取訂單月份

# 創建多層次樞紐表
pivot_table = None  # 替換為您的樞紐表代碼

# 顯示結果
print(pivot_table.head())

# %% [markdown]
# ### 3.2 使用交叉表分析類別關係
# 
# 創建一個交叉表，分析:
# - 不同產品類別在不同國家的銷售分布
# - 計算每個類別在每個國家的銷售佔比 (normalize)
# - 添加邊際總計

# %%
# 在此編寫您的代碼
# 準備數據
merged_data = None  # 替換為您的合併代碼

# 創建交叉表
cross_tab = None  # 替換為您的交叉表代碼

# 顯示結果
print(cross_tab)

# %% [markdown]
# ### 3.3 使用 stack 和 unstack 重塑數據
# 
# 對練習 3.1 中創建的樞紐表:
# - 使用 stack 將月份層級轉為行
# - 然後使用 unstack 將訂單狀態轉為列
# - 最後重置索引得到一個扁平的表格

# %%
# 在此編寫您的代碼
# 使用 stack 和 unstack 重塑數據
reshaped_data = None  # 替換為您的重塑代碼

# 重置索引
flat_data = None  # 替換為您的重置索引代碼

# 顯示結果
print(flat_data.head())

# %% [markdown]
# ## 🔄 練習 4: 數據合併與連接
# 
# 使用 M3.4 中學到的數據合併技術完成以下任務。

# %% [markdown]
# ### 4.1 多表連接創建完整視圖
# 
# 創建一個完整的訂單視圖，包含:
# - 訂單信息
# - 客戶信息
# - 產品信息
# 
# 確保使用正確的連接類型，並處理可能的重複列名。

# %%
# 在此編寫您的代碼
# 連接訂單和客戶
order_customer = None  # 替換為您的合併代碼

# 連接訂單客戶和產品
complete_view = None  # 替換為您的合併代碼

# 顯示結果
print(f"完整視圖的列: {complete_view.columns.tolist()}")
print(f"完整視圖的行數: {len(complete_view)}")
print(complete_view.head())

# %% [markdown]
# ### 4.2 使用不同的合併方法比較結果
# 
# 比較不同合併方法 (inner, left, right, outer) 在合併訂單和產品數據時的結果差異。
# 
# 提示: 為了展示差異，先創建一些沒有對應訂單的產品和沒有對應產品的訂單。

# %%
# 在此編寫您的代碼
# 創建一些沒有對應訂單的產品
missing_products = None  # 替換為您的代碼

# 創建一些沒有對應產品的訂單
missing_orders = None  # 替換為您的代碼

# 比較不同合併方法
inner_join = None  # 替換為您的內連接代碼
left_join = None  # 替換為您的左連接代碼
right_join = None  # 替換為您的右連接代碼
outer_join = None  # 替換為您的外連接代碼

# 顯示結果比較
print(f"Inner Join 行數: {len(inner_join)}")
print(f"Left Join 行數: {len(left_join)}")
print(f"Right Join 行數: {len(right_join)}")
print(f"Outer Join 行數: {len(outer_join)}")

# %% [markdown]
# ### 4.3 條件式合併
# 
# 假設我們有一個折扣表，根據訂單日期和產品類別提供不同的折扣率。使用條件式合併將適當的折扣應用到每個訂單。

# %%
# 在此編寫您的代碼
# 創建折扣表
discount_data = {
    'category': ['Electronics', 'Electronics', 'Clothing', 'Clothing', 'Home', 'Home', 'Books', 'Sports'],
    'start_date': pd.to_datetime(['2022-01-01', '2022-07-01', '2022-01-01', '2022-07-01', 
                                  '2022-01-01', '2022-07-01', '2022-01-01', '2022-01-01']),
    'end_date': pd.to_datetime(['2022-06-30', '2022-12-31', '2022-06-30', '2022-12-31', 
                                '2022-06-30', '2022-12-31', '2022-12-31', '2022-12-31']),
    'discount_rate': [0.05, 0.08, 0.10, 0.15, 0.07, 0.12, 0.20, 0.10]
}
discount_df = pd.DataFrame(discount_data)

# 準備訂單和產品數據
merged_data = None  # 替換為您的合併代碼

# 條件式合併應用折扣
# 提示: 您需要檢查每個訂單的日期是否在折扣的日期範圍內，以及產品類別是否匹配
orders_with_discount = None  # 替換為您的條件式合併代碼

# 計算折扣後金額
orders_with_discount['discounted_amount'] = None  # 替換為您的計算代碼

# 顯示結果
print(orders_with_discount[['order_id', 'order_date', 'category', 'total_amount', 'discount_rate', 'discounted_amount']].head(10))

# %% [markdown]
# ## ⏰ 練習 5: 時間序列分析
# 
# 使用 M3.5 中學到的時間序列分析技術完成以下任務。

# %% [markdown]
# ### 5.1 時間序列重採樣與頻率轉換
# 
# 對訂單數據:
# - 按日、週、月重採樣，計算每個時間單位的訂單數和總金額
# - 比較不同時間尺度下的趨勢
# - 使用適當的視覺化展示結果

# %%
# 在此編寫您的代碼
# 設置訂單日期為索引
orders_ts = None  # 替換為您的代碼

# 按不同頻率重採樣
daily_orders = None  # 替換為您的日重採樣代碼
weekly_orders = None  # 替換為您的週重採樣代碼
monthly_orders = None  # 替換為您的月重採樣代碼

# 視覺化比較
plt.figure(figsize=(15, 10))

# 繪製日訂單量
plt.subplot(3, 1, 1)
# 在此編寫您的繪圖代碼

# 繪製週訂單量
plt.subplot(3, 1, 2)
# 在此編寫您的繪圖代碼

# 繪製月訂單量
plt.subplot(3, 1, 3)
# 在此編寫您的繪圖代碼

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.2 移動窗口計算
# 
# 計算訂單金額的:
# - 7天移動平均
# - 30天移動平均
# - 7天移動標準差
# 
# 使用這些指標識別銷售趨勢和波動性。

# %%
# 在此編寫您的代碼
# 按日期匯總訂單金額
daily_sales = None  # 替換為您的代碼

# 計算移動平均和標準差
daily_sales['7d_MA'] = None  # 替換為您的7天移動平均代碼
daily_sales['30d_MA'] = None  # 替換為您的30天移動平均代碼
daily_sales['7d_STD'] = None  # 替換為您的7天標準差代碼

# 視覺化結果
plt.figure(figsize=(15, 10))

# 繪製移動平均
plt.subplot(2, 1, 1)
# 在此編寫您的繪圖代碼

# 繪製移動標準差
plt.subplot(2, 1, 2)
# 在此編寫您的繪圖代碼

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.3 時間序列分解
# 
# 對月度銷售數據進行時間序列分解:
# - 提取趨勢成分
# - 提取季節性成分
# - 提取殘差成分
# - 分析各成分的特點

# %%
# 在此編寫您的代碼
from statsmodels.tsa.seasonal import seasonal_decompose

# 準備月度銷售數據
monthly_sales = None  # 替換為您的代碼

# 進行時間序列分解
decomposition = None  # 替換為您的分解代碼

# 提取各成分
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# 視覺化分解結果
plt.figure(figsize=(12, 10))

# 繪製原始數據
plt.subplot(4, 1, 1)
# 在此編寫您的繪圖代碼

# 繪製趨勢成分
plt.subplot(4, 1, 2)
# 在此編寫您的繪圖代碼

# 繪製季節性成分
plt.subplot(4, 1, 3)
# 在此編寫您的繪圖代碼

# 繪製殘差成分
plt.subplot(4, 1, 4)
# 在此編寫您的繪圖代碼

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 🏆 綜合挑戰: 電子商務數據分析儀表板
# 
# 結合本模組學到的所有技術，創建一個電子商務數據分析儀表板，包括:
# 
# 1. 銷售概況: 總訂單數、總銷售額、平均訂單金額、取消率
# 2. 時間趨勢: 按月銷售趨勢，識別季節性模式
# 3. 客戶分析: 按客戶細分的銷售分布，識別高價值客戶
# 4. 產品分析: 按類別的銷售分布，識別熱門產品
# 5. 地理分析: 按國家的銷售分布
# 
# 使用適當的視覺化展示您的分析結果。

# %%
# 在此編寫您的綜合分析代碼
# 1. 準備數據
complete_data = None  # 替換為您的數據準備代碼

# 2. 銷售概況
sales_summary = None  # 替換為您的銷售概況計算代碼

# 3. 時間趨勢分析
time_trend = None  # 替換為您的時間趨勢分析代碼

# 4. 客戶分析
customer_analysis = None  # 替換為您的客戶分析代碼

# 5. 產品分析
product_analysis = None  # 替換為您的產品分析代碼

# 6. 地理分析
geo_analysis = None  # 替換為您的地理分析代碼

# 7. 創建儀表板
plt.figure(figsize=(15, 15))

# 銷售趨勢
plt.subplot(3, 2, 1)
# 在此編寫您的繪圖代碼

# 類別分布
plt.subplot(3, 2, 2)
# 在此編寫您的繪圖代碼

# 客戶細分
plt.subplot(3, 2, 3)
# 在此編寫您的繪圖代碼

# 支付方式分布
plt.subplot(3, 2, 4)
# 在此編寫您的繪圖代碼

# 國家分布
plt.subplot(3, 2, 5)
# 在此編寫您的繪圖代碼

# 訂單狀態分布
plt.subplot(3, 2, 6)
# 在此編寫您的繪圖代碼

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📋 總結
# 
# 在這個練習中，您應用了 Pandas 進階模組中學到的各種技術，包括:
# 
# - 進階條件篩選
# - 分組與聚合
# - 樞紐表與交叉表
# - 數據合併與連接
# - 時間序列分析
# 
# 這些技能對於處理複雜的數據分析任務非常重要，能夠幫助您從數據中提取有價值的見解。 