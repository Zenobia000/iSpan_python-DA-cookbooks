# %% [markdown]
# # 📘 M3.4 Pandas 進階數據合併與連接技術
# 
# 本教學將深入探討 Pandas 中數據合併(Merge)與連接(Join)的進階技術，超越基本操作以應對複雜的數據整合場景。
# 我們將學習如何處理複雜的數據關係、優化大型數據集的合併操作，以及應用這些技術解決實際業務問題。

# %% [markdown]
# ## 🎯 教學目標
# 
# - 🔍 掌握複雜數據合併策略與多種連接方式的深入應用
# - 🔄 學習驗證與診斷合併結果的技術，確保數據完整性
# - 📊 理解大數據集合併的性能優化方法
# - 🧮 探索進階合併方式，如條件合併、階層化數據連接等
# - 🛠️ 運用合併技術解決複雜業務場景的數據整合問題

# %% [markdown]
# ## 🧰 1. 環境設置

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from functools import wraps

# 設置顯示選項
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 12)
pd.set_option('display.width', 100)
pd.set_option('display.precision', 2)

# 計時裝飾器用於性能測試
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 執行時間: {(end_time - start_time):.6f} 秒")
        return result
    return wrapper

# %% [markdown]
# ## 📊 2. 創建複雜的示例數據集

# %%
# 創建更複雜的銷售數據環境
np.random.seed(42)

# 1. 客戶數據
customers = pd.DataFrame({
    'customer_id': range(1, 101),
    'customer_name': [f'Customer_{i}' for i in range(1, 101)],
    'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], 100),
    'signup_date': pd.date_range(start='2020-01-01', periods=100),
    'region_id': np.random.randint(1, 6, 100)
})

# 2. 區域數據
regions = pd.DataFrame({
    'region_id': range(1, 6),
    'region_name': ['North', 'South', 'East', 'West', 'Central'],
    'country': ['USA', 'Canada', 'UK', 'Germany', 'France'],
    'regional_manager': ['John Smith', 'Emily Johnson', 'David Brown', 'Sarah Wilson', 'Michael Lee']
})

# 3. 產品數據
products = pd.DataFrame({
    'product_id': range(101, 121),
    'product_name': [f'Product_{i}' for i in range(101, 121)],
    'category_id': np.random.randint(1, 5, 20),
    'unit_price': np.random.uniform(10, 100, 20).round(2),
    'supplier_id': np.random.randint(1, 11, 20)
})

# 4. 類別數據
categories = pd.DataFrame({
    'category_id': range(1, 5),
    'category_name': ['Electronics', 'Clothing', 'Home Goods', 'Food & Beverage'],
    'category_manager': ['Alice Johnson', 'Bob Williams', 'Carol Davis', 'Dan Miller']
})

# 5. 供應商數據
suppliers = pd.DataFrame({
    'supplier_id': range(1, 11),
    'supplier_name': [f'Supplier_{i}' for i in range(1, 11)],
    'supplier_country': np.random.choice(['USA', 'China', 'India', 'Germany', 'Japan'], 10),
    'lead_time_days': np.random.randint(5, 30, 10)
})

# 6. 訂單數據 (將創建1000筆訂單)
order_headers = pd.DataFrame({
    'order_id': range(1001, 2001),
    'customer_id': np.random.choice(customers['customer_id'], 1000),
    'order_date': pd.date_range(start='2023-01-01', periods=1000),
    'status': np.random.choice(['Completed', 'Shipped', 'Processing', 'Cancelled'], 1000, 
                              p=[0.7, 0.15, 0.1, 0.05]),
    'sales_rep_id': np.random.randint(1, 21, 1000)
})

# 7. 訂單詳情 (每個訂單平均2-5個產品項目，共約3000個訂單項目)
num_order_items = 3000
order_items = pd.DataFrame({
    'order_item_id': range(1, num_order_items + 1),
    'order_id': np.random.choice(order_headers['order_id'], num_order_items),
    'product_id': np.random.choice(products['product_id'], num_order_items),
    'quantity': np.random.randint(1, 10, num_order_items),
    'discount': np.random.choice([0, 0.05, 0.1, 0.15, 0.2], num_order_items)
})

# 8. 銷售代表數據
sales_reps = pd.DataFrame({
    'sales_rep_id': range(1, 21),
    'sales_rep_name': [f'Rep_{i}' for i in range(1, 21)],
    'region_id': np.random.randint(1, 6, 20),
    'hire_date': pd.date_range(start='2018-01-01', periods=20)
})

# 9. 支付數據 (只有已完成的訂單有支付記錄)
completed_orders = order_headers[order_headers['status'] == 'Completed']['order_id']
payments = pd.DataFrame({
    'payment_id': range(1, len(completed_orders) + 1),
    'order_id': completed_orders.values,
    'payment_date': pd.date_range(start='2023-01-05', periods=len(completed_orders)),
    'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash'], len(completed_orders)),
    'amount': np.random.uniform(50, 500, len(completed_orders)).round(2)
})

print("創建了以下數據表:")
print(f"1. 客戶 (Customers): {customers.shape[0]} 行 x {customers.shape[1]} 列")
print(f"2. 區域 (Regions): {regions.shape[0]} 行 x {regions.shape[1]} 列")
print(f"3. 產品 (Products): {products.shape[0]} 行 x {products.shape[1]} 列")
print(f"4. 類別 (Categories): {categories.shape[0]} 行 x {categories.shape[1]} 列")
print(f"5. 供應商 (Suppliers): {suppliers.shape[0]} 行 x {suppliers.shape[1]} 列")
print(f"6. 訂單標頭 (Order Headers): {order_headers.shape[0]} 行 x {order_headers.shape[1]} 列")
print(f"7. 訂單項目 (Order Items): {order_items.shape[0]} 行 x {order_items.shape[1]} 列")
print(f"8. 銷售代表 (Sales Reps): {sales_reps.shape[0]} 行 x {sales_reps.shape[1]} 列")
print(f"9. 支付 (Payments): {payments.shape[0]} 行 x {payments.shape[1]} 列")

