# %% [markdown]
# # 📘 M3.3 Pandas 樞紐表與交叉表進階應用
# 
# 本教學將深入探討 Pandas 中樞紐表(Pivot Table)與交叉表(Crosstab)的進階應用技巧。
# 這些強大的數據重塑工具能夠幫助我們從不同維度理解數據間的關聯，是數據分析人員必備的高級技能。

# %% [markdown]
# ## 🎯 教學目標
# 
# - 🔍 深入理解樞紐表與交叉表的原理與運作機制
# - 🔄 掌握複雜多層索引(MultiIndex)的處理與操作技巧
# - 📊 學習樞紐表與交叉表的高級自定義與應用
# - 🧮 掌握數據重塑(Reshaping)技術，如stack、unstack、melt等
# - 🛠️ 探索實際業務案例中的多維數據分析方法

# %% [markdown]
# ## 🧰 1. 環境設置

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

# 設置隨機種子以獲得可重現的結果
np.random.seed(42)

# %% [markdown]
# ## 📊 2. 創建進階樣本數據集

# %%
# 創建一個更複雜的銷售數據集，包含時間、區域、產品、渠道等多個維度
n_rows = 1000

# 生成日期範圍 (2年的數據)
dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
sampled_dates = np.random.choice(dates, n_rows)

sales_data = pd.DataFrame({
    'Date': sampled_dates,
    'Year': [d.year for d in sampled_dates],
    'Quarter': [f'Q{(d.month-1)//3+1}' for d in sampled_dates],
    'Month': [d.month for d in sampled_dates],
    'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_rows),
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                             'Miami', 'Boston', 'Denver', 'Seattle', 'Atlanta'], n_rows),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_rows),
    'Product': np.random.choice(['Product_A', 'Product_B', 'Product_C', 'Product_D', 
                               'Product_E', 'Product_F', 'Product_G', 'Product_H'], n_rows),
    'Channel': np.random.choice(['Online', 'Retail', 'Distributor', 'Direct'], n_rows),
    'Sales': np.random.uniform(100, 1000, n_rows).round(2),
    'Units': np.random.randint(1, 20, n_rows),
    'Returns': np.random.randint(0, 3, n_rows),
    'Discount': np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n_rows),
    'Profit': np.random.uniform(10, 300, n_rows).round(2)
})

# 加入一些計算字段
sales_data['Revenue'] = sales_data['Sales'] * (1 - sales_data['Discount'])
sales_data['ProfitMargin'] = (sales_data['Profit'] / sales_data['Revenue'] * 100).round(1)

# 排序數據
sales_data = sales_data.sort_values(['Date', 'Region', 'Category'])

print("進階銷售數據集預覽:")
print(sales_data.head())
print(f"\n數據集維度: {sales_data.shape}")

# %% [markdown]
# ## 📊 3. 樞紐表高級操作與技巧

# %% [markdown]
# ### 3.1 複雜樞紐表與多層索引

# %%
# 創建複雜的多維度樞紐表
advanced_pivot = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Units', 'Profit', 'ProfitMargin'],  # 多個指標
    index=['Region', 'Category'],  # 多級行索引
    columns=['Year', 'Quarter'],  # 多級列索引
    aggfunc={                     # 不同值應用不同聚合函數
        'Revenue': 'sum',
        'Units': 'sum',
        'Profit': 'sum',
        'ProfitMargin': 'mean'
    },
    fill_value=0,
    margins=True,                 # 添加總計
    margins_name='Total'
)

print("複雜多維樞紐表:")
print(advanced_pivot.round(1))

# %%
# 探索樞紐表的多層索引結構
print("多層行索引(Index)結構:")
print(advanced_pivot.index)

print("\n多層列索引(Columns)結構:")
print(advanced_pivot.columns)

# 使用索引名稱訪問
print("\n索引和列的名稱:")
print(f"行索引名稱: {advanced_pivot.index.names}")
print(f"列索引名稱: {advanced_pivot.columns.names}")

