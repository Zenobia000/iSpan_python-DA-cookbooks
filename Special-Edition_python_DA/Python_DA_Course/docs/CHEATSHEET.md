# Python 資料分析 12H 課程 — 一頁式速查表

> **適用對象**：已完成 S1~S6 全部 6 個 Session 的學員，作為日常查找用的隨身手冊。
>
> **列印建議**：
> - 紙張 **A4 直式**，邊界設為 **窄 (Narrow)**；字級建議 **9~10pt**，可收納在 2~3 頁內。
> - 瀏覽器列印時請勾選「**背景圖形**」並取消頁首頁尾，可得到最乾淨版面。
> - 若使用 VS Code，建議以 `Markdown PDF` 擴充套件輸出，或直接印出瀏覽器預覽。
> - 建議搭配 `README.md` 的課程地圖使用，本表只列**指令**，概念請回看 Notebook。

---

## §1 NumPy 速查（S1：向量化運算）

| 想做什麼 | 怎麼寫 |
|---|---|
| 建立陣列 | `np.array([1, 2, 3])` |
| 看形狀 / 型別 | `arr.shape`, `arr.dtype` |
| 切片 | `arr[1:4]`, `arr[::2]` |
| 二維索引 | `arr[row, col]`, `arr[:, 0]` |
| 布林篩選 | `arr[arr > 10]` |
| 多條件遮罩 | `arr[(arr > 10) & (arr < 50)]` |
| 向量化運算 | `a + b`, `a * 2`（無需 for-loop） |
| 廣播 | `matrix + vector`（自動對齊維度） |
| 基礎統計 | `.sum() .mean() .max() .min() .std()` |
| 條件賦值 | `np.where(cond, a, b)` |
| 排序索引 | `np.argsort(arr)` |

**S1 心法**：看到 `for i in range(len(arr)): result[i] = ...`，**99%** 可以改成一行向量化寫法。

---

## §2 Pandas I/O 與清理（S2：ETL 第一哩路）

| 想做什麼 | 怎麼寫 |
|---|---|
| 讀 CSV | `pd.read_csv(path)` |
| 讀 Excel | `pd.read_excel(path, sheet_name=...)` |
| 快速瞄一眼 | `df.head() / df.info() / df.describe()` |
| 看缺值數量 | `df.isna().sum()` |
| 欄名去空白 | `df.columns = df.columns.str.strip()` |
| 字串 → 數字 | `df['x'].str.replace('$', '').astype(float)` |
| 字串 → 日期 | `pd.to_datetime(df['x'], errors='coerce')` |
| 丟缺值 | `df.dropna(subset=['col'])` |
| 補缺值 | `df['x'].fillna(值)` |
| 去重 | `df.drop_duplicates()` |
| 存檔 | `df.to_csv(path, index=False)` |

**S2 ETL 心法**：拿到任何新資料 → `head / info / isna` 快速掃一遍 → 逐欄處理 → 驗收 → 存乾淨檔給下游。

---

## §3 Pandas 轉換與多表整合（S3：DA/DE 核心）

| 想做什麼 | 怎麼寫 | SQL 對照 |
|---|---|---|
| 區間篩選 | `df[df['x'].between(a, b)]` | `WHERE x BETWEEN a AND b` |
| 清單篩選 | `df[df['x'].isin([...])]` | `WHERE x IN (...)` |
| 分組加總 | `df.groupby('k')['v'].sum()` | `GROUP BY k` |
| 多重聚合 | `df.groupby('k').agg(s=('v','sum'), n=('v','count'))` | 多 `SUM/COUNT/AVG` |
| Join 兩表 | `a.merge(b, on='k', how='left')` | `LEFT JOIN` |
| Join 四種 how | `how='left' / 'right' / 'inner' / 'outer'` | 對應 SQL 四種 JOIN |
| 樞紐分析 | `df.pivot_table(index, columns, values, aggfunc)` | Excel 樞紐 |
| 每組 Top N | `df.sort_values('v', ascending=False).groupby('k').head(n)` | `ROW_NUMBER() OVER(...)` |

**S3 心法**：`groupby` 是 DA 的瑞士刀；搞懂 `merge` 的 `how` 四種差異，就能回答 90% 的商業問題。

---

## §4 時序與 EDA（S4：看趨勢、找洞察）

