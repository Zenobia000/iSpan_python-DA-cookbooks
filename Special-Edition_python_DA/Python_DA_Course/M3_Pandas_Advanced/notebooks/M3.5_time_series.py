# %% [markdown]
# # 📘 M3.5 Pandas 時間序列與財務分析進階應用
# 
# 本教學將深入探討 Pandas 在時間序列數據處理與分析中的進階應用。時間序列數據在金融、經濟、銷售預測、網站流量分析等領域有著廣泛的應用，掌握高效的時間序列處理技術對於數據科學家和分析師至關重要。

# %% [markdown]
# ## 🎯 教學目標
# 
# - 🔍 深入掌握時間序列數據的高級特性與操作方法
# - 📈 學習時間序列的季節性分解、趨勢識別與異常檢測
# - 🧮 探索移動窗口函數與自定義窗口計算技術
# - 📊 掌握財務時間序列分析中的關鍵指標計算
# - 📉 運用時間序列分析解決實際業務問題
# - 🔮 實現基於歷史數據的時間序列預測模型

# %% [markdown]
# ## 🧰 1. 環境設置與數據準備

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, acf, pacf
from scipy import stats
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import statsmodels.api as sm

# 忽略特定警告
warnings.filterwarnings('ignore', category=FutureWarning)

# 設置可視化風格
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 100)
pd.set_option('display.precision', 2)
pd.set_option('display.float_format', '{:.2f}'.format)

# 設置隨機種子確保結果可重現
np.random.seed(42)

# 創建模擬時間序列數據生成函數
def generate_time_series(start_date, periods, freq='D', trend=0.2, seasonality=True, 
                         cycle_period=12, noise_level=0.05, missing_pct=0):
    """
    生成用於教學的模擬時間序列數據
    
    參數:
    - start_date: 開始日期
    - periods: 數據點數量
    - freq: 時間頻率 (D-日, B-工作日, W-週, M-月, Q-季, Y-年)
    - trend: 線性趨勢強度
    - seasonality: 是否包含季節性組件
    - cycle_period: 季節性週期
    - noise_level: 噪聲強度
    - missing_pct: 缺失值百分比
    
    返回:
    - 包含模擬數據的 Pandas Series
    """
    dates = pd.date_range(start=start_date, periods=periods, freq=freq)
    
    # 創建趨勢組件
    trend_component = np.arange(periods) * trend
    
    # 創建季節性組件
    if seasonality:
        seasonal_component = np.sin(np.arange(periods) * (2 * np.pi / cycle_period)) * 10
    else:
        seasonal_component = np.zeros(periods)
    
    # 創建噪聲組件
    noise_component = np.random.normal(0, noise_level * 10, periods)
    
    # 合併組件
    data = 100 + trend_component + seasonal_component + noise_component
    
    # 添加缺失值
    if missing_pct > 0:
        n_missing = int(periods * missing_pct / 100)
        missing_idx = np.random.choice(periods, n_missing, replace=False)
        data[missing_idx] = np.nan
    
    # 創建時間序列
    ts = pd.Series(data, index=dates, name='value')
    return ts

# %% [markdown]
# ## 📊 2. 時間序列數據的進階操作

# %%
# 生成三種不同特性的時間序列數據
daily_sales = generate_time_series('2022-01-01', 365, freq='D', trend=0.1, 
                                  seasonality=True, cycle_period=30)
monthly_revenue = generate_time_series('2015-01-01', 96, freq='M', trend=0.5, 
                                      seasonality=True, cycle_period=12)
hourly_web_traffic = generate_time_series('2023-01-01', 168, freq='H', trend=0.05, 
                                         seasonality=True, cycle_period=24, noise_level=0.2)

# 顯示數據
print("日銷售數據 (Daily Sales):")
print(daily_sales.head())
print("\n月度收入數據 (Monthly Revenue):")
print(monthly_revenue.head())
print("\n每小時網站流量 (Hourly Web Traffic):")
print(hourly_web_traffic.head())

# 可視化三個時間序列
fig, axes = plt.subplots(3, 1, figsize=(12, 12))

daily_sales.plot(ax=axes[0], title='日銷售數據 (2022年)')
axes[0].set_ylabel('銷售量')

monthly_revenue.plot(ax=axes[1], title='月度收入數據 (2015-2023年)')
axes[1].set_ylabel('收入 (千元)')

hourly_web_traffic.plot(ax=axes[2], title='每小時網站流量 (2023年1月初)')
axes[2].set_ylabel('訪問次數')

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 2.1 進階時間序列索引技術

# %%
# 從月度收入數據中選取特定時期的數據
print("2018年整年的月度收入:")
print(monthly_revenue['2018'])

print("\n2019年第一季度的月度收入:")
print(monthly_revenue['2019-01':'2019-03'])

# 使用日期偏移量進行選擇
print("\n最近3年的月度收入:")
current_date = monthly_revenue.index[-1]
three_years_ago = current_date - pd.DateOffset(years=3)
print(monthly_revenue[monthly_revenue.index >= three_years_ago])

# 使用索引的日期屬性進行篩選
summer_months = monthly_revenue[monthly_revenue.index.month.isin([6, 7, 8])]
print("\n夏季月份的平均收入:")
print(summer_months.groupby(summer_months.index.year).mean())

# 使用日期索引的多種方法
print("\n每年第四季度的收入總和:")
q4_revenue = monthly_revenue[monthly_revenue.index.quarter == 4]
print(q4_revenue.groupby(q4_revenue.index.year).sum())

# 創建包含多列的時間序列
multi_ts = pd.DataFrame({
    'Sales': daily_sales.values,
    'Website_Visits': daily_sales.values * 5 + np.random.normal(0, 10, len(daily_sales)),
    'Marketing_Spend': daily_sales.values * 0.5 + np.random.normal(0, 5, len(daily_sales))
}, index=daily_sales.index)

print("\n多變量時間序列數據:")
print(multi_ts.head())

# 計算日期之間的間隔
latest_date = monthly_revenue.index[-1]
earliest_date = monthly_revenue.index[0]
date_range = latest_date - earliest_date
print(f"\n時間序列跨度: {date_range.days} 天 (約 {date_range.days/365.25:.1f} 年)")

# %% [markdown]
# ### 2.2 處理時間戳與時區

# %%
# 創建包含時區的時間序列
timezone_example = pd.DataFrame({
    'UTC': pd.date_range('2023-01-01', periods=24, freq='H'),
    'Value': np.random.normal(100, 10, 24)
})

# 轉換為時區感知的時間戳
timezone_example['UTC'] = timezone_example['UTC'].dt.tz_localize('UTC')
timezone_example.set_index('UTC', inplace=True)

print("UTC時間的時間序列:")
print(timezone_example.head())

# 轉換為其他時區
taipei_time = timezone_example.index.tz_convert('Asia/Taipei')
new_york_time = timezone_example.index.tz_convert('America/New_York')

comparison_df = pd.DataFrame({
    'UTC時間': timezone_example.index,
    '台北時間': taipei_time,
    '紐約時間': new_york_time,
    '數值': timezone_example['Value'].values
})

print("\n跨時區時間比較:")
print(comparison_df.head())

# 在不同時區之間轉換數據
taipei_series = pd.Series(timezone_example['Value'].values, 
                         index=taipei_time, 
                         name='台北時間數值')

# 按照當地時間的小時分組
taipei_hourly_avg = taipei_series.groupby(taipei_series.index.hour).mean()
print("\n台北時間各小時的平均值:")
print(taipei_hourly_avg)

# 繪製各時區的數據
plt.figure(figsize=(12, 6))
plt.plot(timezone_example.index, timezone_example['Value'], label='UTC時間')
plt.plot(taipei_time, timezone_example['Value'], label='台北時間')
plt.legend()
plt.title('不同時區的時間序列視覺化')
plt.xlabel('時間')
plt.ylabel('數值')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 2.3 時間序列的缺失值處理

# %%
# 創建帶有缺失值的時間序列
ts_with_missing = generate_time_series('2022-01-01', 100, freq='D', 
                                      missing_pct=15, noise_level=0.1)

