# Python DA 12 小時精煉課程

> 以資料工程 (DE) + 資料分析 (DA) 實務視角設計，**6 個 Session × 2 小時 = 12 小時**，全程用一個**電商銷售貫穿式案例**串起。

## 📚 課程地圖

| Session | 主題 | 檔案位置 | 核心工具 |
|---|---|---|---|
| **S1** | NumPy 與向量化思維 | `M1_Numpy_Basic/S1_numpy_vectorization.ipynb` | NumPy |
| **S2** | Pandas I/O 與資料清理（ETL 第一哩路） | `M2_Pandas_Basic/S2_pandas_io_cleaning.ipynb` | Pandas |
| **S3** | Pandas 轉換：groupby / merge / pivot | `M3_Pandas_Advanced/S3_pandas_transform.ipynb` | Pandas |
| **S4** | 時間序列 + EDA 實戰 | `M3_Pandas_Advanced/S4_timeseries_eda.ipynb` | Pandas |
| **S5** | 視覺化精華：5 種必懂圖 | `M4_Matplotlib_Seaborn_Basic/S5_visualization_essentials.ipynb` | Matplotlib + Seaborn |
| **S6** | Plotly 互動 + Capstone | `M6_Plotly_Projects/S6_plotly_capstone.ipynb` | Plotly |

每個 Session 的 notebook 統一結構為：  
**課前暖身 → 核心觀念（≤3 個） → 實務 Case → 課堂練習（3 題階梯式） → 小結速查表**

## 🎯 學員前備

- 已會基本 Python：變數、list、dict、for、函式
- 不需要任何 NumPy / Pandas 經驗

## 🗂️ 貫穿式資料集

所有 Session 共用 `datasets/ecommerce/`：

| 檔案 | 說明 | 首次使用 |
|---|---|---|
| `products.csv` | 30 個商品主檔（乾淨） | S1 |
| `orders_raw.csv` | 210 筆訂單（故意髒） | S2 |
| `customers.csv` | 26 位顧客主檔 | S3 |
| `_generate.py` | 資料生成器（可重現） | - |

資料會在 S2 清理後存為 `orders_clean.csv`，S3 合併後存為 `orders_enriched.csv`，供後續 session 延用。

## 📦 安裝

```bash
pip install numpy pandas matplotlib seaborn plotly jupyter
```

## 🚀 開始上課

從 `M1_Numpy_Basic/S1_numpy_vectorization.ipynb` 開始，依序走到 `M6_Plotly_Projects/S6_plotly_capstone.ipynb` 即可。
