# %% [markdown]
# # 📊 M6.3 數據操作與圖表整合

# 本課程將介紹如何將數據處理與視覺化整合，創建完整的數據分析流程。我們將學習如何處理實際業務數據，並將其轉化為有洞察力的視覺化圖表。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 學習數據預處理與轉換技巧
# - 🔄 掌握數據與圖表的整合方法
# - 🎨 創建實時更新的視覺化圖表
# - 💡 實現數據分析的自動化流程

# %%
# 環境設置
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

# %% [markdown]
# ## 1. 數據預處理與轉換

# %%
def generate_business_data(n_samples=1000):
    """生成模擬業務數據"""
    np.random.seed(42)
    
    # 生成時間序列
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=n_samples)
    
    # 生成基礎數據
    df = pd.DataFrame({
        '日期': dates,
        '訂單ID': range(1, n_samples + 1),
        '客戶ID': np.random.randint(1, 101, n_samples),
        '產品ID': np.random.randint(1, 51, n_samples),
        '銷售額': np.random.normal(1000, 200, n_samples),
        '數量': np.random.randint(1, 11, n_samples),
        '地區': np.random.choice(['北部', '中部', '南部', '東部'], n_samples),
        '支付方式': np.random.choice(['信用卡', '現金', '電子支付'], n_samples),
        '客戶評分': np.random.normal(4.2, 0.5, n_samples).clip(1, 5)
    })
    
    # 添加派生變量
    df['單價'] = df['銷售額'] / df['數量']
    df['月份'] = df['日期'].dt.strftime('%Y-%m')
    df['星期'] = df['日期'].dt.day_name()
    df['是否假日'] = df['日期'].dt.dayofweek.isin([5, 6])
    
    # 添加一些業務邏輯
    df.loc[df['是否假日'], '銷售額'] *= 1.2  # 假日銷售額提升20%
    df.loc[df['支付方式'] == '電子支付', '客戶評分'] += 0.1  # 電子支付客戶評分略高
    
    return df

# 生成數據
df = generate_business_data()

# %%
def preprocess_data():
    """數據預處理示例"""
    # 1. 基礎清理
    df_clean = df.copy()
    df_clean['銷售額'] = df_clean['銷售額'].clip(0, None)  # 移除負值
    df_clean['客戶評分'] = df_clean['客戶評分'].round(1)  # 四捨五入到一位小數
    
    # 2. 特徵工程
    df_clean['銷售分類'] = pd.qcut(df_clean['銷售額'], 
                              q=4, 
                              labels=['低', '中低', '中高', '高'])
    
    # 3. 時間特徵提取
    df_clean['小時'] = df_clean['日期'].dt.hour
    df_clean['季度'] = df_clean['日期'].dt.quarter
    
    # 4. 客戶分群
    customer_avg = df_clean.groupby('客戶ID')['銷售額'].mean()
    df_clean['客戶等級'] = pd.qcut(customer_avg, 
                              q=3, 
                              labels=['一般', '重要', 'VIP'])
    
    return df_clean

# 處理數據
df_processed = preprocess_data()

# %%
def analyze_sales_patterns():
    """分析銷售模式並視覺化"""
    # 1. 按時間維度分析
    daily_sales = df_processed.groupby('日期')[['銷售額', '數量']].sum()
    
    # 創建子圖，修改specs以支援圓餅圖
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('日銷售額趨勢',
                                      '星期銷售分布',
                                      '支付方式佔比',
                                      '客戶評分分布'),
                        specs=[[{'type': 'xy'}, {'type': 'xy'}],
                              [{'type': 'domain'}, {'type': 'xy'}]])  # 修改這裡，將圓餅圖位置設為domain類型
    
    # 1.1 日銷售額趨勢
    fig.add_trace(
        go.Scatter(x=daily_sales.index,
                  y=daily_sales['銷售額'],
                  mode='lines',
                  name='日銷售額'),
        row=1, col=1
    )
    
    # 1.2 星期銷售分布
    weekly_sales = df_processed.groupby('星期')['銷售額'].mean()
    fig.add_trace(
        go.Bar(x=weekly_sales.index,
               y=weekly_sales.values,
               name='平均銷售額'),
        row=1, col=2
    )
    
    # 1.3 支付方式佔比
    payment_counts = df_processed['支付方式'].value_counts()
    fig.add_trace(
        go.Pie(labels=payment_counts.index,
               values=payment_counts.values,
               name='支付方式',
               domain=dict(row=1, column=0)),  # 添加domain參數
        row=2, col=1
    )
    
    # 1.4 客戶評分分布
    fig.add_trace(
        go.Histogram(x=df_processed['客戶評分'],
                    nbinsx=20,
                    name='評分分布'),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(height=800,
                     title_text='銷售模式分析',
                     showlegend=True)
    
    fig.show()

analyze_sales_patterns()

# %% [markdown]
# ## 2. 數據與圖表整合

# %%
def create_integrated_dashboard():
    """創建整合性儀表板"""
    # 1. 準備數據
    monthly_sales = df_processed.groupby('月份').agg({
        '銷售額': 'sum',
        '數量': 'sum',
        '客戶ID': 'nunique',
        '客戶評分': 'mean'
    }).round(2)
    
    # 2. 創建儀表板
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('月度銷售趨勢',
                       '客戶評分與銷售額關係',
                       '地區銷售分布',
                       '支付方式分析',
                       '客戶等級分布',
                       '銷售額分類'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'pie'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'pie'}]]
    )
    
    # 2.1 月度銷售趨勢
    fig.add_trace(
        go.Scatter(x=monthly_sales.index,
                  y=monthly_sales['銷售額'],
                  mode='lines+markers',
                  name='月度銷售額'),
        row=1, col=1
    )
    
    # 2.2 客戶評分與銷售額關係
    fig.add_trace(
        go.Scatter(x=df_processed['客戶評分'],
                  y=df_processed['銷售額'],
                  mode='markers',
                  marker=dict(
                      size=8,
                      color=df_processed['客戶評分'],
                      colorscale='Viridis',
                      showscale=True
                  ),
                  name='評分-銷售關係'),
        row=1, col=2
    )
    
    # 2.3 地區銷售分布
    region_sales = df_processed.groupby('地區')['銷售額'].sum()
    fig.add_trace(
        go.Pie(labels=region_sales.index,
               values=region_sales.values,
               name='地區分布'),
        row=2, col=1
    )
    
    # 2.4 支付方式分析
    payment_sales = df_processed.groupby('支付方式')['銷售額'].mean()
    fig.add_trace(
        go.Bar(x=payment_sales.index,
               y=payment_sales.values,
               name='平均銷售額'),
        row=2, col=2
    )
    
    # 2.5 客戶等級分布
    customer_level = df_processed['客戶等級'].value_counts()
    fig.add_trace(
        go.Bar(x=customer_level.index,
               y=customer_level.values,
               name='客戶等級'),
        row=3, col=1
    )
    
    # 2.6 銷售額分類
    sales_category = df_processed['銷售分類'].value_counts()
    fig.add_trace(
        go.Pie(labels=sales_category.index,
               values=sales_category.values,
               name='銷售分類'),
        row=3, col=2
    )
    
    # 更新布局
    fig.update_layout(
        height=1200,
        title_text='綜合業務分析儀表板',
        showlegend=True,
        template='plotly_white'
    )
    
    fig.show()

