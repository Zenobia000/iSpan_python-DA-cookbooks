# S5 講師講稿 — 視覺化精華：5 種必懂圖

> 對應 notebook：`M4_Matplotlib_Seaborn_Basic/S5_visualization_essentials.ipynb`
> 節次時長：120 分鐘（講授 70 + 練習 40 + 收斂 10）

---

## 1. 本節目標

1. 理解「5 種圖涵蓋 90% 的 DA 場景」的選圖思維：趨勢 / 比較 / 關聯 / 分布 / 矩陣。
2. 能用 seaborn 一行畫出可交付的折線、長條、散佈、箱型、熱力圖。
3. 學會 `plt.subplots` 把多張圖組成儀表板，輸出 Q4 Sales Dashboard 成品。
4. 掌握 matplotlib 與 seaborn 的分工：seaborn 打底、matplotlib 微調。
5. 能將 S4 算出的洞察（月度、地區、品類）完整視覺化並輸出簡報級畫面。

## 2. 時間切分表

| 時間 | 內容 | 備註 |
|---|---|---|
| 0~10 | 為什麼「數字不會說話、圖會」+ 5 圖選擇依據 | 先秀對比：表格 vs lineplot |
| 10~20 | 環境設定、`sns.set_theme`、中文字型提醒 | 示範 `axes.unicode_minus=False` |
| 20~30 | 圖 1 折線圖：月度趨勢 | 強調 `marker='o'` 可讀性 |
| 30~40 | 圖 2 長條圖：排序 + 數字標註 | 示範 `sort_values` 與 `plt.text` |
| 40~50 | 圖 3 散佈圖：`hue` 上色、legend 外移 | 帶到 alpha、s 參數 |
| 50~60 | 圖 4 箱型圖：解讀中位數/四分位/離群 | 這是學員最不熟的圖 |
| 60~70 | 圖 5 熱力圖：`annot=True`、`fmt=',.0f'` | 導入「矩陣型」視覺 |
| 70~85 | 實務 Case：2x3 儀表板整合 | 用 `axes[i, j]` 定位 |
| 85~115 | 課堂練習（含 Electronics 迷你儀表板） | 強調「能放進履歷」 |
| 115~120 | 小結 + S6 預告（靜態 → 互動） | |

## 3. 關鍵教學點

- **選圖依據（務必背下來）**：
  - 想看「隨時間變化」→ 折線圖
  - 想看「誰比誰大」→ 長條圖（記得排序）
  - 想看「兩個數值是否相關」→ 散佈圖
  - 想看「單一數值的分布與離群值」→ 箱型/直方圖
  - 想看「兩個類別交叉的數值」→ 熱力圖
- **seaborn 0.13+ 的 palette 警告**：直接對 `barplot(x, y, palette=...)` 上色會出 `FutureWarning: Passing palette without assigning hue is deprecated`。正確寫法是 `hue='region', legend=False` 一併加上。
- **`plt.subplots` 的 axes 索引**：`nrows=2, ncols=3` → `axes[0,1]`；務必提醒「只有一個 row 或 col 時 axes 是一維」。
- **tight_layout vs constrained_layout**：多圖儀表板推 `tight_layout()`，若標籤撞到則改 `constrained_layout=True`。

## 4. 學員常犯錯誤

1. **seaborn 0.13+ 的 palette 警告**：`sns.barplot(..., palette='viridis')` 沒加 `hue` 會觸發警告。解法是 `hue='region', legend=False`。
2. **中文字型亂碼**：沒裝字型就用中文 title，圖上出現方框。建議先把 title 寫英文，或引導學員設定 `plt.rcParams['font.sans-serif']`。
3. **長條圖忘了排序**：直接 `groupby().sum()` 後畫圖，x 軸順序是按字母而非金額，老闆看不懂誰第一名。
4. **`axes[0, 1]` 寫成 `axes[0][1]`**：兩者其實都可用，但不統一會造成 debug 困擾。
5. **在 loop 裡忘了 `plt.figure()`**：上一張圖被蓋掉或疊在同一張畫布。
6. **存檔後圖是空的**：`plt.show()` 在 `plt.savefig()` 之前執行會清空 figure，要求順序：`savefig → show`。

## 5. 提問設計

1. 「老闆要看『哪一個地區最強』，你會選長條圖還是圓餅圖？為什麼？」
2. 「箱型圖上方那些零散的點代表什麼？你會把它們丟掉還是留下？」
3. 「如果同一張儀表板要同時顯示趨勢與比較，你會怎麼排版這 6 張圖？」

## 6. 延伸資源

- Seaborn 官方 gallery（搜尋 "seaborn example gallery"），裡面的每一張圖都有對應程式碼。
- 書籍：《Storytelling with Data》by Cole Nussbaumer Knaflic，談 DA 視覺化選圖與排版。

## 7. 常見 Q&A

- **Q：matplotlib 和 seaborn 到底該選哪個？**
  A：先用 seaborn 一行搞定 90% 場景，需要極度客製（座標軸、雙 y 軸、annotation）才轉 matplotlib。
- **Q：為什麼我的 `sns.heatmap` 數字跑出科學記號？**
  A：用 `fmt=',.0f'` 指定整數千分位格式。
- **Q：圖太擠、標籤重疊怎麼辦？**
  A：`plt.xticks(rotation=45)` + `plt.tight_layout()`，或 figsize 拉大。

## 8. 收斂金句

「能把 5 張圖畫對，你就比 80% 的文組 Excel 使用者更專業。S6 我們再加一層『互動』，讓老闆能自己點、自己篩。」
