"""
M2 Pandas I/O 與資料清理 — 課後作業
====================================
情境：你拿到一份「故意弄髒」的訂單 CSV (orders_raw.csv)，
裡面有欄位名稱空格、金額帶 $ 符號、日期格式錯誤、缺值、重複列。
請用 Pandas 把它清乾淨。

資料路徑：datasets/ecommerce/orders_raw.csv
"""
import pandas as pd


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_read_csv():
    """
    讀取 orders_raw.csv，回傳原始 DataFrame（不做任何清理）
    提示：pd.read_csv()
    """
    # TODO: 你的程式碼
    pass


def green_shape(df):
    """
    回傳 DataFrame 的 (列數, 欄數) tuple
    提示：df.shape
    """
    # TODO: 你的程式碼
    pass


def green_dtypes(df):
    """
    回傳 DataFrame 的欄位型別 (Series)
    提示：df.dtypes
    """
    # TODO: 你的程式碼
    pass


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_columns(df):
    """
    清理欄位名稱：去除前後空白、全部轉小寫
    回傳清理後的 DataFrame（不要修改原始 df）
    提示：df.columns.str.strip().str.lower()
    """
    # TODO: 你的程式碼
    pass


def yellow_clean_amount(df):
    """
    清理 amount 欄位：移除 '$' 和 ',' 符號，轉為 float
    假設欄位名稱已經是小寫的 'amount'
    回傳清理後的 DataFrame（不要修改原始 df）
    提示：.str.replace() + .astype(float)
    """
    # TODO: 你的程式碼
    pass


def yellow_drop_duplicates(df):
    """
    移除完全重複的列，回傳去重後的 DataFrame
    提示：df.drop_duplicates()
    """
    # TODO: 你的程式碼
    pass


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_clean_orders(path):
    """
    完整清理 pipeline：一個函式搞定所有清理步驟
    1. 讀取 CSV
    2. 欄位名稱：去空白、轉小寫
    3. amount：移除 '$' ','，轉 float
    4. order_date：轉為 datetime（無法轉換的設為 NaT）
    5. 刪除 amount 或 order_date 為空的列
    6. 移除重複列

    回傳：清理後的 DataFrame
    提示：pd.to_datetime(errors='coerce')
    """
    # TODO: 你的程式碼
    pass
