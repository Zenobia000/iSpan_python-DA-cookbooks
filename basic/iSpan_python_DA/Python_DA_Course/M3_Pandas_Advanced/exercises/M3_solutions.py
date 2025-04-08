# %% [markdown]
# # 📘 M3 Pandas 進階應用 - 練習題解答

# %% [markdown]
# ## 🧰 環境設置

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 100)
pd.set_option('display.precision', 2)

# 設置隨機種子確保結果可重現
np.random.seed(42)

# %% [markdown]
# ## 🔍 練習 1: 進階條件篩選

# %% [markdown]
# ### 1.1 使用複雜條件組合

# %%
# 篩選訂單
filtered_orders = orders_df[
    ((orders_df['total_amount'] > 500) | (orders_df['quantity'] > 5)) &
    (orders_df['payment_method'].isin(['Credit Card', 'PayPal'])) &
    (orders_df['order_status'] != 'Cancelled')
]

# 顯示結果
print(f"符合條件的訂單數量: {len(filtered_orders)}")
print(filtered_orders.head())

# %% [markdown]
# ### 1.2 使用 query() 方法

# %%
# 合併訂單和產品數據
merged_data = orders_df.merge(products_df, on='product_id')

# 使用 query() 進行篩選
q1_electronics = merged_data.query(
    "order_date.dt.month.isin([1,2,3]) and "
    "category == 'Electronics' and "
    "total_amount > 1000"
)

# 顯示結果
print(f"符合條件的訂單數量: {len(q1_electronics)}")
print(q1_electronics.head())

# %% [markdown]
# ### 1.3 使用字符串方法和正則表達式

# %%
# 找出包含數字5的客戶
customers_with_5 = customers_df[customers_df['customer_name'].str.contains('5')]

# 合併客戶和訂單數據並計算統計
customer_orders = orders_df.merge(customers_with_5, on='customer_id').groupby('customer_name').agg({
    'order_id': 'count',
    'total_amount': 'sum'
}).reset_index()

# 顯示結果
print(f"名稱中包含數字5的客戶數量: {len(customers_with_5)}")
print(customer_orders.head())

# %% [markdown]
# ## 🔄 練習 2: 分組與聚合進階應用

# %% [markdown]
# ### 2.1 多種聚合函數組合

# %%
# 合併訂單和產品數據
merged_data = orders_df.merge(products_df, on='product_id')

# 按類別分組並計算多種聚合指標
category_stats = merged_data.groupby('category').agg({
    'order_id': 'count',
    'total_amount': ['sum', 'mean', 'min', 'max', 'std']
}).round(2)

# 重命名列
category_stats.columns = ['訂單總數', '總銷售金額', '平均訂單金額', '最小訂單金額', '最大訂單金額', '訂單金額標準差']

# 顯示結果
print(category_stats)

# %% [markdown]
# ### 2.2 使用 transform 進行組內標準化

# %%
# 合併訂單和產品數據
merged_data = orders_df.merge(products_df, on='product_id')

# 使用 transform 計算類別平均值
merged_data['category_avg'] = merged_data.groupby('category')['total_amount'].transform('mean')

# 計算與平均值的差異百分比
merged_data['diff_from_avg_pct'] = ((merged_data['total_amount'] - merged_data['category_avg']) 
                                   / merged_data['category_avg'] * 100)

# 計算組內百分位數
merged_data['category_percentile'] = merged_data.groupby('category')['total_amount'].transform(
    lambda x: pd.Series(x).rank(pct=True)
)

# 顯示結果
print(merged_data[['category', 'total_amount', 'category_avg', 
                  'diff_from_avg_pct', 'category_percentile']].head(10))

# %% [markdown]
# ### 2.3 使用 apply 進行複雜的組內操作

# %%
def top_orders(group):
    # 排序並選擇前3個訂單
    top3 = group.nlargest(3, 'total_amount')
    # 計算這些訂單佔總消費的百分比
    total_spent = group['total_amount'].sum()
    top3['pct_of_total'] = (top3['total_amount'] / total_spent * 100).round(2)
    return top3

# 應用函數到每個客戶組
top_customer_orders = orders_df.groupby('customer_id').apply(top_orders).reset_index(drop=True)

