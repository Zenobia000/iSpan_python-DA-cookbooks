# %% [markdown]
# # 📘 M3.2 Pandas 分組與聚合進階應用
# 
# 本教學將深入探討 Pandas 中 `groupby()` 操作的進階應用與聚合函數的多種用法。
# 分組與聚合是數據分析中的核心操作，掌握這些進階技巧可以讓您更高效地從複雜數據中提取洞察。

# %% [markdown]
# ## 🎯 教學目標
# 
# - 🔍 深入理解 groupby() 操作的內部機制與優化
# - 🔄 掌握多種聚合方法與函數的綜合應用
# - 📊 學習創建與使用複雜的自定義聚合函數
# - 🧮 理解分組轉換與過濾的高級技巧
# - 🛠️ 運用分組操作解決實際業務問題

# %% [markdown]
# ## 🧰 1. 環境設置

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 100)
pd.set_option('display.precision', 2)

# %% [markdown]
# ## 📊 2. GroupBy 進階操作

# %%
# 創建較複雜的示例數據集
np.random.seed(42)
n_rows = 1000

# 產品資料
products = pd.DataFrame({
    'ProductID': range(1, 101),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], 100),
    'Supplier': np.random.choice(['SupplierA', 'SupplierB', 'SupplierC', 'SupplierD'], 100),
    'Price': np.random.uniform(10, 1000, 100).round(2),
    'Stock': np.random.randint(0, 100, 100)
})

# 銷售資料
sales = pd.DataFrame({
    'SaleID': range(1, n_rows + 1),
    'Date': pd.date_range(start='2023-01-01', periods=n_rows),
    'ProductID': np.random.choice(products['ProductID'], n_rows),
    'Quantity': np.random.randint(1, 10, n_rows),
    'CustomerID': np.random.randint(1, 21, n_rows),
    'StoreID': np.random.choice(['Store1', 'Store2', 'Store3', 'Store4'], n_rows),
    'Discount': np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n_rows),
})

# 合併產品與銷售資料
sales_data = pd.merge(sales, products, on='ProductID')

# 計算每筆銷售的總金額
sales_data['TotalAmount'] = sales_data['Quantity'] * sales_data['Price'] * (1 - sales_data['Discount'])

print("銷售資料預覽:")
print(sales_data.head())
print(f"\n資料集維度: {sales_data.shape}")

# %% [markdown]
# ### 2.1 GroupBy 對象的深入理解

# %%
# 創建 GroupBy 對象並查看其結構
store_group = sales_data.groupby('StoreID')
print("GroupBy 對象類型:", type(store_group))
print("GroupBy 對象包含的群組:", list(store_group.groups.keys()))
print("第一個群組的索引:", list(store_group.groups['Store1'])[:5], "...")

# 使用 get_group() 方法獲取特定群組
store1_data = store_group.get_group('Store1')
print("\nStore1的資料 (前5行):")
print(store1_data.head())

# %%
# 查看 GroupBy 對象的組成
# 使用 for 循環遍歷群組
print("遍歷群組 (僅顯示每個群組的前2行):")
for name, group in store_group:
    print(f"\n{name} 群組:")
    print(group.head(2))
    if name == 'Store2':  # 只顯示部分群組作為示例
        break

# %% [markdown]
# ### 2.2 多種聚合函數的組合應用

# %%
# 基本聚合操作的進階用法
store_category_summary = sales_data.groupby(['StoreID', 'Category']).agg({
    'TotalAmount': ['sum', 'mean', 'count', 'median', 'std'],
    'Quantity': ['sum', 'mean', 'max'],
    'Discount': ['mean', 'max']
})

print("多級分組與多種聚合函數組合:")
print(store_category_summary)

# %%
# 改進結果格式，展平多級列名
store_category_flat = store_category_summary.reset_index()
store_category_flat.columns = ['_'.join(col).strip('_') for col in store_category_flat.columns.values]
print("展平後的多級分組結果:")
print(store_category_flat.head())