print("帶有缺失值的時間序列:")
print(ts_with_missing.head(10))
print(f"\n缺失值數量: {ts_with_missing.isna().sum()} (總比例: {ts_with_missing.isna().mean():.1%})")

# 可視化缺失值
plt.figure(figsize=(12, 5))
plt.plot(ts_with_missing.index, ts_with_missing.values)
plt.scatter(ts_with_missing[ts_with_missing.isna()].index, 
           [ts_with_missing.min() - 5] * ts_with_missing.isna().sum(), 
           color='red', label='缺失值')
plt.legend()
plt.title('時間序列數據中的缺失值')
plt.tight_layout()
plt.show()

# 比較各種缺失值處理方法
methods = {
    '原始數據 (含缺失)': ts_with_missing,
    '前向填充 (ffill)': ts_with_missing.ffill(),
    '後向填充 (bfill)': ts_with_missing.bfill(),
    '線性插值 (linear)': ts_with_missing.interpolate(method='linear'),
    '多項式插值 (polynomial)': ts_with_missing.interpolate(method='polynomial', order=2),
    '時間加權插值 (time)': ts_with_missing.interpolate(method='time'),
    '樣條插值 (spline)': ts_with_missing.interpolate(method='spline', order=3)
}

# 可視化比較不同填充方法
plt.figure(figsize=(14, 8))
for i, (name, data) in enumerate(methods.items(), 1):
    plt.subplot(3, 3, i)
    plt.plot(data.index, data.values)
    plt.title(name)
    plt.xticks(rotation=45)
    if i == 1:  # 只在第一張圖上標記缺失值
        plt.scatter(ts_with_missing[ts_with_missing.isna()].index, 
                   [ts_with_missing.min() - 5] * ts_with_missing.isna().sum(), 
                   color='red', s=30)
plt.tight_layout()
plt.show()

# 評估各種插值方法
# 首先創建一個完整的參考序列
complete_ts = generate_time_series('2022-01-01', 100, freq='D', missing_pct=0)
# 然後在相同位置添加缺失值
missing_idx = ts_with_missing.isna()
evaluation_ts = complete_ts.copy()
evaluation_ts[missing_idx] = np.nan

# 計算不同方法與原始值的均方誤差 (MSE)
print("\n各種插值方法的評估:")
print("-" * 50)
print(f"{'方法':<20} {'均方誤差 (MSE)':<15} {'優缺點'}")
print("-" * 50)

results = {}
for name, method in [('前向填充', 'ffill'), ('後向填充', 'bfill'), 
                     ('線性插值', 'linear'), ('多項式插值', 'polynomial'),
                     ('時間插值', 'time'), ('樣條插值', 'spline')]:
    
    # 部分方法需要額外參數
    if method in ['polynomial', 'spline']:
        filled = evaluation_ts.interpolate(method=method, order=3)
    else:
        filled = evaluation_ts.interpolate(method=method)
    
    # 計算均方誤差
    mse = ((filled[missing_idx] - complete_ts[missing_idx]) ** 2).mean()
    results[name] = mse
    
    # 優缺點
    if method == 'ffill':
        pros_cons = "優: 簡單快速, 適合階梯狀數據; 缺: 長期缺失時不準確"
    elif method == 'bfill':
        pros_cons = "優: 簡單, 適合未來已知的情況; 缺: 可能引入未來信息"
    elif method == 'linear':
        pros_cons = "優: 簡單直觀, 計算高效; 缺: 無法捕捉非線性趨勢"
    elif method == 'polynomial':
        pros_cons = "優: 可捕捉曲線趨勢; 缺: 過度擬合風險, 邊緣效應"
    elif method == 'time':
        pros_cons = "優: 考慮時間間隔, 適合不規則採樣; 缺: 僅適用於時間索引"
    elif method == 'spline':
        pros_cons = "優: 高度平滑, 適合連續變化數據; 缺: 計算複雜, 可能過度擬合"
    
    print(f"{name:<20} {mse:<15.4f} {pros_cons}")

# 找出最佳方法
best_method = min(results, key=results.get)
print(f"\n對於此數據集, 最佳插值方法為: {best_method} (MSE: {results[best_method]:.4f})")

# %% [markdown]
# ## 📊 3. 進階重採樣與頻率轉換

# %%
# 創建一個高頻時間序列 - 每分鐘的網站訪問記錄
minute_data = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=60*24, freq='T'),  # 一天的每分鐘數據
    'visits': np.random.poisson(lam=5, size=60*24)  # 泊松分布模擬訪問次數
})
minute_data.set_index('timestamp', inplace=True)

print("每分鐘網站訪問數據 (樣本):")
print(minute_data.head())
print(f"數據點總數: {len(minute_data)}")

# %% [markdown]
# ### 3.1 高級重採樣技術

# %%
# 定義各種時間窗口的重採樣
resample_rules = {
    '5分鐘': '5T',
    '小時': 'H',
    '日間 (9點-17點)': 'D',
    '工作日': 'B',
    '週': 'W',
    '月': 'M'
}

# 不同聚合方法的比較
agg_methods = ['sum', 'mean', 'median', 'min', 'max']

# 選擇一小時的數據進行詳細展示
hourly_slice = minute_data['2023-01-01 09:00:00':'2023-01-01 09:59:59']

plt.figure(figsize=(12, 6))
plt.step(hourly_slice.index, hourly_slice['visits'], where='post', label='原始每分鐘數據')

# 添加5分鐘重採樣
five_min_resampled = hourly_slice.resample('5T').sum()
plt.step(five_min_resampled.index, five_min_resampled['visits'], where='post', linewidth=2, label='5分鐘重採樣 (合計)')

plt.title('原始每分鐘數據vs 5分鐘重採樣')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 顯示不同重採樣規則和聚合方法的結果
results = {}
for rule_name, rule in resample_rules.items():
    for method in agg_methods:
        result = minute_data.resample(rule).agg(method)
        results[f"{rule_name} ({method})"] = result

# 繪製每日總訪問量
daily_visits = minute_data.resample('D').sum()
plt.figure(figsize=(12, 6))
plt.bar(daily_visits.index, daily_visits['visits'], width=0.7)
plt.title('每日網站訪問總量')
plt.xlabel('日期')
plt.ylabel('訪問次數')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 3.2 自定義重採樣與分組

# %%
# 創建工作時間與非工作時間的自定義分組
def business_nonbusiness(dt):
    if dt.weekday() < 5:  # 0-4是週一至週五
        if 9 <= dt.hour < 17:  # 9點至17點
            return '工作時間'
    return '非工作時間'

# 按自定義分組聚合
custom_grouped = minute_data.groupby(business_nonbusiness).agg(['sum', 'mean'])
print("工作時間與非工作時間的訪問統計:")
print(custom_grouped)

# 使用函數重採樣每日數據並繪製趨勢
daily_pattern = minute_data.groupby(minute_data.index.hour).mean()

plt.figure(figsize=(12, 6))
plt.plot(daily_pattern.index, daily_pattern['visits'], 'o-', linewidth=2)
plt.title('24小時訪問模式 (每小時平均)')
plt.xlabel('小時')
plt.ylabel('平均訪問次數')
plt.xticks(range(0, 24, 2))
plt.grid(True)
plt.tight_layout()
plt.show()

# 每週模式分析
# 為簡化展示，創建一個更長期的數據集
weekly_data = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=60*24*14, freq='T'),  # 兩週的每分鐘數據
    'visits': np.random.poisson(lam=5, size=60*24*14)  # 泊松分布模擬訪問次數
})
weekly_data.set_index('timestamp', inplace=True)

# 按工作日和小時分組
weekly_pattern = weekly_data.groupby([weekly_data.index.weekday, weekly_data.index.hour]).mean()
weekly_pattern = weekly_pattern.reset_index()
weekly_pattern.columns = ['weekday', 'hour', 'visits']

# 轉換為網格形式以便熱圖繪製
weekly_grid = weekly_pattern.pivot(index='hour', columns='weekday', values='visits')