| 想做什麼 | 怎麼寫 |
|---|---|
| 字串 → 日期 | `pd.to_datetime(col, errors='coerce')` |
| 取年 / 月 / 星期 | `.dt.year` / `.dt.month` / `.dt.day_name()` |
| 轉年月字串 | `.dt.to_period('M')` |
| 每日聚合 | `df.resample('D', on='date')['v'].sum()` |
| 每週 / 每月 / 每季 | `.resample('W') / .resample('ME') / .resample('QE')` |
| 移動平均 | `.rolling(window=7).mean()` |
| 期間成長率 | `.pct_change()` |
| 數值摘要 | `df.describe()` |
| 類別分布 | `df['x'].value_counts()` |
| 相關係數矩陣 | `df[num_cols].corr()` |
| Unique 計數 | `df['x'].nunique()` |

**S4 心法**：所有分析先 **head / info / describe 三連**；再用 `resample + rolling` 找出趨勢與波動。

---

## §5 視覺化 — Matplotlib / Seaborn（S5：靜態交付）

| 想畫什麼 | 標準函式 |
|---|---|
| 趨勢線 | `sns.lineplot(data=df, x='date', y='sales')` |
| 類別比較 | `sns.barplot(data=df, x='region', y='sales')` |
| 雙變數關聯 | `sns.scatterplot(data=df, x='x', y='y', hue='cat')` |
| 數值分布 | `sns.histplot(df['x'], bins=30, kde=True)` |
| 離群檢測 | `sns.boxplot(data=df, x='cat', y='v')` |
| 相關矩陣熱圖 | `sns.heatmap(df.corr(), annot=True, cmap='coolwarm')` |
| 多圖組合 | `fig, axes = plt.subplots(nrows, ncols)` + `ax=axes[i, j]` |
| 全域設定中文 | `plt.rcParams['font.sans-serif'] = ['PingFang TC']` |
| 存圖 | `plt.savefig('out.png', dpi=150, bbox_inches='tight')` |

**S5 心法**：先用 **seaborn 一行** 搞定骨架，不夠漂亮再用 matplotlib 的 `ax.set_*` 微調。

---

## §6 Plotly 互動視覺化（S6：成品交付）

| 想畫什麼 | Plotly Express |
|---|---|
| 折線 | `px.line(df, x, y, markers=True)` |
| 長條 | `px.bar(df, x, y, color, text)` |
| 散佈 | `px.scatter(df, x, y, color, hover_data=[...])` |
| 箱型 | `px.box(df, x, y, color)` |
| 直方 | `px.histogram(df, x, nbins=30)` |
| 圓餅（甜甜圈） | `px.pie(df, names, values, hole=0.4)` |
| 多圖組合 | `make_subplots(rows, cols)` + `fig.add_trace(...)` |
| 版面調整 | `fig.update_layout(title=..., template='plotly_white')` |
| 匯出互動 HTML | `fig.write_html('dashboard.html')` |

**S6 心法**：Plotly Express 一行出圖 → 需要客製時才降級到 `graph_objects` + `make_subplots`。

---

## §7 DA / DE 心法總則

| 原則 | 說明 |
|---|---|
| 資料清理是主戰場 | **60~80%** 的時間花在清理，而非分析；`S2` 的技巧是日常 80% 的工作。 |
| 向量化優先 | 看到 `for` 迴圈在處理數字，**99%** 可以改寫成 NumPy / Pandas 一行。 |
| 三連掃描 | 拿到新資料先做 **`head / info / describe`**，看結構、看型別、看分布。 |
| 數字不會說話 | 算出的洞察若無法畫成圖，老闆不會記得；`S5 / S6` 決定交付品質。 |
| 回答「所以呢？」 | DA/DE 的價值不在技術，在於能回答老闆「**So what？**」這個問題。 |

---

### 附：Session 能力對照

| Session | 能力 | 對應職能 |
|---|---|---|
| S1 | NumPy 向量化運算 | 基礎 Python 資料處理 |
| S2 | 讀檔 + 資料清理 | **DE** 的第一哩路 |
| S3 | 多表 Join + 聚合 | **DE / DA** 核心能力 |
| S4 | 時序分析 + EDA | **DA** 核心能力 |
| S5 | 靜態視覺化（Matplotlib / Seaborn） | 報告交付 |
| S6 | 互動儀表板（Plotly） | 成品交付 |

**下一步自學建議**：**SQL**（`groupby / merge` 思維 100% 通用） → **scikit-learn**（分析延伸至 ML） → **Streamlit / Dash**（Notebook 變 Web App）。