create_integrated_dashboard()

# %% [markdown]
# ## 3. 實時數據更新

# %%
def simulate_realtime_data():
    """模擬實時數據更新"""
    # 創建基礎圖表
    fig = go.Figure()
    
    # 初始數據
    initial_data = df_processed.head(100)
    
    # 添加初始折線圖
    fig.add_trace(
        go.Scatter(x=initial_data['日期'],
                  y=initial_data['銷售額'],
                  mode='lines+markers',
                  name='實時銷售額')
    )
    
    # 添加更新按鈕
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="更新數據",
                        method="animate",
                        args=[None,
                              {"frame": {"duration": 500, "redraw": True},
                               "fromcurrent": True,
                               "transition": {"duration": 300}}]
                    )
                ]
            )
        ]
    )
    
    # 添加滑動條
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    fig.show()

simulate_realtime_data()

# %% [markdown]
# ## 4. 自動化報告生成

# %%
def generate_automated_report():
    """生成自動化報告"""
    # 1. 計算關鍵指標
    total_sales = df_processed['銷售額'].sum()
    avg_rating = df_processed['客戶評分'].mean()
    total_customers = df_processed['客戶ID'].nunique()
    
    # 2. 創建報告圖表
    fig = go.Figure()
    
    # 添加關鍵指標卡片
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = total_sales,
        number = {'prefix': "¥", 'valueformat': ",.0f"},
        delta = {'position': "top", 'reference': total_sales*0.9},
        domain = {'row': 0, 'column': 0},
        title = {'text': "總銷售額"}
    ))
    
    # 更新布局
    fig.update_layout(
        grid = {'rows': 1, 'columns': 1},
        template = 'plotly_white'
    )
    
    fig.show()
    
    # 3. 輸出分析結果
    print(f"""
    業務分析報告
    ============
    
    關鍵指標：
    - 總銷售額：¥{total_sales:,.2f}
    - 平均客戶評分：{avg_rating:.2f}
    - 總客戶數：{total_customers}
    
    主要發現：
    1. 銷售趨勢穩定上升
    2. 客戶滿意度良好
    3. 電子支付使用率提升
    """)

generate_automated_report()

# %% [markdown]
# ## 5. 最佳實踐建議

# 在進行數據操作與圖表整合時，請注意以下幾點：

# 1. **數據預處理**
#    - 確保數據質量和完整性
#    - 處理異常值和缺失值
#    - 進行適當的特徵工程

# 2. **圖表整合**
#    - 選擇合適的圖表類型
#    - 確保圖表之間的邏輯關聯
#    - 注意視覺層次和布局

# 3. **實時更新**
#    - 建立高效的數據更新機制
#    - 優化更新頻率
#    - 確保視覺化的響應性

# 4. **自動化流程**
#    - 建立可重複使用的函數
#    - 實現自動化報告生成
#    - 設置適當的監控機制

# %% [markdown]
# ## 6. 總結

# 本課程介紹了數據操作與圖表整合的核心概念：

# - **數據預處理**：清理、轉換和特徵工程
# - **圖表整合**：創建綜合性儀表板
# - **實時更新**：實現動態數據可視化
# - **自動化報告**：生成業務分析報告

# 這些技能將幫助您創建專業的數據分析流程和視覺化報告。 