# 顯示結果
print(top_customer_orders.head(10))

# %% [markdown]
# ## 📊 練習 3: 樞紐表與交叉表

# %% [markdown]
# ### 3.1 創建多層次樞紐表

# %%
# 準備數據
merged_data = orders_df.merge(products_df, on='product_id')
merged_data['order_month'] = merged_data['order_date'].dt.strftime('%Y-%m')

# 創建多層次樞紐表
pivot_table = pd.pivot_table(
    merged_data,
    values=['total_amount', 'order_id'],
    index=['order_month', 'order_status'],
    columns=['category', 'payment_method'],
    aggfunc={'total_amount': 'sum', 'order_id': 'count'}
)

# 顯示結果
print(pivot_table.head())

# %% [markdown]
# ### 3.2 使用交叉表分析類別關係

# %%
# 準備數據
merged_data = orders_df.merge(products_df, on='product_id').merge(customers_df, on='customer_id')

# 創建交叉表
cross_tab = pd.crosstab(
    merged_data['category'],
    merged_data['country'],
    values=merged_data['total_amount'],
    aggfunc='sum',
    normalize='columns',
    margins=True
).round(3) * 100  # 轉換為百分比

# 顯示結果
print(cross_tab)

# %% [markdown]
# ### 3.3 使用 stack 和 unstack 重塑數據

# %%
# 使用 stack 和 unstack 重塑數據
reshaped_data = pivot_table.stack(level=0).unstack(level=1)

# 重置索引
flat_data = reshaped_data.reset_index()

# 顯示結果
print(flat_data.head())

# %% [markdown]
# ## 🔄 練習 4: 數據合併與連接

# %% [markdown]
# ### 4.1 多表連接創建完整視圖

# %%
# 連接訂單和客戶
order_customer = orders_df.merge(
    customers_df,
    on='customer_id',
    how='left',
    suffixes=('_order', '_customer')
)

# 連接訂單客戶和產品
complete_view = order_customer.merge(
    products_df,
    on='product_id',
    how='left',
    suffixes=('', '_product')
)

# 顯示結果
print(f"完整視圖的列: {complete_view.columns.tolist()}")
print(f"完整視圖的行數: {len(complete_view)}")
print(complete_view.head())

# %% [markdown]
# ### 4.2 使用不同的合併方法比較結果

# %%
# 創建一些沒有對應訂單的產品
new_products = pd.DataFrame({
    'product_id': [1001, 1002],
    'product_name': ['New Product 1', 'New Product 2'],
    'category': ['Electronics', 'Home'],
    'supplier_id': [1, 2],
    'stock_quantity': [100, 200]
})
missing_products = pd.concat([products_df, new_products])

# 創建一些沒有對應產品的訂單
new_orders = orders_df.copy()
new_orders.loc[len(new_orders)] = [len(new_orders)+1, pd.Timestamp('2022-12-31'),
                                  1, 9999, 1, 100, 'Credit Card', 'Standard',
                                  'Completed', 100]

# 比較不同合併方法
inner_join = orders_df.merge(missing_products, on='product_id', how='inner')
left_join = orders_df.merge(missing_products, on='product_id', how='left')
right_join = orders_df.merge(missing_products, on='product_id', how='right')
outer_join = orders_df.merge(missing_products, on='product_id', how='outer')

# 顯示結果比較
print(f"Inner Join 行數: {len(inner_join)}")
print(f"Left Join 行數: {len(left_join)}")
print(f"Right Join 行數: {len(right_join)}")
print(f"Outer Join 行數: {len(outer_join)}")

# %% [markdown]
# ### 4.3 條件式合併

# %%
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
merged_data = orders_df.merge(products_df, on='product_id')

# 條件式合併應用折扣
def apply_discount(row):
    matching_discounts = discount_df[
        (discount_df['category'] == row['category']) &
        (discount_df['start_date'] <= row['order_date']) &
        (discount_df['end_date'] >= row['order_date'])
    ]
    return matching_discounts['discount_rate'].iloc[0] if len(matching_discounts) > 0 else 0

merged_data['discount_rate'] = merged_data.apply(apply_discount, axis=1)

