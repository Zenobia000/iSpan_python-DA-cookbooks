"""M6 Plotly 互動儀表板 — 完整解答"""
SOLUTIONS = {
    "test_green_plotly_bar": {
        "code": """df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
cat_revenue = df.groupby('category')['amount'].sum().reset_index()
return px.bar(cat_revenue, x='category', y='amount', title='各類別總營收')""",
        "explanation": "px.bar() 是 Plotly Express 的長條圖，自帶 hover 互動效果。",
    },
    "test_green_plotly_line": {
        "code": """df = pd.read_csv('datasets/ecommerce/orders_enriched.csv', parse_dates=['order_date'])
monthly = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
return px.line(monthly, x='order_date', y='amount', title='月營收趨勢')""",
        "explanation": "先 resample 聚合到月，再用 px.line() 畫折線。",
    },
    "test_green_plotly_pie": {
        "code": """df = pd.read_csv('datasets/ecommerce/orders_enriched.csv')
vip_counts = df['vip_level'].value_counts().reset_index()
vip_counts.columns = ['vip_level', 'count']
return px.pie(vip_counts, values='count', names='vip_level', title='VIP 等級佔比')""",
        "explanation": "px.pie() 的 values 是數值，names 是標籤。加 hole=0.4 可變成甜甜圈圖。",
    },
    "test_yellow_clean_and_merge": {
        "code": """df = pd.read_csv(raw_path)
df.columns = df.columns.str.strip().str.lower()
df['amount'] = df['amount'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df = df.dropna(subset=['amount', 'order_date']).drop_duplicates()

customers = pd.read_csv(customers_path)
products = pd.read_csv(products_path)
df = df.merge(customers, on='customer_id', how='left')
df = df.merge(products, on='product_id', how='left')
return df""",
        "explanation": "這是 M2 清理 + M3 合併的完整 pipeline。Capstone 就是把前面學的串起來。",
    },
    "test_yellow_kpi_summary": {
        "code": """return {
    'total_revenue': df['amount'].sum(),
    'order_count': len(df),
    'active_customers': df['customer_id'].nunique(),
    'avg_order_value': df['amount'].sum() / len(df),
}""",
        "explanation": "四個核心 KPI：總營收、訂單數、活躍客戶數（nunique）、平均客單價。",
    },
    "test_yellow_plotly_scatter": {
        "code": """return px.scatter(df, x='unit_price', y='amount',
    color='category', hover_data=['product_name'],
    title='商品單價 vs 訂單金額')""",
        "explanation": "color 按類別著色，hover_data 讓滑鼠移上去時顯示商品名稱 — 這就是 Plotly 的互動優勢。",
    },
    "test_red_dashboard_is_figure": {
        "code": """# 1. 清理 + 合併
df = yellow_clean_and_merge(
    'datasets/ecommerce/orders_raw.csv',
    'datasets/ecommerce/customers.csv',
    'datasets/ecommerce/products.csv',
)
# 2. 準備各子圖資料
monthly = df.set_index('order_date').resample('ME')['amount'].sum().reset_index()
top10 = df.groupby('product_name')['amount'].sum().nlargest(10).reset_index()
by_region = df.groupby('region')['amount'].sum().reset_index()
by_cat = df.groupby('category')['amount'].sum().reset_index()

# 3. 建立 2x2 dashboard
fig = make_subplots(rows=2, cols=2,
    subplot_titles=['月營收趨勢', 'Top 10 商品', '各地區營收', '類別佔比'],
    specs=[[{}, {}], [{}, {'type': 'domain'}]])

fig.add_trace(go.Scatter(x=monthly['order_date'], y=monthly['amount'], mode='lines'), row=1, col=1)
fig.add_trace(go.Bar(x=top10['product_name'], y=top10['amount']), row=1, col=2)
fig.add_trace(go.Bar(x=by_region['region'], y=by_region['amount']), row=2, col=1)
fig.add_trace(go.Pie(labels=by_cat['category'], values=by_cat['amount'], hole=0.4), row=2, col=2)

fig.update_layout(title_text='電商營運儀表板', showlegend=False, height=700)
return fig""",
        "explanation": "make_subplots 建立子圖網格。specs 中 {'type': 'domain'} 是給 Pie chart 用的特殊設定。\n這就是完整的資料分析 pipeline：原始資料 → 清理 → 分析 → 視覺化。",
    },
}

def format_report(results: dict) -> str:
    lines = ["## 📖 M6 Plotly 互動儀表板 — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