# %% [markdown]
# ### 3.2 多層索引的高級操作

# %%
# 1. 使用 .loc 進行多層索引選擇
print("選擇特定區域的數據:")
print(advanced_pivot.loc['North'])

# 選擇特定區域和類別的數據
print("\n選擇North區域的Electronics類別:")
print(advanced_pivot.loc[('North', 'Electronics')])

# 2. 使用 .xs (cross-section) 進行更靈活的選擇
print("\n使用xs選擇特定季度的數據 (跨不同年份):")
q1_data = advanced_pivot.xs('Q1', level='Quarter', axis=1)
print(q1_data)

# 選擇特定年份和季度的組合
print("\n選擇2023年Q2的數據:")
q2_2023 = advanced_pivot.xs(('2023', 'Q2'), level=('Year', 'Quarter'), axis=1)
print(q2_2023)

# %%
# 3. 索引重設、排序與重命名
# 重設部分層級
reset_region = advanced_pivot.reset_index(level='Region')
print("重設Region層級:")
print(reset_region.head())

# 索引排序
sorted_pivot = advanced_pivot.sort_index(level='Category', axis=0)
print("\n按類別排序:")
print(sorted_pivot.head())

# 列排序
col_sorted = advanced_pivot.sort_index(level=['Year', 'Quarter'], axis=1)
print("\n按年份和季度排序列:")
print(col_sorted.head())

# 索引重命名
renamed = advanced_pivot.rename_axis(index={'Region': 'Sales_Region', 'Category': 'Product_Category'})
print("\n重命名索引:")
print(renamed.head())

# %%
# 4. 高級索引選擇與過濾
# 使用索引的get_level_values方法
electronics_food = advanced_pivot[advanced_pivot.index.get_level_values('Category').isin(['Electronics', 'Food'])]
print("選擇Electronics和Food類別:")
print(electronics_food.head())

# 選擇特定列數據 - 2023年的所有季度
year_2023 = advanced_pivot.loc[:, (2023, slice(None))]
print("\n選擇2023年的所有季度數據:")
print(year_2023.head())

# %% [markdown]
# ### 3.3 樞紐表的計算與自定義

# %%
# 1. 創建帶自定義聚合函數的樞紐表
def profit_per_unit(x):
    """計算每單位利潤"""
    return x['Profit'].sum() / x['Units'].sum() if x['Units'].sum() > 0 else 0

def return_rate(x):
    """計算退貨率"""
    return (x['Returns'].sum() / x['Units'].sum() * 100) if x['Units'].sum() > 0 else 0

custom_pivot = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit', 'Units', 'Returns'],
    index=['Region', 'Category'],
    columns=['Channel'],
    aggfunc={
        'Revenue': ['sum', 'mean'],
        'Profit': ['sum', 'mean', profit_per_unit],  # 自定義函數
        'Units': 'sum',
        'Returns': [return_rate]  # 自定義函數
    }
)

print("帶自定義聚合函數的樞紐表:")
print(custom_pivot.head())

# %%
# 2. 對樞紐表結果進行進一步處理
# 展平多層列索引
flattened = custom_pivot.copy()
flattened.columns = ['_'.join(map(str, col)).strip('_') for col in flattened.columns.values]
print("展平後的樞紐表:")
print(flattened.head())

# 添加來自樞紐表結果的新計算欄位
flattened['Revenue_sum_total'] = flattened.filter(like='Revenue_sum').sum(axis=1)
flattened['Profit_to_Revenue_ratio'] = (flattened.filter(like='Profit_sum').sum(axis=1) / 
                                      flattened['Revenue_sum_total']) * 100

print("\n添加計算欄位後的結果:")
print(flattened[['Revenue_sum_total', 'Profit_to_Revenue_ratio']].head())

# %%
# 3. 樞紐表計算百分比變化
# 創建按年月分組的時間序列樞紐表
time_pivot = pd.pivot_table(
    data=sales_data,
    values='Revenue',
    index=['Category'],
    columns=['Year', 'Month'],
    aggfunc='sum'
)