# 查看訂單標頭與項目數據示例
print("\n訂單標頭示例:")
print(order_headers.head(3))
print("\n訂單項目示例:")
print(order_items.head(3))

# %% [markdown]
# ## 📊 3. 複雜數據關係處理

# %% [markdown]
# ### 3.1 多表關聯分析

# %%
# 建立訂單的完整視圖（訂單、客戶、產品、類別、銷售代表）
@timing_decorator
def create_order_full_view():
    # 第一步：合併訂單與訂單項目
    order_with_items = pd.merge(
        order_headers,
        order_items,
        on='order_id',
        how='inner'
    )
    
    # 第二步：加入產品信息
    order_with_products = pd.merge(
        order_with_items,
        products,
        on='product_id',
        how='inner'
    )
    
    # 第三步：加入類別信息
    order_with_categories = pd.merge(
        order_with_products,
        categories,
        on='category_id',
        how='inner'
    )
    
    # 第四步：加入客戶信息
    order_with_customers = pd.merge(
        order_with_categories,
        customers,
        on='customer_id',
        how='inner'
    )
    
    # 第五步：加入銷售代表信息
    full_order_view = pd.merge(
        order_with_customers,
        sales_reps,
        on='sales_rep_id',
        how='inner'
    )
    
    # 計算訂單項目金額
    full_order_view['item_price'] = full_order_view['unit_price'] * full_order_view['quantity'] * (1 - full_order_view['discount'])
    
    return full_order_view

# 創建完整訂單視圖
full_orders = create_order_full_view()

print(f"完整訂單視圖維度: {full_orders.shape}")
print("包含的列:")
print(full_orders.columns.tolist())
print("\n前3筆數據:")
print(full_orders.head(3))

# %% [markdown]
# ### 3.2 理解合併後數據量變化

# %%
# 分析逐步合併過程中的數據量變化
def analyze_merge_cardinality():
    # 記錄每一步合併的數據量
    steps = []
    
    # 原始訂單項目數量
    steps.append(("原始訂單項目", len(order_items)))
    
    # 步驟 1: 訂單標頭 + 訂單項目
    step1 = pd.merge(order_items, order_headers, on='order_id')
    steps.append(("訂單+訂單項目", len(step1)))
    
    # 步驟 2: + 產品
    step2 = pd.merge(step1, products, on='product_id')
    steps.append(("+ 產品", len(step2)))
    
    # 步驟 3: + 類別
    step3 = pd.merge(step2, categories, on='category_id')
    steps.append(("+ 類別", len(step3)))
    
    # 步驟 4: + 客戶
    step4 = pd.merge(step3, customers, on='customer_id')
    steps.append(("+ 客戶", len(step4)))
    
    # 步驟 5: + 銷售代表
    step5 = pd.merge(step4, sales_reps, on='sales_rep_id')
    steps.append(("+ 銷售代表", len(step5)))
    
    # 創建結果 DataFrame
    cardinality_df = pd.DataFrame(steps, columns=["合併步驟", "記錄數量"])
    cardinality_df["變化率"] = cardinality_df["記錄數量"].pct_change().fillna(0) * 100
    cardinality_df["變化率"] = cardinality_df["變化率"].map(lambda x: f"{x:.2f}%" if x != 0 else "基準")
    cardinality_df["說明"] = [
        "基準數量",
        "1:1 關係，每個訂單項目對應一個訂單",
        "1:1 關係，每個訂單項目對應一個產品",
        "1:1 關係，每個產品對應一個類別",
        "1:1 關係，每個訂單對應一個客戶",
        "1:1 關係，每個訂單對應一個銷售代表"
    ]
    
    return cardinality_df

cardinality_analysis = analyze_merge_cardinality()
print("合併過程中的數據量變化分析:")
print(cardinality_analysis)

# 可視化數據量變化
plt.figure(figsize=(12, 6))
plt.bar(cardinality_analysis["合併步驟"], cardinality_analysis["記錄數量"])
plt.title("合併過程中的數據量變化")
plt.ylabel("記錄數量")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 3.3 避免笛卡爾積問題

# %%
# 示範笛卡爾積問題
def demonstrate_cartesian_problem():
    # 創建簡單示例數據
    df1 = pd.DataFrame({
        'key': [1, 2, 3],
        'value_a': ['a1', 'a2', 'a3']
    })
    
    df2 = pd.DataFrame({
        'key': [1, 1, 1, 2, 2, 3],  # 注意這裡有重複的鍵
        'value_b': ['b1', 'b2', 'b3', 'b4', 'b5', 'b6']
    })
    
    print("DataFrame 1:")
    print(df1)
    print("\nDataFrame 2 (包含重複的鍵):")
    print(df2)
    
    # 執行內連接
    merged = pd.merge(df1, df2, on='key')
    print("\n合併結果 (產生笛卡爾積):")
    print(merged)
    print(f"合併前: df1有{len(df1)}行, df2有{len(df2)}行")
    print(f"合併後: {len(merged)}行")
    
    # 分析連接基數
    key_counts_df1 = df1['key'].value_counts().reset_index()
    key_counts_df1.columns = ['key', 'count_df1']
    
    key_counts_df2 = df2['key'].value_counts().reset_index()
    key_counts_df2.columns = ['key', 'count_df2']
    
    key_analysis = pd.merge(key_counts_df1, key_counts_df2, on='key', how='outer').fillna(0)
    key_analysis['expected_rows'] = key_analysis['count_df1'] * key_analysis['count_df2']
    
    print("\n鍵分佈分析:")
    print(key_analysis)
    print(f"預期的合併行數: {key_analysis['expected_rows'].sum()}")
    
    return df1, df2, merged

