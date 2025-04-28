# %% [markdown]
# # 📊 儀表板設計邏輯與布局

# 本課程將介紹如何設計和構建有效的數據儀表板，包括布局策略、組件設計和互動機制。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 理解儀表板設計原則
# - 🎨 掌握布局策略與技巧
# - 🔄 學習數據更新機制
# - 💡 實現互動式儀表板

# %%
# 環境設置
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

# %%
def generate_dashboard_data(n_samples=1000):
    """生成儀表板示例數據"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=n_samples)
    
    df = pd.DataFrame({
        '日期': dates,
        '銷售額': np.random.normal(1000, 200, n_samples) + np.linspace(0, 500, n_samples),
        '客戶數': np.random.randint(50, 150, n_samples),
        '滿意度': np.random.normal(4.2, 0.5, n_samples),
        '轉換率': np.random.normal(0.15, 0.03, n_samples),
        '產品類別': np.random.choice(['A', 'B', 'C', 'D'], n_samples),
        '地區': np.random.choice(['北部', '中部', '南部', '東部'], n_samples)
    })
    
    # 確保數據合理性
    df['滿意度'] = df['滿意度'].clip(1, 5)
    df['轉換率'] = df['轉換率'].clip(0, 1)
    
    return df

# %%
def kpi_cards():
    """創建KPI卡片"""
    df = generate_dashboard_data()
    
    # 計算KPI值
    total_sales = df['銷售額'].sum()
    avg_satisfaction = df['滿意度'].mean()
    total_customers = df['客戶數'].sum()
    avg_conversion = df['轉換率'].mean()
    
    # 創建KPI卡片
    fig = go.Figure()
    
    # 添加四個KPI指標
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = total_sales,
        number = {'prefix': "NT$", 'valueformat': ",.0f"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': total_sales*0.9},
        title = {'text': "總銷售額"},
        domain = {'row': 0, 'column': 0}
    ))
    
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = avg_satisfaction,
        number = {'valueformat': ".2f"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': 4.0},
        title = {'text': "平均滿意度"},
        domain = {'row': 0, 'column': 1}
    ))
    
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = total_customers,
        number = {'valueformat': ",d"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': total_customers*0.9},
        title = {'text': "總客戶數"},
        domain = {'row': 1, 'column': 0}
    ))
    
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = avg_conversion,
        number = {'valueformat': ".1%"},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': 0.12},
        title = {'text': "平均轉換率"},
        domain = {'row': 1, 'column': 1}
    ))
    
    # 更新布局
    fig.update_layout(
        grid = {'rows': 2, 'columns': 2, 'pattern': "independent"},
        height = 400,
        title_text = "關鍵績效指標 (KPI)",
        title_x = 0.5,
        showlegend = False
    )
    
    fig.show()

# %%
def create_layout_example():
    """展示不同的布局策略"""
    df = generate_dashboard_data()
    
    # 創建2x2布局的子圖，修改specs以支援圓餅圖
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('銷售趨勢', '地區分布',
                       '滿意度分析', '轉換率分布'),
        specs=[[{'secondary_y': True}, {'type': 'domain'}],  # 修改這裡，將第二個子圖設為domain類型
               [{'type': 'xy'}, {'type': 'xy'}]]
    )
    
    # 1. 銷售趨勢（折線圖）
    daily_sales = df.groupby('日期').agg({
        '銷售額': 'sum',
        '客戶數': 'sum'
    }).reset_index()
    
    fig.add_trace(
        go.Scatter(x=daily_sales['日期'],
                  y=daily_sales['銷售額'],
                  name='銷售額',
                  line=dict(color='#1f77b4')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_sales['日期'],
                  y=daily_sales['客戶數'],
                  name='客戶數',
                  line=dict(color='#ff7f0e', dash='dash')),
        row=1, col=1, secondary_y=True
    )
    
    # 2. 地區分布（圓餅圖）
    region_sales = df.groupby('地區')['銷售額'].sum()
    fig.add_trace(
        go.Pie(labels=region_sales.index,
               values=region_sales.values,
               name='地區銷售',
               domain=dict(row=0, column=1)),  # 添加domain參數
        row=1, col=2
    )
    
    # 3. 滿意度分析（箱型圖）
    fig.add_trace(
        go.Box(x=df['產品類別'],
               y=df['滿意度'],
               name='滿意度分布'),
        row=2, col=1
    )
    
    # 4. 轉換率分布（直方圖）
    fig.add_trace(
        go.Histogram(x=df['轉換率'],
                    nbinsx=30,
                    name='轉換率分布'),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        height=800,
        title_text='多維度數據分析儀表板',
        showlegend=True,
        title_x=0.5
    )
    
    # 更新軸標籤
    fig.update_xaxes(title_text='日期', row=1, col=1)
    fig.update_yaxes(title_text='銷售額', row=1, col=1)
    fig.update_yaxes(title_text='客戶數', row=1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text='產品類別', row=2, col=1)
    fig.update_yaxes(title_text='滿意度', row=2, col=1)
    
    fig.update_xaxes(title_text='轉換率', row=2, col=2)
    fig.update_yaxes(title_text='頻率', row=2, col=2)
    
    fig.show()

# %%
def demonstrate_update_mechanisms():
    """展示數據更新機制"""
    df = generate_dashboard_data()
    
    # 創建基礎圖表
    fig = go.Figure()
    
    # 添加銷售數據
    fig.add_trace(
        go.Scatter(x=df['日期'],
                  y=df['銷售額'],
                  name='銷售額',
                  mode='lines')
    )
    
    # 添加滑動條
    fig.update_layout(
        sliders=[{
            'currentvalue': {"prefix": "時間窗口: ", "suffix": " 天"},
            'steps': [
                {
                    'method': 'update',
                    'label': str(window),
                    'args': [{'visible': [True]},
                            {'title': f'最近 {window} 天銷售趨勢'}],
                }
                for window in [7, 30, 90, 180]
            ]
        }]
    )
    
    # 添加按鈕
    fig.update_layout(
        updatemenus=[{
            'type': "buttons",
            'direction': "right",
            'x': 0.7,
            'y': 1.2,
            'buttons': [
                {
                    'args': [{'type': 'scatter', 'mode': 'lines'}],
                    'label': '折線圖',
                    'method': 'restyle'
                },
                {
                    'args': [{'type': 'bar'}],
                    'label': '柱狀圖',
                    'method': 'restyle'
                }
            ]
        }]
    )
    
    # 更新布局
    fig.update_layout(
        title='動態更新銷售數據',
        xaxis_title='日期',
        yaxis_title='銷售額',
        height=600,
        title_x=0.5
    )
    
    fig.show()

# %%
def create_interactive_dashboard():
    """創建完整的互動式儀表板"""
    df = generate_dashboard_data()
    
    # 創建主圖表，修改specs以支援圓餅圖
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=('銷售趨勢', '地區分布',
                       '產品類別分析', '客戶滿意度',
                       '轉換率分析', '綜合指標'),
        specs=[[{'colspan': 2}, None],
               [{'type': 'domain'}, {'type': 'xy'}],  # 修改這裡，將圓餅圖位置設為domain類型
               [{'type': 'xy'}, {'type': 'xy'}]],
        vertical_spacing=0.12
    )
    
    # 1. 銷售趨勢
    daily_sales = df.groupby('日期')['銷售額'].sum().reset_index()
    fig.add_trace(
        go.Scatter(x=daily_sales['日期'],
                  y=daily_sales['銷售額'],
                  name='銷售額',
                  fill='tozeroy'),
        row=1, col=1
    )
    
    # 2. 地區分布
    region_sales = df.groupby('地區')['銷售額'].sum()
    fig.add_trace(
        go.Pie(labels=region_sales.index,
               values=region_sales.values,
               name='地區銷售',
               domain=dict(row=1, column=0)),  # 添加domain參數
        row=2, col=1
    )
    
    # 3. 產品類別分析
    category_sales = df.groupby('產品類別')['銷售額'].sum()
    fig.add_trace(
        go.Bar(x=category_sales.index,
               y=category_sales.values,
               name='產品銷售'),
        row=2, col=2
    )
    
    # 4. 客戶滿意度
    fig.add_trace(
        go.Box(x=df['產品類別'],
               y=df['滿意度'],
               name='滿意度分布'),
        row=3, col=1
    )
    
    # 5. 轉換率分析
    fig.add_trace(
        go.Histogram(x=df['轉換率'],
                    name='轉換率分布',
                    nbinsx=30),
        row=3, col=2
    )
    
    # 更新布局
    fig.update_layout(
        height=1200,
        title_text='綜合業務分析儀表板',
        showlegend=True,
        title_x=0.5,
        # 添加下拉選單
        updatemenus=[{
            'buttons': [
                {
                    'method': 'update',
                    'label': '日視圖',
                    'args': [{'visible': [True, True, True, True, True]}]
                },
                {
                    'method': 'update',
                    'label': '週視圖',
                    'args': [{'visible': [True, False, True, True, False]}]
                }
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.1,
            'y': 1.1
        }]
    )
    
    fig.show()

# %% [markdown]
# ## 儀表板設計最佳實踐

# 在設計數據儀表板時，請注意以下最佳實踐原則：

# 1. **資訊層級**
#    - 重要KPI放在顯眼位置
#    - 相關資訊集中展示
#    - 保持視覺層級分明

# 2. **互動設計**
#    - 提供適當的過濾器
#    - 實現合理的下鑽功能
#    - 確保響應及時

# 3. **效能優化**
#    - 控制數據載入量
#    - 優化更新機制
#    - 注意記憶體使用

# 4. **用戶體驗**
#    - 保持介面簡潔
#    - 提供清晰的導航
#    - 確保操作直覺

# %% [markdown]
# ## 總結

# 本課程介紹了儀表板設計的核心概念：

# - **KPI設計**：關鍵指標的展示方式
# - **布局策略**：多維度資訊的組織方法
# - **更新機制**：動態數據的處理方式
# - **互動設計**：用戶交互的實現方法
# - **最佳實踐**：儀表板設計原則 

# %% [markdown]
# ## 主程式執行區

# %%
if __name__ == "__main__":
    print("開始執行儀表板展示...")
    
    print("\n1. 生成示例數據")
    df = generate_dashboard_data()
    print(f"已生成 {len(df)} 筆數據")
    
    print("\n2. 展示KPI卡片")
    kpi_cards()
    
    print("\n3. 展示布局範例")
    create_layout_example()
    
    print("\n4. 展示數據更新機制")
    demonstrate_update_mechanisms()
    
    print("\n5. 展示完整互動式儀表板")
    create_interactive_dashboard()
    
    print("\n儀表板展示完成！") 