# %%
# 使用 named aggregation (Pandas 0.25+)
named_agg = sales_data.groupby(['StoreID', 'Category']).agg(
    total_sales=('TotalAmount', 'sum'),
    avg_sales=('TotalAmount', 'mean'),
    sales_count=('TotalAmount', 'count'),
    total_quantity=('Quantity', 'sum'),
    avg_quantity=('Quantity', 'mean'),
    avg_discount=('Discount', 'mean')
)

print("使用命名聚合的結果:")
print(named_agg.head())

# %% [markdown]
# ### 2.3 高級自定義聚合函數

# %%
# 定義複雜自定義聚合函數
def weighted_avg(group, value_col, weight_col):
    """計算加權平均數"""
    return (group[value_col] * group[weight_col]).sum() / group[weight_col].sum()

# 創建部分函數以便在 agg() 中使用
weighted_price = partial(weighted_avg, value_col='Price', weight_col='Quantity')
weighted_discount = partial(weighted_avg, value_col='Discount', weight_col='TotalAmount')

# 使用自定義聚合函數
custom_agg = sales_data.groupby('Category').agg({
    'TotalAmount': ['sum', 'count'],
    'Price': [weighted_price],
    'Discount': [weighted_discount]
})

print("使用自定義聚合函數的結果:")
print(custom_agg)

# %%
# 使用裝飾器定義自定義聚合函數 (更具可讀性的方式)
from pandas.api.extensions import register_series_accessor

@register_series_accessor("custom_stats")
class CustomStats:
    def __init__(self, series):
        self._series = series
        
    def top_n_mean(self, n=3):
        """計算前n個最大值的平均值"""
        return self._series.nlargest(n).mean()
    
    def excludes_extremes_mean(self):
        """計算排除最大值和最小值後的平均值"""
        s = self._series.sort_values()
        return s.iloc[1:-1].mean()

# 測試自定義統計方法
print("客製化Series統計方法:")
price_series = sales_data['Price']
print(f"前3個最大價格的平均值: {price_series.custom_stats.top_n_mean(3):.2f}")
print(f"排除極值後的平均價格: {price_series.custom_stats.excludes_extremes_mean():.2f}")

# %%
# 使用 lambda 函數進行複雜聚合操作
advanced_stats = sales_data.groupby('Category').agg({
    'TotalAmount': [
        'sum', 
        'mean',
        ('above_avg_count', lambda x: (x > x.mean()).sum()),
        ('pct_above_500', lambda x: (x > 500).mean() * 100)
    ],
    'Price': [
        'mean',
        ('price_range', lambda x: x.max() - x.min()),
        ('price_95pct', lambda x: x.quantile(0.95))
    ],
    'Quantity': [
        'sum',
        ('median_qty', 'median'),
        ('mode_qty', lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan)
    ]
})

print("使用 lambda 函數的進階統計結果:")
print(advanced_stats)

# %% [markdown]
# ### 2.4 分組轉換與應用 (Transform & Apply)