# 執行演示
df1, df2, cartesian_result = demonstrate_cartesian_problem()

# 提供避免笛卡爾積的方法
print("\n避免笛卡爾積的方法:")
print("1. 在合併前檢查並刪除重複的鍵值:")
df2_unique = df2.drop_duplicates(subset=['key'])
safe_merge = pd.merge(df1, df2_unique, on='key')
print(f"   去除重複後合併: {len(safe_merge)}行")

print("2. 使用 merge 前的驗證函數:")
def validate_merge_keys(df1, df2, key):
    df1_key_counts = df1[key].value_counts()
    df2_key_counts = df2[key].value_counts()
    
    potential_explosion = 0
    for k in df1_key_counts.index:
        if k in df2_key_counts.index:
            potential_explosion += df1_key_counts[k] * df2_key_counts[k]
    
    print(f"   合併前: df1有{len(df1)}行, df2有{len(df2)}行")
    print(f"   潛在合併結果: {potential_explosion}行")
    
    explosion_factor = potential_explosion / (len(df1) + len(df2))
    print(f"   爆炸因子: {explosion_factor:.2f}x")
    
    if explosion_factor > 2:
        print("   警告: 可能發生大量數據膨脹!")
        return False
    return True

print("\n驗證合併鍵:")
is_safe = validate_merge_keys(df1, df2, 'key')

# %% [markdown]
# ## 📊 4. 合併驗證與診斷技術

# %% [markdown]
# ### 4.1 驗證合併操作的完整性

# %%
# 檢查合併是否遺漏數據
def check_merge_completeness(left_df, right_df, merged_df, left_on, right_on=None, how='inner'):
    if right_on is None:
        right_on = left_on
    
    # 計算預期的結果大小
    if how == 'inner':
        left_keys = set(left_df[left_on])
        right_keys = set(right_df[right_on])
        common_keys = left_keys.intersection(right_keys)
        
        left_matched = left_df[left_df[left_on].isin(common_keys)]
        right_matched = right_df[right_df[right_on].isin(common_keys)]
        
        expected_rows = len(left_matched) if len(left_matched) <= len(right_matched) else len(right_matched)
        if len(left_matched) > 0 and len(right_matched) > 0:
            # 對於多對多關係，計算上限
            left_counts = left_matched[left_on].value_counts()
            right_counts = right_matched[right_on].value_counts()
            max_rows = sum(left_counts[k] * right_counts[k] for k in common_keys if k in left_counts and k in right_counts)
            expected_rows = max_rows
    
    elif how == 'left':
        expected_rows = len(left_df)
    elif how == 'right':
        expected_rows = len(right_df)
    elif how == 'outer':
        # 外連接可能比較複雜，這裡簡化處理
        expected_rows = len(left_df) + len(right_df) - len(set(left_df[left_on]).intersection(set(right_df[right_on])))
    
    actual_rows = len(merged_df)
    
    print(f"合併完整性檢查 ({how} join):")
    print(f"左表行數: {len(left_df)}")
    print(f"右表行數: {len(right_df)}")
    print(f"合併結果行數: {actual_rows}")
    print(f"預期結果行數 (約): {expected_rows}")
    
    if how in ['left', 'right', 'outer']:
        # 檢查空值情況
        if how == 'left' or how == 'outer':
            null_count = merged_df[right_df.columns[0]].isna().sum()
            print(f"右表列中的空值數: {null_count} ({null_count/len(merged_df):.2%})")
        
        if how == 'right' or how == 'outer':
            null_count = merged_df[left_df.columns[0]].isna().sum()
            print(f"左表列中的空值數: {null_count} ({null_count/len(merged_df):.2%})")
    
    return {
        'left_rows': len(left_df),
        'right_rows': len(right_df),
        'merged_rows': actual_rows,
        'expected_rows': expected_rows,
        'match_rate': actual_rows / expected_rows if expected_rows > 0 else 0
    }

# 示範合併驗證
orders_sample = order_headers.sample(100, random_state=42)
customers_sample = customers.sample(50, random_state=42)

# 執行左連接
left_join = pd.merge(orders_sample, customers_sample, on='customer_id', how='left')

# 驗證合併結果
merge_stats = check_merge_completeness(orders_sample, customers_sample, left_join, 'customer_id', how='left')

# %% [markdown]
# ### 4.2 合併後數據一致性驗證