# 創建星期標籤
weekday_labels = ['週一', '週二', '週三', '週四', '週五', '週六', '週日']

# 繪製熱圖
plt.figure(figsize=(12, 8))
sns.heatmap(weekly_grid, cmap='YlOrRd', linewidths=0.5, 
           xticklabels=weekday_labels, yticklabels=range(0, 24))
plt.title('週內每小時訪問模式')
plt.xlabel('星期')
plt.ylabel('小時')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 3.3 時區調整與時間偏移

# %%
# 創建跨時區的時間序列
international_data = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=24, freq='H'),
    'utc_visitors': np.random.randint(100, 500, 24)
})
international_data.set_index('timestamp', inplace=True)

# 添加時區信息 (UTC)
international_data.index = international_data.index.tz_localize('UTC')
print("UTC時區的訪客數據:")
print(international_data.head())

# 轉換為不同時區
international_data['taipei_visitors'] = international_data['utc_visitors'].shift(-8)  # 台北時間 UTC+8
international_data['ny_visitors'] = international_data['utc_visitors'].shift(5)  # 紐約時間 UTC-5
international_data['london_visitors'] = international_data['utc_visitors'].shift(0)  # 倫敦時間 UTC±0

# 檢查不同時區的訪客數據
print("\n各時區的訪客數據:")
print(international_data.head(10))

# 計算全球總訪客數 (不考慮缺失值)
international_data['global_visitors'] = international_data[['utc_visitors', 'taipei_visitors', 
                                                            'ny_visitors', 'london_visitors']].sum(axis=1, skipna=True)

# 視覺化跨時區流量分佈
plt.figure(figsize=(12, 6))
for col in ['taipei_visitors', 'ny_visitors', 'london_visitors']:
    plt.plot(international_data.index, international_data[col], label=col.split('_')[0])

plt.title('不同時區的網站訪客數量')
plt.xlabel('UTC時間')
plt.ylabel('訪客數')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 使用時間偏移量創建特殊頻率
offsets_example = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=20, freq='D')
})
offsets_example.set_index('date', inplace=True)

# 添加各種偏移日期
offsets_example['next_business_day'] = offsets_example.index + pd.offsets.BDay()
offsets_example['next_month_end'] = offsets_example.index + pd.offsets.MonthEnd()
offsets_example['next_quarter_end'] = offsets_example.index + pd.offsets.QuarterEnd()
offsets_example['same_day_next_month'] = offsets_example.index + pd.DateOffset(months=1)

print("\n各種時間偏移範例:")
print(offsets_example.head())

# %% [markdown]
# ### 3.4 不規則時間序列與近似重採樣

# %%
# 創建不規則間隔的時間序列
np.random.seed(42)
n_points = 50
irregular_timestamps = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.sort(np.random.uniform(0, 100, n_points)), unit='d')
irregular_values = np.random.normal(100, 15, n_points)
irregular_ts = pd.Series(irregular_values, index=irregular_timestamps)

print("不規則間隔的時間序列:")
print(irregular_ts.head())

# 檢查時間間隔
time_diffs = irregular_ts.index.to_series().diff().dt.total_seconds() / (60*60*24)  # 轉換為天數
print("\n時間點之間的間隔 (天):")
print(time_diffs.describe())

# 繪製不規則時間序列
plt.figure(figsize=(12, 6))
plt.plot(irregular_ts.index, irregular_ts.values, 'o-', markersize=6, linewidth=1)
plt.title('不規則間隔的時間序列')
plt.xlabel('日期')
plt.ylabel('值')
plt.grid(True)
plt.tight_layout()
plt.show()

# 使用各種方法進行重採樣
# 1. 使用asfreq()來定義固定頻率 (使用前值填充)
regular_asfreq = irregular_ts.asfreq('D', method='ffill')

# 2. 使用resample()進行重採樣
regular_resample = irregular_ts.resample('D').mean()  # 使用每日平均值

# 3. 使用Pandas的近似合併
# 創建規則頻率的空時間序列
regular_dates = pd.date_range(start=irregular_ts.index.min(), 
                             end=irregular_ts.index.max(), freq='D')
regular_df = pd.DataFrame(index=regular_dates)

# 使用merge_asof進行近似合併
regular_merge_asof = pd.merge_asof(
    regular_df,
    irregular_ts.reset_index().rename(columns={'index': 'date', 0: 'value'}),
    left_index=True,
    right_on='date',
    direction='backward'  # 使用之前最近的值
)
regular_merge_asof = regular_merge_asof['value']

# 檢查處理結果
resampling_methods = {
    '原始不規則數據': irregular_ts,
    'asfreq 方法 (前值填充)': regular_asfreq,
    'resample 方法 (平均值)': regular_resample,
    'merge_asof 方法 (近似合併)': regular_merge_asof
}

# 可視化比較不同重採樣方法
plt.figure(figsize=(12, 8))
for i, (name, data) in enumerate(resampling_methods.items(), 1):
    plt.subplot(2, 2, i)
    if name == '原始不規則數據':
        plt.plot(data.index, data.values, 'o-', markersize=6)
    else:
        plt.plot(data.index, data.values, '-')
    plt.title(name)
    plt.xticks(rotation=45)
    plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 4. 進階窗口計算與移動函數

# %%
# 創建模擬股票價格數據
stock_dates = pd.date_range(start='2022-01-01', periods=252, freq='B')  # 一年的交易日
np.random.seed(42)
# 隨機遊走模擬股票價格
price_changes = np.random.normal(0.0005, 0.01, 252)
stock_prices = 100 * np.exp(np.cumsum(price_changes))

# 創建Pandas DataFrame
stock_df = pd.DataFrame({
    'Close': stock_prices,
    'Volume': np.random.randint(100000, 1000000, 252)
}, index=stock_dates)

# 添加開盤、最高、最低價格
stock_df['Open'] = stock_df['Close'].shift(1) * (1 + np.random.normal(0, 0.002, 252))
stock_df['High'] = np.maximum(stock_df['Close'], stock_df['Open']) * (1 + np.abs(np.random.normal(0, 0.003, 252)))
stock_df['Low'] = np.minimum(stock_df['Close'], stock_df['Open']) * (1 - np.abs(np.random.normal(0, 0.003, 252)))
stock_df = stock_df[['Open', 'High', 'Low', 'Close', 'Volume']]
stock_df = stock_df.fillna(method='bfill')

print("股票OHLCV數據樣本:")
print(stock_df.head())

# 繪製股價走勢
plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['Close'])
plt.title('模擬股票價格走勢 (2022年)')
plt.xlabel('日期')
plt.ylabel('收盤價')
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 4.1 自定義窗口函數

# %%
# 定義一個自定義的窗口函數來計算波動率
def volatility(x):
    """計算價格序列的波動率 (移動標準差除以均值)"""
    return np.std(x) / np.mean(x) * 100  # 結果以百分比表示

# 定義一個函數計算布林帶
def bollinger_bands(x, window=20, num_std=2):
    """計算布林帶 (均值±標準差)"""
    mean = x.mean()
    std = x.std()
    upper = mean + num_std * std
    lower = mean - num_std * std
    return pd.Series([lower, mean, upper], index=['lower', 'mean', 'upper'])

# 定義一個函數計算相對強弱指標 (RSI)
def compute_rsi(prices, window=14):
    """計算RSI指標"""
    # 計算價格變化
    delta = prices.diff()
    
    # 分離上漲和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # 計算平均值
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # 計算相對強度
    rs = avg_gain / avg_loss
    
    # 計算RSI
    rsi = 100 - (100 / (1 + rs))
    return rsi

# 應用各種窗口計算
# 1. 計算標準移動平均線
stock_df['SMA_20'] = stock_df['Close'].rolling(window=20).mean()
stock_df['SMA_50'] = stock_df['Close'].rolling(window=50).mean()
stock_df['SMA_200'] = stock_df['Close'].rolling(window=200).mean()

# 2. 計算波動率
stock_df['Volatility_20'] = stock_df['Close'].rolling(window=20).apply(volatility)

