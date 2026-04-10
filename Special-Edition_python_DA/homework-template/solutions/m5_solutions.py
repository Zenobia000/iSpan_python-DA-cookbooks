"""M5 Matplotlib & Seaborn 視覺化 — 完整解答"""
SOLUTIONS = {
    "test_green_bar_category": {
        "code": """df = _load_data()
fig, ax = plt.subplots(figsize=(8, 5))
df['category'].value_counts().plot.bar(ax=ax)
ax.set_title('訂單數 by Category')
return fig""",
        "explanation": "value_counts().plot.bar() 是最快的長條圖畫法。記得回傳 fig 而非 ax。",
    },
    "test_green_hist_amount": {
        "code": """df = _load_data()
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['amount'], bins=20)
return fig""",
        "explanation": "bins=20 控制分組數量。也可用 sns.histplot(data=df, x='amount', bins=20)。",
    },
    "test_green_set_labels": {
        "code": """fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C'], [10, 20, 30])
ax.set_title('範例圖表')
ax.set_xlabel('類別')
ax.set_ylabel('數值')
return fig""",
        "explanation": "set_title / set_xlabel / set_ylabel 是圖表標註的三件套。好圖表一定要有標題和軸標籤。",
    },
    "test_yellow_line_region_trend": {
        "code": """df = _load_data()
fig, ax = plt.subplots(figsize=(10, 5))
for region in ['North', 'South']:
    sub = df[df['region'] == region]
    monthly = sub.set_index('order_date').resample('ME')['amount'].sum()
    ax.plot(monthly.index, monthly.values, label=region)
ax.legend()
ax.set_title('月營收趨勢 by Region')
return fig""",
        "explanation": "分別 groupby 兩個地區，畫兩條線。ax.legend() 顯示圖例。也可用 sns.lineplot(hue='region') 一行搞定。",
    },
    "test_yellow_box_vip": {
        "code": """df = _load_data()
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x='vip_level', y='amount', ax=ax)
return fig""",
        "explanation": "箱形圖顯示分佈：中位數、四分位距、極值。一眼看出不同 VIP 等級的消費力差異。",
    },
    "test_yellow_scatter_price_amount": {
        "code": """df = _load_data()
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df['unit_price'], df['amount'], alpha=0.5)
ax.set_xlabel('Unit Price')
ax.set_ylabel('Amount')
return fig""",
        "explanation": "散佈圖看兩個數值變數的關係。alpha=0.5 讓重疊點透明，避免過度繪製。",
    },
    "test_red_category_dashboard_is_figure": {
        "code": """df = _load_data()
cat_df = df[df['category'] == category]
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 左上：月營收趨勢
monthly = cat_df.set_index('order_date').resample('ME')['amount'].sum()
axes[0, 0].plot(monthly.index, monthly.values)
axes[0, 0].set_title(f'{category} 月營收趨勢')

# 右上：各地區營收
cat_df.groupby('region')['amount'].sum().plot.bar(ax=axes[0, 1])
axes[0, 1].set_title(f'{category} 地區營收')

# 左下：Top 5 商品
cat_df.groupby('product_name')['amount'].sum().nlargest(5).plot.barh(ax=axes[1, 0])
axes[1, 0].set_title(f'{category} Top 5 商品')

# 右下：金額分佈
axes[1, 1].hist(cat_df['amount'], bins=15)
axes[1, 1].set_title(f'{category} 金額分佈')

fig.tight_layout()
return fig""",
        "explanation": "plt.subplots(2, 2) 建立 2×2 網格，axes[row, col] 指定每個子圖。tight_layout() 自動調整間距。",
    },
}

def format_report(results: dict) -> str:
    lines = ["## 📖 M5 Matplotlib & Seaborn — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