# %%
# 合併後的數據一致性檢查
def validate_merge_consistency(original_df1, original_df2, merged_df, key):
    """檢查合併後的數據是否與原始數據集一致"""
    # 檢查鍵的唯一性
    print("檢查合併鍵的唯一性:")
    print(f"左表 '{key}' 唯一值數量: {original_df1[key].nunique()}")
    print(f"右表 '{key}' 唯一值數量: {original_df2[key].nunique()}")
    print(f"合併表 '{key}' 唯一值數量: {merged_df[key].nunique()}")
    
    # 檢查聚合指標是否保持一致
    print("\n檢查數值列的聚合指標:")
    
    # 選擇數值列
    numeric_cols1 = original_df1.select_dtypes(include=['number']).columns
    numeric_cols2 = original_df2.select_dtypes(include=['number']).columns
    
    # 排除合併鍵
    numeric_cols1 = [col for col in numeric_cols1 if col != key]
    numeric_cols2 = [col for col in numeric_cols2 if col != key]
    
    # 檢查左表的數值列
    for col in numeric_cols1[:2]:  # 僅檢查前兩列作為示例
        if col in merged_df.columns:
            orig_sum = original_df1[col].sum()
            merged_sum = merged_df[col].sum()
            
            print(f"列 '{col}' 總和 - 原始: {orig_sum}, 合併後: {merged_sum}, 差異: {abs(orig_sum - merged_sum)}")
    
    # 檢查右表的數值列
    for col in numeric_cols2[:2]:  # 僅檢查前兩列作為示例
        if col in merged_df.columns:
            orig_sum = original_df2[col].sum()
            merged_sum = merged_df[col].sum()
            
            print(f"列 '{col}' 總和 - 原始: {orig_sum}, 合併後: {merged_sum}, 差異: {abs(orig_sum - merged_sum)}")
    
    # 檢查每個合併鍵值的行數一致性
    print("\n檢查各鍵值的行數:")
    key_counts_orig1 = original_df1[key].value_counts().sort_index()
    key_counts_orig2 = original_df2[key].value_counts().sort_index()
    key_counts_merged = merged_df[key].value_counts().sort_index()
    
    # 取樣展示幾個鍵值
    sample_keys = sorted(list(set(key_counts_orig1.index) & set(key_counts_orig2.index)))[:3]
    
    for k in sample_keys:
        count1 = key_counts_orig1.get(k, 0)
        count2 = key_counts_orig2.get(k, 0)
        count_merged = key_counts_merged.get(k, 0)
        
        print(f"鍵值 {k}: 左表 {count1} 行, 右表 {count2} 行, 合併表 {count_merged} 行")
        
        # 如果是一對多或多對多關係，解釋預期行數
        if count1 > 1 or count2 > 1:
            expected = count1 * count2
            print(f"  預期行數: {count1} x {count2} = {expected}")
    
    return True

# 示範驗證
validate_merge_consistency(orders_sample, customers, left_join, 'customer_id')

# %% [markdown]
# ## 📊 5. 高性能合併技術

# %% [markdown]
# ### 5.1 大數據集合併優化