# 3. 計算布林帶
bollinger = stock_df['Close'].rolling(window=20).apply(lambda x: bollinger_bands(x))
bollinger_df = pd.DataFrame({
    'lower': [x['lower'] for x in bollinger],
    'mean': [x['mean'] for x in bollinger],
    'upper': [x['upper'] for x in bollinger]
}, index=stock_df.index)

# 4. 計算RSI
stock_df['RSI_14'] = compute_rsi(stock_df['Close'], window=14)

# 5. 應用自定義窗口函數
def price_momentum(prices, window=20):
    """計算價格動量 (當前價格相對於窗口期初價格的變化百分比)"""
    return (prices[-1] / prices[0] - 1) * 100

stock_df['Momentum_20'] = stock_df['Close'].rolling(window=20).apply(price_momentum)

# 打印結果
print("\n應用各種窗口計算後的數據:")
print(stock_df.tail())

# 繪製股價與移動平均線
plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['Close'], label='收盤價')
plt.plot(stock_df.index, stock_df['SMA_20'], label='20日均線', linestyle='--')
plt.plot(stock_df.index, stock_df['SMA_50'], label='50日均線', linestyle='-.')
plt.plot(stock_df.index, stock_df['SMA_200'], label='200日均線', linestyle=':')
plt.title('股價與移動平均線')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 繪製布林帶
plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['Close'], label='收盤價')
plt.plot(bollinger_df.index, bollinger_df['mean'], label='20日均線', linestyle='--')
plt.fill_between(bollinger_df.index, bollinger_df['lower'], bollinger_df['upper'], alpha=0.2, label='布林帶區間')
plt.title('布林帶指標 (Bollinger Bands)')
plt.xlabel('日期')
plt.ylabel('價格')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 繪製RSI
plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['RSI_14'])
plt.axhline(y=70, color='r', linestyle='--', alpha=0.5)
plt.axhline(y=30, color='g', linestyle='--', alpha=0.5)
plt.fill_between(stock_df.index, stock_df['RSI_14'], 70, where=(stock_df['RSI_14'] >= 70), color='r', alpha=0.3)
plt.fill_between(stock_df.index, stock_df['RSI_14'], 30, where=(stock_df['RSI_14'] <= 30), color='g', alpha=0.3)
plt.title('相對強弱指標 (RSI)')
plt.xlabel('日期')
plt.ylabel('RSI值')
plt.legend(['RSI-14', '超買區域 (70+)', '超賣區域 (30-)'])
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 4.2 窗口函數與分組聚合的結合

# %%
# 創建跨市場的股票價格數據
markets = ['美國', '台灣', '日本', '歐洲']
stocks_per_market = 5
n_days = 252

multi_market_stocks = pd.DataFrame()

# 為每個市場創建股票數據
for market in markets:
    for i in range(1, stocks_per_market + 1):
        # 為不同市場設定不同的波動特性
        if market == '美國':
            mean_return = 0.0007
            volatility = 0.015
        elif market == '台灣':
            mean_return = 0.0006
            volatility = 0.018
        elif market == '日本':
            mean_return = 0.0004
            volatility = 0.014
        else:  # 歐洲
            mean_return = 0.0005
            volatility = 0.016
        
        # 生成價格序列
        np.random.seed(42 + markets.index(market) * 10 + i)
        price_changes = np.random.normal(mean_return, volatility, n_days)
        prices = 100 * np.exp(np.cumsum(price_changes))
        
        # 添加到DataFrame
        stock_id = f"{market}_{i}"
        temp_df = pd.DataFrame({
            'date': pd.date_range(start='2022-01-01', periods=n_days, freq='B'),
            'stock_id': stock_id,
            'market': market,
            'price': prices
        })
        multi_market_stocks = pd.concat([multi_market_stocks, temp_df])

# 設置索引
multi_market_stocks.set_index('date', inplace=True)

print("多市場股票價格資料:")
print(multi_market_stocks.head())
print(f"股票總數: {stocks_per_market * len(markets)}")
print(f"數據總行數: {len(multi_market_stocks)}")

# 按市場分組計算每日平均價格
market_avg = multi_market_stocks.groupby(['market', multi_market_stocks.index])['price'].mean().unstack(level=0)

# 繪製每個市場的平均價格趨勢
plt.figure(figsize=(12, 6))
for market in markets:
    plt.plot(market_avg.index, market_avg[market], label=market)
plt.title('各市場平均股票價格趨勢')
plt.xlabel('日期')
plt.ylabel('平均價格')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 結合分組和窗口計算
# 1. 計算每個市場的20日滾動收益率
market_returns = market_avg.pct_change().rolling(20).mean() * 100
market_returns = market_returns.dropna()

# 繪製20日移動平均收益率
plt.figure(figsize=(12, 6))
for market in markets:
    plt.plot(market_returns.index, market_returns[market], label=market)
plt.title('各市場20日平均收益率')
plt.xlabel('日期')
plt.ylabel('收益率 (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. 計算每個股票的波動率，然後按市場分組比較
stock_volatility = multi_market_stocks.groupby('stock_id')['price'].apply(
    lambda x: x.pct_change().rolling(20).std().mean() * 100
)
stock_volatility = stock_volatility.reset_index()
stock_volatility['market'] = stock_volatility['stock_id'].str.split('_').str[0]

# 按市場分組的波動率箱型圖
plt.figure(figsize=(12, 6))
sns.boxplot(x='market', y='price', data=stock_volatility)
plt.title('各市場股票波動率分布')
plt.xlabel('市場')
plt.ylabel('20日滾動波動率 (%)')
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# 3. 自定義分析：計算跨市場相關性
# 每個市場選擇第一支股票計算相關係數
selected_stocks = [f"{market}_1" for market in markets]
selected_data = multi_market_stocks[multi_market_stocks['stock_id'].isin(selected_stocks)]
pivot_data = selected_data.pivot(columns='stock_id', values='price')

# 計算收益率
returns = pivot_data.pct_change().dropna()

# 計算並繪製相關性熱圖
plt.figure(figsize=(10, 8))
corr_matrix = returns.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('各市場股票收益率相關性')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 4.3 滾動相關性與協方差

# %%
# 選擇兩個市場進行深入分析
market1 = '美國'
market2 = '台灣'
stock1 = f"{market1}_1"
stock2 = f"{market2}_1"

# 提取這兩個股票的數據
paired_data = multi_market_stocks[multi_market_stocks['stock_id'].isin([stock1, stock2])]
pivot_paired = paired_data.pivot(columns='stock_id', values='price')

# 計算收益率
paired_returns = pivot_paired.pct_change().dropna()

# 計算60日滾動相關性
rolling_corr = paired_returns[stock1].rolling(60).corr(paired_returns[stock2])

# 繪製滾動相關性
plt.figure(figsize=(12, 6))
plt.plot(rolling_corr.index, rolling_corr)
plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
plt.title(f'{market1}與{market2}市場股票60日滾動相關性')
plt.xlabel('日期')
plt.ylabel('相關係數')
plt.grid(True)
plt.tight_layout()
plt.show()

# 計算60日滾動協方差
rolling_cov = paired_returns[stock1].rolling(60).cov(paired_returns[stock2])

# 繪製滾動協方差
plt.figure(figsize=(12, 6))
plt.plot(rolling_cov.index, rolling_cov)
plt.title(f'{market1}與{market2}市場股票60日滾動協方差')
plt.xlabel('日期')
plt.ylabel('協方差')
plt.grid(True)
plt.tight_layout()
plt.show()

# 綜合分析：創建一個多指標圖表
fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# 繪製股票價格（歸一化以便比較）
normalized_prices = pivot_paired / pivot_paired.iloc[0]
normalized_prices.plot(ax=axes[0])
axes[0].set_title('歸一化股票價格')
axes[0].set_ylabel('價格 (基於初始值)')
axes[0].legend([f'{market1}股票', f'{market2}股票'])
axes[0].grid(True)

# 繪製滾動相關性
rolling_corr.plot(ax=axes[1])
axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.3)
axes[1].set_title('60日滾動相關性')
axes[1].set_ylabel('相關係數')
axes[1].grid(True)