print("時間序列樞紐表:")
print(time_pivot.head())

# 計算各類別同比增長 (2023 vs 2022)
growth_pivot = pd.DataFrame()
for month in range(1, 13):
    if (2022, month) in time_pivot.columns and (2023, month) in time_pivot.columns:
        col_name = f'Growth_M{month}'
        growth_pivot[col_name] = ((time_pivot[(2023, month)] / time_pivot[(2022, month)]) - 1) * 100

print("\n同比增長率 (%):")
print(growth_pivot.round(1).head())

# %% [markdown]
# ## 📊 4. 交叉表高級應用

# %% [markdown]
# ### 4.1 進階交叉表與多層次分析

# %%
# 1. 基本交叉表複習與進階用法
region_category_cross = pd.crosstab(
    index=sales_data['Region'],
    columns=sales_data['Category'],
    values=sales_data['Revenue'],
    aggfunc='sum',
    normalize=True,  # 標準化為比例
    margins=True,
    margins_name='Total'
)

print("區域和類別的收入交叉表 (佔比):")
print(region_category_cross.round(3))

# %%
# 2. 多層次交叉表
# 創建一個三維交叉表: Region x Category x Channel
multi_cross = pd.crosstab(
    index=[sales_data['Region'], sales_data['City']],
    columns=[sales_data['Category'], sales_data['Channel']],
    values=sales_data['Revenue'],
    aggfunc='sum',
    normalize=False
)

print("多層次交叉表:")
print(multi_cross.head(10))

# %%
# 3. 條件交叉表與高級標準化
# 只針對單位銷量大於5的記錄
high_volume_mask = sales_data['Units'] > 5
high_volume_cross = pd.crosstab(
    index=sales_data.loc[high_volume_mask, 'Region'],
    columns=sales_data.loc[high_volume_mask, 'Category'],
    values=sales_data.loc[high_volume_mask, 'Revenue'],
    aggfunc='sum',
    normalize='columns'  # 按列標準化 (每列加總為1)
)

print("高銷量記錄的交叉表 (按列標準化):")
print(high_volume_cross.round(3))

# 按行標準化 (每行加總為1)
high_volume_cross_row = pd.crosstab(
    index=sales_data.loc[high_volume_mask, 'Region'],
    columns=sales_data.loc[high_volume_mask, 'Category'],
    values=sales_data.loc[high_volume_mask, 'Revenue'],
    aggfunc='sum',
    normalize='index'  # 按行標準化
)

print("\n高銷量記錄的交叉表 (按行標準化):")
print(high_volume_cross_row.round(3))

# %% [markdown]
# ### 4.2 交叉表的統計檢驗與應用

# %%
# 1. 卡方檢驗 (Chi-Square Test)
from scipy.stats import chi2_contingency

# 創建類別和渠道的頻次交叉表 (無值，只計數)
category_channel_counts = pd.crosstab(sales_data['Category'], sales_data['Channel'])
print("類別和渠道的頻次交叉表:")
print(category_channel_counts)

# 執行卡方檢驗
chi2, p, dof, expected = chi2_contingency(category_channel_counts)
print("\n卡方檢驗結果:")
print(f"卡方值: {chi2:.2f}")
print(f"p值: {p:.6f}")
print(f"自由度: {dof}")

# 展示期望頻次
expected_df = pd.DataFrame(
    expected, 
    index=category_channel_counts.index, 
    columns=category_channel_counts.columns
)
print("\n期望頻次:")
print(expected_df.round(2))

# %%
# 2. 標準化殘差 (衡量實際與期望的差異程度)
# 計算標準化殘差: (觀察值 - 期望值) / sqrt(期望值)
observed = category_channel_counts.values
residuals = (observed - expected) / np.sqrt(expected)

