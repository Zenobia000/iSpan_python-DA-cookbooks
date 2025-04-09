# %% [markdown]
# # 📊 M6.1 Plotly快速入門

# 本課程介紹 Plotly 函式庫的基礎使用方法。Plotly 是一個強大的互動式視覺化工具，能夠創建網頁版的動態圖表。我們將學習如何使用 Plotly Express 和 Plotly Graph Objects 來創建各種互動式圖表。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 掌握 Plotly 的基本使用方法
# - 🔄 學習創建互動式圖表
# - 🎨 瞭解 Plotly Express 和 Graph Objects 的差異
# - 💡 掌握圖表客製化技巧

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

# %% [markdown]
# ## 1. Plotly Express 基礎圖表

# %%
def generate_sample_data(n_samples=1000):
    """生成示例數據"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=n_samples)
    
    df = pd.DataFrame({
        '日期': dates,
        '銷售額': np.random.normal(1000, 100, n_samples),
        '利潤': np.random.normal(200, 30, n_samples),
        '地區': np.random.choice(['北部', '中部', '南部', '東部'], n_samples),
        '產品類別': np.random.choice(['A', 'B', 'C'], n_samples)
    })
    
    # 添加一些趨勢
    df['銷售額'] = df['銷售額'] + np.linspace(0, 500, n_samples)
    
    return df

# 生成數據
df = generate_sample_data()

# %%
def basic_line_plot():
    """基本折線圖示範"""
    # 計算每日銷售額平均值
    daily_sales = df.groupby('日期')['銷售額'].mean().reset_index()
    
    # 創建互動式折線圖
    fig = px.line(daily_sales, x='日期', y='銷售額',
                  title='每日銷售額趨勢',
                  labels={'銷售額': '銷售額 (元)', '日期': '日期'},
                  template='plotly_white')
    
    # 更新布局
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        showlegend=True,
        hovermode='x unified'
    )
    
    fig.show()

basic_line_plot()

# %%
def scatter_plot():
    """散點圖示範"""
    fig = px.scatter(df, x='銷售額', y='利潤',
                    color='地區', size='銷售額',
                    title='銷售額與利潤關係散點圖',
                    labels={'銷售額': '銷售額 (元)',
                           '利潤': '利潤 (元)',
                           '地區': '地區'},
                    template='plotly_white')
    
    fig.update_layout(
        title_x=0.5,
        title_font_size=20
    )
    
    fig.show()

scatter_plot()

# %% [markdown]
# ## 2. Plotly Graph Objects 進階圖表

# %%
def advanced_bar_chart():
    """使用 Graph Objects 創建進階長條圖"""
    # 計算各地區各產品類別的平均銷售額
    region_product_sales = df.groupby(['地區', '產品類別'])['銷售額'].mean().reset_index()
    
    # 創建圖表
    fig = go.Figure()
    
    # 為每個產品類別添加長條
    for product in df['產品類別'].unique():
        product_data = region_product_sales[region_product_sales['產品類別'] == product]
        
        fig.add_trace(go.Bar(
            name=f'產品{product}',
            x=product_data['地區'],
            y=product_data['銷售額'],
            text=product_data['銷售額'].round(2),
            textposition='auto',
        ))
    
    # 更新布局
    fig.update_layout(
        title='各地區產品銷售額比較',
        title_x=0.5,
        title_font_size=20,
        barmode='group',
        template='plotly_white',
        xaxis_title='地區',
        yaxis_title='平均銷售額 (元)'
    )
    
    fig.show()

advanced_bar_chart()

# %%
def create_pie_chart():
    """圓餅圖示範"""
    # 計算各地區總銷售額
    region_sales = df.groupby('地區')['銷售額'].sum()
    
    # 創建圓餅圖
    fig = go.Figure(data=[go.Pie(
        labels=region_sales.index,
        values=region_sales.values,
        hole=0.3,  # 設置成環圈圖
        textinfo='label+percent',
        textposition='outside',
        pull=[0.1, 0, 0, 0]  # 第一個區塊突出
    )])
    
    # 更新布局
    fig.update_layout(
        title='各地區銷售額佔比',
        title_x=0.5,
        title_font_size=20,
        showlegend=True,
        template='plotly_white'
    )
    
    fig.show()

create_pie_chart()

# %% [markdown]
# ## 3. 組合圖表

# %%
def combined_charts():
    """創建組合圖表"""
    # 創建子圖
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('銷售額趨勢', '地區銷售分布',
                       '產品類別銷售額', '銷售額與利潤關係'),
        specs=[[{"type": "scatter"}, {"type": "box"}],
               [{"type": "bar"}, {"type": "scatter"}]]
    )
    
    # 1. 銷售額趨勢
    daily_sales = df.groupby('日期')['銷售額'].mean()
    fig.add_trace(
        go.Scatter(x=daily_sales.index, y=daily_sales.values,
                  mode='lines', name='銷售額趨勢'),
        row=1, col=1
    )
    
    # 2. 地區銷售分布
    fig.add_trace(
        go.Box(x=df['地區'], y=df['銷售額'], name='銷售分布'),
        row=1, col=2
    )
    
    # 3. 產品類別銷售額
    product_sales = df.groupby('產品類別')['銷售額'].mean()
    fig.add_trace(
        go.Bar(x=product_sales.index, y=product_sales.values,
               name='產品銷售額'),
        row=2, col=1
    )
    
    # 4. 銷售額與利潤關係
    fig.add_trace(
        go.Scatter(x=df['銷售額'], y=df['利潤'], mode='markers',
                  marker=dict(size=5, color='red', opacity=0.5),
                  name='銷售-利潤關係'),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        height=800,
        title_text='銷售數據綜合分析',
        title_x=0.5,
        title_font_size=20,
        showlegend=True,
        template='plotly_white'
    )
    
    fig.show()

combined_charts()

# %% [markdown]
# ## 4. 互動性設置

# %%
def interactive_chart():
    """創建具有高度互動性的圖表"""
    # 計算每日各地區銷售額
    daily_region_sales = df.groupby(['日期', '地區'])['銷售額'].sum().reset_index()
    
    # 創建具有多個互動功能的折線圖
    fig = px.line(daily_region_sales, x='日期', y='銷售額',
                  color='地區', title='各地區銷售額趨勢',
                  labels={'銷售額': '銷售額 (元)', '日期': '日期'},
                  template='plotly_white')
    
    # 添加範圍選擇器
    fig.update_xaxes(rangeslider_visible=True)
    
    # 更新布局和互動設置
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        hovermode='x unified',
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True, True, True, True]}],
                        label="顯示全部",
                        method="restyle"
                    ),
                    dict(
                        args=[{"visible": [True, False, False, False]}],
                        label="只顯示北部",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.1,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )
    
    fig.show()

interactive_chart()

# %% [markdown]
# ## 5. 圖表客製化

# %%
def customized_chart():
    """展示圖表客製化選項"""
    # 計算月度銷售數據
    monthly_data = df.groupby([df['日期'].dt.strftime('%Y-%m')])['銷售額'].agg(['mean', 'std']).reset_index()
    
    # 創建自定義圖表
    fig = go.Figure()
    
    # 添加帶有誤差範圍的折線
    fig.add_trace(go.Scatter(
        x=monthly_data['日期'],
        y=monthly_data['mean'],
        mode='lines+markers',
        name='平均銷售額',
        line=dict(color='rgb(31, 119, 180)', width=2),
        marker=dict(size=8, symbol='diamond')
    ))
    
    # 添加誤差範圍
    fig.add_trace(go.Scatter(
        name='誤差範圍',
        x=monthly_data['日期'],
        y=monthly_data['mean'] + monthly_data['std'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        name='誤差範圍',
        x=monthly_data['日期'],
        y=monthly_data['mean'] - monthly_data['std'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    ))
    
    # 客製化布局
    fig.update_layout(
        title='月度銷售額趨勢與波動範圍',
        title_x=0.5,
        title_font_size=20,
        template='plotly_white',
        xaxis_title='月份',
        yaxis_title='銷售額 (元)',
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # 客製化軸線
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    fig.show()

customized_chart()

# %% [markdown]
# ## 6. Plotly 使用技巧

# 在使用 Plotly 時，需要注意以下幾點：

# 1. **選擇適當的圖表類型**
#    - 使用 Plotly Express 快速創建基本圖表
#    - 使用 Graph Objects 進行深度客製化
#    - 根據數據特性選擇合適的視覺化方式

# 2. **互動性設計**
#    - 添加適當的工具提示
#    - 設置縮放和平移功能
#    - 加入篩選和選擇功能

# 3. **性能優化**
#    - 控制數據量
#    - 使用適當的更新方法
#    - 優化互動響應速度

# 4. **布局優化**
#    - 合理安排圖表位置
#    - 設置適當的圖表大小
#    - 注意標籤和標題的位置

# %% [markdown]
# ## 7. 總結

# 本課程介紹了 Plotly 的基礎使用方法：

# - **基本圖表**：使用 Plotly Express 快速創建圖表
# - **進階圖表**：使用 Graph Objects 進行深度客製化
# - **組合圖表**：創建多圖表儀表板
# - **互動性**：添加互動功能和動態效果
# - **客製化**：調整圖表樣式和布局

# 這些技能將幫助您創建專業的互動式數據視覺化。 