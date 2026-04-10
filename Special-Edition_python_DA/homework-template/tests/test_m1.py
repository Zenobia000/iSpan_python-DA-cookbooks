"""
M1 NumPy 自動評分測試
=====================
每個 test 對應 homework/m1_numpy.py 中的一個函式。
pytest 會收集 pass/fail，grader 據此計分。
"""
import numpy as np
import pytest

# ---------- 載入學生程式碼 ----------
from homework.m1_numpy import (
    green_mean,
    green_double,
    green_filter,
    yellow_expensive_count,
    yellow_top3_stock_indices,
    yellow_restock_cost,
    red_double11_prices,
)

# ---------- 載入 products.csv ----------
DATA_PATH = "datasets/ecommerce/products.csv"
prices = np.genfromtxt(DATA_PATH, delimiter=",", skip_header=1, usecols=3)
stocks = np.genfromtxt(DATA_PATH, delimiter=",", skip_header=1, usecols=4)


# ============================================================
# 🟢 送分題 (10 分 × 3)
# ============================================================

class TestGreen:
    def test_green_mean(self):
        result = green_mean()
        assert result is not None, "函式回傳了 None，請確認有 return"
        assert float(result) == pytest.approx(30.0), f"平均值應為 30.0，你的結果: {result}"

    def test_green_double(self):
        result = green_double()
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected = np.array([20, 40, 60, 80, 100])
        np.testing.assert_array_equal(result, expected)

    def test_green_filter(self):
        result = green_filter()
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected = np.array([30, 40, 50])
        np.testing.assert_array_equal(result, expected)


# ============================================================
# 🟡 核心題 (15 分 × 3)
# ============================================================

class TestYellow:
    def test_yellow_expensive_count(self):
        result = yellow_expensive_count(prices)
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected = int((prices > 1000).sum())
        assert int(result) == expected, f"預期 {expected}，你的結果: {result}"

    def test_yellow_top3_stock_indices(self):
        result = yellow_top3_stock_indices(stocks)
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected_indices = np.argsort(stocks)[-3:][::-1]
        # 只檢查集合相同（前 3 大的索引，順序可不同）
        assert set(result) == set(expected_indices), (
            f"前 3 大庫存索引應為 {expected_indices}，你的結果: {result}"
        )

    def test_yellow_restock_cost(self):
        result = yellow_restock_cost(prices, stocks)
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected = (prices[prices < 500] * 50).sum()
        assert float(result) == pytest.approx(expected), (
            f"進貨總花費應為 {expected}，你的結果: {result}"
        )


# ============================================================
# 🔴 挑戰題 (25 分)
# ============================================================

class TestRed:
    def test_red_double11_prices(self):
        result = red_double11_prices(prices, stocks)
        assert result is not None, "函式回傳了 None，請確認有 return"
        expected = np.where(
            stocks >= 100, prices * 0.7,
            np.where(stocks >= 20, prices * 0.9, prices),
        )
        np.testing.assert_allclose(result, expected, rtol=1e-7, err_msg="雙 11 售價計算有誤")

    def test_red_no_forloop(self):
        """檢查學生沒有使用 for-loop"""
        import inspect
        import ast

        source = inspect.getsource(red_double11_prices)
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                pytest.fail("請使用向量化寫法（np.where），不要用 for/while 迴圈！")
