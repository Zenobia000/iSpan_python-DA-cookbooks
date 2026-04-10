"""M2 Pandas 資料清理 — 自動評分測試"""
import pandas as pd
import pytest

from homework.m2_pandas_cleaning import (
    green_read_csv, green_shape, green_dtypes,
    yellow_clean_columns, yellow_clean_amount, yellow_drop_duplicates,
    red_clean_orders,
)

RAW_PATH = "datasets/ecommerce/orders_raw.csv"
raw_df = pd.read_csv(RAW_PATH)


class TestGreen:
    def test_green_read_csv(self):
        result = green_read_csv()
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_green_shape(self):
        result = green_shape(raw_df)
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert result == raw_df.shape, f"預期 {raw_df.shape}，你的結果: {result}"

    def test_green_dtypes(self):
        result = green_dtypes(raw_df)
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert isinstance(result, pd.Series)


class TestYellow:
    def test_yellow_clean_columns(self):
        result = yellow_clean_columns(raw_df)
        assert result is not None, "函式回傳了 None，請確認有 return"
        for col in result.columns:
            assert col == col.strip().lower(), f"欄位 '{col}' 還有空白或大寫"

    def test_yellow_clean_amount(self):
        # 先清欄位名稱再測 amount
        df = raw_df.copy()
        df.columns = df.columns.str.strip().str.lower()
        result = yellow_clean_amount(df)
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert result["amount"].dtype in ["float64", "float32"], \
            f"amount 應為 float，你的是 {result['amount'].dtype}"

    def test_yellow_drop_duplicates(self):
        result = yellow_drop_duplicates(raw_df)
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert len(result) < len(raw_df), "去重後列數應該減少"
        assert len(result) == len(raw_df.drop_duplicates())


class TestRed:
    def test_red_clean_orders_returns_df(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert isinstance(result, pd.DataFrame)

    def test_red_clean_orders_columns(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None
        for col in result.columns:
            assert col == col.strip().lower(), f"欄位 '{col}' 未清理"

    def test_red_clean_orders_amount_is_numeric(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None
        assert pd.api.types.is_numeric_dtype(result["amount"]), \
            "amount 欄位應為數值型別"

    def test_red_clean_orders_date_is_datetime(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"]), \
            "order_date 應為 datetime 型別"

    def test_red_clean_orders_no_nulls(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None
        assert result[["amount", "order_date"]].isna().sum().sum() == 0, \
            "amount 和 order_date 不應有缺值"

    def test_red_clean_orders_no_duplicates(self):
        result = red_clean_orders(RAW_PATH)
        assert result is not None
        assert len(result) == len(result.drop_duplicates()), \
            "不應有重複列"