# %%
# 使用 transform 進行組內標準化
# 計算每個類別中產品價格的 z-score
sales_data['Price_ZScore'] = sales_data.groupby('Category')['Price'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# 計算每個門店銷售額相對於該門店平均值的百分比
sales_data['SalesVsStoreAvg'] = sales_data.groupby('StoreID')['TotalAmount'].transform(
    lambda x: x / x.mean() * 100
)

print("使用 transform 進行數據轉換的結果:")
print(sales_data[['ProductID', 'Category', 'Price', 'Price_ZScore', 
                 'StoreID', 'TotalAmount', 'SalesVsStoreAvg']].head(10))

# %%
# 使用 transform 計算累計和移動統計量
# 按門店和日期分組，計算每個門店的累計銷售額
sales_data['Date'] = pd.to_datetime(sales_data['Date'])
sales_data['Month'] = sales_data['Date'].dt.to_period('M')

# 計算每個門店每月累計銷售額
sales_data['CumulativeStoreSales'] = sales_data.sort_values('Date').groupby(['StoreID', 'Month'])['TotalAmount'].transform(
    lambda x: x.cumsum()
)

# 計算每個產品類別的3天移動平均銷售額
sales_data['MovingAvgCategorySales'] = sales_data.sort_values('Date').groupby(['Category', 'Date'])['TotalAmount'].transform(
    lambda x: x.rolling(3, min_periods=1).mean()
)

print("累計和移動統計結果:")
print(sales_data[['Date', 'Month', 'StoreID', 'Category', 'TotalAmount', 
                 'CumulativeStoreSales', 'MovingAvgCategorySales']].sort_values(['StoreID', 'Date']).head(10))

# %%
# 使用 apply 進行更複雜的組內操作
# 找出每個類別中銷售額最高的前3個產品
top_products = sales_data.groupby('Category').apply(
    lambda x: x.nlargest(3, 'TotalAmount')
).reset_index(drop=True)

print("每個類別銷售額最高的前3個產品:")
print(top_products[['Category', 'ProductID', 'TotalAmount']])

# %%
# 使用 apply 計算每個類別的銷售趨勢
category_trend = sales_data.groupby('Category').apply(
    lambda group: pd.Series({
        'SalesGrowth': (group['TotalAmount'].iloc[-30:].mean() / 
                        group['TotalAmount'].iloc[:30].mean() - 1) * 100,
        'QuantityGrowth': (group['Quantity'].iloc[-30:].sum() / 
                          group['Quantity'].iloc[:30].sum() - 1) * 100,
        'IsGrowing': group['TotalAmount'].iloc[-30:].mean() > group['TotalAmount'].iloc[:30].mean()
    })
)

print("各類別銷售趨勢分析:")
print(category_trend)

# %% [markdown]
# ### 2.5 分組過濾 (Filtering)

# %%
# 使用 filter 方法進行組級過濾
# 只保留平均銷售額超過300的類別
high_value_categories = sales_data.groupby('Category').filter(
    lambda x: x['TotalAmount'].mean() > 300
)

print("高價值類別 (平均銷售額 > 300):")
cat_names = high_value_categories['Category'].unique()
print(f"篩選後的類別: {', '.join(cat_names)}")
print(f"篩選前行數: {len(sales_data)}, 篩選後行數: {len(high_value_categories)}")

# %%
# 複雜過濾：保留至少有100筆銷售且平均折扣率低於10%的店鋪
qualified_stores = sales_data.groupby('StoreID').filter(
    lambda x: (len(x) >= 100) & (x['Discount'].mean() < 0.1)
)

print("符合條件的店鋪:")
store_names = qualified_stores['StoreID'].unique()
print(f"篩選後的店鋪: {', '.join(store_names)}")
print(f"篩選前行數: {len(sales_data)}, 篩選後行數: {len(qualified_stores)}")

# %%
# 組合過濾與聚合：找出產品類別中至少有3種產品且平均價格高於300的類別
price_threshold = 300
min_products = 3

# 步驟1：計算每個類別的獨特產品數量
product_counts = sales_data.groupby('Category')['ProductID'].nunique()
qualified_categories = product_counts[product_counts >= min_products].index

# 步驟2：計算每個類別的平均價格
avg_prices = sales_data.groupby('Category')['Price'].mean()
high_price_categories = avg_prices[avg_prices > price_threshold].index

# 步驟3：找出同時滿足兩個條件的類別
target_categories = set(qualified_categories) & set(high_price_categories)
print(f"符合條件的類別 (至少{min_products}個產品且平均價格 > {price_threshold}):")
print(target_categories)

# 步驟4：篩選出這些類別的資料
target_data = sales_data[sales_data['Category'].isin(target_categories)]
print(f"\n篩選後的資料預覽:")
print(target_data[['Category', 'ProductID', 'Price']].head())

# %% [markdown]
# ## 📊 3. 實際案例：銷售數據多維度分析

# %%
# 創建時間維度
sales_data['Year'] = sales_data['Date'].dt.year
sales_data['Month'] = sales_data['Date'].dt.month
sales_data['Quarter'] = sales_data['Date'].dt.quarter
sales_data['Day'] = sales_data['Date'].dt.day_name()

# 1. 多維度銷售分析：按季度、門店和產品類別進行分組
multi_dim_analysis = sales_data.groupby(['Year', 'Quarter', 'StoreID', 'Category']).agg({
    'TotalAmount': ['sum', 'mean', 'count'],
    'Quantity': 'sum',
    'Discount': 'mean'
}).round(2)

print("多維度銷售分析 (季度 x 門店 x 類別):")
print(multi_dim_analysis.head(8))

# %%
# 2. 時段分析：不同時間維度的銷售趨勢
time_analysis = sales_data.groupby(['Month', 'Day']).agg(
    total_sales=('TotalAmount', 'sum'),
    avg_sales=('TotalAmount', 'mean'),
    transactions=('SaleID', 'nunique'),
    avg_quantity=('Quantity', 'mean')
).reset_index()

print("月份與星期分析:")
print(time_analysis.head(10))

# 可視化月份銷售趨勢
plt.figure(figsize=(14, 6))
sns.barplot(x='Month', y='total_sales', data=time_analysis, estimator=sum, ci=None)
plt.title('每月總銷售額', fontsize=14)
plt.xlabel('月份')
plt.ylabel('總銷售額')
plt.tight_layout()
plt.show()

# %%
# 3. 客戶購買分析：研究每個客戶的購買行為
customer_analysis = sales_data.groupby('CustomerID').agg(
    total_spent=('TotalAmount', 'sum'),
    total_transactions=('SaleID', 'nunique'),
    avg_transaction_value=('TotalAmount', lambda x: x.sum() / len(x.unique())),
    first_purchase=('Date', 'min'),
    last_purchase=('Date', 'max'),
    favorite_category=('Category', lambda x: x.mode().iloc[0]),
    favorite_store=('StoreID', lambda x: x.mode().iloc[0]),
    product_variety=('ProductID', 'nunique')
)

# 計算客戶活躍期 (天數)
customer_analysis['active_days'] = (customer_analysis['last_purchase'] - 
                                   customer_analysis['first_purchase']).dt.days

print("客戶購買行為分析:")
print(customer_analysis.head())

# %%
# 客戶價值分層 (RFM分析簡化版)
# R(Recency) - 最近一次購買時間
# F(Frequency) - 購買頻率
# M(Monetary) - 購買金額
today = pd.Timestamp('2023-12-31')
rfm = sales_data.groupby('CustomerID').agg(
    recency=('Date', lambda x: (today - x.max()).days),
    frequency=('SaleID', 'nunique'),
    monetary=('TotalAmount', 'sum')
)

# 將RFM三個維度分為5個等級
for metric in ['recency', 'frequency', 'monetary']:
    if metric == 'recency':
        # 對於recency, 天數越小越好
        rfm[f'{metric}_score'] = pd.qcut(rfm[metric], 5, labels=False, duplicates='drop')
        rfm[f'{metric}_score'] = 4 - rfm[f'{metric}_score']  # 反轉分數
    else:
        # 對於frequency和monetary, 數值越大越好
        rfm[f'{metric}_score'] = pd.qcut(rfm[metric], 5, labels=False, duplicates='drop')

# 計算RFM總分
rfm['rfm_score'] = rfm['recency_score'] + rfm['frequency_score'] + rfm['monetary_score']

# 定義客戶分層
rfm['customer_segment'] = pd.qcut(rfm['rfm_score'], 4, 
                                 labels=['Bronze', 'Silver', 'Gold', 'Platinum'])

print("客戶RFM分析與分層:")
print(rfm.head(10))

# 展示各客戶分層的平均指標
segment_analysis = rfm.groupby('customer_segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean'
}).round(2)

