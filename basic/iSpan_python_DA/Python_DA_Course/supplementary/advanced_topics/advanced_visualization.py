# %% [markdown]
# # 📊 進階資料視覺化技巧

# 本課程將介紹進階的資料視覺化技巧，包括複雜圖表製作、自定義主題、動態視覺化等進階主題。

# %% [markdown]
# ## 🎯 教學目標

# - 📈 掌握複雜圖表的製作方法
# - 🎨 學習自定義視覺化主題
# - 🔄 實現動態和互動式視覺化
# - 💡 理解視覺化最佳實踐

# %%
# 環境設置
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from plotly.colors import n_colors
import warnings

# 忽略警告
warnings.filterwarnings('ignore')

# %% [markdown]
# ## 1. 自定義主題設計

# %%
def create_custom_theme():
    """創建自定義主題"""
    # 定義自定義主題
    custom_theme = {
        'layout': {
            'font': {'family': 'Arial, sans-serif'},
            'title': {
                'font': {'size': 24, 'color': '#1f77b4'},
                'x': 0.5,
                'xanchor': 'center'
            },
            'plot_bgcolor': '#f8f9fa',
            'paper_bgcolor': '#ffffff',
            'colorway': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
            'margin': {'t': 80, 'r': 50, 'b': 50, 'l': 50},
            'showlegend': True,
            'legend': {
                'bgcolor': '#ffffff',
                'bordercolor': '#cccccc',
                'borderwidth': 1,
                'font': {'size': 12}
            }
        }
    }
    
    # 註冊自定義主題
    pio.templates['custom_theme'] = custom_theme
    pio.templates.default = 'custom_theme'