residual_df = pd.DataFrame(
    residuals, 
    index=category_channel_counts.index, 
    columns=category_channel_counts.columns
)

print("標準化殘差:")
print(residual_df.round(2))

# 可視化標準化殘差
plt.figure(figsize=(12, 8))
sns.heatmap(residual_df, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
plt.title('類別和渠道之間的標準化殘差', fontsize=14)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 5. 數據重塑技術 (Reshaping)

# %% [markdown]
# ### 5.1 Stack & Unstack 操作

# %%
# 1. Stack操作 - 將列轉為索引層級
# 先創建一個簡化的樞紐表用於演示
demo_pivot = pd.pivot_table(
    data=sales_data,
    values='Revenue',
    index=['Region', 'Category'],
    columns=['Year', 'Quarter'],
    aggfunc='sum'
)

print("示範用樞紐表:")
print(demo_pivot.head())

# Stack: 將列層級轉為行層級
stacked = demo_pivot.stack()
print("\nStack操作後:")
print(stacked.head(10))

# 進一步堆疊
multi_stacked = demo_pivot.stack(level=['Year', 'Quarter'])
print("\n多層級Stack後:")
print(multi_stacked.head(10))

# %%
# 2. Unstack操作 - 將索引層級轉為列
# 從前面的stacked數據繼續
unstacked = stacked.unstack(level='Quarter')
print("部分Unstack後:")
print(unstacked.head())

# 多層級unstack
multi_unstacked = multi_stacked.unstack(level=['Category', 'Quarter'])
print("\n多層級Unstack後:")
print(multi_unstacked.head())

# 從原始數據中選擇性地unstack特定層級
region_cat_year_quarter = pd.pivot_table(
    data=sales_data,
    values='Revenue',
    index=['Region', 'Category', 'Year', 'Quarter'],
    aggfunc='sum'
)

print("\n四層級索引樞紐表:")
print(region_cat_year_quarter.head())

# 選擇性unstack - 將'Year'和'Quarter'提升為列
selective_unstack = region_cat_year_quarter.unstack(['Year', 'Quarter'])
print("\n選擇性Unstack後:")
print(selective_unstack.head())

# %% [markdown]
# ### 5.2 Melt, Wide to Long & Long to Wide

# %%
# 1. Melt操作 - 將寬數據轉為長數據
# 創建一個寬格式的數據用於演示
wide_df = pd.pivot_table(
    data=sales_data,
    values='Revenue',
    index=['Region', 'Category'],
    columns='Channel',
    aggfunc='sum'
).reset_index()

print("寬格式數據:")
print(wide_df.head())

# 使用melt將數據從寬格式轉為長格式
melted = pd.melt(
    wide_df,
    id_vars=['Region', 'Category'],
    var_name='Channel',
    value_name='Revenue'
)

print("\n使用melt後的長格式數據:")
print(melted.head(10))

# %%
# 2. 多列melt
# 創建包含多個指標的寬格式數據
multi_metric_wide = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit'],
    index=['Region'],
    columns='Category',
    aggfunc='sum'
).reset_index()

print("多指標寬格式數據:")
print(multi_metric_wide.head())

# 合併列名以便於melt
multi_metric_wide.columns = ['_'.join(map(str, col)).strip('_') if col[0] != 'Region' else 'Region' 
                           for col in multi_metric_wide.columns.values]

print("\n合併列名後:")
print(multi_metric_wide.head())

# 使用melt轉換為長格式
multi_melted = pd.melt(
    multi_metric_wide,
    id_vars=['Region'],
    var_name='Metric_Category',
    value_name='Value'
)

# 分割Metric_Category成Metric和Category
multi_melted[['Metric', 'Category']] = multi_melted['Metric_Category'].str.split('_', n=1, expand=True)

print("\n多指標melt後的結果:")
print(multi_melted.head(10))

# %%
# 3. 使用pivot將長格式數據轉為寬格式
# 從melted數據轉回寬格式
pivot_back = melted.pivot(
    index=['Region', 'Category'],
    columns='Channel',
    values='Revenue'
)