print("\n不同客戶層級的平均指標:")
print(segment_analysis)

# %% [markdown]
# ## 📊 4. 高級分組技巧與最佳實踐

# %%
# 1. 使用 pd.Grouper 進行時間序列分組
time_grouped = sales_data.groupby([
    pd.Grouper(key='Date', freq='W'),  # 按週分組
    'Category'
]).agg({
    'TotalAmount': 'sum',
    'Quantity': 'sum'
}).reset_index()

print("使用 pd.Grouper 按週分組:")
print(time_grouped.head())

# %%
# 2. 使用分組索引實現高級選擇
print("使用 .xs() 進行跨層級選擇:")
# 選擇特定類別在每個店鋪的銷售數據
electronics_by_store = multi_dim_analysis.xs('Electronics', level='Category', drop_level=False)
print(electronics_by_store.head())

# %%
# 3. 組內排名
sales_data['StoreRank'] = sales_data.groupby('StoreID')['TotalAmount'].rank(method='dense', ascending=False)
sales_data['CategoryRank'] = sales_data.groupby(['StoreID', 'Category'])['TotalAmount'].rank(method='dense', ascending=False)

print("組內排名示例:")
print(sales_data[['StoreID', 'Category', 'TotalAmount', 'StoreRank', 'CategoryRank']].head(15))

