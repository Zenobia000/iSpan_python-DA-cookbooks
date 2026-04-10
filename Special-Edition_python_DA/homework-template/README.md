# Python 資料分析 — 自動批改作業系統

> **第一次用？** 請先讀 [Git/CI/CD/PR 教學手冊 →](docs/STUDENT_GUIDE.md)

## 繳交流程（4 步驟）

### Step 1：Fork 這個 Repo

點擊右上角 **「Fork」** 按鈕，建立你自己的副本。

### Step 2：寫作業

Clone 你 fork 的 repo 到本機，編輯 `homework/` 資料夾中的 `.py` 檔：

```bash
git clone https://github.com/你的帳號/repo名稱.git
cd repo名稱
```

### Step 3：Push 到你的 Fork

```bash
git add homework/
git commit -m "完成 M1 作業"
git push
```

### Step 4：發 PR 繳交

1. 到你 fork 的 repo 頁面
2. 點 **「Contribute」** → **「Open pull request」**
3. PR 標題寫：`M1 作業 — 你的姓名`
4. 點 **「Create pull request」**

> 每次 push 新的 commit，都會自動重新批改。可以無限次修改重交。

### 查看成績

批改結果會出現在**兩個地方**：

| 位置 | 內容 | 怎麼看 |
|:-----|:-----|:-------|
| **PR 留言區** | 分數 + 對錯表 | 回到你發的 PR 頁面往下滑 |
| **你 fork 的 Actions** | 分數 + **完整解答** | 你的 repo → Actions → 最新一次 run → 點進去看 Summary |

> 解答只會出現在你自己 fork 的 Actions 裡，其他同學看不到。

---

## 作業列表

| 作業檔案 | 對應課程 | 滿分 |
|:---------|:---------|:----:|
| `homework/m1_numpy.py` | M1 NumPy 向量化思維 | 100 |
| `homework/m2_pandas_cleaning.py` | M2 Pandas I/O 與資料清理 | 100 |
| `homework/m3_pandas_advanced.py` | M3 Pandas 進階：merge / groupby / RFM | 100 |
| `homework/m4_timeseries.py` | M4 時間序列與 EDA | 100 |
| `homework/m5_visualization.py` | M5 Matplotlib & Seaborn 視覺化 | 100 |
| `homework/m6_plotly_capstone.py` | M6 Plotly 互動儀表板 & Capstone | 100 |
| | **總計** | **600** |

每份作業都是 🟢 送分題 30 分 + 🟡 核心題 45 分 + 🔴 挑戰題 25 分

---

## 本地測試（選用）

```bash
pip install -r requirements.txt

# 測試單一模組
python -m pytest tests/test_m1.py -v

# 測試全部
python -m pytest tests/ -v
```

## 專案結構

```
├── homework/               ← 你要編輯的作業檔案
│   ├── m1_numpy.py
│   ├── m2_pandas_cleaning.py
│   ├── m3_pandas_advanced.py
│   ├── m4_timeseries.py
│   ├── m5_visualization.py
│   └── m6_plotly_capstone.py
├── tests/                  ← 自動測試（不要改）
├── solutions/              ← 解答（只在你的 fork Actions 顯示）
├── grader/                 ← 評分引擎（不要改）
├── datasets/ecommerce/     ← 資料檔（不要改）
├── docs/
│   └── STUDENT_GUIDE.md    ← Git/CI/CD/PR 教學手冊
└── .github/workflows/      ← CI/CD 設定（不要改）
```

---

## 老師專區

### 查看全班繳交狀況

到 repo 的 **Pull requests** 頁籤，可以看到所有學生的 PR。
- 有 `graded` label = 已批改
- `score:A` ~ `score:F` label = 成績等級

### 匯出成績總表

1. 到 **Actions** 頁籤
2. 點左側 **「📋 彙整全班成績」**
3. 點右側 **「Run workflow」**
4. 完成後在 Job Summary 看表格，或下載 `grades.csv`