# 計算折扣後金額
merged_data['discounted_amount'] = merged_data['total_amount'] * (1 - merged_data['discount_rate'])

# 顯示結果
print(merged_data[['order_id', 'order_date', 'category', 'total_amount', 
                  'discount_rate', 'discounted_amount']].head(10))

# %% [markdown]
# ## ⏰ 練習 5: 時間序列分析

# %% [markdown]
# ### 5.1 時間序列重採樣與頻率轉換

# %%
# 設置訂單日期為索引
orders_ts = orders_df.set_index('order_date')

# 按不同頻率重採樣
daily_orders = orders_ts.resample('D').agg({
    'order_id': 'count',
    'total_amount': 'sum'
})

weekly_orders = orders_ts.resample('W').agg({
    'order_id': 'count',
    'total_amount': 'sum'
})

monthly_orders = orders_ts.resample('M').agg({
    'order_id': 'count',
    'total_amount': 'sum'
})

# 視覺化比較
plt.figure(figsize=(15, 10))

# 繪製日訂單量
plt.subplot(3, 1, 1)
plt.plot(daily_orders.index, daily_orders['order_id'])
plt.title('日訂單量')
plt.grid(True)

# 繪製週訂單量
plt.subplot(3, 1, 2)
plt.plot(weekly_orders.index, weekly_orders['order_id'])
plt.title('週訂單量')
plt.grid(True)

# 繪製月訂單量
plt.subplot(3, 1, 3)
plt.plot(monthly_orders.index, monthly_orders['order_id'])
plt.title('月訂單量')
plt.grid(True)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.2 移動窗口計算

# %%
# 按日期匯總訂單金額
daily_sales = orders_ts['total_amount'].resample('D').sum()

# 計算移動平均和標準差
daily_sales = pd.DataFrame(daily_sales)
daily_sales['7d_MA'] = daily_sales['total_amount'].rolling(window=7).mean()
daily_sales['30d_MA'] = daily_sales['total_amount'].rolling(window=30).mean()
daily_sales['7d_STD'] = daily_sales['total_amount'].rolling(window=7).std()

# 視覺化結果
plt.figure(figsize=(15, 10))

# 繪製移動平均
plt.subplot(2, 1, 1)
plt.plot(daily_sales.index, daily_sales['total_amount'], label='Daily Sales', alpha=0.5)
plt.plot(daily_sales.index, daily_sales['7d_MA'], label='7-day MA')
plt.plot(daily_sales.index, daily_sales['30d_MA'], label='30-day MA')
plt.title('銷售額移動平均')
plt.legend()
plt.grid(True)

# 繪製移動標準差
plt.subplot(2, 1, 2)
plt.plot(daily_sales.index, daily_sales['7d_STD'])
plt.title('7天移動標準差')
plt.grid(True)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.3 移動窗口計算與時間序列分解

# %%
# 對月度銷售數據進行分析：
# - 計算3個月移動平均
# - 進行時間序列分解，識別趨勢和季節性
# - 視覺化展示結果

# %%
# 計算3個月移動平均
monthly_orders['3個月移動平均_訂單數'] = monthly_orders['訂單數'].rolling(window=3).mean()
monthly_orders['3個月移動平均_總金額'] = monthly_orders['總金額'].rolling(window=3).mean()

# 進行時間序列分解
# 使用加法模型進行分解
decomposition = seasonal_decompose(monthly_orders['總金額'], period=12, model='additive')

# 視覺化分解結果
plt.figure(figsize=(12, 10))

# 繪製原始數據
plt.subplot(4, 1, 1)
plt.plot(monthly_orders.index, monthly_orders['總金額'])
plt.title('原始月度銷售數據')
plt.grid(True)

# 繪製趨勢成分
plt.subplot(4, 1, 2)
plt.plot(monthly_orders.index, decomposition.trend)
plt.title('趨勢成分')
plt.grid(True)

# 繪製季節性成分
plt.subplot(4, 1, 3)
plt.plot(monthly_orders.index, decomposition.seasonal)
plt.title('季節性成分')
plt.grid(True)