# %%
# 創建較大的測試數據集
def create_large_test_data(size=1000000):
    """創建大型測試數據集用於性能測試"""
    np.random.seed(42)
    large_df1 = pd.DataFrame({
        'id': np.arange(size),
        'key': np.random.randint(0, size // 10, size),
        'value_a': np.random.randn(size)
    })
    
    large_df2 = pd.DataFrame({
        'key': np.random.randint(0, size // 10, size // 5),
        'value_b': np.random.randn(size // 5)
    })
    
    return large_df1, large_df2

# 較小規模測試 (為了演示，使用較小的數據集)
large_df1, large_df2 = create_large_test_data(size=100000)

print(f"大型數據集 1: {large_df1.shape}")
print(f"大型數據集 2: {large_df2.shape}")

# 性能測試：未優化的合併
@timing_decorator
def merge_unoptimized(df1, df2):
    return pd.merge(df1, df2, on='key')

# 性能測試：預排序優化
@timing_decorator
def merge_presorted(df1, df2):
    df1_sorted = df1.sort_values('key')
    df2_sorted = df2.sort_values('key')
    return pd.merge(df1_sorted, df2_sorted, on='key', sort=False)

# 性能測試：類別優化
@timing_decorator
def merge_category(df1, df2):
    df1_cat = df1.copy()
    df2_cat = df2.copy()
    df1_cat['key'] = df1_cat['key'].astype('category')
    df2_cat['key'] = df2_cat['key'].astype('category')
    return pd.merge(df1_cat, df2_cat, on='key')

# 性能測試：分塊處理
@timing_decorator
def merge_chunked(df1, df2, chunk_size=20000):
    result_chunks = []
    
    # 根據 chunk_size 分割第一個 DataFrame
    for i in range(0, len(df1), chunk_size):
        chunk = df1.iloc[i:i+chunk_size]
        # 合併每個塊與第二個 DataFrame
        merged_chunk = pd.merge(chunk, df2, on='key')
        result_chunks.append(merged_chunk)
    
    # 將所有塊連接成最終結果
    return pd.concat(result_chunks, ignore_index=True)

# 運行性能測試
print("\n性能測試結果:")
result1 = merge_unoptimized(large_df1, large_df2)
result2 = merge_presorted(large_df1, large_df2)
result3 = merge_category(large_df1, large_df2)
result4 = merge_chunked(large_df1, large_df2)

print(f"\n合併結果行數 (檢查結果一致性):")
print(f"未優化: {len(result1)}")
print(f"預排序: {len(result2)}")
print(f"類別化: {len(result3)}")
print(f"分塊處理: {len(result4)}")

# %% [markdown]
# ### 5.2 使用 SQL 進行合併 (超大數據集)

# %%
# 使用 SQLite 演示超大數據集合併
import sqlite3
from io import StringIO

@timing_decorator
def merge_with_sql(df1, df2, key):
    """使用 SQLite 進行大數據集合併"""
    # 創建臨時的內存數據庫連接
    conn = sqlite3.connect(':memory:')
    
    # 將 DataFrames 寫入 SQLite 表
    df1.to_sql('table1', conn, index=False, if_exists='replace')
    df2.to_sql('table2', conn, index=False, if_exists='replace')
    
    # 創建索引以加速合併
    conn.execute(f'CREATE INDEX idx_table1_{key} ON table1({key})')
    conn.execute(f'CREATE INDEX idx_table2_{key} ON table2({key})')
    
    # 編寫合併查詢
    query = f"""
    SELECT *
    FROM table1 t1
    INNER JOIN table2 t2 ON t1.{key} = t2.{key}
    """
    
    # 執行查詢並返回結果
    result = pd.read_sql_query(query, conn)
    
    # 關閉連接
    conn.close()
    
    return result

# 運行 SQL 合併測試
result_sql = merge_with_sql(large_df1, large_df2, 'key')
print(f"SQL合併結果行數: {len(result_sql)}")

# 比較合併方法的性能（不同規模的數據集）
def compare_merge_performance():
    results = []
    
    for size in [10000, 50000, 100000]:
        df1, df2 = create_large_test_data(size)
        
        # 測量未優化合併的時間
        start = time.time()
        pd.merge(df1, df2, on='key')
        time_unoptimized = time.time() - start
        
        # 測量預排序合併的時間
        start = time.time()
        df1_sorted = df1.sort_values('key')
        df2_sorted = df2.sort_values('key')
        pd.merge(df1_sorted, df2_sorted, on='key', sort=False)
        time_presorted = time.time() - start
        
        # 測量 SQL 合併的時間
        start = time.time()
        merge_with_sql(df1, df2, 'key')
        time_sql = time.time() - start
        
        results.append({
            'size': size,
            'unoptimized': time_unoptimized,
            'presorted': time_presorted,
            'sql': time_sql
        })
    
    return pd.DataFrame(results)

# 創建性能比較結果
performance_results = compare_merge_performance()
print("\n不同規模數據集的合併性能比較:")
print(performance_results)

# 可視化比較結果
plt.figure(figsize=(12, 6))
for method in ['unoptimized', 'presorted', 'sql']:
    plt.plot(performance_results['size'], performance_results[method], marker='o', label=method)
plt.title('不同合併方法的性能比較')
plt.xlabel('數據集大小')
plt.ylabel('執行時間 (秒)')
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# ## 📊 6. 進階特殊合併技術

# %% [markdown]
# ### 6.1 條件式合併

# %%
# 演示條件式合併
print("條件式合併 (Conditional Merge)")

# 創建價格表 (根據日期和產品的價格表)
price_history = pd.DataFrame({
    'product_id': np.repeat(np.arange(1, 6), 3),  # 5個產品，每個有3個不同的價格歷史
    'start_date': pd.to_datetime([
        '2023-01-01', '2023-04-01', '2023-07-01',  # 產品1
        '2023-01-01', '2023-03-01', '2023-06-01',  # 產品2
        '2023-01-01', '2023-05-01', '2023-08-01',  # 產品3
        '2023-01-01', '2023-02-01', '2023-09-01',  # 產品4
        '2023-01-01', '2023-06-01', '2023-10-01'   # 產品5
    ]),
    'end_date': pd.to_datetime([
        '2023-03-31', '2023-06-30', '2023-12-31',  # 產品1
        '2023-02-28', '2023-05-31', '2023-12-31',  # 產品2
        '2023-04-30', '2023-07-31', '2023-12-31',  # 產品3
        '2023-01-31', '2023-08-31', '2023-12-31',  # 產品4
        '2023-05-31', '2023-09-30', '2023-12-31'   # 產品5
    ]),
    'unit_price': [
        10.0, 12.0, 15.0,  # 產品1
        20.0, 22.0, 25.0,  # 產品2
        30.0, 28.0, 32.0,  # 產品3
        15.0, 18.0, 20.0,  # 產品4
        25.0, 30.0, 35.0   # 產品5
    ]
})

# 創建訂單資料，包含日期和產品
sample_orders = pd.DataFrame({
    'order_id': np.arange(1001, 1011),
    'product_id': np.random.randint(1, 6, 10),  # 隨機選擇產品
    'order_date': pd.to_datetime([
        '2023-02-15', '2023-03-20', '2023-04-10', '2023-05-05', '2023-06-15',
        '2023-07-20', '2023-08-10', '2023-09-05', '2023-10-15', '2023-11-20'
    ]),
    'quantity': np.random.randint(1, 10, 10)
})

print("價格歷史表:")
print(price_history.head())
print("\n訂單表:")
print(sample_orders)

# 條件式合併：根據日期範圍合併正確的價格
def merge_with_date_condition(orders, prices):
    """根據訂單日期在價格區間內進行條件式合併"""
    merged_data = []
    
    for _, order in orders.iterrows():
        order_date = order['order_date']
        product_id = order['product_id']
        
        # 找出適用的價格記錄
        applicable_price = prices[
            (prices['product_id'] == product_id) & 
            (prices['start_date'] <= order_date) & 
            (prices['end_date'] >= order_date)
        ]
        
        if not applicable_price.empty:
            # 將訂單與價格資訊合併
            order_dict = order.to_dict()
            order_dict.update({
                'unit_price': applicable_price.iloc[0]['unit_price'],
                'price_start_date': applicable_price.iloc[0]['start_date'],
                'price_end_date': applicable_price.iloc[0]['end_date']
            })
            merged_data.append(order_dict)
        else:
            # 沒有找到適用的價格
            order_dict = order.to_dict()
            order_dict.update({
                'unit_price': None,
                'price_start_date': None,
                'price_end_date': None
            })
            merged_data.append(order_dict)
    
    return pd.DataFrame(merged_data)

# 執行條件式合併
@timing_decorator
def perform_conditional_merge():
    return merge_with_date_condition(sample_orders, price_history)

conditional_merged = perform_conditional_merge()
print("\n條件式合併結果:")
print(conditional_merged[['order_id', 'product_id', 'order_date', 'quantity', 'unit_price']])
conditional_merged['total_amount'] = conditional_merged['quantity'] * conditional_merged['unit_price']
print("\n計算總金額後:")
print(conditional_merged[['order_id', 'product_id', 'quantity', 'unit_price', 'total_amount']])

# %% [markdown]
# ### 6.2 使用 pd.merge_asof 進行近似合併

# %%
# 使用 merge_asof 進行近似合併 (類似資料庫中的近似連接)
print("近似合併 (Merge Asof)")

# 創建股票價格時間序列
np.random.seed(42)
stock_prices = pd.DataFrame({
    'timestamp': pd.date_range('2023-01-01', periods=10, freq='D'),
    'stock_price': np.random.randn(10).cumsum() + 100  # 模擬股票價格
})

# 創建訂單時間序列 (時間與股票價格不完全匹配)
trade_orders = pd.DataFrame({
    'timestamp': pd.to_datetime([
        '2023-01-01 12:30:00', '2023-01-02 09:15:00', 
        '2023-01-03 16:45:00', '2023-01-05 10:30:00',
        '2023-01-07 14:20:00', '2023-01-08 11:05:00'
    ]),
    'order_id': ['A001', 'A002', 'A003', 'A004', 'A005', 'A006'],
    'quantity': [100, 150, 200, 120, 180, 250]
})

print("股票價格時間序列:")
print(stock_prices)
print("\n訂單時間序列:")
print(trade_orders)

# 確保數據已排序 (merge_asof 要求按合併鍵排序)
stock_prices = stock_prices.sort_values('timestamp')
trade_orders = trade_orders.sort_values('timestamp')

# 使用 merge_asof 進行近似合併
# 這會找到每個訂單時間之前最近的股票價格
asof_merged = pd.merge_asof(
    trade_orders,
    stock_prices,
    on='timestamp',
    direction='backward'  # 使用之前最近的價格 (可改為 'forward' 或 'nearest')
)

print("\nmerge_asof 近似合併結果:")
print(asof_merged)

# 計算訂單值
asof_merged['order_value'] = asof_merged['quantity'] * asof_merged['stock_price']
print("\n計算訂單價值:")
print(asof_merged[['order_id', 'timestamp', 'quantity', 'stock_price', 'order_value']])

# %% [markdown]
# ### 6.3 分層數據的合併 (階層式數據)

# %%
# 演示處理分層數據的合併
print("階層式數據合併")

# 創建組織結構數據
org_hierarchy = pd.DataFrame({
    'employee_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'name': ['John', 'Emma', 'Michael', 'Sophia', 'William', 'Olivia', 'James', 'Ava', 'Benjamin', 'Mia'],
    'department': ['Sales', 'IT', 'Marketing', 'Sales', 'Finance', 'IT', 'Marketing', 'Finance', 'Sales', 'IT'],
    'manager_id': [None, 101, 101, 101, 102, 102, 103, 105, 104, 106]  # None 表示 CEO
})

# 創建業績數據
performance = pd.DataFrame({
    'employee_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'sales': [150000, 0, 120000, 180000, 0, 0, 90000, 0, 200000, 0],
    'rating': [4.5, 4.8, 4.0, 4.7, 4.2, 4.9, 3.8, 4.1, 4.6, 4.3]
})

print("組織結構:")
print(org_hierarchy)
print("\n業績數據:")
print(performance)

# 基本合併：員工與業績
employee_performance = pd.merge(
    org_hierarchy,
    performance,
    on='employee_id'
)

print("\n員工業績基本合併:")
print(employee_performance)

# 階層合併：查找每個員工的經理及其業績
# 首先，創建經理 DataFrame
managers = org_hierarchy.rename(columns={
    'employee_id': 'manager_id',
    'name': 'manager_name',
    'department': 'manager_department'
})

# 移除不必要的列
managers = managers.drop('manager_id', axis=1)

# 合併員工與其經理資訊
employees_with_managers = pd.merge(
    employee_performance,
    managers,
    on='manager_id',
    how='left'  # 保留所有員工，包括沒有經理的人
)

print("\n員工與經理階層合併:")
print(employees_with_managers[['employee_id', 'name', 'manager_id', 'manager_name', 'sales', 'rating']])

# 計算每個經理的團隊總業績
team_performance = employees_with_managers.groupby('manager_id').agg({
    'sales': 'sum',
    'rating': 'mean'
}).reset_index().rename(columns={'sales': 'team_sales', 'rating': 'team_avg_rating'})

# 合併經理與團隊業績
manager_performance = pd.merge(
    org_hierarchy,
    team_performance,
    left_on='employee_id',
    right_on='manager_id',
    how='left'
)

print("\n經理的團隊業績:")
print(manager_performance[['employee_id', 'name', 'team_sales', 'team_avg_rating']])

# %% [markdown]
# ## 📊 7. 業務智能實際案例

# %% [markdown]
# ### 7.1 銷售數據多維分析

# %%
# 使用之前創建的完整訂單視圖進行多維銷售分析
print("銷售數據多維分析")

# 確保我們有完整訂單視圖數據
if 'full_orders' in locals():
    # 計算每個類別的銷售總計
    category_sales = full_orders.groupby('category_name').agg({
        'item_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index()
    
    category_sales.columns = ['類別', '銷售總額', '訂單數', '客戶數']
    category_sales['平均訂單金額'] = category_sales['銷售總額'] / category_sales['訂單數']
    category_sales['客單價'] = category_sales['銷售總額'] / category_sales['客戶數']
    
    print("類別銷售分析:")
    print(category_sales)
    
    # 按銷售代表和地區的銷售分析
    region_sales_rep = full_orders.groupby(['region', 'sales_rep_name']).agg({
        'item_price': 'sum',
        'order_id': 'nunique',
        'customer_id': 'nunique'
    }).reset_index()
    
    region_sales_rep.columns = ['地區', '銷售代表', '銷售總額', '訂單數', '客戶數']
    region_sales_rep['平均訂單金額'] = region_sales_rep['銷售總額'] / region_sales_rep['訂單數']
    
    print("\n地區與銷售代表績效:")
    print(region_sales_rep.sort_values('銷售總額', ascending=False).head(10))
    
    # 按類別和客戶類型的交叉分析
    category_customer_type = full_orders.groupby(['category_name', 'customer_type']).agg({
        'item_price': 'sum'
    }).reset_index()
    
    # 數據透視表轉換
    category_customer_pivot = category_customer_type.pivot(
        index='category_name',
        columns='customer_type',
        values='item_price'
    ).fillna(0)
    
    # 添加總計列
    category_customer_pivot['總計'] = category_customer_pivot.sum(axis=1)
    
    # 計算百分比
    for col in category_customer_pivot.columns:
        if col != '總計':
            category_customer_pivot[f'{col} %'] = category_customer_pivot[col] / category_customer_pivot['總計'] * 100
    
    print("\n類別與客戶類型交叉分析:")
    print(category_customer_pivot)
    
    # 可視化類別銷售
    plt.figure(figsize=(12, 6))
    plt.bar(category_sales['類別'], category_sales['銷售總額'])
    plt.title('各類別銷售總額')
    plt.xlabel('產品類別')
    plt.ylabel('銷售總額')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()
else:
    print("尚未創建完整訂單視圖，請確保執行前面的代碼")

# %% [markdown]
# ### 7.2 供應鏈分析

# %%
# 供應鏈分析 - 產品供應商績效評估
print("供應鏈分析")

# 創建產品供應時間數據
np.random.seed(42)
order_dates = pd.date_range('2023-01-01', periods=300, freq='D')
product_ids = np.random.choice(products['product_id'].values, 300)
supplier_ids = [products[products['product_id'] == pid]['supplier_id'].values[0] for pid in product_ids]

supply_chain_data = pd.DataFrame({
    'order_date': order_dates,
    'product_id': product_ids,
    'supplier_id': supplier_ids,
    'order_quantity': np.random.randint(10, 100, 300),
    'lead_time_days': np.random.randint(1, 30, 300),  # 供應商供貨天數
    'defect_rate': np.random.uniform(0, 0.05, 300)   # 產品缺陷率
})

# 合併供應商資訊
supply_chain_with_supplier = pd.merge(
    supply_chain_data,
    suppliers,
    on='supplier_id'
)

# 合併產品資訊
supply_chain_full = pd.merge(
    supply_chain_with_supplier,
    products[['product_id', 'product_name', 'category_id']],
    on='product_id'
)

# 合併類別資訊
supply_chain_full = pd.merge(
    supply_chain_full,
    categories,
    on='category_id'
)

print("供應鏈數據:")
print(supply_chain_full.head())

# 供應商績效評估
supplier_performance = supply_chain_full.groupby('supplier_name').agg({
    'lead_time_days': ['mean', 'min', 'max', 'std'],
    'defect_rate': ['mean', 'max'],
    'order_quantity': 'sum',
    'product_id': 'nunique'
})

# 降級多級列索引
supplier_performance.columns = ['平均供貨天數', '最短供貨天數', '最長供貨天數', '供貨天數標準差', 
                              '平均缺陷率', '最高缺陷率', '訂購總量', '產品種類數']

# 創建綜合評分
supplier_performance['評分'] = (
    (1 / supplier_performance['平均供貨天數']) * 30 +  # 供貨天數越短越好
    (1 - supplier_performance['平均缺陷率']) * 50 +    # 缺陷率越低越好
    np.log10(supplier_performance['訂購總量']) * 10 +  # 訂購量大但影響較小
    np.log10(supplier_performance['產品種類數']) * 10  # 產品多樣性也考慮
)

# 排序
supplier_performance = supplier_performance.sort_values('評分', ascending=False)

print("\n供應商績效評估:")
print(supplier_performance)

# 可視化供應商評比
plt.figure(figsize=(12, 6))
supplier_performance['評分'].plot(kind='bar')
plt.title('供應商績效評分')
plt.xlabel('供應商')
plt.ylabel('評分')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 7.3 客戶生命週期價值分析

# %%
# 客戶生命週期價值分析 (CLV)
print("客戶生命週期價值分析")

# 假設我們已有完整的訂單資料
if 'full_orders' in locals():
    # 添加訂單年份列
    full_orders['order_year'] = full_orders['order_date'].dt.year
    
    # 計算每個客戶每年的消費
    customer_yearly_spending = full_orders.groupby(['customer_id', 'customer_name', 'order_year']).agg({
        'item_price': 'sum',
        'order_id': 'nunique'
    }).reset_index()
    
    customer_yearly_spending.columns = ['客戶ID', '客戶名稱', '年份', '年度消費', '訂單數量']
    
    # 計算平均訂單金額
    customer_yearly_spending['平均訂單金額'] = customer_yearly_spending['年度消費'] / customer_yearly_spending['訂單數量']
    
    # 計算客戶生命週期價值 (簡化版 - 平均年度消費 * 預期客戶年限)
    customer_avg_yearly = customer_yearly_spending.groupby(['客戶ID', '客戶名稱']).agg({
        '年度消費': 'mean',
        '訂單數量': 'mean',
        '平均訂單金額': 'mean'
    }).reset_index()
    
    # 假設平均客戶關係維持5年 (實際應使用更複雜的存活分析)
    expected_years = 5
    customer_avg_yearly['預估生命週期價值'] = customer_avg_yearly['年度消費'] * expected_years
    
    # 對客戶進行細分 (基於CLV)
    def clv_segment(clv):
        if clv >= 50000:
            return 'A - 高價值'
        elif clv >= 20000:
            return 'B - 中高價值'
        elif clv >= 5000:
            return 'C - 中價值'
        else:
            return 'D - 低價值'
    
    customer_avg_yearly['客戶細分'] = customer_avg_yearly['預估生命週期價值'].apply(clv_segment)
    
    # 按照CLV排序
    customer_avg_yearly = customer_avg_yearly.sort_values('預估生命週期價值', ascending=False)
    
    print("客戶生命週期價值 (CLV) 分析:")
    print(customer_avg_yearly.head(10))
    
    # 計算每個細分的客戶數量和總CLV
    segment_analysis = customer_avg_yearly.groupby('客戶細分').agg({
        '客戶ID': 'count',
        '預估生命週期價值': 'sum'
    }).reset_index()
    
    segment_analysis.columns = ['客戶細分', '客戶數量', '總CLV']
    segment_analysis['平均CLV'] = segment_analysis['總CLV'] / segment_analysis['客戶數量']
    segment_analysis['客戶佔比'] = segment_analysis['客戶數量'] / segment_analysis['客戶數量'].sum() * 100
    segment_analysis['收入佔比'] = segment_analysis['總CLV'] / segment_analysis['總CLV'].sum() * 100
    
    print("\n客戶細分分析:")
    print(segment_analysis)
    
    # 繪製客戶細分佔比圖
    plt.figure(figsize=(10, 6))
    plt.pie(segment_analysis['客戶數量'], labels=segment_analysis['客戶細分'], 
            autopct='%1.1f%%', startangle=90)
    plt.title('客戶分群佔比')
    plt.axis('equal')
    plt.show()
    
    # 繪製客戶收入佔比圖
    plt.figure(figsize=(10, 6))
    plt.pie(segment_analysis['總CLV'], labels=segment_analysis['客戶細分'], 
            autopct='%1.1f%%', startangle=90)
    plt.title('客戶收入佔比')
    plt.axis('equal')
    plt.show()
else:
    print("尚未創建完整訂單視圖，請確保執行前面的代碼")

# %% [markdown]
# ## 📊 8. 合併的最佳實踐與總結

# %%
# 整理合併操作的最佳實踐
merge_best_practices = pd.DataFrame({
    '領域': [
        '數據準備', '數據準備', '性能優化', '性能優化', '性能優化',
        '數據驗證', '數據驗證', '高階技巧', '高階技巧', '高階技巧'
    ],
    '最佳實踐': [
        '合併前檢查鍵的分布', '確保合併鍵沒有意外的缺失值', '對大型數據集先排序再合併', 
        '使用分塊策略處理超大數據集', '考慮將字符串類型的鍵轉換為類別(category)型別',
        '驗證合併後的行數是否符合預期', '檢查合併後聚合指標是否保持一致',
        '多表合併時使用逐步合併，檢查每步結果', '使用 merge_asof 處理時間相近但不完全匹配的情況',
        '利用 SQL 處理非常複雜的合併邏輯'
    ],
    '說明': [
        '分析每個合併鍵的唯一值數量和重複情況，避免意外的笛卡爾積',
        '缺失值在合併時的行為可能不如預期，特別是在外部合併時',
        '對排序好的數據進行合併可以顯著提高大型數據集的合併性能',
        '將大型數據集分割成小塊逐個合併，可以減少記憶體使用',
        '對於重複值多的字串鍵，轉換為category可以節省記憶體並加速合併',
        '檢查合併後的數據量是否符合預期，特別是有重複鍵的情況',
        '合併後，確保關鍵的總計、計數等聚合指標保持正確',
        '複雜的多表合併應分步驟執行，每步都檢查結果的正確性',
        '金融、物聯網等領域常需要將事件與最近的參考數據匹配',
        '對於特別複雜的合併邏輯，使用SQL可能更為直觀且高效'
    ]
})

print("合併操作最佳實踐:")
print(merge_best_practices)

# %% [markdown]
# **課程總結**：
# 
# 本課程深入探討了 Pandas 中的進階數據合併與連接技術，涵蓋的關鍵內容包括：
# 
# 1. **複雜數據關係處理**
#    - 多表關聯分析和數據量變化的理解
#    - 避免笛卡爾積問題的策略
# 
# 2. **合併驗證與診斷技術**
#    - 驗證合併操作的完整性
#    - 合併後數據一致性檢查
# 
# 3. **高性能合併技術**
#    - 大數據集合併優化方法
#    - 使用 SQL 處理超大數據集
# 
# 4. **進階特殊合併技術**
#    - 條件式合併
#    - 使用 pd.merge_asof 進行近似合併
#    - 分層數據的合併
# 
# 5. **業務智能實際案例**
#    - 銷售數據多維分析
#    - 供應鏈分析
#    - 客戶生命週期價值分析
# 
# 掌握這些進階技術，能夠幫助數據分析師和數據工程師處理複雜的數據整合任務，提高數據處理的效率和準確性，從而為業務決策提供更全面、更深入的數據支持。 