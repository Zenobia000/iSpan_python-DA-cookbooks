"""M3 Pandas 進階 — 自動評分測試"""
import pandas as pd
import pytest

from homework.m3_pandas_advanced import (
    green_load_and_merge, green_row_count, green_column_list,
    yellow_top_category, yellow_gold_vip_stats, yellow_region_avg_amount,
    red_rfm_top5,
)

# 預先載入合併資料作為參考答案
orders = pd.read_csv("datasets/ecommerce/orders_clean.csv")
customers = pd.read_csv("datasets/ecommerce/customers.csv")
products = pd.read_csv("datasets/ecommerce/products.csv")
ref_df = orders.merge(customers, on="customer_id", how="left") \
               .merge(products, on="product_id", how="left")


class TestGreen:
    def test_green_load_and_merge(self):
        result = green_load_and_merge()
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert isinstance(result, pd.DataFrame)
        assert "customer_name" in result.columns, "缺少 customer_name，是否忘了 merge customers?"
        assert "product_name" in result.columns, "缺少 product_name，是否忘了 merge products?"

    def test_green_row_count(self):
        result = green_row_count(ref_df)
        assert result is not None, "函式回傳了 None"
        assert int(result) == len(ref_df)

    def test_green_column_list(self):
        result = green_column_list(ref_df)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, list)
        assert len(result) == len(ref_df.columns)


class TestYellow:
    def test_yellow_top_category(self):
        result = yellow_top_category(ref_df)
        assert result is not None, "函式回傳了 None"
        expected = ref_df.groupby("category")["amount"].sum().idxmax()
        assert result == expected, f"預期 '{expected}'，你的結果: '{result}'"

    def test_yellow_gold_vip_stats(self):
        result = yellow_gold_vip_stats(ref_df)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, tuple) and len(result) == 2, \
            "應回傳 (訂單數, 總金額) 的 tuple"
        gold = ref_df[ref_df["vip_level"] == "Gold"]
        expected_count = len(gold)
        expected_amount = gold["amount"].sum()
        assert int(result[0]) == expected_count
        assert float(result[1]) == pytest.approx(expected_amount, rel=1e-2)

    def test_yellow_region_avg_amount(self):
        result = yellow_region_avg_amount(ref_df)
        assert result is not None, "函式回傳了 None"
        expected = ref_df.groupby("region")["amount"].mean()
        pd.testing.assert_series_equal(
            result.sort_index().astype(float),
            expected.sort_index().astype(float),
            check_names=False, atol=1,
        )


class TestRed:
    def test_red_rfm_top5_shape(self):
        result = red_rfm_top5(ref_df)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5, f"應回傳 5 筆，你有 {len(result)} 筆"

    def test_red_rfm_top5_columns(self):
        result = red_rfm_top5(ref_df)
        assert result is not None
        required = {"customer_id", "customer_name", "F", "M"}
        assert required.issubset(set(result.columns)), \
            f"缺少必要欄位，你的欄位: {list(result.columns)}"

    def test_red_rfm_top5_sorted_by_m(self):
        result = red_rfm_top5(ref_df)
        assert result is not None
        m_values = result["M"].values
        assert all(m_values[i] >= m_values[i + 1] for i in range(len(m_values) - 1)), \
            "應按 M（消費總金額）由大到小排序"