# 繪製殘差成分
plt.subplot(4, 1, 4)
plt.plot(monthly_orders.index, decomposition.resid)
plt.title('殘差成分')
plt.grid(True)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 🏆 綜合挑戰: 電子商務數據分析儀表板

# %%
# 1. 準備數據 - 合併訂單、客戶和產品數據
complete_data = orders_df.merge(customers_df, on='customer_id', how='left')\
                        .merge(products_df, on='product_id', how='left')

# 2. 銷售概況
sales_summary = {
    '總訂單數': len(complete_data),
    '總銷售額': complete_data['total_amount'].sum(),
    '平均訂單金額': complete_data['total_amount'].mean(),
    '取消率': (complete_data['order_status'] == 'Cancelled').mean() * 100
}

# 3. 時間趨勢分析
time_trend = complete_data.groupby('order_date')['total_amount'].sum().reset_index()
time_trend.set_index('order_date', inplace=True)
monthly_trend = time_trend.resample('M').sum()

# 4. 客戶分析
customer_analysis = complete_data.groupby('customer_segment').agg({
    'order_id': 'count',
    'total_amount': 'sum'
}).reset_index()

# 5. 產品分析
product_analysis = complete_data.groupby('category').agg({
    'order_id': 'count',
    'total_amount': 'sum'
}).reset_index()

# 6. 地理分析
geo_analysis = complete_data.groupby('country').agg({
    'order_id': 'count',
    'total_amount': 'sum'
}).reset_index()

# 7. 創建儀表板
plt.figure(figsize=(15, 15))

# 銷售趨勢
plt.subplot(3, 2, 1)
plt.plot(monthly_trend.index, monthly_trend['total_amount'])
plt.title('月度銷售趨勢')
plt.xticks(rotation=45)
plt.grid(True)

# 類別分布
plt.subplot(3, 2, 2)
plt.pie(product_analysis['total_amount'], labels=product_analysis['category'], autopct='%1.1f%%')
plt.title('各類別銷售額分布')

# 客戶細分
plt.subplot(3, 2, 3)
sns.barplot(data=customer_analysis, x='customer_segment', y='total_amount')
plt.title('客戶細分銷售分布')
plt.xticks(rotation=45)

# 支付方式分布
plt.subplot(3, 2, 4)
payment_dist = complete_data['payment_method'].value_counts()
plt.pie(payment_dist, labels=payment_dist.index, autopct='%1.1f%%')
plt.title('支付方式分布')

# 國家分布
plt.subplot(3, 2, 5)
sns.barplot(data=geo_analysis.sort_values('total_amount', ascending=False), 
            x='country', y='total_amount')
plt.title('各國家銷售額分布')
plt.xticks(rotation=45)

# 訂單狀態分布
plt.subplot(3, 2, 6)
status_dist = complete_data['order_status'].value_counts()
plt.pie(status_dist, labels=status_dist.index, autopct='%1.1f%%')
plt.title('訂單狀態分布')

plt.tight_layout()
plt.show()

# 打印銷售概況
print("\n銷售概況:")
for metric, value in sales_summary.items():
    if metric in ['總銷售額', '平均訂單金額']:
        print(f"{metric}: ${value:,.2f}")
    elif metric == '取消率':
        print(f"{metric}: {value:.1f}%")
    else:
        print(f"{metric}: {value:,}")

# %% [markdown]
# ## 📋 總結
# 
# 在這個綜合練習中，我們應用了 Pandas 進階模組中學到的各種技術：
# 
# 1. **進階條件篩選**
#    - 使用複雜的布林條件組合
#    - 應用 query() 方法進行高效篩選
# 
# 2. **分組與聚合**
#    - 使用多種聚合函數
#    - 應用 transform() 進行組內計算
# 
# 3. **樞紐表與交叉表**
#    - 創建多維度分析視圖
#    - 使用不同的聚合方法
# 
# 4. **數據合併與連接**
#    - 合併多個數據表
#    - 處理不同類型的連接
# 
# 5. **時間序列分析**
#    - 重採樣與頻率轉換
#    - 移動窗口計算
#    - 時間序列分解
# 
# 這些技術的綜合運用使我們能夠從電子商務數據中提取有價值的業務洞察，
# 幫助理解銷售趨勢、客戶行為和產品表現。 