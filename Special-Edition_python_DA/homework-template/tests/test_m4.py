"""M4 時間序列與 EDA — 自動評分測試"""
import pandas as pd
import pytest

from homework.m4_timeseries import (
    green_avg_by_month, green_top3_dates, green_date_range,
    yellow_monthly_revenue, yellow_rolling_avg, yellow_category_median,
    red_monthly_report,
)

df = pd.read_csv("datasets/ecommerce/orders_enriched.csv",
                 parse_dates=["order_date"])


class TestGreen:
    def test_green_avg_by_month(self):
        result = green_avg_by_month()
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        expected = df.groupby(df["order_date"].dt.month)["amount"].mean()
        pd.testing.assert_series_equal(
            result.sort_index().astype(float),
            expected.sort_index().astype(float),
            check_names=False, atol=1,
        )

    def test_green_top3_dates(self):
        result = green_top3_dates()
        assert result is not None, "函式回傳了 None"
        assert len(result) == 3
        expected_top = df["order_date"].dt.date.value_counts().head(3)
        assert result.iloc[0] == expected_top.iloc[0], "第一名的訂單數不符"

    def test_green_date_range(self):
        result = green_date_range()
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, tuple) and len(result) == 2
        assert pd.Timestamp(result[0]) == df["order_date"].min()
        assert pd.Timestamp(result[1]) == df["order_date"].max()


class TestYellow:
    def test_yellow_monthly_revenue(self):
        result = yellow_monthly_revenue()
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        total = result.sum()
        expected_total = df["amount"].sum()
        assert total == pytest.approx(expected_total, rel=0.01), \
            "每月營收加總應等於總營收"

    def test_yellow_rolling_avg(self):
        monthly = df.set_index("order_date").resample("ME")["amount"].sum()
        result = yellow_rolling_avg(monthly)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.Series)
        assert len(result) == len(monthly)
        expected = monthly.rolling(window=3).mean()
        pd.testing.assert_series_equal(
            result.astype(float), expected.astype(float),
            check_names=False, atol=1,
        )

    def test_yellow_category_median(self):
        result = yellow_category_median(df)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.Series)
        # 檢查是由大到小排序
        values = result.values
        assert all(values[i] >= values[i + 1] for i in range(len(values) - 1)), \
            "應由大到小排序"


class TestRed:
    def test_red_monthly_report_columns(self):
        result = red_monthly_report()
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.DataFrame)
        required = {"order_count", "revenue", "active_customers",
                     "avg_order_value", "revenue_growth"}
        actual = set(result.columns)
        missing = required - actual
        assert not missing, f"缺少欄位: {missing}"

    def test_red_monthly_report_values(self):
        result = red_monthly_report()
        assert result is not None
        assert result["order_count"].sum() == len(df), \
            "所有月份的 order_count 加總應等於總訂單數"
        assert result["revenue"].sum() == pytest.approx(df["amount"].sum(), rel=0.01)

    def test_red_monthly_report_growth(self):
        result = red_monthly_report()
        assert result is not None
        assert pd.isna(result["revenue_growth"].iloc[0]), \
            "第一個月的 revenue_growth 應為 NaN（沒有上月可比）"
