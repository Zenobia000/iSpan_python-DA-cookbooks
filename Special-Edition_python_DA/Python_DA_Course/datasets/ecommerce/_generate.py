"""
貫穿式電商資料集生成器（S1~S6 通用）

設計原則：
- products.csv: 乾淨資料，給 S1 NumPy 向量化用
- orders_raw.csv: 故意髒的訂單，給 S2 資料清理用（含缺值/字串數字/重複列/亂欄名）
- customers.csv: 乾淨顧客主檔，給 S3 merge/join 用

三份資料透過 product_id / customer_id 可以 join，日期橫跨 12 個月讓 S4 能做時序分析。

執行方式：python _generate.py
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)  # 讓每次產出一致，學員環境可重現

OUT_DIR = "."

# ---------- products.csv ----------
CATEGORIES = ["Electronics", "Books", "Clothing", "Home", "Sports"]
PRODUCT_NAMES = {
    "Electronics": ["Wireless Mouse", "USB-C Cable", "Bluetooth Speaker", "Webcam HD", "Laptop Stand", "Power Bank"],
    "Books":       ["Python Cookbook", "Data Science Handbook", "SQL Guide", "ML Primer", "Statistics 101", "Clean Code"],
    "Clothing":    ["Cotton T-Shirt", "Denim Jeans", "Hoodie", "Sneakers", "Cap", "Scarf"],
    "Home":        ["Coffee Mug", "Desk Lamp", "Throw Pillow", "Candle Set", "Wall Clock", "Plant Pot"],
    "Sports":      ["Yoga Mat", "Dumbbell 5kg", "Running Shoes", "Water Bottle", "Jump Rope", "Resistance Band"],
}

products = []
pid = 1001
for cat in CATEGORIES:
    for name in PRODUCT_NAMES[cat]:
        price = round(random.uniform(80, 2500), 0)
        stock = random.randint(0, 300)
        products.append({
            "product_id": pid,
            "product_name": name,
            "category": cat,
            "unit_price": int(price),
            "stock_qty": stock,
        })
        pid += 1

with open(f"{OUT_DIR}/products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["product_id", "product_name", "category", "unit_price", "stock_qty"])
    w.writeheader()
    w.writerows(products)

print(f"products.csv: {len(products)} rows")

# ---------- customers.csv ----------
REGIONS = ["North", "South", "East", "West"]
FIRST_NAMES = ["Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry",
               "Ivy", "Jack", "Kate", "Leo", "Mia", "Nick", "Olivia", "Paul",
               "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xander", "Yuki", "Zoe"]
LAST_NAMES = ["Chen", "Wang", "Liu", "Lin", "Huang"]

customers = []
for i, fn in enumerate(FIRST_NAMES):
    cid = 2001 + i
    customers.append({
        "customer_id": cid,
        "customer_name": f"{fn} {random.choice(LAST_NAMES)}",
        "region": random.choice(REGIONS),
        "signup_date": (date(2023, 1, 1) + timedelta(days=random.randint(0, 500))).isoformat(),
        "vip_level": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
    })

with open(f"{OUT_DIR}/customers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["customer_id", "customer_name", "region", "signup_date", "vip_level"])
    w.writeheader()
    w.writerows(customers)

print(f"customers.csv: {len(customers)} rows")

# ---------- orders_raw.csv (intentionally dirty) ----------
# 亂欄名：有尾端空白、大小寫不一致
HEADERS = ["Order_ID ", "customer_id", "Product_ID", " qty", "order_date", "amount"]

rows = []
start = date(2025, 1, 1)
for oid in range(5001, 5201):  # 200 orders
    customer = random.choice(customers)["customer_id"]
    product = random.choice(products)
    qty = random.randint(1, 5)
    d = start + timedelta(days=random.randint(0, 364))
    amount = product["unit_price"] * qty

    # 刻意污染資料
    # 1) ~8% 訂單日期缺失
    date_str = "" if random.random() < 0.08 else d.isoformat()
    # 2) ~15% amount 寫成帶 $ 和逗號的字串（模擬從 Excel 抓來的髒資料）
    if random.random() < 0.15:
        amount_str = f"${amount:,}"
    else:
        amount_str = str(amount)
    # 3) ~5% qty 缺失
    qty_str = "" if random.random() < 0.05 else str(qty)

    rows.append([oid, customer, product["product_id"], qty_str, date_str, amount_str])

# 4) 塞入 10 筆重複列（同一 order_id 出現兩次）
for _ in range(10):
    rows.append(random.choice(rows[:]))

# 5) 打亂順序模擬真實情況
random.shuffle(rows)

with open(f"{OUT_DIR}/orders_raw.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(rows)

print(f"orders_raw.csv: {len(rows)} rows (含 10 筆重複 + 約 8% 缺日期 + 15% 字串金額)")
print("\n全部資料集生成完畢。")
