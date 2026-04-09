# Kaggle 實戰分析技巧 — 融會貫通篇

> **定位**：進階選修課程，銜接 Special-Edition 12 小時基礎課程
> **時數**：5 堂 × 2 小時 + 1 堂環境設定 (20 min)
> **先修**：M1 NumPy / M2 Pandas I/O / M3 Pandas 進階 / M4 Matplotlib-Seaborn / M6 Plotly

---

## 課程地圖

| Session | 主題 | 核心技巧 | 資料集 |
|:--------|:-----|:---------|:-------|
| S0 | Kaggle API 環境設定 | kaggle CLI / pathlib / zipfile | — |
| S1 | 第一眼檢查清單 First Look | shape-info-describe / target 分析 / 欄位分類 | Titanic |
| S2 | 缺失值策略 Missing Data | NA 全景圖 / MCAR-MAR-MNAR / 填補工具箱 | Titanic |
| S3 | 分布偵探 Distribution & Outlier | histogram-KDE-boxplot / 交叉比較 / 離群值 | Titanic + House Prices |
| S4 | 特徵工程思維 Feature Thinking | 組合特徵 / 文字拆解 / 分箱與交互 | Titanic |
| S5 | EDA 大統整 Capstone | 相關性分析 / EDA Checklist / 分析報告 | Spaceship Titanic |

## 學習路徑

```
M1-M6 基礎課程
  │
  ▼
S0: 環境設定 → 下載 3 個 Kaggle 資料集
  │
  ▼
S1: First Look → 拿到資料的前 10 分鐘該做什麼
  │
  ▼
S2: Missing Data → 缺失值不是刪掉就好
  │
  ▼
S3: Distribution → 每個欄位都有自己的故事
  │
  ▼
S4: Feature Engineering → 從觀察到創造
  │
  ▼
S5: EDA Capstone → 從零到報告的完整流程
```

## 使用的 Kaggle 資料集

| 資料集 | 用途 | 下載指令 |
|:-------|:-----|:---------|
| [Titanic](https://www.kaggle.com/c/titanic) | S1-S4 教學主軸 | `kaggle competitions download -c titanic` |
| [House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) | S1-S3 練習 | `kaggle competitions download -c house-prices-advanced-regression-techniques` |
| [Spaceship Titanic](https://www.kaggle.com/c/spaceship-titanic) | S4 練習 + S5 Capstone | `kaggle competitions download -c spaceship-titanic` |

## 環境需求

```bash
pip install pandas numpy matplotlib seaborn kaggle
```

## 目錄結構

```
kaggle-win-tricks/
├── README.md
├── datasets/           # Kaggle 資料集（不進版控）
├── S0_kaggle_setup.ipynb / _solution.ipynb
├── S1_first_look.ipynb / _solution.ipynb
├── S2_missing_strategy.ipynb / _solution.ipynb
├── S3_distribution_detective.ipynb / _solution.ipynb
├── S4_feature_thinking.ipynb / _solution.ipynb
├── S5_eda_capstone.ipynb / _solution.ipynb
└── reference/          # 舊檔案歸檔（Ensembling model 等）
```
