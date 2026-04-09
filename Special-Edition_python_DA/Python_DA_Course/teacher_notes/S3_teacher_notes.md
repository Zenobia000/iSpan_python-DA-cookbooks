# S3 — Pandas 轉換：groupby / merge / pivot｜講師講稿

> **課程時長**：2 小時（講授 70 min + 課堂練習 40 min + QA 10 min）
> **對應 Notebook**：`M3_Pandas_Advanced/S3_pandas_transform.ipynb`

---

## 1. 本節目標 (Learning Objectives)

完成本節後，學員應能：

1. 運用 `between`、`isin`、`&` / `|` 組合條件篩選 DataFrame。
2. 使用 `groupby().agg()` 做單欄／多欄、單函式／多函式聚合，並說明它對應 SQL 的哪些子句。
3. 使用 `merge()` 的 `on` 與 `how` 參數完成兩表、三表 join，並判斷應該使用 `left` / `inner` / `outer`。
4. 使用 `pivot_table()` 建立「列 × 欄」的交叉分析矩陣，並說明與 `groupby` 的差異與等價性。
5. 在電商三表資料（orders + customers + products）上，回答「各地區營收」「地區 Top3 商品」「VIP 貢獻佔比」等多維分析問題。

---

## 2. 時間切分表

```
00:00-00:05  開場暖身：上節 S2 回顧，確認大家都有 orders_clean.csv
00:05-00:15  核心觀念 1/3：條件篩選補強（between / isin / 多條件括號）
00:15-00:40  核心觀念 2/3：groupby 三層（單欄聚合 → agg 多函式 → 多欄多函式）
00:40-01:00  核心觀念 3/3：merge 兩表 / 三表 join + how 四種選擇的差別
01:00-01:10  實務 Case：電商銷售洞察 Q1~Q3 + pivot_table bonus
01:10-01:50  課堂練習（40 min）：🟡 品類營收 Top N + 🔴 RFM 粗估挑戰題
01:50-02:00  QA + 下節預告（S4 時間序列 EDA）
```

---

## 3. 關鍵教學點 (Key Teaching Points)

1. **groupby 的心智模型 = Split → Apply → Combine**：先按 key 分組、再對每組套用函式、最後把結果拼回去。這個三步驟講清楚，所有 groupby 題都能秒解。
2. **`agg` 的三種寫法要全部示範**：
   - 單函式：`.agg('sum')` 或 `.sum()`
   - 多函式：`.agg(['count', 'sum', 'mean'])`
   - 具名聚合：`.agg(total=('amount','sum'), cnt=('amount','count'))`（最推薦，結果欄名乾淨）
3. **`merge` 的 `how` 四選一要畫 Venn 圖**：`inner`（交集）、`left`（保留左表全部）、`right`、`outer`（聯集）。90% 情境用 `left`，因為你通常是「從主表的角度去補資訊」。
4. **`on` 欄名不一致時**：用 `left_on='uid', right_on='customer_id'`。要提醒學員 merge 後常見 bug 是「筆數暴增」——這通常代表 right 表的 key 不唯一（1:N 或 N:N）。
5. **`groupby` vs `pivot_table` 何時用哪個**：兩者可互換，但想要「行=A, 列=B, 值=metric」的交叉報表時用 `pivot_table` 最直觀；想要程式化後續處理時用 `groupby`。

---

## 4. 學員常犯錯誤 (Common Pitfalls)

- **`merge` 的 `on` 寫錯**：兩表欄名不同卻都寫 `on='id'` → `KeyError`。要改成 `left_on` / `right_on`。
- **merge 後筆數爆炸**：沒先檢查 right 表 key 是否唯一，1:N 變 N:M。merge 前先跑 `df_right['key'].duplicated().sum()`。
- **`groupby` 後忘記 reset_index**：結果變成 MultiIndex，後續 `merge` 或畫圖會卡住。視情況補 `.reset_index()`。
- **`SettingWithCopyWarning`**：`df[df.a>0]['b'] = 1` 這種鏈式賦值會噴警告且不一定生效，要改用 `df.loc[df.a>0, 'b'] = 1`。
- **`pivot_table` 預設 `aggfunc='mean'`**：想算總和時忘了指定 `aggfunc='sum'` 會得到錯誤結果。
- **多條件篩選少了括號**：`df[df.a>0 & df.b<10]`——`&` 優先級高於 `>`，會先算 `0 & df.b` 報錯；正確是 `df[(df.a>0) & (df.b<10)]`。

---

## 5. 提問設計 (Discussion Prompts)

1. 同樣算「每個地區總營收」，可以用 `groupby('region').sum()`、`pivot_table(index='region', values='amount', aggfunc='sum')`，甚至 SQL。三者背後的運算是一樣的嗎？你會怎麼選？
2. 為什麼大多數情境 `merge` 都用 `how='left'` 而不是 `inner`？`inner` 會造成什麼隱性資料損失？
3. 如果 orders 有 100 萬筆、customers 有 1 萬筆，merge 之後應該是幾筆？如果變成 150 萬筆，代表發生了什麼事？

---

## 6. 延伸資源 (Further Reading)

- Pandas 官方 User Guide「Group by: split-apply-combine」與「Merge, join, concatenate and compare」章節（可在 pandas.pydata.org 搜尋）。
- 查詢 Pandas 官方 Comparison with SQL 頁面，對照 SQL 與 Pandas 寫法。

---

## 7. 常見 Q&A

**Q1：`merge` 和 `join` 有什麼差別？**
A：`df.join()` 是 `merge` 的簡化版，預設用 index 對齊、預設 `how='left'`。彈性上 `merge` 完勝，實務上 90% 用 `merge` 就好。

**Q2：`groupby` 很慢怎麼辦？**
A：先確認是不是真的慢（1000 萬筆以下通常沒事）。若資料大，可試：(1) 先 `astype('category')` 分組欄、(2) 改用 `polars` 或 `duckdb`、(3) 避免 `apply(lambda)`，改用內建 `agg`。

**Q3：可以用 SQL 做完這些為什麼要學 Pandas？**
A：Pandas 的優勢是「與 Python 生態整合」——清完資料直接丟 scikit-learn 訓練、丟 matplotlib 畫圖，不需要中間層。SQL 和 Pandas 是互補而非取代關係。
