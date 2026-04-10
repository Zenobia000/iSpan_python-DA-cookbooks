"""M4 時間序列與 EDA — 完整解答"""
SOLUTIONS = {
    "test_green_avg_by_month": {
        "code": """df = _load_data()
return df.groupby(df['order_date'].dt.month)['amount'].mean()""",
        "explanation": ".dt.month 從日期提取月份 (1~12)，再 groupby + mean。",
    },
    "test_green_top3_dates": {
        "code": """df = _load_data()
return df['order_date'].dt.date.value_counts().head(3)""",
        "explanation": ".dt.date 取日期部分（去掉時間），value_counts() 計數後預設由大到小排列。",
    },
    "test_green_date_range": {
        "code": """df = _load_data()
return (df['order_date'].min(), df['order_date'].max())""",
        "explanation": ".min() 和 .max() 直接取得最早和最晚日期。",
    },
    "test_yellow_monthly_revenue": {
        "code": """df = _load_data()
return df.set_index('order_date').resample('ME')['amount'].sum()""",
        "explanation": "set_index 把日期設為索引後，resample('ME') 按月底重取樣，.sum() 加總。",
    },
    "test_yellow_rolling_avg": {
        "code": "return monthly_revenue.rolling(window=3).mean()",
        "explanation": ".rolling(window=3) 建立 3 個月的滾動視窗，.mean() 算移動平均。前 2 筆因為不滿 3 個月會是 NaN。",
    },
    "test_yellow_category_median": {
        "code": "return df.groupby('category')['amount'].median().sort_values(ascending=False)",
        "explanation": ".median() 算中位數，sort_values(ascending=False) 由大到小排。中位數比平均更能反映「典型」訂單金額。",
    },
    "test_red_monthly_report_columns": {
        "code": """df = _load_data()
monthly = df.set_index('order_date').resample('ME').agg(
    order_count=('amount', 'count'),
    revenue=('amount', 'sum'),
    active_customers=('customer_id', 'nunique'),
)
monthly['avg_order_value'] = monthly['revenue'] / monthly['order_count']
monthly['revenue_growth'] = monthly['revenue'].pct_change()
return monthly""",
        "explanation": "resample + agg 一次算多個指標。\nnunique() 計算不重複客戶數。\npct_change() 算環比成長率（本月/上月 - 1）。",
    },
}

def format_report(results: dict) -> str:
    lines = ["## 📖 M4 時間序列與 EDA — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
