"""M6 Plotly 互動儀表板 — 自動評分測試"""
import pandas as pd
import plotly.graph_objects as go
import pytest

from homework.m6_plotly_capstone import (
    green_plotly_bar, green_plotly_line, green_plotly_pie,
    yellow_clean_and_merge, yellow_kpi_summary, yellow_plotly_scatter,
    red_dashboard,
)


def _assert_is_plotly_figure(result, name):
    assert result is not None, f"{name}: 函式回傳了 None"
    assert isinstance(result, go.Figure), \
        f"{name}: 應回傳 plotly Figure，你回傳了 {type(result)}"


class TestGreen:
    def test_green_plotly_bar(self):
        result = green_plotly_bar()
        _assert_is_plotly_figure(result, "green_plotly_bar")
        assert len(result.data) > 0, "圖表應有資料"

    def test_green_plotly_line(self):
        result = green_plotly_line()
        _assert_is_plotly_figure(result, "green_plotly_line")
        assert len(result.data) > 0

    def test_green_plotly_pie(self):
        result = green_plotly_pie()
        _assert_is_plotly_figure(result, "green_plotly_pie")
        assert len(result.data) > 0


class TestYellow:
    def test_yellow_clean_and_merge(self):
        result = yellow_clean_and_merge(
            "datasets/ecommerce/orders_raw.csv",
            "datasets/ecommerce/customers.csv",
            "datasets/ecommerce/products.csv",
        )
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, pd.DataFrame)
        assert "customer_name" in result.columns
        assert "product_name" in result.columns
        assert pd.api.types.is_numeric_dtype(result["amount"])

    def test_yellow_kpi_summary(self):
        df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
        result = yellow_kpi_summary(df)
        assert result is not None, "函式回傳了 None"
        assert isinstance(result, dict)
        required = {"total_revenue", "order_count", "active_customers", "avg_order_value"}
        assert required.issubset(set(result.keys())), \
            f"缺少 key: {required - set(result.keys())}"
        assert result["order_count"] == len(df)
        assert result["total_revenue"] == pytest.approx(df["amount"].sum(), rel=0.01)

    def test_yellow_plotly_scatter(self):
        df = pd.read_csv("datasets/ecommerce/orders_enriched.csv")
        result = yellow_plotly_scatter(df)
        _assert_is_plotly_figure(result, "yellow_plotly_scatter")


class TestRed:
    def test_red_dashboard_is_figure(self):
        result = red_dashboard()
        _assert_is_plotly_figure(result, "red_dashboard")

    def test_red_dashboard_has_traces(self):
        result = red_dashboard()
        assert result is not None
        assert len(result.data) >= 4, \
            f"儀表板應至少有 4 個 trace（4 個子圖），你有 {len(result.data)} 個"