print("使用pivot將長格式轉回寬格式:")
print(pivot_back.head())

# 與原始wide_df比較
print("\n與原始寬格式數據相同嗎?")
comparison = pivot_back.reset_index() == wide_df.set_index(['Region', 'Category']).reset_index()
print(comparison.all().all())  # 檢查所有值是否都相同

# %% [markdown]
# ## 📊 6. 實際業務應用案例

# %% [markdown]
# ### 6.1 銷售數據多維分析儀表板

# %%
# 1. 年度銷售趨勢分析
yearly_trend = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit'],
    index=['Year', 'Quarter', 'Month'],
    aggfunc='sum'
).reset_index()

print("年度銷售趨勢:")
print(yearly_trend)

# 可視化年度趨勢
plt.figure(figsize=(14, 7))
yearly_by_quarter = pd.pivot_table(
    data=sales_data,
    values=['Revenue'],
    index=['Quarter'],
    columns=['Year'],
    aggfunc='sum'
)

yearly_by_quarter.plot(kind='bar', ax=plt.gca())
plt.title('各季度收入比較 (按年份)', fontsize=14)
plt.xlabel('季度')
plt.ylabel('收入')
plt.legend(title='年份')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# %%
# 2. 產品組合分析
product_mix = pd.crosstab(
    index=sales_data['Category'],
    columns=sales_data['Region'],
    values=sales_data['Revenue'],
    aggfunc='sum',
    normalize='columns',
    margins=True,
    margins_name='Total'
)

print("產品組合分析 (按區域):")
print(product_mix.round(3))

# 可視化產品組合
plt.figure(figsize=(14, 7))
product_mix.loc[:'Total', :'West'].drop('Total', axis=1).plot(
    kind='bar', stacked=True, ax=plt.gca(), colormap='tab10'
)
plt.title('各區域產品組合佔比', fontsize=14)
plt.xlabel('產品類別')
plt.ylabel('佔比')
plt.legend(title='區域')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# %%
# 3. 銷售渠道效率分析
channel_efficiency = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit', 'Units', 'Returns'],
    index=['Channel'],
    aggfunc={
        'Revenue': 'sum',
        'Profit': 'sum',
        'Units': 'sum',
        'Returns': 'sum'
    }
).reset_index()

# 計算KPI
channel_efficiency['Profit_Margin'] = (channel_efficiency['Profit'] / channel_efficiency['Revenue'] * 100).round(1)
channel_efficiency['Return_Rate'] = (channel_efficiency['Returns'] / channel_efficiency['Units'] * 100).round(1)
channel_efficiency['Revenue_per_Unit'] = (channel_efficiency['Revenue'] / channel_efficiency['Units']).round(2)

print("銷售渠道效率分析:")
print(channel_efficiency)

# 可視化渠道效率
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# 利潤率比較
ax[0].bar(channel_efficiency['Channel'], channel_efficiency['Profit_Margin'])
ax[0].set_title('各渠道利潤率 (%)')
ax[0].set_xlabel('銷售渠道')
ax[0].set_ylabel('利潤率 (%)')
ax[0].grid(axis='y', linestyle='--', alpha=0.7)

# 退貨率比較
ax[1].bar(channel_efficiency['Channel'], channel_efficiency['Return_Rate'], color='crimson')
ax[1].set_title('各渠道退貨率 (%)')
ax[1].set_xlabel('銷售渠道')
ax[1].set_ylabel('退貨率 (%)')
ax[1].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 6.2 高級報表與指標分析

# %%
# 1. 區域經理績效儀表板
# 假設每個Region有一名區域經理
region_manager = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit', 'Units'],
    index=['Region'],
    aggfunc='sum'
)

# 計算更多KPI
region_manager['Avg_Unit_Price'] = (region_manager['Revenue'] / region_manager['Units']).round(2)
region_manager['Profit_Margin'] = (region_manager['Profit'] / region_manager['Revenue'] * 100).round(1)