# 繪製滾動波動率
rolling_vol1 = paired_returns[stock1].rolling(20).std() * np.sqrt(252) * 100  # 年化波動率
rolling_vol2 = paired_returns[stock2].rolling(20).std() * np.sqrt(252) * 100
pd.DataFrame({stock1: rolling_vol1, stock2: rolling_vol2}).plot(ax=axes[2])
axes[2].set_title('20日滾動波動率 (年化)')
axes[2].set_ylabel('波動率 (%)')
axes[2].legend([f'{market1}股票', f'{market2}股票'])
axes[2].grid(True)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 📊 5. 時間序列分解與趨勢分析

# %% [markdown]
# ### 5.1 時間序列的組成成分

# %%
# 創建一個具有明顯季節性、趨勢和噪聲的時間序列
# 使用確定性模型生成數據
np.random.seed(42)

# 生成4年的月度數據
dates = pd.date_range(start='2018-01-01', periods=48, freq='M')

# 趨勢組件: 線性增長
trend = np.linspace(100, 150, 48)

# 季節性組件: 每年的循環模式
seasonality = 15 * np.sin(np.arange(48) * (2 * np.pi / 12))

# 循環組件: 較長週期的波動
cycle = 10 * np.sin(np.arange(48) * (2 * np.pi / 24))

# 噪聲組件: 隨機波動
noise = np.random.normal(0, 5, 48)

# 組合所有組件
ts_components = pd.DataFrame({
    'trend': trend,
    'seasonality': seasonality,
    'cycle': cycle,
    'noise': noise,
    'data': trend + seasonality + cycle + noise
}, index=dates)

print("時間序列組成成分:")
print(ts_components.head())

# 繪製各個組件
fig, axes = plt.subplots(5, 1, figsize=(12, 15), sharex=True)

# 繪製原始數據
ts_components['data'].plot(ax=axes[0], title='原始時間序列數據')
axes[0].set_ylabel('數值')
axes[0].grid(True)

# 繪製趨勢組件
ts_components['trend'].plot(ax=axes[1], title='趨勢組件')
axes[1].set_ylabel('數值')
axes[1].grid(True)

# 繪製季節性組件
ts_components['seasonality'].plot(ax=axes[2], title='季節性組件')
axes[2].set_ylabel('數值')
axes[2].grid(True)

# 繪製循環組件
ts_components['cycle'].plot(ax=axes[3], title='循環組件')
axes[3].set_ylabel('數值')
axes[3].grid(True)

# 繪製噪聲組件
ts_components['noise'].plot(ax=axes[4], title='噪聲組件')
axes[4].set_ylabel('數值')
axes[4].grid(True)

plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.2 經典時間序列分解

# %%
# 使用statsmodels進行經典時間序列分解
# 加法模型: Y(t) = T(t) + S(t) + e(t)
decomposition_add = seasonal_decompose(ts_components['data'], model='additive', period=12)

# 乘法模型: Y(t) = T(t) * S(t) * e(t)
decomposition_mult = seasonal_decompose(ts_components['data'], model='multiplicative', period=12)

# 繪製加法分解結果
fig = plt.figure(figsize=(12, 10))
fig.suptitle('加法模型時間序列分解', fontsize=16)

plt.subplot(411)
plt.plot(ts_components.index, decomposition_add.observed)
plt.title('原始時間序列')
plt.grid(True)

plt.subplot(412)
plt.plot(ts_components.index, decomposition_add.trend)
plt.title('趨勢組件')
plt.grid(True)

plt.subplot(413)
plt.plot(ts_components.index, decomposition_add.seasonal)
plt.title('季節性組件')
plt.grid(True)

plt.subplot(414)
plt.plot(ts_components.index, decomposition_add.resid)
plt.title('殘差 (含循環與噪聲)')
plt.grid(True)

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

# 繪製乘法分解結果
fig = plt.figure(figsize=(12, 10))
fig.suptitle('乘法模型時間序列分解', fontsize=16)

plt.subplot(411)
plt.plot(ts_components.index, decomposition_mult.observed)
plt.title('原始時間序列')
plt.grid(True)

plt.subplot(412)
plt.plot(ts_components.index, decomposition_mult.trend)
plt.title('趨勢組件')
plt.grid(True)

plt.subplot(413)
plt.plot(ts_components.index, decomposition_mult.seasonal)
plt.title('季節性組件')
plt.grid(True)

plt.subplot(414)
plt.plot(ts_components.index, decomposition_mult.resid)
plt.title('殘差 (含循環與噪聲)')
plt.grid(True)

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()

# %% [markdown]
# ### 5.3 頻率域分析與週期識別

# %%
# 對原始數據進行去趨勢和季節性處理
detrended = ts_components['data'] - decomposition_add.trend
deseasonalized = detrended - decomposition_add.seasonal

# 繪製處理後的數據
plt.figure(figsize=(12, 6))
plt.plot(ts_components.index, ts_components['data'], label='原始數據')
plt.plot(ts_components.index, detrended, label='去除趨勢')
plt.plot(ts_components.index, deseasonalized, label='去除趨勢和季節性')
plt.title('時間序列數據預處理')
plt.xlabel('日期')
plt.ylabel('數值')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 使用FFT分析週期性
from scipy import fftpack

# 預處理: 去除缺失值並轉為標準間隔數據
values = detrended.dropna().values
N = len(values)

# 計算FFT
f_values = fftpack.fft(values)
frequencies = fftpack.fftfreq(N, d=1)  # 使用單位間隔

