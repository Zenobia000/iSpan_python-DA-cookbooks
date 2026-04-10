"""M5 Matplotlib & Seaborn 視覺化 — 自動評分測試"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from homework.m5_visualization import (
    green_bar_category, green_hist_amount, green_set_labels,
    yellow_line_region_trend, yellow_box_vip, yellow_scatter_price_amount,
    red_category_dashboard,
)


def _assert_is_figure(result, name):
    assert result is not None, f"{name}: 函式回傳了 None"
    assert isinstance(result, plt.Figure), \
        f"{name}: 應回傳 matplotlib Figure，你回傳了 {type(result)}"


class TestGreen:
    def test_green_bar_category(self):
        result = green_bar_category()
        _assert_is_figure(result, "green_bar_category")
        axes = result.get_axes()
        assert len(axes) >= 1, "圖表應至少有一個 Axes"
        plt.close("all")

    def test_green_hist_amount(self):
        result = green_hist_amount()
        _assert_is_figure(result, "green_hist_amount")
        plt.close("all")

    def test_green_set_labels(self):
        result = green_set_labels()
        _assert_is_figure(result, "green_set_labels")
        ax = result.get_axes()[0]
        assert ax.get_title() != "", "請設定圖標題 (title)"
        assert ax.get_xlabel() != "", "請設定 X 軸標籤 (xlabel)"
        assert ax.get_ylabel() != "", "請設定 Y 軸標籤 (ylabel)"
        plt.close("all")


class TestYellow:
    def test_yellow_line_region_trend(self):
        result = yellow_line_region_trend()
        _assert_is_figure(result, "yellow_line_region_trend")
        ax = result.get_axes()[0]
        lines = ax.get_lines()
        assert len(lines) >= 2, "應有至少 2 條線（North 和 South）"
        plt.close("all")

    def test_yellow_box_vip(self):
        result = yellow_box_vip()
        _assert_is_figure(result, "yellow_box_vip")
        plt.close("all")

    def test_yellow_scatter_price_amount(self):
        result = yellow_scatter_price_amount()
        _assert_is_figure(result, "yellow_scatter_price_amount")
        plt.close("all")


class TestRed:
    def test_red_category_dashboard_is_figure(self):
        result = red_category_dashboard("Electronics")
        _assert_is_figure(result, "red_category_dashboard")
        plt.close("all")

    def test_red_category_dashboard_has_4_subplots(self):
        result = red_category_dashboard("Electronics")
        assert result is not None
        axes = result.get_axes()
        assert len(axes) == 4, f"應有 4 個 subplot，你有 {len(axes)} 個"
        plt.close("all")
