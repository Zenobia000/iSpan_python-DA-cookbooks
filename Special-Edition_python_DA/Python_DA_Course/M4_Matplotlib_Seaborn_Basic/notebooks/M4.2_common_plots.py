# %% [markdown]
# # 📊 M4.2 常見圖表實作

# 本課程專注於使用Matplotlib和Pandas實現各種常見的數據視覺化圖表。我們將學習如何創建和定製各種專業圖表，這些圖表廣泛應用於數據分析、科學研究和商業報告中。通過實際案例，我們將深入學習如何選擇適當的圖表類型來有效呈現不同類型的數據關係。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 掌握各類常見統計圖表的實現方法
# - 🔍 學習如何選擇適合特定數據類型的圖表
# - 🎨 了解圖表定製和美化的實用技巧
# - 📊 結合Pandas數據結構創建快速視覺化

# %%
# 環境設置
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import warnings
from matplotlib.ticker import PercentFormatter

# 忽略警告信息
warnings.filterwarnings('ignore')

# 設置中文字體支持 (如果系統支持)
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
except:
    pass

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 100)

# 設置圖表風格
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# 設置隨機種子確保結果可重現
np.random.seed(42)

# %% [markdown]
# ## 📊 1. 基本統計視覺化

# %%
# 1.1 創建示例數據集
# 創建一個模擬銷售數據集
dates = pd.date_range('2022-01-01', periods=100, freq='D')
sales_data = pd.DataFrame({
    '日期': dates,
    '銷售額': np.random.normal(1000, 200, 100) + np.linspace(0, 300, 100),  # 帶上升趨勢的銷售數據
    '利潤': np.random.normal(300, 80, 100) + np.linspace(0, 100, 100),      # 帶上升趨勢的利潤數據
    '客戶數': np.random.randint(80, 200, 100),                              # 隨機客戶數
    '地區': np.random.choice(['北區', '南區', '東區', '西區'], 100)          # 隨機地區
})

# 添加一些類別數據
sales_data['產品類別'] = np.random.choice(['電子產品', '家具', '服裝', '食品', '書籍'], 100)
sales_data['促銷活動'] = np.random.choice(['是', '否'], 100, p=[0.3, 0.7])  # 30%有促銷

# 設置日期為索引
sales_data_indexed = sales_data.set_index('日期')

print("銷售數據集預覽:")
print(sales_data.head())
print(f"\n數據集形狀: {sales_data.shape}")

# %%
# 1.2 折線圖：顯示時間趨勢
plt.figure(figsize=(12, 6))
plt.plot(sales_data['日期'], sales_data['銷售額'], 'b-', label='銷售額')
plt.plot(sales_data['日期'], sales_data['利潤'], 'g-', label='利潤')
plt.xlabel('日期')
plt.ylabel('金額')
plt.title('銷售額和利潤隨時間變化趨勢')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 使用Pandas繪製
sales_data_indexed[['銷售額', '利潤']].plot(figsize=(12, 6), grid=True)
plt.title('使用Pandas繪製銷售趨勢')
plt.ylabel('金額')
plt.tight_layout()
plt.show()

# %%
# 1.3 長條圖：比較類別數據
# 按產品類別計算平均銷售額
category_sales = sales_data.groupby('產品類別')['銷售額'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 6))
bars = plt.bar(category_sales.index, category_sales.values, color='skyblue', edgecolor='black')

# 在長條上顯示數值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{height:.0f}', ha='center', va='bottom')

plt.xlabel('產品類別')
plt.ylabel('平均銷售額')
plt.title('各產品類別平均銷售額')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 1.4 散點圖：顯示兩個變數之間的關係
plt.figure(figsize=(10, 6))
plt.scatter(sales_data['客戶數'], sales_data['銷售額'], 
            alpha=0.6, c=sales_data.index, cmap='viridis')
plt.xlabel('客戶數')
plt.ylabel('銷售額')
plt.title('客戶數與銷售額的關係')
plt.colorbar(label='日期順序')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 添加分類維度
fig, ax = plt.subplots(figsize=(12, 6))
for region, group in sales_data.groupby('地區'):
    ax.scatter(group['客戶數'], group['銷售額'], alpha=0.6, label=region)
ax.set_xlabel('客戶數')
ax.set_ylabel('銷售額')
ax.set_title('各地區客戶數與銷售額的關係')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 1.5 餅圖：顯示部分佔整體的比例
# 按地區計算銷售總額
region_sales = sales_data.groupby('地區')['銷售額'].sum()
total_sales = region_sales.sum()
percentages = region_sales / total_sales * 100

plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%',
                                   startangle=90, shadow=True, 
                                   colors=plt.cm.Pastel1.colors)
plt.axis('equal')  # 確保餅圖是圓的
plt.title('各地區銷售額佔比')

# 增強文本對比度
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_weight('bold')
    autotext.set_color('black')

plt.tight_layout()
plt.show()

# 替代方案：圓環圖
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(region_sales, labels=region_sales.index, autopct='%1.1f%%',
                                   startangle=90, wedgeprops=dict(width=0.5),
                                   colors=plt.cm.Pastel2.colors)
plt.axis('equal')
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_weight('bold')
plt.title('各地區銷售額佔比（圓環圖）')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 2. 分佈與統計圖表

# %%
# 2.1 直方圖(Histogram)：查看數據分佈
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.hist(sales_data['銷售額'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.xlabel('銷售額')
plt.ylabel('頻率')
plt.title('銷售額分佈')
plt.grid(True, axis='y', alpha=0.3)

plt.subplot(1, 2, 2)
plt.hist(sales_data['利潤'], bins=20, color='salmon', edgecolor='black', alpha=0.7)
plt.xlabel('利潤')
plt.ylabel('頻率')
plt.title('利潤分佈')
plt.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# 2.2 核密度圖(KDE)：平滑的分佈估計
plt.figure(figsize=(12, 6))
sales_data['銷售額'].plot(kind='kde', color='blue', label='銷售額')
sales_data['利潤'].plot(kind='kde', color='green', label='利潤')
plt.xlabel('金額')
plt.ylabel('密度')
plt.title('銷售額和利潤的核密度估計')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 2.3 箱型圖(Box Plot)：數據分佈與離群值
plt.figure(figsize=(12, 6))

# 按產品類別繪製銷售額箱型圖
plt.subplot(1, 2, 1)
boxplot = plt.boxplot([sales_data[sales_data['產品類別'] == cat]['銷售額'] 
                        for cat in sales_data['產品類別'].unique()],
                       patch_artist=True)

# 箱型圖著色
for box, color in zip(boxplot['boxes'], plt.cm.Pastel1.colors):
    box.set(facecolor=color)

plt.xticks(range(1, len(sales_data['產品類別'].unique()) + 1),
           sales_data['產品類別'].unique(), rotation=45)
plt.xlabel('產品類別')
plt.ylabel('銷售額')
plt.title('各產品類別銷售額分佈')
plt.grid(True, axis='y', alpha=0.3)

# 按地區繪製利潤箱型圖
plt.subplot(1, 2, 2)
boxplot = plt.boxplot([sales_data[sales_data['地區'] == region]['利潤'] 
                        for region in sales_data['地區'].unique()],
                       patch_artist=True)

for box, color in zip(boxplot['boxes'], plt.cm.Pastel2.colors):
    box.set(facecolor=color)

plt.xticks(range(1, len(sales_data['地區'].unique()) + 1),
           sales_data['地區'].unique())
plt.xlabel('地區')
plt.ylabel('利潤')
plt.title('各地區利潤分佈')
plt.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# 2.4 小提琴圖(Violin Plot)：結合箱型圖與核密度估計
plt.figure(figsize=(14, 6))

# 使用Seaborn繪製小提琴圖
plt.subplot(1, 2, 1)
sns.violinplot(x='產品類別', y='銷售額', data=sales_data, palette='pastel')
plt.title('各產品類別銷售額分佈(小提琴圖)')
plt.xlabel('產品類別')
plt.ylabel('銷售額')
plt.xticks(rotation=45)
plt.grid(True, axis='y', alpha=0.3)

plt.subplot(1, 2, 2)
sns.violinplot(x='地區', y='利潤', data=sales_data, palette='pastel')
plt.title('各地區利潤分佈(小提琴圖)')
plt.xlabel('地區')
plt.ylabel('利潤')
plt.grid(True, axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# %%
# 2.5 帕累托圖(Pareto Chart)：80/20法則視覺化
# 計算每個產品類別的總銷售額並排序
category_total = sales_data.groupby('產品類別')['銷售額'].sum().sort_values(ascending=False)
category_percentage = category_total / category_total.sum() * 100
cumulative_percentage = category_percentage.cumsum()

fig, ax1 = plt.subplots(figsize=(12, 6))

# 繪製長條圖
bars = ax1.bar(category_total.index, category_total.values, color='skyblue', edgecolor='black')
ax1.set_xlabel('產品類別')
ax1.set_ylabel('總銷售額')
ax1.tick_params(axis='x', rotation=45)

# 繪製累積百分比線
ax2 = ax1.twinx()
ax2.plot(category_total.index, cumulative_percentage.values, 'ro-', linewidth=2)
ax2.set_ylabel('累積百分比')
ax2.set_ylim([0, 110])
ax2.yaxis.set_major_formatter(PercentFormatter())

# 添加參考線
ax2.axhline(y=80, color='gray', linestyle='--', alpha=0.7)

# 添加資料標籤
for i, bar in enumerate(bars):
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1000,
             f'{category_total.values[i]:.0f}', ha='center')
    ax2.text(i, cumulative_percentage.values[i] + 2, 
             f'{cumulative_percentage.values[i]:.1f}%', ha='center', color='red')

plt.title('產品類別銷售額帕累托圖')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 3. 多變量關係圖表

# %%
# 3.1 相關性熱圖(Correlation Heatmap)：變量間相關性
# 計算數值列的相關係數
correlation_matrix = sales_data[['銷售額', '利潤', '客戶數']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, 
            linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('變量間相關性熱圖')
plt.tight_layout()
plt.show()

# %%
# 3.2 散點矩陣圖(Scatter Matrix)：多變量關係
pd.plotting.scatter_matrix(sales_data[['銷售額', '利潤', '客戶數']], 
                           figsize=(12, 10), diagonal='kde', alpha=0.7)
plt.suptitle('多變量散點矩陣圖', y=1.02)
plt.tight_layout()
plt.show()

# 使用Seaborn的pairplot
sns.pairplot(sales_data[['銷售額', '利潤', '客戶數', '地區']], 
             hue='地區', height=2.5, diag_kind='kde')
plt.suptitle('多變量配對圖(按地區分類)', y=1.02)
plt.tight_layout()
plt.show()

# %%
# 3.3 氣泡圖(Bubble Chart)：三維數據可視化
plt.figure(figsize=(12, 8))

# 按產品類別設置不同顏色
categories = sales_data['產品類別'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))

for i, category in enumerate(categories):
    df_subset = sales_data[sales_data['產品類別'] == category]
    plt.scatter(df_subset['客戶數'], df_subset['銷售額'], 
                s=df_subset['利潤'] / 5, alpha=0.6, 
                label=category, color=colors[i])

plt.xlabel('客戶數')
plt.ylabel('銷售額')
plt.title('客戶數、銷售額與利潤關係(氣泡大小表示利潤)')
plt.legend(title='產品類別')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 3.4 平行坐標圖(Parallel Coordinates)：多維數據可視化
from pandas.plotting import parallel_coordinates

# 準備數據：標準化數值列
numeric_columns = ['銷售額', '利潤', '客戶數']
normalized_df = sales_data.copy()
for col in numeric_columns:
    normalized_df[col] = (sales_data[col] - sales_data[col].mean()) / sales_data[col].std()

plt.figure(figsize=(12, 8))
parallel_coordinates(normalized_df[numeric_columns + ['地區']], '地區', colormap=plt.cm.Set2)
plt.title('按地區的平行坐標圖 (標準化數據)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 4. 專業業務圖表

# %%
# 4.1 瀑布圖(Waterfall Chart)：財務變化分析
# 模擬財務數據
financial_data = {'項目': ['基礎銷售', '促銷增益', '新產品', '成本增加', '價格調整', '最終銷售'],
                 '金額': [10000, 2000, 3000, -1500, -500, 13000]}
df_financial = pd.DataFrame(financial_data)

# 計算每個項目的累積變化
df_financial['累積'] = df_financial['金額'].cumsum()
df_financial['前一個'] = df_financial['累積'].shift(1)
df_financial['前一個'].iloc[0] = 0
df_financial['類別'] = np.where(df_financial['金額']>=0, '增加', '減少')

# 瀑布圖的前後連接點
df_financial['bottom'] = np.where(df_financial['金額']>=0, 
                                 df_financial['前一個'], 
                                 df_financial['累積'])
df_financial['height'] = np.where(df_financial['金額']>=0, 
                                 df_financial['金額'], 
                                 -df_financial['金額'])

# 繪製瀑布圖
plt.figure(figsize=(12, 6))
plt.bar(df_financial['項目'], df_financial['height'], bottom=df_financial['bottom'], 
        color=df_financial['類別'].map({'增加': 'green', '減少': 'red'}), 
        edgecolor='black')

# 添加金額標籤
for i, row in df_financial.iterrows():
    plt.text(i, row['累積'] + 200, f"{row['金額']:+,.0f}", 
             ha='center', va='bottom', fontweight='bold')

# 繪製連接線
for i in range(len(df_financial) - 1):
    plt.plot([i, i+1], [df_financial['累積'].iloc[i], df_financial['前一個'].iloc[i+1]], 
             'k--', alpha=0.3)

plt.title('銷售額變化瀑布圖')
plt.ylabel('金額')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 4.2 面積圖(Area Chart)：堆疊時間序列
# 按產品類別和日期匯總銷售數據
sales_by_cat = sales_data.pivot_table(index='日期', columns='產品類別', 
                                       values='銷售額', aggfunc='sum')
# 填充缺失值
sales_by_cat = sales_by_cat.fillna(0)

# 繪製堆疊面積圖
plt.figure(figsize=(12, 6))
plt.stackplot(sales_by_cat.index, sales_by_cat.values.T, 
              labels=sales_by_cat.columns, alpha=0.8)
plt.xlabel('日期')
plt.ylabel('銷售額')
plt.title('各產品類別銷售額隨時間變化(堆疊面積圖)')
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# 4.3 雷達圖(Radar Chart)：多維度比較
# 按地區計算各績效指標平均值
radar_data = sales_data.groupby('地區').agg({
    '銷售額': 'mean',
    '利潤': 'mean',
    '客戶數': 'mean'
}).reset_index()

# 標準化數據
for col in ['銷售額', '利潤', '客戶數']:
    radar_data[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min())

# 雷達圖設置
categories = ['銷售額', '利潤', '客戶數']
N = len(categories)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # 閉合雷達圖

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

# 繪製每個地區的雷達圖
for i, region in enumerate(radar_data['地區']):
    values = radar_data.loc[i, categories].values.tolist()
    values += values[:1]  # 閉合雷達圖
    ax.plot(angles, values, linewidth=2, label=region)
    ax.fill(angles, values, alpha=0.1)

# 設置雷達圖標籤和樣式
ax.set_theta_offset(np.pi / 2)  # 從正上方開始
ax.set_theta_direction(-1)  # 順時針方向
ax.set_thetagrids(np.degrees(angles[:-1]), categories)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8'])
ax.grid(True)
plt.title('各地區績效指標比較(雷達圖)', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.tight_layout()
plt.show()

# %%
# 4.4 甘特圖(Gantt Chart)：專案排程視覺化
# 模擬專案數據
tasks = ['需求分析', '設計', '開發', '測試', '部署']
start_dates = pd.date_range('2022-01-01', periods=5, freq='7D')
durations = [7, 14, 30, 10, 5]  # 天數
colors = plt.cm.viridis(np.linspace(0, 1, len(tasks)))

# 計算結束日期
end_dates = start_dates + pd.to_timedelta(durations, unit='D')

# 繪製甘特圖
fig, ax = plt.subplots(figsize=(12, 6))

for i, task in enumerate(tasks):
    start = start_dates[i]
    duration = durations[i]
    
    ax.barh(task, duration, left=i*2, color=colors[i], 
            edgecolor='black', alpha=0.8)
    ax.text(i*2 + duration/2, i, f"{duration}天", 
            ha='center', va='center', color='white', fontweight='bold')

# 設置圖表樣式
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)
ax.set_xlabel('持續時間(天)')
ax.set_title('專案排程甘特圖')
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📋 5. 總結

# %% [markdown]
# 在本課程中，我們學習了使用Matplotlib和Pandas實現各種常見的數據視覺化圖表：
# 
# - **基本統計視覺化**：掌握了折線圖、長條圖、散點圖和餅圖等基本圖表的繪製方法，這些圖表對於基礎數據分析非常有用。
# 
# - **分佈與統計圖表**：學習了如何使用直方圖、核密度圖、箱型圖和帕累托圖等查看數據分佈和統計特性。
# 
# - **多變量關係圖表**：探索了相關性熱圖、散點矩陣圖、氣泡圖和平行坐標圖等表現多維數據關係的圖表。
# 
# - **專業業務圖表**：實作了瀑布圖、面積圖、雷達圖和甘特圖等專業圖表，這些圖表在業務分析和報告中有著廣泛應用。
# 
# 這些圖表類型為我們提供了多種展示數據的方式，選擇適合的圖表類型對於有效地傳達數據見解至關重要。在後續課程中，我們將進一步學習Seaborn庫和圖表美化技巧，使我們的視覺化更加專業和有吸引力。 