# %%
# 4. 性能優化技巧
import time

def performance_test():
    results = {}
    
    # 測試1: 標準groupby
    start = time.time()
    std_groupby = sales_data.groupby('Category')['TotalAmount'].mean()
    results['Standard groupby'] = time.time() - start
    
    # 測試2: 預先排序後groupby
    start = time.time()
    # 先排序數據，使用排序的數據進行分組能提高速度
    sorted_data = sales_data.sort_values('Category')
    sorted_groupby = sorted_data.groupby('Category')['TotalAmount'].mean()
    results['Sorted groupby'] = time.time() - start
    
    # 測試3: 使用categoricals
    start = time.time()
    # 將分組列轉換為categorical可以提高分組速度
    cat_data = sales_data.copy()
    cat_data['Category'] = cat_data['Category'].astype('category')
    cat_groupby = cat_data.groupby('Category')['TotalAmount'].mean()
    results['Categorical groupby'] = time.time() - start
    
    return results

# 執行性能測試
perf_results = performance_test()
print("分組操作性能比較 (秒):")
for method, duration in perf_results.items():
    print(f"{method}: {duration:.5f}")

# %% [markdown]
# ## 📋 5. 總結

# %% [markdown]
# ### 5.1 分組與聚合的核心概念
# 
# - **GroupBy 對象**：理解其內部結構、分組鍵和數據分割方式
# - **多層次分組**：使用多個鍵實現複雜的數據分層聚合
# - **聚合函數**：靈活組合內置與自定義的聚合函數
# - **聚合方法**：掌握 agg()、transform()、apply() 和 filter() 的區別與應用場景

# %% [markdown]
# ### 5.2 進階應用技巧
# 
# - **自定義聚合函數**：使用 lambda、partial 函數和裝飾器創建複雜聚合功能
# - **分組轉換**：使用 transform() 進行組內標準化、累計統計和移動窗口計算
# - **分層聚合**：在多個維度上進行數據摘要，提取業務洞察
# - **高效分組**：利用索引、排序和類別優化分組性能
# - **結果處理**：清理和重塑聚合結果，使其更易於分析和可視化

# %% [markdown]
# ### 5.3 實務應用思考
# 
# - **業務指標設計**：基於分組聚合構建KPI和業務指標
# - **客戶分層**：使用RFM等模型進行客戶價值分析
# - **時間序列分析**：在不同時間粒度上分析業務趨勢和季節性
# - **多維度分析**：結合不同維度的數據，發現隱藏的業務關聯
# - **預測建模準備**：使用分組聚合創建有效的模型特徵 