# 計算各區域的排名
region_manager['Revenue_Rank'] = region_manager['Revenue'].rank(ascending=False, method='min').astype(int)
region_manager['Profit_Rank'] = region_manager['Profit'].rank(ascending=False, method='min').astype(int)
region_manager['Margin_Rank'] = region_manager['Profit_Margin'].rank(ascending=False, method='min').astype(int)

# 按收入排序
region_manager = region_manager.sort_values('Revenue', ascending=False)

print("區域經理績效儀表板:")
print(region_manager)

# %%
# 2. 類別-渠道矩陣分析
category_channel_matrix = pd.pivot_table(
    data=sales_data,
    values=['Revenue', 'Profit', 'ProfitMargin'],
    index=['Category'],
    columns=['Channel'],
    aggfunc={
        'Revenue': 'sum',
        'Profit': 'sum',
        'ProfitMargin': 'mean'
    }
)

# 計算總計
category_channel_matrix['Total_Revenue'] = category_channel_matrix['Revenue'].sum(axis=1)
category_channel_matrix['Total_Profit'] = category_channel_matrix['Profit'].sum(axis=1)
category_channel_matrix['Overall_Margin'] = (category_channel_matrix['Total_Profit'] / 
                                          category_channel_matrix['Total_Revenue'] * 100).round(1)

print("類別-渠道矩陣分析:")
print(category_channel_matrix)

# 找出每個類別最佳的銷售渠道
best_channel = pd.DataFrame()
for category in category_channel_matrix.index:
    revenue_by_channel = category_channel_matrix.loc[category, 'Revenue']
    best_revenue_channel = revenue_by_channel.idxmax()[1]  # [1]獲取渠道名
    
    profit_by_channel = category_channel_matrix.loc[category, 'Profit']
    best_profit_channel = profit_by_channel.idxmax()[1]
    
    margin_by_channel = category_channel_matrix.loc[category, 'ProfitMargin']
    best_margin_channel = margin_by_channel.idxmax()[1]
    
    best_channel.loc[category, 'Best_Revenue_Channel'] = best_revenue_channel
    best_channel.loc[category, 'Best_Profit_Channel'] = best_profit_channel
    best_channel.loc[category, 'Best_Margin_Channel'] = best_margin_channel

print("\n每個類別的最佳銷售渠道:")
print(best_channel)

# %% [markdown]
# ## 📋 7. 總結與最佳實踐

# %% [markdown]
# ### 7.1 樞紐表與交叉表的核心優勢
# 
# - **多維數據分析**：可同時從多個角度分析數據，發現複雜關係
# - **彙總與計算**：強大的聚合函數能力，支持自定義計算公式
# - **可視化準備**：提供結構化數據，便於後續視覺化展示
# - **業務儀表板**：適合創建管理報表和業務儀表板

# %% [markdown]
# ### 7.2 進階應用技巧總結
# 
# - **多層索引操作**：掌握Stack/Unstack/xs等操作，靈活處理複雜索引結構
# - **數據重塑**：熟練運用Melt和Pivot轉換數據格式，適應不同分析需求
# - **優化查詢**：巧用切片、過濾和索引選擇，高效獲取所需數據
# - **清理結果**：使用重命名、索引重組和格式化，增強結果可讀性
# - **深度分析**：結合統計檢驗和業務指標，實現從數據到洞察的轉化

# %% [markdown]
# ### 7.3 實際應用建議
# 
# - **適用場景**：適合多維度對比、時間序列分析、組合分析等業務場景
# - **性能考量**：處理大數據集時，先進行必要的過濾和抽樣，再進行樞紐操作
# - **結果呈現**：根據受眾需求選擇適當的指標和格式，增強溝通效果
# - **集成應用**：將樞紐表結果與視覺化工具結合，創建動態報表和儀表板
# - **持續學習**：關注Pandas更新，掌握新特性和優化方法 