# 只保留正頻率
positive_frequencies = frequencies[1:N//2]
amplitudes = 2.0/N * np.abs(f_values[1:N//2])

# 繪製振幅譜
plt.figure(figsize=(12, 6))
plt.stem(positive_frequencies, amplitudes)
plt.title('頻率域分析 (FFT)')
plt.xlabel('頻率 (1/月)')
plt.ylabel('振幅')
plt.grid(True)
plt.tight_layout()
plt.show()

# 識別主要週期性
# 頻率轉換為週期 (月數)
periods = 1 / positive_frequencies
# 找出前5個主要週期
top_indices = np.argsort(amplitudes)[-5:]
top_periods = periods[top_indices]
top_amplitudes = amplitudes[top_indices]

print("\n識別出的主要週期性:")
for period, amplitude in zip(top_periods, top_amplitudes):
    if 1 <= period <= N/2:  # 只顯示合理範圍內的週期
        if abs(period - 12) < 1:  # 12個月週期 (年度)
            period_type = "年度週期"
        elif abs(period - 6) < 1:  # 6個月週期 (半年)
            period_type = "半年度週期"
        elif abs(period - 3) < 1:  # 3個月週期 (季度)
            period_type = "季度週期"
        elif abs(period - 24) < 2:  # 24個月週期 (兩年)
            period_type = "兩年度週期"
        else:
            period_type = "其他週期"
        print(f"週期: {period:.2f} 個月 (振幅: {amplitude:.2f}) - 可能是{period_type}")

# %% [markdown]
# ### 5.4 時間序列平穩性檢驗

# %%
# ADF檢驗 (Augmented Dickey-Fuller test)
def check_stationarity(time_series, window=12, title=""):
    """
    執行時間序列的平穩性檢驗
    - 繪製滾動均值和標準差
    - 執行ADF測試
    """
    # 繪製原始數據、滾動均值和標準差
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(time_series, label='原始數據')
    ax.plot(time_series.rolling(window=window).mean(), label=f'{window}個月滾動平均')
    ax.plot(time_series.rolling(window=window).std(), label=f'{window}個月滾動標準差')
    ax.set_title(f'滾動統計量 - {title}')
    ax.set_xlabel('日期')
    ax.legend()
    ax.grid(True)
    
    # ADF檢驗
    result = adfuller(time_series.dropna())
    print(f"ADF測試結果 - {title}:")
    print(f'ADF統計量: {result[0]:.4f}')
    print(f'p值: {result[1]:.4f}')
    print(f'滯後項數: {result[2]}')
    print(f'觀測值數量: {result[3]}')
    for key, value in result[4].items():
        print(f'臨界值 ({key}): {value:.4f}')
    
    # 判斷是否平穩
    if result[1] <= 0.05:
        print("結論: 序列可能是平穩的 (在5%顯著性水平下拒絕單位根存在的原假設)")
    else:
        print("結論: 序列可能是非平穩的 (不能在5%顯著性水平下拒絕單位根存在的原假設)")
    
    plt.tight_layout()
    plt.show()
    
    return result

# 對原始數據進行平穩性檢驗
print("\n原始時間序列的平穩性檢驗:")
original_adf = check_stationarity(ts_components['data'], title="原始時間序列")

# 對去趨勢數據進行平穩性檢驗
print("\n去趨勢時間序列的平穩性檢驗:")
detrended_adf = check_stationarity(detrended, title="去趨勢時間序列")

# 對去除趨勢和季節性的數據進行平穩性檢驗
print("\n去除趨勢和季節性後的時間序列平穩性檢驗:")
deseasonalized_adf = check_stationarity(deseasonalized, title="去除趨勢和季節性的時間序列")

# 差分法使時間序列平穩
diff1 = ts_components['data'].diff().dropna()  # 一階差分
print("\n一階差分後的時間序列平穩性檢驗:")
diff1_adf = check_stationarity(diff1, title="一階差分時間序列")

# 若一階差分還不夠，可以進行季節性差分
seasonal_diff = ts_components['data'].diff(12).dropna()  # 季節性差分 (12個月)
print("\n季節性差分後的時間序列平穩性檢驗:")
seasonal_diff_adf = check_stationarity(seasonal_diff, title="季節性差分時間序列")

# 繪製ACF和PACF圖 (識別ARIMA模型的參數)
def plot_acf_pacf(series, lags=40, title=""):
    """繪製ACF和PACF圖"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # ACF
    plot_acf(series.dropna(), lags=lags, ax=ax1)
    ax1.set_title(f'自相關函數 (ACF) - {title}')
    ax1.grid(True)
    
    # PACF
    plot_pacf(series.dropna(), lags=lags, ax=ax2)
    ax2.set_title(f'偏自相關函數 (PACF) - {title}')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# 對去除趨勢和季節性後的數據繪製ACF和PACF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf_pacf(deseasonalized, title="去除趨勢和季節性的時間序列") 

# %% [markdown]
# ## 🌟 8. 總結與進階資源

# %%
# 顯示本課程的總結內容
print("📚 Pandas 時間序列分析課程總結 📚")
print("=" * 50)
print("本課程中，我們深入學習了以下進階時間序列分析技術：")
print("1. 時間序列數據結構與基本操作")
print("2. 時間索引與日期範圍生成")
print("3. 時區處理與轉換")
print("4. 重採樣與頻率轉換")
print("5. 滾動窗口計算與移動平均")
print("6. 財務時間序列分析")
print("7. 實際業務案例與異常檢測")
print("=" * 50)
print("\n進階學習資源:")
print("- 官方文件: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html")
print("- 書籍推薦: 'Python for Data Analysis' by Wes McKinney")
print("- 進階課程: 'Time Series Forecasting with Python' on Various Online Learning Platforms")
print("- 相關套件: statsmodels, prophet, pmdarima, tensorflow, pytorch")

# %% [markdown]
# ## 📊 7. 實際業務案例與異常檢測

# %% [markdown]
# ### 7.1 零售銷售預測

# %%
# 創建零售銷售數據
np.random.seed(42)
date_range = pd.date_range(start='2018-01-01', end='2022-12-31', freq='D')
n_days = len(date_range)

# 基礎銷售量
base_sales = 1000

# 創建各種時間效應
# 1. 季節性：一年為週期
annual_cycle = 200 * np.sin(np.arange(n_days) * (2 * np.pi / 365))

# 2. 週效應：一週為週期 (週末銷售高)
weekday_effect = np.zeros(n_days)
for i, date in enumerate(date_range):
    if date.dayofweek >= 5:  # 週末
        weekday_effect[i] = 150
    elif date.dayofweek == 4:  # 週五
        weekday_effect[i] = 100

# 3. 節假日效應
holiday_effect = np.zeros(n_days)
for i, date in enumerate(date_range):
    # 新年
    if date.month == 1 and date.day == 1:
        holiday_effect[i] = 300
    # 農曆新年 (簡化為固定2月初)
    elif date.month == 2 and 1 <= date.day <= 5:
        holiday_effect[i] = 400
    # 清明節
    elif date.month == 4 and 4 <= date.day <= 6:
        holiday_effect[i] = 100
    # 端午節
    elif date.month == 6 and 20 <= date.day <= 22:
        holiday_effect[i] = 200
    # 中秋節
    elif date.month == 9 and 10 <= date.day <= 12:
        holiday_effect[i] = 300
    # 雙十節
    elif date.month == 10 and date.day == 10:
        holiday_effect[i] = 200
    # 聖誕節/跨年
    elif date.month == 12 and 20 <= date.day <= 31:
        holiday_effect[i] = 300 + (date.day - 20) * 20

# 4. 長期趨勢
trend = np.linspace(0, 500, n_days)  # 5年內增加500的基礎銷量

# 5. 特殊事件 (如促銷活動)
promotion_effect = np.zeros(n_days)
# 每季度促銷
for year in range(2018, 2023):
    for month in [3, 6, 9, 12]:
        # 每季度最後一個月的1號開始，持續10天
        start_idx = date_range.get_indexer([pd.Timestamp(f"{year}-{month}-01")])[0]
        promotion_effect[start_idx:start_idx+10] = 300

# 6. 隨機噪聲
noise = np.random.normal(0, 50, n_days)

# 合併所有效應
sales = base_sales + trend + annual_cycle + weekday_effect + holiday_effect + promotion_effect + noise
sales = np.maximum(sales, 0)  # 確保銷售量非負

# 創建銷售數據框
retail_data = pd.DataFrame({
    'Date': date_range,
    'Sales': sales,
    'IsWeekend': [1 if date.dayofweek >= 5 else 0 for date in date_range],
    'DayOfWeek': [date.dayofweek for date in date_range],
    'Month': [date.month for date in date_range],
    'Year': [date.year for date in date_range],
    'DayOfMonth': [date.day for date in date_range],
    'IsHoliday': [1 if effect > 0 else 0 for effect in holiday_effect],
    'IsPromotion': [1 if effect > 0 else 0 for effect in promotion_effect]
})

# 設置日期為索引
retail_data.set_index('Date', inplace=True)

print("零售銷售數據預覽:")
print(retail_data.head())
print(f"\n數據範圍: {retail_data.index.min().strftime('%Y-%m-%d')} 至 {retail_data.index.max().strftime('%Y-%m-%d')}")
print(f"數據點數量: {len(retail_data)}")

# 繪製銷售時間序列
plt.figure(figsize=(12, 6))
plt.plot(retail_data.index, retail_data['Sales'])
plt.title('零售銷售量 (2018-2022)')
plt.xlabel('日期')
plt.ylabel('銷售量')
plt.grid(True)
plt.tight_layout()
plt.show()

# 1. 基本時間序列分析
# 計算滾動平均和標準差以識別趨勢和波動
retail_data['SalesMA30'] = retail_data['Sales'].rolling(window=30).mean()
retail_data['SalesMA90'] = retail_data['Sales'].rolling(window=90).mean()
retail_data['SalesSTD30'] = retail_data['Sales'].rolling(window=30).std()

# 可視化趨勢和波動
plt.figure(figsize=(12, 8))
# 繪製銷售和移動平均
plt.subplot(2, 1, 1)
plt.plot(retail_data.index, retail_data['Sales'], alpha=0.6, label='每日銷售')
plt.plot(retail_data.index, retail_data['SalesMA30'], label='30日移動平均')
plt.plot(retail_data.index, retail_data['SalesMA90'], label='90日移動平均')
plt.title('零售銷售趨勢分析')
plt.xlabel('日期')
plt.ylabel('銷售量')
plt.legend()
plt.grid(True)

# 繪製波動性
plt.subplot(2, 1, 2)
plt.plot(retail_data.index, retail_data['SalesSTD30'], label='30日滾動標準差')
plt.title('銷售波動性分析')
plt.xlabel('日期')
plt.ylabel('標準差')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 2. 季節性分解
# 使用STL分解法將時間序列分解為趨勢、季節性和殘差
from statsmodels.tsa.seasonal import STL

# 每日數據重採樣為週數據以簡化分析
weekly_sales = retail_data['Sales'].resample('W').mean()

# STL分解 (週度數據)
stl = STL(weekly_sales, period=52)  # 52週為一年
result = stl.fit()

# 可視化分解結果
plt.figure(figsize=(12, 10))
plt.subplot(4, 1, 1)
plt.plot(result.observed)
plt.title('原始週銷售數據')
plt.subplot(4, 1, 2)
plt.plot(result.trend)
plt.title('趨勢成分')
plt.subplot(4, 1, 3)
plt.plot(result.seasonal)
plt.title('季節性成分')
plt.subplot(4, 1, 4)
plt.plot(result.resid)
plt.title('殘差成分')
plt.tight_layout()
plt.show()

# 3. 週度和月度模式分析
# 週度模式
weekly_pattern = retail_data.groupby('DayOfWeek')['Sales'].mean()
weekly_pattern = weekly_pattern / weekly_pattern.sum()

# 月度模式
monthly_pattern = retail_data.groupby('Month')['Sales'].mean()
monthly_pattern = monthly_pattern / monthly_pattern.sum()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.barplot(x=weekly_pattern.index, y=weekly_pattern.values)
plt.title('平均每週銷售模式')
plt.xlabel('星期幾 (0=週一, 6=週日)')
plt.ylabel('相對銷售比例')

plt.subplot(1, 2, 2)
sns.barplot(x=monthly_pattern.index, y=monthly_pattern.values)
plt.title('平均每月銷售模式')
plt.xlabel('月份')
plt.ylabel('相對銷售比例')
plt.tight_layout()
plt.show()

# 4. 簡單的銷售預測模型
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 選擇最近一年的數據進行預測評估
train_data = weekly_sales[:-52]
test_data = weekly_sales[-52:]

# 嘗試基本的SARIMA模型，自動尋找最佳參數
model = SARIMAX(train_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 52))
results = model.fit(disp=False)

# 生成預測
forecast = results.forecast(steps=len(test_data))

# 評估預測性能
mae = mean_absolute_error(test_data, forecast)
rmse = np.sqrt(mean_squared_error(test_data, forecast))
mape = np.mean(np.abs((test_data - forecast) / test_data)) * 100

print("\n預測評估指標:")
print(f"平均絕對誤差 (MAE): {mae:.2f}")
print(f"均方根誤差 (RMSE): {rmse:.2f}")
print(f"平均絕對百分比誤差 (MAPE): {mape:.2f}%")

# 繪製預測結果
plt.figure(figsize=(12, 6))
plt.plot(train_data.index, train_data, label='訓練數據')
plt.plot(test_data.index, test_data, label='實際銷售')
plt.plot(test_data.index, forecast, label='預測銷售')
plt.title('銷售預測模型評估')
plt.xlabel('日期')
plt.ylabel('週銷售量')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 5. 節假日和促銷效應分析
# 創建一個模型來估計各種因素對銷售的影響
import statsmodels.api as sm

# 使用日數據以捕捉節假日效應
features = retail_data[['IsWeekend', 'IsHoliday', 'IsPromotion', 'Month', 'DayOfMonth']].copy()

# 將月份和星期幾轉換為onehot編碼
month_dummies = pd.get_dummies(retail_data['Month'], prefix='Month')
dow_dummies = pd.get_dummies(retail_data['DayOfWeek'], prefix='DoW')

# 合併特徵
X = pd.concat([features, month_dummies, dow_dummies], axis=1)
y = retail_data['Sales']

# 添加常數項
X = sm.add_constant(X)

# 擬合線性模型
model = sm.OLS(y, X).fit()
print("\n銷售因素分析:")
print(model.summary().tables[1])

# 提取重要係數
coefficients = model.params
significant = model.pvalues < 0.05
significant_coef = coefficients[significant]
top_features = significant_coef.abs().sort_values(ascending=False).head(10)

# 可視化最重要的影響因素
plt.figure(figsize=(12, 6))
top_features.plot(kind='bar')
plt.title('銷售的主要影響因素')
plt.xlabel('特徵')
plt.ylabel('影響係數')
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 7.2 網站流量異常檢測

# %%
# 創建網站流量數據
np.random.seed(43)
date_range = pd.date_range(start='2022-01-01', end='2022-12-31', freq='H')
n_hours = len(date_range)

# 基礎流量
base_traffic = 1000

# 創建各種時間效應
# 1. 日內變化：人們在白天上網較多
hourly_pattern = np.zeros(24)
for hour in range(24):
    if 0 <= hour < 6:  # 凌晨
        hourly_pattern[hour] = 0.3
    elif 6 <= hour < 9:  # 早上上班前
        hourly_pattern[hour] = 0.8 + (hour - 6) * 0.2
    elif 9 <= hour < 12:  # 上午工作時間
        hourly_pattern[hour] = 1.2
    elif 12 <= hour < 14:  # 午休
        hourly_pattern[hour] = 1.4
    elif 14 <= hour < 18:  # 下午工作時間
        hourly_pattern[hour] = 1.3
    elif 18 <= hour < 22:  # 晚上休閒時間
        hourly_pattern[hour] = 1.5
    else:  # 深夜
        hourly_pattern[hour] = 0.7

daily_pattern = np.array([hourly_pattern[date.hour] for date in date_range])

# 2. 週間變化：週末流量高於工作日
weekly_pattern = np.zeros(n_hours)
for i, date in enumerate(date_range):
    if date.dayofweek >= 5:  # 週末
        weekly_pattern[i] = 1.2
    else:  # 工作日
        weekly_pattern[i] = 1.0

# 3. 長期趨勢：流量逐漸增加
trend = np.linspace(1, 1.3, n_hours)

# 4. 特殊事件：DDoS攻擊(流量異常尖峰)、服務中斷(流量驟降)、營銷活動(流量上升)
events = np.zeros(n_hours)

# DDoS攻擊 (3次)
for month in [2, 5, 10]:
    # 每次持續6小時
    start_idx = date_range.get_indexer([pd.Timestamp(f"2022-{month}-15 10:00:00")])[0]
    events[start_idx:start_idx+6] = 10.0  # 流量暴增10倍

# 服務中斷 (2次)
for month in [4, 8]:
    # 每次持續3小時
    start_idx = date_range.get_indexer([pd.Timestamp(f"2022-{month}-10 14:00:00")])[0]
    events[start_idx:start_idx+3] = -0.9  # 流量降至正常的10%

# 營銷活動 (4次)
for month in [3, 6, 9, 12]:
    # 每次持續3天
    start_idx = date_range.get_indexer([pd.Timestamp(f"2022-{month}-01 00:00:00")])[0]
    events[start_idx:start_idx+72] = 2.0  # 流量增加2倍

# 5. 隨機噪聲
noise = np.random.normal(0, 0.1, n_hours)

# 合併所有效應
traffic_multiplier = daily_pattern * weekly_pattern * trend * (1 + events)
traffic = base_traffic * traffic_multiplier * (1 + noise)
traffic = np.maximum(traffic, 0)  # 確保流量非負

# 創建網站流量數據框
traffic_data = pd.DataFrame({
    'Timestamp': date_range,
    'Traffic': traffic,
    'Hour': [date.hour for date in date_range],
    'DayOfWeek': [date.dayofweek for date in date_range],
    'Month': [date.month for date in date_range],
    'DayOfMonth': [date.day for date in date_range],
    'IsWeekend': [1 if date.dayofweek >= 5 else 0 for date in date_range]
})

# 設置時間戳為索引
traffic_data.set_index('Timestamp', inplace=True)

print("網站流量數據預覽:")
print(traffic_data.head())
print(f"\n數據範圍: {traffic_data.index.min().strftime('%Y-%m-%d %H:%M')} 至 {traffic_data.index.max().strftime('%Y-%m-%d %H:%M')}")
print(f"數據點數量: {len(traffic_data)}")

# 繪製一個月的流量時間序列以便觀察模式
start_date = '2022-03-01'
end_date = '2022-03-31'
monthly_traffic = traffic_data.loc[start_date:end_date]

plt.figure(figsize=(12, 6))
plt.plot(monthly_traffic.index, monthly_traffic['Traffic'])
plt.title(f'網站流量 ({start_date} 至 {end_date})')
plt.xlabel('日期')
plt.ylabel('流量')
plt.grid(True)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 7.3 異常檢測技術

# %%
# 使用多種方法檢測網站流量異常

# 1. 基於統計的方法 - Z-分數法
def detect_anomalies_zscore(data, column, window=24*7, threshold=3):
    """使用移動窗口Z-分數法檢測異常"""
    rolling_mean = data[column].rolling(window=window).mean()
    rolling_std = data[column].rolling(window=window).std()
    
    # 計算Z分數
    z_scores = (data[column] - rolling_mean) / rolling_std
    
    # 識別異常
    anomalies = data[abs(z_scores) > threshold].copy()
    anomalies['Z-Score'] = z_scores[abs(z_scores) > threshold]
    anomalies['Method'] = 'Z-Score'
    
    return anomalies

# 2. 移動平均法 - 檢測與趨勢的偏離
def detect_anomalies_ma(data, column, window=24*7, threshold=3):
    """使用移動平均與標準差檢測異常"""
    rolling_mean = data[column].rolling(window=window).mean()
    rolling_std = data[column].rolling(window=window).std()
    
    # 計算上下閾值
    upper_bound = rolling_mean + threshold * rolling_std
    lower_bound = rolling_mean - threshold * rolling_std
    
    # 識別異常
    anomalies = data[(data[column] > upper_bound) | (data[column] < lower_bound)].copy()
    anomalies['UpperBound'] = upper_bound[(data[column] > upper_bound) | (data[column] < lower_bound)]
    anomalies['LowerBound'] = lower_bound[(data[column] > upper_bound) | (data[column] < lower_bound)]
    anomalies['Method'] = 'Moving Average'
    
    return anomalies

# 3. 基於IQR的方法（箱形圖法則）
def detect_anomalies_iqr(data, column, window=24*7, threshold=1.5):
    """使用移動窗口IQR檢測異常"""
    results = []
    
    for i in range(window, len(data)):
        subset = data[column].iloc[i-window:i]
        q1 = subset.quantile(0.25)
        q3 = subset.quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        current_value = data[column].iloc[i]
        
        if current_value > upper_bound or current_value < lower_bound:
            results.append({
                'Timestamp': data.index[i],
                column: current_value,
                'UpperBound': upper_bound,
                'LowerBound': lower_bound,
                'Method': 'IQR'
            })
    
    return pd.DataFrame(results).set_index('Timestamp') if results else pd.DataFrame()

# 應用異常檢測方法
window_size = 24*7  # 7天滾動窗口
z_anomalies = detect_anomalies_zscore(traffic_data, 'Traffic', window=window_size, threshold=3)
ma_anomalies = detect_anomalies_ma(traffic_data, 'Traffic', window=window_size, threshold=3)
iqr_anomalies = detect_anomalies_iqr(traffic_data, 'Traffic', window=window_size, threshold=1.5)

# 合併結果
all_anomalies = pd.concat([z_anomalies, ma_anomalies, iqr_anomalies])
all_anomalies = all_anomalies[~all_anomalies.index.duplicated(keep='first')]
all_anomalies.sort_index(inplace=True)

print(f"檢測到 {len(all_anomalies)} 個異常點")
print("異常點分布:")
print(all_anomalies.groupby('Method').size())

# 可視化部分時間範圍的異常檢測結果
# 選擇具有異常的時間範圍進行可視化
start_date = '2022-05-01'
end_date = '2022-05-31'

# 篩選該時間範圍的數據
period_data = traffic_data.loc[start_date:end_date]
period_anomalies = all_anomalies.loc[start_date:end_date]

# 計算該期間的移動平均和標準差邊界
rolling_mean = period_data['Traffic'].rolling(window=window_size).mean()
rolling_std = period_data['Traffic'].rolling(window=window_size).std()
upper_bound = rolling_mean + 3 * rolling_std
lower_bound = rolling_mean - 3 * rolling_std

# 繪製原始數據、移動平均線和異常點
plt.figure(figsize=(15, 8))
plt.plot(period_data.index, period_data['Traffic'], label='流量', alpha=0.7)
plt.plot(rolling_mean.loc[start_date:end_date].index, 
         rolling_mean.loc[start_date:end_date], 
         'g--', label='移動平均')
plt.plot(upper_bound.loc[start_date:end_date].index, 
         upper_bound.loc[start_date:end_date], 
         'r--', label='上界 (3σ)')
plt.plot(lower_bound.loc[start_date:end_date].index, 
         lower_bound.loc[start_date:end_date], 
         'r--', label='下界 (3σ)')

# 標記不同類型的異常
for method in period_anomalies['Method'].unique():
    method_anomalies = period_anomalies[period_anomalies['Method'] == method]
    plt.scatter(method_anomalies.index, method_anomalies['Traffic'], 
               label=f'異常 ({method})', s=50, alpha=0.8)

plt.title(f'網站流量異常檢測 ({start_date} 至 {end_date})')
plt.xlabel('日期')
plt.ylabel('流量')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 異常分類和分析
# 將異常分類為：突增、突降和異常波動
def classify_anomalies(anomalies, data, window=24):
    """對異常進行分類"""
    classified = anomalies.copy()
    classified['AnomalyType'] = 'Unknown'
    
    for idx in classified.index:
        # 獲取當前值和前一段時間的平均值
        current_value = data.loc[idx, 'Traffic']
        if idx - pd.Timedelta(hours=window) in data.index:
            prev_window = data.loc[idx - pd.Timedelta(hours=window):idx - pd.Timedelta(hours=1)]
            if len(prev_window) > 0:
                prev_mean = prev_window['Traffic'].mean()
                percent_change = (current_value - prev_mean) / prev_mean
                
                # 分類異常
                if percent_change > 1.0:  # 流量增加超過100%
                    classified.loc[idx, 'AnomalyType'] = 'Spike'
                elif percent_change < -0.5:  # 流量減少超過50%
                    classified.loc[idx, 'AnomalyType'] = 'Drop'
                else:
                    classified.loc[idx, 'AnomalyType'] = 'Fluctuation'
    
    return classified

# 對異常進行分類
classified_anomalies = classify_anomalies(all_anomalies, traffic_data)

# 查看異常類型分布
anomaly_counts = classified_anomalies.groupby('AnomalyType').size()
print("\n異常類型分布:")
print(anomaly_counts)

# 繪製異常類型分布
plt.figure(figsize=(10, 6))
anomaly_counts.plot(kind='bar')
plt.title('網站流量異常類型分布')
plt.xlabel('異常類型')
plt.ylabel('數量')
plt.grid(True)
plt.tight_layout()
plt.show()

# 根據時間分布分析異常
# 按小時分析異常
hourly_anomalies = classified_anomalies.groupby(classified_anomalies.index.hour).size()
# 按星期幾分析異常
weekly_anomalies = classified_anomalies.groupby(classified_anomalies.index.dayofweek).size()
# 按月分析異常
monthly_anomalies = classified_anomalies.groupby(classified_anomalies.index.month).size()

plt.figure(figsize=(15, 10))
plt.subplot(3, 1, 1)
hourly_anomalies.plot(kind='bar')
plt.title('異常按小時分布')
plt.xlabel('小時')
plt.ylabel('異常數量')
plt.grid(True)

plt.subplot(3, 1, 2)
weekly_anomalies.plot(kind='bar')
plt.title('異常按星期幾分布')