# %%
def generate_sample_data(n_samples=1000):
    """生成示例數據"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=n_samples)
    categories = ['A', 'B', 'C', 'D']
    regions = ['北部', '中部', '南部', '東部']
    
    df = pd.DataFrame({
        '日期': dates,
        '數值1': np.random.normal(100, 20, n_samples),
        '數值2': np.random.normal(50, 10, n_samples),
        '類別': np.random.choice(categories, n_samples),
        '地區': np.random.choice(regions, n_samples),
        '群組': np.random.choice(['Group1', 'Group2', 'Group3'], n_samples)
    })
    
    # 添加一些趨勢和模式
    df['數值1'] = df['數值1'] + np.linspace(0, 50, n_samples)
    df['數值2'] = df['數值2'] * (1 + np.sin(np.linspace(0, 4*np.pi, n_samples)) * 0.2)
    
    return df

# 生成數據
df = generate_sample_data()

# %% [markdown]
# ## 2. 複雜圖表製作

# %%
def create_advanced_chart():
    """創建進階複合圖表"""
    # 準備數據
    daily_values = df.groupby('日期').agg({
        '數值1': 'mean',
        '數值2': 'mean'
    }).reset_index()
    
    # 創建子圖
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('時間序列分析', '相關性分析',
                       '分布比較', '類別分析'),
        specs=[[{'secondary_y': True}, {'type': 'scatter'}],
               [{'type': 'box'}, {'type': 'bar'}]]
    )
    
    # 1. 時間序列分析（主軸和次軸）
    fig.add_trace(
        go.Scatter(x=daily_values['日期'],
                  y=daily_values['數值1'],
                  name='數值1',
                  line=dict(color='#1f77b4', width=2)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=daily_values['日期'],
                  y=daily_values['數值2'],
                  name='數值2',
                  line=dict(color='#ff7f0e', width=2,
                           dash='dash')),
        row=1, col=1, secondary_y=True
    )
    
    # 2. 相關性分析
    fig.add_trace(
        go.Scatter(x=df['數值1'],
                  y=df['數值2'],
                  mode='markers',
                  marker=dict(
                      size=8,
                      color=df['數值1'],
                      colorscale='Viridis',
                      showscale=True
                  ),
                  name='相關性'),
        row=1, col=2
    )
    
    # 3. 分布比較
    fig.add_trace(
        go.Box(x=df['地區'],
               y=df['數值1'],
               name='數值1分布'),
        row=2, col=1
    )
    
    # 4. 類別分析
    category_stats = df.groupby('類別')[['數值1', '數值2']].mean()
    fig.add_trace(
        go.Bar(x=category_stats.index,
               y=category_stats['數值1'],
               name='類別平均值'),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        height=800,
        title_text='進階數據分析圖表',
        showlegend=True,
        hovermode='closest'
    )
    
    # 更新軸標籤
    fig.update_xaxes(title_text='日期', row=1, col=1)
    fig.update_yaxes(title_text='數值1', row=1, col=1)
    fig.update_yaxes(title_text='數值2', row=1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text='數值1', row=1, col=2)
    fig.update_yaxes(title_text='數值2', row=1, col=2)
    
    fig.update_xaxes(title_text='地區', row=2, col=1)
    fig.update_yaxes(title_text='數值分布', row=2, col=1)
    
    fig.update_xaxes(title_text='類別', row=2, col=2)
    fig.update_yaxes(title_text='平均值', row=2, col=2)
    
    fig.show()

create_advanced_chart()

# %% [markdown]
# ## 3. 動態視覺化

# %%
def create_animated_chart():
    """創建動態視覺化圖表"""
    # 準備動態數據
    animated_df = df.copy()
    animated_df['月份'] = animated_df['日期'].dt.strftime('%Y-%m')
    
    monthly_stats = animated_df.groupby(['月份', '地區']).agg({
        '數值1': 'mean',
        '數值2': 'mean'
    }).reset_index()
    
    # 創建動態散點圖
    fig = px.scatter(monthly_stats,
                    x='數值1',
                    y='數值2',
                    color='地區',
                    size='數值1',
                    animation_frame='月份',
                    title='月度數據變化動態展示',
                    labels={'數值1': '指標1',
                           '數值2': '指標2',
                           '地區': '地區'},
                    range_x=[monthly_stats['數值1'].min() * 0.9,
                            monthly_stats['數值1'].max() * 1.1],
                    range_y=[monthly_stats['數值2'].min() * 0.9,
                            monthly_stats['數值2'].max() * 1.1])
    
    # 更新布局
    fig.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [{
                'label': '播放',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 500, 'redraw': True},
                               'fromcurrent': True}]
            }, {
                'label': '暫停',
                'method': 'animate',
                'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                 'mode': 'immediate',
                                 'transition': {'duration': 0}}]
            }]
        }]
    )
    
    fig.show()

create_animated_chart()

# %% [markdown]
# ## 4. 互動式儀表板

# %%
def create_interactive_dashboard():
    """創建互動式儀表板"""
    # 準備數據
    df_agg = df.groupby(['地區', '類別', '群組']).agg({
        '數值1': ['mean', 'std'],
        '數值2': ['mean', 'std']
    }).reset_index()
    
    df_agg.columns = ['地區', '類別', '群組', 
                      '數值1_平均', '數值1_標準差',
                      '數值2_平均', '數值2_標準差']
    
    # 創建互動式圖表
    fig = go.Figure()
    
    # 添加散點圖
    for group in df_agg['群組'].unique():
        mask = df_agg['群組'] == group
        fig.add_trace(
            go.Scatter(
                x=df_agg[mask]['數值1_平均'],
                y=df_agg[mask]['數值2_平均'],
                error_x=dict(type='data',
                           array=df_agg[mask]['數值1_標準差'],
                           visible=True),
                error_y=dict(type='data',
                           array=df_agg[mask]['數值2_標準差'],
                           visible=True),
                mode='markers',
                marker=dict(size=10),
                name=group,
                text=df_agg[mask]['類別'],
                hovertemplate=(
                    '群組: %{text}<br>' +
                    '數值1: %{x:.2f} ± %{error_x.array:.2f}<br>' +
                    '數值2: %{y:.2f} ± %{error_y.array:.2f}<br>'
                )
            )
        )
    
    # 添加控制按鈕
    fig.update_layout(
        updatemenus=[
            # 顯示/隱藏誤差線
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(args=[{"error_x.visible": True,
                              "error_y.visible": True}],
                         label="顯示誤差線",
                         method="restyle"
                    ),
                    dict(args=[{"error_x.visible": False,
                              "error_y.visible": False}],
                         label="隱藏誤差線",
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
            # 切換標記大小
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(args=[{"marker.size": 10}],
                         label="標準大小",
                         method="restyle"
                    ),
                    dict(args=[{"marker.size": 20}],
                         label="放大標記",
                         method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.3,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ]
    )
    
    # 更新布局
    fig.update_layout(
        title='互動式數據分析儀表板',
        xaxis_title='數值1平均值',
        yaxis_title='數值2平均值',
        hovermode='closest',
        height=600
    )
    
    fig.show()

create_interactive_dashboard()

# %% [markdown]
# ## 5. 視覺化最佳實踐

# 在進行資料視覺化時，請注意以下最佳實踐原則：

# 1. **清晰的資訊傳達**
#    - 確保圖表標題、軸標籤清晰明確
#    - 使用適當的顏色方案
#    - 避免過度裝飾

# 2. **互動性設計**
#    - 提供適當的互動控制
#    - 確保互動響應及時
#    - 保持介面直覺易用

# 3. **效能優化**
#    - 控制數據量
#    - 優化更新機制
#    - 注意記憶體使用

# 4. **適配性考慮**
#    - 支援不同螢幕尺寸
#    - 考慮載入時間
#    - 提供適當的回饋機制

# %% [markdown]
# ## 6. 總結

# 本課程介紹了進階資料視覺化的核心概念：

# - **自定義主題**：創建專業的視覺化風格
# - **複雜圖表**：製作多維度的分析圖表
# - **動態視覺化**：實現動態數據展示
# - **互動式儀表板**：打造互動性的分析工具
# - **最佳實踐**：遵循視覺化設計原則 