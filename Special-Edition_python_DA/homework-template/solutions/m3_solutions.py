"""M3 Pandas 進階 — 完整解答"""
SOLUTIONS = {
    "test_green_load_and_merge": {
        "code": """orders = pd.read_csv('datasets/ecommerce/orders_clean.csv')
customers = pd.read_csv('datasets/ecommerce/customers.csv')
products = pd.read_csv('datasets/ecommerce/products.csv')
df = orders.merge(customers, on='customer_id', how='left')
df = df.merge(products, on='product_id', how='left')
return df""",
        "explanation": "用 merge() 的 LEFT JOIN 確保保留所有訂單，即使沒有匹配的客戶或商品。",
    },
    "test_green_row_count": {
        "code": "return len(df)",
        "explanation": "len(df) 或 df.shape[0] 都可以取得列數。",
    },
    "test_green_column_list": {
        "code": "return list(df.columns)",
        "explanation": "df.columns 是 Index 物件，用 list() 轉換。",
    },
    "test_yellow_top_category": {
        "code": "return df.groupby('category')['amount'].sum().idxmax()",
        "explanation": "groupby + sum 算出每類營收，idxmax() 取最大值的 index（類別名稱）。",
    },
    "test_yellow_gold_vip_stats": {
        "code": """gold = df[df['vip_level'] == 'Gold']
return (len(gold), gold['amount'].sum())""",
        "explanation": "先用布林遮罩篩出 Gold VIP，再分別算 len() 和 .sum()。",
    },
    "test_yellow_region_avg_amount": {
        "code": "return df.groupby('region')['amount'].mean()",
        "explanation": "groupby('region') 分組，.mean() 算平均。",
    },
    "test_red_rfm_top5_shape": {
        "code": """rfm = df.groupby(['customer_id', 'customer_name']).agg(
    R=('order_date', 'max'),
    F=('order_id', 'count'),
    M=('amount', 'sum'),
).reset_index()
return rfm.sort_values('M', ascending=False).head(5)""",
        "explanation": "RFM 是客戶價值分析經典模型：\nR (Recency) = 最近一次消費日期\nF (Frequency) = 消費頻率\nM (Monetary) = 消費總金額\n用 .agg() 一次算三個指標。",
    },
}

def format_report(results: dict) -> str:
    lines = ["## 📖 M3 Pandas 進階 — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
