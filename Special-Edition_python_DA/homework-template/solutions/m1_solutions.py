"""
M1 NumPy 向量化思維 — 完整解答
"""
import numpy as np

SOLUTIONS = {
    "green_mean": {
        "code": """
arr = np.array([10, 20, 30, 40, 50])
return arr.mean()       # → 30.0
""",
        "explanation": "用 .mean() 直接算平均，不需要 sum/len。",
    },
    "green_double": {
        "code": """
arr = np.array([10, 20, 30, 40, 50])
return arr * 2          # → [20, 40, 60, 80, 100]（廣播）
""",
        "explanation": "向量化：陣列直接乘以純量，NumPy 自動廣播到每個元素。",
    },
    "green_filter": {
        "code": """
arr = np.array([10, 20, 30, 40, 50])
return arr[arr > 25]    # → [30, 40, 50]（布林遮罩）
""",
        "explanation": "arr > 25 產生布林陣列 [F, F, T, T, T]，用它當索引就能篩選。",
    },
    "yellow_expensive_count": {
        "code": """
return int((prices > 1000).sum())
""",
        "explanation": "prices > 1000 產生布林陣列，True=1 / False=0，.sum() 就是計數。",
    },
    "yellow_top3_stock_indices": {
        "code": """
return np.argsort(stocks)[-3:][::-1]
""",
        "explanation": (
            "np.argsort 回傳「從小到大排序後的原始索引」，\n"
            "取最後 3 個就是最大的 3 個，[::-1] 反轉成由大到小。"
        ),
    },
    "yellow_restock_cost": {
        "code": """
cheap_mask = prices < 500
return (prices[cheap_mask] * 50).sum()
""",
        "explanation": "先用布林遮罩篩出便宜商品，乘以 50（進貨量），再 .sum() 加總。",
    },
    "red_double11_prices": {
        "code": """
return np.where(
    stocks >= 100, prices * 0.7,
    np.where(stocks >= 20, prices * 0.9, prices)
)
""",
        "explanation": (
            "np.where(條件, 真值, 假值) 可以巢狀：\n"
            "外層：庫存>=100 → 7折，否則進內層\n"
            "內層：庫存>=20 → 9折，否則原價"
        ),
    },
}


def format_report(results: dict) -> str:
    """產生解答 markdown，results = {func_name: passed}"""
    lines = ["## 📖 M1 NumPy — 完整解答\n"]
    for name, sol in SOLUTIONS.items():
        status = "✅" if results.get(name) else "❌"
        lines.append(f"### {status} `{name}`\n")
        lines.append(f"```python\n{sol['code'].strip()}\n```\n")
        lines.append(f"> {sol['explanation']}\n")
    return "\n".join(lines)
