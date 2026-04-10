"""M2 Pandas 資料清理 — 完整解答"""
SOLUTIONS = {
    "test_green_read_csv": {
        "code": "return pd.read_csv('datasets/ecommerce/orders_raw.csv')",
        "explanation": "pd.read_csv() 是最基本的資料讀取方式。",
    },
    "test_green_shape": {
        "code": "return df.shape",
        "explanation": ".shape 回傳 (列數, 欄數) 的 tuple。",
    },
    "test_green_dtypes": {
        "code": "return df.dtypes",
        "explanation": ".dtypes 回傳每個欄位的資料型別。",
    },
    "test_yellow_clean_columns": {
        "code": """result = df.copy()
result.columns = result.columns.str.strip().str.lower()
return result""",
        "explanation": ".str.strip() 去除前後空白，.str.lower() 轉小寫。記得用 .copy() 避免修改原始資料。",
    },
    "test_yellow_clean_amount": {
        "code": """result = df.copy()
result['amount'] = result['amount'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).astype(float)
return result""",
        "explanation": "先用 .str.replace() 移除貨幣符號和千分位逗號，再 .astype(float) 轉數值。",
    },
    "test_yellow_drop_duplicates": {
        "code": "return df.drop_duplicates()",
        "explanation": ".drop_duplicates() 移除完全相同的列，預設保留第一筆。",
    },
    "test_red_clean_orders_returns_df": {
        "code": """df = pd.read_csv(path)
df.columns = df.columns.str.strip().str.lower()
df['amount'] = df['amount'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
df = df.dropna(subset=['amount', 'order_date'])
df = df.drop_duplicates()
return df""",
        "explanation": "完整清理 pipeline：欄位名稱 → 金額轉數值 → 日期轉 datetime → 刪缺值 → 去重複。\nerrors='coerce' 會把無法轉換的值設為 NaN/NaT，再用 dropna 統一清除。",
    },
}

def format_report(results: dict) -> str:
    lines = ["## 📖 M2 Pandas 資料清理 — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
